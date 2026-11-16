"""Bounded checks; network is opt-in for the existing finite public-pilot command only."""

import argparse
import fcntl
import json
import os
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path

from append_only import verify_published_prefix
from evidence import write_snapshot

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/technical_admission"))
from runtime_guard import group_rss, restrict  # noqa: E402


def tree_bytes(root):
    total = 0
    for path in root.rglob("*"):
        try:
            if not path.is_symlink() and path.is_file():
                total += path.stat().st_size
        except FileNotFoundError:
            # Atomic publication removes temporary names while the writer is active.
            continue
    return total


def signal_owned_group(process, signum):
    try:
        os.killpg(process.pid, signum)
    except ProcessLookupError:
        # A child may finish between the last poll and the supervision action.
        pass


def validate_public_pilot(command, budget):
    """Constrain the runner, leaving actual approval validation to the existing CLI."""
    if budget.get("public_pilot") is not True:
        raise ValueError("This campaign does not permit public-pilot execution.")
    if (
        len(command) != 13
        or Path(os.path.abspath(command[0])) != REPO / ".venv/bin/python"
        or command[1:4] != ["-m", "bot_trader.cli", "--state-dir"]
        or command[5:7] != ["capture-pilot", "--capture-id"]
        or command[8] != "--config"
        or command[10] != "--approval"
        or command[12] != "--execute"
    ):
        raise ValueError("Network is limited to the existing public capture-pilot command.")
    root = Path(budget["scratch_root"]).resolve()
    state = Path(command[4]).resolve()
    if state == root or not state.is_relative_to(root):
        raise ValueError("Pilot state must be a private subdirectory of the campaign root.")
    if not all(Path(command[i]).is_file() for i in (9, 11)):
        raise ValueError("Pilot configuration and approval must already exist.")
    if not 5 < budget["command_seconds"] <= 620:
        raise ValueError("A finite public-pilot watchdog of at most 620 seconds is required.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--public-pilot", action="store_true")
    parser.add_argument("--budget", type=Path, required=True)
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    budget = json.loads(args.budget.read_text())
    root = Path(budget["scratch_root"])
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise ValueError("A concrete command is required.")
    if args.public_pilot:
        validate_public_pilot(command, budget)
    root.mkdir(exist_ok=True)
    if args.child:
        os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[: budget["cpus"]])
        restrict(root, args.public_pilot)
        os.execvpe(command[0], command, os.environ)
    with (root / "checks.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = root / "checks.jsonl"
        prior = [json.loads(r) for r in ledger.read_text().splitlines()] if ledger.exists() else []
        remaining = budget["machine_seconds"] - sum(r["wall_seconds"] for r in prior)
        if remaining <= 0:
            raise RuntimeError("Campaign machine budget exhausted.")
        baseline = budget["published_baseline_commit"]
        history = verify_published_prefix(REPO, baseline)
        output = root / args.label
        output.mkdir(exist_ok=False)
        (root / "tmp").mkdir(exist_ok=True)
        initial = root / "resource-baseline.json"
        objects = REPO / ".git/objects"
        if not initial.exists():
            initial.write_text(json.dumps({"git_object_bytes": tree_bytes(objects)}) + "\n")
        object_baseline = json.loads(initial.read_text())["git_object_bytes"]
        source = write_snapshot(REPO, root / "tmp", output, args.label)
        (output / "history-prefix.json").write_text(json.dumps(history, indent=2) + "\n")
        environment = os.environ | {
            "PYTHONDONTWRITEBYTECODE": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "RAYON_NUM_THREADS": str(budget["cpus"]),
            "TMPDIR": str(root / "tmp"),
            "SLICE_EVIDENCE_DIR": str(output / "private"),
        }
        started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        started = time.monotonic()
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak = disk_peak = 0
        stopped = None
        monitor_error_type = None
        termination_requested = False
        allowance = min(budget["command_seconds"], remaining)
        with (output / "output.log").open("xb") as log:
            proc = subprocess.Popen(
                [
                    sys.executable,
                    __file__,
                    "--child",
                    *(["--public-pilot"] if args.public_pilot else []),
                    "--budget",
                    str(args.budget.resolve()),
                    args.label,
                    "--",
                    *command,
                ],
                cwd=REPO,
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                while proc.poll() is None:
                    peak = max(peak, group_rss(proc.pid))
                    size = tree_bytes(root) + max(0, tree_bytes(objects) - object_baseline)
                    size += sum(
                        tree_bytes(Path(p)) for p in budget.get("additional_temp_roots", [])
                    )
                    disk_peak = max(disk_peak, size)
                    elapsed = time.monotonic() - started
                    if elapsed > allowance - (5 if args.public_pilot else 0):
                        stopped = "time_budget"
                    if peak > budget["ram_bytes"] * 0.9:
                        stopped = "memory_guard"
                    if disk_peak > budget["temporary_bytes"]:
                        stopped = "disk_guard"
                    if stopped:
                        # Reserve the last five seconds inside the hard bound for local shutdown.
                        # Resource guards remain immediate through the grace period.
                        if args.public_pilot and stopped == "time_budget" and elapsed < allowance:
                            if not termination_requested:
                                signal_owned_group(proc, signal.SIGTERM)
                                termination_requested = True
                            time.sleep(0.1)
                            continue
                        signal_owned_group(proc, signal.SIGKILL)
                        break
                    time.sleep(0.1)
            except (Exception, KeyboardInterrupt) as error:
                # A failed supervisor must not silently leave an acquisition child running.
                # Preserve the exception type, never potentially private exception payloads.
                stopped = "supervisor_error"
                monitor_error_type = type(error).__name__
                signal_owned_group(proc, signal.SIGKILL)
            child_code = proc.wait()
            code = 2 if monitor_error_type is not None else child_code
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        record = dict(
            schema_version=2,
            label=args.label,
            command=command,
            exit_code=code,
            child_exit_code=child_code,
            wall_seconds=time.monotonic() - started,
            cpu_seconds=after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
            peak_sampled_rss_bytes=peak,
            peak_sampled_temporary_bytes=disk_peak,
            stop_reason=stopped,
            monitor_error_type=monitor_error_type,
            graceful_stop_requested=termination_requested,
            started_utc=started_utc,
            completed_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            budget=budget,
            source_commit=source["snapshot_commit"],
            evidence_ref=source["evidence_ref"],
            network=(
                "IPv4/IPv6 allowed for approved public-pilot CLI; application endpoint/request "
                "allowlist, not a kernel destination firewall"
                if args.public_pilot
                else "IPv4/IPv6 denied; no new datasets/software downloads"
            ),
            limits=(
                "CPU affinity; sampled RSS/disk, not hard peak certification; "
                "private output not exported"
            ),
        )
        (output / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
        with ledger.open("a") as stream:
            stream.write(json.dumps(record) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        print(json.dumps(record))
        raise SystemExit(code)


if __name__ == "__main__":
    main()
