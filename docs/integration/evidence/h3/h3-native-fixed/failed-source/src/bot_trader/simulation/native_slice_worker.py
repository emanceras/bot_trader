# mypy: ignore-errors
"""Isolated rc7 transport for the synthetic slice; native matching only.

This file is executed with the separately installed CPython 3.13 interpreter.
It has no application imports and adds no dependency to the stable environment.
Only validated development fixtures and market/cancel commands are accepted.
Upstream native types are unavailable in the host runtime; this isolated file
uses runtime wire checks and native integration tests, not host static typing.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import sys
import sysconfig
import traceback
from decimal import Decimal
from pathlib import Path
from typing import Any


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def exact_ns(value: Any) -> int:
    if type(value) is not int or not 0 <= value < 2**64:
        raise ValueError("Timestamp must be an exact unsigned nanosecond integer")
    return value


def number(value: Any, *, positive: bool = False, step: bool = False) -> Decimal:
    if not isinstance(value, str):
        raise ValueError("Decimal inputs must be explicit strings")
    result = Decimal(value)
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError("Invalid nonnegative finite Decimal")
    if step and result % Decimal("0.01"):
        raise ValueError("Unsupported precision; no rounding to instrument increment")
    return result


def identity(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", value):
        raise ValueError("Invalid independent identity")
    return value


def validate(request: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate the finite transport before importing or constructing an engine."""
    if (
        type(request.get("schema_version")) is not int
        or request["schema_version"] != 1
        or request.get("mode") != "technical"
        or request.get("synthetic") is not True
        or request.get("partition") != "development"
        or request.get("instrument") != "SYNTH-USD"
    ):
        raise ValueError("Only versioned synthetic development SYNTH-USD is permitted")
    number(request["initial_cash_usd"], step=True)
    policy = request["policy"]
    identity(policy["version"])
    if not Decimal(0) <= number(policy["fee_rate"]) <= Decimal(1):
        raise ValueError("Unsupported technical fee rate")
    if number(policy["slippage_usd"]) != 0:
        raise ValueError("Nonzero additional slippage has no admitted native mapping")
    if exact_ns(policy["latency_ns"]) != 0:
        raise ValueError("This slice supports only explicitly zero native order latency")
    exact_ns(policy["max_quote_age_ns"])
    quotes, commands = request["quotes"], request["commands"]
    if not isinstance(quotes, list) or not 1 <= len(quotes) <= 200:
        raise ValueError("One to 200 synthetic quote events required")
    if not isinstance(commands, list) or len(commands) > 100:
        raise ValueError("At most 100 technical commands permitted")
    by_quote: dict[str, dict[str, Any]] = {}
    previous_init = -1
    for quote in quotes:
        qid = identity(quote["id"])
        if qid in by_quote:
            raise ValueError("Quote identity duplicated after replay normalization")
        event = exact_ns(quote["event_ns"])
        available = exact_ns(quote["available_ns"])
        init = exact_ns(quote["engine_init_ns"])
        if available < event or init < available or init <= previous_init or init == 0:
            raise ValueError("Incompatible quote clocks or nondeterministic replay ordering")
        previous_init = init
        identity(quote["source_event_id"])
        if not re.fullmatch(r"[a-f0-9]{64}", quote["source_hash"]):
            raise ValueError("Missing quote source hash")
        for side in ("bids", "asks"):
            if not isinstance(quote[side], list) or not 1 <= len(quote[side]) <= 20:
                raise ValueError("Bounded nonempty synthetic depth required")
            seen: set[Decimal] = set()
            for price, quantity in quote[side]:
                price_d = number(price, positive=True, step=True)
                number(quantity, positive=True, step=True)
                if price_d in seen:
                    raise ValueError("Duplicate synthetic depth price")
                seen.add(price_d)
        if max(Decimal(x[0]) for x in quote["bids"]) >= min(
            Decimal(x[0]) for x in quote["asks"]
        ):
            raise ValueError("Crossed/locked depth is not silently repaired")
        by_quote[qid] = quote
    seen_commands: dict[str, str] = {}
    for command in commands:
        cid = identity(command["id"])
        identity(command["signal_id"])
        signature = digest(command)
        if cid in seen_commands and seen_commands[cid] != signature:
            raise ValueError("Conflicting duplicate command identity")
        seen_commands[cid] = signature
        quote = by_quote[identity(command["quote_id"])]
        decision = exact_ns(command["decision_ns"])
        submitted = exact_ns(command["submitted_ns"])
        if (
            submitted != quote["engine_init_ns"]
            or quote["event_ns"] < decision
            or quote["available_ns"] < decision
            or submitted <= decision
            or submitted - quote["event_ns"] > policy["max_quote_age_ns"]
        ):
            raise ValueError("Command lacks an eligible later quote or valid freshness")
        if command["kind"] == "market":
            if command["side"] not in ("buy", "sell"):
                raise ValueError("Only spot buy/sell supported")
            number(command["quantity"], positive=True, step=True)
        elif command["kind"] == "cancel":
            identity(command["target"])
        else:
            raise ValueError("Only market and explicit cancellation supported")
    return quotes, commands


def run(request: dict[str, Any], journal_path: Path) -> dict[str, Any]:
    quotes, commands = validate(request)
    if (
        sys.version_info[:3] != (3, 13, 16)
        or sysconfig.get_config_var("Py_GIL_DISABLED")
        or importlib.metadata.version("nautilus-trader") != "2.0.0rc7"
    ):
        raise ValueError("The approved isolated runtime is required; no auto installation")

    from nautilus_trader.backtest import BacktestEngine, BacktestEngineConfig
    from nautilus_trader.execution import MakerTakerFeeModel
    from nautilus_trader.model import (
        AccountType,
        BookAction,
        BookOrder,
        BookType,
        ClientOrderId,
        Currency,
        CurrencyPair,
        CurrencyType,
        InstrumentId,
        InstrumentStatus,
        MarketStatusAction,
        Money,
        OmsType,
        OrderBookDelta,
        OrderBookDeltas,
        OrderSide,
        Price,
        Quantity,
        QuoteTick,
        RecordFlag,
        StrategyId,
        Symbol,
        TimeInForce,
        Venue,
    )
    from nautilus_trader.trading import Strategy, StrategyConfig

    venue = Venue("SIM")
    iid = InstrumentId.from_str("SYN-USD.SIM")
    usd = Currency.from_str("USD")
    base = Currency("SYN", 8, 0, "Invented slice token", CurrencyType.CRYPTO)
    Currency.register(base, overwrite=True)
    events: list[dict[str, Any]] = []
    fills: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = []
    dispatched: dict[str, str] = {}
    order_provenance: dict[str, dict[str, Any]] = {}
    chain = "0" * 64
    journal = journal_path.open("x", encoding="utf-8")

    def emit(kind: str, at: int, **values: Any) -> dict[str, Any]:
        nonlocal chain
        row = {"sequence": len(events) + 1, "kind": kind, "at": at, **values}
        envelope = {"previous_hash": chain, "event": row}
        chain = digest(envelope)
        journal.write(json.dumps({**envelope, "hash": chain}, sort_keys=True) + "\n")
        journal.flush()
        os.fsync(journal.fileno())
        events.append(row)
        return row

    engine = BacktestEngine(BacktestEngineConfig(run_analysis=False, bypass_logging=True))
    cache = engine.cache
    policy = request["policy"]
    fee = Decimal(policy["fee_rate"])
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.CASH,
        starting_balances=[
            Money.from_decimal(Decimal(request["initial_cash_usd"]), usd),
            Money.from_decimal(Decimal(0), base),
        ],
        base_currency=None,
        book_type=BookType.L2_MBP,
        fee_model=MakerTakerFeeModel(fee, fee),
        use_message_queue=False,
        use_market_order_acks=True,
        use_random_ids=False,
        liquidity_consumption=True,
        allow_cash_borrowing=False,
        bar_execution=False,
        trade_execution=False,
    )
    engine.add_instrument(
        CurrencyPair(
            iid,
            Symbol("SYN-USD"),
            base,
            usd,
            2,
            2,
            Price.from_str("0.01"),
            Quantity.from_str("0.01"),
            0,
            0,
            min_quantity=Quantity.from_str("0.01"),
            min_notional=Money.from_decimal(Decimal("10.00"), usd),
        )
    )

    def money(value: Any) -> str:
        return str(value.as_decimal())

    def snapshot(at: int, reason: str) -> dict[str, Any]:
        account = cache.account_for_venue(venue)
        row = {
            "at": at,
            "reason": reason,
            "cash": {str(k): money(v) for k, v in account.balances_total().items()},
            "free": {str(k): money(v) for k, v in account.balances_free().items()},
            "reserved": {str(k): money(v) for k, v in account.balances_locked().items()},
            "orders": [
                {
                    "id": str(o.client_order_id),
                    "status": o.status.name,
                    "side": o.side.name.lower(),
                    "quantity": str(o.quantity),
                    "filled": str(o.filled_qty),
                    "remaining": str(o.leaves_qty),
                }
                for o in cache.orders()
            ],
            "positions": [
                {
                    "id": str(p.id),
                    "quantity": str(p.quantity),
                    "signed_quantity": str(-p.quantity.as_decimal() if p.side.name == "SHORT"
                                           else p.quantity.as_decimal()),
                    "side": p.side.name,
                }
                for p in cache.positions()
            ],
        }
        snapshots.append(row)
        emit("account_snapshot", at, state=row)
        return row

    by_init = {q["engine_init_ns"]: q for q in quotes}
    by_quote: dict[str, list[dict[str, Any]]] = {q["id"]: [] for q in quotes}
    for command in commands:
        by_quote[command["quote_id"]].append(command)

    class SliceStrategy(Strategy):
        def __init__(self) -> None:
            super().__init__(
                StrategyConfig(
                    strategy_id=StrategyId("slice-probe"),
                    order_id_tag="S",
                    log_events=False,
                    log_commands=False,
                )
            )

        def on_start(self) -> None:
            self.subscribe_book_deltas(iid, BookType.L2_MBP, managed=True)
            self.subscribe_quotes(iid)

        def fail(self, exc: Exception) -> None:
            row = {"type": type(exc).__name__, "message": str(exc)}
            errors.append(row)
            emit("callback_error", self.clock.timestamp_ns(), error=row)

        def on_book_deltas(self, deltas: Any) -> None:
            emit(
                "book_received",
                self.clock.timestamp_ns(),
                ts_event=deltas.ts_event,
                ts_init=deltas.ts_init,
                source_event_id=by_init[deltas.ts_init]["source_event_id"],
            )

        def on_quote(self, quote: Any) -> None:
            try:
                now = self.clock.timestamp_ns()
                source = by_init[quote.ts_init]
                emit(
                    "quote_received",
                    now,
                    quote_id=source["id"],
                    ts_event=quote.ts_event,
                    ts_init=quote.ts_init,
                    source_event_id=source["source_event_id"],
                    source_hash=source["source_hash"],
                    bid=str(quote.bid_price),
                    ask=str(quote.ask_price),
                    origin="synthetic depth top-of-book reference, no extra liquidity",
                )
                snapshot(now, "before_quote_commands:" + source["id"])
                for command in by_quote[source["id"]]:
                    if errors:
                        break
                    self.dispatch(command, source, now)
            except Exception as exc:
                self.fail(exc)

        def dispatch(self, command: dict[str, Any], source: dict[str, Any], now: int) -> None:
            if now != command["submitted_ns"] or source["event_ns"] < command["decision_ns"]:
                raise ValueError("Native callback violates causal command binding")
            cid, signature = command["id"], digest(command)
            if cid in dispatched:
                if dispatched[cid] != signature:
                    raise ValueError("Conflicting repeated command during dispatch")
                emit("duplicate_command_suppressed", now, command_id=cid)
                return
            emit("command_pending", now, command=command, signature=signature)
            dispatched[cid] = signature
            if command["kind"] == "cancel":
                current = cache.order(ClientOrderId(command["target"]))
                if current is None:
                    emit("cancel_unknown", now, command_id=cid, target=command["target"])
                    errors.append({"type": "UnknownOrder", "message": command["target"]})
                    return
                if current.status.name in ("FILLED", "CANCELED", "REJECTED", "DENIED", "EXPIRED"):
                    emit(
                        "cancel_not_needed_terminal",
                        now,
                        command_id=cid,
                        target=command["target"],
                        native_status=current.status.name,
                    )
                    return
                self.cancel_order(ClientOrderId(command["target"]))
                emit("cancel_requested", now, command_id=cid, target=command["target"])
                return
            order_provenance[cid] = command
            order = self.order_factory.market(
                instrument_id=iid,
                order_side=OrderSide.BUY if command["side"] == "buy" else OrderSide.SELL,
                quantity=Quantity.from_str(command["quantity"]),
                time_in_force=TimeInForce.GTC,
                client_order_id=ClientOrderId(cid),
            )
            self.submit_order(order)
            emit(
                "dispatch_returned",
                now,
                command_id=cid,
                nominal_arrival_ns=now,
                arrival_is_observed=False,
            )

        def record(self, event: Any) -> None:
            values = {
                name: str(getattr(event, name))
                for name in ("client_order_id", "venue_order_id", "trade_id", "reason")
                if hasattr(event, name)
            }
            emit(
                "native_order_event",
                self.clock.timestamp_ns(),
                event_type=type(event).__name__,
                ts_event=event.ts_event,
                ts_init=event.ts_init,
                **values,
            )

        def on_order_submitted(self, event: Any) -> None:
            self.record(event)

        def on_order_accepted(self, event: Any) -> None:
            self.record(event)

        def on_order_denied(self, event: Any) -> None:
            self.record(event)

        def on_order_rejected(self, event: Any) -> None:
            self.record(event)

        def on_order_pending_cancel(self, event: Any) -> None:
            self.record(event)

        def on_order_canceled(self, event: Any) -> None:
            self.record(event)

        def on_order_cancel_rejected(self, event: Any) -> None:
            self.record(event)

        def on_order_filled(self, event: Any) -> None:
            try:
                self.record(event)
                if event.commission is None:
                    raise ValueError("Missing fee is not zero")
                command = order_provenance[str(event.client_order_id)]
                row = {
                    "id": str(event.trade_id),
                    "order_id": str(event.client_order_id),
                    "signal_id": command["signal_id"],
                    "quote_id": command["quote_id"],
                    "side": event.order_side.name.lower(),
                    "quantity": str(event.last_qty),
                    "price": str(event.last_px),
                    "fee": money(event.commission),
                    "currency": str(event.commission.currency),
                    "at": self.clock.timestamp_ns(),
                    "ts_event": event.ts_event,
                    "ts_init": event.ts_init,
                    "origin": "native OrderFilled; no injected fill",
                }
                fills.append(row)
                emit("native_fill", row["at"], fill=row)
            except Exception as exc:
                self.fail(exc)

    engine.add_strategy(SliceStrategy())
    data: list[Any] = []
    for sequence, quote in enumerate(quotes, 1):
        t, init = quote["event_ns"], quote["engine_init_ns"]
        deltas = [OrderBookDelta.clear(iid, sequence, t, init)]
        levels = [(OrderSide.BUY, p, q) for p, q in quote["bids"]]
        levels += [(OrderSide.SELL, p, q) for p, q in quote["asks"]]
        for index, (side, price, quantity) in enumerate(levels):
            flags = RecordFlag.F_SNAPSHOT.value
            if index == len(levels) - 1:
                flags |= RecordFlag.F_LAST.value
            deltas.append(
                OrderBookDelta(
                    iid,
                    BookAction.ADD,
                    BookOrder(side, Price.from_str(price), Quantity.from_str(quantity), index + 1),
                    flags,
                    sequence,
                    t,
                    init,
                )
            )
        data.append(OrderBookDeltas(iid, deltas))
        bid, bid_size = max(quote["bids"], key=lambda level: Decimal(level[0]))
        ask, ask_size = min(quote["asks"], key=lambda level: Decimal(level[0]))
        data.append(
            QuoteTick(
                iid,
                Price.from_str(bid),
                Price.from_str(ask),
                Quantity.from_str(bid_size),
                Quantity.from_str(ask_size),
                t,
                init,
            )
        )
    first, last = quotes[0]["engine_init_ns"], quotes[-1]["engine_init_ns"]
    exact_ns(last + 101)
    data.append(
        InstrumentStatus(
            iid,
            MarketStatusAction.NONE,
            last + 100,
            last + 100,
            reason="terminal clock drain only; no synthetic price update",
        )
    )
    emit("worker_started", first - 1, request_hash=digest(request))
    try:
        engine.add_data(data, sort=True)
        engine.run(start=first - 1, end=last + 101)
        final = snapshot(last + 101, "final_after_native_queue")
        result = {
            "schema_version": 1,
            "status": "completed" if not errors else "failed",
            "synthetic": True,
            "financial_validation": False,
            "engine": "NautilusTrader",
            "engine_version": "2.0.0rc7",
            "python": "3.13.16",
            "request_hash": digest(request),
            "instrument_mapping": {"SYNTH-USD": "SYN-USD.SIM"},
            "policy": policy,
            "native_configuration": {
                "book_type": "L2_MBP",
                "bar_execution": False,
                "trade_execution": False,
                "liquidity_consumption": True,
                "native_latency_ns": 0,
                "use_message_queue": False,
                "risk_enabled": True,
                "custom_fill_model": False,
            },
            "fills": fills,
            "orders": final["orders"],
            "cash": final["cash"],
            "free": final["free"],
            "reserved": final["reserved"],
            "positions": final["positions"],
            "snapshots": snapshots,
            "errors": errors,
            "limitations": [
                "Synthetic depth/reference quotes are assumptions, not observed liquidity.",
                "OrderAccepted is observed processing, not independent arrival measurement.",
                "Pending commands and cancel requests are not execution confirmation.",
                "No automatic replay/resubmission after interruption or unknown state.",
            ],
        }
        emit("worker_completed", last + 101, status=result["status"])
        result["events"] = events
        result["journal_terminal_hash"] = chain
        return result
    finally:
        engine.dispose()
        journal.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--journal", type=Path)
    args = parser.parse_args()
    if args.request.stat().st_size > 3 * 1024**2:
        raise ValueError("Input exceeds the finite synthetic slice limit")
    request = json.loads(args.request.read_text())
    journal = args.journal or args.output.with_suffix(".events.jsonl")
    try:
        result = run(request, journal)
    except Exception as exc:
        result = {
            "schema_version": 1,
            "status": "failed",
            "synthetic": True,
            "financial_validation": False,
            "errors": [{"type": type(exc).__name__, "message": str(exc)}],
            "traceback": traceback.format_exc(),
            "native_state": "unknown_if_journal_exists; no inferred fills or cancellations",
        }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "output": str(args.output)}))
    raise SystemExit(0 if result["status"] == "completed" else 2)


if __name__ == "__main__":
    main()
