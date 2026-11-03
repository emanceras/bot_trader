# D-050 E3-L2 / E4 correction evidence

[Canonical findings](../../../en/phase-iv/engine-correction.md) / [Español](../../../es/phase-iv/engine-correction.md). Evidence generated 2026-11-02–03 UTC; original results under `../E-recovery` and `../E` remain untouched. [Summary](summary.json) separates component success, original E4 failure and modality-specific pending admission.

## Inventory and exact scope

- `budget-baseline.json`, `attempts.jsonl`, `runs.jsonl`, `logs/`: six test/diagnostic invocations, two preparation commands. Four native worker processes; the other two test invocations exercise the supervisor only. Runtime reuse3.13.16/rc7, no downloads. The additional guard enforces the12/1800s/1GiB envelope inside the existing offline guard; sampled RSS can miss short peaks.
- `l2/`: source frozen before the corrected original E3-L2 and before the two separate six-unit diagnostic outcomes. Prior worker, exact worker diff, full correction diff, transformation hash and fixture hash preserved. Original four-unit E3-L2 doubles as the requested4-versus4 observation, without another run.
- `e4/`: one separately frozen idempotency correction, previous L2 worker and exact/full diffs. E4 was run with `--idempotent`, **without** `--l2-reference`, so its duplicate correction is not confounded with a new reference quote.
- `observations/`, `journals/`: actual native fills/events/account/order/position snapshots; command journal and supervisor request journal for E4. Observation order follows native asynchronous callbacks; an immediate after-submit snapshot can still show INITIALIZED. Do not infer terminal state from a submission return alone.
- `evaluations/boundary-regressions.json`:27/32 checks pass; five expectation-dependent failures remain. An empty frozen accounting-oracle problem list is not universal admission; conversely this original oracle includes required fill totals in addition to arithmetic. Read the report's explanation of misleadingly broad check names.
- `fill-consolidation/`: a separately frozen17/17 supervisor-only probe. Invented equal-value different-ID records are explicitly marked, never injected into Nautilus and never counted as the missing second original E4 fill. Actual native accounting is reconciled separately without rewriting the original E4 oracle.
- `sources/`: additional guard and consolidation source. `publication-manifest.json`: hashes of copied original receipts. `preservation.json`, `resources.json`, `verification.json`: final integrity, resources and publication checks; not extra native cases.

The **original E4 native sequence remains adverse**: total3 rather than required6, one native fill rather than two. Its order/fill/position state is now coherent and the USD300 reservation belongs to a partial limit order. `E4:first_native_order_history_preserved` in the32-check suite also requires FILLED6; its failure is not evidence that the new history was erased. `command:completed_duplicate_preserves_actual_native_result` covers a processed request with a partial order, not a completed order. Both labels/results are retained rather than silently edited.

## Reproduction and resumption

The unchanged original bundle is reconstructed by the preserved `engine_fixtures.py` with absolute temporal path `/workspace/bot_trader/tools/technical_admission/fixtures/temporal_journals.json`; expected SHA256 `5aabcb23eb3d29273b299d3731031db511553da4ded5f24066278bb09a27af83`. Absolute path is part of this historical bundle hash. The original fixture generator was not changed.

Exact guarded commands are in `runs.jsonl`. For authorized independent reproduction, use new output directories, the frozen `l2/nautilus_worker.py` with its `l2_reference.py` for E3-L2/D6, and the frozen `e4/nautilus_worker.py` with `command_boundary.py` for E4. Keep the original bundles, timestamps and flags. `sources/fill_consolidation_probe.py` plus the preserved command boundary performs the supervisor-only probe; it deliberately uses the stated scratch path. Do not overwrite earlier outputs or redirect results into the production application.

No more work is automatically implied by the six unused slots. One correction per blocker has been used. The E4-dependent route stops rather than changing the native fill model or fixture to obtain6. E1/bar execution integration remains a defined small future gate, not a reason to repeat160R or undertake a new framework survey. E6, financial datasets, production changes, Phase V and prospective trading remain outside this delivery.
