"""Read-only preservation audit for the optional public client delivery."""

import hashlib
import json
import re
import subprocess
import tomllib
from pathlib import Path

from append_only import verify_published_prefix

ROOT = Path(__file__).resolve().parents[2]
BASE = "a5e9997da2552186e8373dacf85135c21b86002a"


def previous(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def main():
    protected = [
        "src/bot_trader/core",
        "src/bot_trader/simulation",
        "RESEARCH.md",
        "HYPOTHESES.md",
        "docs/research",
        "docs/phase-ii",
        "docs/phase-iv",
        "docs/integration/evidence",
        "docs/integration/kraken",
        "docs/integration/kraken-ws",
        "docs/integration/REPORT.md",
        "docs/en/integration/kraken-ws.md",
        "docs/es/integration/kraken-ws.md",
        "tools/technical_admission",
        "tools/admission",
        "web",
        "migrations",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--", *protected], cwd=ROOT, text=True
    ).splitlines()
    assert not changed, changed
    history = verify_published_prefix(ROOT, BASE)
    old = tomllib.loads(previous("pyproject.toml").decode())
    new = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert old["project"]["dependencies"] == new["project"]["dependencies"]
    assert old["dependency-groups"] == new["dependency-groups"]
    assert new["project"]["optional-dependencies"] == {"capture": ["websockets==17.4"]}
    old_lock = {p["name"]: p for p in tomllib.loads(previous("uv.lock").decode())["package"]}
    new_lock = {p["name"]: p for p in tomllib.loads((ROOT / "uv.lock").read_text())["package"]}
    assert set(new_lock) - set(old_lock) == {"websockets"}
    for name, package in old_lock.items():
        if name == "bot-trader":
            assert package["dependencies"] == new_lock[name]["dependencies"]
        else:
            assert new_lock[name] == package, name
    entries = json.loads(
        (ROOT / "docs/phase-iv/technical-results/preservation-baseline.json").read_text()
    )["venv_files"]
    for name, expected in entries.items():
        with (ROOT / ".venv" / name).open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == expected, name
    links = 0
    for language in ("en", "es"):
        path = ROOT / f"docs/{language}/integration/kraken-ws-client.md"
        content = path.read_text()
        assert "2026-11-14" in content
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in target and not target.startswith("#"):
                assert (path.parent / target.split("#")[0]).exists(), target
                links += 1
    print(
        json.dumps(
            {
                "passed": True,
                "baseline": BASE,
                "history": history,
                "protected_changes": changed,
                "unchanged_existing_lock_packages": len(old_lock) - 1,
                "optional_addition_only": "websockets17.4",
                "stable_environment_files": len(entries),
                "report_links": links,
                "actual_kraken_connections": 0,
                "limit": "Integrity/dependency preservation; no actual provider/TLS validation",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
