from copy import deepcopy
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from typing import cast

import pytest
from pydantic import JsonValue

from bot_trader.core.contracts import DatasetSpec, Principal
from bot_trader.core.errors import AccessDenied, NotFound, PlatformError
from bot_trader.core.security import Policy
from bot_trader.core.settings import Settings
from bot_trader.market_data import DatasetService, LocalArtifactStore, MemoryArtifactStore
from bot_trader.persistence import Database, Repository, migrate

ROOT = Path(__file__).resolve().parents[1]
ADMIN = Principal(id="admin", role="admin")
VIEWER = Principal(id="viewer", role="viewer")


@pytest.fixture
def service(tmp_path: Path) -> DatasetService:
    settings = Settings(repository_root=ROOT, data_dir=tmp_path / "state")
    database = Database(settings)
    migrate(database)
    return DatasetService(
        Repository(database),
        LocalArtifactStore(settings.state_path / "artifacts"),
        Policy(),
        settings,
    )


def test_repeatability_provenance_and_memory_substitution(service: DatasetService) -> None:
    spec = DatasetSpec(seed=17, rows=16, interval_seconds=13)
    first = service.create(spec, ADMIN)
    assert service.create(spec, ADMIN) == first
    other_store = MemoryArtifactStore()
    replacement = DatasetService(service.repo, other_store, service.policy, service.settings)
    identical = replacement.create(spec, ADMIN)
    assert identical == first
    assert service.bars(first.id, VIEWER) == replacement.bars(first.id, VIEWER)
    assert service.inspect(first.id, VIEWER) == replacement.inspect(first.id, VIEWER)
    assert first.body["generator_version"] == "synthetic-bars/1"
    assert first.body["synthetic"] is True
    assert service.create(DatasetSpec(seed=18, rows=16, interval_seconds=13), ADMIN).id != first.id
    bars = service.bars(first.id, VIEWER)
    assert all(bar.instrument == "SYNTH-USD" and bar.quote_currency == "USD" for bar in bars)
    assert bars[1].event_time - bars[0].event_time == timedelta(seconds=13)
    assert all(bar.received_at > bar.event_time for bar in bars)
    assert bars[0].received_at - bars[0].event_time == timedelta(milliseconds=700)
    assert bars[0].provider_available_at is not None
    assert bars[0].published_at is not None
    assert bars[0].published_at < bars[0].provider_available_at < bars[0].received_at
    assert service.inspect(first.id, VIEWER)["rows"] == 16


def test_causal_overlay_records_inputs_and_availability(service: DatasetService) -> None:
    dataset = service.create(DatasetSpec(rows=20), ADMIN)
    bars = service.bars(dataset.id, ADMIN)
    series = service.series(dataset.id, VIEWER, window=4)
    points = cast(list[dict[str, JsonValue]], series["overlay"])
    assert len(points) == 17
    assert points[0]["time"] == int(bars[3].event_time.timestamp())
    assert points[0]["available_at"] == bars[3].received_at.isoformat()
    expected = sum((bar.close for bar in bars[:4]), Decimal(0)) / 4
    assert points[0]["value"] == float(expected)
    transformed = service.transform(dataset.id, ADMIN, window=4)
    assert service.transform(dataset.id, ADMIN, window=4) == transformed
    assert transformed.body["input_dataset"] == {
        "id": dataset.id,
        "version": dataset.version,
        "content_hash": dataset.content_hash,
    }
    assert service.series(dataset.id, VIEWER, window=30)["overlay"] == []
    for invalid in (0, 501, True):
        with pytest.raises(PlatformError, match="Window"):
            service.series(dataset.id, VIEWER, window=invalid)


@pytest.mark.parametrize("role", ["admin", "researcher", "viewer", "agent"])
def test_reserved_partition_denied_before_storage_for_every_role(
    service: DatasetService,
    role: str,
) -> None:
    principal = Principal.model_validate({"id": role, "role": role})
    development = service.create(DatasetSpec(rows=10), ADMIN)
    reserved_body = deepcopy(development.body)
    reserved_body["partition"] = "final"
    reserved_spec = cast(dict[str, JsonValue], reserved_body["spec"])
    reserved_spec["partition"] = "final"
    reserved = service.repo.put("dataset", "sealed-fixture", reserved_body)
    # A store without any content proves no reserved payload is fetched first.
    isolated = DatasetService(service.repo, MemoryArtifactStore(), service.policy, service.settings)
    with pytest.raises(AccessDenied):
        isolated.create(DatasetSpec(partition="final"), principal)
    for operation in (isolated.bars, isolated.series, isolated.inspect, isolated.transform):
        with pytest.raises(AccessDenied):
            operation(reserved.id, principal)
    if role != "agent":
        descriptor = isolated.get(reserved.id, principal)
        assert descriptor.content_hash == "reserved"
        assert descriptor.body == {
            "mode": "technical",
            "synthetic": True,
            "partition": "final",
            "payload_access": "reserved",
        }
        assert "spec" not in descriptor.body and "artifact" not in descriptor.body
        assert isolated.list(principal)[0].body == descriptor.body
    assert any(event.outcome == "denied" for event in service.repo.list_audit())


def test_catalog_partition_cannot_be_overridden_by_spec(service: DatasetService) -> None:
    development = service.create(DatasetSpec(rows=4), ADMIN)
    body = deepcopy(development.body)
    cast(dict[str, JsonValue], body["spec"])["partition"] = "final"
    service.repo.put("dataset", "confused-partition", body)
    with pytest.raises(PlatformError, match="partition differs"):
        service.bars("confused-partition", ADMIN)


def test_dataset_creation_limits_permissions_and_immutable_versions(
    service: DatasetService,
) -> None:
    with pytest.raises(AccessDenied):
        service.create(DatasetSpec(), VIEWER)
    with pytest.raises(PlatformError, match="SYNTH-USD"):
        service.create(DatasetSpec(instrument="BTC-USD"), ADMIN)
    with pytest.raises(PlatformError, match="SYNTH-USD"):
        service.create(DatasetSpec(quote_currency="USDT"), ADMIN)
    bounded = DatasetService(
        service.repo,
        service.store,
        service.policy,
        service.settings.model_copy(update={"max_dataset_rows": 5}),
    )
    with pytest.raises(PlatformError, match="row limit"):
        bounded.create(DatasetSpec(rows=6), ADMIN)
    dataset = service.create(DatasetSpec(rows=4), ADMIN)
    with pytest.raises(AccessDenied):
        service.transform(dataset.id, VIEWER)
    before = service.bars(dataset.id, ADMIN, 1)
    amended = deepcopy(dataset.body)
    amended["annotation"] = "versioned provenance correction"
    assert service.repo.put("dataset", dataset.id, amended).version == 2
    assert service.get(dataset.id, ADMIN).version == 2
    assert service.get(dataset.id, ADMIN, 1).body == dataset.body
    assert service.bars(dataset.id, ADMIN, 1) == before


def test_corrupted_missing_and_invalid_manifest_payloads_fail_closed(
    service: DatasetService,
) -> None:
    dataset = service.create(DatasetSpec(rows=6), ADMIN)
    artifact = cast(dict[str, JsonValue], dataset.body["artifact"])
    store = cast(LocalArtifactStore, service.store)
    path = store.root / f"{artifact['digest']}.parquet"
    original = path.read_bytes()
    path.write_bytes(b"corrupt")
    with pytest.raises(PlatformError, match="checksum"):
        service.bars(dataset.id, ADMIN)
    with pytest.raises(PlatformError, match="checksum"):
        store.put(original, "parquet")
    assert path.read_bytes() == b"corrupt"
    path.unlink()
    with pytest.raises(NotFound):
        service.bars(dataset.id, ADMIN)
    store.put(original, "parquet")
    bad_body = deepcopy(dataset.body)
    cast(dict[str, JsonValue], bad_body["artifact"])["size_bytes"] = 1
    bad = service.repo.put("dataset", "bad-size", bad_body)
    with pytest.raises(PlatformError, match="size"):
        service.inspect(bad.id, ADMIN)
    malformed = store.put(b"not parquet", "parquet")
    cast(dict[str, JsonValue], bad_body["artifact"]).update(
        {"digest": malformed, "size_bytes": len(b"not parquet")}
    )
    service.repo.put("dataset", "malformed", bad_body)
    with pytest.raises(PlatformError, match="schema"):
        service.bars("malformed", ADMIN)


def test_storage_path_symlink_and_size_boundaries(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path / "artifacts", max_bytes=20)
    digest = store.put(b"safe", "json")
    assert store.put(b"safe", "json") == digest
    for bad in ("../secret", "a" * 63, "A" * 64):
        with pytest.raises(PlatformError):
            store.get(bad, "json")
    for suffix in ("../json", ".json", "pickle", "json/../../secret"):
        with pytest.raises(PlatformError):
            store.put(b"safe", suffix)
    with pytest.raises(PlatformError, match="size"):
        store.put(b"x" * 21, "json")
    outside = tmp_path / "outside"
    outside.write_bytes(b"safe")
    path = store.root / f"{digest}.json"
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(PlatformError, match="safe regular"):
        store.get(digest, "json")
    with pytest.raises(PlatformError):
        store.put(b"safe", "json")
    alias = tmp_path / "alias"
    alias.symlink_to(store.root, target_is_directory=True)
    with pytest.raises(PlatformError, match="symlinks"):
        LocalArtifactStore(alias)
    # Replacing the root after construction also fails closed.
    store.root.rename(tmp_path / "moved")
    store.root.symlink_to(tmp_path / "moved", target_is_directory=True)
    with pytest.raises(PlatformError, match="symlinks"):
        store.get(digest, "json")


def test_memory_store_and_local_store_share_missing_and_format_failures(tmp_path: Path) -> None:
    for store in (MemoryArtifactStore(max_bytes=8), LocalArtifactStore(tmp_path, max_bytes=8)):
        with pytest.raises(NotFound):
            store.get("a" * 64, "json")
        with pytest.raises(PlatformError):
            store.put(b"", "json")
        with pytest.raises(PlatformError):
            store.put(b"123456789", "json")
        digest = store.put(b"hello", "md")
        assert store.get(digest, "md") == b"hello"


def test_transform_availability_includes_prior_transformation_delay():
    from datetime import timedelta

    from bot_trader.market_data.service import _generate, _overlay

    bars = _generate(DatasetSpec(rows=2))
    delayed = bars[0].model_copy(
        update={"transformed_at": bars[0].received_at + timedelta(minutes=2)}
    )
    points = _overlay((delayed, bars[1]), 2)
    assert points[0]["available_at"] == delayed.transformed_at.isoformat()


def test_causal_transform_prefix_and_future_perturbation_invariance():
    from decimal import Decimal

    from bot_trader.market_data.service import _generate, _overlay

    bars = _generate(DatasetSpec(rows=12))
    full = _overlay(bars, 5)
    assert _overlay(bars[:8], 5) == full[:4]
    changed = bars[-1].model_copy(
        update={"close": bars[-1].close + Decimal(100), "high": bars[-1].high + Decimal(100)}
    )
    perturbed = _overlay((*bars[:-1], changed), 5)
    assert perturbed[:-1] == full[:-1]
    assert perturbed[-1]["value"] != full[-1]["value"]
    assert _overlay(bars[:4], 5) == []
