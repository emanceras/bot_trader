# R — executed evidence and independent internal review

Reviewed 2026-10-29. This is a review of the preserved outputs and source, **not another execution**. The authority and finite scope are [the user authorization](../../APPROVAL-M-R-E.es.md) and [M/R specification](../../../en/phase-iv/technical-packages/dependencies-temporal.md). Runtime source is [temporal_probe.py](../../../../tools/technical_admission/temporal_probe.py); its frozen input is [temporal_journals.json](../../../../tools/technical_admission/fixtures/temporal_journals.json).

## Actual result

The eight journals executed through five delivery paths, each with its complete input and three prefix cuts: **160 passed, zero failed, zero blocked**. Journal lengths are 6, 8, 11, 9, 9, 9, 10 and 7 events. No repeat of an actual R case was needed. [Summary](initial/summary.json), [all case receipts](initial/runs.jsonl), [frozen manifest](initial/frozen-manifest.json) and forty full-output journals are preserved byte-for-byte from the scratch run. The 160 cases are software checks of one shared implementation, not 160 independent financial observations or independent implementations.

The separate [review receipt](review.json) verifies the executed harness, fixture and timezone hashes, the 160 unique case/path/prefix keys, all stored full journals against the explicit frozen oracle, and every stored prefix digest. All 93 artifact-review checks passed. They are metadata/output verification, not additional R attempts, and do not increase the experimental sample.

The fixture-authoring utility specifies expected state deltas, exact arithmetic and UTC strings independently of the tested transition. It expands these into complete per-event states and does not import or invoke that transition. The five paths intentionally reuse the causal transformation; agreement between paths alone would be inadequate, hence the frozen oracle comparison. This internal review is not an external verification or exhaustive proof.

## Covered mechanics and scope limits

| Journal | Evidence in this bounded prototype | Limit on inference |
|---|---|---|
| R1 | Future effective time with already available announcement; delayed/unknown availability and equal cutoff | No provider timestamp quality or inferred historical reception |
| R2 | Integer submicrosecond ticks, explicit ms/us/ns, scoped identity and duplicates | No universal source-normalization contract; unsupported/malformed variants beyond the fixed fixture were not tested |
| R3 | Provisional versus explicitly closed bars; exact two-bin arithmetic; compatible coarse aggregation, misalignment rejection and a late correction | Trade storage is keyed by raw trade ID inside this single-instrument fixture. It is not safe to infer general multiasset/source aggregation support. Provisional values exist in state; `latest_complete_bar` identifies completed material. No production indicator is implemented |
| R4 | Gap invalidation, rejected unavailable recovery, explicit resnapshot and stale sequence | No real exchange resynchronization or continuous feed |
| R5 | Pinned New York DST fold/gap and explicit invented session boundaries | No exchange holiday/calendar certification; session dates are fixture-supplied |
| R6 | Two named inputs and causal USDT/USD conversion, including missing and stale conversion | A small as-of conversion example, not a generic multiasset join/aggregation engine or a claim that USDT equals USD |
| R7 | Delayed release, warm-up, later correction/backfill, and unchanged emitted prefixes | Revision-parent metadata is retained in the fixture; a general revision lineage validator is not demonstrated |
| R8 | JSON serialization/restoration of the same transformation state, duplicate suppression and maker/taker mapping | In-memory reconstruction versus uninterrupted replay; no process crash, durable journal, engine recovery or provider adapter certification |

The only decisions are `OBSERVE`/`BLOCK`. No financial strategy, order, return, model, provider data, live input or execution fill is evaluated. The recommendation is to retain these cases as a future adapter conformance specification; their pass does not certify historical/direct equivalence for a real provider.

## Preserved setup failures and resources

[Guard receipts](guard-runs.jsonl) retain all five invocations. The two first attempts failed in bootstrap because the host did not provide the required Landlock ABI; neither payload nor any journal case ran. Their historical isolation labels are intentions of that failed guard version, **not evidence of successful write confinement**. [isolation-check.log](isolation-check.log) and [write-confinement.log](write-confinement.log) preserve the failures. The revised guard uses disposable paths and later source/runtime hash audits rather than claiming unavailable kernel write isolation. [network-guard-probe.log](network-guard-probe.log) records actual IPv4/IPv6 socket denial.

The first harness command omitted required `--fixtures` and exited in argument parsing before any case: [initial-160.log](initial-160.log). The complete command then executed once: [initial-160-with-fixtures.log](initial-160-with-fixtures.log). These invocation failures must remain separate from the 160 actual case outcomes.

The successful harness reports 0.049896 seconds wall time, 0.047560 CPU seconds and 15,204,352 bytes of process peak RSS. Its enclosing guarded invocation took 0.214788 seconds and 0.146642 CPU seconds; its 100 ms sampled process-group peak was 13,238,272 bytes. The two memory figures use different observation methods; the sample can miss a short peak and is not a kernel hard-limit guarantee. All five R guard invocations together consumed about 0.654550 wall seconds. Software downloads: zero. The `artifact_bytes` field was measured before writing `summary.json`, so it is not the eventual complete publication size.

The frozen [America_New_York.TZif](initial/America_New_York.TZif) is a 3,552-byte copy of the already installed timezone file; SHA256 is in the manifest. The host package labels it tzdata 2026b. The preserved [Debian copyright notice](TZDATA-COPYRIGHT.txt) identifies IANA and states that the database is public domain. No new timezone package was downloaded; this does not certify the latest upstream release.

## Reproduction boundary

To reproduce only after confirming an applicable authorization and the same finite run budget, use Python 3.12.14 and a **new empty output directory**, the committed fixture, and `--zone-source` pointing to the preserved TZif. Follow the exact successful command in `guard-runs.jsonl`, adjusting only workspace locations. Do not overwrite the initial result, regenerate the frozen fixture, or silently substitute a timezone. The current task intentionally did not rerun R while collecting or reviewing this evidence.
