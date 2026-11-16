"""Offline, data-only QA of one private public-feed capture; never opens a feed.

Only counts, timing aggregates and hashes leave this verifier. Original messages,
market values and normalized sidecars remain in the private platform state.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from bot_trader.application import build_services
from bot_trader.core.contracts import Principal
from bot_trader.core.events import QuoteData, TradeData
from bot_trader.core.settings import Settings
from bot_trader.market_data.capture_authority import PilotApproval, PilotConfiguration
from bot_trader.market_data.kraken_ws import (
    WSCaptureNormalization,
    exact_ws_json,
    rfc3339_ns,
)
from bot_trader.market_data.replay import CaptureReplayResult, MarketReplay

REPO = Path(__file__).resolve().parents[2]
ADMIN = Principal(id="pilot-offline-verifier", role="admin")


def timing(values):
    ordered = sorted(values)
    if not ordered:
        return {"count": 0, "min_ns": None, "median_observation_ns": None, "max_ns": None}
    return {
        "count": len(ordered),
        "min_ns": ordered[0],
        "median_observation_ns": ordered[(len(ordered) - 1) // 2],
        "max_ns": ordered[-1],
    }


def verify(args, report):
    config = PilotConfiguration.model_validate_json(args.config.read_bytes())
    report.update(capture_id=args.capture_id, config_hash=config.digest)
    report["stage"] = "fresh_process_inspection"
    command = [
        sys.executable, "-m", "bot_trader.cli", "--state-dir", str(args.state_dir.resolve()),
        "capture-pilot", "--capture-id", args.capture_id, "--config",
        str(args.config.resolve()), "--inspect",
    ]
    process = subprocess.run(command, cwd=REPO, capture_output=True, timeout=90, check=False)
    report["fresh_process"] = {
        "exit_code": process.returncode,
        "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
    }
    if process.returncode:
        report.update(status="blocked", reason="fresh_process_inspection_failed", passed=False)
        return
    first = json.loads(process.stdout)
    settings = Settings(
        data_dir=args.state_dir.resolve(), repository_root=REPO, max_artifact_bytes=33_554_432
    )
    services = build_services(settings)
    try:
        report["stage"] = "reconstructed_service_inspection"
        second = services.capture.inspect(args.capture_id, config, ADMIN)
        checks = report["checks"] = {}
        identity_keys = (
            "archive_hash", "normalization_hash", "replay_hash", "journal_checkpoint",
            "checkpoint", "market_events", "channels_seen", "config_hash",
        )
        checks["fresh_process_artifacts_and_checkpoints_identical"] = all(
            first[key] == second[key] for key in identity_keys
        )
        original_bytes = args.capture_report.read_bytes()
        candidates = [line for line in original_bytes.splitlines() if line.startswith(b"{")]
        if len(candidates) != 1:
            raise ValueError("Exactly one original structured capture report is required.")
        original = json.loads(candidates[0])
        report["original_command_report_sha256"] = hashlib.sha256(original_bytes).hexdigest()
        checks["original_capture_artifacts_preserved_after_restart"] = all(
            original[key] == second[key] for key in identity_keys
        )
        checks["original_pilot_accepted"] = original.get("pilot_acceptance", {}).get("passed") is True
        report["artifact_hashes"] = {key: second[key] for key in identity_keys[:3]}
        report["stage"] = "journal_and_provenance"
        journal = services.capture.journal(args.capture_id, config, ADMIN)
        with journal.capture_lease():
            checkpoint = journal.audit()
            records = journal.records()
            frames = journal.frames()
            checks["journal_integrity_no_pending_intent"] = not checkpoint.pending_intent
            checks["journal_checkpoint_unchanged"] = (
                checkpoint.model_dump(mode="json") == second["journal_checkpoint"]
            )
            normalized = WSCaptureNormalization.model_validate_json(
                services.capture.store.get(second["normalization_hash"], "json")
            )
            saved = CaptureReplayResult.model_validate_json(
                services.capture.store.get(second["replay_hash"], "json")
            )
            approvals = [r for r in records if r.kind == "capture_authorization"]
            for record in approvals:
                approval = PilotApproval.model_validate_json(
                    services.capture.store.get(record.details["approval_hash"], "json")
                )
                # Historical binding at intake; no fresh connection or renewed authority.
                approval.require(args.capture_id, config, record.received_ns, approval.host_id)
            checks["recorded_approval_binding_at_intake"] = bool(approvals)
            checks["utc_receipt_order"] = all(
                a.received_ns <= b.received_ns for a, b in zip(records, records[1:])
            )
            session_clocks = {}
            monotonic_ok = True
            for record in records:
                monotonic_ok &= record.monotonic_ns >= session_clocks.get(record.session_id, 0)
                session_clocks[record.session_id] = record.monotonic_ns
            checks["per_session_monotonic_order"] = monotonic_ok
            events = {event.event_id: event for event in normalized.events}
            sidecars = {(row.frame_sequence, row.item_index): row for row in normalized.rows}
            exact = causal = units = provenance = duplicate_semantics = True
            ages = defaultdict(list)
            coverage = defaultdict(list)
            messages = Counter()
            deliveries = Counter()
            native_seen = {}
            raw_rows = duplicate_count = 0
            for frame in frames:
                value = exact_ws_json(journal.read_frame(frame))
                channel = value.get("channel", "method")
                messages[channel] += 1
                if channel not in ("trade", "ticker"):
                    continue
                for index, raw in enumerate(value["data"]):
                    raw_rows += 1
                    row = sidecars[(frame.local_sequence, index)]
                    event = events[row.event_id]
                    event_ns = rfc3339_ns(raw["timestamp"])
                    exact &= (
                        row.timestamp_text == raw["timestamp"]
                        and event_ns == event.event_ns == event.original_tick
                        and event.original_unit == "ns"
                    )
                    causal &= (
                        event_ns <= event.received_ns == event.available_ns
                        and event.effective_ns == event.received_ns <= frame.received_ns
                    )
                    units &= raw["symbol"] == row.original_symbol == "BTC/EUR"
                    units &= event.instrument == "BTC-EUR" and event.quote_currency == "EUR"
                    provenance &= (
                        row.raw_sha256 == frame.raw_sha256
                        and row.received_ns == frame.received_ns
                        and row.monotonic_ns == frame.monotonic_ns
                        and row.session_id == frame.session_id
                    )
                    if not row.duplicate_delivery:
                        provenance &= (
                            event.raw_sha256 == frame.raw_sha256
                            and event.received_ns == frame.received_ns
                        )
                    if channel == "trade":
                        trade_id = str(raw["trade_id"])
                        duplicate = trade_id in native_seen
                        duplicate_semantics &= row.duplicate_delivery == duplicate
                        duplicate_semantics &= row.native_trade_id == trade_id
                        signature = (
                            event_ns, raw["symbol"], raw["side"], raw["ord_type"],
                            Decimal(str(raw["price"])), Decimal(str(raw["qty"])),
                        )
                        if duplicate:
                            duplicate_semantics &= native_seen[trade_id] == signature
                        else:
                            native_seen[trade_id] = signature
                        duplicate_semantics &= isinstance(event.data, TradeData)
                        if isinstance(event.data, TradeData):
                            duplicate_semantics &= (
                                Decimal(event.data.price) == signature[-2]
                                and Decimal(event.data.quantity) == signature[-1]
                            )
                        duplicate_count += duplicate
                    else:
                        duplicate_semantics &= not row.duplicate_delivery
                        duplicate_semantics &= isinstance(event.data, QuoteData)
                        if isinstance(event.data, QuoteData):
                            duplicate_semantics &= event.data.origin == "observed"
                            for name, levels in (
                                ("bid", event.data.bids), ("ask", event.data.asks)
                            ):
                                duplicate_semantics &= (
                                    Decimal(levels[0].price) == Decimal(str(raw[name]))
                                    and Decimal(levels[0].quantity)
                                    == Decimal(str(raw[name + "_qty"]))
                                )
                    kind = "snapshot" if row.snapshot else "update"
                    provenance &= row.snapshot == (value["type"] == "snapshot")
                    ages[channel + ":" + kind].append(frame.received_ns - event_ns)
                    coverage[channel].append(frame.received_ns)
                    deliveries[channel] += 1
            checks.update(
                exact_original_timestamps=exact,
                receipt_availability_causality=causal,
                native_instrument_and_currency=units,
                raw_to_sidecar_to_event_provenance=provenance,
                duplicate_and_observed_quote_semantics=duplicate_semantics,
                row_accounting=(raw_rows == len(normalized.rows)
                                == len(normalized.events) + duplicate_count),
            )
        report["stage"] = "causal_replay"
        replay = MarketReplay()
        full = replay.inspect_capture(normalized.events, data_class="exposed_structural_only")
        checks["stored_replay_matches_recomputation"] = full == saved
        checks["replay_repeat_deterministic"] = full == replay.inspect_capture(
            normalized.events, data_class="exposed_structural_only"
        )
        checks["nonempty_both_channels"] = set(coverage) == {"trade", "ticker"}
        causal_cutoffs = []
        for cutoff in sorted({e.effective_ns for e in full.events}):
            # Three representative boundaries are enough; avoid O(N²) verification.
            causal_cutoffs.append(cutoff)
        selected = (
            sorted({
                causal_cutoffs[0], causal_cutoffs[len(causal_cutoffs) // 2], causal_cutoffs[-1]
            })
            if causal_cutoffs else []
        )
        cutoff_checks = []
        for cutoff in selected:
            before = replay.inspect_capture(
                normalized.events, data_class="exposed_structural_only", until_ns=cutoff - 1
            )
            at = replay.inspect_capture(
                normalized.events, data_class="exposed_structural_only", until_ns=cutoff
            )
            resumed = replay.inspect_capture(
                normalized.events, data_class="exposed_structural_only", checkpoint=at.checkpoint
            )
            cutoff_checks.append(
                all(e.effective_ns < cutoff for e in before.events)
                and at.events == tuple(e for e in full.events if e.effective_ns <= cutoff)
                and len(at.events) > len(before.events)
                and resumed.events == full.events and resumed.checkpoint == full.checkpoint
            )
        checks["causal_boundaries_and_checkpoint_resume"] = bool(selected) and all(cutoff_checks)
        controls = Counter(record.kind for record in records if record.kind != "frame")
        terminal = records[-1] if records else None
        stop = (
            terminal.details.get("reason")
            if terminal and terminal.kind == "capture_stop" else None
        )
        checks["target_duration_stop"] = stop == "duration_limit"
        closes = [r.details.get("outcome") for r in records if r.kind == "transport_close"]
        checks["local_shutdown_recorded"] = bool(closes) and all(
            outcome in ("graceful", "local_closed_remote_unknown") for outcome in closes
        )
        report.update(
            status="passed" if all(checks.values()) else "incomplete_or_failed",
            passed=all(checks.values()), stage="complete",
            record_counts=dict(controls), message_counts=dict(messages),
            market_delivery_counts=dict(deliveries), unique_market_events=len(full.events),
            duplicate_trade_deliveries=duplicate_count,
            causal_boundaries_checked=len(selected), stop_reason=stop,
            journal_checkpoint=checkpoint.model_dump(mode="json"),
            replay_checkpoint=full.checkpoint.model_dump(mode="json"),
            application_source_age_ns={key: timing(values) for key, values in sorted(ages.items())},
            channel_coverage={key: {
                "first_received_ns": min(values), "last_received_ns": max(values),
                "receipt_span_ns": max(values) - min(values),
            } for key, values in sorted(coverage.items())},
            coverage_gaps_recorded=controls["coverage_gap"],
            recovery_records_observed=controls["interruption"],
            corruption_observed=False,
            fault_coverage=(
                "No faults injected into original capture. Unobserved disconnects, corruption "
                "and interrupted-write recovery require the separately executed synthetic tests."
            ),
            timing_limitations=(
                "Source-to-application receipt age, not measured network latency; host clock "
                "synchronization and upstream completeness are not proved by this verifier."
            ),
        )
    finally:
        services.database.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--capture-id", required=True)
    parser.add_argument("--capture-report", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "schema_version": 1, "purpose": "private_public_capture_technical_qa",
        "network_contacted": False, "financial_validation": False,
        "status": "blocked", "passed": False, "stage": "configuration",
    }
    try:
        verify(args, report)
    except Exception as error:
        # Never publish exception text or captured provider payloads.
        report.update(status="blocked", passed=False, error_type=type(error).__name__)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as output:
            output.write(encoded)
    print(encoded, end="")
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
