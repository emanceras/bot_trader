"""Bounded immutable content storage; callers authorize catalog access first."""

import hashlib
import os
import re
import stat
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from bot_trader.core.errors import NotFound, PlatformError

_SUFFIXES = frozenset({"parquet", "json", "md"})


def _validate_key(digest: str, suffix: str) -> str:
    if not re.fullmatch(r"[a-f0-9]{64}", digest) or suffix not in _SUFFIXES:
        raise PlatformError("invalid_artifact", "Invalid artifact identifier or format.")
    return f"{digest}.{suffix}"


def _validate_data(data: bytes, suffix: str, max_bytes: int) -> str:
    if not isinstance(data, bytes) or not 0 < len(data) <= max_bytes:
        raise PlatformError("artifact_limit", "Artifact size is outside the configured limit.")
    digest = hashlib.sha256(data).hexdigest()
    _validate_key(digest, suffix)
    return digest


class ArtifactStore(Protocol):
    def put(self, data: bytes, suffix: str) -> str: ...

    def get(self, digest: str, suffix: str) -> bytes: ...


class LocalArtifactStore:
    """A flat digest namespace, atomic publication, no-follow opens and read verification."""

    def __init__(self, root: Path, max_bytes: int = 10_485_760) -> None:
        if max_bytes < 1:
            raise ValueError("Artifact limit must be positive.")
        self.root = Path(os.path.abspath(root))
        self.max_bytes = max_bytes
        self._check_parents()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._check_parents()

    def _check_parents(self) -> None:
        if any(path.is_symlink() for path in (self.root, *self.root.parents)):
            raise PlatformError("unsafe_storage", "Artifact storage cannot contain symlinks.")

    @contextmanager
    def _directory(self) -> Iterator[int]:
        self._check_parents()
        try:
            descriptor = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except OSError as error:
            raise PlatformError("unsafe_storage", "Artifact storage is unavailable.") from error
        try:
            yield descriptor
        finally:
            os.close(descriptor)

    def put(self, data: bytes, suffix: str) -> str:
        digest = _validate_data(data, suffix, self.max_bytes)
        filename = _validate_key(digest, suffix)
        temporary = f".pending-{uuid4().hex}"
        with self._directory() as directory:
            descriptor = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=directory,
            )
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                try:
                    os.link(temporary, filename, src_dir_fd=directory, dst_dir_fd=directory)
                except FileExistsError:
                    # Never replace content at an existing digest, even if it was corrupted.
                    if self.get(digest, suffix) != data:
                        raise PlatformError(
                            "artifact_corrupt", "Artifact checksum mismatch."
                        ) from None
                os.fsync(directory)
            finally:
                os.unlink(temporary, dir_fd=directory)
        return digest

    def get(self, digest: str, suffix: str) -> bytes:
        filename = _validate_key(digest, suffix)
        with self._directory() as directory:
            try:
                descriptor = os.open(
                    filename,
                    os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                    dir_fd=directory,
                )
            except FileNotFoundError as error:
                raise NotFound("Artifact is missing.") from error
            except OSError as error:
                raise PlatformError(
                    "unsafe_storage", "Artifact is not a safe regular file."
                ) from error
            with os.fdopen(descriptor, "rb") as stream:
                metadata = os.fstat(stream.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > self.max_bytes:
                    raise PlatformError("artifact_limit", "Artifact is not a bounded regular file.")
                data = stream.read(self.max_bytes + 1)
        if not data or len(data) > self.max_bytes or hashlib.sha256(data).hexdigest() != digest:
            raise PlatformError("artifact_corrupt", "Artifact checksum mismatch.")
        return data


class MemoryArtifactStore:
    """Same content contract for isolated tests and implementation substitution."""

    def __init__(self, max_bytes: int = 10_485_760) -> None:
        if max_bytes < 1:
            raise ValueError("Artifact limit must be positive.")
        self.max_bytes = max_bytes
        self._content: dict[tuple[str, str], bytes] = {}

    def put(self, data: bytes, suffix: str) -> str:
        digest = _validate_data(data, suffix, self.max_bytes)
        self._content[(digest, suffix)] = data
        return digest

    def get(self, digest: str, suffix: str) -> bytes:
        _validate_key(digest, suffix)
        try:
            data = self._content[(digest, suffix)]
        except KeyError as error:
            raise NotFound("Artifact is missing.") from error
        if len(data) > self.max_bytes or hashlib.sha256(data).hexdigest() != digest:
            raise PlatformError("artifact_corrupt", "Artifact checksum mismatch.")
        return data
