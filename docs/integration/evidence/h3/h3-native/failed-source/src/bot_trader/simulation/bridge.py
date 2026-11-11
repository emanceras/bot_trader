"""Replaceable process boundary for an installed engine; never installs dependencies."""

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Protocol

from bot_trader.core.events import canonical_bytes, content_hash


class SliceExecution(Protocol):
    def execute(self, request: dict[str, Any], directory: Path) -> dict[str, Any]: ...


def verify_journal(data: bytes, result: dict[str, Any]) -> None:
    previous = "0" * 64
    events = []
    for line in data.splitlines():
        row = json.loads(line)
        expected = content_hash({"previous_hash": previous, "event": row["event"]})
        if row["previous_hash"] != previous or row["hash"] != expected:
            raise ValueError("Native journal integrity/continuity failure.")
        events.append(row["event"])
        if events[-1]["sequence"] != len(events):
            raise ValueError("Native journal sequence gap.")
        previous = expected
    if (
        not events
        or events[0]["kind"] != "worker_started"
        or (events[-1]["kind"] != "worker_completed" or events[-1]["status"] != "completed")
    ):
        raise ValueError("Native execution is incomplete; no confirmed final state.")
    if result.get("events") != events or result.get("journal_terminal_hash") != previous:
        raise ValueError("Native output does not match its journal.")


class NativeSliceProcess:
    """Finite synthetic adapter, isolated from the application's Python dependency graph."""

    def __init__(self, python: Path, *, timeout_seconds: int = 60) -> None:
        if not 1 <= timeout_seconds <= 120:
            raise ValueError("Native execution requires a bounded timeout.")
        self.python = python
        self.timeout_seconds = timeout_seconds

    def execute(self, request: dict[str, Any], directory: Path) -> dict[str, Any]:
        if (
            request.get("synthetic") is not True
            or request.get("mode") != "technical"
            or (request.get("partition") != "development")
        ):
            raise ValueError("Native bridge denies non-synthetic/reserved execution.")
        if not self.python.is_file():
            raise ValueError("Isolated runtime absent; automatic installation is forbidden.")
        directory.mkdir(parents=True, exist_ok=False)
        worker = Path(__file__).with_name("native_slice_worker.py")
        request_path, output = directory / "request.json", directory / "result.json"
        request_path.write_bytes(canonical_bytes(request))
        receipt: dict[str, Any] = {
            "request_hash": content_hash(request),
            "worker_sha256": hashlib.sha256(worker.read_bytes()).hexdigest(),
            "runtime": str(self.python),
            "status": "started",
            "automatic_retry": False,
        }
        receipt_path = directory / "transport.json"
        receipt_path.write_bytes(canonical_bytes(receipt))
        try:
            with (directory / "native.log").open("xb") as log:
                process = subprocess.run(
                    [
                        str(self.python),
                        str(worker),
                        "--request",
                        str(request_path),
                        "--output",
                        str(output),
                    ],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    timeout=self.timeout_seconds,
                    check=False,
                )
            receipt["exit_code"] = process.returncode
            if process.returncode != 0 or not output.exists():
                raise ValueError(
                    "Native integration failed; preserved output/state may be unknown."
                )
            result: dict[str, Any] = json.loads(output.read_bytes())
            if (
                result.get("status") != "completed"
                or result.get("errors")
                or (result.get("request_hash") != receipt["request_hash"])
            ):
                raise ValueError("Native result is unconfirmed or bound to a different request.")
            verify_journal(output.with_suffix(".events.jsonl").read_bytes(), result)
            receipt["status"] = "verified_completed"
            return result
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            receipt["status"] = "failed_or_unknown"
            receipt["error"] = str(error)
            raise
        finally:
            receipt_path.write_bytes(canonical_bytes(receipt))
