"""Native rc7 synthetic worker. No expected fills or custom execution model."""
from __future__ import annotations

import argparse
from decimal import Decimal
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import sysconfig
import traceback

from nautilus_trader.backtest import BacktestEngine, BacktestEngineConfig, SimulationModule
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import (
    AccountType, BookAction, BookOrder, BookType, ClientOrderId, Currency,
    CurrencyPair, CurrencyType, InstrumentId, InstrumentStatus, MarketStatusAction,
    Money, OmsType, OrderBookDelta, OrderBookDeltas, OrderSide, Price, Quantity,
    QuoteTick, RecordFlag, StrategyId, Symbol, TimeInForce, Venue,
)
from nautilus_trader.trading import Strategy, StrategyConfig


def decimal_text(value):
    return str(value.as_decimal()) if hasattr(value, "as_decimal") else str(value)


def book_view(book):
    return {
        "instrument_id": str(book.instrument_id),
        "bid": str(book.best_bid_price()) if book.best_bid_price() is not None else None,
        "ask": str(book.best_ask_price()) if book.best_ask_price() is not None else None,
        "bid_size": str(book.best_bid_size()) if book.best_bid_size() is not None else None,
        "ask_size": str(book.best_ask_size()) if book.best_ask_size() is not None else None,
        "bids": {str(k): str(v) for k, v in book.bids_to_dict().items()},
        "asks": {str(k): str(v) for k, v in book.asks_to_dict().items()},
    }


def run_fixture(fixture, book_type, consumption, journal_dir=None, cut_point=None):
    assert sys.version_info[:3] == (3, 13, 16)
    assert not sysconfig.get_config_var("Py_GIL_DISABLED")
    assert importlib.metadata.version("nautilus-trader") == "2.0.0rc7"
    instrument_spec = fixture["instrument"]
    instrument_id = InstrumentId.from_str(instrument_spec["id"])
    venue = Venue("SIM")
    usd = Currency.from_str("USD")
    base = Currency(instrument_spec["base"], 8, 0, "Invented technical token", CurrencyType.CRYPTO)
    Currency.register(base, overwrite=True)
    currencies = {name: Currency.from_str(name) for name in fixture["initial_cash"]}
    native_instrument = CurrencyPair(
        instrument_id, Symbol("SYN-USD"), base, usd, 2, 2,
        Price.from_str(instrument_spec["price_tick"]),
        Quantity.from_str(instrument_spec["quantity_step"]), 0, 0,
        min_quantity=Quantity.from_str(instrument_spec["quantity_step"]),
        min_notional=Money.from_decimal(Decimal(instrument_spec["minimum_notional"]), usd),
    )
    trace, fills, native_events, rejected, snapshots, module_books, errors = [], [], [], [], [], [], []
    decisions = []
    conversion = {"before": None, "after": None, "origin": "harness causal Decimal conversion; native USD/USDT cash remains distinct"}
    latency = fixture["latency_ns"]
    journal = Path(journal_dir) if journal_dir else None
    if journal:
        journal.mkdir(parents=True, exist_ok=True)

    def durable(name, row):
        if journal:
            with (journal / name).open("a") as stream:
                stream.write(json.dumps(row, sort_keys=True) + "\n")
                stream.flush()
                os.fsync(stream.fileno())

    class BookObserver(SimulationModule):
        def process(self, ts_now, context):
            module_books.append({"at": ts_now, "origin": "native SimulationModuleContext.order_books",
                                 "phase": "native module process callback", "books": [book_view(b) for b in context.order_books]})
            return None  # Never adjust cash or invent execution effects.

    engine = BacktestEngine(BacktestEngineConfig(run_analysis=False, bypass_logging=True))
    engine.add_venue(
        venue=venue, oms_type=OmsType.NETTING, account_type=AccountType.CASH,
        starting_balances=[Money.from_decimal(Decimal(amount), currencies[name]) for name, amount in fixture["initial_cash"].items()],
        book_type=getattr(BookType, book_type), base_currency=None,
        fee_model=MakerTakerFeeModel(Decimal(instrument_spec["maker_fee"]), Decimal(instrument_spec["taker_fee"])),
        modules=[BookObserver()], use_message_queue=False,
        use_market_order_acks=True, use_random_ids=False,
        liquidity_consumption=consumption, allow_cash_borrowing=False,
        bar_execution=False, trade_execution=False,
    )
    engine.add_instrument(native_instrument)
    # Obtain the shared cache handle before run(): borrowing engine.cache again
    # inside a clock callback conflicts with the engine's mutable run borrow.
    cache = engine.cache

    def snapshot(at, source):
        account = cache.account_for_venue(venue)
        row = {
            "at": at, "source": source,
            "balances": {str(k): decimal_text(v) for k, v in account.balances_total().items()},
            "free": {str(k): decimal_text(v) for k, v in account.balances_free().items()},
            "reserved": {str(k): decimal_text(v) for k, v in account.balances_locked().items()},
            "orders": [{"id": str(o.client_order_id), "status": o.status.name,
                        "filled": str(o.filled_qty), "remaining": str(o.leaves_qty),
                        "strategy_id": str(o.strategy_id)} for o in cache.orders()],
            "positions": [{"id": str(p.id), "signed_quantity": str(p.signed_qty),
                           "quantity": str(p.quantity), "side": p.side.name,
                           "instrument_id": str(p.instrument_id)} for p in cache.positions()],
            "origin": "native cache/account snapshot; callbacks may precede later native account updates",
        }
        cached_quote = cache.quote(instrument_id)
        row["cached_quote"] = cached_quote.to_dict() if cached_quote is not None else None
        cached_book = cache.order_book(instrument_id)
        row["cached_book"] = book_view(cached_book) if cached_book is not None else None
        snapshots.append(row)
        return row

    class MechanicalFixture(Strategy):
        def __init__(self, owner):
            tag = "A" if owner == "strategy-A" else "B"
            super().__init__(StrategyConfig(strategy_id=StrategyId(f"fixture-{tag}"), order_id_tag=tag,
                                           log_events=False, log_commands=False))
            self.owner = owner
            self.known_orders = {}

        def protect(self, function, *args):
            try:
                function(*args)
            except Exception as exc:
                errors.append({"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()})

        def on_start(self):
            self.subscribe_quotes(instrument_id)
            if book_type == "L2_MBP":
                self.subscribe_book_deltas(instrument_id, BookType.L2_MBP, managed=True)
            for index, item in enumerate(fixture["commands"]):
                if item.get("strategy_id", "strategy-A") != self.owner:
                    continue
                due = item["available_ns"] + latency
                self.clock.set_time_alert_ns(f"command-{index}", due,
                    callback=lambda event, item=item: self.protect(self.command, item, event.ts_event))
            if self.owner == "strategy-A":
                for index, item in enumerate(fixture["events"]):
                    if item["kind"] not in ("quote", "book_snapshot"):
                        self.clock.set_time_alert_ns(f"information-{index}", item["available_ns"],
                            callback=lambda event, item=item: self.protect(self.information, item, event.ts_event), allow_past=True)

        def information(self, item, at):
            assert at == item["available_ns"]
            trace.append({"kind": "information_admitted", "at": at, "event": item,
                          "origin": "native nanosecond clock; harness information rule"})
            if item["kind"] == "bar_open":
                decisions.append({"at": at, "decision": "BLOCK", "bar_id": None})
            elif item["kind"] in ("bar_close", "bar_revision"):
                decisions.append({"at": at, "decision": "OBSERVE", "bar_id": item["bar_id"], "close": item["close"]})
            elif item["kind"] == "conversion":
                conversion["after"] = str(Decimal(fixture["initial_cash"]["USDT"]) * Decimal(item["rate"]))

        def command(self, item, at):
            assert at == item["available_ns"] + latency
            cid = item["command_id"]
            trace.append({"kind": "command_arrival", "at": at, "native_clock": self.clock.timestamp_ns(),
                          "command": item, "owner": self.owner})
            durable("commands.jsonl", {"at": at, "command": item})
            snapshot(at, "before:" + cid)
            if item["kind"] == "cancel":
                self.cancel_order(ClientOrderId(item["target"]))
            elif cid in self.known_orders:
                try:
                    self.submit_order(self.known_orders[cid])
                    trace.append({"kind": "duplicate_submission_returned", "command_id": cid, "at": at})
                except Exception as exc:
                    trace.append({"kind": "native_duplicate_submission_exception", "command_id": cid, "at": at,
                                  "exception": type(exc).__name__, "message": str(exc)})
            else:
                options = dict(instrument_id=instrument_id, order_side=getattr(OrderSide, item["side"]),
                               quantity=Quantity.from_str(item["quantity"]),
                               time_in_force=getattr(TimeInForce, item["tif"]), client_order_id=ClientOrderId(cid))
                try:
                    if item["kind"] == "market":
                        order = self.order_factory.market(**options)
                    else:
                        order = self.order_factory.limit(**options, price=Price.from_str(item["price"]), post_only=item.get("post_only", False))
                    self.known_orders[cid] = order
                    self.submit_order(order)
                except Exception as exc:
                    rejected.append(cid)
                    trace.append({"kind": "native_constructor_or_submit_exception", "command_id": cid,
                                  "at": at, "exception": type(exc).__name__, "message": str(exc)})
            snapshot(at, "after:" + cid)

        def record(self, event):
            row = {"type": type(event).__name__, "at": event.ts_event,
                   "ts_init": event.ts_init, "owner": self.owner}
            for name in ("client_order_id", "venue_order_id", "trade_id", "reason"):
                if hasattr(event, name):
                    row[name] = str(getattr(event, name))
            native_events.append(row)
            durable("native-events.jsonl", row)
            return row

        def on_order_submitted(self, event):
            self.record(event)
            if cut_point == "after-submit-before-ack":
                os._exit(71)

        def on_order_accepted(self, event): self.record(event)
        def on_order_canceled(self, event): self.record(event)
        def on_order_cancel_rejected(self, event): self.record(event)

        def on_order_pending_cancel(self, event):
            self.record(event)
            if cut_point == "during-cancel": os._exit(73)

        def on_order_denied(self, event):
            self.record(event); rejected.append(str(event.client_order_id))

        def on_order_rejected(self, event):
            self.record(event); rejected.append(str(event.client_order_id))

        def on_order_filled(self, event):
            self.protect(self.record_fill, event)

        def record_fill(self, event):
            self.record(event)
            if event.commission is None:
                raise ValueError("Native fill has no commission; cannot assume zero")
            row = {"venue": "SIM", "fill_id": str(event.trade_id), "command_id": str(event.client_order_id),
                   "instrument_id": str(event.instrument_id), "strategy_label": self.owner,
                   "side": event.order_side.name, "quantity": str(event.last_qty), "price": str(event.last_px),
                   "fee": decimal_text(event.commission), "fee_currency": str(event.commission.currency),
                   "liquidity_role": event.liquidity_side.name.lower(), "at": event.ts_event,
                   "origin": "native OrderFilled; no expected-fill injection"}
            fills.append(row)
            durable("venue-fills.jsonl", row)
            if cut_point == "after-fill-before-checkpoint": os._exit(72)

        def on_quote(self, quote):
            if self.owner == "strategy-A": trace.append({"kind": "native_quote_callback", "at": self.clock.timestamp_ns(), "quote": quote.to_dict()})

        def on_book_deltas(self, deltas):
            if self.owner == "strategy-A": trace.append({"kind": "native_book_callback", "at": self.clock.timestamp_ns(), "source_ts_init": deltas.ts_init})

    for owner in fixture["strategy_ids"]:
        engine.add_strategy(MechanicalFixture(owner))
    data = []
    for index, item in enumerate(fixture["events"]):
        t, available = item["event_ns"], item["available_ns"]
        if item["kind"] == "quote":
            data.append(QuoteTick(instrument_id, Price.from_str(item["bid"]), Price.from_str(item["ask"]),
                                  Quantity.from_str(item["bid_size"]), Quantity.from_str(item["ask_size"]), t, available))
        elif item["kind"] == "book_snapshot":
            deltas = [OrderBookDelta.clear(instrument_id, index + 1, t, available)]
            levels = [("BUY", p, q) for p, q in item["bids"]] + [("SELL", p, q) for p, q in item["asks"]]
            for level, (side, price, qty) in enumerate(levels):
                flags = RecordFlag.F_SNAPSHOT.value | (RecordFlag.F_LAST.value if level == len(levels)-1 else 0)
                deltas.append(OrderBookDelta(instrument_id, BookAction.ADD,
                    BookOrder(getattr(OrderSide, side), Price.from_str(price), Quantity.from_str(qty), level+1),
                    flags, index+1, t, available))
            data.append(OrderBookDeltas(instrument_id, deltas))
    first = min(item["available_ns"] for item in fixture["events"])
    last = max([e["available_ns"] for e in fixture["events"]] + [c["available_ns"] + latency for c in fixture["commands"]])
    marker = InstrumentStatus(instrument_id, MarketStatusAction.NONE, last + 100, last + 100,
                              reason="synthetic clock drain; no quote/book or market-state flags")
    if not data:
        data.append(InstrumentStatus(instrument_id, MarketStatusAction.NONE, first-1, first-1, reason="synthetic initial clock boundary"))
    data.append(marker)
    engine.add_data(data, sort=True)
    engine.run(start=first-1, end=last+101)
    final = snapshot(last+101, "final")
    result = {
        "engine": "Nautilus", "version": "2.0.0rc7", "case_id": fixture["case_id"], "run_id": fixture["run_id"], "synthetic_only": True,
        "native_configuration": {"book_type": book_type, "liquidity_consumption": consumption,
            "use_message_queue": False, "native_latency": 0, "harness_delay_ns": latency,
            "fee_model": "native MakerTakerFeeModel", "new_fill_model": False},
        "fills": fills, "native_events": native_events, "trace": trace, "snapshots": snapshots,
        "module_book_observations": module_books, "rejected_command_ids": sorted(set(rejected)),
        "decisions": decisions, "conversion": conversion, "callback_errors": errors,
        "balances": final["balances"], "free": final["free"], "reserved": final["reserved"],
        "orders": final["orders"], "positions": final["positions"],
        "terminal_marker": {"at": last+100, "type": "InstrumentStatus.NONE", "quote_or_depth_change_requested": False},
        "native_consumption_budget": None,
        "native_consumption_budget_limit": "public module exposes book state, not a separately certified internal consumption counter",
    }
    durable("completed.jsonl", {"case_id": fixture["case_id"], "balances": result["balances"], "orders": result["orders"]})
    engine.dispose()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--book", choices=["L1_MBP", "L2_MBP"])
    parser.add_argument("--consumption", choices=["true", "false"], default="true")
    parser.add_argument("--journal", type=Path)
    parser.add_argument("--cut", choices=["after-submit-before-ack", "after-fill-before-checkpoint", "during-cancel"])
    args = parser.parse_args()
    bundle = json.loads(args.bundle.read_text())
    fixtures = bundle.get("functional", bundle.get("cases"))
    fixture = next(f for f in fixtures if f["case_id"] == args.case)
    book = args.book or ("L2_MBP" if any(e["kind"] == "book_snapshot" for e in fixture["events"]) else "L1_MBP")
    result = run_fixture(fixture, book, args.consumption == "true", args.journal, args.cut)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2); stream.write("\n")
    print(json.dumps({"case_id": args.case, "native_worker_completed": True,
                      "fills": len(result["fills"]), "callback_errors": len(result["callback_errors"])}))


if __name__ == "__main__":
    main()
