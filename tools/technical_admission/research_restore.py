"""Bounded E5 interruption/reconstruction evidence, not live recovery admission.

Run only inside runtime_guard. The unchanged native worker has no resume gate:
comparison and identity-safe journal consolidation are explicitly POST-HOC.
This establishes at most deterministic offline recomputation from the same
persisted invented source, never original E5 or prospective reconciliation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

from engine_fixtures import check_accounting


POINTS = {
    "after-submit-before-ack": 71,
    "after-fill-before-checkpoint": 72,
    "during-cancel": 73,
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def state(value):
    # Record order identities and exact Decimal strings; do not round or remove
    # identities to force determinism. Fields unrelated to state are excluded.
    return {key: value[key] for key in (
        "fills", "balances", "free", "reserved", "orders", "positions",
    )}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--worker", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source = args.output / "same-source-engine-cases.json"
    shutil.copyfile(args.bundle, source)
    shutil.copyfile(Path(__file__), args.output / "research_restore.frozen.py")
    fixtures = {f["case_id"]: f for f in json.loads(source.read_text())["functional"]}
    write_new(args.output / "protocol-before-execution.json", {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(source), "worker_sha256": sha(args.worker),
        "supervisor_sha256": sha(Path(__file__)),
        "oracle_sha256": sha(Path(__file__).with_name("engine_fixtures.py")),
        "case_attempts": 4, "maximum_native_processes": 7,
        "cut_exit_codes": POINTS,
        "initial_conditions": "Frozen fixture unchanged; consumption=true, L1, standard pinned runtime",
        "acceptance_component": [
            "Reference completes with no callback or independent accounting error.",
            "Each cut exits at its expected code, without completed checkpoint.",
            "Original durable files retain their hashes after reconstruction.",
            "Reconstruction uses the exact same persisted source bytes and fixture run_id.",
            "Persisted command/event/fill streams equal prefixes of reconstruction streams.",
            "Exact final native financial state equals the uninterrupted reference.",
            "Identity-based consolidation never doubles an existing fill and never merges unequal identities.",
        ],
        "full_original_E5_admission": False,
        "limitations": [
            "Reconstruction starts a fresh isolated simulator using the same durable source, not a native checkpoint.",
            "The venue-fills file is a native callback journal, not an independent venue authority.",
            "Prefix reconciliation is post-hoc; no before-new-command recovery gate exists in the worker.",
            "Idempotency belongs to the consolidated harness research ledger, not native duplicate-event handling.",
            "No exchange, unknown external fill, broker restart or prospective safe resumption is tested.",
        ],
    })
    invocations = []

    def run(case_id, directory, cut=None):
        directory.mkdir(parents=True, exist_ok=False)
        observations = directory / "observations.json"
        command = [str(args.python), str(args.worker), "--bundle", str(source),
                   "--case", case_id, "--output", str(observations),
                   "--journal", str(directory / "journal")]
        if cut:
            command.extend(["--cut", cut])
        started = time.monotonic()
        timed_out = False
        with (directory / "native.log").open("x") as log:
            try:
                completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                           timeout=60, check=False)
                code = completed.returncode
            except subprocess.TimeoutExpired:
                code, timed_out = None, True
        receipt = {"case_id": case_id, "cut": cut, "command": command,
                   "exit_code": code, "timed_out": timed_out,
                   "wall_seconds": time.monotonic()-started}
        invocations.append(receipt)
        write_new(directory / "invocation.json", receipt)
        return code, json.loads(observations.read_text()) if observations.exists() else None

    reference_code, reference = run("E5-reference", args.output / "reference")
    reference_problems = []
    if reference_code != 0 or reference is None:
        reference_problems.append("reference_did_not_complete")
    else:
        reference_problems.extend(check_accounting(fixtures["E5-reference"], reference))
        if reference["callback_errors"]:
            reference_problems.append("reference_callback_error")
    results = []
    if reference_problems:
        results = [{"case_id": "E5-" + point, "status": "not_executed_reference_blocked"} for point in POINTS]
    else:
        for point, expected_code in POINTS.items():
            case_id = "E5-" + point
            root = args.output / point
            code, unexpected_result = run(case_id, root / "interrupted", cut=point)
            journal = root / "interrupted" / "journal"
            hashes = {p.name: sha(p) for p in journal.glob("*.jsonl")}
            problems = []
            if code != expected_code:
                problems.append("cut_exit_code_mismatch")
            if unexpected_result is not None or (journal / "completed.jsonl").exists():
                problems.append("cut_did_not_precede_completed_checkpoint")
            result = {"case_id": case_id, "run_id": fixtures[case_id]["run_id"],
                      "cut_exit_code": code, "original_journal_hashes": hashes,
                      "source_sha256": sha(source), "problems": problems,
                      "full_original_E5_admission": False,
                      "new_command_reconciliation_gate": "absent; post-hoc audit only"}
            # A wrong/missing cut is a stopping condition for this attempt.
            if problems:
                result["status"] = "interruption_failed_no_reconstruction"
                results.append(result)
                write_new(root / "result.json", result)
                continue
            restart_code, reconstructed = run(case_id, root / "reconstructed")
            if restart_code != 0 or reconstructed is None:
                problems.append("reconstruction_did_not_complete")
            else:
                problems.extend(check_accounting(fixtures[case_id], reconstructed))
                if reconstructed["callback_errors"]:
                    problems.append("reconstruction_callback_error")
                if reconstructed["run_id"] != fixtures[case_id]["run_id"]:
                    problems.append("run_id_changed")
                if state(reconstructed) != state(reference):
                    problems.append("native_final_state_differs_from_reference")
                reconstructed_journal = root / "reconstructed" / "journal"
                for name in ("commands.jsonl", "native-events.jsonl", "venue-fills.jsonl"):
                    before, after = rows(journal / name), rows(reconstructed_journal / name)
                    if before != after[:len(before)]:
                        problems.append("persisted_prefix_mismatch:" + name)
                # Consolidate actual rows only after identity/content checks.
                merged, duplicate_rows, conflicts = {}, 0, []
                for row in rows(journal / "venue-fills.jsonl") + reconstructed["fills"]:
                    identity = row["venue"] + ":" + row["fill_id"]
                    if identity in merged:
                        duplicate_rows += 1
                        if merged[identity] != row:
                            conflicts.append(identity)
                    else:
                        merged[identity] = row
                if conflicts:
                    problems.append("same_fill_identity_conflicting_content")
                write_new(root / "consolidated-harness-research-ledger.json", {
                    "origin": "post-hoc harness identity consolidation; no native ledger modification",
                    "fills": list(merged.values()), "duplicate_rows_suppressed": duplicate_rows,
                    "identity_conflicts": conflicts,
                    "native_execution_or_resume_gate": False,
                })
                result["duplicate_rows_suppressed"] = duplicate_rows
                if list(merged.values()) != reconstructed["fills"]:
                    problems.append("consolidated_ledger_differs_from_native_reference_effects")
            if {p.name: sha(p) for p in journal.glob("*.jsonl")} != hashes:
                problems.append("original_durable_journal_changed")
            if sha(source) != sha(args.bundle):
                problems.append("same_source_bytes_changed")
            result["status"] = "posthoc_reconstruction_component_checks_pass" if not problems else "posthoc_reconstruction_component_failed"
            results.append(result)
            write_new(root / "result.json", result)
    summary = {
        "reference_problems": reference_problems, "results": results,
        "native_process_invocations": len(invocations),
        "full_original_E5_admission": False,
        "prospective_recovery_proved": False,
        "interpretation": "Actual cuts and same-source deterministic research recomputation only. Post-hoc comparison cannot demonstrate reconciliation before new commands.",
    }
    write_new(args.output / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
