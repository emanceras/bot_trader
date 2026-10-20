"""Synthetic-only, versioned datasets with availability and reserved-partition gates."""

import hashlib
import json
import random
from datetime import timedelta
from decimal import Decimal, localcontext
from io import BytesIO
from typing import cast

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import JsonValue, ValidationError

from bot_trader.core.contracts import DatasetSpec, MarketBar, Partition, Principal
from bot_trader.core.errors import AccessDenied, PlatformError
from bot_trader.core.security import Policy
from bot_trader.core.settings import Settings
from bot_trader.persistence import DocumentRecord, Repository
from bot_trader.persistence.repository import canonical_json, content_hash

from .storage import ArtifactStore

GENERATOR_VERSION = "synthetic-bars/1"
TRANSFORM_VERSION = "causal-sma/1"


def _generate(spec: DatasetSpec) -> tuple[MarketBar, ...]:
    """Simulated clocks and prices, not historical observations or execution evidence."""
    rng = random.Random(spec.seed)
    previous = 10_000
    bars = []
    try:
        for index in range(spec.rows):
            close = max(500, previous + rng.randint(-80, 80))
            high = max(previous, close) + rng.randint(1, 30)
            low = min(previous, close) - rng.randint(1, 30)
            event_time = spec.start + timedelta(seconds=index * spec.interval_seconds)
            bars.append(
                MarketBar(
                    instrument=spec.instrument,
                    event_time=event_time,
                    published_at=event_time + timedelta(milliseconds=200),
                    provider_available_at=event_time + timedelta(milliseconds=400),
                    received_at=event_time + timedelta(milliseconds=700),
                    open=Decimal(previous) / 100,
                    high=Decimal(high) / 100,
                    low=Decimal(low) / 100,
                    close=Decimal(close) / 100,
                    volume=Decimal(rng.randint(100, 10_000)) / 100,
                    quote_currency="USD",
                    interval_seconds=spec.interval_seconds,
                )
            )
            previous = close
    except OverflowError as error:
        raise PlatformError("invalid_dataset", "Synthetic timestamp range is invalid.") from error
    return tuple(bars)


def _serialize(bars: tuple[MarketBar, ...]) -> bytes:
    timestamp = pa.timestamp("us", tz="UTC")
    schema = pa.schema(
        [
            ("schema_version", pa.int16()),
            ("instrument", pa.string()),
            ("event_time", timestamp),
            ("published_at", timestamp),
            ("provider_available_at", timestamp),
            ("received_at", timestamp),
            ("transformed_at", timestamp),
            *[(name, pa.decimal128(24, 8)) for name in ("open", "high", "low", "close", "volume")],
            ("quote_currency", pa.string()),
            ("interval_seconds", pa.int64()),
        ]
    )
    table = pa.Table.from_pylist([bar.model_dump() for bar in bars], schema=schema)
    buffer = BytesIO()
    pq.write_table(table, buffer, compression="zstd", version="2.6")
    return buffer.getvalue()


def _overlay(bars: tuple[MarketBar, ...], window: int) -> list[dict[str, JsonValue]]:
    if not isinstance(window, int) or isinstance(window, bool) or not 1 <= window <= 500:
        raise PlatformError("invalid_transform", "Window must be an integer from 1 to 500.")
    points: list[dict[str, JsonValue]] = []
    with localcontext() as context:
        context.prec = 28
        for index in range(window - 1, len(bars)):
            observed = bars[index - window + 1 : index + 1]
            available = max(bar.transformed_at or bar.received_at for bar in observed)
            value = sum((bar.close for bar in observed), Decimal(0)) / Decimal(window)
            points.append(
                {
                    "time": int(bars[index].event_time.timestamp()),
                    "value": str(value),
                    "available_at": available.isoformat(),
                    "input_last_event_time": bars[index].event_time.isoformat(),
                }
            )
    return points


class DatasetService:
    def __init__(
        self,
        repo: Repository,
        store: ArtifactStore,
        policy: Policy,
        settings: Settings,
    ) -> None:
        self.repo, self.store, self.policy, self.settings = repo, store, policy, settings

    def _require(
        self,
        principal: Principal,
        action: str,
        *,
        partition: Partition | None = None,
        resource: str = "datasets",
    ) -> None:
        try:
            self.policy.require(principal, action, partition=partition, mode=self.settings.mode)
        except AccessDenied:
            self.repo.append_audit(principal.id, action, resource, "denied")
            raise

    def create(self, spec: DatasetSpec, principal: Principal) -> DocumentRecord:
        self._require(principal, "datasets.create", partition=spec.partition)
        if spec.instrument != "SYNTH-USD" or spec.quote_currency != "USD":
            raise PlatformError(
                "synthetic_only", "Only the SYNTH-USD technical fixture is available."
            )
        if spec.rows > self.settings.max_dataset_rows:
            raise PlatformError("dataset_limit", "Dataset exceeds the configured row limit.")
        bars = _generate(spec)
        payload = _serialize(bars)
        if len(payload) > self.settings.max_artifact_bytes:
            raise PlatformError("artifact_limit", "Dataset exceeds the configured artifact size.")
        digest = self.store.put(payload, "parquet")
        specification = cast(dict[str, JsonValue], spec.model_dump(mode="json"))
        identity = content_hash({"spec": specification, "generator": GENERATOR_VERSION})
        body: dict[str, JsonValue] = {
            "mode": "technical",
            "synthetic": True,
            "partition": spec.partition,
            "spec": specification,
            "generator_version": GENERATOR_VERSION,
            "artifact": {
                "digest": digest,
                "suffix": "parquet",
                "media_type": "application/vnd.apache.parquet",
                "size_bytes": len(payload),
            },
            "source": {
                "id": GENERATOR_VERSION,
                "access_level": "internal",
                "title": "Seeded synthetic fixture; no market history",
                "clock_semantics": "Simulated UTC bar-close and delayed availability clocks",
            },
            "quality": {
                "rows": len(bars),
                "duplicates": 0,
                "missing": 0,
                "ohlc_valid": True,
                "availability_order_valid": True,
                "first_event_time": bars[0].event_time.isoformat(),
                "last_event_time": bars[-1].event_time.isoformat(),
            },
            "schema": {
                "contract": "MarketBar",
                "version": 1,
                "prices": "decimal(24,8)",
                "timestamps": "UTC microseconds",
                "quote_currency": "USD",
            },
        }
        document = self.repo.put("dataset", f"synthetic-{identity[:24]}", body)
        self.repo.append_audit(
            principal.id,
            "datasets.create",
            document.id,
            "recorded",
            {"version": document.version, "content_hash": document.content_hash},
        )
        return document

    def _record(self, id: str, version: int | None = None) -> DocumentRecord:
        document = self.repo.get("dataset", id, version)
        if document.body.get("partition") not in {"development", "validation", "final"}:
            raise PlatformError("invalid_dataset", "Dataset partition is missing or invalid.")
        return document

    @staticmethod
    def _metadata(document: DocumentRecord) -> DocumentRecord:
        if document.body.get("partition") == "final":
            # Seeds, hashes, ranges and quality summaries can disclose reserved payloads.
            return document.model_copy(
                update={
                    "content_hash": "reserved",
                    "body": {
                        "mode": "technical",
                        "synthetic": True,
                        "partition": "final",
                        "payload_access": "reserved",
                    },
                }
            )
        return document

    def get(self, id: str, principal: Principal, version: int | None = None) -> DocumentRecord:
        self._require(principal, "datasets.read", resource=id)
        return self._metadata(self._record(id, version))

    def list(self, principal: Principal, limit: int = 100) -> list[DocumentRecord]:
        self._require(principal, "datasets.read")
        return [self._metadata(document) for document in self.repo.list("dataset", limit=limit)]

    def _payload(
        self,
        id: str,
        principal: Principal,
        version: int | None,
    ) -> tuple[DocumentRecord, bytes]:
        # Resolve stored partition before inspecting any payload descriptor or artifact.
        self._require(principal, "datasets.payload", resource=id)
        document = self._record(id, version)
        partition = cast(Partition, document.body["partition"])
        self._require(principal, "datasets.payload", partition=partition, resource=id)
        if document.body.get("mode") != "technical" or document.body.get("synthetic") is not True:
            raise PlatformError(
                "synthetic_only", "Only synthetic technical datasets are authorized."
            )
        try:
            spec = DatasetSpec.model_validate(document.body.get("spec"))
        except ValidationError as error:
            raise PlatformError("invalid_dataset", "Dataset specification is invalid.") from error
        if spec.partition != partition:
            raise PlatformError(
                "invalid_dataset", "Dataset partition differs from its specification."
            )
        artifact = document.body.get("artifact")
        if not isinstance(artifact, dict) or artifact.get("suffix") != "parquet":
            raise PlatformError("invalid_dataset", "Dataset artifact descriptor is invalid.")
        digest = artifact.get("digest")
        if not isinstance(digest, str):
            raise PlatformError("invalid_dataset", "Dataset artifact digest is invalid.")
        payload = self.store.get(digest, "parquet")
        if len(payload) > self.settings.max_artifact_bytes or len(payload) != artifact.get(
            "size_bytes"
        ):
            raise PlatformError(
                "artifact_limit", "Dataset artifact size does not match its manifest."
            )
        return document, payload

    def bars(
        self,
        id: str,
        principal: Principal,
        version: int | None = None,
    ) -> tuple[MarketBar, ...]:
        document, payload = self._payload(id, principal, version)
        try:
            metadata = pq.read_metadata(BytesIO(payload))
            if not 2 <= metadata.num_rows <= self.settings.max_dataset_rows:
                raise PlatformError(
                    "dataset_limit", "Stored dataset exceeds the configured row limit."
                )
            table = pq.read_table(BytesIO(payload))
            bars = tuple(MarketBar.model_validate(row) for row in table.to_pylist())
            spec = DatasetSpec.model_validate(document.body.get("spec"))
        except (pa.ArrowException, ValidationError) as error:
            raise PlatformError("invalid_dataset", "Stored dataset schema is invalid.") from error
        if len(bars) != spec.rows or spec.instrument != "SYNTH-USD" or spec.quote_currency != "USD":
            raise PlatformError(
                "invalid_dataset", "Stored dataset does not match its specification."
            )
        for index, bar in enumerate(bars):
            if (
                bar.instrument != spec.instrument
                or bar.quote_currency != spec.quote_currency
                or bar.interval_seconds != spec.interval_seconds
                or bar.event_time != spec.start + timedelta(seconds=index * spec.interval_seconds)
            ):
                raise PlatformError(
                    "invalid_dataset", "Stored dataset identity or clock is invalid."
                )
        return bars

    def series(
        self,
        id: str,
        principal: Principal,
        version: int | None = None,
        window: int = 5,
    ) -> dict[str, JsonValue]:
        bars = self.bars(id, principal, version)
        document = self._record(id, version)
        points = _overlay(bars, window)
        return {
            "dataset_id": id,
            "dataset_version": document.version,
            "synthetic": True,
            "mode": "technical",
            "quote_currency": "USD",
            "candles": [
                {
                    "time": int(bar.event_time.timestamp()),
                    "open": float(bar.open),
                    "high": float(bar.high),
                    "low": float(bar.low),
                    "close": float(bar.close),
                }
                for bar in bars
            ],
            "volume": [
                {"time": int(bar.event_time.timestamp()), "value": float(bar.volume)}
                for bar in bars
            ],
            "overlay": [
                {
                    "time": point["time"],
                    "value": float(str(point["value"])),
                    "available_at": point["available_at"],
                }
                for point in points
            ],
            "transform": {
                "name": "causal_sma",
                "version": TRANSFORM_VERSION,
                "window": window,
                "input_content_hash": document.content_hash,
            },
            "display_only": "Chart floats are not accounting values; fixture clocks are simulated.",
        }

    def inspect(
        self,
        id: str,
        principal: Principal,
        version: int | None = None,
    ) -> dict[str, JsonValue]:
        bars = self.bars(id, principal, version)
        # Registered Arrow input has already passed checksum, schema, row and authorization gates.
        table = pa.table(
            {"close": [bar.close for bar in bars], "volume": [bar.volume for bar in bars]}
        )
        with duckdb.connect(
            ":memory:",
            config={
                "enable_external_access": "false",
                "autoinstall_known_extensions": "false",
                "autoload_known_extensions": "false",
                "threads": "1",
                "memory_limit": "64MB",
            },
        ) as query:
            query.register("verified_fixture", table)
            row = query.execute(
                "SELECT count(*), min(close), max(close), sum(volume) FROM verified_fixture"
            ).fetchone()
        assert row is not None
        return {
            "rows": int(row[0]),
            "minimum_close": str(row[1]),
            "maximum_close": str(row[2]),
            "total_volume": str(row[3]),
            "synthetic": True,
            "mode": "technical",
            "query_version": "bounded-quality/1",
            "quote_currency": "USD",
        }

    def transform(
        self,
        id: str,
        principal: Principal,
        version: int | None = None,
        window: int = 5,
    ) -> DocumentRecord:
        bars = self.bars(id, principal, version)
        self._require(principal, "datasets.create", resource=id)
        document = self._record(id, version)
        points = _overlay(bars, window)
        output: dict[str, JsonValue] = {
            "mode": "technical",
            "synthetic": True,
            "name": "causal_sma",
            "version": TRANSFORM_VERSION,
            "window": window,
            "points": cast(JsonValue, points),
            "input_dataset": {
                "id": id,
                "version": document.version,
                "content_hash": document.content_hash,
            },
        }
        data = canonical_json(output).encode()
        digest = self.store.put(data, "json")
        body: dict[str, JsonValue] = {
            "mode": "technical",
            "synthetic": True,
            "partition": document.body["partition"],
            "algorithm": TRANSFORM_VERSION,
            "parameters": {"window": window},
            "input_dataset": output["input_dataset"],
            "artifact": {
                "digest": digest,
                "suffix": "json",
                "media_type": "application/json",
                "size_bytes": len(data),
            },
            "availability_policy": "Trailing window only; latest input reception/transformation",
        }
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:24]
        result = self.repo.put("transform", f"sma-{key}", body)
        self.repo.append_audit(
            principal.id,
            "datasets.transform",
            id,
            "recorded",
            {"transform_id": result.id, "version": result.version},
        )
        return result
