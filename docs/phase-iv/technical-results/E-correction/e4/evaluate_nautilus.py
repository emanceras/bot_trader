"""Independent post-run checks; never create engine fills or amend fixtures."""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path

from engine_fixtures import check_accounting


def evaluate(fixture, observed):
    problems = check_accounting(fixture, observed)
    if observed["callback_errors"]:
        problems.append("worker_callback_errors")
    arrivals = [t for t in observed["trace"] if t["kind"] == "command_arrival"]
    if [(t["command"], t["at"]) for t in arrivals] != [
        (c, c["available_ns"] + fixture["latency_ns"]) for c in fixture["commands"]
    ]:
        problems.append("command_timeline_differs_from_fixture")
    if any(t["at"] != t["native_clock"] for t in arrivals):
        problems.append("native_clock_command_disagreement")
    for snap in observed["snapshots"]:
        for currency, amount in snap["balances"].items():
            if currency not in snap["free"] or currency not in snap["reserved"]:
                problems.append("missing_free_reserved:" + currency)
            elif Decimal(snap["free"][currency]) + Decimal(snap["reserved"][currency]) != Decimal(amount):
                problems.append("snapshot_free_reserved_equation:" + currency)
            if Decimal(amount) < 0:
                problems.append("negative_native_balance:" + currency)
    total_position = sum((Decimal(p["quantity"]) * (1 if p["side"] == "LONG" else -1 if p["side"] == "SHORT" else 0)
                          for p in observed["positions"]), Decimal(0))
    if total_position != Decimal(observed["balances"]["SYN"]):
        problems.append("native_position_inventory_disagreement")
    quantities = Counter()
    for fill in observed["fills"]:
        quantities[fill["command_id"]] += Decimal(fill["quantity"])
        commands = [c for c in fixture["commands"] if c["command_id"] == fill["command_id"]]
        if not commands or fill["at"] < commands[0]["available_ns"] + fixture["latency_ns"]:
            problems.append("fill_before_arrival")
    orders = {o["id"]: o for o in observed["orders"]}
    for command in fixture["commands"]:
        if command["kind"] == "cancel" or command["command_id"] not in orders:
            continue
        order = orders[command["command_id"]]
        if Decimal(order["filled"]) + Decimal(order["remaining"]) != Decimal(command["quantity"]):
            problems.append("order_quantity_conservation:" + command["command_id"])
    specifics = {}
    if fixture["case_id"] == "E1-causality":
        if observed["decisions"] != fixture["expected_decisions"]:
            problems.append("closed_bar_decision_mismatch")
        specifics["full_R_native_parity"] = "not established; small canary and harness decision rule only"
    if "expected_conversion" in fixture:
        for key, expected in fixture["expected_conversion"].items():
            actual = observed["conversion"][key]
            if (actual is None) != (expected is None) or (expected is not None and Decimal(actual) != Decimal(expected)):
                problems.append("causal_conversion_mismatch:" + key)
        specifics["conversion_origin"] = observed["conversion"]["origin"]
    if fixture["case_id"] == "E3-L2":
        depth = [(f["price"], f["quantity"]) for f in observed["fills"] if f["command_id"] == "depth-market"]
        if [(Decimal(p), Decimal(q)) for p, q in depth] != [(Decimal(100), Decimal(1)), (Decimal(101), Decimal(2)), (Decimal(102), Decimal(1))]:
            problems.append("depth_market_levels_differ")
        for cid in ("resting-partial", "ioc-2", "before-fill"):
            if cid not in orders or orders[cid]["status"] != "CANCELED":
                problems.append("required_terminal_cancel:" + cid)
        if quantities["resting-partial"] != Decimal(1) or quantities["before-fill"] != 0:
            problems.append("partial_or_cancel_before_fill_mismatch")
        # Both commands see the snapshot at offset300; no intervening refresh.
        if quantities["resting-partial"] + quantities["ioc-2"] > Decimal(1):
            problems.append("resting_and_IOC_reuse_same_snapshot_liquidity")
        specifics["IOC_quantity"] = str(quantities["ioc-2"])
        specifics["IOC_arrival_before_next_snapshot"] = True
    if fixture["case_id"] == "E4-idempotency":
        specifics["duplicate_fill_redelivery"] = "not exercised by this worker; native fill-id replay remains unproved"
        specifics["shared_capital_policy"] = "native risk/account behavior; no harness reservation shim"
    if "diagnostic_configuration" in fixture:
        cfg = fixture["diagnostic_configuration"]
        total = sum(quantities.values(), Decimal(0))
        available = Decimal(cfg["initial_visible_ask_quantity"])
        market_callbacks = [t for t in observed["trace"] if t["kind"] in ("native_quote_callback", "native_book_callback")]
        if len(market_callbacks) != 1:
            problems.append("diagnostic_not_exactly_one_market_callback")
        specifics.update({
            "initial_visible_ask_quantity": str(available), "filled_total": str(total),
            "derived_initial_budget_minus_fills": str(available-total),
            "derived_budget_is_native_counter": False,
            "category": "no_native_effect" if total == 0 else "filled_total_at_most_initial_visible" if total <= available else "filled_total_exceeds_initial_visible",
            "no_intervening_market_updates": len(market_callbacks) == 1,
        })
    return {
        "case_id": fixture["case_id"], "problems": sorted(set(problems)),
        "component_checks_pass": not problems,
        "full_E_admission": False,
        "admission_note": "Component checks alone do not certify all original E requirements, native R parity, independent venue recovery or real-market execution.",
        "filled_by_command": {k: str(v) for k, v in quantities.items()},
        "specifics": specifics,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    observed = json.loads(args.observations.read_text())
    bundle = json.loads(args.bundle.read_text())
    fixture = next(f for f in bundle.get("functional", bundle.get("cases")) if f["case_id"] == observed["case_id"])
    result = evaluate(fixture, observed)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2); stream.write("\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
