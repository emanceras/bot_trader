"""Content identities are separate from run timestamps and attempt identifiers."""

import hashlib
import platform
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pydantic import JsonValue

from bot_trader.core.errors import Conflict

PACKAGES = ("bot-trader", "pydantic", "sqlalchemy", "duckdb", "pyarrow", "fastapi")


def code_identity(root: Path) -> dict[str, JsonValue]:
    root = root.resolve()
    paths = sorted((root / "src").rglob("*.py"))
    paths += [root / name for name in ("pyproject.toml", "uv.lock")]
    if not paths or any(not path.is_file() for path in paths):
        raise Conflict(
            "Source tree and locked dependency manifest are required for a technical run."
        )
    digest = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix().encode()
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain", "--untracked-files=all"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            ).stdout
        )
    except (OSError, subprocess.SubprocessError):
        revision, dirty = "unavailable", True
    versions: dict[str, JsonValue] = {}
    for package in PACKAGES:
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "unavailable"
    return {
        "source_sha256": digest.hexdigest(),
        "git_revision": revision,
        "dirty": dirty,
        "uv_lock_sha256": hashlib.sha256((root / "uv.lock").read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "platform": platform.system(),
        "machine": platform.machine(),
        "packages": versions,
    }
