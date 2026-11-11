"""Immutable local acquisition with explicit provenance and resumable checkpoints.

This is a bounded local-file importer, not a downloader or a live feed. A source
declaration records the caller's rights/provenance assertion; its hash does not
independently prove that assertion. Original, checkpoint and archive records use
the existing content store, so a partial acquisition never becomes a complete
archive merely because some chunks exist.
"""

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bot_trader.core.contracts import Identifier, Partition
from bot_trader.core.errors import AccessDenied, PlatformError
from bot_trader.market_data.storage import ArtifactStore

Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Nanoseconds = Annotated[int, Field(strict=True, ge=0, lt=2**64)]


class ArchiveContract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True, validate_default=True)
    schema_version: Literal[2] = 2


class SourceSpec(ArchiveContract):
    """Identity and allowed purpose of one exact local source version."""

    source_id: Identifier
    source_version: Identifier
    source_schema: Identifier
    locator: str = Field(min_length=1, max_length=2048)
    rights: str = Field(min_length=1, max_length=4096)
    permitted_use: Literal["technical_validation_only"] = "technical_validation_only"
    acquired_ns: Nanoseconds
    raw_sha256: Digest
    size_bytes: int = Field(strict=True, gt=0)
    data_class: Literal["synthetic", "exposed_structural_only"]
    partition: Partition = "development"


class ImportCheckpoint(ArchiveContract):
    kind: Literal["local-import-checkpoint"] = "local-import-checkpoint"
    source_manifest_hash: Digest
    chunk_size: int = Field(strict=True, gt=0)
    chunk_hashes: tuple[Digest, ...] = Field(max_length=10_000)
    offset: int = Field(strict=True, ge=0)


class RawArchive(ArchiveContract):
    kind: Literal["raw-archive"] = "raw-archive"
    source_manifest_hash: Digest
    raw_sha256: Digest
    size_bytes: int = Field(strict=True, gt=0)
    chunk_hashes: tuple[Digest, ...] = Field(min_length=1, max_length=10_000)


class ImportProgress(ArchiveContract):
    checkpoint_hash: Digest
    archive_hash: Digest | None = None
    offset: int = Field(strict=True, ge=0)
    complete: bool

    @model_validator(mode="after")
    def validate_completion(self) -> Self:
        if self.complete != (self.archive_hash is not None):
            raise ValueError("Completion requires an archive identity.")
        return self


def _canonical(record: ArchiveContract) -> bytes:
    return json.dumps(record.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _failure(message: str) -> PlatformError:
    return PlatformError("archive_integrity", message)


class LocalArchive:
    """Small additive acquisition service using replaceable content storage.

    Every call verifies the bounded input and existing staged prefix. The resume
    token is itself an immutable hash, so stale or interrupted calls may repeat
    safely. Restarting without a token reuses the same chunk objects. No local
    file, corrupt artifact or prior checkpoint is silently replaced.
    """

    def __init__(
        self, store: ArtifactStore, *, max_bytes: int = 10_485_760, chunk_size: int = 65_536
    ) -> None:
        if type(max_bytes) is not int or type(chunk_size) is not int:
            raise ValueError("Archive bounds must be exact integers.")
        if max_bytes < 1 or not 1 <= chunk_size <= max_bytes:
            raise ValueError("Archive bounds must be positive and consistent.")
        self.store = store
        self.max_bytes = max_bytes
        self.chunk_size = chunk_size

    @staticmethod
    def _authorize(spec: SourceSpec) -> None:
        if spec.partition != "development":
            raise AccessDenied("Reserved archive payloads are unavailable for technical import.")

    def _read_local(self, path: Path, spec: SourceSpec) -> bytes:
        path = Path(os.path.abspath(path))
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            raise _failure("Source paths cannot contain symlinks.")
        if spec.size_bytes > self.max_bytes:
            raise _failure("Source size exceeds the configured technical archive bound.")
        try:
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except OSError as error:
            raise _failure("Source is unavailable or not a safe regular file.") from error
        with os.fdopen(descriptor, "rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_size != spec.size_bytes:
                raise _failure("Source type or declared size does not match.")
            data = stream.read(self.max_bytes + 1)
            after = os.fstat(stream.fileno())
        before_state = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        after_state = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        )
        if before_state != after_state:
            raise _failure("Source changed while it was being read.")
        if len(data) != spec.size_bytes or _sha(data) != spec.raw_sha256:
            raise _failure("Source size or checksum differs from the immutable declaration.")
        return data

    def import_step(
        self,
        path: Path,
        spec: SourceSpec,
        *,
        checkpoint_hash: str | None = None,
        max_chunks: int = 1,
    ) -> ImportProgress:
        # Revalidate public typed values; model_copy alone does not validate updates.
        spec = SourceSpec.model_validate(spec.model_dump())
        self._authorize(spec)
        if type(max_chunks) is not int or not 1 <= max_chunks <= 1000:
            raise ValueError("A local import step requires 1 to 1000 chunks.")
        data = self._read_local(path, spec)
        source_hash = self.store.put(_canonical(spec), "json")
        checkpoint = ImportCheckpoint(
            source_manifest_hash=source_hash,
            chunk_size=self.chunk_size,
            chunk_hashes=(),
            offset=0,
        )
        if checkpoint_hash is not None:
            checkpoint = ImportCheckpoint.model_validate_json(
                self.store.get(checkpoint_hash, "json")
            )
            if checkpoint.source_manifest_hash != source_hash:
                raise _failure("Resume checkpoint belongs to a different source declaration.")
            if checkpoint.chunk_size != self.chunk_size:
                raise _failure("Resume chunk size differs from the original configuration.")
        offset = 0
        for index, digest in enumerate(checkpoint.chunk_hashes):
            chunk = self.store.get(digest, "bin")
            expected = data[offset : offset + self.chunk_size]
            if chunk != expected or not chunk or _sha(chunk) != digest:
                raise _failure("Staged chunk does not match the unchanged source prefix.")
            if len(chunk) != self.chunk_size and index != len(checkpoint.chunk_hashes) - 1:
                raise _failure("An incomplete chunk cannot precede another staged chunk.")
            offset += len(chunk)
        if offset != checkpoint.offset or offset > spec.size_bytes:
            raise _failure("Resume offset differs from verified staged chunks.")
        chunks = list(checkpoint.chunk_hashes)
        for _ in range(max_chunks):
            if offset == spec.size_bytes:
                break
            chunk = data[offset : offset + self.chunk_size]
            chunks.append(self.store.put(chunk, "bin"))
            offset += len(chunk)
        completed = offset == spec.size_bytes
        new_checkpoint = ImportCheckpoint(
            source_manifest_hash=source_hash,
            chunk_size=self.chunk_size,
            chunk_hashes=tuple(chunks),
            offset=offset,
        )
        token = self.store.put(_canonical(new_checkpoint), "json")
        archive_hash = None
        if completed:
            digest = self.store.put(data, "bin")
            if digest != spec.raw_sha256:
                raise _failure("Content storage returned an incorrect raw identity.")
            archive = RawArchive(
                source_manifest_hash=source_hash,
                raw_sha256=digest,
                size_bytes=spec.size_bytes,
                chunk_hashes=tuple(chunks),
            )
            archive_hash = self.store.put(_canonical(archive), "json")
        return ImportProgress(
            checkpoint_hash=token, archive_hash=archive_hash, offset=offset, complete=completed
        )

    def inspect(self, archive_hash: str) -> tuple[RawArchive, SourceSpec]:
        """Read immutable metadata; do not open raw bytes or reserved partitions."""
        archive = RawArchive.model_validate_json(self.store.get(archive_hash, "json"))
        spec = SourceSpec.model_validate_json(self.store.get(archive.source_manifest_hash, "json"))
        self._authorize(spec)
        if archive.raw_sha256 != spec.raw_sha256 or archive.size_bytes != spec.size_bytes:
            raise _failure("Archive and source declarations disagree.")
        if archive.size_bytes > self.max_bytes:
            raise _failure("Archive exceeds the configured technical bound.")
        return archive, spec

    def read(self, archive_hash: str) -> tuple[RawArchive, SourceSpec, bytes]:
        archive, spec = self.inspect(archive_hash)
        data = self.store.get(archive.raw_sha256, "bin")
        if len(data) != archive.size_bytes or _sha(data) != archive.raw_sha256:
            raise _failure("Raw content differs from the immutable archive.")
        return archive, spec, data
