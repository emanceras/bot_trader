# D-052 E1/bar execution — preserved results

[Canonical report](../../../en/phase-iv/bar-execution.md) / [Informe español](../../../es/phase-iv/bar-execution.md). Executed 2026-11-03 UTC, starting from `c1d4029`; [summary](summary.json). Prior E, E-recovery and E-correction evidence is unchanged.

## What actually ran

| Group | Native child contexts | Component checks | Outcome |
|---|---:|---:|---|
| `native-zero` | 2 | 12 | Both adaptive settings fill1@100.50 at N close; adverse for project contract |
| `timestamps` | 4 | 48 | Incorrect init delivers full bar early; corrected and close labels deliver at close;123 ns preserved; selected helper checks pass |
| `native-latency` | 2 | 12 | Both settings fill1@112.00 at next bar close, not open |
| `causal` | 1 | 9 | Native fill1@110.05 after eligible synthetic quote |
| `invariance` | 4 | 40 | Four previous trace prefixes unchanged; later revision actually received |
| `late-decision` | 2 | 14 | Early opening skipped; later quote fills111.05; absent later quote means no fill |

All135 **component** checks pass, including expected reproduction of invalid timestamp configuration. This does not admit the native same-close path, all engine cases, a financial strategy or the production bridge. All15 native processes are disclosed; the six outer invocations group related controls as authorized. There was one preparation and no harness repair. No remaining slot needs to be used.

## Evidence map

- `frozen/`: all initial sources, exact `cases.json`, pre-execution source/bundle hashes, selected original R records and source hash. Bundle SHA256 `f5ed1089095f42830ce8e582a58e37419be1e7a9c7ef7523b9dec485606d0c37`. Nothing was edited after execution to change an expectation.
- Each group/case directory: `invocation.json`, raw `native.log`, `observations.json`. Includes exact bar/quote input configuration, native callback ordering, exposed book snapshots, decision/submission times, nominal latency-derived arrival separately from observed acceptance/fill, actual fees and balances.
- Each group `summary.json`: original checker output, counts, digests and preserved native adverse observations. Accounting is an independent Decimal check for these BUY/USD fixtures, not a certified general ledger.
- `budget-baseline.json`, `attempts.jsonl`, `runs.jsonl`, `logs/`: original guard records. Preparations are explicitly identified; all native workers are sequential under the guarded group.
- `api-source-manifest.json`: hashes of installed rc7 type stubs read for API signatures. The prior recovery preserves wheel/runtime provenance; no new download or broad framework review occurred.
- `sources/`: unchanged resource guard and final audit scripts. `publication-manifest.json` hashes exact copies of scratch/source artifacts. Generated summaries are separate from source copies.
- `preservation.json`:73 runtime/config and4,630 regular production-environment files unchanged; no additions/protected scientific changes. Its limitations on symlinks/runtime state are preserved.
- `resources.json`: cumulative historical M/R/E resource snapshot. `summary.json` isolates this delivery:9.712751 guarded seconds,6.404959 CPU seconds,82,489,344 bytes sampled peakRSS,556,529 additional E scratch bytes at audit. Publication copies are separate; neither scratch measurement nor sampledRSS is a continuous peak guarantee. Zero new downloads; software ledger hash unchanged.
- `verification.json`: publication/source/JSON/link checks, not another engine invocation or financial test.

## Reproduction and continuation

Exact commands and timestamps are in `runs.jsonl`; native child commands are in each case's `invocation.json`. They use standard CPython3.13.16 and NautilusTrader2.0.0rc7 from the existing isolated environment. The rc7 wheel SHA256 remains `b3928f37d75d57508030a421dc762186ad1f9ffc5d5420d7daf1d2c6badb8044` (72,042,580 bytes); no dependency update follows from these results.

For a separately authorized independent reproduction, preserve `frozen/` and its fixture hash, point the recorded isolated Python path to the identical runtime, and use a **new** output root. The frozen suite accepts `--root`; worker and case bundle paths are explicit. Run groups in the recorded priority order: native-zero, timestamps, native-latency, causal, invariance, late-decision. Invariance reads the earlier causal result. Do not regenerate the fixture from a changed generator or overwrite the original output. The historical generator's preparation step expects `/tmp/bar-r-selection.json`; the exact selected records are preserved as `frozen/R-selection.json`, so the published frozen bundle can be used directly without regenerating it. Absolute paths in original receipts are historical provenance, not portable installation instructions.

This is not a Windows verification. The Linux resource guard uses `/proc`, affinity and seccomp. Resumption should inspect these completed artifacts, not rerun M/R/LEAN or use unused slots to obtain another favorable native behavior. No full adapter, additional fill model, remaining-market cancel manager, financial data access, production migration or Phase V permission is created by this delivery. Economic E3/E4 and the26 scientific specifications remain unchanged.
