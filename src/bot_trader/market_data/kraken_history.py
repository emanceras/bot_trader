"""Bounded, private normalization of the explicitly versioned Kraken quarterly CSVs.

No provider autodetection, quotes, strategy or execution. Fractional source seconds
remain verbatim in a private sidecar; v2 carries their exact integer ns equivalent.
"""

from __future__ import annotations

import csv
import hashlib
import re
import stat
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Literal
from zipfile import ZipFile

from pydantic import Field, model_validator

from bot_trader.core.contracts import Currency, Identifier
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import (
    BarData,
    Digest,
    ImmutableV2,
    MarketEventV2,
    Nanoseconds,
    TradeData,
    content_hash,
    exact_ns,
)
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.normalization import NormalizedBatch

TRADE_COLUMNS = ("timestamp", "price", "volume", "type", "order_type", "misc", "trade_id")
TRADE_SCHEMA = "kraken-trades-csv-v2"
BAR_SCHEMA = "kraken-ohlcvt-csv-v1"
MAX_SLICE_BYTES = 2 * 1024 * 1024


def seconds_to_ns(text: str) -> int:
    """Exact decimal seconds, independent of ambient Decimal context or binary floats."""
    if not isinstance(text, str) or len(text) > 64 or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", text):
        raise ValueError("Timestamp must be a finite unsigned decimal-seconds string.")
    number = Decimal(text)
    sign, digits, exponent = number.as_tuple()
    if not isinstance(exponent, int):
        raise ValueError("Invalid timestamp exponent.")
    coefficient = int("".join(map(str, digits)))
    shift = exponent + 9
    if shift >= 0:
        result = coefficient * 10**shift
    else:
        result, remainder = divmod(coefficient, 10**-shift)
        if remainder:
            raise ValueError("Timestamp would lose subnanosecond precision.")
    return exact_ns(result)


def _identity(path: Path) -> tuple[int, int, int, int, int]:
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Archive path cannot contain symlinks.")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("Archive must be a regular file.")
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


class VerifiedArchive(ImmutableV2):
    schema_version: Literal[1] = 1
    sha256: Digest
    size_bytes: int = Field(strict=True, gt=0)
    file_identity: tuple[int, int, int, int, int]


def verify_archive(path: Path, *, expected_sha256: str, expected_size: int) -> VerifiedArchive:
    """Read the existing compressed body once with a 4 MiB buffer; never acquire it."""
    before = _identity(path)
    if before[2] != expected_size:
        raise ValueError("Existing archive size differs from the acquisition receipt.")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(4 * 1024 * 1024):
            digest.update(chunk)
    if before != _identity(path) or digest.hexdigest() != expected_sha256:
        raise ValueError("Existing archive changed or differs from its acquisition receipt.")
    return VerifiedArchive(sha256=digest.hexdigest(), size_bytes=expected_size, file_identity=before)


class KrakenSelection(ImmutableV2):
    schema_version: Literal[1] = 1
    selection: Literal["member-first-data-rows-v1"] = "member-first-data-rows-v1"
    archive_sha256: Digest
    archive_size_bytes: int = Field(strict=True, gt=0)
    member: str
    member_size_bytes: int = Field(strict=True, gt=0)
    member_crc32: int = Field(strict=True, ge=0, le=2**32 - 1)
    readme_sha256: Digest
    source_schema: Literal["kraken-trades-csv-v2", "kraken-ohlcvt-csv-v1"]
    instrument: Identifier
    base_currency: Currency
    quote_currency: Currency
    interval_seconds: int | None = Field(default=None, strict=True, gt=0)
    rows: int = Field(strict=True, ge=1, le=10_000)
    raw_sha256: Digest
    size_bytes: int = Field(strict=True, gt=0, le=MAX_SLICE_BYTES)
    first_data_row: Literal[1] = 1
    whole_member_crc_verified: Literal[False] = False

    @model_validator(mode="after")
    def schema_matches(self) -> KrakenSelection:
        path = PurePosixPath(self.member)
        if path.name != self.member or path.suffix != ".csv":
            raise ValueError("Only a declared top-level CSV member is admitted.")
        if self.source_schema == BAR_SCHEMA:
            if self.interval_seconds is None or self.interval_seconds % 60:
                raise ValueError("OHLCVT requires an explicit whole-minute interval.")
            expected = f"{self.instrument}_{self.interval_seconds // 60}.csv"
        else:
            if self.interval_seconds is not None:
                raise ValueError("Trade CSV has no bar interval.")
            expected = f"{self.instrument}.csv"
        if self.member != expected:
            raise ValueError("Member name differs from the declared original instrument/interval.")
        return self


def select_prefix(
    path: Path,
    verified: VerifiedArchive,
    *,
    member: str,
    source_schema: Literal["kraken-trades-csv-v2", "kraken-ohlcvt-csv-v1"],
    instrument: str,
    base_currency: str,
    quote_currency: str,
    interval_seconds: int | None = None,
    max_rows: int = 64,
) -> tuple[bytes, KrakenSelection]:
    """Read only the declared prefix, without extracting or importing a full member.

    Repeating selection reconstructs the same prefix. LocalArchive supplies durable
    chunk checkpoints once this bounded private raw object has been selected.
    """
    if type(max_rows) is not int or not 1 <= max_rows <= 10_000:
        raise ValueError("Selection must declare 1 to 10000 source rows.")
    if _identity(path) != verified.file_identity:
        raise ValueError("Archive identity changed after full-body verification.")
    data = bytearray()
    rows = 0
    with ZipFile(path) as archive:
        if archive.namelist().count(member) != 1:
            raise ValueError("CSV member missing or duplicated in archive directory.")
        info = archive.getinfo(member)
        readme = archive.getinfo("README.md")
        if readme.file_size > 65536:
            raise ValueError("Unexpectedly large source schema notice.")
        readme_hash = hashlib.sha256(archive.read(readme)).hexdigest()
        with archive.open(info) as stream:
            if source_schema == TRADE_SCHEMA:
                header = stream.readline(4097)
                if len(header) > 4096:
                    raise ValueError("CSV header exceeds declared bound.")
                data.extend(header)
            for _ in range(max_rows):
                line = stream.readline(4097)
                if not line:
                    break
                if len(line) > 4096 or len(data) + len(line) > MAX_SLICE_BYTES:
                    raise ValueError("CSV record/slice exceeds declared memory bound.")
                if not line.strip():
                    raise ValueError("Blank record inside selected CSV prefix.")
                data.extend(line)
                rows += 1
    if _identity(path) != verified.file_identity:
        raise ValueError("Archive changed during bounded prefix selection.")
    raw = bytes(data)
    selection = KrakenSelection(
        archive_sha256=verified.sha256,
        archive_size_bytes=verified.size_bytes,
        member=member,
        member_size_bytes=info.file_size,
        member_crc32=info.CRC,
        readme_sha256=readme_hash,
        source_schema=source_schema,
        instrument=instrument,
        base_currency=base_currency,
        quote_currency=quote_currency,
        interval_seconds=interval_seconds,
        rows=rows,
        raw_sha256=hashlib.sha256(raw).hexdigest(),
        size_bytes=len(raw),
    )
    return raw, selection


class HistoricalAvailability(ImmutableV2):
    version: Literal["kraken-history-optimistic-v1"] = "kraken-history-optimistic-v1"
    delay_ns: Nanoseconds = 0
    interpretation: Literal["event-or-bar-end-plus-declared-delay"] = (
        "event-or-bar-end-plus-declared-delay"
    )
    optimistic_assumption: Literal[True] = True
    historical_reception_observed: Literal[False] = False


class KrakenRowProvenance(ImmutableV2):
    data_row: int
    physical_line: int
    row_sha256: Digest
    event_id: str
    original_timestamp: str
    original_unit: Literal["fractional_unix_seconds"] = "fractional_unix_seconds"
    v2_tick_interpretation: Literal["exact-derived-nanoseconds"] = "exact-derived-nanoseconds"
    native_trade_id: str | None = None
    side: str | None = None
    order_type: str | None = None
    misc: str | None = None
    trade_count: int | None = None


class KrakenNormalizedSlice(ImmutableV2):
    schema_version: Literal[1] = 1
    selection: KrakenSelection
    availability: HistoricalAvailability
    batch: NormalizedBatch
    rows: tuple[KrakenRowProvenance, ...]
    price_unit: str
    quantity_unit: str
    sequence_origin: Literal["unique-selected-row-ordinal-not-provider-sequence"] = (
        "unique-selected-row-ordinal-not-provider-sequence"
    )


class KrakenHistoricalNormalizer:
    """Implements the existing Normalizer port; metadata absent in v2 stays in a sidecar."""

    def __init__(
        self,
        selection: KrakenSelection,
        availability: HistoricalAvailability | None = None,
    ) -> None:
        self.selection = KrakenSelection.model_validate(selection.model_dump())
        self.availability = availability or HistoricalAvailability()

    def normalize(self, raw: bytes, source: SourceSpec, manifest_hash: str) -> NormalizedBatch:
        return self.normalize_with_provenance(raw, source, manifest_hash).batch

    def normalize_with_provenance(
        self, raw: bytes, source: SourceSpec, manifest_hash: str
    ) -> KrakenNormalizedSlice:
        source = SourceSpec.model_validate(source.model_dump())
        selected = self.selection
        if source.partition != "development":
            raise AccessDenied("Reserved source cannot enter historical technical QA.")
        if source.source_schema != selected.source_schema:
            raise ValueError("Explicit source schema differs from adapter version.")
        if content_hash(source.model_dump(mode="json")) != manifest_hash:
            raise ValueError("Source declaration hash mismatch.")
        digest = hashlib.sha256(raw).hexdigest()
        if (len(raw), digest) != (selected.size_bytes, selected.raw_sha256) or (
            len(raw), digest
        ) != (source.size_bytes, source.raw_sha256):
            raise ValueError("Selected raw bytes no longer match their declared provenance.")
        lines = raw.splitlines(keepends=True)
        header = selected.source_schema == TRADE_SCHEMA
        if header:
            parsed_header = tuple(next(csv.reader([lines[0].decode("utf-8")])))
            if parsed_header != TRADE_COLUMNS:
                raise ValueError("Trade header differs from explicit schema v2; no autodetection.")
            lines = lines[1:]
        if len(lines) != selected.rows:
            raise ValueError("Selected source row count changed.")
        events: list[MarketEventV2] = []
        provenance: list[KrakenRowProvenance] = []
        identities: dict[str, tuple[tuple[str, ...], MarketEventV2]] = {}
        diagnostics = [
            "availability_is_optimistic_assumption_not_historical_reception",
            "adapter_ordinal_is_not_provider_sequence",
            "timestamp_lexeme_and_source_units_preserved_in_private_sidecar",
        ]
        previous_ns: int | None = None
        previous_id: int | None = None
        for index, raw_line in enumerate(lines, start=1):
            fields = tuple(next(csv.reader([raw_line.decode("utf-8")])))
            if len(fields) != 7:
                raise ValueError(f"Unexpected CSV field count at data row {index}.")
            timestamp = seconds_to_ns(fields[0])
            native_id = side = order_type = misc = None
            count = None
            payload: TradeData | BarData
            if header:
                side, order_type, misc = fields[3:6]
                if side not in ("", "b", "s") or order_type not in ("", "l", "m"):
                    raise ValueError(f"Unsupported trade metadata at data row {index}.")
                native_id = fields[6] or None
                if native_id is not None and not re.fullmatch(r"[0-9]+", native_id):
                    raise ValueError(f"Invalid native trade ID at data row {index}.")
                event_id = (
                    "trade-" + native_id if native_id is not None else
                    f"row-{selected.archive_sha256[:16]}-{index}"
                )
                payload = TradeData(price=fields[1], quantity=fields[2])
                eligible = timestamp
                stream = "trades-" + selected.instrument
                if native_id is None:
                    diagnostics.append(f"missing_native_id:row-{index}")
                elif previous_id is not None and int(native_id) > previous_id + 1:
                    diagnostics.append(f"native_id_gap_not_proven_loss:row-{index}")
                if native_id is not None:
                    if previous_id is not None and int(native_id) < previous_id:
                        diagnostics.append(f"native_id_reversal:row-{index}")
                    previous_id = int(native_id)
            else:
                assert selected.interval_seconds is not None
                interval = selected.interval_seconds * 10**9
                if timestamp % interval:
                    raise ValueError(f"Opening timestamp is not interval aligned at row {index}.")
                if not re.fullmatch(r"[0-9]+", fields[6]) or int(fields[6]) < 1:
                    raise ValueError(f"Invalid populated-bar trade count at row {index}.")
                count = int(fields[6])
                event_id = f"bar-{timestamp}-{interval}"
                payload = BarData(
                    bar_id=event_id, start_ns=timestamp, end_ns=exact_ns(timestamp + interval),
                    status="closed", label="open", open=fields[1], high=fields[2],
                    low=fields[3], close=fields[4], volume=fields[5],
                )
                eligible = payload.end_ns
                stream = f"ohlcvt-{selected.instrument}-{selected.interval_seconds}"
                if previous_ns is not None and timestamp > previous_ns + interval:
                    diagnostics.append(f"sparse_bar_intervals_not_proven_loss:row-{index}")
            if previous_ns is not None and timestamp < previous_ns:
                diagnostics.append(f"source_timestamp_reversal:row-{index}")
            previous_ns = timestamp
            old = identities.get(event_id)
            if old is not None:
                if fields != old[0]:
                    raise ValueError(f"Conflicting native identity at data row {index}.")
                event = old[1]
                diagnostics.append(f"identical_duplicate:row-{index}")
            else:
                event = MarketEventV2(
                    event_id=event_id, source_id=source.source_id,
                    source_version=source.source_version, stream_id=stream,
                    sequence=len(identities) + 1, instrument=selected.instrument,
                    quote_currency=selected.quote_currency,
                    original_tick=timestamp, original_unit="ns", event_ns=timestamp,
                    available_ns=exact_ns(eligible + self.availability.delay_ns),
                    received_ns=None, raw_sha256=digest, data=payload,
                )
                identities[event_id] = fields, event
            events.append(event)
            provenance.append(KrakenRowProvenance(
                data_row=index, physical_line=index + int(header),
                row_sha256=hashlib.sha256(raw_line).hexdigest(), event_id=event.event_id,
                original_timestamp=fields[0], native_trade_id=native_id, side=side,
                order_type=order_type, misc=misc, trade_count=count,
            ))
        return KrakenNormalizedSlice(
            selection=selected, availability=self.availability,
            batch=NormalizedBatch(
                normalizer="kraken-history-v1", source_manifest_hash=manifest_hash,
                raw_sha256=digest, events=tuple(events), diagnostics=tuple(diagnostics),
            ),
            rows=tuple(provenance), price_unit=f"{selected.quote_currency}/{selected.base_currency}",
            quantity_unit=selected.base_currency,
        )
