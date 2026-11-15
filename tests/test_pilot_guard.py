"""The evidence runner grants network access only to the finite pilot entry point."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest


@pytest.fixture
def guard(monkeypatch, tmp_path):
    source = Path(__file__).resolve().parents[1] / "tools/integration/check.py"
    monkeypatch.syspath_prepend(str(source.parent))
    spec = importlib.util.spec_from_file_location("pilot_check", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "REPO", tmp_path / "repo")
    return module


def pilot_input(guard, tmp_path):
    root = tmp_path / "private"
    root.mkdir()
    config, approval = root / "config.json", root / "approval.json"
    # This wrapper checks the entry point, not authorization content; the real CLI owns that gate.
    config.write_text("{}")
    approval.write_text("{}")
    budget = {"scratch_root": str(root), "public_pilot": True, "command_seconds": 320, "cpus": 1}
    command = [
        str(guard.REPO / ".venv/bin/python"), "-m", "bot_trader.cli",
        "--state-dir", str(root / "state"), "capture-pilot",
        "--capture-id", "bounded-test", "--config", str(config),
        "--approval", str(approval), "--execute",
    ]
    return budget, command


def test_public_runner_requires_existing_entry_point_and_private_state(guard, tmp_path):
    budget, command = pilot_input(guard, tmp_path)
    guard.validate_public_pilot(command, budget)
    for altered in (
        ["python", *command[1:]],
        [*command, "--inspect"],
        [*command[:-1], "--inspect"],
        command[:4] + [str(tmp_path / "outside")] + command[5:],
        command[:4] + [budget["scratch_root"]] + command[5:],
        command[:10] + ["--approval", str(tmp_path / "missing"), "--execute"],
    ):
        with pytest.raises(ValueError):
            guard.validate_public_pilot(altered, budget)
    for altered_budget in (
        budget | {"public_pilot": False},
        budget | {"public_pilot": 1},
        budget | {"command_seconds": 621},
    ):
        with pytest.raises(ValueError):
            guard.validate_public_pilot(command, altered_budget)


@pytest.mark.parametrize("public", [False, True])
def test_child_network_default_is_denied_and_opt_in_is_forwarded(
    guard, tmp_path, monkeypatch, public
):
    budget, command = pilot_input(guard, tmp_path)
    path = tmp_path / "budget.json"
    path.write_text(json.dumps(budget))
    calls = []
    monkeypatch.setattr(guard.os, "sched_setaffinity", lambda *_: None)
    monkeypatch.setattr(guard, "restrict", lambda root, network: calls.append((root, network)))

    class Executed(Exception):
        pass

    def execvpe(executable, arguments, environment):
        assert executable == command[0] and arguments == command
        raise Executed

    monkeypatch.setattr(guard.os, "execvpe", execvpe)
    monkeypatch.setattr(
        sys, "argv", ["check.py", "--child", *(["--public-pilot"] if public else []),
                      "--budget", str(path), "test", "--", *command],
    )
    with pytest.raises(Executed):
        guard.main()
    assert calls == [(Path(budget["scratch_root"]), public)]


@pytest.mark.parametrize("public", [False, True])
def test_watchdog_reserves_public_shutdown_grace_inside_total_bound(
    guard, tmp_path, monkeypatch, public
):
    budget, command = pilot_input(guard, tmp_path)
    budget.update(
        machine_seconds=1000, ram_bytes=8 * 1024**3, temporary_bytes=512 * 1024**2,
        published_baseline_commit="test-baseline",
    )
    path = tmp_path / "budget.json"
    path.write_text(json.dumps(budget))
    signals = []
    times = iter([0, 316, 318, 320.1, 320.1])
    monkeypatch.setattr(guard.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(guard.time, "sleep", lambda _: None)
    monkeypatch.setattr(guard, "group_rss", lambda _: 1)
    monkeypatch.setattr(guard, "tree_bytes", lambda _: 0)
    monkeypatch.setattr(guard, "verify_published_prefix", lambda *_: {})
    monkeypatch.setattr(
        guard, "write_snapshot", lambda *_: {"snapshot_commit": "test", "evidence_ref": "test"}
    )
    monkeypatch.setattr(guard.os, "killpg", lambda pid, sig: signals.append(sig))

    class UnresponsiveProcess:
        pid = 123

        def poll(self):
            return None

        def wait(self):
            return -9

    monkeypatch.setattr(guard.subprocess, "Popen", lambda *_, **__: UnresponsiveProcess())
    monkeypatch.setattr(
        sys, "argv", ["check.py", *(["--public-pilot"] if public else []),
                      "--budget", str(path), "watchdog", "--", *command],
    )
    with pytest.raises(SystemExit) as result:
        guard.main()
    assert result.value.code == -9
    assert signals == (
        [guard.signal.SIGTERM, guard.signal.SIGKILL] if public else [guard.signal.SIGKILL]
    )
    receipt = json.loads((Path(budget["scratch_root"]) / "watchdog/receipt.json").read_text())
    assert receipt["graceful_stop_requested"] is public
    assert receipt["stop_reason"] == "time_budget"
