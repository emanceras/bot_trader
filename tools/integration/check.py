"""Bounded offline development checks with source snapshots, logs and resource receipts."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[2]
ROOT = Path("/workspace/platform-slice")
sys.path.insert(0, str(REPO / "tools/technical_admission"))
from runtime_guard import group_rss, restrict  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", action="store_true")
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    ROOT.mkdir(exist_ok=True)
    if args.child:
        os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:4])
        restrict(ROOT, False)
        os.execvpe(command[0], command, os.environ)
    with (ROOT / "checks.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = ROOT / "checks.jsonl"
        prior = [json.loads(row) for row in ledger.read_text().splitlines()] if ledger.exists() else []
        remaining = 1800 - sum(row["wall_seconds"] for row in prior)
        if remaining <= 0:
            raise RuntimeError("Thirty-minute machine execution budget exhausted")
        output = ROOT / args.label
        output.mkdir(exist_ok=False)
        files = sorted((REPO / "src").rglob("*.py")) + sorted((REPO / "tests").rglob("*.py"))
        files += sorted((REPO / "tests/fixtures/integration").glob("*.json*"))
        files += sorted((REPO / "tools/integration").glob("*.py"))
        files += [REPO / "pyproject.toml", REPO / "uv.lock"]
        hashes = {}
        for path in files:
            relative = path.relative_to(REPO)
            target = output / "source" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            hashes[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
        (output / "source-manifest.json").write_text(json.dumps(hashes, indent=2) + "\n")
        environment = os.environ.copy()
        environment.update(PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1",
                           OMP_NUM_THREADS="1", RAYON_NUM_THREADS="4",
                           SLICE_EVIDENCE_DIR=str(output / "native"))
        started = time.monotonic()
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak = 0
        stopped = None
        with (output / "output.log").open("xb") as log:
            proc = subprocess.Popen([sys.executable, __file__, "--child", args.label,
                                     "--", *command], cwd=REPO, env=environment,
                                    stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            while proc.poll() is None:
                peak = max(peak, group_rss(proc.pid))
                if time.monotonic() - started > min(300, remaining):
                    stopped = "time_budget"
                if peak > 8 * 1024**3 * .9:
                    stopped = "memory_guard"
                if stopped:
                    os.killpg(proc.pid, signal.SIGKILL)
                    break
                time.sleep(.1)
            code = proc.wait()
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        record = dict(label=args.label, command=command, exit_code=code,
                      wall_seconds=time.monotonic()-started,
                      cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                      peak_sampled_rss_bytes=peak, stop_reason=stopped,
                      started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      network="IPv4/IPv6 denied; no new downloads",
                      limits="4 CPU affinity; RSS sampled100ms, not a hard memory certificate")
        (output / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
        with ledger.open("a") as stream:
            stream.write(json.dumps(record) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        print(json.dumps(record))
        raise SystemExit(code)


if __name__ == "__main__":
    main()
