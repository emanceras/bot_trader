"""Finite pilot command orchestration; dry plan is the default and never opens a socket."""

import importlib.metadata
import signal
import socket
import threading
import time
from argparse import Namespace
from typing import Any

from bot_trader.application import build_services
from bot_trader.core.contracts import Principal
from bot_trader.core.events import canonical_bytes
from bot_trader.core.settings import Settings
from bot_trader.market_data.capture_authority import PilotApproval, PilotConfiguration


class SystemReceiptClock:
    def __init__(self) -> None:
        self.stopped = threading.Event()

    def now(self) -> tuple[int, int]:
        return time.time_ns(), time.monotonic_ns()

    def sleep_ns(self, duration_ns: int) -> None:
        self.stopped.wait(duration_ns / 1_000_000_000)


def execute_command(args: Namespace, settings: Settings) -> dict[str, Any]:
    config = PilotConfiguration.model_validate_json(args.config.read_bytes())
    try:
        installed = importlib.metadata.version("websockets")
    except importlib.metadata.PackageNotFoundError:
        installed = None
    if not (args.execute or args.inspect or args.recover_stopped_writer):
        return {
            "status": "plan_only",
            "network_contacted": False,
            "capture_id": args.capture_id,
            "config_hash": config.digest,
            "config": config.model_dump(mode="json"),
            "websockets_required": "17.4",
            "websockets_installed": installed,
            "host_id": socket.gethostname(),
            "execution_authorized": False,
            "requires": [
                "explicit user approval matching this plan",
                "applicable retention rights",
                "synchronized host clock and private POSIX disk",
                "external wall-time watchdog",
            ],
            "normalization_artifact_limit_bytes": 33_554_432,
        }
    clock = SystemReceiptClock()
    approval = None
    if args.execute:
        if args.approval is None:
            raise ValueError("Provide the separately authorized finite pilot approval record.")
        approval = PilotApproval.model_validate_json(args.approval.read_bytes())
        approval.require(args.capture_id, config, clock.now()[0], socket.gethostname())
    if args.execute and installed != "17.4":
        raise ValueError("Install the pinned optional capture extra before an approved pilot.")
    # Dedicated pilot state; larger bounded sidecars don't change the platform default.
    settings = settings.model_copy(update={"max_artifact_bytes": 33_554_432})
    services = build_services(settings)
    administrator = Principal(id="local-admin", role="admin")
    stopped = clock.stopped
    handlers: dict[signal.Signals, Any] = {}
    try:
        if args.inspect:
            report = services.capture.inspect(args.capture_id, config, administrator)
        elif args.recover_stopped_writer:
            journal = services.capture.journal(args.capture_id, config, administrator)
            with journal.capture_lease():
                recovered = journal.recover(
                    writer_stopped=True,
                    session_id="recovery-" + str(clock.now()[0]),
                    received_ns=clock.now()[0],
                    monotonic_ns=clock.now()[1],
                )
            report = {
                "status": "recovery_recorded",
                "network_contacted": False,
                "recovered": recovered.model_dump(mode="json") if recovered else None,
            }
        else:
            from bot_trader.market_data.kraken_transport import KrakenWebSocketTransport

            for signum in (signal.SIGINT, signal.SIGTERM):
                handlers[signum] = signal.signal(signum, lambda *_: stopped.set())
            assert approval is not None
            report = services.capture.run_public_pilot(
                args.capture_id,
                config,
                administrator,
                approval,
                clock=clock,
                factory=lambda _: KrakenWebSocketTransport(
                    max_frame_bytes=config.limits.max_frame_bytes
                ),
                stop_requested=stopped.is_set,
            )
        # Persist a content-addressed technical receipt. No market rows are printed.
        digest = services.capture.store.put(canonical_bytes(report), "json")
        return {**report, "report_hash": digest}
    finally:
        for signum, handler in handlers.items():
            signal.signal(signum, handler)
        services.database.close()
