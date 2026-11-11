"""New vertical-path checks, not a rerun of the historical M/R/E engine packages."""

import json
import os
from pathlib import Path

import pytest

from bot_trader.application import build_services
from bot_trader.core.contracts import Principal
from bot_trader.core.settings import Settings
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.replay import ReplayPolicy
from bot_trader.persistence import Database, migrate
from bot_trader.simulation.bridge import NativeSliceProcess
from bot_trader.simulation.slice import SliceConfiguration

FIXTURES = Path(__file__).parent / "fixtures/integration"
PYTHON = Path(
    os.environ.get(
        "BOT_TRADER_NATIVE_PYTHON", "/workspace/technical-admission/E/recovery/venv/bin/python"
    )
)
ADMIN = Principal(id="technical-test", role="admin")
pytestmark = pytest.mark.skipif(
    not PYTHON.is_file() or "SLICE_EVIDENCE_DIR" not in os.environ,
    reason="Requires an explicitly guarded artifact directory and existing isolated rc7 runtime.",
)


@pytest.fixture
def platform(tmp_path):
    settings = Settings(data_dir=tmp_path / "platform", repository_root=Path.cwd())
    db = Database(settings)
    migrate(db)
    db.close()
    services = build_services(settings)
    yield services
    services.database.close()


def execute(services, case, name, config=None):
    source = SourceSpec.model_validate_json((FIXTURES / f"{case}.source.json").read_bytes())
    acquired = services.slice.import_file(FIXTURES / f"{case}.jsonl", source, ADMIN)
    assert acquired.archive_hash
    output = Path(os.environ["SLICE_EVIDENCE_DIR"]) / name
    report = services.slice.run(
        acquired.archive_hash,
        config or SliceConfiguration(),
        ADMIN,
        execution=NativeSliceProcess(PYTHON),
        directory=output,
    )
    (output / "platform-report.json").write_text(json.dumps(report, indent=2) + "\n")
    native = json.loads((output / "result.json").read_text())
    accounting = json.loads(services.slice.store.get(report["accounting_hash"], "json"))
    (output / "accounting.json").write_text(json.dumps(accounting, indent=2) + "\n")
    replay = json.loads(services.slice.store.get(report["replay_hash"], "json"))
    (output / "replay.json").write_text(json.dumps(replay, indent=2) + "\n")
    return report, native, accounting


def test_integrated_native_round_trip_and_determinism(platform):
    first, native, accounting = execute(platform, "roundtrip", "full-a")
    assert first["status"] == "reconciled", accounting["problems"]
    assert [(f["side"], f["quantity"], f["price"], f["fee"]) for f in native["fills"]] == [
        ("buy", "1.00", "105.05", "0.21"),
        ("sell", "1.00", "106.95", "0.21"),
    ]
    assert accounting["cash_usd"] == "1001.48"
    assert accounting["inventory"] == "0" and accounting["fees_usd"] == "0.42"
    assert {o["status"] for o in native["orders"]} == {"FILLED"}
    second, repeated, _ = execute(platform, "roundtrip", "full-b")
    assert second == first
    assert repeated == native


def test_integrated_partial_cancel_then_sell(platform):
    config = SliceConfiguration(
        replay=ReplayPolicy(buy_quantity="2", sell_quantity="1", complete_trade_coverage=True)
    )
    report, native, accounting = execute(platform, "partial", "partial", config)
    assert report["status"] == "reconciled", accounting["problems"]
    buy = next(order for order in native["orders"] if order["side"] == "buy")
    assert (buy["status"], buy["quantity"], buy["filled"], buy["remaining"]) == (
        "CANCELED",
        "2.00",
        "1.00",
        "1.00",
    )
    assert any(event.get("event_type") == "OrderCanceled" for event in native["events"])
    assert [f["quantity"] for f in native["fills"]] == ["1.00", "1.00"]
    assert accounting["cash_usd"] == "1001.48" and accounting["inventory"] == "0"
    assert any(
        order["status"] == "PARTIALLY_FILLED"
        for state in native["snapshots"]
        for order in state["orders"]
    )


def test_integrated_native_rejection_preserves_cash(platform):
    report, native, accounting = execute(
        platform, "roundtrip", "rejection", SliceConfiguration(initial_cash_usd="50")
    )
    assert report["status"] == "reconciled", accounting["problems"]
    assert native["fills"] == [] and len(native["orders"]) == 2
    assert all(order["status"] in ("DENIED", "REJECTED") for order in native["orders"])
    assert accounting["cash_usd"] == "50" and accounting["inventory"] == "0"
    assert accounting["fees_usd"] == "0"
