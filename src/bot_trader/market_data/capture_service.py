"""Finite simulated public-feed capture composed with the platform's storage and policy.

Transport is injected; this module has no socket client or order interface. A future
real connector requires separate admission rather than a runtime flag bypass.
"""

import hashlib
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, Protocol

from pydantic import Field

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import AccessDenied, PlatformError
from bot_trader.core.events import ImmutableV2, canonical_bytes, content_hash, exact_ns
from bot_trader.core.security import Policy
from bot_trader.market_data.archive import LocalArchive, SourceSpec
from bot_trader.market_data.capture import CaptureJournal, CaptureLimitError, CaptureLimits
from bot_trader.market_data.kraken_ws import SCHEMA, KrakenProtocol, KrakenWSNormalizer
from bot_trader.market_data.replay import CaptureReplayCheckpoint, MarketReplay
from bot_trader.market_data.storage import ArtifactStore


class ReceiptClock(Protocol):
    def now(self) -> tuple[int, int]: ...
    def sleep_ns(self, duration_ns: int) -> None: ...


class FrameTransport(Protocol):
    simulated: bool

    def connect(self, endpoint: str) -> None: ...
    def send(self, request: dict[str, Any]) -> None: ...
    def receive(self, timeout_ns: int) -> bytes: ...
    def close(self) -> None: ...


class FixtureComplete(Exception):
    """Finite scripted input ended; a real remote disconnect is not this condition."""


class CaptureConfiguration(ImmutableV2):
    version: Literal["kraken-simulated-capture-v1"] = "kraken-simulated-capture-v1"
    mode: Literal["simulated"] = "simulated"
    synthetic: Literal[True] = True
    symbol: Literal["BTC/EUR"] = "BTC/EUR"
    endpoint: Literal["wss://ws.kraken.com/v2"] = "wss://ws.kraken.com/v2"
    partition: Literal["development"] = "development"
    max_duration_ns: int = Field(default=600_000_000_000, strict=True, gt=0, le=600_000_000_000)
    receive_timeout_ns: int = Field(default=2_000_000_000, strict=True, gt=0, le=10_000_000_000)
    max_reconnects: int = Field(default=2, strict=True, ge=0, le=10)
    reconnect_delay_ns: int = Field(default=1_000_000_000, strict=True, ge=0, le=10_000_000_000)
    limits: CaptureLimits = CaptureLimits()

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


def collect(
    journal: CaptureJournal,
    config: CaptureConfiguration,
    factory: Callable[[int], FrameTransport],
    clock: ReceiptClock,
    stop_requested: Callable[[], bool] = lambda: False,
) -> dict[str, Any]:
    """Bounded collector; every received raw frame is durable before protocol decoding."""
    with journal.capture_lease():
        return _collect(journal, config, factory, clock, stop_requested)


def _collect(
    journal: CaptureJournal,
    config: CaptureConfiguration,
    factory: Callable[[int], FrameTransport],
    clock: ReceiptClock,
    stop_requested: Callable[[], bool],
) -> dict[str, Any]:
    config = CaptureConfiguration.model_validate(config.model_dump())
    if config.digest != journal.config_hash:
        raise ValueError("Collector configuration differs from the journal binding.")
    if journal.checkpoint.pending_intent:
        raise ValueError("Explicit interrupted-writer recovery is required before capture.")
    initial = journal.records()
    if (
        initial
        and initial[-1].kind == "capture_stop"
        and initial[-1].details.get("reason") != "interrupted"
    ):
        return {
            "reason": initial[-1].details["reason"],
            "resumed_terminal": True,
            "sessions_started": sum(r.kind == "session_start" for r in initial),
            "checkpoint": journal.checkpoint.model_dump(mode="json"),
            "diagnostics": [],
            "real_capture": False,
        }
    utc, started_monotonic = clock.now()
    exact_ns(utc)
    exact_ns(started_monotonic)
    start_utc = initial[0].received_ns if initial else utc
    deadline = start_utc + config.max_duration_ns
    sessions = sum(record.kind == "session_start" for record in initial)
    reason = "reconnect_limit"
    diagnostics: list[str] = []
    last_utc = initial[-1].received_ns if initial else utc
    session = "none"
    transport: FrameTransport | None = None

    def control(kind: str, details: dict[str, Any] | None = None) -> None:
        nonlocal last_utc
        received, monotonic = clock.now()
        journal.append_control(
            kind,
            session_id=session,
            received_ns=received,
            monotonic_ns=monotonic,
            details=details or {},
        )
        last_utc = max(last_utc, received)

    def close_transport() -> None:
        nonlocal transport
        current, transport = transport, None
        if current is not None:
            try:
                current.close()
            except (OSError, ValueError):
                diagnostics.append("transport_close_not_confirmed")

    try:
        while sessions <= config.max_reconnects:
            now, monotonic = clock.now()
            if now >= deadline or monotonic - started_monotonic >= config.max_duration_ns:
                reason = "duration_limit"
                break
            if stop_requested():
                reason = "user_stop"
                break
            if journal.checkpoint.frames >= config.limits.max_frames:
                reason = "frame_limit"
                break
            session = f"session-{sessions + 1}"
            transport = factory(sessions)
            if transport.simulated is not True:
                raise AccessDenied("This delivery has no admitted real-capture transport.")
            sessions += 1
            protocol = KrakenProtocol()
            subscribed = False
            control("session_start", {"attempt": sessions, "deadline_utc_ns": deadline})
            try:
                transport.connect(config.endpoint)
                for request in protocol.requests_for_preflight():
                    control("public_request", {"request": request})
                    transport.send(request)
                while True:
                    now, monotonic = clock.now()
                    if now >= deadline or monotonic - started_monotonic >= config.max_duration_ns:
                        reason = "duration_limit"
                        break
                    if stop_requested():
                        reason = "user_stop"
                        break
                    if journal.checkpoint.frames >= config.limits.max_frames:
                        reason = "frame_limit"
                        break
                    remaining = min(
                        deadline - now, config.max_duration_ns - (monotonic - started_monotonic)
                    )
                    raw = transport.receive(min(config.receive_timeout_ns, remaining))
                    received, received_monotonic = clock.now()  # before parsing
                    journal.append_frame(
                        raw,
                        session_id=session,
                        received_ns=received,
                        monotonic_ns=received_monotonic,
                    )
                    if received < last_utc:
                        reason = "clock_regression"
                        control("clock_regression", {"normalization_allowed": False})
                        break
                    last_utc = received
                    if (
                        received >= deadline
                        or received_monotonic - started_monotonic >= config.max_duration_ns
                    ):
                        # Preserve the receipt but do not subscribe or consume another frame.
                        reason = "duration_limit"
                        break
                    result = protocol.accept(raw)
                    diagnostics.extend(result.diagnostics)
                    if protocol.preflight_ready and not subscribed:
                        for request in protocol.market_requests():
                            control("public_request", {"request": request})
                            transport.send(request)
                        subscribed = True
            except FixtureComplete:
                reason = "fixture_complete"
            except (ConnectionError, TimeoutError) as error:
                reason = "disconnected"
                control("coverage_gap", {"cause": type(error).__name__, "coverage": "unknown"})
            except CaptureLimitError:
                raise
            except ValueError as error:
                reason = "protocol_error"
                control(
                    "protocol_error", {"error_type": type(error).__name__, "raw_preserved": True}
                )
            finally:
                close_transport()
            if "transport_close_not_confirmed" in diagnostics:
                reason = "transport_close_failure"
                break
            if reason != "disconnected":
                break
            if sessions > config.max_reconnects:
                reason = "reconnect_limit"
                break
            jitter = (
                int(hashlib.sha256(f"{journal.capture_id}:{sessions}".encode()).hexdigest()[:8], 16)
                % 201
                + 900
            )
            delay = (
                min(10_000_000_000, config.reconnect_delay_ns * 2 ** (sessions - 1))
                * jitter
                // 1000
            )
            now, monotonic = clock.now()
            remaining = min(
                deadline - now, config.max_duration_ns - (monotonic - started_monotonic)
            )
            if remaining <= 0:
                reason = "duration_limit"
                break
            control(
                "reconnect_wait", {"delay_ns": min(delay, remaining), "policy": "bounded-jitter-v1"}
            )
            clock.sleep_ns(min(delay, remaining))
        control("capture_stop", {"reason": reason})
    except CaptureLimitError:
        reason = "storage_or_record_limit"
    except KeyboardInterrupt:
        reason = "interrupted"
        try:
            control("capture_stop", {"reason": reason})
        except (OSError, ValueError):
            diagnostics.append("stop_record_not_confirmed")
    except OSError:
        reason = "storage_failure"
    except PlatformError as error:
        if isinstance(error, AccessDenied):
            raise
        reason = "artifact_failure"
        diagnostics.append(error.code)
    finally:
        close_transport()
    return {
        "reason": reason,
        "sessions_started": sessions,
        "checkpoint": journal.checkpoint.model_dump(mode="json"),
        "diagnostics": diagnostics,
        "real_capture": False,
    }


class KrakenCaptureService:
    """Platform service using the existing store, normalizer port and data-only replay."""

    def __init__(self, store: ArtifactStore, policy: Policy, directory: Path) -> None:
        self.store, self.policy, self.directory = store, policy, directory

    def journal(
        self, capture_id: str, config: CaptureConfiguration, principal: Principal
    ) -> CaptureJournal:
        self.policy.require(principal, "worker.execute", partition=config.partition)
        config = CaptureConfiguration.model_validate(config.model_dump())
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", capture_id):
            raise ValueError("Use a bounded portable capture identity, not a path.")
        journal = CaptureJournal(
            self.store,
            self.directory / capture_id,
            capture_id=capture_id,
            config_hash=config.digest,
            limits=config.limits,
        )
        if self.store.put(canonical_bytes(config.model_dump(mode="json")), "json") != config.digest:
            raise ValueError("Configuration artifact identity changed.")
        return journal

    def run_simulated(
        self,
        capture_id: str,
        config: CaptureConfiguration,
        principal: Principal,
        factory: Callable[[int], FrameTransport],
        clock: ReceiptClock,
        stop_requested: Callable[[], bool] = lambda: False,
    ) -> dict[str, Any]:
        journal = self.journal(capture_id, config, principal)
        capture = collect(journal, config, factory, clock, stop_requested)
        if journal.checkpoint.pending_intent:
            return {"status": "blocked_pending_recovery", "capture": capture, "synthetic": True}
        try:
            result = self.inspect(capture_id, config, principal)
        except (ValueError, OSError, PlatformError) as error:
            return {
                "status": "blocked_normalization",
                "capture": capture,
                "synthetic": True,
                "error_type": type(error).__name__,
                "financial_validation": False,
            }
        return {**result, "capture": capture}

    def inspect(
        self,
        capture_id: str,
        config: CaptureConfiguration,
        principal: Principal,
        *,
        until_ns: int | None = None,
        checkpoint: CaptureReplayCheckpoint | None = None,
    ) -> dict[str, Any]:
        journal = self.journal(capture_id, config, principal)
        with journal.capture_lease():
            return self._inspect(journal, capture_id, config, until_ns, checkpoint)

    def _inspect(
        self,
        journal: CaptureJournal,
        capture_id: str,
        config: CaptureConfiguration,
        until_ns: int | None,
        checkpoint: CaptureReplayCheckpoint | None,
    ) -> dict[str, Any]:
        journal.records()  # Refresh and verify the committed prefix under the capture lease.
        if journal.checkpoint.pending_intent:
            raise ValueError("Unresolved writer intent prevents capture admission.")
        if journal.diagnostics:
            raise ValueError("Receipt clock regression prevents capture admission.")
        frames = journal.frames()
        manifest = canonical_bytes(
            {
                "schema_version": 1,
                "capture_id": capture_id,
                "frames": [record.model_dump(mode="json") for record in frames],
            }
        )
        digest = hashlib.sha256(manifest).hexdigest()
        path = self.directory / capture_id / ("manifest-" + digest + ".json")
        if path.exists():
            if path.read_bytes() != manifest:
                raise ValueError("Capture manifest content changed.")
        else:
            with path.open("xb") as stream:
                stream.write(manifest)
                stream.flush()
                os.fsync(stream.fileno())
        source = SourceSpec(
            source_id="kraken-ws-v2",
            source_version="1",
            source_schema=SCHEMA,
            locator=f"internal:simulated-capture:{capture_id}",
            rights="Invented transport fixtures; no market-data acquisition.",
            acquired_ns=frames[-1].received_ns if frames else 0,
            raw_sha256=digest,
            size_bytes=len(manifest),
            data_class="synthetic",
        )
        archive = LocalArchive(self.store)
        imported = archive.import_step(path, source, max_chunks=1000)
        if imported.archive_hash is None:
            raise ValueError("Bounded capture manifest import remains incomplete.")
        record, declaration, raw = archive.read(imported.archive_hash)
        normalizer = KrakenWSNormalizer(self.store, synthetic=True)
        normalized = normalizer.normalize_with_provenance(
            raw, declaration, record.source_manifest_hash
        )
        replay = MarketReplay().inspect_capture(
            normalized.events, data_class="synthetic", until_ns=until_ns, checkpoint=checkpoint
        )
        sidecar = self.store.put(canonical_bytes(normalized.model_dump(mode="json")), "json")
        replay_hash = self.store.put(canonical_bytes(replay.model_dump(mode="json")), "json")
        return {
            "status": "technical_qa",
            "synthetic": True,
            "financial_validation": False,
            "capture_id": capture_id,
            "config_hash": config.digest,
            "journal_checkpoint": journal.checkpoint.model_dump(mode="json"),
            "upstream_completeness": "unknown",
            "archive_hash": imported.archive_hash,
            "normalization_hash": sidecar,
            "replay_hash": replay_hash,
            "market_events": len(replay.events),
            "checkpoint": replay.checkpoint.model_dump(mode="json"),
        }
