import hashlib
import json

import pytest

from bot_trader.core.events import canonical_bytes
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.normalization import FixtureJSONLNormalizer, store_normalized
from bot_trader.market_data.storage import MemoryArtifactStore


def row(identity="a", sequence=1, at=100):
    return dict(schema_version=2, event_id=identity, source_id="fixture", source_version="1",
                stream_id="events", sequence=sequence, instrument="SYNTH-USD",
                original_tick=at, original_unit="ns", event_ns=at,
                available_ns=at+1, received_ns=at+2,
                data=dict(kind="trade", price="100.00", quantity="1"))


def normalize(rows, **source_updates):
    raw = b"\n".join(canonical_bytes(r) for r in rows) + b"\n"
    spec = SourceSpec(source_id="fixture", source_version="1", source_schema="fixture-jsonl-v2",
                      locator="internal:normalization-fixture", rights="Internally generated",
                      acquired_ns=1000, raw_sha256=hashlib.sha256(raw).hexdigest(),
                      size_bytes=len(raw), data_class=source_updates.get("data_class", "synthetic"))
    return FixtureJSONLNormalizer().normalize(raw, spec, "a" * 64)


def test_normalization_has_provenance_and_no_silent_sort_or_dedup():
    batch = normalize([row("b", 2, 200), row(), row()])
    assert [e.event_id for e in batch.events] == ["b", "a", "a"]
    assert batch.diagnostics == ("raw_availability_disorder:1", "identical_duplicate:2:a")
    assert batch.events[1].data.price == "100"
    assert batch.events[1].raw_sha256 == batch.raw_sha256
    assert batch.events[1].received_ns == 102
    assert batch.events[1].engine_ts_init_ns is None
    store = MemoryArtifactStore()
    key = store_normalized(batch, store)
    assert key == batch.digest
    assert json.loads(store.get(key, "json"))["source_manifest_hash"] == "a" * 64


def test_normalization_rejects_conflict_and_non_synthetic_source():
    with pytest.raises(ValueError, match="Conflicting duplicate"):
        normalize([row(), row(at=101)])
    with pytest.raises(ValueError, match="source sequence"):
        normalize([row(), row("b")])
    with pytest.raises(ValueError, match="synthetic fixture"):
        normalize([row()], data_class="exposed_structural_only")
    invalid = row()
    invalid["data"]["price"] = 100.1
    with pytest.raises(ValueError, match="Binary JSON"):
        normalize([invalid])
