import hashlib
from pathlib import Path

import pytest
from pydantic import ValidationError

from bot_trader.core.errors import AccessDenied, PlatformError
from bot_trader.market_data.archive import ImportCheckpoint, LocalArchive, SourceSpec
from bot_trader.market_data.storage import LocalArtifactStore, MemoryArtifactStore


def source_spec(data: bytes, **updates: object) -> SourceSpec:
    body: dict[str, object] = {
        "source_id": "synthetic-fixture",
        "source_version": "v1",
        "source_schema": "fixture-jsonl-v1",
        "locator": "internal:fixture-v1",
        "rights": "Internally generated; authorized technical validation only.",
        "acquired_ns": 1_700_000_000_000_000_123,
        "raw_sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "data_class": "synthetic",
        **updates,
    }
    return SourceSpec.model_validate(body)


def test_local_archive_resume_identity_and_original_integrity(tmp_path: Path) -> None:
    data = b'{"a":1}\n{"a":2}\n'
    source = tmp_path / "fixture.jsonl"
    source.write_bytes(data)
    spec = source_spec(data)
    store = LocalArtifactStore(tmp_path / "archive")
    archive = LocalArchive(store, chunk_size=5)
    first = archive.import_step(source, spec)
    assert first.offset == 5 and not first.complete and first.archive_hash is None
    checkpoint = ImportCheckpoint.model_validate_json(store.get(first.checkpoint_hash, "json"))
    assert checkpoint.offset == 5
    assert archive.import_step(source, spec) == first
    # A new service instance resumes solely from a persistent immutable token.
    resumed = LocalArchive(store, chunk_size=5).import_step(
        source, spec, checkpoint_hash=first.checkpoint_hash, max_chunks=100
    )
    assert resumed.complete and resumed.archive_hash is not None
    whole = archive.import_step(source, spec, max_chunks=100)
    assert whole == resumed
    assert archive.import_step(source, spec, checkpoint_hash=resumed.checkpoint_hash) == resumed
    raw, declaration, payload = archive.read(resumed.archive_hash)
    assert declaration == spec and payload == data and source.read_bytes() == data
    assert raw.raw_sha256 == hashlib.sha256(data).hexdigest()
    assert (
        ImportCheckpoint.model_validate_json(store.get(first.checkpoint_hash, "json")) == checkpoint
    )
    # Substituting the artifact store changes neither content identity nor result.
    memory = LocalArchive(MemoryArtifactStore(), chunk_size=5)
    assert memory.import_step(source, spec, max_chunks=100) == whole


def test_archive_rejects_changed_input_and_incompatible_resume(tmp_path: Path) -> None:
    data = b"abcdefgh"
    source = tmp_path / "raw"
    source.write_bytes(data)
    store = LocalArtifactStore(tmp_path / "archive")
    archive = LocalArchive(store, chunk_size=3)
    spec = source_spec(data)
    first = archive.import_step(source, spec)
    source.write_bytes(b"abcdEfgh")
    with pytest.raises(PlatformError, match="checksum"):
        archive.import_step(source, spec, checkpoint_hash=first.checkpoint_hash)
    source.write_bytes(data)
    changed = source_spec(data, source_version="v2")
    with pytest.raises(PlatformError, match="different source"):
        archive.import_step(source, changed, checkpoint_hash=first.checkpoint_hash)
    with pytest.raises(PlatformError, match="chunk size"):
        LocalArchive(store, chunk_size=4).import_step(
            source, spec, checkpoint_hash=first.checkpoint_hash
        )


def test_corrupt_staged_chunk_and_original_are_never_repaired(tmp_path: Path) -> None:
    data = b"abcdefgh"
    source = tmp_path / "raw"
    source.write_bytes(data)
    store = LocalArtifactStore(tmp_path / "archive")
    archive = LocalArchive(store, chunk_size=3)
    spec = source_spec(data)
    first = archive.import_step(source, spec)
    checkpoint = ImportCheckpoint.model_validate_json(store.get(first.checkpoint_hash, "json"))
    corrupt = store.root / f"{checkpoint.chunk_hashes[0]}.bin"
    corrupt.write_bytes(b"bad")
    with pytest.raises(PlatformError, match="checksum"):
        archive.import_step(source, spec, checkpoint_hash=first.checkpoint_hash)
    with pytest.raises(PlatformError, match="checksum"):
        archive.import_step(source, spec)
    assert corrupt.read_bytes() == b"bad"
    # Original corruption after a separately completed acquisition is detected too.
    clean_store = LocalArtifactStore(tmp_path / "clean")
    clean = LocalArchive(clean_store, chunk_size=3)
    complete = clean.import_step(source, spec, max_chunks=100)
    assert complete.archive_hash is not None
    (clean_store.root / f"{spec.raw_sha256}.bin").write_bytes(b"corrupt")
    with pytest.raises(PlatformError, match="checksum"):
        clean.read(complete.archive_hash)


def test_interrupted_local_acquisition_is_not_a_complete_archive(tmp_path: Path) -> None:
    class InterruptingStore(MemoryArtifactStore):
        fail = True

        def put(self, data: bytes, suffix: str) -> str:
            if suffix == "bin" and data == b"def" and self.fail:
                raise InterruptedError("Synthetic interruption before second chunk publication")
            return super().put(data, suffix)

    data = b"abcdefgh"
    source = tmp_path / "raw"
    source.write_bytes(data)
    spec = source_spec(data)
    store = InterruptingStore()
    archive = LocalArchive(store, chunk_size=3)
    first = archive.import_step(source, spec)
    with pytest.raises(InterruptedError):
        archive.import_step(source, spec, checkpoint_hash=first.checkpoint_hash, max_chunks=100)
    assert not first.complete and first.archive_hash is None
    assert (
        ImportCheckpoint.model_validate_json(store.get(first.checkpoint_hash, "json")).offset == 3
    )
    store.fail = False
    done = archive.import_step(source, spec, checkpoint_hash=first.checkpoint_hash, max_chunks=100)
    assert done.complete and done.archive_hash is not None
    assert archive.read(done.archive_hash)[2] == data


def test_reserved_partition_is_denied_before_reading_source(tmp_path: Path) -> None:
    archive = LocalArchive(MemoryArtifactStore())
    for role in ("validation", "final"):
        with pytest.raises(AccessDenied):
            archive.import_step(tmp_path / "nonexistent", source_spec(b"a", partition=role))


def test_exact_acquisition_timestamp_and_path_size_checks(tmp_path: Path) -> None:
    for value in (1.0, True, -1, 2**64):
        with pytest.raises(ValidationError):
            source_spec(b"a", acquired_ns=value)
    source = tmp_path / "raw"
    source.write_bytes(b"ab")
    archive = LocalArchive(MemoryArtifactStore(), max_bytes=10, chunk_size=3)
    with pytest.raises(PlatformError, match="size"):
        archive.import_step(source, source_spec(b"a"))
    alias = tmp_path / "alias"
    alias.symlink_to(source)
    with pytest.raises(PlatformError, match="symlinks"):
        archive.import_step(alias, source_spec(b"ab"))
    with pytest.raises(PlatformError, match="bound"):
        LocalArchive(MemoryArtifactStore(), max_bytes=1, chunk_size=1).import_step(
            source, source_spec(b"ab")
        )
