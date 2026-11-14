"""Finite public-feed QA with separate simulated and explicitly approved pilot entry points."""

import hashlib
import os
import re
import socket
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
from bot_trader.market_data.capture_authority import PilotApproval, PilotConfiguration
from bot_trader.market_data.kraken_ws import (
    SCHEMA,
    KrakenProtocol,
    KrakenWSNormalizer,
    exact_ws_json,
)
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


class CaptureDeadline(Exception):
    """The declared intake window ended; shutdown may use its separately bounded grace."""


class ReceivePollTimeout(TimeoutError):
    """No message in a short poll; service idle/deadline policy decides when to reconnect."""


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


CaptureConfig = CaptureConfiguration | PilotConfiguration


def validated_config(config: CaptureConfig) -> CaptureConfig:
    kind = PilotConfiguration if isinstance(config, PilotConfiguration) else CaptureConfiguration
    return kind.model_validate(config.model_dump())


def collect(
    journal: CaptureJournal,
    config: CaptureConfiguration,
    factory: Callable[[int], FrameTransport],
    clock: ReceiptClock,
    stop_requested: Callable[[], bool] = lambda: False,
) -> dict[str, Any]:
    """Bounded collector; every received raw frame is durable before protocol decoding."""
    if not isinstance(config, CaptureConfiguration):
        raise AccessDenied("Use the separately approved pilot entry point for real data.")
    with journal.capture_lease():
        return _collect(journal, config, factory, clock, stop_requested)


def _collect(
    journal: CaptureJournal,
    config: CaptureConfig,
    factory: Callable[[int], FrameTransport],
    clock: ReceiptClock,
    stop_requested: Callable[[], bool],
    *,
    expected_simulated: bool = True,
) -> dict[str, Any]:
    config = validated_config(config)
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
            "real_capture": not expected_simulated,
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
    market_rows = 0
    for prior in initial:
        if prior.kind == "frame":
            value = exact_ws_json(journal.read_frame(prior))
            if value.get("channel") in ("trade", "ticker"):
                market_rows += len(value.get("data", []))
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
                return
            outcome = getattr(current, "close_outcome", None)
            if outcome is not None:
                diagnostics.append("transport_close:" + str(outcome))
                try:
                    control("transport_close", {"outcome": str(outcome)})
                except (OSError, ValueError, PlatformError):
                    diagnostics.append("transport_close_record_not_confirmed")

    def send_request(request: dict[str, Any]) -> None:
        now, monotonic = clock.now()
        if now >= deadline or monotonic - started_monotonic >= config.max_duration_ns:
            raise CaptureDeadline
        control("public_request", {"request": request})
        assert transport is not None
        transport.send(request)

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
            if transport.simulated is not expected_simulated:
                raise AccessDenied(
                    "Transport classification differs from the admitted configuration."
                )
            sessions += 1
            session_started = clock.now()[1]
            last_message = session_started
            protocol = KrakenProtocol()
            subscribed = False
            control("session_start", {"attempt": sessions, "deadline_utc_ns": deadline})
            try:
                transport.connect(config.endpoint)
                for request in protocol.requests_for_preflight():
                    send_request(request)
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
                    if isinstance(config, PilotConfiguration):
                        if market_rows >= config.max_market_rows:
                            reason = "market_row_limit"
                            break
                        if (
                            not protocol.ready
                            and monotonic - session_started >= config.handshake_timeout_ns
                            or monotonic - last_message >= config.idle_timeout_ns
                        ):
                            raise TimeoutError("Public feed handshake or idle deadline exceeded.")
                    try:
                        raw = transport.receive(min(config.receive_timeout_ns, remaining))
                    except ReceivePollTimeout:
                        continue
                    received, received_monotonic = (
                        clock.now()
                    )  # application delivery, before parsing
                    last_message = received_monotonic
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
                    if result.kind == "market":
                        market_rows += len(exact_ws_json(raw)["data"])
                    if protocol.preflight_ready and not subscribed:
                        for request in protocol.market_requests():
                            send_request(request)
                        subscribed = True
            except CaptureDeadline:
                reason = "duration_limit"
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
        "real_capture": not expected_simulated,
    }


class KrakenCaptureService:
    """Platform service using the existing store, normalizer port and data-only replay."""

    def __init__(self, store: ArtifactStore, policy: Policy, directory: Path) -> None:
        self.store, self.policy, self.directory = store, policy, directory

    def journal(
        self, capture_id: str, config: CaptureConfig, principal: Principal
    ) -> CaptureJournal:
        self.policy.require(principal, "worker.execute", partition=config.partition)
        config = validated_config(config)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", capture_id):
            raise ValueError("Use a bounded portable capture identity, not a path.")
        journal = CaptureJournal(
            self.store,
            self.directory / capture_id,
            capture_id=capture_id,
            config_hash=config.digest,
            limits=config.limits,
            synthetic=config.synthetic,
            rights_reference=(
                config.rights_reference
                if isinstance(config, PilotConfiguration)
                else "synthetic-technical-fixture"
            ),
        )
        if self.store.put(canonical_bytes(config.model_dump(mode="json")), "json") != config.digest:
            raise ValueError("Configuration artifact identity changed.")
        return journal

    def run_simulated(
        self,
        capture_id: str,
        config: CaptureConfig,
        principal: Principal,
        factory: Callable[[int], FrameTransport],
        clock: ReceiptClock,
        stop_requested: Callable[[], bool] = lambda: False,
    ) -> dict[str, Any]:
        if not isinstance(config, CaptureConfiguration):
            raise AccessDenied(
                "Simulated entry point requires its original synthetic configuration."
            )
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

    def run_public_pilot(
        self,
        capture_id: str,
        config: PilotConfiguration,
        principal: Principal,
        approval: PilotApproval,
        *,
        clock: ReceiptClock,
        factory: Callable[[int], FrameTransport],
        host_id: str | None = None,
        stop_requested: Callable[[], bool] = lambda: False,
    ) -> dict[str, Any]:
        self.policy.require(principal, "worker.execute", partition=config.partition)
        config = PilotConfiguration.model_validate(config.model_dump())
        approval.require(capture_id, config, clock.now()[0], host_id or socket.gethostname())
        journal = self.journal(capture_id, config, principal)
        approval_hash = self.store.put(canonical_bytes(approval.model_dump(mode="json")), "json")
        with journal.capture_lease():
            capture = _collect(
                journal, config, factory, clock, stop_requested, expected_simulated=False
            )
        if journal.checkpoint.pending_intent:
            return {
                "status": "blocked_pending_recovery",
                "capture": capture,
                "synthetic": False,
                "approval_hash": approval_hash,
            }
        try:
            result = self.inspect(capture_id, config, principal)
        except (ValueError, OSError, PlatformError) as error:
            return {
                "status": "blocked_normalization",
                "capture": capture,
                "synthetic": False,
                "approval_hash": approval_hash,
                "error_type": type(error).__name__,
            }
        checks = {
            "data_integrity_and_replay": True,
            "both_channels_observed": set(result["channels_seen"]) == {"trade", "ticker"},
            "target_duration_completed": capture["reason"] == "duration_limit",
            "local_shutdown_confirmed": any(
                d.startswith("transport_close:") for d in capture["diagnostics"]
            )
            and "transport_close_not_confirmed" not in capture["diagnostics"],
        }
        return {
            **result,
            "capture": capture,
            "approval_hash": approval_hash,
            "pilot_acceptance": {
                "checks": checks,
                "passed": all(checks.values()),
                "scope": "finite data QA only; provider completeness remains unknown",
            },
        }

    def inspect(
        self,
        capture_id: str,
        config: CaptureConfig,
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
        config: CaptureConfig,
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
        data_class: Literal["synthetic", "exposed_structural_only"] = (
            "synthetic" if config.synthetic else "exposed_structural_only"
        )
        source = SourceSpec(
            source_id="kraken-ws-v2",
            source_version="1",
            source_schema=SCHEMA,
            locator=(
                f"internal:{'simulated' if config.synthetic else 'public'}-capture:{capture_id}"
            ),
            rights=(
                config.rights_reference
                if isinstance(config, PilotConfiguration)
                else "Invented transport fixtures; no market-data acquisition."
            ),
            acquired_ns=frames[-1].received_ns if frames else 0,
            raw_sha256=digest,
            size_bytes=len(manifest),
            data_class=data_class,
        )
        archive = LocalArchive(self.store)
        imported = archive.import_step(path, source, max_chunks=1000)
        if imported.archive_hash is None:
            raise ValueError("Bounded capture manifest import remains incomplete.")
        record, declaration, raw = archive.read(imported.archive_hash)
        normalizer = KrakenWSNormalizer(self.store, synthetic=config.synthetic)
        normalized = normalizer.normalize_with_provenance(
            raw, declaration, record.source_manifest_hash
        )
        replay = MarketReplay().inspect_capture(
            normalized.events, data_class=data_class, until_ns=until_ns, checkpoint=checkpoint
        )
        sidecar = self.store.put(canonical_bytes(normalized.model_dump(mode="json")), "json")
        replay_hash = self.store.put(canonical_bytes(replay.model_dump(mode="json")), "json")
        return {
            "status": "technical_qa",
            "synthetic": config.synthetic,
            "financial_validation": False,
            "capture_id": capture_id,
            "config_hash": config.digest,
            "journal_checkpoint": journal.checkpoint.model_dump(mode="json"),
            "upstream_completeness": "unknown",
            "archive_hash": imported.archive_hash,
            "normalization_hash": sidecar,
            "replay_hash": replay_hash,
            "market_events": len(replay.events),
            "channels_seen": sorted({e.stream_id.split("-")[0] for e in replay.events}),
            "checkpoint": replay.checkpoint.model_dump(mode="json"),
        }
