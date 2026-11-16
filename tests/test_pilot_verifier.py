"""The offline verifier is exercised with invented messages, never a public feed."""

import importlib.util
from argparse import Namespace
from pathlib import Path

from test_capture_service import handshake, ticker, trade
from test_public_capture import PublicBranchFixture, pilot, run

from bot_trader.core.events import canonical_bytes
from bot_trader.core.settings import Settings
from bot_trader.persistence import Database, migrate


def test_private_capture_verifier_restarts_and_checks_duplicate_causal_prefixes(tmp_path):
    source = Path(__file__).resolve().parents[1] / "tools/integration/verify_pilot.py"
    spec = importlib.util.spec_from_file_location("verify_pilot", source)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    db = Database(Settings(data_dir=tmp_path))
    migrate(db)
    db.close()
    service, config, approval, clock = pilot(tmp_path)

    class EndAtDeadline(PublicBranchFixture):
        def receive(self, timeout_ns):
            if len(self.timeouts) == 7:
                clock.sleep_ns(config.max_duration_ns)
                return canonical_bytes({"channel": "heartbeat"})
            return super().receive(timeout_ns)

    result = run(service, config, approval, clock, lambda _: EndAtDeadline(
        clock, handshake() + [trade(), trade(), ticker()]
    ))
    assert result["pilot_acceptance"]["passed"]
    path = tmp_path / "config.json"
    path.write_text(config.model_dump_json())
    args = Namespace(state_dir=tmp_path, config=path, capture_id="pilot")
    report = {}
    verifier.verify(args, report)
    assert report["passed"], report
    assert report["unique_market_events"] == 2
    assert report["duplicate_trade_deliveries"] == 1
    assert report["causal_boundaries_checked"] == 2
    assert report["checks"]["fresh_process_artifacts_and_checkpoints_identical"]
