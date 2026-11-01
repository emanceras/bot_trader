"""Summarize preserved M/R/E receipts without rerunning a technical case."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path


def records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def size(path: Path) -> int:
    total = 0
    for directory, _, files in os.walk(path):
        for name in files:
            item = Path(directory) / name
            if item.is_file() and not item.is_symlink():
                total += item.stat().st_size
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packages = {}
    for name in ("M", "R", "E"):
        root = args.scratch / name
        runs = records(root / "runs.jsonl")
        transfers = records(root / "downloads.jsonl")
        # runtime_guard fetch receipts have an output path and are not enclosed
        # in a guarded child. Git/NuGet proxy receipts are enclosed: do not add
        # their duration a second time to actual measured active wall time.
        standalone = [r for r in transfers if "output" in r]
        packages[name] = {
            "guarded_invocations": len(runs),
            "guard_wall_seconds": sum(r["wall_seconds"] for r in runs),
            "standalone_download_wall_seconds": sum(r["wall_seconds"] for r in standalone),
            "active_wall_seconds": sum(r["wall_seconds"] for r in runs + standalone),
            "guard_cpu_seconds": sum(r["cpu_seconds"] for r in runs),
            "peak_sampled_process_group_rss_bytes": max((r["peak_sampled_process_group_rss_bytes"] for r in runs), default=0),
            "maximum_recorded_scratch_after_command_bytes": max((r["scratch_bytes_after"] for r in runs), default=0),
            "current_scratch_regular_file_bytes": size(root),
            "software_transfer_allowance_bytes_charged": sum(r.get("body_bytes", 0) for r in transfers),
            "resource_stop_reasons": [r["stop_reason"] for r in runs if r.get("stop_reason")],
        }
    result = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "packages": packages,
        "aggregate": {
            "active_wall_seconds": sum(p["active_wall_seconds"] for p in packages.values()),
            "guard_cpu_seconds": sum(p["guard_cpu_seconds"] for p in packages.values()),
            "peak_sampled_process_group_rss_bytes": max(p["peak_sampled_process_group_rss_bytes"] for p in packages.values()),
            "current_scratch_regular_file_bytes": size(args.scratch),
            "software_transfer_allowance_bytes_charged": sum(p["software_transfer_allowance_bytes_charged"] for p in packages.values()),
        },
        "measurement_limits": [
            "Recorded machine setup/test time, including failed invocations; excludes interruption time and unmeasured engineering/review effort.",
            "Active time includes standalone wheel/SDK downloads once; nested Git/NuGet transfer time is already included in guarded invocations.",
            "Wheel/SDK counts are response body bytes; Git/NuGet counts conservatively include TLS traffic in both directions, excluding unknown lower-level overhead.",
            "RSS is sampled every100ms; recorded scratch after commands/current bytes are not a continuous peak certificate.",
            "Packages ran sequentially under one lock. No services were contracted; personal time/electricity costs were not estimated.",
        ],
    }
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
