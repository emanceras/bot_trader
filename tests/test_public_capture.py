"""Invented messages exercise the future public branch; these are not observed market data.

Every transport below is an in-process test double. No DNS, socket or provider access occurs.
"""

import json

import pytest
from test_capture_service import ADMIN, BASE, Clock, Transport, handshake, ticker, trade

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import canonical_bytes
from bot_trader.core.security import Policy
from bot_trader.market_data.capture_authority import PilotApproval, PilotConfiguration
from bot_trader.market_data.capture_service import KrakenCaptureService, ReceivePollTimeout
from bot_trader.market_data.replay import CaptureReplayCheckpoint
from bot_trader.market_data.storage import LocalArtifactStore

HOST = "fixture-host"


class PublicBranchFixture(Transport):
    """Only classification matches the future connector; all messages are invented."""

    simulated = False
    close_outcome = "local_closed_remote_unknown"


def pilot(tmp_path, **options):
    store = LocalArtifactStore(tmp_path / "artifacts", max_bytes=32 * 1024 * 1024)
    service = KrakenCaptureService(store, Policy(), tmp_path / "captures")
    config = PilotConfiguration(rights_reference="fixture-rights", **options)
    approval = PilotApproval(
        approved=True,
        capture_id="pilot",
        config_hash=config.digest,
        approved_by="fixture-user",
        decision_reference="invented-approval-for-unit-test-only",
        rights_reference=config.rights_reference,
        host_id=HOST,
        not_before_ns=BASE,
        expires_ns=BASE + 1_000_000_000_000,
    )
    return service, config, approval, Clock()


def run(service, config, approval, clock, factory, **options):
    return service.run_public_pilot(
        "pilot",
        config,
        ADMIN,
        approval,
        clock=clock,
        factory=factory,
        host_id=HOST,
        **options,
    )


@pytest.mark.parametrize(
    "changed",
    [
        {"approved": False},
        {"config_hash": "0" * 64},
        {"host_id": "another-host"},
        {"capture_id": "another-capture"},
        {"rights_reference": "other-rights"},
        {"not_before_ns": BASE + 1_000_000_000},
        {"expires_ns": BASE + 300_000_000_000},
    ],
)
def test_public_approval_binding_rejects_before_factory_or_journal(tmp_path, changed):
    service, config, approval, clock = pilot(tmp_path)

    def forbidden(_):
        pytest.fail("Unapproved pilot reached transport factory.")

    with pytest.raises(AccessDenied):
        run(service, config, approval.model_copy(update=changed), clock, forbidden)
    assert not service.directory.exists()


def test_public_approval_requires_administrator_and_simulated_entry_stays_closed(tmp_path):
    service, config, approval, clock = pilot(tmp_path)

    def forbidden(_):
        pytest.fail("Denied caller reached transport factory.")

    with pytest.raises(AccessDenied):
        service.run_public_pilot(
            "pilot",
            config,
            Principal(id="reader", role="viewer"),
            approval,
            clock=clock,
            factory=forbidden,
            host_id=HOST,
        )
    with pytest.raises(AccessDenied):
        service.run_simulated("pilot", config, ADMIN, forbidden, clock)
    assert not service.directory.exists()


def test_public_branch_preserves_declaration_eur_receipts_and_replay(tmp_path):
    service, config, approval, clock = pilot(tmp_path)
    transport = PublicBranchFixture(clock, handshake() + [trade(), ticker()])
    result = run(service, config, approval, clock, lambda _: transport)
    assert result["status"] == "technical_qa"
    assert result["synthetic"] is False and not result["financial_validation"]
    assert result["capture"]["real_capture"] is True  # tested branch, not evidence of real I/O
    assert result["market_events"] == 2 and transport.closed
    journal = service.journal("pilot", config, ADMIN)
    assert journal.read_frame(journal.frames()[-1]) == canonical_bytes(ticker())
    header = json.loads((service.directory / "pilot" / "capture.json").read_bytes())
    assert header["synthetic"] is False and header["rights_reference"] == "fixture-rights"
    assert json.loads(service.store.get(result["approval_hash"], "json")) == approval.model_dump(
        mode="json"
    )
    archive = json.loads(service.store.get(result["archive_hash"], "json"))
    source = json.loads(service.store.get(archive["source_manifest_hash"], "json"))
    assert source["data_class"] == "exposed_structural_only"
    assert source["rights"] == "fixture-rights"
    normalized = json.loads(service.store.get(result["normalization_hash"], "json"))
    assert all(event["quote_currency"] == "EUR" for event in normalized["events"])
    assert normalized["events"][1]["data"]["origin"] == "observed"
    assert normalized["events"][0]["received_ns"] == journal.frames()[4].received_ns
    assert any(
        record.kind == "transport_close"
        and record.details["outcome"] == "local_closed_remote_unknown"
        for record in journal.records()
    )
    receipt = normalized["events"][0]["received_ns"]
    before = service.inspect("pilot", config, ADMIN, until_ns=receipt - 1)
    prefix = service.inspect("pilot", config, ADMIN, until_ns=receipt)
    assert before["market_events"] == 0 and prefix["market_events"] == 1
    checkpoint = CaptureReplayCheckpoint.model_validate(prefix["checkpoint"])
    restarted = KrakenCaptureService(service.store, Policy(), service.directory)
    resumed = restarted.inspect("pilot", config, ADMIN, checkpoint=checkpoint)
    assert resumed["checkpoint"] == result["checkpoint"] and resumed["market_events"] == 2
    repeated = restarted.inspect("pilot", config, ADMIN)
    assert repeated["replay_hash"] == result["replay_hash"]


def test_short_empty_polls_do_not_reconnect_or_invent_messages(tmp_path):
    service, config, approval, clock = pilot(tmp_path)
    transport = PublicBranchFixture(
        clock,
        handshake() + [trade(), ReceivePollTimeout(), ReceivePollTimeout(), ticker()],
        step_ns=1_000_000_000,
    )
    result = run(service, config, approval, clock, lambda _: transport)
    assert result["market_events"] == 2
    assert result["capture"]["sessions_started"] == 1
    records = service.journal("pilot", config, ADMIN).records()
    assert not any(record.kind == "coverage_gap" for record in records)
    assert len([record for record in records if record.kind == "frame"]) == 6


def test_idle_feed_reconnects_at_declared_deadline_and_preserves_duplicate_receipt(tmp_path):
    service, config, approval, clock = pilot(tmp_path, max_reconnects=1, reconnect_delay_ns=1)
    first = PublicBranchFixture(
        clock,
        handshake() + [trade(), ticker()] + [ReceivePollTimeout() for _ in range(15)],
        step_ns=1_000_000_000,
    )
    second = PublicBranchFixture(clock, handshake() + [trade(), trade(2)])
    created = []

    def factory(index):
        created.append(index)
        return (first, second)[index]

    result = run(service, config, approval, clock, factory)
    assert created == [0, 1] and first.closed and second.closed
    assert len(first.timeouts) == 21  # six frames then fifteen one-second empty polls
    assert result["market_events"] == 3
    records = service.journal("pilot", config, ADMIN).records()
    gaps = [record for record in records if record.kind == "coverage_gap"]
    assert len(gaps) == 1 and gaps[0].details["coverage"] == "unknown"
    sidecar = json.loads(service.store.get(result["normalization_hash"], "json"))
    assert sum(row["duplicate_delivery"] for row in sidecar["rows"]) == 1
    assert any(record.kind == "transport_close" for record in records)


def test_heartbeats_cannot_keep_an_unacknowledged_handshake_alive(tmp_path):
    service, config, approval, clock = pilot(tmp_path, max_reconnects=0)
    transport = PublicBranchFixture(
        clock, [{"channel": "heartbeat"} for _ in range(30)], step_ns=1_000_000_000
    )
    result = run(service, config, approval, clock, lambda _: transport)
    assert result["capture"]["reason"] == "reconnect_limit"
    assert result["capture"]["sessions_started"] == 1 and transport.closed
    assert len(transport.timeouts) == 15
    assert result["market_events"] == 0
    gaps = [
        r for r in service.journal("pilot", config, ADMIN).records() if r.kind == "coverage_gap"
    ]
    assert len(gaps) == 1 and gaps[0].details["cause"] == "TimeoutError"


def test_row_stop_keeps_whole_final_message_and_does_not_read_later_information(tmp_path):
    service, config, approval, clock = pilot(tmp_path, max_market_rows=2)
    batch = trade()
    batch["data"] += [trade(2)["data"][0], trade(3)["data"][0]]
    transport = PublicBranchFixture(clock, handshake() + [batch, ticker()])
    result = run(service, config, approval, clock, lambda _: transport)
    assert result["capture"]["reason"] == "market_row_limit" and transport.closed
    assert result["market_events"] == 3  # threshold stops after the indivisible received message
    assert len(transport.timeouts) == 5
    frames = service.journal("pilot", config, ADMIN).frames()
    assert len(frames) == 5 and frames[-1].raw_sha256
    assert service.journal("pilot", config, ADMIN).read_frame(frames[-1]) == canonical_bytes(batch)
    assert config.max_market_rows + 1000 <= 10_000


def test_finished_public_branch_retry_never_reconnects(tmp_path):
    service, config, approval, clock = pilot(tmp_path)
    first = run(
        service,
        config,
        approval,
        clock,
        lambda _: PublicBranchFixture(clock, handshake() + [trade(), ticker()]),
    )

    def forbidden(_):
        pytest.fail("Terminal capture retry created a transport.")

    repeated = run(service, config, approval, clock, forbidden)
    assert repeated["capture"]["resumed_terminal"] is True
    assert repeated["replay_hash"] == first["replay_hash"]


def test_terminal_pilot_keeps_acceptance_and_durable_authority(tmp_path):
    service, config, approval, clock = pilot(tmp_path)

    class EndAtDeadline(PublicBranchFixture):
        def receive(self, timeout_ns):
            if len(self.timeouts) == 6:
                clock.sleep_ns(config.max_duration_ns)
                return canonical_bytes({"channel": "heartbeat"})
            return super().receive(timeout_ns)

    first = run(
        service,
        config,
        approval,
        clock,
        lambda _: EndAtDeadline(clock, handshake() + [trade(), ticker()]),
    )
    assert first["pilot_acceptance"]["passed"] is True
    records = service.journal("pilot", config, ADMIN).records()
    assert records[0].kind == "capture_authorization"
    assert records[0].details["approval_hash"] == first["approval_hash"]
    second = run(service, config, approval, clock, lambda _: pytest.fail("terminal transport"))
    assert second["pilot_acceptance"] == first["pilot_acceptance"]
    assert service.journal("pilot", config, ADMIN).records() == records


def test_stop_during_connection_prevents_any_subscription(tmp_path):
    service, config, approval, clock = pilot(tmp_path)
    stop = []

    class StopDuringOpen(PublicBranchFixture):
        def connect(self, endpoint):
            super().connect(endpoint)
            stop.append(True)

    transport = StopDuringOpen(clock, [])
    result = run(
        service, config, approval, clock, lambda _: transport, stop_requested=lambda: bool(stop)
    )
    assert result["capture"]["reason"] == "user_stop" and transport.closed
    assert not transport.sent
    assert not result["pilot_acceptance"]["passed"]


def test_real_connector_class_composes_entire_pipeline_with_invented_peer(tmp_path, monkeypatch):
    from test_kraken_transport import FakeConnection

    from bot_trader.market_data.capture_service import FixtureComplete
    from bot_trader.market_data.kraken_transport import KrakenWebSocketTransport

    service, config, approval, clock = pilot(tmp_path)
    peer = FakeConnection(
        [canonical_bytes(m) for m in handshake() + [trade(), ticker()]] + [FixtureComplete()]
    )
    transport = KrakenWebSocketTransport()

    async def fake_dial(endpoint, context):
        assert context.check_hostname and endpoint == config.endpoint
        return peer

    monkeypatch.setattr(transport, "_dial", fake_dial)
    result = run(service, config, approval, clock, lambda _: transport)
    assert result["market_events"] == 2 and result["capture"]["reason"] == "fixture_complete"
    assert transport.close_outcome == "graceful" and transport._loop is None
    assert len(peer.sent) == 3
    repeated = service.inspect("pilot", config, ADMIN)
    assert result["replay_hash"] == repeated["replay_hash"]
