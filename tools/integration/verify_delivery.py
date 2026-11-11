"""Read-only preservation audit; does not rerun an engine or financial experiment."""

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    preserved = [
        "pyproject.toml", "uv.lock", "src/bot_trader/core/contracts.py",
        "RESEARCH.md", "HYPOTHESES.md", "docs/research", "docs/phase-ii",
        "docs/phase-iv", "docs/en/phase-iv", "docs/es/phase-iv",
        "docs/en/ux-evolution.md", "docs/es/ux-evolution.md",
        "tools/technical_admission", "tools/admission", "web", "migrations",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "9be75a2", "--", *preserved],
        cwd=ROOT, text=True,
    ).splitlines()
    assert not changed, changed
    historical = subprocess.check_output(
        ["git", "show", "64929d6:DECISIONS.md"], cwd=ROOT,
    )
    assert (ROOT / "DECISIONS.md").read_bytes().startswith(historical)
    experiments = subprocess.check_output(
        ["git", "show", "9be75a2:EXPERIMENTS.md"], cwd=ROOT,
    )
    assert (ROOT / "EXPERIMENTS.md").read_bytes().startswith(experiments)
    baseline = ROOT / "docs/phase-iv/technical-results/preservation-baseline.json"
    entries = json.loads(baseline.read_text())["venv_files"]
    for name, expected in entries.items():
        path = ROOT / ".venv" / name
        assert path.is_file() and not path.is_symlink() and digest(path) == expected, name
    actual = {
        str(p.relative_to(ROOT / ".venv")) for p in (ROOT / ".venv").rglob("*")
        if p.is_file() and not p.is_symlink()
    }
    assert actual == set(entries), sorted(actual.symmetric_difference(entries))
    evidence_count = 0
    for manifest in sorted((ROOT / "docs/integration/evidence").glob("h*/manifest.json")):
        for name, expected in json.loads(manifest.read_text()).items():
            assert digest(manifest.parent / name) == expected, str(manifest.parent / name)
            evidence_count += 1
    print(json.dumps({
        "passed": True,
        "protected_paths_changed": changed,
        "decisions_restored_prefix_bytes": len(historical),
        "experiments_historical_prefix_bytes": len(experiments),
        "production_regular_files_unchanged": len(entries),
        "evidence_hashes_verified": evidence_count,
        "limits": [
            "Baseline excludes symlink targets and runtime state.",
            "Evidence manifests as exported before this audit receipt; no recursive self-proof.",
            "No credentials, financial datasets, engine execution or financial metrics read.",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
