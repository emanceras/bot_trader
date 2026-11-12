"""Bounded offline checks with compact Git evidence and an explicit campaign budget."""

import argparse
import fcntl
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

from append_only import verify_published_prefix
from evidence import write_snapshot

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/technical_admission"))
from runtime_guard import group_rss, restrict  # noqa: E402


def tree_bytes(root):
    return sum(p.stat().st_size for p in root.rglob("*") if p.is_file() and not p.is_symlink())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--budget", type=Path, required=True)
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    budget = json.loads(args.budget.read_text())
    root = Path(budget["scratch_root"])
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise ValueError("A concrete command is required.")
    root.mkdir(exist_ok=True)
    if args.child:
        os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:budget["cpus"]])
        restrict(root, False)
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
            "PYTHONDONTWRITEBYTECODE": "1", "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1", "RAYON_NUM_THREADS": str(budget["cpus"]),
            "TMPDIR": str(root / "tmp"), "SLICE_EVIDENCE_DIR": str(output / "private"),
        }
        started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        started = time.monotonic()
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak = disk_peak = 0
        stopped = None
        with (output / "output.log").open("xb") as log:
            proc = subprocess.Popen(
                [sys.executable, __file__, "--child", "--budget", str(args.budget.resolve()),
                 args.label, "--", *command], cwd=REPO, env=environment,
                stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
            )
            while proc.poll() is None:
                peak = max(peak, group_rss(proc.pid))
                size = tree_bytes(root) + max(0, tree_bytes(objects)-object_baseline)
                size += sum(tree_bytes(Path(p)) for p in budget.get("additional_temp_roots", []))
                disk_peak = max(disk_peak, size)
                if time.monotonic() - started > min(budget["command_seconds"], remaining):
                    stopped = "time_budget"
                if peak > budget["ram_bytes"] * .9:
                    stopped = "memory_guard"
                if disk_peak > budget["temporary_bytes"]:
                    stopped = "disk_guard"
                if stopped:
                    os.killpg(proc.pid, signal.SIGKILL)
                    break
                time.sleep(.1)
            code = proc.wait()
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        record = dict(
            schema_version=2, label=args.label, command=command, exit_code=code,
            wall_seconds=time.monotonic()-started,
            cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
            peak_sampled_rss_bytes=peak, peak_sampled_temporary_bytes=disk_peak,
            stop_reason=stopped, started_utc=started_utc,
            completed_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            budget=budget, source_commit=source["snapshot_commit"], evidence_ref=source["evidence_ref"],
            network="IPv4/IPv6 denied; no new datasets/software downloads",
            limits="CPU affinity; sampled RSS/disk, not hard peak certification; private output not exported",
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
