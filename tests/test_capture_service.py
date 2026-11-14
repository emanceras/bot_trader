"""Finite invented transports exercise the existing archive and data-only replay path."""

import json

import pytest

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import canonical_bytes
from bot_trader.core.security import Policy
from bot_trader.market_data.capture import CaptureLimits
from bot_trader.market_data.capture_service import (
    CaptureConfiguration,
    FixtureComplete,
    KrakenCaptureService,
    collect,
)
from bot_trader.market_data.kraken_ws import rfc3339_ns
from bot_trader.market_data.replay import CaptureReplayCheckpoint
from bot_trader.market_data.storage import LocalArtifactStore

STAMP = "2026-01-01T00:00:00.000000123Z"
BASE = rfc3339_ns("2026-01-01T00:00:00Z")
ADMIN = Principal(id="capture-admin", role="admin")


class Clock:
    def __init__(self):
        self.utc = BASE + 1_000_000
        self.monotonic = 10_000

    def now(self):
        return self.utc, self.monotonic

    def sleep_ns(self, duration_ns):
        self.utc += duration_ns
        self.monotonic += duration_ns


class Transport:
    simulated = True

    def __init__(self, clock, messages, *, step_ns=1000):
        self.clock = clock
        self.messages = iter(messages)
        self.step_ns = step_ns
        self.connected = False
        self.closed = False
        self.sent = []
        self.timeouts = []

    def connect(self, endpoint):
        assert endpoint == "wss://ws.kraken.com/v2"
        self.connected = True

    def send(self, request):
        self.sent.append(request)

    def receive(self, timeout_ns):
        self.timeouts.append(timeout_ns)
        self.clock.sleep_ns(self.step_ns)
        try:
            message = next(self.messages)
        except StopIteration:
            raise FixtureComplete from None
        if isinstance(message, BaseException):
            raise message
        return message if isinstance(message, bytes) else canonical_bytes(message)

    def close(self):
        self.closed = True


def handshake():
    acknowledgements = []
    for channel, request in (("instrument", 1), ("trade", 2), ("ticker", 3)):
        result = {"channel": channel, "snapshot": True}
        if channel != "instrument":
            result["symbol"] = "BTC/EUR"
        acknowledgements.append(
            {"method": "subscribe", "success": True, "result": result, "req_id": request}
        )
    instrument = {
        "channel": "instrument",
        "type": "snapshot",
        "data": {
            "pairs": [
                {"symbol": "BTC/EUR", "base": "BTC", "quote": "EUR", "status": "online"},
            ]
        },
    }
    return [acknowledgements[0], instrument, *acknowledgements[1:]]


def trade(identity=1):
    return {
        "channel": "trade",
        "type": "update",
        "data": [
            {
                "symbol": "BTC/EUR",
                "timestamp": STAMP,
                "trade_id": identity,
                "side": "buy",
                "ord_type": "limit",
                "price": "100.125",
                "qty": "0.25",
            }
        ],
    }


def ticker():
    return {
        "channel": "ticker",
        "type": "update",
        "data": [
            {
                "symbol": "BTC/EUR",
                "timestamp": STAMP,
                "bid": "100",
                "ask": "101",
                "bid_qty": "2",
                "ask_qty": "3",
            }
        ],
    }


def setup(tmp_path, **configuration):
    store = LocalArtifactStore(tmp_path / "artifacts")
    service = KrakenCaptureService(store, Policy(), tmp_path / "captures")
    config = CaptureConfiguration(**configuration)
    return service, config, Clock()


def test_end_to_end_capture_archive_normalization_replay_and_repeat(tmp_path):
    service, config, clock = setup(tmp_path)
    transport = Transport(clock, handshake() + [trade(), ticker()])
    result = service.run_simulated("capture", config, ADMIN, lambda _: transport, clock)
    assert result["status"] == "technical_qa"
    assert result["market_events"] == 2
    assert result["synthetic"] is True and result["financial_validation"] is False
    assert result["capture"]["reason"] == "fixture_complete"
    assert transport.closed and transport.connected
    assert [request["params"]["channel"] for request in transport.sent] == [
        "instrument",
        "trade",
        "ticker",
    ]
    assert transport.sent[-1]["params"]["event_trigger"] == "bbo"
    journal = service.journal("capture", config, ADMIN)
    assert len(journal.frames()) == 6
    raw = journal.read_frame(journal.frames()[-1])
    assert raw == canonical_bytes(ticker())
    replay = json.loads(service.store.get(result["replay_hash"], "json"))
    assert [event["quote_currency"] for event in replay["events"]] == ["EUR", "EUR"]
    assert replay["events"][1]["data"]["origin"] == "synthetic_explicit"
    repeated = service.inspect("capture", config, ADMIN)
    for key in ("archive_hash", "normalization_hash", "replay_hash", "checkpoint"):
        assert repeated[key] == result[key]


def test_receipt_cutoff_and_checkpoint_reconstruction_are_causal(tmp_path):
    service, config, clock = setup(tmp_path)
    transport = Transport(clock, handshake() + [trade(), ticker()])
    full = service.run_simulated("capture", config, ADMIN, lambda _: transport, clock)
    first_receipt = service.journal("capture", config, ADMIN).frames()[4].received_ns
    before = service.inspect("capture", config, ADMIN, until_ns=first_receipt - 1)
    partial = service.inspect("capture", config, ADMIN, until_ns=first_receipt)
    assert before["market_events"] == 0 and partial["market_events"] == 1
    checkpoint = CaptureReplayCheckpoint.model_validate(partial["checkpoint"])
    restarted_service = KrakenCaptureService(service.store, Policy(), service.directory)
    resumed = restarted_service.inspect("capture", config, ADMIN, checkpoint=checkpoint)
    assert resumed["market_events"] == 2 and resumed["checkpoint"] == full["checkpoint"]
    changed = checkpoint.model_copy(update={"prefix_hash": "0" * 64})
    with pytest.raises(ValueError, match="prefix"):
        service.inspect("capture", config, ADMIN, checkpoint=changed)


def test_finished_capture_retry_never_opens_a_second_transport(tmp_path):
    service, config, clock = setup(tmp_path)
    first = service.run_simulated(
        "capture", config, ADMIN, lambda _: Transport(clock, handshake() + [trade()]), clock
    )
    count = service.journal("capture", config, ADMIN).checkpoint.committed_records

    def forbidden(_):
        raise AssertionError("Terminal capture retry must not create a transport.")

    second = service.run_simulated("capture", config, ADMIN, forbidden, clock)
    assert second["replay_hash"] == first["replay_hash"]
    assert service.journal("capture", config, ADMIN).checkpoint.committed_records == count


def test_reconnect_retains_unknown_gap_and_deduplicates_only_native_trades(tmp_path):
    service, config, clock = setup(tmp_path, reconnect_delay_ns=1000)
    transports = [
        Transport(clock, handshake() + [trade(), ticker(), ConnectionError("fixture")]),
        Transport(clock, handshake() + [trade(), ticker(), trade(2)]),
    ]
    result = service.run_simulated("capture", config, ADMIN, lambda i: transports[i], clock)
    assert result["market_events"] == 4
    assert result["capture"]["sessions_started"] == 2
    assert all(transport.closed for transport in transports)
    records = service.journal("capture", config, ADMIN).records()
    gaps = [record for record in records if record.kind == "coverage_gap"]
    assert len(gaps) == 1 and gaps[0].details["coverage"] == "unknown"
    assert len([record for record in records if record.kind == "session_start"]) == 2
    sidecar = json.loads(service.store.get(result["normalization_hash"], "json"))
    assert sum(row["duplicate_delivery"] for row in sidecar["rows"]) == 1
    events = sidecar["events"]
    assert events[0]["available_ns"] < sidecar["rows"][2]["received_ns"]
    assert events[1]["event_id"] != events[2]["event_id"]


@pytest.mark.parametrize("role", ["viewer", "researcher", "agent"])
def test_policy_denies_before_creating_transport_or_journal(tmp_path, role):
    service, config, clock = setup(tmp_path)

    def forbidden(_):
        raise AssertionError("Denied role reached transport factory.")

    with pytest.raises(AccessDenied):
        service.run_simulated("capture", config, Principal(id="user", role=role), forbidden, clock)
    assert not service.directory.exists()


def test_real_classification_is_rejected_before_connect(tmp_path):
    service, config, clock = setup(tmp_path)
    transport = Transport(clock, [])
    transport.simulated = False
    with pytest.raises(AccessDenied):
        service.run_simulated("capture", config, ADMIN, lambda _: transport, clock)
    assert not transport.connected


def test_partition_and_path_cannot_bypass_configuration(tmp_path):
    service, config, clock = setup(tmp_path)
    with pytest.raises(AccessDenied):
        service.journal("capture", config.model_copy(update={"partition": "final"}), ADMIN)
    for identity in ("../outside", "/absolute", ".", "capture/sub", "a" * 65):
        with pytest.raises(ValueError):
            service.journal(identity, config, ADMIN)
    with pytest.raises(ValueError):
        CaptureConfiguration(mode="live")


def test_frame_limit_stops_before_next_receive(tmp_path):
    service, config, clock = setup(tmp_path, limits=CaptureLimits(max_frames=5))
    transport = Transport(clock, handshake() + [trade(), ticker()])
    result = service.run_simulated("capture", config, ADMIN, lambda _: transport, clock)
    assert result["capture"]["reason"] == "frame_limit"
    assert result["market_events"] == 1 and len(transport.timeouts) == 5
    assert transport.closed


def test_duration_and_reconnect_budget_remain_bounded(tmp_path):
    service, config, clock = setup(
        tmp_path, max_duration_ns=2500, receive_timeout_ns=1000, reconnect_delay_ns=0
    )
    transport = Transport(clock, handshake())
    journal = service.journal("capture", config, ADMIN)
    result = collect(journal, config, lambda _: transport, clock)
    assert result["reason"] == "duration_limit"
    assert max(transport.timeouts) <= 1000
    assert transport.timeouts[-1] <= 500
    assert transport.closed
    other = service.journal("bounded-reconnect", config, ADMIN)
    disconnected = []

    def factory(_):
        instance = Transport(clock, [ConnectionError("fixture")], step_ns=1)
        disconnected.append(instance)
        return instance

    result = collect(other, config, factory, clock)
    assert result["reason"] == "reconnect_limit"
    assert len(disconnected) == config.max_reconnects + 1
    assert all(item.closed for item in disconnected)


def test_user_stop_does_not_open_transport(tmp_path):
    service, config, clock = setup(tmp_path)
    journal = service.journal("capture", config, ADMIN)

    def forbidden(_):
        raise AssertionError("Stopped capture created transport.")

    result = collect(journal, config, forbidden, clock, stop_requested=lambda: True)
    assert result["reason"] == "user_stop" and not journal.frames()
    assert journal.records()[-1].kind == "capture_stop"


def test_bad_raw_is_preserved_before_protocol_rejection(tmp_path):
    service, config, clock = setup(tmp_path)
    journal = service.journal("capture", config, ADMIN)
    transport = Transport(clock, [b'{"unrecognized":true}'])
    result = collect(journal, config, lambda _: transport, clock)
    assert result["reason"] == "protocol_error" and transport.closed
    assert journal.read_frame(journal.frames()[0]) == b'{"unrecognized":true}'
    with pytest.raises(ValueError):
        service.inspect("capture", config, ADMIN)


def test_frame_storage_limit_is_not_reported_as_protocol_error(tmp_path):
    service, config, clock = setup(tmp_path, limits=CaptureLimits(max_frame_bytes=8))
    journal = service.journal("capture", config, ADMIN)
    transport = Transport(clock, [b"longer-than-eight"])
    result = collect(journal, config, lambda _: transport, clock)
    assert result["reason"] == "storage_or_record_limit" and transport.closed
    assert not journal.frames() and not journal.checkpoint.pending_intent


def test_interrupted_capture_resumes_new_handshake_without_losing_prefix(tmp_path):
    service, config, clock = setup(tmp_path)
    first = Transport(clock, handshake() + [trade(), KeyboardInterrupt()])
    result = service.run_simulated("capture", config, ADMIN, lambda _: first, clock)
    assert result["capture"]["reason"] == "interrupted" and first.closed
    prefix = service.journal("capture", config, ADMIN).records()
    second = Transport(clock, handshake() + [trade(), trade(2)])
    attempts = []

    def factory(index):
        attempts.append(index)
        return second

    resumed = service.run_simulated("capture", config, ADMIN, factory, clock)
    assert attempts == [1]
    assert resumed["market_events"] == 2 and second.closed
    assert service.journal("capture", config, ADMIN).records()[: len(prefix)] == prefix


def test_storage_interruption_requires_explicit_recovery_before_resume(tmp_path, monkeypatch):
    service, config, clock = setup(tmp_path)
    original = service.store.put
    failed_raw = canonical_bytes(trade())

    def fail(data, suffix):
        if suffix == "bin" and data == failed_raw:
            raise OSError("injected one-time interrupted write")
        return original(data, suffix)

    monkeypatch.setattr(service.store, "put", fail)
    transport = Transport(clock, handshake() + [trade()])
    result = service.run_simulated("capture", config, ADMIN, lambda _: transport, clock)
    assert result["status"] == "blocked_pending_recovery" and transport.closed
    monkeypatch.setattr(service.store, "put", original)
    journal = service.journal("capture", config, ADMIN)
    prefix = journal.records()
    assert journal.checkpoint.pending_intent
    with pytest.raises(ValueError, match="recovery"):
        collect(journal, config, lambda _: transport, clock)
    journal.recover(
        writer_stopped=True,
        session_id="recovery",
        received_ns=clock.utc,
        monotonic_ns=clock.monotonic,
    )
    second = Transport(clock, handshake() + [trade(), ticker()])
    resumed = service.run_simulated("capture", config, ADMIN, lambda _: second, clock)
    assert resumed["market_events"] == 2
    records = service.journal("capture", config, ADMIN).records()
    assert records[: len(prefix)] == prefix
    assert any(record.kind == "interruption" for record in records)
    assert not service.journal("capture", config, ADMIN).checkpoint.pending_intent


def test_configuration_is_reconstructible_and_cannot_change_under_same_capture(tmp_path):
    service, config, clock = setup(tmp_path, max_duration_ns=123456)
    journal = service.journal("capture", config, ADMIN)
    assert json.loads(service.store.get(config.digest, "json")) == config.model_dump(mode="json")
    with pytest.raises(ValueError, match="configuration"):
        collect(journal, CaptureConfiguration(), lambda _: pytest.fail("factory"), clock)


def test_capture_lease_rejects_second_collector_and_inspector(tmp_path):
    service, config, clock = setup(tmp_path)
    first = service.journal("capture", config, ADMIN)
    second = service.journal("capture", config, ADMIN)
    with first.capture_lease():
        with pytest.raises(BlockingIOError):
            collect(second, config, lambda _: pytest.fail("factory"), clock)
        with pytest.raises(BlockingIOError):
            service.inspect("capture", config, ADMIN)
    assert not first.frames()


def test_growing_capture_retains_replay_checkpoint_and_first_receipt(tmp_path):
    service, config, clock = setup(tmp_path)
    first = service.run_simulated(
        "capture",
        config,
        ADMIN,
        lambda _: Transport(clock, handshake() + [trade(), KeyboardInterrupt()]),
        clock,
    )
    checkpoint = CaptureReplayCheckpoint.model_validate(first["checkpoint"])
    service.run_simulated(
        "capture",
        config,
        ADMIN,
        lambda _: Transport(clock, handshake() + [trade(), ticker(), trade(2)]),
        clock,
    )
    resumed = service.inspect("capture", config, ADMIN, checkpoint=checkpoint)
    assert resumed["market_events"] == 3
    before = json.loads(service.store.get(first["replay_hash"], "json"))["events"]
    after = json.loads(service.store.get(resumed["replay_hash"], "json"))["events"]
    assert after[:1] == before


def test_close_failure_stops_reconnect_and_reports_unconfirmed_state(tmp_path):
    service, config, clock = setup(tmp_path)
    transport = Transport(clock, [ConnectionError("fixture")])

    def fail_close():
        raise OSError("injected close failure")

    transport.close = fail_close
    result = collect(service.journal("capture", config, ADMIN), config, lambda _: transport, clock)
    assert result["reason"] == "transport_close_failure"
    assert result["sessions_started"] == 1
    assert "transport_close_not_confirmed" in result["diagnostics"]


def test_existing_platform_composes_capture_without_financial_modules(tmp_path):
    from bot_trader.application import build_services
    from bot_trader.core.settings import Settings
    from bot_trader.persistence import Database, migrate

    settings = Settings(data_dir=tmp_path / "platform")
    database = Database(settings)
    try:
        migrate(database)
    finally:
        database.close()
    services = build_services(settings)
    try:
        clock = Clock()
        result = services.capture.run_simulated(
            "composed",
            CaptureConfiguration(),
            ADMIN,
            lambda _: Transport(clock, handshake() + [trade(), ticker()]),
            clock,
        )
        assert result["market_events"] == 2 and not result["financial_validation"]
        assert services.capture.store is services.slice.store
    finally:
        services.database.close()


@pytest.mark.parametrize("during_open", [True, False])
def test_rejection_does_not_claim_a_raw_frame_that_was_never_delivered(tmp_path, during_open):
    service, config, clock = setup(tmp_path)
    transport = Transport(clock, [b'{"unexpected":true}'])
    if during_open:

        def reject_open(_):
            raise ValueError("injected TLS/handshake rejection")

        transport.connect = reject_open
    journal = service.journal("capture", config, ADMIN)
    result = collect(journal, config, lambda _: transport, clock)
    assert result["reason"] == "protocol_error"
    rejection = next(record for record in journal.records() if record.kind == "protocol_error")
    assert rejection.details["raw_preserved"] is (not during_open)
    assert rejection.details["stage"] == ("connect" if during_open else "decode")
    assert len(journal.frames()) == (0 if during_open else 1)
