"""Freeze the explicitly authorized two-order consumption diagnostic.

This complement records observations; it does not change any frozen E case.
Native execution is supplied by the same pinned worker as the recovery cases.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from engine_fixtures import base, command, event, quote


def make_bundle() -> dict:
    cases = []
    for book_type in ("L1_MBP", "L2_MBP"):
        for consume in (False, True):
            name = f"D-{book_type}-consumption-{str(consume).lower()}"
            initial = quote(100, "99.00", "100.00", "1.00", "1.00")
            if book_type == "L2_MBP":
                initial = event(100, "book_snapshot", bids=[["99.00", "1.00"]], asks=[["100.00", "1.00"]])
            fixture = base(name, [initial], [
                command(110, "competing-first", "market", side="BUY", quantity="1.00", tif="GTC"),
                command(120, "competing-second", "market", side="BUY", quantity="1.00", tif="GTC"),
            ])
            fixture["diagnostic_configuration"] = {
                "book_type": book_type,
                "liquidity_consumption": consume,
                "no_market_update_after_initial_event": True,
                "clock_only_drain_after_last_command_allowed": True,
                "initial_visible_ask_quantity": "1.00",
                "initial_visible_ask_price": "100.00",
            }
            cases.append(fixture)
    return {
        "schema": "bot-trader.consumption-diagnostic.v1",
        "authority": "D-048 user supplement; four initial applicable configurations only",
        "synthetic_only": True,
        "admission_effect": "complementary observation; does not replace or amend frozen E acceptance",
        "cases": cases,
        "prospective_checks": [
            "Use exact fixture identity and command times; latency is applied once.",
            "Exactly one initial market/book observation, no intervening or later liquidity refresh.",
            "Two separate persistent command identities; native fill identities must remain distinct.",
            "Each command quantity is1; no fill exceeds its requested quantity.",
            "Retain native fills, prices, fees, order statuses and balances; no expected-fill injection.",
            "Report book quantities before/after each order when exposed; otherwise mark native remaining state unknown.",
            "Derived initial-visible-budget minus fills is an arithmetic diagnostic, not native remaining liquidity.",
            "Compare observed quantities, statuses and native book reports for enabled/disabled settings within each book type.",
        ],
        "predeclared_observation_categories": {
            "filled_total_at_most_initial_visible": "observed executions respect the single visible quantity budget",
            "filled_total_exceeds_initial_visible": "observed executions reuse or exceed the single visible quantity budget",
            "no_native_effect": "no fill observed; determine native rejection/cancellation/availability rather than calling a liquidity pass",
            "configuration_unsupported": "not executed for that route; record native configuration error without a custom model",
        },
        "no_expected_configuration_winner": True,
        "limitations": [
            "One invented level and two orders do not establish general market impact, queue priority or real liquidity.",
            "An engine may retain raw displayed depth while separately tracking consumption; do not conflate the states.",
            "External reported observations are not outcomes of this diagnostic.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    args = parser.parse_args()
    args.freeze.mkdir(parents=True, exist_ok=False)
    data = json.dumps(make_bundle(), indent=2, sort_keys=True).encode() + b"\n"
    (args.freeze / "diagnostic.json").write_bytes(data)
    manifest = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "state": "frozen_before_diagnostic_execution",
        "fixture_sha256": hashlib.sha256(data).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "original_fixture_generator_sha256": hashlib.sha256(Path(__file__).with_name("engine_fixtures.py").read_bytes()).hexdigest(),
        "initial_configurations": 4,
        "original_E_cases_mutated": False,
    }
    (args.freeze / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
