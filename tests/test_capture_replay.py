"""Recorded-feed QA uses invented frames; no financial signal or execution path."""

import pytest
from test_kraken_ws import frames, handshake, session, ticker, trade

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import BarData, MarketEventV2, QuoteData
from bot_trader.market_data.kraken_ws import KrakenWSNormalizer
from bot_trader.market_data.replay import (
    CaptureReplayCheckpoint,
    MarketReplay,
    QAReplayCheckpoint,
    ReplayCheckpoint,
    ReplayPolicy,
)


def captured_events(*, future_price="102"):
    store, references = frames(
        session(handshake() + [trade(), ticker(), trade(2, price=future_price)])
    )
    return KrakenWSNormalizer(store).normalize_frames(references, "a" * 64).events


def changed_event(event, **updates):
    value = event.model_dump()
    value.update(updates)
    return MarketEventV2.model_validate(value)


def test_capture_cutoff_checkpoint_and_future_suffix_invariance(monkeypatch):
    events = captured_events()
    replay = MarketReplay()
    monkeypatch.setattr(
        "bot_trader.market_data.replay._state", lambda *_: pytest.fail("Analytics invoked")
    )
    before = replay.inspect_capture(
        events, data_class="synthetic", until_ns=events[0].received_ns - 1
    )
    assert before.events == () and before.checkpoint.consumed_count == 0
    first = replay.inspect_capture(events, data_class="synthetic", until_ns=events[0].received_ns)
    assert first.events == (events[0],)
    assert events[0].event_ns < events[0].received_ns
    prefix = replay.inspect_capture(events, data_class="synthetic", until_ns=events[1].received_ns)
    altered = captured_events(future_price="999")
    assert altered[-1].digest != events[-1].digest
    assert (
        replay.inspect_capture(altered, data_class="synthetic", until_ns=events[1].received_ns)
        == prefix
    )
    # A later received trade with an earlier exchange timestamp stays unavailable.
    late = changed_event(altered[-1], event_ns=1, original_tick=1)
    assert (
        replay.inspect_capture(
            (*altered[:-1], late), data_class="synthetic", until_ns=events[1].received_ns
        )
        == prefix
    )
    full = replay.inspect_capture(events, data_class="synthetic")
    resumed = replay.inspect_capture(events, data_class="synthetic", checkpoint=prefix.checkpoint)
    assert full.events == resumed.events == events
    assert full.checkpoint == resumed.checkpoint
    assert "capture_checkpoint_reconstructed_and_verified" in resumed.diagnostics
    assert full == replay.inspect_capture(events, data_class="synthetic")
    assert not full.financial_validation
    assert not hasattr(full, "signals") and not hasattr(full, "indicators")


@pytest.mark.parametrize(
    "profile",
    [
        {"data_class": "financial"},
        {"data_class": "synthetic", "partition": "validation"},
        {"data_class": "synthetic", "partition": "final"},
        {"data_class": "synthetic", "purpose": "financial"},
        {"data_class": "synthetic", "purpose": "structural_qa"},
    ],
)
def test_capture_profile_rejects_other_purposes_and_reserved_data(profile):
    with pytest.raises(AccessDenied):
        MarketReplay().inspect_capture(captured_events(), **profile)


def test_capture_checkpoints_reject_changed_prefix_other_profiles_and_wrong_type():
    replay, events = MarketReplay(), captured_events()
    checkpoint = replay.inspect_capture(events, data_class="synthetic").checkpoint
    changed = events[0].model_dump()
    changed["data"]["price"] = "99"
    with pytest.raises(ValueError, match="prefix changed"):
        replay.inspect_capture(
            (MarketEventV2.model_validate(changed), *events[1:]),
            data_class="synthetic",
            checkpoint=checkpoint,
        )
    for other in (
        QAReplayCheckpoint(consumed_count=0, prefix_hash="a" * 64),
        ReplayCheckpoint(
            consumed_count=0, prefix_hash="a" * 64, state_hash="b" * 64, policy_hash="c" * 64
        ),
    ):
        with pytest.raises(ValueError, match="own versioned checkpoint"):
            replay.inspect_capture(events, data_class="synthetic", checkpoint=other)
    for count in (0, 10):
        with pytest.raises(ValueError, match="prefix changed"):
            replay.inspect_capture(
                events,
                data_class="synthetic",
                checkpoint=CaptureReplayCheckpoint(consumed_count=count, prefix_hash="d" * 64),
            )
    trades = (events[0], events[2])
    synthetic = replay.inspect_capture(trades, data_class="synthetic")
    with pytest.raises(ValueError, match="prefix changed"):
        replay.inspect_capture(
            trades, data_class="exposed_structural_only", checkpoint=synthetic.checkpoint
        )


def test_capture_requires_reception_trade_bbo_and_explicit_quote_origin():
    replay, events = MarketReplay(), captured_events()
    without_receipt = changed_event(events[0], received_ns=None)
    with pytest.raises(ValueError, match="recorded receipt"):
        replay.inspect_capture((without_receipt,), data_class="synthetic")
    bar = BarData(
        bar_id="bar-1",
        start_ns=0,
        end_ns=1,
        status="closed",
        label="close",
        open="100",
        high="101",
        low="99",
        close="100",
        volume="1",
    )
    bar_event = changed_event(events[0], data=bar.model_dump(), event_ns=1, original_tick=1)
    with pytest.raises(ValueError, match="trade/BBO"):
        replay.inspect_capture((bar_event,), data_class="synthetic")
    quote = events[1]
    assert isinstance(quote.data, QuoteData)
    for origin in ("observed", "ohlc_assumption"):
        value = quote.data.model_dump()
        value["origin"] = origin
        mismatched = changed_event(quote, data=value)
        with pytest.raises(ValueError, match="origin"):
            replay.inspect_capture((mismatched,), data_class="synthetic")
    with pytest.raises(ValueError, match="origin"):
        replay.inspect_capture((quote,), data_class="exposed_structural_only")
    observed_data = quote.data.model_dump()
    observed_data["origin"] = "observed"
    observed = changed_event(quote, data=observed_data)
    assert replay.inspect_capture((observed,), data_class="exposed_structural_only").events == (
        observed,
    )
    # Adding captured BBO support must not widen the historical OHLC/trade route.
    with pytest.raises(ValueError, match="does not admit quotes"):
        replay.inspect_history((observed,), data_class="exposed_structural_only")


def test_capture_shared_identity_sequence_and_budget_guards():
    events, replay = captured_events(), MarketReplay()
    expected = replay.inspect_capture(events, data_class="synthetic")
    reordered = replay.inspect_capture((*reversed(events), events[0]), data_class="synthetic")
    assert reordered.events == expected.events and reordered.checkpoint == expected.checkpoint
    assert any("identical_duplicate_ignored" in item for item in reordered.diagnostics)
    with pytest.raises(ValueError, match="Sequence gap"):
        replay.inspect_capture((events[2],), data_class="synthetic")
    changed = events[0].model_dump()
    changed["data"]["price"] = "99"
    with pytest.raises(ValueError, match="Conflicting duplicate"):
        replay.inspect_capture(
            (*events, MarketEventV2.model_validate(changed)), data_class="synthetic"
        )
    with pytest.raises(ValueError, match="bounded event budget"):
        MarketReplay(ReplayPolicy(max_events=1)).inspect_capture(events, data_class="synthetic")
