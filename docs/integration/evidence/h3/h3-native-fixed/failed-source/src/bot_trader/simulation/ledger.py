"""Deterministic spot accounting fixture with explicit adapter validation.

This harness only accepts SYNTH-USD. Its full fills at observed fixture prices
are accounting assumptions, not evidence of executable market prices. It has no
strategy, exchange, leverage, partial-fill, funding or financial-metric engine.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, localcontext

from pydantic import JsonValue

from bot_trader.core.contracts import Fill, MarketBar, Order, Portfolio, Position, utc_time
from bot_trader.core.errors import PlatformError
from bot_trader.core.ports import Cost, Execution, Risk

INSTRUMENT = "SYNTH-USD"
MAX_BARS = 10_000
MAX_FILLS = 100
ZERO = Decimal("0")


def _reject(code: str, message: str) -> PlatformError:
    return PlatformError(code, message)


def _available_at(observation: MarketBar) -> datetime:
    return max(
        value
        for value in (
            observation.event_time,
            observation.published_at,
            observation.provider_available_at,
            observation.received_at,
            observation.transformed_at,
        )
        if value is not None
    )


@dataclass(frozen=True)
class ProportionalCost:
    """Explicit nonnegative technical fee assumption, not an exchange tariff."""

    rate: Decimal = Decimal("0.001")

    def __post_init__(self) -> None:
        if not self.rate.is_finite() or not ZERO <= self.rate <= Decimal("1"):
            raise ValueError("Technical fee rate must be finite and between zero and one.")

    def calculate(self, order: Order, price: Decimal) -> Decimal:
        with localcontext() as context:
            context.prec = 50
            return order.quantity * price * self.rate


@dataclass(frozen=True)
class ClosePriceExecution:
    """Full fixture fill at a previously received close; no market realism claim."""

    cost: Cost
    latency: timedelta = timedelta(0)

    def __post_init__(self) -> None:
        if not timedelta(0) <= self.latency <= timedelta(days=1):
            raise ValueError("Technical execution latency must be between zero and one day.")

    def execute(self, order: Order, observation: MarketBar) -> Fill:
        return Fill(
            order_id=order.id,
            instrument=order.instrument,
            side=order.side,
            quantity=order.quantity,
            price=observation.close,
            fee=self.cost.calculate(order, observation.close),
            filled_at=order.submitted_at + self.latency,
        )


@dataclass(frozen=True)
class TechnicalSpotRisk:
    """Independent quantity/short-sale check; cash is validated after the fill quote."""

    maximum_quantity: Decimal = Decimal("1000000")

    def __post_init__(self) -> None:
        if not self.maximum_quantity.is_finite() or self.maximum_quantity <= ZERO:
            raise ValueError("The quantity bound must be positive and finite.")

    def check(self, order: Order, portfolio: Portfolio) -> None:
        if order.quantity > self.maximum_quantity:
            raise _reject("risk_rejected", "Technical order exceeds the quantity bound.")
        position = next(
            (item.quantity for item in portfolio.positions if item.instrument == order.instrument),
            ZERO,
        )
        if order.side == "sell" and order.quantity > position:
            raise _reject("risk_rejected", "Technical spot accounting does not allow short sales.")


class SyntheticSpotLedger:
    """One instrument, finite full fills, atomic validated cash/inventory changes.

    Adapters are trusted in-process implementations, but their outputs are still
    checked. A rejected order leaves balances, fills and order identities unchanged.
    No output can activate a different runtime mode or instrument.
    """

    def __init__(
        self,
        initial_cash: Decimal,
        valued_at: datetime,
        *,
        execution: Execution | None = None,
        cost: Cost | None = None,
        risk: Risk | None = None,
    ) -> None:
        if not initial_cash.is_finite() or initial_cash < ZERO:
            raise ValueError("Initial technical cash must be finite and nonnegative.")
        self._cost = cost if cost is not None else ProportionalCost()
        self._execution = execution if execution is not None else ClosePriceExecution(self._cost)
        self._risk = risk if risk is not None else TechnicalSpotRisk()
        self._portfolio = Portfolio(cash=initial_cash, valued_at=utc_time(valued_at))
        self._initial_cash = initial_cash
        self._fills: tuple[Fill, ...] = ()
        self._order_ids: set[str] = set()
        self._latest_event_time: datetime | None = None

    @property
    def portfolio(self) -> Portfolio:
        return self._portfolio

    @property
    def fills(self) -> tuple[Fill, ...]:
        return self._fills

    def apply(self, order: Order, observation: MarketBar) -> Fill:
        if order.instrument != INSTRUMENT or observation.instrument != INSTRUMENT:
            raise _reject("unsupported_instrument", "Only the SYNTH-USD fixture is supported.")
        if observation.quote_currency != "USD":
            raise _reject("unsupported_currency", "Technical accounting requires actual USD units.")
        if order.id in self._order_ids:
            raise _reject("duplicate_order", "This technical order has already been filled.")
        if len(self._fills) >= MAX_FILLS:
            raise _reject("resource_limit", "The finite technical fill budget is exhausted.")
        if order.decided_at < _available_at(observation):
            raise _reject("unavailable_information", "Decision precedes observation availability.")
        if order.decided_at < self._portfolio.valued_at:
            raise _reject("nonchronological_order", "Decision precedes the previous ledger state.")
        if self._latest_event_time is not None and observation.event_time < self._latest_event_time:
            raise _reject(
                "nonchronological_observation", "Observation is older than the ledger input."
            )
        self._risk.check(order, self._portfolio)
        fill = self._execution.execute(order, observation)
        if (
            fill.order_id != order.id
            or fill.instrument != order.instrument
            or fill.side != order.side
            or fill.quantity != order.quantity
            or fill.quote_currency != "USD"
            or fill.mode != "technical"
        ):
            raise _reject(
                "invalid_fill", "Execution returned a mismatched or unsupported full fill."
            )
        if fill.filled_at < order.submitted_at or fill.filled_at < _available_at(observation):
            raise _reject(
                "invalid_fill_time", "Execution precedes submission or information receipt."
            )
        expected_fee = self._cost.calculate(order, fill.price)
        if not expected_fee.is_finite() or expected_fee < ZERO or fill.fee != expected_fee:
            raise _reject(
                "invalid_fee", "Execution fee does not match the configured cost adapter."
            )
        quantity = next((item.quantity for item in self._portfolio.positions), ZERO)
        with localcontext() as context:
            context.prec = 50
            notional = fill.quantity * fill.price
            if fill.side == "buy":
                cash = self._portfolio.cash - notional - fill.fee
                quantity += fill.quantity
            else:
                cash = self._portfolio.cash + notional - fill.fee
                quantity -= fill.quantity
            if cash < ZERO or quantity < ZERO:
                raise _reject(
                    "insufficient_balance", "The fill exceeds available cash or inventory."
                )
            portfolio = Portfolio(
                cash=cash,
                positions=(Position(instrument=INSTRUMENT, quantity=quantity),),
                valued_at=fill.filled_at,
            )
        self._portfolio = portfolio
        self._fills += (fill,)
        self._order_ids.add(order.id)
        self._latest_event_time = observation.event_time
        return fill

    def conservation(self) -> dict[str, JsonValue]:
        """Reconstruct state from recorded flows, without mark-to-market returns."""
        with localcontext() as context:
            context.prec = 50
            bought = sum((f.quantity for f in self._fills if f.side == "buy"), ZERO)
            sold = sum((f.quantity for f in self._fills if f.side == "sell"), ZERO)
            spent = sum((f.price * f.quantity for f in self._fills if f.side == "buy"), ZERO)
            received = sum((f.price * f.quantity for f in self._fills if f.side == "sell"), ZERO)
            fees = sum((f.fee for f in self._fills), ZERO)
            quantity = next((item.quantity for item in self._portfolio.positions), ZERO)
            cash_expected = self._initial_cash - spent + received - fees
            return {
                "cash_conserved": self._portfolio.cash == cash_expected,
                "inventory_conserved": quantity == bought - sold,
                "initial_cash_usd": str(self._initial_cash),
                "cash_usd": str(self._portfolio.cash),
                "inventory_synth": str(quantity),
                "fees_usd": str(fees),
                "gross_purchase_flows_usd": str(spent),
                "gross_sale_flows_usd": str(received),
            }


def run_technical_ledger(bars: Sequence[MarketBar]) -> dict[str, JsonValue]:
    """Run two fixed fixture intentions for accounting and adapter checks only.

    Quantity and synthetic cash are derived only from the first received fixture
    observation. There is no signal fitting, parameter search or profit metric.
    """
    if not 2 <= len(bars) <= MAX_BARS:
        raise _reject("invalid_fixture", "A technical ledger requires 2 to 10000 fixture bars.")
    for previous, current in zip(bars, bars[1:], strict=False):
        if current.event_time <= previous.event_time:
            raise _reject("invalid_fixture", "Fixture event times must be unique and increasing.")
        if _available_at(current) < _available_at(previous):
            raise _reject("invalid_fixture", "Fixture information availability must be ordered.")
    if any(bar.instrument != INSTRUMENT or bar.quote_currency != "USD" for bar in bars):
        raise _reject("invalid_fixture", "All fixture rows must be explicitly SYNTH-USD in USD.")
    first, last = bars[0], bars[-1]
    with localcontext() as context:
        context.prec = 50
        initial_cash = first.close * Decimal("10")
    ledger = SyntheticSpotLedger(initial_cash=initial_cash, valued_at=_available_at(first))
    for identifier, side, observation in (
        ("technical-buy", "buy", first),
        ("technical-sell", "sell", last),
    ):
        order = Order(
            id=identifier,
            instrument=INSTRUMENT,
            side="buy" if side == "buy" else "sell",
            quantity=Decimal("1"),
            decided_at=_available_at(observation),
            submitted_at=_available_at(observation),
        )
        ledger.apply(order, observation)
    return {
        "kind": "synthetic_ledger_check",
        "protocol_version": 1,
        "synthetic": True,
        "financial_validation": False,
        "label": "Technical accounting fixture; no financial-performance evaluation",
        "instrument": INSTRUMENT,
        "account_currency": "USD",
        "fill_count": len(ledger.fills),
        "assumptions": "Two fixed full fills at received fixture closes; technical fee rate 0.001.",
        "checks": ledger.conservation(),
        "fills": [fill.model_dump(mode="json") for fill in ledger.fills],
    }
