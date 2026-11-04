"""Read-only final integrity audit; this does not execute package/financial cases."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text())
    mismatches = []
    checks = {}
    for key, root in (("files", args.repository), ("venv_files", args.repository / ".venv")):
        entries = baseline[key]
        for name, expected in entries.items():
            path = root / name
            if not path.is_file() or path.is_symlink() or sha(path) != expected:
                mismatches.append(f"{key}:{name}")
        checks[key] = len(entries)
    venv = args.repository / ".venv"
    current = {str(p.relative_to(venv)) for p in venv.rglob("*") if p.is_file() and not p.is_symlink()}
    additions = sorted(current - set(baseline["venv_files"]))
    protected = [
        "src", "tests", "web", "migrations", "scripts", "pyproject.toml", "uv.lock", "alembic.ini",
        "RESEARCH.md", "HYPOTHESES.md", "docs/research", "docs/phase-ii",
        "docs/en/phase-iv/protocol.md", "docs/es/phase-iv/protocol.md",
        "docs/phase-iv/freeze-template.json", "docs/en/phase-iv/staged-amendment.md",
        "docs/es/phase-iv/staged-amendment.md", "docs/en/ux-evolution.md", "docs/es/ux-evolution.md",
        "docs/phase-iv/admission", "tools/admission",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", baseline["source_commit"], "--", *protected],
        cwd=args.repository, text=True,
    ).splitlines()
    result = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "base_commit": baseline["source_commit"], "baseline_sha256": sha(args.baseline),
        "checked": checks, "mismatches": mismatches,
        "new_regular_venv_files": additions, "protected_paths_changed": changed,
        "passed": not (mismatches or additions or changed),
        "limits": [
            "Verifies the recorded regular files; original baseline excludes symlink targets and runtime state.",
            "No credentials or financial archives read; no claim of hostile-code write confinement.",
            "A source/hash match is integrity evidence, not proof of financial or upstream correctness.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
