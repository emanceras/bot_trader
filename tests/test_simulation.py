from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, localcontext
from typing import Literal

import pytest
from pydantic import ValidationError

from bot_trader.core.contracts import Fill, MarketBar, Order, Portfolio
from bot_trader.core.errors import PlatformError
from bot_trader.core.ports import Cost, Execution
from bot_trader.simulation import (
    ClosePriceExecution,
    ProportionalCost,
    SyntheticSpotLedger,
    TechnicalSpotRisk,
    run_technical_ledger,
)

START = datetime(2020, 1, 1, tzinfo=UTC)


def bar(seconds: int = 0, price: str = "10", **overrides: object) -> MarketBar:
    at = START + timedelta(seconds=seconds)
    values: dict[str, object] = {
        "instrument": "SYNTH-USD",
        "event_time": at,
        "received_at": at + timedelta(seconds=1),
        "transformed_at": at + timedelta(seconds=2),
        "open": price,
        "high": price,
        "low": price,
        "close": price,
        "volume": "1",
        "interval_seconds": 60,
    }
    return MarketBar.model_validate(values | overrides)


def order(
    identifier: str = "buy-1",
    side: Literal["buy", "sell"] = "buy",
    quantity: str = "2",
    seconds: int = 2,
    **overrides: object,
) -> Order:
    at = START + timedelta(seconds=seconds)
    values: dict[str, object] = {
        "id": identifier,
        "instrument": "SYNTH-USD",
        "side": side,
        "quantity": quantity,
        "decided_at": at,
        "submitted_at": at,
    }
    return Order.model_validate(values | overrides)


@dataclass(frozen=True)
class FixedCost:
    fee: Decimal = Decimal("0.25")

    def calculate(self, order: Order, price: Decimal) -> Decimal:
        return self.fee


@dataclass(frozen=True)
class LimitlessRisk:
    """Test adapter: ledger accounting must remain safe even without risk screening."""

    def check(self, order: Order, portfolio: Portfolio) -> None:
        return None


@dataclass(frozen=True)
class AlternateExecution:
    cost: Cost

    def execute(self, order: Order, observation: MarketBar) -> Fill:
        # An independently supplied price/latency implementation behind the same port.
        price = observation.close + Decimal("1")
        return Fill(
            order_id=order.id,
            instrument=order.instrument,
            side=order.side,
            quantity=order.quantity,
            price=price,
            fee=self.cost.calculate(order, price),
            filled_at=order.submitted_at + timedelta(seconds=1),
        )


def test_cash_inventory_and_fee_conservation_for_partial_position_reduction() -> None:
    ledger = SyntheticSpotLedger(Decimal("100"), START)
    ledger.apply(order(), bar())
    ledger.apply(order("sell-1", "sell", "1", 62), bar(60, "12"))
    assert ledger.portfolio.cash == Decimal("91.968")
    assert ledger.portfolio.positions[0].quantity == Decimal("1")
    checks = ledger.conservation()
    assert checks["cash_conserved"] is True
    assert checks["inventory_conserved"] is True
    assert checks["fees_usd"] == "0.032"
    assert checks["gross_purchase_flows_usd"] == "20"
    assert checks["gross_sale_flows_usd"] == "12"


@pytest.mark.parametrize("adapter", ["observed", "alternate"])
@pytest.mark.parametrize("cost", [ProportionalCost(), FixedCost()])
def test_c_same_ledger_consumer_accepts_execution_and_cost_substitution(
    adapter: str, cost: Cost
) -> None:
    execution: Execution = (
        ClosePriceExecution(cost) if adapter == "observed" else AlternateExecution(cost)
    )
    ledger = SyntheticSpotLedger(Decimal("100"), START, execution=execution, cost=cost)
    first = ledger.apply(order(), bar())
    second = ledger.apply(order("sell-1", "sell", "2", 62), bar(60, "12"))
    expected = Decimal("100") - first.price * 2 + second.price * 2 - first.fee - second.fee
    assert ledger.portfolio.cash == expected
    assert ledger.portfolio.positions[0].quantity == 0
    assert ledger.conservation()["cash_conserved"] is True
    assert ledger.conservation()["inventory_conserved"] is True
    assert first.price == (Decimal("10") if adapter == "observed" else Decimal("11"))


@pytest.mark.parametrize(
    ("intent", "observation", "code"),
    [
        (order(quantity="20"), bar(), "insufficient_balance"),
        (order(side="sell"), bar(), "risk_rejected"),
        (order(seconds=1), bar(), "unavailable_information"),
        (order(instrument="BTC-USD"), bar(), "unsupported_instrument"),
        (order(), bar(instrument="BTC-USD"), "unsupported_instrument"),
        (order(), bar(quote_currency="USDT"), "unsupported_currency"),
        (order(), bar(quote_currency="USDC"), "unsupported_currency"),
    ],
)
def test_rejected_intention_does_not_change_state_or_consume_order_id(
    intent: Order, observation: MarketBar, code: str
) -> None:
    ledger = SyntheticSpotLedger(Decimal("100"), START)
    before = ledger.portfolio
    with pytest.raises(PlatformError) as failure:
        ledger.apply(intent, observation)
    assert failure.value.code == code
    assert ledger.portfolio == before
    assert ledger.fills == ()
    ledger.apply(order(), bar())
    assert len(ledger.fills) == 1


def test_duplicate_and_nonchronological_inputs_are_atomic() -> None:
    ledger = SyntheticSpotLedger(Decimal("100"), START)
    ledger.apply(order(), bar())
    with pytest.raises(PlatformError, match="already"):
        ledger.apply(order(), bar())
    ledger.apply(order("buy-2", seconds=62), bar(60))
    before = ledger.portfolio
    with pytest.raises(PlatformError) as failure:
        ledger.apply(order("buy-3", seconds=61), bar())
    assert failure.value.code == "nonchronological_order"
    with pytest.raises(PlatformError) as failure:
        ledger.apply(order("buy-3", seconds=63), bar())
    assert failure.value.code == "nonchronological_observation"
    assert ledger.portfolio == before
    assert len(ledger.fills) == 2


@dataclass(frozen=True)
class BadExecution:
    change: dict[str, object]

    def execute(self, order: Order, observation: MarketBar) -> Fill:
        valid = ClosePriceExecution(ProportionalCost()).execute(order, observation)
        return Fill.model_validate(valid.model_dump() | self.change)


@pytest.mark.parametrize(
    "change",
    [
        {"order_id": "another"},
        {"instrument": "BTC-USD"},
        {"side": "sell"},
        {"quantity": "1"},
        {"quote_currency": "USDT"},
        {"fee": "0"},
        {"filled_at": START},
    ],
)
def test_mismatched_execution_output_is_rejected_before_state_change(
    change: dict[str, object],
) -> None:
    ledger = SyntheticSpotLedger(Decimal("100"), START, execution=BadExecution(change))
    with pytest.raises(PlatformError):
        ledger.apply(order(), bar())
    assert ledger.portfolio.cash == 100
    assert ledger.portfolio.positions == ()
    assert ledger.fills == ()


def test_ledger_rejects_short_sales_independently_of_risk_adapter() -> None:
    ledger = SyntheticSpotLedger(Decimal("100"), START, risk=LimitlessRisk())
    with pytest.raises(PlatformError) as failure:
        ledger.apply(order(side="sell"), bar())
    assert failure.value.code == "insufficient_balance"
    assert ledger.portfolio.cash == 100


def test_risk_quantity_and_fill_resource_limits() -> None:
    ledger = SyntheticSpotLedger(
        Decimal("1000"), START, risk=TechnicalSpotRisk(maximum_quantity=Decimal("1"))
    )
    with pytest.raises(PlatformError, match="quantity"):
        ledger.apply(order(), bar())
    for index in range(100):
        ledger.apply(order(str(index), quantity="0.01"), bar())
    before = ledger.portfolio
    with pytest.raises(PlatformError) as failure:
        ledger.apply(order("overflow", quantity="0.01"), bar())
    assert failure.value.code == "resource_limit"
    assert ledger.portfolio == before


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-1"])
def test_nonfinite_negative_configuration_is_rejected(value: str) -> None:
    with pytest.raises(ValueError):
        SyntheticSpotLedger(Decimal(value), START)
    with pytest.raises(ValueError):
        ProportionalCost(Decimal(value))
    with pytest.raises(ValueError):
        TechnicalSpotRisk(Decimal(value))


def test_execution_latency_bounds_and_missing_timezone() -> None:
    for latency in (timedelta(seconds=-1), timedelta(days=2)):
        with pytest.raises(ValueError):
            ClosePriceExecution(ProportionalCost(), latency)
    with pytest.raises(ValueError, match="timezone"):
        SyntheticSpotLedger(Decimal("100"), datetime(2020, 1, 1))
    with pytest.raises(ValidationError):
        order(mode="live")


def test_technical_report_is_deterministic_and_has_no_financial_metrics() -> None:
    source = (bar(), bar(60, "12"), bar(120, "8"))
    report = run_technical_ledger(source)
    with localcontext() as context:
        context.prec = 8
        repeated = run_technical_ledger(source)
    assert repeated == report
    assert report["synthetic"] is True
    assert report["financial_validation"] is False
    assert report["fill_count"] == 2
    assert report["account_currency"] == "USD"
    assert not {"sharpe", "return", "annualized_return", "profit_factor"} & report.keys()
    checks = report["checks"]
    assert isinstance(checks, dict)
    assert checks["cash_conserved"] is True
    assert checks["inventory_conserved"] is True


@pytest.mark.parametrize(
    "source",
    [
        (),
        (bar(),),
        (bar(), bar()),
        (bar(60), bar()),
        (bar(), bar(60, instrument="BTC-USD")),
        (bar(), bar(60, quote_currency="USDT")),
        (bar(transformed_at=START + timedelta(seconds=100)), bar(60)),
    ],
)
def test_technical_report_requires_a_bounded_chronological_synthetic_fixture(
    source: tuple[MarketBar, ...],
) -> None:
    with pytest.raises(PlatformError) as failure:
        run_technical_ledger(source)
    assert failure.value.code == "invalid_fixture"
