"""Tiny temporary Git histories verify exact preservation and explicit exceptions."""

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "append_only", Path(__file__).resolve().parents[1] / "tools/integration/append_only.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.fixture
def history(tmp_path):
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    for name in MODULE.PROTECTED:
        (tmp_path / name).write_bytes(b"Published first line\r\nPreserved second line\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "Published baseline",
        ],
        cwd=tmp_path,
        check=True,
    )
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    return tmp_path, commit


def test_exact_prefix_accepts_only_append_and_does_not_change_history(history):
    root, commit = history
    original = (root / "DECISIONS.md").read_bytes()
    (root / "DECISIONS.md").write_bytes(original + b"\nNew decision\n")
    result = MODULE.verify_published_prefix(root, commit)
    assert result["accepted"]
    assert all(row["prefix_preserved"] for row in result["files"])
    assert subprocess.check_output(["git", "show", f"{commit}:DECISIONS.md"], cwd=root) == original


@pytest.mark.parametrize("mutation", ["replace", "truncate", "normalize_newlines", "remove"])
def test_unamended_change_is_rejected(history, mutation):
    root, commit = history
    path = root / "EXPERIMENTS.md"
    original = path.read_bytes()
    if mutation == "remove":
        path.unlink()
    else:
        replacement = {
            "replace": b"Replacement history\n",
            "truncate": original[:-1],
            "normalize_newlines": original.replace(b"\r\n", b"\n"),
        }[mutation]
        path.write_bytes(replacement)
    with pytest.raises(ValueError):
        MODULE.verify_published_prefix(root, commit)


def test_mutable_baseline_is_rejected(history):
    root, _ = history
    with pytest.raises(ValueError, match="immutable"):
        MODULE.verify_published_prefix(root, "HEAD")


def test_exception_requires_exact_recorded_amendment(history):
    root, commit = history
    path = root / "DECISIONS.md"
    previous = path.read_bytes()
    replacement = b"Explicit synthetic test correction\n"
    path.write_bytes(replacement)
    amendment = {
        "file": "DECISIONS.md",
        "baseline_commit": commit,
        "previous_sha256": hashlib.sha256(previous).hexdigest(),
        "replacement_sha256": hashlib.sha256(replacement).hexdigest(),
        "amendment_id": "TEST-ONLY-001",
        "reason": "Exercise the exception contract.",
        "authority_reference": "Synthetic test fixture, not project authorization.",
    }
    result = MODULE.verify_published_prefix(root, commit, [amendment])
    assert result["files"][0]["prefix_preserved"] is False
    assert result["files"][0]["explicit_amendment"] == amendment
    for key in ("reason", "authority_reference", "previous_sha256", "replacement_sha256"):
        with pytest.raises(ValueError):
            MODULE.verify_published_prefix(root, commit, [amendment | {key: ""}])
    for key in ("baseline_commit", "previous_sha256", "replacement_sha256"):
        with pytest.raises(ValueError, match="exact"):
            MODULE.verify_published_prefix(root, commit, [amendment | {key: "0" * 64}])
    path.write_bytes(replacement + b"Unrecorded later modification\n")
    with pytest.raises(ValueError, match="exact"):
        MODULE.verify_published_prefix(root, commit, [amendment])
