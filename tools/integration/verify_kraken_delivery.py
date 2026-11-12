"""Read-only publication audit and explicit late binding of a documentation input."""

import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

from bot_trader.core.events import datetime_ns

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path("/workspace/kraken-integration")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    protected = [
        "src/bot_trader/core",
        "pyproject.toml",
        "uv.lock",
        "RESEARCH.md",
        "HYPOTHESES.md",
        "docs/research",
        "docs/phase-ii",
        "docs/phase-iv",
        "docs/en",
        "docs/es",
        "docs/integration/evidence",
        "docs/integration/REPORT.md",
        "tools/technical_admission",
        "tools/admission",
        "web",
        "migrations",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "7206eb1", "--", *protected],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert not changed, changed
    assert not subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            "kraken-historical-a",
            "--",
            "docs/integration/kraken/evidence/a",
        ],
        cwd=ROOT,
    )
    entries = json.loads(
        (ROOT / "docs/phase-iv/technical-results/preservation-baseline.json").read_text()
    )["venv_files"]
    for name, expected in entries.items():
        assert digest(ROOT / ".venv" / name) == expected, name
    source_name = "docs/integration/kraken/sources.json"
    source_path = ROOT / source_name
    original = json.loads((SCRATCH / "b-originals/receipt.json").read_text())
    manifest = json.loads((SCRATCH / "b-backend/source-manifest.json").read_text())
    source_hash = digest(source_path)
    assert manifest["files"][source_name] == source_hash
    saved = subprocess.check_output(
        ["git", "show", manifest["snapshot_commit"] + ":" + source_name],
        cwd=ROOT,
    )
    assert hashlib.sha256(saved).hexdigest() == source_hash
    before = max(source_path.stat().st_mtime_ns, source_path.stat().st_ctime_ns)
    assert before < datetime_ns(datetime.fromisoformat(original["started_utc"]))
    summary = json.loads((SCRATCH / "b-originals/output.log").read_text())
    assert summary["status"] == "completed" and summary["signals_generated"] == 0
    assert not summary["engine_invoked"] and not summary["financial_metrics_computed"]
    assert all(case["selected_rows"] == 64 for case in summary["cases"])
    print(
        json.dumps(
            {
                "passed": True,
                "protected_changes": changed,
                "production_regular_files_unchanged": len(entries),
                "originals_summary_sha256": digest(SCRATCH / "b-originals/output.log"),
                "documentation_binding": {
                    "path": source_name,
                    "sha256": source_hash,
                    "bound_in_commit": manifest["snapshot_commit"],
                    "file_metadata_predates_original_run": True,
                    "timing": "Binding recorded after original QA, original receipt left unchanged",
                    "limit": (
                        "Filesystem times support continuity but cannot independently "
                        "prove past content"
                    ),
                },
                "limits": [
                    "Public original-data log inspected: hashes/counts/assumptions only",
                    "No financial values or private sidecars copied; "
                    "runtime symlinks not certified",
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
