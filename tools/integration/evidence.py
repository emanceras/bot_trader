"""Compact, reconstructible public-source snapshots backed by immutable Git refs."""

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

SOURCE_PATHS = (
    "src",
    "tests",
    "tools/integration",
    "pyproject.toml",
    "uv.lock",
    "AGENTS.md",
    "STATE.md",
    "DECISIONS.md",
    "EXPERIMENTS.md",
    "ROADMAP.md",
    "docs/integration/kraken/budget.json",
    "docs/integration/kraken/sources.json",
    "docs/integration/kraken/capture-spec.json",
    "docs/integration/kraken-ws/budget.json",
)


def git(repo, *args, env=None, input=None):
    return subprocess.check_output(["git", *args], cwd=repo, env=env, input=input)


def snapshot(repo: Path, scratch: Path, label: str) -> tuple[dict, bytes]:
    """Preserve dirty sources without changing HEAD, the real index or worktree."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", label):
        raise ValueError("Use a bounded plain evidence label.")
    base = git(repo, "rev-parse", "HEAD").decode().strip()
    ref = "refs/tags/evidence/kraken-" + label
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as temporary:
        env = os.environ | {"GIT_INDEX_FILE": str(Path(temporary) / "index")}
        git(repo, "read-tree", base, env=env)
        paths = [
            p
            for p in SOURCE_PATHS
            if (repo / p).exists() or git(repo, "ls-tree", "--name-only", base, "--", p).strip()
        ]
        git(repo, "add", "--all", "--", *paths, env=env)
        tree = git(repo, "write-tree", env=env).decode().strip()
        manifest = {}
        entries = git(repo, "ls-files", "-z", "--", *paths, env=env).split(b"\0")
        for entry in filter(None, entries):
            name = entry.decode()
            path = repo / name
            if path.is_symlink() or not path.is_file():
                raise ValueError("Only regular public source files may enter a snapshot.")
            saved = git(repo, "show", f"{tree}:{name}")
            if path.read_bytes() != saved:
                raise RuntimeError("Source changed during snapshot: " + name)
            manifest[name] = hashlib.sha256(saved).hexdigest()
        commit = (
            git(
                repo,
                "commit-tree",
                tree,
                "-p",
                base,
                input=("Technical evidence " + label + "\n").encode(),
            )
            .decode()
            .strip()
        )
        git(repo, "update-ref", ref, commit, "")
    patch = git(repo, "diff", "--binary", base, commit)
    return {
        "schema_version": 2,
        "base_commit": base,
        "snapshot_commit": commit,
        "snapshot_tree": tree,
        "evidence_ref": ref,
        "files": manifest,
        "source_paths": list(SOURCE_PATHS),
        "patch_sha256": hashlib.sha256(patch).hexdigest(),
        "reconstruct": f"git fetch origin {ref}; git show {commit}:PATH",
    }, patch


def write_snapshot(repo: Path, scratch: Path, output: Path, label: str) -> dict:
    record, patch = snapshot(repo, scratch, label)
    (output / "source-manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    (output / "source.diff").write_bytes(patch)
    return record
