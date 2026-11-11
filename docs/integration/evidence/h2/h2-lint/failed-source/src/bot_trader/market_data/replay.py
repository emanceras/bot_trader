"""Deterministic information replay, with no order matching or financial metrics.

The technical signal is a fixed second/third-closed-bar action, not an investment
hypothesis. Checkpoints verify replay prefixes; they never restore an exchange
or native execution engine. Source sequence coverage starts at one in this slice.
"""

from collections.abc import Sequence
from decimal import Decimal, localcontext
from typing import Literal

from pydantic import Field, field_validator

from bot_trader.core.contracts import Identifier
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import (
    BarData,
    Digest,
    ImmutableV2,
    MarketEventV2,
    Nanoseconds,
    QuoteData,
    TradeData,
    content_hash,
    decimal_text,
    exact_ns,
)

Feed = tuple[str, str, str]
BarKey = tuple[str, str, str, str]
BucketKey = tuple[str, str, str, int]
TIE_POLICY: Literal["effective_ns/source_id/stream_id/sequence/event_id:v1"] = (
    "effective_ns/source_id/stream_id/sequence/event_id:v1"
)


def information_hash(event: MarketEventV2) -> str:
    """Hash causal contents independently of the enclosing archive's future rows.

    Full event digests still bind records/checkpoints to exact raw provenance.
    Changing a future raw row may change that archive hash but must not change
    an already determined action's identity solely through archive metadata.
    """
    return content_hash(event.model_dump(mode="json", exclude={"raw_sha256"}))


class ReplayPolicy(ImmutableV2):
    schema_version: Literal[1] = 1
    version: Identifier = "synthetic-round-trip-v1"
    interval_ns: Nanoseconds = Field(default=1_000_000_000, gt=0)
    mean_window: int = Field(default=2, strict=True, ge=1, le=100)
    buy_quantity: str = "1"
    sell_quantity: str = "1"
    complete_trade_coverage: bool = Field(default=False, strict=True)
    max_events: int = Field(default=10_000, strict=True, ge=1, le=10_000)

    @field_validator("buy_quantity", "sell_quantity", mode="before")
    @classmethod
    def quantities(cls, value: object) -> str:
        return decimal_text(value, positive=True)

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


class BarSnapshot(ImmutableV2):
    source_id: Identifier
    stream_id: Identifier
    instrument: Identifier
    event_id: Identifier
    bar: BarData


class TradeBucket(ImmutableV2):
    source_id: Identifier
    stream_id: Identifier
    instrument: Identifier
    start_ns: Nanoseconds
    end_ns: Nanoseconds
    open: str
    high: str
    low: str
    close: str
    volume: str
    trade_ids: tuple[str, ...]


class IndicatorState(ImmutableV2):
    source_id: Identifier
    stream_id: Identifier
    instrument: Identifier
    closed_count: int
    ready: bool
    mean: str | None
    contributing_event_ids: tuple[str, ...]


class AnalyticalState(ImmutableV2):
    bars: tuple[BarSnapshot, ...] = ()
    trade_buckets: tuple[TradeBucket, ...] = ()
    indicators: tuple[IndicatorState, ...] = ()

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


class SyntheticSignal(ImmutableV2):
    schema_version: Literal[1] = 1
    id: Identifier
    instrument: Identifier
    side: Literal["buy", "sell"]
    quantity: str
    decision_ns: Nanoseconds
    source_event_id: Identifier
    source_event_hash: Digest
    state_hash: Digest
    policy_hash: Digest
    synthetic: Literal[True] = True


class ReplayRecord(ImmutableV2):
    event_id: Identifier
    source_id: Identifier
    stream_id: Identifier
    event_hash: Digest
    effective_ns: Nanoseconds
    kind: Literal["trade", "bar", "quote"]
    state: AnalyticalState
    prefix_hash: Digest
    signal_id: Identifier | None = None


class ReplayCheckpoint(ImmutableV2):
    schema_version: Literal[1] = 1
    consumed_count: int = Field(strict=True, ge=0)
    prefix_hash: Digest
    state_hash: Digest
    policy_hash: Digest
    tie_policy: Literal["effective_ns/source_id/stream_id/sequence/event_id:v1"] = TIE_POLICY


class ReplayResult(ImmutableV2):
    schema_version: Literal[1] = 1
    records: tuple[ReplayRecord, ...]
    signals: tuple[SyntheticSignal, ...]
    quotes: tuple[MarketEventV2, ...]
    diagnostics: tuple[str, ...]
    checkpoint: ReplayCheckpoint
    synthetic: Literal[True] = True
    financial_validation: Literal[False] = False


def _feed(event: MarketEventV2) -> Feed:
    return event.source_id, event.stream_id, event.instrument


def _key(event: MarketEventV2) -> tuple[int, str, str, int, str]:
    return (event.effective_ns, event.source_id, event.stream_id, event.sequence, event.event_id)


def _bucket(events: list[MarketEventV2], interval_ns: int) -> TradeBucket:
    ordered = sorted(events, key=lambda event: (event.event_ns, event.sequence, event.event_id))
    first = ordered[0]
    payloads = [event.data for event in ordered]
    if not all(isinstance(data, TradeData) for data in payloads):
        raise ValueError("Only trades can build a trade bucket.")
    prices = [Decimal(data.price) for data in payloads if isinstance(data, TradeData)]
    with localcontext() as context:
        context.prec = 50
        volume = sum(
            (Decimal(data.quantity) for data in payloads if isinstance(data, TradeData)),
            Decimal(0),
        )
    start = first.event_ns // interval_ns * interval_ns
    return TradeBucket(
        source_id=first.source_id,
        stream_id=first.stream_id,
        instrument=first.instrument,
        start_ns=start,
        end_ns=exact_ns(start + interval_ns),
        open=decimal_text(str(prices[0])),
        high=decimal_text(str(max(prices))),
        low=decimal_text(str(min(prices))),
        close=decimal_text(str(prices[-1])),
        volume=decimal_text(str(volume)),
        trade_ids=tuple(event.event_id for event in ordered),
    )


def _state(
    bars: dict[BarKey, BarSnapshot],
    trades: dict[BucketKey, list[MarketEventV2]],
    policy: ReplayPolicy,
) -> AnalyticalState:
    indicators = []
    feeds = sorted({key[:3] for key in bars})
    for feed in feeds:
        closed = sorted(
            (
                value
                for key, value in bars.items()
                if key[:3] == feed and value.bar.status != "open"
            ),
            key=lambda value: (value.bar.end_ns, value.bar.bar_id),
        )
        ready = len(closed) >= policy.mean_window
        selected = closed[-policy.mean_window :]
        mean = None
        if ready:
            with localcontext() as context:
                context.prec = 50
                mean = decimal_text(
                    str(
                        sum((Decimal(item.bar.close) for item in selected), Decimal(0))
                        / Decimal(policy.mean_window)
                    )
                )
        indicators.append(
            IndicatorState(
                source_id=feed[0],
                stream_id=feed[1],
                instrument=feed[2],
                closed_count=len(closed),
                ready=ready,
                mean=mean,
                contributing_event_ids=tuple(item.event_id for item in selected) if ready else (),
            )
        )
    return AnalyticalState(
        bars=tuple(bars[key] for key in sorted(bars)),
        trade_buckets=tuple(_bucket(trades[key], policy.interval_ns) for key in sorted(trades)),
        indicators=tuple(indicators),
    )


class MarketReplay:
    """One replay input boundary; downstream execution consumes the same ordered inputs.

    Reordering is explicit and diagnosed. Sequence gaps/conflicts stop the run.
    A closed snapshot can be accepted without all underlying trades only when the
    policy explicitly does not claim complete trade coverage. Late trades for a
    closed interval require a source correction; they are never silently inserted.
    """

    def __init__(self, policy: ReplayPolicy | None = None) -> None:
        self.policy = policy or ReplayPolicy()

    def run(
        self,
        events: Sequence[MarketEventV2],
        *,
        synthetic: bool,
        mode: str = "technical",
        partition: str = "development",
        until_ns: int | None = None,
        checkpoint: ReplayCheckpoint | None = None,
    ) -> ReplayResult:
        if synthetic is not True or mode != "technical" or partition != "development":
            raise AccessDenied("This replay/analytical path accepts synthetic development only.")
        if len(events) > self.policy.max_events:
            raise ValueError("Replay input exceeds its finite technical budget.")
        if until_ns is not None:
            exact_ns(until_ns)
        eligible = [event for event in events if until_ns is None or event.effective_ns <= until_ns]
        ordered = sorted(eligible, key=_key)
        diagnostics = []
        if [_key(event) for event in eligible] != [_key(event) for event in ordered]:
            diagnostics.append("input_reordered_by_explicit_availability_policy")
        bars: dict[BarKey, BarSnapshot] = {}
        trades: dict[BucketKey, list[MarketEventV2]] = {}
        identities: dict[tuple[str, str, str], str] = {}
        sequences: dict[tuple[str, str], int] = {}
        records: list[ReplayRecord] = []
        signals: list[SyntheticSignal] = []
        quotes: list[MarketEventV2] = []
        prefix = content_hash({"policy": self.policy.digest, "tie_policy": TIE_POLICY})
        initial = AnalyticalState()
        checkpoints = [
            ReplayCheckpoint(
                consumed_count=0,
                prefix_hash=prefix,
                state_hash=initial.digest,
                policy_hash=self.policy.digest,
            )
        ]
        for event in ordered:
            prior = identities.get(event.identity)
            if prior is not None:
                if prior != event.digest:
                    raise ValueError("Conflicting duplicate event identity.")
                diagnostics.append("identical_duplicate_ignored:" + ":".join(event.identity))
                continue
            stream = event.source_id, event.stream_id
            expected = sequences.get(stream, 0) + 1
            if event.sequence != expected:
                raise ValueError(
                    f"Sequence gap/reversal for {stream}: expected {expected}, got {event.sequence}."
                )
            identities[event.identity] = event.digest
            sequences[stream] = event.sequence
            data = event.data
            feed = _feed(event)
            new_close = False
            if isinstance(data, TradeData):
                start = event.event_ns // self.policy.interval_ns * self.policy.interval_ns
                if any(
                    key[:3] == feed
                    and value.bar.status != "open"
                    and value.bar.start_ns <= event.event_ns < value.bar.end_ns
                    for key, value in bars.items()
                ):
                    raise ValueError(
                        "Late trade for a closed interval needs an explicit correction."
                    )
                trades.setdefault((*feed, start), []).append(event)
            elif isinstance(data, BarData):
                key = (*feed, data.bar_id)
                old = bars.get(key)
                if data.start_ns % self.policy.interval_ns or (
                    data.end_ns - data.start_ns != self.policy.interval_ns
                ):
                    raise ValueError("Bar interval is incompatible with the versioned replay grid.")
                if data.status == "corrected":
                    if old is None or old.bar.status == "open" or data.revision_of != old.event_id:
                        raise ValueError(
                            "Correction must reference the current closed predecessor."
                        )
                    if (data.start_ns, data.end_ns) != (old.bar.start_ns, old.bar.end_ns):
                        raise ValueError(
                            "A correction cannot silently replace a different interval."
                        )
                elif old is not None and old.bar.status != "open":
                    raise ValueError("Replacing a closed bar requires an explicit correction.")
                if data.status == "closed":
                    if any(
                        other_key[:3] == feed
                        and value.bar.status != "open"
                        and value.bar.end_ns >= data.end_ns
                        for other_key, value in bars.items()
                    ):
                        raise ValueError(
                            "A late closed interval requires explicit revision handling."
                        )
                    if self.policy.complete_trade_coverage:
                        inputs = trades.get((*feed, data.start_ns))
                        if not inputs:
                            raise ValueError("Claimed complete trade coverage is missing.")
                        observed = _bucket(inputs, self.policy.interval_ns)
                        if any(
                            getattr(data, name) != getattr(observed, name)
                            for name in ("open", "high", "low", "close", "volume")
                        ):
                            raise ValueError(
                                "Closed snapshot disagrees with available prefix trades."
                            )
                    new_close = True
                bars[key] = BarSnapshot(
                    source_id=event.source_id,
                    stream_id=event.stream_id,
                    instrument=event.instrument,
                    event_id=event.event_id,
                    bar=data,
                )
            elif isinstance(data, QuoteData):
                if data.origin == "observed":
                    raise ValueError(
                        "Observed market quotes are outside this synthetic replay path."
                    )
                quotes.append(event)
            state = _state(bars, trades, self.policy)
            signal = None
            if new_close:
                indicator = next(
                    item
                    for item in state.indicators
                    if (item.source_id, item.stream_id, item.instrument) == feed
                )
                if indicator.ready and indicator.closed_count in (2, 3):
                    side: Literal["buy", "sell"] = "buy" if indicator.closed_count == 2 else "sell"
                    signal = SyntheticSignal(
                        id="signal-"
                        + content_hash(
                            {
                                "source": information_hash(event),
                                "policy": self.policy.digest,
                                "state": state.digest,
                                "side": side,
                            }
                        ),
                        instrument=event.instrument,
                        side=side,
                        quantity=(
                            self.policy.buy_quantity if side == "buy" else self.policy.sell_quantity
                        ),
                        decision_ns=event.effective_ns,
                        source_event_id=event.event_id,
                        source_event_hash=information_hash(event),
                        state_hash=state.digest,
                        policy_hash=self.policy.digest,
                    )
                    signals.append(signal)
            prefix = content_hash({"previous": prefix, "event": event.digest})
            records.append(
                ReplayRecord(
                    event_id=event.event_id,
                    source_id=event.source_id,
                    stream_id=event.stream_id,
                    event_hash=event.digest,
                    effective_ns=event.effective_ns,
                    kind=data.kind,
                    state=state,
                    prefix_hash=prefix,
                    signal_id=None if signal is None else signal.id,
                )
            )
            checkpoints.append(
                ReplayCheckpoint(
                    consumed_count=len(records),
                    prefix_hash=prefix,
                    state_hash=state.digest,
                    policy_hash=self.policy.digest,
                )
            )
        if checkpoint is not None:
            if checkpoint.consumed_count >= len(checkpoints) or (
                checkpoints[checkpoint.consumed_count] != checkpoint
            ):
                raise ValueError("Checkpoint prefix/state/policy changed; resumption is forbidden.")
            diagnostics.append("checkpoint_prefix_reconstructed_and_verified")
        return ReplayResult(
            records=tuple(records),
            signals=tuple(signals),
            quotes=tuple(quotes),
            diagnostics=tuple(diagnostics),
            checkpoint=checkpoints[-1],
        )
