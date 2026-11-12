"""Data-only historical replay with invented Kraken-format records, never a strategy."""

import pytest
from test_kraken_history import BAR, BAR_SCHEMA, prepared

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import MarketEventV2
from bot_trader.market_data.kraken_history import HistoricalAvailability, KrakenHistoricalNormalizer
from bot_trader.market_data.replay import MarketReplay


def bars():
    raw = BAR + b"1700000100,11,13,10,12,3,4\n" + b"1700000160,12,14,11,13,4,5\n"
    selection, source, manifest = prepared(raw, BAR_SCHEMA, rows=3)
    return KrakenHistoricalNormalizer(
        selection, HistoricalAvailability(delay_ns=123),
    ).normalize(raw, source, manifest).events


def test_closed_bar_canary_and_no_signal_or_analytic_path(monkeypatch):
    events = bars()
    replay = MarketReplay()
    monkeypatch.setattr("bot_trader.market_data.replay._state", lambda *_: pytest.fail("Analytics invoked"))
    before = replay.inspect_history(events, data_class="exposed_structural_only", until_ns=events[0].data.end_ns-1)
    assert before.events == ()
    delayed = replay.inspect_history(events, data_class="exposed_structural_only", until_ns=events[0].data.end_ns)
    assert delayed.events == ()
    first = replay.inspect_history(events, data_class="exposed_structural_only", until_ns=events[0].available_ns)
    assert len(first.events) == 1
    whole = replay.inspect_history(events, data_class="exposed_structural_only", checkpoint=first.checkpoint)
    assert len(whole.events) == 3 and not hasattr(whole, "signals") and not hasattr(whole, "indicators")
    assert whole.checkpoint == replay.inspect_history(events, data_class="exposed_structural_only").checkpoint


def test_duplicate_reorder_gap_and_changed_prefix():
    events = bars()
    replay = MarketReplay()
    whole = replay.inspect_history(events, data_class="exposed_structural_only")
    repeated = replay.inspect_history((*reversed(events), events[0]), data_class="exposed_structural_only")
    assert repeated.events == whole.events and repeated.checkpoint == whole.checkpoint
    assert len(repeated.diagnostics) == 2
    with pytest.raises(ValueError, match="Sequence gap"):
        replay.inspect_history((events[0], events[2]), data_class="exposed_structural_only")
    changed = events[0].model_dump()
    changed["data"]["close"] = "10"
    altered = MarketEventV2.model_validate(changed)
    with pytest.raises(ValueError, match="prefix changed"):
        replay.inspect_history((altered, *events[1:]), data_class="exposed_structural_only", checkpoint=whole.checkpoint)


def test_qa_authority_does_not_bypass_synthetic_strategy_or_reserved_partition():
    replay, events = MarketReplay(), bars()
    with pytest.raises(AccessDenied):
        replay.run(events, synthetic=False)
    for partition in ("validation", "final"):
        with pytest.raises(AccessDenied):
            replay.inspect_history(events, data_class="exposed_structural_only", partition=partition)
    with pytest.raises(AccessDenied):
        replay.inspect_history(events, data_class="exposed_structural_only", purpose="financial")
