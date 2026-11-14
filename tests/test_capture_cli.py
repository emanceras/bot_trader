"""Pilot command is exercised offline, including its default no-network boundary."""

import json
import subprocess
import sys
from argparse import Namespace

import pytest

from bot_trader.core.events import canonical_bytes
from bot_trader.core.settings import Settings
from bot_trader.market_data.capture_authority import PilotConfiguration
from bot_trader.market_data.capture_cli import execute_command


def test_cli_dry_plan_never_opens_a_connection_or_creates_state(tmp_path):
    path = tmp_path / "config.json"
    config = PilotConfiguration(rights_reference="pending-retention-review")
    path.write_bytes(canonical_bytes(config.model_dump(mode="json")))
    state = tmp_path / "private"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "bot_trader.cli",
            "--state-dir",
            str(state),
            "capture-pilot",
            "--capture-id",
            "pilot-001",
            "--config",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "plan_only" and not report["network_contacted"]
    assert not report["execution_authorized"] and report["config_hash"] == config.digest
    assert not state.exists()


def test_cli_execute_requires_approval_before_building_services(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(PilotConfiguration(rights_reference="fixture").model_dump_json())
    monkeypatch.setattr(
        "bot_trader.market_data.capture_cli.build_services",
        lambda *_: pytest.fail("Unauthorized capture created services"),
    )
    args = Namespace(
        config=config,
        capture_id="pilot",
        execute=True,
        inspect=False,
        recover_stopped_writer=False,
        approval=None,
    )
    with pytest.raises(ValueError, match="approval"):
        execute_command(args, Settings(data_dir=tmp_path / "private"))


def test_offline_recovery_does_not_require_fresh_network_authorization(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from bot_trader.core.security import Policy
    from bot_trader.market_data.capture_service import KrakenCaptureService
    from bot_trader.market_data.storage import LocalArtifactStore

    config_path = tmp_path / "config.json"
    config_path.write_text(PilotConfiguration(rights_reference="fixture").model_dump_json())
    store = LocalArtifactStore(tmp_path / "artifacts")
    capture = KrakenCaptureService(store, Policy(), tmp_path / "captures")
    services = SimpleNamespace(capture=capture, database=SimpleNamespace(close=lambda: None))
    monkeypatch.setattr("bot_trader.market_data.capture_cli.build_services", lambda _: services)
    args = Namespace(
        config=config_path,
        capture_id="pilot",
        execute=False,
        inspect=False,
        recover_stopped_writer=True,
        approval=None,
    )
    result = execute_command(args, Settings(data_dir=tmp_path / "private"))
    assert result["status"] == "recovery_recorded" and not result["network_contacted"]
