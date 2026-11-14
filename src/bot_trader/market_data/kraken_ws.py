"""Exact public Kraken v2 decoding; no network client, orders or strategy interface."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

from pydantic import Field

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import (
    Digest,
    ImmutableV2,
    Level,
    MarketEventV2,
    Nanoseconds,
    QuoteData,
    TradeData,
    content_hash,
    datetime_ns,
    decimal_text,
    exact_ns,
)
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.normalization import NormalizedBatch
from bot_trader.market_data.storage import ArtifactStore

SYMBOL: Literal["BTC/EUR"] = "BTC/EUR"
INSTRUMENT = "BTC-EUR"
SCHEMA = "kraken-ws-v2-capture-v1"
MAPPING = "kraken-symbol-map-v1:BTC/EUR=BTC-EUR;quote=EUR;base=BTC"


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key in public frame.")
        result[key] = value
    return result


def _constant(_: str) -> None:
    raise ValueError("Non-finite JSON number in public frame.")


def exact_ws_json(raw: bytes) -> dict[str, Any]:
    return _exact_json_object(raw, 1_048_576)


def _exact_json_object(raw: bytes, max_bytes: int) -> dict[str, Any]:
    if not isinstance(raw, bytes) or not 0 < len(raw) <= max_bytes:
        raise ValueError("JSON object must be nonempty bytes within its declared bound.")
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_pairs,
            parse_float=Decimal,
            parse_constant=_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("Malformed or excessively nested public JSON frame.") from error
    if not isinstance(value, dict):
        raise ValueError("Kraken v2 public frame must be an object.")
    return value


def rfc3339_ns(value: object) -> int:
    if not isinstance(value, str):
        raise ValueError("RFC3339 event timestamp must be a string.")
    match = re.fullmatch(
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})",
        value,
    )
    if match is None:
        raise ValueError("Unsupported RFC3339 syntax or precision beyond nanoseconds.")
    base, fraction, zone = match.groups()
    if zone != "Z" and (int(zone[1:3]) > 23 or int(zone[4:6]) > 59 or zone == "-00:00"):
        raise ValueError("RFC3339 offset is invalid or denotes an unknown local offset.")
    seconds = datetime_ns(datetime.fromisoformat(base + ("+00:00" if zone == "Z" else zone)))
    return exact_ns(seconds + int((fraction or "").ljust(9, "0")))


def _number(value: object) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError("Market numbers require exact decimal input, never binary floats.")
    text = str(value)
    if len(text) > 128:
        raise ValueError("Market numeric representation exceeds the admitted bound.")
    try:
        number = Decimal(text)
    except InvalidOperation as error:
        raise ValueError("Invalid market decimal.") from error
    exponent = number.as_tuple().exponent
    if not number.is_finite() or not isinstance(exponent, int) or abs(exponent) > 1000:
        raise ValueError("Market number is non-finite or has an unsupported exponent.")
    return decimal_text(text, positive=True)


def _market_rows(value: dict[str, Any]) -> list[dict[str, Any]]:
    if value.get("channel") not in ("trade", "ticker") or value.get("type") not in (
        "snapshot",
        "update",
    ):
        raise ValueError("Only declared trade/ticker snapshot/update schemas are admitted.")
    rows = value.get("data")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 1000:
        raise ValueError("Market data requires a bounded nonempty list.")
    for row in rows:
        if not isinstance(row, dict) or row.get("symbol") != SYMBOL:
            raise ValueError("Unexpected or ambiguous public-market symbol.")
    if value["channel"] == "ticker" and len(rows) != 1:
        raise ValueError("Single-market ticker frame must contain exactly one observation.")
    return rows


@dataclass(frozen=True)
class ProtocolResult:
    kind: Literal["control", "market"]
    channel: str
    ready: bool
    diagnostics: tuple[str, ...] = ()


class KrakenProtocol:
    """Per-connection public handshake; original wire responses are archived separately."""

    def __init__(self, symbol: str = SYMBOL) -> None:
        if symbol != SYMBOL:
            raise ValueError("This version admits only the explicit BTC/EUR mapping.")
        self.instrument_online = False
        self._instrument: dict[str, Any] | None = None
        self.acknowledged: set[str] = set()

    @property
    def preflight_ready(self) -> bool:
        return self.instrument_online and "instrument" in self.acknowledged

    @property
    def ready(self) -> bool:
        return self.preflight_ready and {"trade", "ticker"}.issubset(self.acknowledged)

    @staticmethod
    def preflight_request() -> dict[str, Any]:
        return {
            "method": "subscribe",
            "params": {"channel": "instrument", "snapshot": True},
            "req_id": 1,
        }

    @classmethod
    def requests_for_preflight(cls) -> tuple[dict[str, Any], ...]:
        return (cls.preflight_request(),)

    def market_requests(self) -> tuple[dict[str, Any], ...]:
        if not self.preflight_ready:
            raise ValueError(
                "Instrument metadata and subscription acknowledgement are required first."
            )
        return (
            {
                "method": "subscribe",
                "params": {"channel": "trade", "symbol": [SYMBOL], "snapshot": True},
                "req_id": 2,
            },
            {
                "method": "subscribe",
                "params": {
                    "channel": "ticker",
                    "symbol": [SYMBOL],
                    "event_trigger": "bbo",
                    "snapshot": True,
                },
                "req_id": 3,
            },
        )

    def accept(self, raw: bytes) -> ProtocolResult:
        value = exact_ws_json(raw)
        diagnostics: list[str] = []
        method = value.get("method")
        if method is not None:
            if method == "pong":
                return ProtocolResult("control", "pong", self.ready)
            if method != "subscribe" or value.get("success") is not True:
                raise ValueError("Unexpected method or rejected public subscription.")
            result = value.get("result")
            if not isinstance(result, dict):
                raise ValueError("Subscription acknowledgement lacks a result object.")
            channel = result.get("channel")
            expected = {"instrument": 1, "trade": 2, "ticker": 3}
            if (
                channel not in expected
                or type(value.get("req_id")) is not int
                or value["req_id"] != expected[channel]
            ):
                raise ValueError("Subscription acknowledgement does not match the public request.")
            if channel in ("trade", "ticker"):
                if not self.preflight_ready or result.get("symbol") != SYMBOL:
                    raise ValueError(
                        "Market acknowledgement lacks the admitted instrument context."
                    )
            if result.get("snapshot") is not True:
                raise ValueError("Snapshot acknowledgement does not match the public request.")
            if channel == "ticker":
                if "event_trigger" in result and result["event_trigger"] != "bbo":
                    raise ValueError("Ticker acknowledgement reports a different trigger.")
                if "event_trigger" not in result:
                    diagnostics.append("bbo_requested_but_not_echoed_by_documented_subscribe_ack")
            self.acknowledged.add(channel)
            return ProtocolResult("control", channel, self.ready, tuple(diagnostics))
        channel = value.get("channel")
        if channel == "heartbeat":
            return ProtocolResult("control", "heartbeat", self.ready)
        if channel == "status":
            rows = value.get("data")
            if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
                raise ValueError("Invalid status schema.")
            if rows[0].get("system") != "online":
                raise ValueError("Public service is not online.")
            return ProtocolResult("control", "status", self.ready)
        if channel == "instrument":
            if value.get("type") not in ("snapshot", "update") or not isinstance(
                value.get("data"), dict
            ):
                raise ValueError("Invalid instrument schema.")
            data = value["data"]
            pairs = data.get("pairs")
            if (
                value["type"] == "update"
                and "pairs" not in data
                and isinstance(data.get("assets"), list)
            ):
                return ProtocolResult("control", "instrument", self.ready)
            if not isinstance(pairs, list):
                raise ValueError("Instrument message has no pair list.")
            selected = [p for p in pairs if isinstance(p, dict) and p.get("symbol") == SYMBOL]
            if not selected and value["type"] == "update":
                return ProtocolResult("control", "instrument", self.ready)
            if len(selected) != 1:
                raise ValueError("Requested v2 instrument is absent or ambiguous.")
            pair = selected[0]
            if value["type"] == "update":
                if self._instrument is None:
                    raise ValueError("Instrument update cannot replace the initial full snapshot.")
                # A sparse update changes only present fields. Raw frames retain all
                # metadata; omitted identity/status never silently become missing.
                pair = self._instrument | pair
            if (pair.get("base"), pair.get("quote"), pair.get("status")) != (
                "BTC",
                "EUR",
                "online",
            ):
                self.instrument_online = False
                self._instrument = None
                raise ValueError("Requested v2 instrument has incompatible identity or status.")
            self._instrument = dict(pair)
            self.instrument_online = True
            return ProtocolResult("control", "instrument", self.ready)
        if channel in ("trade", "ticker"):
            if not self.preflight_ready or channel not in self.acknowledged:
                raise ValueError(
                    "Market frame arrived before its admitted channel handshake completed."
                )
            _market_rows(value)
            return ProtocolResult("market", channel, self.ready)
        raise ValueError("Unrecognized public frame schema; raw bytes remain the evidence.")


class FrameReference(ImmutableV2):
    capture_id: str
    session_id: str
    local_sequence: int = Field(strict=True, ge=1)
    raw_sha256: Digest
    received_ns: Nanoseconds
    monotonic_ns: Nanoseconds
    config_hash: Digest
    source_id: str
    source_version: str

    @classmethod
    def from_record(cls, record: object) -> FrameReference:
        if isinstance(record, dict):
            data = {name: record[name] for name in cls.model_fields}
        else:
            data = {name: getattr(record, name) for name in cls.model_fields}
        return cls.model_validate(data)


class WSRowProvenance(ImmutableV2):
    frame_sequence: int
    session_id: str
    raw_sha256: Digest
    item_index: int
    original_symbol: Literal["BTC/EUR"] = SYMBOL
    mapping_version: Literal["kraken-symbol-map-v1"] = "kraken-symbol-map-v1"
    timestamp_text: str
    timestamp_unit: Literal["RFC3339"] = "RFC3339"
    received_ns: Nanoseconds
    monotonic_ns: Nanoseconds
    native_trade_id: str | None = None
    event_id: str
    duplicate_delivery: bool = False
    snapshot: bool


class WSCaptureNormalization(ImmutableV2):
    version: Literal["kraken-ws-v2-normalizer-v1"] = "kraken-ws-v2-normalizer-v1"
    events: tuple[MarketEventV2, ...]
    batch: NormalizedBatch | None
    rows: tuple[WSRowProvenance, ...]
    diagnostics: tuple[str, ...]


class KrakenWSNormalizer:
    """Existing normalizer port over a frame-manifest with raw blobs in ArtifactStore."""

    def __init__(
        self, store: ArtifactStore, *, symbol: str = SYMBOL, synthetic: bool = True
    ) -> None:
        if symbol != SYMBOL or type(synthetic) is not bool:
            raise ValueError(
                "Only the explicit BTC/EUR mapping and a declared data class are admitted."
            )
        self.store = store
        self.synthetic = synthetic

    def normalize_frames(
        self,
        frames: Sequence[object],
        source_manifest_hash: str,
        *,
        manifest_raw_hash: str | None = None,
    ) -> WSCaptureNormalization:
        if len(frames) > 10_000:
            raise ValueError("Capture normalization requires a bounded frame prefix.")
        references = [FrameReference.from_record(frame) for frame in frames]
        raw_digest = manifest_raw_hash or content_hash(
            [f.model_dump(mode="json") for f in references]
        )
        events: list[MarketEventV2] = []
        sidecars: list[WSRowProvenance] = []
        diagnostics = [MAPPING, "ticker_bbo_is_not_complete_order_flow_or_upstream_gap_proof"]
        identities: dict[str, tuple[str, MarketEventV2]] = {}
        sequences = {"trade": 0, "ticker": 0}
        last_sequence = 0
        last_receipt = 0
        last_monotonic: dict[str, int] = {}
        capture_id = config_hash = None
        prior_trade_id: int | None = None
        protocol = KrakenProtocol()
        session_id: str | None = None
        visited_sessions: set[str] = set()
        for reference in references:
            if reference.source_id != "kraken-ws-v2" or reference.source_version != "1":
                raise ValueError("Frame source does not match the versioned Kraken adapter.")
            if capture_id is None:
                capture_id, config_hash = reference.capture_id, reference.config_hash
            if (capture_id, config_hash) != (reference.capture_id, reference.config_hash):
                raise ValueError("Capture/config identity changed within normalization.")
            if reference.local_sequence <= last_sequence or reference.received_ns < last_receipt:
                raise ValueError("Capture frame ordinal or UTC receipt order reversed.")
            if reference.monotonic_ns < last_monotonic.get(reference.session_id, 0):
                raise ValueError("Monotonic receipt clock reversed within a session.")
            last_sequence, last_receipt = reference.local_sequence, reference.received_ns
            last_monotonic[reference.session_id] = reference.monotonic_ns
            raw = self.store.get(reference.raw_sha256, "bin")
            if hashlib.sha256(raw).hexdigest() != reference.raw_sha256:
                raise ValueError("Captured frame content hash mismatch.")
            if reference.session_id != session_id:
                if reference.session_id in visited_sessions:
                    raise ValueError(
                        "A closed connection session cannot resume without a new identity."
                    )
                session_id = reference.session_id
                visited_sessions.add(session_id)
                protocol = KrakenProtocol()
            admitted = protocol.accept(raw)
            diagnostics.extend(admitted.diagnostics)
            if admitted.kind == "control":
                diagnostics.append(f"control_frame_retained:{reference.local_sequence}")
                continue
            value = exact_ws_json(raw)
            channel = admitted.channel
            for index, row in enumerate(_market_rows(value)):
                if len(sidecars) >= 10_000:
                    raise ValueError(
                        "Market-row count exceeds the bounded normalization admission."
                    )
                timestamp_text = row.get("timestamp")
                event_ns = rfc3339_ns(timestamp_text)
                assert isinstance(timestamp_text, str)  # validated by the exact parser
                if event_ns > reference.received_ns:
                    raise ValueError(
                        "Exchange timestamp follows receipt; clock skew cannot be clamped."
                    )
                native_id = None
                payload: TradeData | QuoteData
                semantic: dict[str, Any]
                if channel == "trade":
                    trade_id = row.get("trade_id")
                    if type(trade_id) is not int or not 0 <= trade_id < 2**64:
                        raise ValueError("Native trade identity must be an exact unsigned integer.")
                    native_id = str(trade_id)
                    if row.get("side") not in ("buy", "sell") or row.get("ord_type") not in (
                        "limit",
                        "market",
                    ):
                        raise ValueError("Trade side/order type differs from admitted v2 schema.")
                    payload = TradeData(
                        price=_number(row.get("price")), quantity=_number(row.get("qty"))
                    )
                    event_id = "trade-" + native_id
                    semantic = {
                        "time": event_ns,
                        "symbol": SYMBOL,
                        "side": row["side"],
                        "ord_type": row["ord_type"],
                        "payload": payload.model_dump(mode="json"),
                    }
                else:
                    payload = QuoteData(
                        origin="synthetic_explicit" if self.synthetic else "observed",
                        bids=(
                            Level(
                                price=_number(row.get("bid")), quantity=_number(row.get("bid_qty"))
                            ),
                        ),
                        asks=(
                            Level(
                                price=_number(row.get("ask")), quantity=_number(row.get("ask_qty"))
                            ),
                        ),
                    )
                    event_id = "ticker-" + content_hash(
                        {"capture": capture_id, "frame": reference.local_sequence}
                    )
                    semantic = {"frame": reference.local_sequence}
                signature = content_hash(semantic)
                previous = identities.get(event_id)
                duplicate = previous is not None
                if previous is not None:
                    if previous[0] != signature:
                        raise ValueError(
                            "Repeated native trade ID has conflicting semantic content."
                        )
                    event = previous[1]
                    diagnostics.append(
                        f"duplicate_trade_delivery:{reference.local_sequence}:{index}"
                    )
                else:
                    sequences[channel] += 1
                    event = MarketEventV2(
                        event_id=event_id,
                        source_id=reference.source_id,
                        source_version=reference.source_version,
                        stream_id=channel + "-BTC-EUR",
                        sequence=sequences[channel],
                        instrument=INSTRUMENT,
                        quote_currency="EUR",
                        original_tick=event_ns,
                        original_unit="ns",
                        event_ns=event_ns,
                        available_ns=reference.received_ns,
                        received_ns=reference.received_ns,
                        raw_sha256=reference.raw_sha256,
                        data=payload,
                    )
                    identities[event_id] = signature, event
                    events.append(event)
                    if channel == "trade":
                        assert type(trade_id) is int  # validated in the trade branch
                        number = trade_id  # exact integer validated in the trade branch
                        if prior_trade_id is not None and number > prior_trade_id + 1:
                            diagnostics.append(
                                f"native_trade_id_gap_not_proven_loss:{reference.local_sequence}"
                            )
                        if prior_trade_id is not None and number < prior_trade_id:
                            diagnostics.append(
                                f"late_native_trade_not_retroactive:{reference.local_sequence}"
                            )
                        prior_trade_id = (
                            number if prior_trade_id is None else max(prior_trade_id, number)
                        )
                sidecars.append(
                    WSRowProvenance(
                        frame_sequence=reference.local_sequence,
                        session_id=reference.session_id,
                        raw_sha256=reference.raw_sha256,
                        item_index=index,
                        timestamp_text=timestamp_text,
                        received_ns=reference.received_ns,
                        monotonic_ns=reference.monotonic_ns,
                        native_trade_id=native_id,
                        event_id=event.event_id,
                        duplicate_delivery=duplicate,
                        snapshot=value["type"] == "snapshot",
                    )
                )
        if len(events) > 10_000:
            raise ValueError("Normalized event count exceeds the bounded replay admission.")
        batch = (
            None
            if not events
            else NormalizedBatch(
                normalizer="kraken-ws-v2-normalizer-v1",
                source_manifest_hash=source_manifest_hash,
                raw_sha256=raw_digest,
                events=tuple(events),
                diagnostics=tuple(diagnostics),
            )
        )
        return WSCaptureNormalization(
            events=tuple(events), batch=batch, rows=tuple(sidecars), diagnostics=tuple(diagnostics)
        )

    def normalize_with_provenance(
        self, raw: bytes, source: SourceSpec, manifest_hash: str
    ) -> WSCaptureNormalization:
        source = SourceSpec.model_validate(source.model_dump())
        if source.partition != "development":
            raise AccessDenied("Reserved captures cannot enter technical normalization.")
        if (
            source.source_schema != SCHEMA
            or source.source_id != "kraken-ws-v2"
            or source.source_version != "1"
        ):
            raise ValueError("Capture declaration differs from the admitted source/schema.")
        if (source.data_class == "synthetic") != self.synthetic:
            raise ValueError(
                "Declared synthetic/observed data class differs from adapter configuration."
            )
        digest = hashlib.sha256(raw).hexdigest()
        if (digest, len(raw)) != (source.raw_sha256, source.size_bytes) or content_hash(
            source.model_dump(mode="json")
        ) != manifest_hash:
            raise ValueError("Capture manifest identity or source declaration changed.")
        value = _exact_json_object(raw, 10_485_760)
        if (
            type(value.get("schema_version")) is not int
            or value["schema_version"] != 1
            or not isinstance(value.get("capture_id"), str)
            or not value["capture_id"]
            or not isinstance(value.get("frames"), list)
        ):
            raise ValueError("Unknown captured-frame manifest schema.")
        references = [FrameReference.from_record(frame) for frame in value["frames"]]
        if any(frame.capture_id != value.get("capture_id") for frame in references):
            raise ValueError("Manifest capture identity differs from its frame records.")
        return self.normalize_frames(references, manifest_hash, manifest_raw_hash=digest)

    def normalize(self, raw: bytes, source: SourceSpec, manifest_hash: str) -> NormalizedBatch:
        result = self.normalize_with_provenance(raw, source, manifest_hash)
        if result.batch is None:
            raise ValueError(
                "Control-only capture has no nonempty market batch; use provenance result."
            )
        return result.batch
