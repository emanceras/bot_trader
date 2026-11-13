"""Read-only preservation and bilingual-document checks for the simulated WS delivery."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from append_only import verify_published_prefix

ROOT = Path(__file__).resolve().parents[2]
BASE = "dc859e816ae3fc700f6423f1e32ea849d1f833f3"


def main():
    history = verify_published_prefix(ROOT, BASE)
    protected = [
        "src/bot_trader/core",
        "pyproject.toml",
        "uv.lock",
        "RESEARCH.md",
        "HYPOTHESES.md",
        "docs/research",
        "docs/phase-ii",
        "docs/phase-iv",
        "docs/integration/evidence",
        "docs/integration/REPORT.md",
        "docs/integration/kraken",
        "tools/technical_admission",
        "tools/admission",
        "web",
        "migrations",
        "src/bot_trader/simulation",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--", *protected],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert not changed, changed
    previous = json.loads(
        (ROOT / "docs/phase-iv/technical-results/preservation-baseline.json").read_text()
    )["venv_files"]
    for name, expected in previous.items():
        with (ROOT / ".venv" / name).open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == expected, name
    paths = [ROOT / f"docs/{language}/integration/kraken-ws.md" for language in ("en", "es")]
    links = 0
    for path in paths:
        content = path.read_text()
        assert "2026-11-13" in content
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            assert (path.parent / target.split("#")[0]).exists(), (path, target)
            links += 1
    print(
        json.dumps(
            {
                "passed": True,
                "baseline": BASE,
                "protected_changes": changed,
                "stable_environment_files_unchanged": len(previous),
                "history": history,
                "paired_reports": len(paths),
                "local_report_links": links,
                "scope": "Preservation/document audit only; no market input, engine or financial test",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
