#!/usr/bin/env python3
"""Isolated Nautilus 1.231.0 technical admission probe; invented data only.

Run with the authorized disposable venv Python, never the application worker:
  python tools/admission/nautilus_probe.py --output /absolute/scratch/probe
No market adapter, network, financial analysis or investment rule is used.
Fixed order schedules are mechanical test fixtures. Fees/minima/latency below
are test constants, not proposed operational/economic criteria.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import resource
import subprocess
import sys
import time
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

CASES = (
    "roundtrip",
    "early_sell",
    "partial_market",
    "partial_ioc",
    "unfilled_cancel",
    "post_only_reject",
    "maker_fill",
    "insufficient_cash",
    "minimum_notional",
    "quantity_precision",
    "duplicate_submit",
    "duplicate_fill",
    "bounded_load",
    "interrupted",
)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def native_case(name, path):
    import nautilus_trader
    from nautilus_trader.backtest.engine import BacktestEngine
    from nautilus_trader.backtest.models import LatencyModel
    from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
    from nautilus_trader.model.currencies import USD
    from nautilus_trader.model.data import QuoteTick
    from nautilus_trader.model.enums import (
        AccountType,
        CurrencyType,
        OmsType,
        OrderSide,
        TimeInForce,
    )
    from nautilus_trader.model.identifiers import InstrumentId, Symbol, Venue
    from nautilus_trader.model.instruments import CurrencyPair
    from nautilus_trader.model.objects import Currency, Money, Price, Quantity
    from nautilus_trader.trading.strategy import Strategy

    assert nautilus_trader.__version__ == "1.231.0", "Exact authorized version required"
    synthetic = Currency("SYN", 8, 0, "Invented fixture token", CurrencyType.CRYPTO)
    Currency.register(synthetic)
    instrument = CurrencyPair(
        InstrumentId.from_str("SYN-USD.SIM"),
        Symbol("SYN-USD"),
        synthetic,
        USD,
        2,
        2,
        Price.from_str("0.01"),
        Quantity.from_str("0.01"),
        0,
        0,
        min_quantity=Quantity.from_str("0.01"),
        min_notional=Money(10, USD),
        maker_fee=Decimal("0.001"),
        taker_fee=Decimal("0.002"),
    )
    engine = BacktestEngine(
        BacktestEngineConfig(
            run_analysis=False,
            logging=LoggingConfig(bypass_logging=True),
        )
    )
    engine.add_venue(
        Venue("SIM"),
        OmsType.NETTING,
        AccountType.CASH,
        [Money(1000, USD), Money(0, synthetic)],
        base_currency=None,
        latency_model=LatencyModel(base_latency_nanos=25),
        use_market_order_acks=True,
        liquidity_consumption=True,
    )
    engine.add_instrument(instrument)

    def event_record(event):
        result = {
            "type": type(event).__name__,
            "ts_event": event.ts_event,
            "ts_init": event.ts_init,
        }
        for field in (
            "client_order_id",
            "venue_order_id",
            "trade_id",
            "order_side",
            "last_qty",
            "last_px",
            "commission",
            "liquidity_side",
            "reason",
        ):
            if hasattr(event, field):
                value = getattr(event, field)
                result[field] = str(getattr(value, "name", value))
        return result

    def snapshot():
        account = engine.cache.account_for_venue(Venue("SIM"))
        return {
            "balances": {str(k): str(v.as_decimal()) for k, v in account.balances_total().items()},
            "free_balances": {
                str(k): str(v.as_decimal()) for k, v in account.balances_free().items()
            },
            "locked_balances": {
                str(k): str(v.as_decimal()) for k, v in account.balances_locked().items()
            },
            "orders": [
                {
                    "id": str(o.client_order_id),
                    "status": o.status.name,
                    "filled_qty": str(o.filled_qty),
                    "leaves_qty": str(o.leaves_qty),
                }
                for o in engine.cache.orders()
            ],
            "positions": [
                {
                    "id": str(p.id),
                    "side": p.side.name,
                    "quantity": str(p.quantity),
                    "signed_qty": str(p.signed_qty),
                }
                for p in engine.cache.positions()
            ],
        }

    class MechanicalFixture(Strategy):
        def __init__(self):
            super().__init__(
                StrategyConfig(order_id_tag="SYN", log_events=False, log_commands=False)
            )
            self.tick_count = 0
            self.events = []
            self.order = None
            self.duplicate_error = None
            self.trace = []
            self.pre_cancel_snapshot = None

        def on_start(self):
            self.subscribe_quote_ticks(instrument.id)

        def on_quote_tick(self, tick):
            self.tick_count += 1
            if len(self.trace) < 6:
                self.trace.append(
                    {"tick": self.tick_count, "ts_event": tick.ts_event, "ts_init": tick.ts_init}
                )
            if name == "interrupted" and self.tick_count == 3:
                write_json(
                    path,
                    {
                        "status": "intentional_process_interruption",
                        "snapshot": snapshot(),
                        "events": [event_record(e) for e in self.events],
                        "resources": {
                            "user_cpu_seconds": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                            "system_cpu_seconds": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
                            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                        },
                    },
                )
                os._exit(23)  # Deliberate crash; output is evidence, not an engine checkpoint.
            if name == "bounded_load":
                return
            if self.tick_count == 1:
                quantity = {
                    "partial_market": "4.00",
                    "partial_ioc": "4.00",
                    "insufficient_cash": "20.00",
                    "minimum_notional": "0.01",
                    "quantity_precision": "1.001",
                }.get(name, "2.00")
                if name in ("unfilled_cancel", "post_only_reject", "maker_fill"):
                    limit_price = {
                        "unfilled_cancel": "50.00",
                        "post_only_reject": "110.00",
                        "maker_fill": "100.00",
                    }[name]
                    self.order = self.order_factory.limit(
                        instrument.id,
                        OrderSide.BUY,
                        Quantity.from_str("2.00"),
                        Price.from_str(limit_price),
                        post_only=name == "post_only_reject",
                    )
                else:
                    self.order = self.order_factory.market(
                        instrument.id,
                        OrderSide.BUY,
                        Quantity.from_str(quantity),
                        time_in_force=TimeInForce.IOC if name == "partial_ioc" else TimeInForce.GTC,
                    )
                self.submit_order(self.order)
                if name == "duplicate_submit":
                    try:
                        self.submit_order(self.order)
                    except Exception as error:
                        self.duplicate_error = {"type": type(error).__name__, "message": str(error)}
            if self.tick_count == 2 and name == "early_sell":
                self.submit_order(
                    self.order_factory.market(
                        instrument.id, OrderSide.SELL, Quantity.from_str("2.00")
                    )
                )
            if self.tick_count == 3:
                if name == "roundtrip":
                    self.submit_order(
                        self.order_factory.market(
                            instrument.id, OrderSide.SELL, Quantity.from_str("2.00")
                        )
                    )
                if name == "unfilled_cancel":
                    self.pre_cancel_snapshot = snapshot()
                    self.cancel_order(self.order)

        def on_order_event(self, event):
            self.events.append(event)

    strategy = MechanicalFixture()
    engine.add_strategy(strategy)
    depth = "1.00" if name in ("partial_market", "partial_ioc") else "5.00"
    prices = [("99.00", "101.00"), ("102.00", "104.00"), ("103.00", "105.00"), ("105.00", "107.00")]
    if name == "maker_fill":
        prices[2] = ("98.00", "99.00")
    tick_count = 10000 if name == "bounded_load" else len(prices)
    quotes = []
    for n in range(tick_count):
        bid, ask = prices[n % len(prices)]
        stamp = (n + 1) * 1_000_000_000
        quotes.append(
            QuoteTick(
                instrument.id,
                Price.from_str(bid),
                Price.from_str(ask),
                Quantity.from_str(depth),
                Quantity.from_str(depth),
                stamp,
                stamp + 10,
            )
        )
    engine.add_data(quotes)
    run_start = time.perf_counter()
    engine.run()
    run_seconds = time.perf_counter() - run_start
    before_duplicate = snapshot()
    duplicate = None
    if name == "duplicate_fill":
        fills = [e for e in strategy.events if type(e).__name__ == "OrderFilled"]
        assert len(fills) == 1
        event_count_before = len(strategy.events)
        engine.kernel.exec_engine.process(fills[0])
        duplicate = {
            "unchanged_account_orders_positions": before_duplicate == snapshot(),
            "no_second_strategy_event": event_count_before == len(strategy.events),
            "scope": "native same-fill/trade-ID idempotency; not venue matching",
        }
    events = [event_record(e) for e in strategy.events]
    state = snapshot()
    fills = [e for e in events if e["type"] == "OrderFilled"]
    cash, inventory = Decimal("1000"), Decimal("0")
    fees_expected = []
    for fill in fills:
        size, price = Decimal(fill["last_qty"]), Decimal(fill["last_px"])
        sign = Decimal(1) if fill["order_side"] == "BUY" else Decimal(-1)
        observed_fee, currency = fill["commission"].split(" ")
        rate = Decimal("0.001") if fill["liquidity_side"] == "MAKER" else Decimal("0.002")
        expected_fee = (size * price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        fees_expected.append(
            {
                "expected_usd": str(expected_fee),
                "observed_usd": observed_fee,
                "equal": currency == "USD" and Decimal(observed_fee) == expected_fee,
            }
        )
        cash -= sign * size * price + expected_fee
        inventory += sign * size
    oracle = {
        "cash_usd": str(cash),
        "inventory_syn": str(inventory),
        "fees": fees_expected,
        "balances_equal": cash == Decimal(state["balances"]["USD"])
        and inventory == Decimal(state["balances"]["SYN"]),
        "position_equal": inventory
        == sum((Decimal(p["signed_qty"]) for p in state["positions"]), Decimal(0)),
        "scope": "independent Decimal cash/inventory/fees; no external venue statement",
    }
    result = {
        "case": name,
        "events": events,
        "state": state,
        "oracle": oracle,
        "duplicate_fill": duplicate,
        "duplicate_submit_error": strategy.duplicate_error,
        "pre_cancel_snapshot": strategy.pre_cancel_snapshot,
        "tick_trace": strategy.trace,
        "tick_count": strategy.tick_count,
        "input_tick_count": tick_count,
        "engine_run_seconds": run_seconds,
    }
    engine.dispose()
    result["resources"] = {
        "user_cpu_seconds": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
        "system_cpu_seconds": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    write_json(path, result)


def check_case(result):
    name = result["case"]
    checks = []

    def check(description, condition):
        checks.append({"check": description, "passed": bool(condition)})

    state, events, oracle = result["state"], result["events"], result["oracle"]
    fills = [e for e in events if e["type"] == "OrderFilled"]
    statuses = [o["status"] for o in state["orders"]]
    check("independent cash and inventory reconciliation", oracle["balances_equal"])
    check("independent position reconciliation", oracle["position_equal"])
    check(
        "cash account free plus locked equals total",
        all(
            Decimal(state["free_balances"][currency]) + Decimal(state["locked_balances"][currency])
            == Decimal(total)
            for currency, total in state["balances"].items()
        ),
    )
    check("per-fill synthetic fee oracle", all(f["equal"] for f in oracle["fees"]))
    check(
        "no fill before its order submission",
        all(
            f["ts_event"]
            >= next(
                e["ts_event"]
                for e in events
                if e["type"] == "OrderSubmitted" and e["client_order_id"] == f["client_order_id"]
            )
            for f in fills
        ),
    )
    if name == "roundtrip":
        check(
            "scripted buy and sell fully close inventory",
            len(fills) == 2 and oracle["inventory_syn"] == "0.00",
        )
        check("fixed-price fee/cash oracle", oracle["cash_usd"] == "1001.1600")
        check(
            "queued latency resolves at following tick",
            [f["ts_event"] for f in fills] == [2_000_000_010, 4_000_000_010],
        )
    elif name == "early_sell":
        check(
            "sell before bought inventory arrives denied natively", statuses == ["FILLED", "DENIED"]
        )
    elif name == "partial_market":
        check(
            "native matching emits partial size smaller than requested",
            bool(fills) and Decimal(fills[0]["last_qty"]) < Decimal("4"),
        )
        check(
            "finite visible liquidity is not overfilled",
            sum(Decimal(f["last_qty"]) for f in fills) <= Decimal("1"),
        )
    elif name == "partial_ioc":
        check(
            "native IOC partially fills visible size then cancels remainder",
            len(fills) == 1 and fills[0]["last_qty"] == "1.00" and statuses == ["CANCELED"],
        )
    elif name == "post_only_reject":
        check(
            "native simulated venue rejects marketable post-only order",
            not fills and statuses == ["REJECTED"],
        )
    elif name == "maker_fill":
        check(
            "resting limit fills with maker fee",
            len(fills) == 1 and fills[0]["liquidity_side"] == "MAKER",
        )
    elif name == "unfilled_cancel":
        check(
            "nonmarketable limit stays unfilled and cancels", not fills and statuses == ["CANCELED"]
        )
        check(
            "cancel releases previously locked funds",
            Decimal(result["pre_cancel_snapshot"]["locked_balances"]["USD"]) > 0
            and Decimal(state["locked_balances"]["USD"]) == 0,
        )
    elif name in ("insufficient_cash", "minimum_notional", "quantity_precision"):
        check(
            "native risk validation denies invalid order without a fill",
            not fills and statuses == ["DENIED"],
        )
    elif name == "duplicate_submit":
        check(
            "duplicate submission does not add order or fill",
            len(state["orders"]) == 1 and len(fills) == 1,
        )
    elif name == "duplicate_fill":
        check(
            "same fill ID is idempotent in native execution engine",
            result["duplicate_fill"]["unchanged_account_orders_positions"]
            and result["duplicate_fill"]["no_second_strategy_event"],
        )
    elif name == "bounded_load":
        check(
            "bounded load executes all 10000 invented ticks without orders",
            result["tick_count"] == result["input_tick_count"] == 10000 and not state["orders"],
        )
    return checks


def manager(output):
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise SystemExit("Use an empty output directory to preserve prior runs")
    start = time.perf_counter()
    metadata = []
    for dist in sorted(
        importlib.metadata.distributions(), key=lambda d: d.metadata["Name"].lower()
    ):
        record = dist.read_text("RECORD")
        metadata.append(
            {
                "name": dist.metadata["Name"],
                "version": dist.version,
                "installed_record_sha256": hashlib.sha256(record.encode()).hexdigest()
                if record
                else None,
            }
        )
    (output / "requirements-resolved.txt").write_text(
        "".join(f"{d['name']}=={d['version']}\n" for d in metadata)
    )
    outcomes = []
    for name in (*CASES, "roundtrip"):
        label = "roundtrip_replay" if name == "roundtrip" and outcomes else name
        child_output = output / f"{label}.json"
        log_path = output / f"{label}.log"
        child_start = time.perf_counter()
        with log_path.open("w") as log:
            process = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--case",
                    name,
                    "--child-output",
                    str(child_output),
                ],
                stdout=log,
                stderr=log,
                timeout=90,
                check=False,
            )
        elapsed = time.perf_counter() - child_start
        item = {
            "case": label,
            "process_exit": process.returncode,
            "wall_seconds": elapsed,
            "log_sha256": hashlib.sha256(log_path.read_bytes()).hexdigest(),
        }
        if child_output.exists():
            result = json.loads(child_output.read_text())
            if name == "interrupted":
                item["checks"] = [
                    {
                        "check": "deliberate in-flight crash preserves external observation trace",
                        "passed": process.returncode == 23
                        and bool(result["snapshot"]["positions"]),
                    }
                ]
                item["status"] = "passed" if all(c["passed"] for c in item["checks"]) else "failed"
                item["snapshot"] = result["snapshot"]
                item["resources"] = result["resources"]
                item["limitation"] = (
                    "No native durable checkpoint restored; "
                    "later full replay is recovery by reconstruction only"
                )
            else:
                item["checks"] = check_case(result)
                item["status"] = (
                    "passed"
                    if process.returncode == 0 and all(c["passed"] for c in item["checks"])
                    else "failed"
                )
                item["resources"] = result["resources"]
                item["engine_run_seconds"] = result["engine_run_seconds"]
                item["state"] = result["state"]
                item["oracle"] = result["oracle"]
                item["order_event_types"] = [e["type"] for e in result["events"]]
                item["denial_reasons"] = [e["reason"] for e in result["events"] if "reason" in e]
                item["fill_events"] = [e for e in result["events"] if e["type"] == "OrderFilled"]
                item["semantic_digest"] = digest(
                    {
                        k: result[k]
                        for k in ("events", "state", "oracle", "tick_trace", "tick_count")
                    }
                )
            item["result_sha256"] = hashlib.sha256(child_output.read_bytes()).hexdigest()
        else:
            item["status"] = "failed"
            item["error"] = log_path.read_text()[-2000:]
        outcomes.append(item)
    initial, replay = outcomes[0], outcomes[-1]
    replay_equal = (
        initial.get("semantic_digest") == replay.get("semantic_digest")
        and "semantic_digest" in initial
    )
    summary = {
        "schema_version": 1,
        "package": "B",
        "technical_only": True,
        "engine": "nautilus-trader",
        "version": "1.231.0",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "libc": platform.libc_ver(),
        },
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "installed_distributions": metadata,
        "distribution_hash_scope": (
            "SHA256 of installed RECORD metadata, not archive/wheel hash "
            "or independent supply-chain attestation"
        ),
        "cases": outcomes,
        "fresh_process_replay": {
            "passed": replay_equal,
            "scope": "identical fixture in fresh process; not checkpoint or venue recovery",
        },
        "suite_wall_seconds": time.perf_counter() - start,
        "financial_experiments": 0,
        "market_data_rows": 0,
        "limitations": [
            "Synthetic constants do not calibrate fees, latency, spread, queues or real liquidity.",
            "In-flight checkpoint recovery and external reconciliation are not demonstrated.",
            "Network faults, rate limits, venue rules and authentication are not exercised.",
            "Spot synthetic pair only; no derivatives, margin, funding or real FX conversion.",
            "No production integration, synthetic v1 contract widening or Windows execution.",
            "10000 ticks without orders is a smoke test, not full 26-slot workload sizing.",
        ],
    }
    summary["all_implemented_checks_passed"] = (
        all(o["status"] == "passed" for o in outcomes) and replay_equal
    )
    write_json(output / "results.json", summary)
    print(
        json.dumps(
            {
                "output": str(output),
                "passed": summary["all_implemented_checks_passed"],
                "cases": [{k: o[k] for k in ("case", "status", "process_exit")} for o in outcomes],
            },
            indent=2,
        )
    )
    return 0 if summary["all_implemented_checks_passed"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--case", choices=CASES)
    parser.add_argument("--child-output", type=Path)
    args = parser.parse_args()
    if args.case:
        if not args.child_output:
            parser.error("--case requires --child-output")
        native_case(args.case, args.child_output)
    else:
        if not args.output or not args.output.is_absolute():
            parser.error("--output requires an absolute scratch directory")
        raise SystemExit(manager(args.output))
