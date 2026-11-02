"""Frozen invented E inputs and independent accounting checks.

This module does not simulate fills. Engine workers must report their actual
observations; expected data are used only by the supervisor for comparison.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

SCHEMA = "bot-trader.synthetic-engine-probe.v1"
ORIGIN_NS = 1_700_000_000_000_000_000
OFFSET_UNIT_NS = 100  # Common representable granularity for native engine cases.


def time_ns(offset: int) -> int:
    return ORIGIN_NS + offset * OFFSET_UNIT_NS


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def event(offset: int, kind: str, **fields: object) -> dict:
    return {
        "event_id": f"source-{offset}-{kind}",
        "event_ns": time_ns(offset),
        "available_ns": time_ns(offset),
        "receive_ordinal": offset,
        "kind": kind,
        **fields,
    }


def command(offset: int, command_id: str, kind: str, **fields: object) -> dict:
    return {
        "command_id": command_id,
        "available_ns": time_ns(offset),
        "strategy_id": "strategy-A",
        "instrument_id": "SYN-USD.SIM",
        "kind": kind,
        **fields,
    }


def quote(offset: int, bid: str, ask: str, bid_size="10.00", ask_size="10.00"):
    return event(offset, "quote", bid=bid, ask=ask, bid_size=bid_size, ask_size=ask_size)


def base(case_id: str, events: list, commands: list) -> dict:
    assert len(events) <= 256 and len(commands) <= 32
    return {
        "schema": SCHEMA,
        "synthetic": True,
        "case_id": case_id,
        "run_id": f"fixed-{case_id}",
        "initial_cash": {"USD": "1000.00", "USDT": "40.00", "SYN": "0.00"},
        "instrument": {
            "id": "SYN-USD.SIM", "base": "SYN", "quote": "USD",
            "price_tick": "0.01", "quantity_step": "0.01",
            "minimum_notional": "10.00", "maker_fee": "0.001", "taker_fee": "0.002",
        },
        "strategy_ids": ["strategy-A", "strategy-B"],
        "account_id": "shared-synthetic-account",
        "latency_ns": 10 * OFFSET_UNIT_NS,
        "time_unit": "nanoseconds",
        "accounting": {"USD_quantum": "0.01", "fee_rounding": "ROUND_HALF_EVEN"},
        "events": events,
        "commands": commands,
    }


def functional_cases() -> list[dict]:
    """One immutable nine-case plan; all prices and schedules are invented."""
    e1 = base("E1-causality", [
        event(100, "bar_open", bar_id="b0", close="100.00"),
        event(200, "bar_close", bar_id="b0", close="101.00"),
        event(300, "bar_revision", bar_id="b0", revision_of="source-200-bar_close", close="99.00"),
        {**event(400, "external"), "event_ns": time_ns(100), "available_ns": time_ns(500)},
    ], [])
    e1["decision_rule"] = "OBSERVE only the latest received closed-bar version; otherwise BLOCK"
    e1["expected_decisions"] = [
        {"at": time_ns(100), "decision": "BLOCK", "bar_id": None},
        {"at": time_ns(200), "decision": "OBSERVE", "bar_id": "b0", "close": "101.00"},
        {"at": time_ns(300), "decision": "OBSERVE", "bar_id": "b0", "close": "99.00"},
    ]
    e2 = base("E2-accounting", [
        quote(100, "99.00", "100.00"), quote(300, "100.00", "101.00"),
        quote(500, "102.00", "103.00"),
        event(700, "conversion", instrument_id="USDT-USD.SIM", rate="0.99"),
        quote(900, "102.00", "103.00"),
    ], [
        command(110, "buy-2", "market", side="BUY", quantity="2.00", tif="GTC"),
        command(310, "sell-1", "limit", side="SELL", quantity="1.00", price="102.00", post_only=True, tif="GTC"),
        command(510, "bad-step", "market", side="BUY", quantity="0.001", tif="GTC"),
        command(520, "below-minimum", "market", side="BUY", quantity="0.01", tif="GTC"),
        command(530, "insufficient", "market", side="BUY", quantity="20.00", tif="GTC"),
    ])
    e2["expected_rejected_ids"] = ["bad-step", "below-minimum", "insufficient"]
    e2["expected_conversion"] = {"before": None, "after": "39.6000"}
    e2["required_fill_totals"] = {"buy-2": "2.00", "sell-1": "1.00"}
    e2["required_liquidity_roles"] = {"buy-2": "taker", "sell-1": "maker"}
    l1 = base("E3-L1", [quote(100, "99.00", "100.00", "1.00", "1.00"), quote(300, "99.00", "100.00", "0.00", "0.00")], [
        command(110, "l1-market-4", "market", side="BUY", quantity="4.00", tif="GTC")])
    l1["visible_buy_quantity_limit"] = "1.00"
    l2 = base("E3-L2", [
        event(100, "book_snapshot", bids=[["99.00", "5.00"]], asks=[["100.00", "1.00"], ["101.00", "2.00"], ["102.00", "1.00"]]),
        event(300, "book_snapshot", bids=[["98.00", "5.00"]], asks=[["99.00", "1.00"]]),
        event(500, "book_snapshot", bids=[["98.00", "5.00"]], asks=[["99.00", "1.00"]]),
        event(700, "book_snapshot", bids=[["98.00", "5.00"]], asks=[["99.00", "1.00"]]),
    ], [
        command(110, "depth-market", "market", side="BUY", quantity="4.00", tif="GTC"),
        command(210, "resting-partial", "limit", side="BUY", quantity="3.00", price="99.00", tif="GTC"),
        command(350, "cancel-partial", "cancel", target="resting-partial"),
        command(410, "ioc-2", "limit", side="BUY", quantity="2.00", price="99.00", tif="IOC"),
        command(550, "before-fill", "limit", side="BUY", quantity="1.00", price="98.00", tif="GTC"),
        command(560, "cancel-before", "cancel", target="before-fill"),
    ])
    e4 = base("E4-idempotency", [
        event(100, "book_snapshot", bids=[["99.00", "5.00"]], asks=[["100.00", "3.00"]]),
        event(300, "book_snapshot", bids=[["99.00", "5.00"]], asks=[["100.00", "3.00"]]),
    ], [
        command(110, "shared-first", "limit", side="BUY", quantity="6.00", price="100.00", tif="GTC"),
        command(110, "shared-first", "limit", side="BUY", quantity="6.00", price="100.00", tif="GTC"),
        command(120, "shared-second", "limit", side="BUY", quantity="6.00", price="100.00", tif="GTC", strategy_id="strategy-B"),
    ])
    e4["duplicate_fill_injection"] = "redeliver actual first fill identity; do not synthesize a fill"
    e4["required_distinct_equal_fills"] = {"command_id": "shared-first", "quantity": "3.00", "price": "100.00", "count": 2}
    e4["required_fill_totals"] = {"shared-first": "6.00", "shared-second": "0.00"}
    e4["expected_rejected_ids"] = ["shared-second"]
    recovery = base("E5-reference", [quote(100, "99.00", "100.00"), quote(300, "100.00", "101.00"), quote(600, "102.00", "103.00")], [
        command(110, "recovery-buy", "market", side="BUY", quantity="2.00", tif="GTC"),
        command(310, "recovery-resting", "limit", side="BUY", quantity="1.00", price="50.00", tif="GTC"),
        command(410, "recovery-cancel", "cancel", target="recovery-resting"),
    ])
    cases = [e1, e2, l1, l2, e4, recovery]
    for point in ("after-submit-before-ack", "after-fill-before-checkpoint", "during-cancel"):
        value = json.loads(json.dumps(recovery))
        value["case_id"] = f"E5-{point}"
        value["run_id"] = "fixed-E5-interrupted-state"
        value["cut_point"] = point
        value["reference_case"] = "E5-reference"
        cases.append(value)
    assert len(cases) == 9
    return cases


def resource_case() -> dict:
    """One fixed E6 workload; repeated cold/warm, never optimized."""
    result = base("E6-fixed-workload", [], [])
    instruments = [result["instrument"], {
        **result["instrument"], "id": "SYN2-USD.SIM", "base": "SYN2"}]
    result["instruments"] = instruments
    result["initial_cash"]["SYN2"] = "0.00"
    result["events"] = [
        {**quote(100 * (i + 1), "99.00", "100.00"),
         "instrument_id": instruments[(i // 100) // 2 % 2]["id"]}
        for i in range(10_000)
    ]
    result["commands"] = [
        command(100 * (100 * i + 1) + 10, f"resource-{i}", "market",
                side="BUY" if i % 2 == 0 else "SELL", quantity="0.11", tif="GTC",
                instrument_id=instruments[(i // 2) % 2]["id"],
                strategy_id="strategy-A" if i % 4 < 2 else "strategy-B")
        for i in range(100)
    ]
    result["required_fill_totals"] = {c["command_id"]: c["quantity"] for c in result["commands"]}
    return result


def check_accounting(fixture: dict, observations: dict) -> list[str]:
    """Independent Decimal conservation equations over actual reported fills.

    Never use this function to create fills or restore engine balances.
    """
    problems = []
    cash = {k: Decimal(v) for k, v in fixture["initial_cash"].items()}
    seen = set()
    requested = {c["command_id"]: Decimal(c["quantity"]) for c in fixture["commands"] if "quantity" in c}
    filled = {key: Decimal(0) for key in requested}
    for fill in observations.get("fills", []):
        identity = (fill["venue"], fill["fill_id"])
        if identity in seen:
            problems.append(f"duplicate_effect:{identity}")
            continue
        seen.add(identity)
        qty, px, fee = (Decimal(fill[k]) for k in ("quantity", "price", "fee"))
        if qty <= 0 or px <= 0:
            problems.append("nonpositive_fill")
        if fill["fee_currency"] != "USD":
            problems.append("unsupported_fee_currency")
            continue
        expected_fee = (qty * px * Decimal(fixture["instrument"][f'{fill["liquidity_role"]}_fee'])).quantize(
            Decimal(fixture["accounting"]["USD_quantum"]), rounding=ROUND_HALF_EVEN
        )
        if fee != expected_fee:
            problems.append(f"fee_equation:{fill['fill_id']}")
        direction = Decimal(1) if fill["side"] == "BUY" else Decimal(-1)
        instrument_map = {i["id"]: i for i in fixture.get("instruments", [fixture["instrument"]])}
        instrument = instrument_map.get(fill.get("instrument_id", fixture["instrument"]["id"]))
        if instrument is None:
            problems.append("unsupported_instrument")
            continue
        cash[instrument["base"]] += direction * qty
        cash["USD"] -= direction * qty * px + fee
        cid = fill["command_id"]
        if cid not in requested:
            problems.append(f"unknown_command:{cid}")
        else:
            filled[cid] += qty
    for cid, qty in filled.items():
        if qty > requested[cid]:
            problems.append(f"overfilled_order:{cid}")
    for cid, quantity in fixture.get("required_fill_totals", {}).items():
        if filled.get(cid) != Decimal(quantity):
            problems.append(f"required_fill_quantity:{cid}")
    for cid, role in fixture.get("required_liquidity_roles", {}).items():
        actual = [f for f in observations.get("fills", []) if f["command_id"] == cid]
        if not actual or any(f["liquidity_role"] != role for f in actual):
            problems.append(f"required_liquidity_role:{cid}")
    rejected = set(observations.get("rejected_command_ids", []))
    for cid in fixture.get("expected_rejected_ids", []):
        if cid not in rejected:
            problems.append(f"required_rejection:{cid}")
    if fixture.get("required_distinct_equal_fills"):
        required = fixture["required_distinct_equal_fills"]
        equal = [f for f in observations.get("fills", [])
                 if f["command_id"] == required["command_id"]
                 and Decimal(f["quantity"]) == Decimal(required["quantity"])
                 and Decimal(f["price"]) == Decimal(required["price"])]
        if len(equal) != required["count"] or len({f["fill_id"] for f in equal}) != required["count"]:
            problems.append("distinct_equal_fills_not_preserved")
    balances = observations.get("balances", {})
    for currency, expected in cash.items():
        if currency not in balances or Decimal(balances[currency]) != expected:
            problems.append(f"balance_equation:{currency}")
    if any(value < 0 for value in cash.values()):
        problems.append("negative_cash_or_inventory")
    for currency in balances:
        if currency in observations.get("free", {}) and currency in observations.get("reserved", {}):
            if Decimal(observations["free"][currency]) + Decimal(observations["reserved"][currency]) != Decimal(balances[currency]):
                problems.append(f"free_reserved_equation:{currency}")
    if fixture["case_id"] == "E3-L1" and sum(filled.values()) > Decimal(fixture["visible_buy_quantity_limit"]):
        problems.append("fill_exceeds_visible_L1_quantity")
    return problems


def freeze(output: Path, temporal_path: Path) -> None:
    """Freeze preparation inputs before engine execution; refuse replacement."""
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / "fixture-manifest.json"
    if manifest.exists():
        raise FileExistsError("Frozen fixture manifest already exists; do not replace it")
    json.loads(temporal_path.read_text())
    temporal_bytes = temporal_path.read_bytes()
    bundle = {"schema": SCHEMA, "synthetic": True, "functional": functional_cases(),
              "resource": resource_case(),
              "temporal_fixture_sha256": hashlib.sha256(temporal_bytes).hexdigest(),
              "temporal_fixture_path": str(temporal_path)}
    # Store the exact shared source rather than invent another equivalent journal.
    (output / "temporal_journals.json").write_bytes(temporal_bytes)
    encoded = canonical(bundle)
    (output / "engine-cases.json").write_bytes(encoded + b"\n")
    manifest.write_text(json.dumps({
        "scope_commit": "fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f",
        "fixture_schema": SCHEMA,
        "functional_cases": 9,
        "resource_attempts_per_engine": 4,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "bundle_sha256": hashlib.sha256(encoded + b"\n").hexdigest(),
        "temporal_sha256": hashlib.sha256(temporal_bytes).hexdigest(),
        "state": "frozen_before_engine_execution",
        "note": "Independent expected outcomes are comparison inputs, never worker fill instructions."
    }, indent=2) + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--temporal", type=Path, required=True)
    args = parser.parse_args()
    freeze(args.freeze, args.temporal)
