"""Publish compact receipts and Git diffs; never copy source trees or market data."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUBLIC_FILES = (
    "output.log",
    "receipt.json",
    "source-manifest.json",
    "source.diff",
    "history-prefix.json",
)


def export(scratch: Path, out: Path, milestone: str):
    rows = [json.loads(line) for line in (scratch / "checks.jsonl").read_text().splitlines()]
    selected = [r for r in rows if r["label"].startswith(milestone + "-")]
    out.mkdir(parents=True, exist_ok=True)
    for row in selected:
        if row.get("schema_version") != 2:
            raise ValueError("Historical evidence is frozen; use its recorded exporter if needed.")
        source, target = scratch / row["label"], out / row["label"]
        target.mkdir(exist_ok=True)
        for name in PUBLIC_FILES:
            original, copied = source / name, target / name
            if copied.exists():
                if original.read_bytes() != copied.read_bytes():
                    raise RuntimeError("Previously exported evidence changed: " + str(copied))
            else:
                shutil.copyfile(original, copied)
    # A later invocation set receives a new index; existing indices are never rewritten.
    index_id = hashlib.sha256(json.dumps([r["label"] for r in selected]).encode()).hexdigest()[:16]
    manifest = {
        str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
        for row in selected
        for p in (out / row["label"]).iterdir()
        if p.is_file()
    }
    index = {
        "schema_version": 2,
        "milestone": milestone,
        "invocations": selected,
        "files": manifest,
        "guarded_wall_seconds": sum(r["wall_seconds"] for r in selected),
        "scope": "Technical source/QA evidence; private market records are never copied",
    }
    destination = out / ("index-" + index_id + ".json")
    payload = (json.dumps(index, indent=2) + "\n").encode()
    if destination.exists() and destination.read_bytes() != payload:
        raise RuntimeError("Previously published evidence index changed.")
    if not destination.exists():
        destination.write_bytes(payload)
    return len(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("milestone")
    parser.add_argument("--budget", type=Path, required=True)
    args = parser.parse_args()
    budget = json.loads(args.budget.read_text())
    count = export(
        Path(budget["scratch_root"]),
        REPO / budget["public_evidence"] / args.milestone,
        args.milestone,
    )
    print(json.dumps({"milestone": args.milestone, "receipts": count}))


if __name__ == "__main__":
    main()
