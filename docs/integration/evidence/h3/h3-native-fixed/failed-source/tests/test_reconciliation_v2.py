"""Invented records test bookkeeping; they are never native execution evidence."""

from copy import deepcopy
from decimal import Decimal
from typing import Any

import pytest

from bot_trader.core.events import content_hash
from bot_trader.simulation.reconciliation import PostingLedger, reconcile


def fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    quotes = [
        {
            "id": "q1",
            "event_ns": 20,
            "available_ns": 21,
            "engine_init_ns": 22,
            "source_event_id": "source1",
            "source_hash": "a" * 64,
            "bids": [["99.95", "3.00"]],
            "asks": [["100.05", "3.00"]],
        },
        {
            "id": "q2",
            "event_ns": 40,
            "available_ns": 41,
            "engine_init_ns": 42,
            "source_event_id": "source2",
            "source_hash": "b" * 64,
            "bids": [["100.95", "3.00"]],
            "asks": [["101.05", "3.00"]],
        },
    ]
    commands = [
        {
            "id": "buy",
            "kind": "market",
            "signal_id": "signal-buy",
            "quote_id": "q1",
            "decision_ns": 10,
            "submitted_ns": 22,
            "side": "buy",
            "quantity": "2.00",
        },
        {
            "id": "sell",
            "kind": "market",
            "signal_id": "signal-sell",
            "quote_id": "q2",
            "decision_ns": 30,
            "submitted_ns": 42,
            "side": "sell",
            "quantity": "2.00",
        },
    ]
    request = {
        "schema_version": 1,
        "mode": "technical",
        "synthetic": True,
        "partition": "development",
        "instrument": "SYNTH-USD",
        "initial_cash_usd": "1000.00",
        "policy": {
            "version": "fixture-1",
            "fee_rate": "0.002",
            "slippage_usd": "0.00",
            "latency_ns": 0,
            "max_quote_age_ns": 10,
        },
        "quotes": quotes,
        "commands": commands,
    }
    fills = [
        {
            "id": "f1",
            "order_id": "buy",
            "signal_id": "signal-buy",
            "quote_id": "q1",
            "side": "buy",
            "quantity": "2.00",
            "price": "100.05",
            "fee": "0.40",
            "currency": "USD",
            "at": 22,
            "ts_event": 22,
            "ts_init": 22,
            "origin": "invented bookkeeping unit fixture; not a native fill",
        },
        {
            "id": "f2",
            "order_id": "sell",
            "signal_id": "signal-sell",
            "quote_id": "q2",
            "side": "sell",
            "quantity": "2.00",
            "price": "100.95",
            "fee": "0.40",
            "currency": "USD",
            "at": 42,
            "ts_event": 42,
            "ts_init": 42,
            "origin": "invented bookkeeping unit fixture; not a native fill",
        },
    ]
    result = {
        "schema_version": 1,
        "status": "completed",
        "synthetic": True,
        "financial_validation": False,
        "request_hash": content_hash(request),
        "fills": fills,
        "errors": [],
        "events": [],
        "snapshots": [],
        "cash": {"USD": "1001.00", "SYN": "0.00"},
        "free": {"USD": "1001.00", "SYN": "0.00"},
        "reserved": {"USD": "0.00", "SYN": "0.00"},
        "orders": [
            {
                "id": "buy",
                "status": "FILLED",
                "side": "buy",
                "quantity": "2.00",
                "filled": "2.00",
                "remaining": "0.00",
            },
            {
                "id": "sell",
                "status": "FILLED",
                "side": "sell",
                "quantity": "2.00",
                "filled": "2.00",
                "remaining": "0.00",
            },
        ],
        "positions": [{"id": "position1", "signed_quantity": "0.00"}],
    }
    return request, result


def partial_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    request, result = fixture()
    request["quotes"][0]["asks"][0][1] = "1.00"
    request["commands"][0]["quantity"] = "3.00"
    request["commands"][1] = {
        "id": "cancel-buy",
        "kind": "cancel",
        "target": "buy",
        "signal_id": "cancel-1",
        "quote_id": "q2",
        "decision_ns": 30,
        "submitted_ns": 42,
    }
    result["request_hash"] = content_hash(request)
    result["fills"] = result["fills"][:1]
    result["fills"][0].update(quantity="1.00", fee="0.20")
    result["cash"] = {"USD": "899.75", "SYN": "1.00"}
    result["free"] = dict(result["cash"])
    result["orders"] = [
        {
            "id": "buy",
            "status": "CANCELED",
            "side": "buy",
            "quantity": "3.00",
            "filled": "1.00",
            "remaining": "2.00",
        }
    ]
    result["positions"] = [{"id": "position1", "signed_quantity": "1.00"}]
    result["events"] = [
        {
            "kind": "native_order_event",
            "event_type": "OrderCanceled",
            "client_order_id": "buy",
            "at": 42,
            "origin": "invented unit fixture; not native execution evidence",
        }
    ]
    return request, result


def test_buy_sell_postings_match_separate_oracle_and_native_shaped_balances() -> None:
    request, result = fixture()
    checked = reconcile(request, result)
    assert checked["passed"] and not checked["financial_validation"]
    assert checked["cash_usd"] == "1001"
    assert checked["inventory"] == "0"
    assert checked["fees_usd"] == "0.8"
    assert checked["batch_oracle"]["purchase_flows_usd"] == "200.1"
    assert checked["batch_oracle"]["sale_flows_usd"] == "201.9"
    assert len(checked["postings"]) == 2
    assert checked["postings"][0]["order_id"] == "buy"
    assert checked["postings"][1]["cash_delta_usd"] == "201.5"
    assert reconcile(request, result) == checked


def test_fill_redelivery_is_idempotent_and_conflicts_do_not_change_ledger() -> None:
    request, result = fixture()
    ledger = PostingLedger("1000.00")
    first, second = result["fills"]
    assert ledger.apply(first) and ledger.apply(second)
    preserved = ledger.state()
    assert ledger.apply(deepcopy(first)) is False
    assert ledger.state() == preserved
    conflicting = {**first, "price": "100.06"}
    with pytest.raises(ValueError, match="Conflicting"):
        ledger.apply(conflicting)
    assert ledger.state() == preserved
    result["fills"].append(deepcopy(first))
    checked = reconcile(request, result)
    assert checked["passed"] and checked["duplicate_fill_rows_suppressed"] == 1
    assert checked["cash_usd"] == "1001" and len(checked["postings"]) == 2
    result["fills"].append(conflicting)
    with pytest.raises(ValueError, match="Conflicting"):
        reconcile(request, result)


def test_partial_canceled_order_keeps_only_actual_fills_and_remainder() -> None:
    request, result = partial_fixture()
    checked = reconcile(request, result)
    assert checked["passed"]
    assert checked["cash_usd"] == "899.75" and checked["inventory"] == "1"
    assert checked["fees_usd"] == "0.2" and len(checked["postings"]) == 1
    assert result["orders"][0]["remaining"] == "2.00"
    result["events"] = []
    unconfirmed = reconcile(request, result)
    assert not unconfirmed["passed"]
    assert "cancellation_confirmed:buy" in unconfirmed["problems"]
    assert unconfirmed["unresolved_orders"] == ["buy"]
    assert unconfirmed["postings"] == checked["postings"]


@pytest.mark.parametrize("status", ["PARTIALLY_FILLED", "PENDING_CANCEL", "UNKNOWN"])
def test_open_or_unknown_state_is_not_accepted_when_balances_reconcile(status: str) -> None:
    request, result = partial_fixture()
    result["orders"][0]["status"] = status
    checked = reconcile(request, result)
    assert not checked["passed"] and checked["unresolved_orders"] == ["buy"]
    assert "terminal_order:buy" in checked["problems"]
    assert checked["cash_usd"] == "899.75" and checked["inventory"] == "1"


def test_native_divergence_fee_price_and_time_anomalies_are_rejected() -> None:
    request, result = fixture()
    changed = deepcopy(result)
    changed["cash"]["USD"] = "1002.00"
    checked = reconcile(request, changed)
    assert not checked["passed"]
    assert "native_totals_equal_independent_batch" in checked["problems"]
    changed = deepcopy(result)
    changed["fills"][0]["fee"] = "0.41"
    assert "fee_quantization:f1" in reconcile(request, changed)["problems"]
    changed = deepcopy(result)
    changed["fills"][0]["price"] = "100.06"
    assert "price_and_depth_capacity:f1" in reconcile(request, changed)["problems"]
    changed = deepcopy(result)
    changed["fills"][0].update(at=19, ts_event=19, ts_init=19)
    assert "causal_bound_quote:f1" in reconcile(request, changed)["problems"]


def test_rejected_command_has_zero_effect_and_no_pending_reservations() -> None:
    request, result = fixture()
    request["commands"] = request["commands"][:1]
    result["request_hash"] = content_hash(request)
    result["fills"] = []
    result["orders"] = [
        {
            "id": "buy",
            "side": "buy",
            "quantity": "2.00",
            "status": "DENIED",
            "filled": "0.00",
            "remaining": "2.00",
        }
    ]
    result["cash"] = {"USD": "1000.00", "SYN": "0.00"}
    result["free"] = dict(result["cash"])
    assert reconcile(request, result)["passed"]
    result["reserved"]["USD"] = "5.00"
    result["free"]["USD"] = "995.00"
    assert "terminal_market_reservations_zero" in reconcile(request, result)["problems"]


def test_invalid_short_overspend_or_nondecimal_fill_does_not_mutate_ledger() -> None:
    _, result = fixture()
    ledger = PostingLedger(Decimal("1000"))
    preserved = ledger.state()
    for invalid in (
        result["fills"][1],
        {**result["fills"][0], "quantity": "1000"},
        {**result["fills"][0], "price": 100.05},
        {**result["fills"][0], "price": "NaN"},
    ):
        with pytest.raises(ValueError):
            ledger.apply(invalid)
        assert ledger.state() == preserved
