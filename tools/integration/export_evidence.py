"""Copy completed check receipts, preserving failed versions and exact correction diffs."""

import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[2]
SCRATCH = Path("/workspace/platform-slice")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("milestone")
    args = parser.parse_args()
    out = REPO / "docs/integration/evidence" / args.milestone
    out.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in (SCRATCH / "checks.jsonl").read_text().splitlines()]
    selected = [r for r in rows if r["label"].startswith(args.milestone + "-")]
    files = {}
    for row in selected:
        source = SCRATCH / row["label"]
        target = out / row["label"]
        if target.exists():
            for name in ("output.log", "receipt.json", "source-manifest.json"):
                if (source / name).read_bytes() != (target / name).read_bytes():
                    raise RuntimeError("Previously exported evidence changed: " + row["label"])
            continue
        target.mkdir()
        for name in ("output.log", "receipt.json", "source-manifest.json"):
            shutil.copyfile(source / name, target / name)
        if (source / "native").exists():
            shutil.copytree(source / "native", target / "native")
        if row["exit_code"]:
            shutil.copytree(source / "source", target / "failed-source")
            diff = []
            for old in sorted((source / "source").rglob("*.py")):
                relative = old.relative_to(source / "source")
                new = REPO / relative
                if new.exists():
                    diff += difflib.unified_diff(old.read_text().splitlines(True),
                        new.read_text().splitlines(True), fromfile="failed/" + str(relative),
                        tofile="current/" + str(relative))
            (target / "changes-after-failure.diff").write_text("".join(diff))
    for path in out.rglob("*"):
        if path.is_file() and path not in (out / "manifest.json", out / "summary.json"):
            files[str(path.relative_to(out))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (out / "manifest.json").write_text(json.dumps(files, indent=2) + "\n")
    (out / "summary.json").write_text(json.dumps({
        "milestone": args.milestone, "invocations": selected,
        "guarded_wall_seconds": sum(row["wall_seconds"] for row in selected),
        "scope": "Synthetic technical implementation; no financial experiments or downloads",
    }, indent=2) + "\n")
    print(json.dumps({"milestone": args.milestone, "receipts": len(selected)}))


if __name__ == "__main__":
    main()
