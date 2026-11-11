"""Small synthetic replay regressions; no engine execution or investment hypothesis."""

from decimal import Decimal
from typing import Literal

import pytest
from pydantic import ValidationError

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import (
    BarData,
    Level,
    MarketEventV2,
    QuoteData,
    TradeData,
)
from bot_trader.market_data.replay import (
    MarketReplay,
    ReplayCheckpoint,
    ReplayPolicy,
    ReplayResult,
    information_hash,
)


def event(
    sequence: int,
    data: BarData | TradeData | QuoteData,
    *,
    event_ns: int,
    available_ns: int,
    event_id: str | None = None,
    source: str = "fixture",
    received_ns: int | None = None,
) -> MarketEventV2:
    return MarketEventV2(
        event_id=event_id or f"event-{sequence}",
        source_id=source,
        source_version="fixture-v2",
        stream_id="market",
        sequence=sequence,
        instrument="SYNTH-USD",
        original_tick=event_ns,
        original_unit="ns",
        event_ns=event_ns,
        available_ns=available_ns,
        received_ns=received_ns,
        raw_sha256="1" * 64,
        data=data,
    )


def bar(
    number: int,
    sequence: int,
    *,
    close: str = "100",
    status: Literal["open", "closed", "corrected"] = "closed",
    available_ns: int | None = None,
    event_id: str | None = None,
    revision_of: str | None = None,
) -> MarketEventV2:
    start, end = (number - 1) * 10, number * 10
    event_time = start if status == "open" else end
    return event(
        sequence,
        BarData(
            bar_id=f"bar-{number}",
            start_ns=start,
            end_ns=end,
            status=status,
            label="open" if status == "open" else "close",
            open=close,
            high=str(Decimal(close) + 1),
            low=str(Decimal(close) - 1),
            close=close,
            volume="2",
            revision_of=revision_of,
        ),
        event_ns=event_time,
        available_ns=event_time + 1 if available_ns is None else available_ns,
        event_id=event_id,
    )


def replay(**values: object) -> MarketReplay:
    return MarketReplay(ReplayPolicy.model_validate({"interval_ns": 10, **values}))


def three_bars() -> tuple[MarketEventV2, ...]:
    return (bar(1, 1, close="100"), bar(2, 2, close="110"), bar(3, 3, close="120"))


def test_closed_only_warmup_and_fixed_round_trip_signal() -> None:
    source = (
        bar(1, 1, status="open", available_ns=1),
        bar(1, 2, close="100"),
        bar(2, 3, status="open", available_ns=12),
        bar(2, 4, close="110"),
        bar(3, 5, close="120"),
    )
    result = replay().run(source, synthetic=True)
    assert result.records[0].state.indicators[0].closed_count == 0
    assert result.records[2].state.indicators[0].closed_count == 1
    assert result.records[2].state.indicators[0].mean is None
    assert result.records[3].state.indicators[0].mean == "105"
    assert result.records[4].state.indicators[0].mean == "115"
    assert [(signal.side, signal.quantity, signal.decision_ns) for signal in result.signals] == [
        ("buy", "1", 21),
        ("sell", "1", 31),
    ]
    assert result.signals[0].source_event_hash == information_hash(source[3])
    assert result.signals[0].state_hash == result.records[3].state.digest
    assert result.signals[0].policy_hash == replay().policy.digest


def test_available_and_received_clocks_preserve_one_nanosecond_boundary() -> None:
    first, second, _ = three_bars()
    delayed = MarketEventV2.model_validate(
        second.model_dump(mode="json") | {"available_ns": 20, "received_ns": 21}
    )
    before = replay().run((first, delayed), synthetic=True, until_ns=20)
    at = replay().run((first, delayed), synthetic=True, until_ns=21)
    assert len(before.records) == 1 and before.signals == ()
    assert len(at.records) == 2 and at.signals[0].decision_ns == 21
    with pytest.raises(ValueError, match="exact integer"):
        replay().run((first,), synthetic=True, until_ns=True)


def test_deterministic_replay_and_serialization() -> None:
    first = replay().run(three_bars(), synthetic=True)
    second = replay().run(three_bars(), synthetic=True)
    assert first == second
    assert first.model_dump_json() == second.model_dump_json()
    assert ReplayResult.model_validate_json(first.model_dump_json()) == first
    with pytest.raises(ValidationError):
        first.signals[0].quantity = "20"


def test_identical_duplicate_has_no_second_state_or_signal_effect() -> None:
    source = three_bars()
    baseline = replay().run(source, synthetic=True)
    duplicate = replay().run((source[0], source[1], source[1], source[2]), synthetic=True)
    assert duplicate.records == baseline.records
    assert duplicate.signals == baseline.signals
    assert duplicate.checkpoint == baseline.checkpoint
    assert duplicate.diagnostics == ("identical_duplicate_ignored:fixture:market:event-2",)


def test_conflicting_duplicate_is_rejected() -> None:
    source = three_bars()
    conflict = bar(2, 2, close="111")
    with pytest.raises(ValueError, match="Conflicting duplicate"):
        replay().run((source[0], source[1], conflict), synthetic=True)


def test_gap_and_source_sequence_reversal_are_not_repaired() -> None:
    source = three_bars()
    with pytest.raises(ValueError, match="Sequence gap/reversal"):
        replay().run((source[0], source[2]), synthetic=True)
    first_late = MarketEventV2.model_validate(
        source[0].model_dump(mode="json") | {"available_ns": 22}
    )
    with pytest.raises(ValueError, match="Sequence gap/reversal"):
        replay().run((first_late, source[1]), synthetic=True)


def test_transport_reordering_is_explicit_and_preserves_canonical_decisions() -> None:
    source = three_bars()
    baseline = replay().run(source, synthetic=True)
    reordered = replay().run(tuple(reversed(source)), synthetic=True)
    assert reordered.records == baseline.records
    assert reordered.signals == baseline.signals
    assert reordered.diagnostics == ("input_reordered_by_explicit_availability_policy",)


def test_equal_availability_uses_stable_source_tie_policy() -> None:
    data = TradeData(price="100", quantity="1")
    alpha = event(1, data, event_ns=1, available_ns=2, source="alpha")
    beta = event(1, data, event_ns=1, available_ns=2, source="beta")
    baseline = replay().run((alpha, beta), synthetic=True)
    reordered = replay().run((beta, alpha), synthetic=True)
    assert [record.source_id for record in reordered.records] == ["alpha", "beta"]
    assert reordered.records == baseline.records
    assert reordered.checkpoint == baseline.checkpoint


def test_trade_buckets_use_only_received_prefix_then_validate_closed_snapshot() -> None:
    first = event(1, TradeData(price="100", quantity="1"), event_ns=1, available_ns=2)
    second = event(2, TradeData(price="102", quantity="2"), event_ns=4, available_ns=5)
    close = event(
        3,
        BarData(
            bar_id="bar-1",
            start_ns=0,
            end_ns=10,
            status="closed",
            label="close",
            open="100",
            high="102",
            low="100",
            close="102",
            volume="3",
        ),
        event_ns=10,
        available_ns=11,
    )
    result = replay(complete_trade_coverage=True).run((first, second, close), synthetic=True)
    before, after = (record.state.trade_buckets[0] for record in result.records[:2])
    assert (before.open, before.high, before.close, before.volume) == ("100", "100", "100", "1")
    assert (after.open, after.high, after.close, after.volume) == ("100", "102", "102", "3")
    assert before.trade_ids == ("event-1",)
    assert result.records[-1].state.indicators[0].closed_count == 1
    inconsistent = MarketEventV2.model_validate(
        close.model_dump(mode="json")
        | {"data": close.data.model_dump(mode="json") | {"volume": "4"}}
    )
    with pytest.raises(ValueError, match="disagrees"):
        replay(complete_trade_coverage=True).run((first, second, inconsistent), synthetic=True)
    with pytest.raises(ValueError, match="coverage is missing"):
        replay(complete_trade_coverage=True).run((bar(1, 1),), synthetic=True)


def test_late_trade_cannot_rewrite_a_closed_interval() -> None:
    close = bar(1, 1)
    late = event(2, TradeData(price="101", quantity="1"), event_ns=4, available_ns=12)
    with pytest.raises(ValueError, match="Late trade"):
        replay().run((close, late), synthetic=True)


def test_revision_updates_current_indicator_without_rewriting_prior_decision() -> None:
    first, second, _ = three_bars()
    prefix = replay().run((first, second), synthetic=True)
    correction = bar(
        1,
        3,
        close="90",
        status="corrected",
        revision_of=first.event_id,
        event_id="revision-1",
        available_ns=25,
    )
    third = bar(3, 4, close="120")
    extended = replay().run((first, second, correction, third), synthetic=True)
    assert extended.records[:2] == prefix.records
    assert extended.signals[0] == prefix.signals[0]
    assert extended.records[2].state.indicators[0].mean == "100"
    assert extended.records[2].signal_id is None
    assert len(extended.signals) == 2
    assert extended.records[2].state.bars[0].event_id == "revision-1"
    invalid_parent = bar(
        1,
        3,
        close="90",
        status="corrected",
        revision_of="unknown",
        available_ns=25,
    )
    with pytest.raises(ValueError, match="current closed predecessor"):
        replay().run((first, second, invalid_parent), synthetic=True)


def test_future_high_change_preserves_prior_decision_and_state_prefix() -> None:
    source = three_bars()
    changed_last = MarketEventV2.model_validate(
        source[2].model_dump(mode="json")
        | {"data": source[2].data.model_dump(mode="json") | {"high": "135"}}
    )
    baseline = replay().run(source, synthetic=True)
    changed = replay().run((*source[:2], changed_last), synthetic=True)
    assert baseline.records[:2] == changed.records[:2]
    assert baseline.signals[0] == changed.signals[0]
    # The final signal observes the changed bar, so its provenance should differ.
    assert baseline.signals[1].source_event_hash != changed.signals[1].source_event_hash


def test_future_archive_change_does_not_change_earlier_causal_signal_identity() -> None:
    source = three_bars()
    changed_archive = tuple(
        MarketEventV2.model_validate(item.model_dump(mode="json") | {"raw_sha256": "2" * 64})
        for item in source
    )
    changed_last = MarketEventV2.model_validate(
        changed_archive[2].model_dump(mode="json")
        | {"data": changed_archive[2].data.model_dump(mode="json") | {"high": "135"}}
    )
    baseline = replay().run(source, synthetic=True)
    changed = replay().run((*changed_archive[:2], changed_last), synthetic=True)
    assert baseline.signals[0] == changed.signals[0]
    assert baseline.records[1].state == changed.records[1].state
    assert baseline.records[1].event_hash != changed.records[1].event_hash
    assert baseline.records[1].prefix_hash != changed.records[1].prefix_hash
    with pytest.raises(ValueError, match="Checkpoint"):
        replay().run(changed_archive, synthetic=True, checkpoint=baseline.checkpoint)


def test_checkpoint_resumption_verifies_prefix_without_emitting_duplicates() -> None:
    source = three_bars()
    prefix = replay().run(source, synthetic=True, until_ns=21)
    encoded = prefix.checkpoint.model_dump_json()
    checkpoint = ReplayCheckpoint.model_validate_json(encoded)
    resumed = replay().run(source, synthetic=True, checkpoint=checkpoint)
    baseline = replay().run(source, synthetic=True)
    assert resumed.records == baseline.records and resumed.signals == baseline.signals
    assert resumed.checkpoint == baseline.checkpoint
    assert resumed.diagnostics == ("checkpoint_prefix_reconstructed_and_verified",)
    with pytest.raises(ValueError, match="Checkpoint"):
        replay().run((bar(1, 1, close="99"), *source[1:]), synthetic=True, checkpoint=checkpoint)
    with pytest.raises(ValueError, match="Checkpoint"):
        replay(mean_window=1).run(source, synthetic=True, checkpoint=checkpoint)
    with pytest.raises(ValueError, match="Checkpoint"):
        replay().run(source[:1], synthetic=True, checkpoint=checkpoint)


def test_quote_is_replayed_at_effective_availability_without_financial_execution() -> None:
    quote = event(
        1,
        QuoteData(
            origin="synthetic_explicit",
            bids=(Level(price="99", quantity="2"),),
            asks=(Level(price="101", quantity="2"),),
        ),
        event_ns=1,
        available_ns=2,
        received_ns=3,
    )
    assert replay().run((quote,), synthetic=True, until_ns=2).quotes == ()
    result = replay().run((quote,), synthetic=True, until_ns=3)
    assert result.quotes == (quote,) and result.signals == ()
    assert result.financial_validation is False
    observed = MarketEventV2.model_validate(
        quote.model_dump(mode="json")
        | {"data": quote.data.model_dump(mode="json") | {"origin": "observed"}}
    )
    with pytest.raises(ValueError, match="Observed market"):
        replay().run((observed,), synthetic=True)


@pytest.mark.parametrize(
    "synthetic,mode,partition",
    [
        (False, "technical", "development"),
        (True, "live", "development"),
        (True, "technical", "final"),
        (True, "technical", "validation"),
    ],
)
def test_nontechnical_or_reserved_access_is_denied(
    synthetic: bool,
    mode: str,
    partition: str,
) -> None:
    with pytest.raises(AccessDenied):
        replay().run(three_bars(), synthetic=synthetic, mode=mode, partition=partition)


def test_closed_replacement_and_grid_mismatch_are_rejected() -> None:
    first = bar(1, 1)
    with pytest.raises(ValueError, match="explicit correction"):
        replay().run((first, bar(1, 2, available_ns=12)), synthetic=True)
    with pytest.raises(ValueError, match="versioned replay grid"):
        MarketReplay(ReplayPolicy(interval_ns=9)).run((first,), synthetic=True)
    with pytest.raises(ValueError, match="finite technical budget"):
        replay(max_events=2).run(three_bars(), synthetic=True)
