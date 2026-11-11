"""Small replaceable normalizer; originals, normalized events and derivatives stay distinct."""

import hashlib
import json
from typing import Protocol, cast

from pydantic import Field

from bot_trader.core.events import (
    Digest,
    ImmutableV2,
    MarketEventV2,
    canonical_bytes,
    content_hash,
)
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.storage import ArtifactStore


def _object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _no_float(value: str) -> None:
    raise ValueError(
        "Binary JSON numbers/non-finite constants are not admitted; use decimal strings."
    )


def exact_json(data: bytes) -> object:
    return cast(
        object,
        json.loads(
            data, object_pairs_hook=_object, parse_float=_no_float, parse_constant=_no_float
        ),
    )


class NormalizedBatch(ImmutableV2):
    schema_version: int = Field(default=2, strict=True, ge=2, le=2)
    normalizer: str = "fixture-jsonl-v2.1"
    source_manifest_hash: Digest
    raw_sha256: Digest
    events: tuple[MarketEventV2, ...] = Field(min_length=1, max_length=10_000)
    diagnostics: tuple[str, ...] = ()

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


class Normalizer(Protocol):
    def normalize(self, raw: bytes, source: SourceSpec, manifest_hash: str) -> NormalizedBatch: ...


class FixtureJSONLNormalizer:
    """Only the declared local fixture schema, no exchange/provider autodetection."""

    def normalize(self, raw: bytes, source: SourceSpec, manifest_hash: str) -> NormalizedBatch:
        digest = hashlib.sha256(raw).hexdigest()
        if digest != source.raw_sha256 or len(raw) != source.size_bytes:
            raise ValueError("Normalization source integrity mismatch.")
        if source.source_schema != "fixture-jsonl-v2" or source.data_class != "synthetic":
            raise ValueError("This adapter admits only the declared synthetic fixture schema.")
        rows = raw.splitlines()
        if not 1 <= len(rows) <= 10_000:
            raise ValueError("Technical event count must be between one and10000.")
        events = []
        identities: dict[tuple[str, str, str], str] = {}
        sequences: dict[tuple[str, str, int], str] = {}
        diagnostics = []
        for index, row in enumerate(rows):
            payload = exact_json(row)
            if not isinstance(payload, dict) or "raw_sha256" in payload:
                raise ValueError(
                    "Raw rows must be objects; source hash is attached by normalization."
                )
            event = MarketEventV2.model_validate({**payload, "raw_sha256": digest})
            if (event.source_id, event.source_version) != (source.source_id, source.source_version):
                raise ValueError("Event source differs from the archived declaration.")
            if event.identity in identities:
                if identities[event.identity] != event.digest:
                    raise ValueError("Conflicting duplicate event identity.")
                diagnostics.append(f"identical_duplicate:{index}:{event.event_id}")
            sequence_key = (event.source_id, event.stream_id, event.sequence)
            if sequence_key in sequences and sequences[sequence_key] != event.event_id:
                raise ValueError("Different events share a source sequence.")
            identities[event.identity] = event.digest
            sequences[sequence_key] = event.event_id
            if events and event.effective_ns < events[-1].effective_ns:
                diagnostics.append(f"raw_availability_disorder:{index}")
            events.append(event)
        return NormalizedBatch(
            source_manifest_hash=manifest_hash,
            raw_sha256=digest,
            events=tuple(events),
            diagnostics=tuple(diagnostics),
        )


def store_normalized(batch: NormalizedBatch, store: ArtifactStore) -> str:
    return store.put(canonical_bytes(batch.model_dump(mode="json")), "json")
