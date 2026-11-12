"""Tiny Git repositories exercise reconstructible dirty failures without tree copies."""

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


def module(name):
    path = Path(__file__).resolve().parents[1] / "tools/integration" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


EVIDENCE = module("evidence")
EXPORT = module("export_evidence")


def test_uncommitted_failed_source_reconstructs_exactly_without_touching_index(tmp_path):
    repo, scratch = tmp_path / "repo", tmp_path / "scratch"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    for key, value in (("user.name", "Test"), ("user.email", "test@example.invalid")):
        subprocess.run(["git", "config", key, value], cwd=repo, check=True)
    (repo / "src").mkdir()
    program = repo / "src/canary.py"
    program.write_text("assert 1 == 1\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
    index_before = (repo / ".git/index").read_bytes()
    program.write_text("assert 1 == 2, 'deliberate negative control'\n")
    original = program.read_bytes()
    record, patch = EVIDENCE.snapshot(repo, scratch, "test-failure")
    assert (repo / ".git/index").read_bytes() == index_before
    assert program.read_bytes() == original
    assert record["files"]["src/canary.py"] == hashlib.sha256(original).hexdigest()
    assert hashlib.sha256(patch).hexdigest() == record["patch_sha256"]
    saved = EVIDENCE.git(repo, "show", record["snapshot_commit"] + ":src/canary.py")
    restored = subprocess.run(["python", "-c", saved.decode()], capture_output=True)
    assert restored.returncode == 1 and b"deliberate negative control" in restored.stderr
    program.write_text("assert 1 == 1\n")
    assert EVIDENCE.git(repo, "show", record["evidence_ref"] + ":src/canary.py") == original
    with pytest.raises(subprocess.CalledProcessError):
        EVIDENCE.snapshot(repo, scratch, "test-failure")
    assert not list(scratch.rglob("canary.py"))


def test_export_is_immutable_and_excludes_private_market_and_full_source(tmp_path):
    scratch, out = tmp_path / "private", tmp_path / "public"
    check = scratch / "a-failure"
    check.mkdir(parents=True)
    row = {"schema_version": 2, "label": "a-failure", "exit_code": 1, "wall_seconds": 0.1}
    (scratch / "checks.jsonl").write_text(json.dumps(row) + "\n")
    for name in EXPORT.PUBLIC_FILES:
        (check / name).write_text("public receipt only\n")
    (check / "private").mkdir()
    (check / "private/market.csv").write_text("private record must not be exported\n")
    (check / "source").mkdir()
    (check / "source/example.py").write_text("pass\n")
    assert EXPORT.export(scratch, out, "a") == 1
    first = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()}
    assert EXPORT.export(scratch, out, "a") == 1
    assert not list(out.rglob("market.csv")) and not list(out.rglob("example.py"))
    assert first == {str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()}
    (check / "output.log").write_text("altered evidence\n")
    with pytest.raises(RuntimeError, match="Previously exported"):
        EXPORT.export(scratch, out, "a")


def test_old_evidence_export_is_refused_not_rewritten(tmp_path):
    (tmp_path / "checks.jsonl").write_text('{"label":"h1-old","wall_seconds":1}\n')
    with pytest.raises(ValueError, match="Historical evidence is frozen"):
        EXPORT.export(tmp_path, tmp_path / "out", "h1")
