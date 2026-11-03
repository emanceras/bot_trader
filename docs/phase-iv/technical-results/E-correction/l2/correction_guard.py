"""D-050 sub-budget layered on the existing offline M/R/E guard."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import runtime_guard as guard


ROOT = guard.ROOT / "E" / "correction"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preparation", action="store_true")
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    ROOT.mkdir(exist_ok=True)
    pin = ROOT / "budget-baseline.json"
    if not pin.exists():
        pin.write_text(json.dumps({"recorded_utc": datetime.now(timezone.utc).isoformat(),
            "E_scratch_start_bytes": guard.size(ROOT.parent),
            "E_receipts_start": len(guard.rows(ROOT.parent / "runs.jsonl")),
            "software_downloads_start_sha256": __import__('hashlib').sha256((ROOT.parent / 'downloads.jsonl').read_bytes()).hexdigest(),
            "max_test_invocations": 12, "max_additional_wall_seconds": 1800,
            "max_additional_scratch_bytes": 1024**3}, indent=2) + "\n")
    baseline = json.loads(pin.read_text())
    attempts = guard.rows(ROOT / "attempts.jsonl")
    if not args.preparation and sum(not r["preparation"] for r in attempts) >= 12:
        raise RuntimeError("D-050 test invocation limit exhausted")
    since = guard.rows(ROOT.parent / "runs.jsonl")[baseline["E_receipts_start"]:]
    elapsed = sum(r["wall_seconds"] for r in since)
    if elapsed >= 1800:
        raise RuntimeError("D-050 active time exhausted")
    cap = baseline["E_scratch_start_bytes"] + 1024**3
    if guard.size(ROOT.parent) >= cap:
        raise RuntimeError("D-050 additional disk exhausted")
    cpus, memory, disk, transfer, seconds = guard.LIMITS["E"]
    guard.LIMITS["E"] = (cpus, memory, min(disk, cap), transfer, seconds)
    label = "bridge-" + args.label
    if any(r["label"] == label for r in attempts):
        raise RuntimeError("Attempt already reserved; never overwrite")
    guard.append(ROOT / "attempts.jsonl", {"label": label, "preparation": args.preparation,
        "recorded_utc": datetime.now(timezone.utc).isoformat(), "state": "reserved_before_process"})
    # runtime_guard.main normally owns this shared lock; direct run needs it too.
    with (guard.ROOT / "execution.lock").open("a") as lock:
        guard.fcntl.flock(lock, guard.fcntl.LOCK_EX)
        code = guard.run(argparse.Namespace(package="E", label=label, network=False,
            cwd=str(ROOT), seconds=min(600, 1800-elapsed), command=args.command))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
