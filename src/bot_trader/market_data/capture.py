"""Bounded, append-only raw receipt journal over the existing artifact store.

Local durability uses the same POSIX filesystem assumptions as LocalArtifactStore.
A receipt ordinal is not an exchange sequence or evidence of upstream completeness.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Self
from uuid import uuid4

from pydantic import Field, model_validator

from bot_trader.core.contracts import Identifier
from bot_trader.core.events import (
    Digest,
    ImmutableV2,
    Nanoseconds,
    canonical_bytes,
    content_hash,
)
from bot_trader.market_data.storage import ArtifactStore

_RECORD_CHARGE = 8192
_METADATA_LIMIT = 4096


class CaptureLimitError(ValueError):
    """A configured capture bound prevents a further durable receipt."""


class CaptureLimits(ImmutableV2):
    max_frames: int = Field(default=1000, strict=True, gt=0, le=10_000)
    max_records: int = Field(default=2000, strict=True, gt=0, le=20_000)
    max_frame_bytes: int = Field(default=1_048_576, strict=True, gt=0, le=1_048_576)
    max_total_bytes: int = Field(default=67_108_864, strict=True, gt=0)
    min_free_disk_bytes: int = Field(default=0, strict=True, ge=0)


class CaptureRecord(ImmutableV2):
    capture_id: Identifier
    session_id: Identifier
    local_sequence: int = Field(strict=True, ge=1)
    kind: Identifier
    raw_sha256: Digest | None = None
    raw_size: int = Field(default=0, strict=True, ge=0)
    received_ns: Nanoseconds
    monotonic_ns: Nanoseconds
    config_hash: Digest
    source_id: Identifier
    source_version: Identifier
    details: dict[str, Any] = Field(default_factory=dict)
    previous_hash: Digest
    abandoned_charge: int = Field(default=0, strict=True, ge=0)

    @model_validator(mode="after")
    def bounded(self) -> Self:
        if (self.kind == "frame") != (self.raw_sha256 is not None):
            raise ValueError("Only raw frame receipts carry a content hash.")
        if self.kind != "frame" and self.raw_size:
            raise ValueError("Control records cannot claim raw bytes.")
        if len(canonical_bytes(self.model_dump(mode="json"))) > _METADATA_LIMIT:
            raise CaptureLimitError("Receipt metadata exceeds its bounded envelope.")
        return self

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


class CaptureCheckpoint(ImmutableV2):
    capture_id: Identifier
    config_hash: Digest
    committed_records: int
    frames: int
    total_charged_bytes: int
    last_hash: Digest
    pending_intent: bool


class CaptureJournal:
    """Single local writer; raw bytes precede publication of each immutable index.

    The index and envelope establish local integrity, not source truth or adversarial
    tamper resistance. Explicit recovery never invents an uncommitted market frame.
    """

    def __init__(
        self,
        store: ArtifactStore,
        directory: Path,
        capture_id: str,
        config_hash: str,
        limits: CaptureLimits | None = None,
        source_id: str = "kraken-ws-v2",
        source_version: str = "1",
        rights_reference: str = "synthetic-technical-fixture",
        synthetic: bool = True,
    ) -> None:
        self.store, self.directory = store, Path(os.path.abspath(directory))
        self.capture_id, self.config_hash = capture_id, config_hash
        self.source_id, self.source_version = source_id, source_version
        self.limits = CaptureLimits.model_validate((limits or CaptureLimits()).model_dump())
        if type(synthetic) is not bool or not rights_reference or len(rights_reference) > 1024:
            raise ValueError("Capture requires a bounded rights declaration and data class.")
        # Validate identities even for an empty journal.
        CaptureRecord(
            capture_id=capture_id,
            session_id="header",
            local_sequence=1,
            kind="header",
            received_ns=0,
            monotonic_ns=0,
            config_hash=config_hash,
            source_id=source_id,
            source_version=source_version,
            previous_hash="0" * 64,
        )
        self._safe_directory()
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._safe_directory()
        self._index = self.directory / "records"
        self._index.mkdir(exist_ok=True, mode=0o700)
        self._header = {
            "version": "raw-receipt-journal-v1",
            "capture_id": capture_id,
            "config_hash": config_hash,
            "source_id": source_id,
            "source_version": source_version,
            "rights_reference": rights_reference,
            "synthetic": synthetic,
            "limits": self.limits.model_dump(mode="json"),
        }
        self._genesis = content_hash(self._header)
        with self._writer():
            header = self.directory / "capture.json"
            if not header.exists():
                self._publish(header, canonical_bytes(self._header))
            if self._read(header) != canonical_bytes(self._header):
                raise ValueError(
                    "Capture identity, source, rights, configuration or limits changed."
                )
            self._load()

    def _safe_directory(self) -> None:
        if any(path.is_symlink() for path in (self.directory, *self.directory.parents)):
            raise ValueError("Capture directory cannot contain symlinks.")

    @contextmanager
    def _writer(self) -> Iterator[None]:
        import fcntl  # POSIX durability is required only when capture is instantiated.

        self._safe_directory()
        descriptor = os.open(
            self.directory / "writer.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        finally:
            os.close(descriptor)

    @contextmanager
    def capture_lease(self) -> Iterator[None]:
        """One collector/inspector per capture; separate from short append locks."""
        import fcntl

        self._safe_directory()
        descriptor = os.open(
            self.directory / "capture.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        finally:
            os.close(descriptor)

    @staticmethod
    def _sync(directory: Path) -> None:
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _publish(self, path: Path, data: bytes, *, replace: bool = False) -> None:
        if path.parent.is_symlink():
            raise ValueError("Journal metadata directory cannot be a symlink.")
        temporary = path.parent / (".pending-" + uuid4().hex)
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if replace:
                os.replace(temporary, path)
            else:
                os.link(temporary, path)
            self._sync(path.parent)
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _read(path: Path) -> bytes:
        if path.parent.is_symlink():
            raise ValueError("Journal metadata directory cannot be a symlink.")
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > _METADATA_LIMIT:
                raise ValueError("Journal metadata is not a bounded regular file.")
            return stream.read(_METADATA_LIMIT + 1)

    def _pending(self) -> CaptureRecord | None:
        path = self.directory / "pending.json"
        if not path.exists() and not path.is_symlink():
            return None
        record = CaptureRecord.model_validate_json(self._read(path))
        self._binding(record)
        sequence = record.local_sequence
        if sequence == len(self._records) + 1:
            if record.previous_hash != self._head:
                raise ValueError("Pending intent does not extend the committed prefix.")
        elif sequence != len(self._records) or record.digest != self._head:
            raise ValueError("Pending intent conflicts with the committed prefix.")
        return record

    def _binding(self, record: CaptureRecord) -> None:
        if (record.capture_id, record.config_hash, record.source_id, record.source_version) != (
            self.capture_id,
            self.config_hash,
            self.source_id,
            self.source_version,
        ):
            raise ValueError("Receipt identity or provenance differs from capture header.")
        if record.raw_size > self.limits.max_frame_bytes:
            raise CaptureLimitError("Raw frame exceeds the configured bound.")

    def _load(self) -> None:
        if self._index.is_symlink():
            raise ValueError("Journal index cannot be a symlink.")
        records: list[CaptureRecord] = []
        head = self._genesis
        clocks: dict[str, int] = {}
        for path in sorted(self._index.iterdir()):
            # Leftover unpublished atomic-write temporaries are not committed receipts.
            if path.name.startswith(".pending-"):
                continue
            if path.name != f"{len(records) + 1:012d}.json":
                raise ValueError("Journal index has a missing, unexpected or reordered entry.")
            reference = json.loads(self._read(path))
            if not isinstance(reference, dict) or set(reference) != {"record_hash"}:
                raise ValueError("Invalid journal index reference.")
            raw = self.store.get(reference["record_hash"], "json")
            record = CaptureRecord.model_validate_json(raw)
            self._binding(record)
            if (
                record.local_sequence != len(records) + 1
                or record.previous_hash != head
                or record.digest != reference["record_hash"]
            ):
                raise ValueError("Journal receipt hash, ordinal or predecessor changed.")
            if record.monotonic_ns < clocks.get(record.session_id, 0):
                raise ValueError("Monotonic clock reversed within a journal session.")
            clocks[record.session_id] = record.monotonic_ns
            if record.kind == "frame":
                self.read_frame(record)
            records.append(record)
            head = record.digest
            if len(records) > self.limits.max_records:
                raise CaptureLimitError("Committed journal exceeds its record bound.")
        self._records, self._head = records, head
        self._pending()

    def records(self) -> tuple[CaptureRecord, ...]:
        with self._writer():
            self._load()
            return tuple(record.model_copy(deep=True) for record in self._records)

    def frames(self) -> tuple[CaptureRecord, ...]:
        return tuple(record for record in self.records() if record.kind == "frame")

    def read_frame(self, record: CaptureRecord) -> bytes:
        record = CaptureRecord.model_validate(record.model_dump())
        self._binding(record)
        if record.kind != "frame" or record.raw_sha256 is None:
            raise ValueError("Only frame receipts reference raw content.")
        raw = self.store.get(record.raw_sha256, "bin") if record.raw_size else b""
        if len(raw) != record.raw_size or hashlib.sha256(raw).hexdigest() != record.raw_sha256:
            raise ValueError("Raw frame size or checksum changed.")
        return raw

    @property
    def checkpoint(self) -> CaptureCheckpoint:
        pending = self._pending()
        charged = sum(_RECORD_CHARGE + r.raw_size + r.abandoned_charge for r in self._records)
        if pending is not None and pending.local_sequence > len(self._records):
            charged += _RECORD_CHARGE + pending.raw_size + pending.abandoned_charge
        return CaptureCheckpoint(
            capture_id=self.capture_id,
            config_hash=self.config_hash,
            committed_records=len(self._records),
            frames=sum(r.kind == "frame" for r in self._records),
            total_charged_bytes=charged,
            last_hash=self._head,
            pending_intent=pending is not None,
        )

    @property
    def diagnostics(self) -> tuple[str, ...]:
        return tuple(
            f"utc_receipt_regression:{current.local_sequence}"
            for previous, current in zip(self._records, self._records[1:], strict=False)
            if current.received_ns < previous.received_ns
        )

    def _budget(self, record: CaptureRecord) -> None:
        total = sum(_RECORD_CHARGE + r.raw_size + r.abandoned_charge for r in self._records)
        charge = _RECORD_CHARGE + record.raw_size + record.abandoned_charge
        if (
            len(self._records) + 1 > self.limits.max_records
            or sum(r.kind == "frame" for r in self._records) + (record.kind == "frame")
            > self.limits.max_frames
            or total + charge > self.limits.max_total_bytes
        ):
            raise CaptureLimitError("Capture record, frame or conservative disk budget exhausted.")
        if shutil.disk_usage(self.directory).free < self.limits.min_free_disk_bytes + charge:
            raise CaptureLimitError("Capture free-disk reserve would be crossed.")

    def _record(
        self,
        kind: str,
        session_id: str,
        received_ns: int,
        monotonic_ns: int,
        raw: bytes | None,
        details: dict[str, Any] | None = None,
        abandoned_charge: int = 0,
    ) -> CaptureRecord:
        if len(canonical_bytes(details or {})) > 2048:
            raise CaptureLimitError("Receipt details exceed the bounded metadata budget.")
        record = CaptureRecord(
            capture_id=self.capture_id,
            session_id=session_id,
            local_sequence=len(self._records) + 1,
            kind=kind,
            raw_sha256=hashlib.sha256(raw).hexdigest() if raw is not None else None,
            raw_size=len(raw) if raw is not None else 0,
            received_ns=received_ns,
            monotonic_ns=monotonic_ns,
            config_hash=self.config_hash,
            source_id=self.source_id,
            source_version=self.source_version,
            details=details or {},
            previous_hash=self._head,
            abandoned_charge=abandoned_charge,
        )
        self._binding(record)
        previous = next((r for r in reversed(self._records) if r.session_id == session_id), None)
        if previous is not None and record.monotonic_ns < previous.monotonic_ns:
            raise ValueError("Monotonic receipt clock cannot reverse within a session.")
        self._budget(record)
        return record

    def _clear_pending(self) -> None:
        (self.directory / "pending.json").unlink()
        self._sync(self.directory)

    def _commit(self, record: CaptureRecord, raw: bytes | None) -> CaptureRecord:
        if raw:
            if self.store.put(raw, "bin") != record.raw_sha256:
                raise ValueError("Artifact store changed the raw content identity.")
        digest = self.store.put(canonical_bytes(record.model_dump(mode="json")), "json")
        if digest != record.digest:
            raise ValueError("Artifact store changed the receipt identity.")
        self._publish(
            self._index / f"{record.local_sequence:012d}.json",
            canonical_bytes({"record_hash": digest}),
        )
        self._records.append(record.model_copy(deep=True))
        self._head = digest
        self._clear_pending()
        return record.model_copy(deep=True)

    def append_frame(
        self, raw: bytes, *, session_id: str, received_ns: int, monotonic_ns: int
    ) -> CaptureRecord:
        if not isinstance(raw, bytes):
            raise ValueError("Original frames must be bytes, without decoding or reserialization.")
        return self._append("frame", session_id, received_ns, monotonic_ns, raw)

    def append_control(
        self,
        kind: str,
        *,
        session_id: str,
        received_ns: int,
        monotonic_ns: int,
        details: dict[str, Any] | None = None,
    ) -> CaptureRecord:
        if kind == "frame":
            raise ValueError("A control cannot impersonate a raw frame receipt.")
        return self._append(kind, session_id, received_ns, monotonic_ns, None, details)

    def _append(
        self,
        kind: str,
        session_id: str,
        received_ns: int,
        monotonic_ns: int,
        raw: bytes | None,
        details: dict[str, Any] | None = None,
    ) -> CaptureRecord:
        with self._writer():
            self._load()
            if self._pending() is not None:
                raise ValueError("Pending writer intent requires explicit recovery before append.")
            record = self._record(kind, session_id, received_ns, monotonic_ns, raw, details)
            self._publish(
                self.directory / "pending.json", canonical_bytes(record.model_dump(mode="json"))
            )
            return self._commit(record, raw)

    def recover(
        self, *, writer_stopped: bool, session_id: str, received_ns: int, monotonic_ns: int
    ) -> CaptureRecord | None:
        if writer_stopped is not True:
            raise ValueError("Recovery requires explicit confirmation that the old writer stopped.")
        with self._writer():
            self._load()
            pending = self._pending()
            if pending is None:
                return None
            committed = pending.local_sequence == len(self._records)
            if pending.kind == "interruption" and "recovery_of" in pending.details:
                if committed:
                    self._clear_pending()
                    return pending
                return self._commit(pending, None)
            record = self._record(
                "interruption",
                session_id,
                received_ns,
                monotonic_ns,
                None,
                {
                    "recovery_of": pending.digest,
                    "intent_already_committed": committed,
                    "coverage": "unknown",
                    "uncommitted_frame_not_reconstructed": not committed,
                },
                abandoned_charge=0 if committed else _RECORD_CHARGE + pending.raw_size,
            )
            preserved = self.directory / ("interrupted-" + pending.digest + ".json")
            raw = canonical_bytes(pending.model_dump(mode="json"))
            if preserved.exists():
                if self._read(preserved) != raw:
                    raise ValueError("Preserved writer intent changed.")
            else:
                self._publish(preserved, raw)
            self._publish(
                self.directory / "pending.json",
                canonical_bytes(record.model_dump(mode="json")),
                replace=True,
            )
            return self._commit(record, None)
