# M, R and E — executed technical admission

**Recovery update, 2026-11-02:** D-048/D-049 records actual Nautilus execution with standard Python 3.13.16, adverse/partial cases and the finite consumption diagnostic. Read the [new report](engine-recovery.md). This dated report below remains the original `00131bc` record; M/R and LEAN were not repeated.

Document ID: IV-TECH-RESULT-001 · Version: 1 · Date: 2026-11-01 · English canonical. [Spanish](../../es/phase-iv/technical-results.md).

Authority is the user's [express execution approval](../../phase-iv/APPROVAL-M-R-E.es.md) of the exact scopes at `fa435a4`, recorded in D-046. The proposal documents retain their historical wording; this report records actual execution. No production migration, financial experiment, additional market data, Phase V or prospective trading is implied. E3/E4 remain pending.

## M — compatibility demonstrated for the tested storage boundary

The two disposable exports use application/tests from `fa435a4`, Python **3.12.14**, uv **0.12.23** and DuckDB **1.5.6**. One offline candidate resolution changed **only PyArrow 23.0.1 → 26.0.0** among the 37 lock entries. The candidate wheel's exact size and SHA256 match the approved metadata. Fresh isolated environments reused copied caches; production was not the test working directory.

| Actual check | Result | Interpretation |
|---|---|---|
| Three packs × two writers × two readers | **12/12 passed** | Parquet/IPC values, metadata and DuckDB projections satisfy their declared invariants |
| Digest corruption, reserved partition and real-data label in both environments | **6/6 passed** | Existing access guards reject the prohibited objects |
| Writer SIGKILL before atomic artifact publication, both environments | **2/2 passed** | Partial output is not admitted and the original artifact survives this cut point |
| Existing backend suite, control | **110 passed**, no skips/failures | One invocation |
| Existing backend suite, candidate | **110 passed**, no skips/failures | One invocation |
| Dependency consistency | Both passed | No additional version change |
| Eligible previously stored synthetic artifacts | **Unavailable; zero optional reads** | Local artifact inventory was empty; not a failed read or an historical-file pass |

No custom case correction/rerun was needed. Both backend invocations retain the same Starlette/httpx deprecation warning. [M evidence](../../phase-iv/technical-results/M/) preserves locks, commands, frozen expectations, logs and individual outcomes.

The three fixture packs are the existing 120-row/seed42 synthetic v1 recipe, 32 boundary rows and 32 precision events. The v1 reference comes from the control implementation; it is a compatibility reference, not independent proof that the generator is scientifically correct. Boundary/precision expectations are independently specified.

**Adverse precision observation preserved:** DuckDB's zoned timestamp conversion loses nanoseconds in all four writer/reader combinations. The passing precision case detects that loss and requires the canonical integer-tick route to preserve values; it does not assert that every DuckDB timestamp representation is safe. Keep explicit ticks, units and availability metadata across the future boundary.

These tests support Arrow 26 as a **technically viable migration candidate** for this application version. They neither perform nor authorize migration, certify arbitrary old artifacts, test power failure/catalog transactions, nor prove order/engine recovery. Since Nautilus v2 does not require Arrow, there is no engine-driven reason to rush this independent storage change.

## R — causal prototype executed, provider equivalence remains untested

**160/160 initial runs passed**, with no case reruns: eight fixed journals, five delivery paths (batch chunks 1/7/64, replay and simulated streaming injection), each at full length and three prefixes. The independently authored per-event oracle, source/fixture hashes and exact New_York TZif are preserved in the [R evidence and review](../../phase-iv/technical-results/R/REVIEW.md).

The journals cover delayed closed bars, session/DST metadata, raw trades and late/corrected events, precision, gaps/duplicates/recovery, a causal conversion join, distinct event/availability order, and transformation-state restoration. Assertions compare admitted information and decisions, forbid future-prefix contamination and preserve explicit unavailable/blocked states. They do not compare simulated fills with actual execution.

Scope is deliberately narrow: trade aggregation uses one instrument and fixed bins; the multi-input case is a fixed conversion join, not a generic cross-market engine. Revision-parent validation is not implemented. R8 restores transformation state in memory; it is **not** E5's process interruption, durable venue reconciliation or native engine recovery. Real historical/direct-feed equivalence still requires a separately admitted source-specific replay/capture check.

Two early isolation bootstrap probes failed before their intended payloads because Landlock was unavailable. A separate successful probe demonstrated IPv4/IPv6 socket denial. The first R invocation omitted the required fixture argument and exited before any case; the corrected command then executed the 160 cases once. All original logs remain visible. Setup failures are not erased, counted as passing cases or represented as a consumed case-repair cycle.

## E — partial execution; neither engine admitted

**E is not complete: 3 component cases executed, 23 case slots unexecuted and zero fully admitted cases.** The installation paths were actually attempted. This is not a completed two-engine comparison. [E receipts and case dispositions](../../phase-iv/technical-results/E/README.md) distinguish every unexecuted slot from a failure and a pass.

| Candidate / actual work | Result | Consequence |
|---|---|---|
| Nautilus 2.0.0rc7, pinned Python 3.13.18 through uv 0.12.23 | Downloadable runtime unavailable; actual install reports `No download found`. All13case slots unexecuted | Blocked setup route, not evidence of incorrect engine behavior. No substitute version installed |
| LEAN exact commit 22404ea28; SDK 10.0.403 | SDK verified; partial source acquisition excludes financial data bodies; dependency restore, offline locked restore and offline build succeed | Build compatibility demonstrated for this graph, not financial admission |
| LEAN E1 | Small frozen decision example matches; **partial harness/component evidence**, not full case admission | Availability guards are supplied by the harness. R1/R3/R7 canaries, prefixes and explicit unsupported-precision execution are missing |
| LEAN E2 | Native buy 2 at 100, fee 0.4 and resulting USD 799.6/SYN 2 reconcile. Required sell 1 limit 102 remains open | **Mandatory comparison fails**: the chosen native limit model requires crossing, while the fixture only touches 102 |
| LEAN E3-L1 | Native market order fills 4 at 100 despite visible ask quantity 1; fee 0.8 | **Mandatory finite-visible-liquidity comparison fails**; full fill quantity is not constrained by supplied L1 size |
| LEAN remaining slots | E3-L2, E4, E5 reference/three cuts and four resource runs **not run** | Finite L2/IOC consumption, broker identities/shared attribution and same-journal reconciliation are absent from this bridge; performance follows functional admission |

**Interpretation of the adverse evidence:** E2 does not establish incorrect cash accounting or a universal LEAN defect. A touch is not a guaranteed maker fill when queue/priority information is absent; the frozen fixture's expected sale is an assumption, and this configured native model does not satisfy it. No price, tolerance or expectation was changed after seeing the result. E3 demonstrates a concrete default-model limit under the approved conservative L1 requirement; it does not prove that all LEAN models or future custom integrations overfill.

The worker actually invokes native Common `ImmediateFillModel`, configured `CoinbaseFeeModel` and `SecurityPortfolioManager`; it does not run LEAN's default Launcher or a complete brokerage lifecycle. Native fills/fees/cash are retained. Order admission, available/free/reserved cash, scheduling, observation IDs and maker/taker labels have explicitly recorded harness origins. They cannot prove native brokerage rejection, idempotency, multibot allocation or recovery. No expected-fill emitter or new fill model was substituted.

E1's incomplete coverage is a **harness gap**, not an observed native causality failure. The untouched R canaries include sub-100 ns timestamps; LEAN's DateTime boundary cannot silently represent them. Explicit rejection of these inputs remains unexecuted. E5 is also an unproved integration/reconciliation requirement, not proof that the engine universally cannot recover. These gaps remain on the acceptance list rather than being removed to declare success.

Original .NET restore failed before transfer because its named mutex attempted a read-only home directory. Isolated `XDG_RUNTIME_DIR`/`XDG_DATA_HOME` fixed that environment setup without changing HOME, SDK, upstream source or production. The original failure and one configuration correction are preserved. The upstream build reported4,046 warnings and zero errors; these warnings and the disabled online NuGet audit are retained, with no vulnerability clearance claimed. No engine cases were retried or model assumptions relaxed.

## Recommendation and material next choices

1. **Retain current production dependencies.** M makes an exact Arrow 26 migration supportable, but it is optional and separately authorized; it does not resolve Nautilus's Python requirement. Preserve the integer timestamp route.
2. **Retain R as a future conformance specification.** Source-specific historical/direct verification remains necessary before trusting an actual provider; no new dataset/feed acquisition follows from this pass.
3. **Do not select a financial engine from this partial comparison.** To reopen Nautilus, bind an obtainable managed Python distribution and installer route in a narrowly reviewed version change; the pinned unavailable route cannot be repaired by silently upgrading. For LEAN, first decide whether to investigate an additional finite-liquidity model/bridge beyond the existing-model-only scope, or retain the candidate as deferred. The observed model limitations and remaining E1/E4/E5 coverage must be resolved before admission. Another broad framework survey is unnecessary.

E3/E4's budget/capital/economic/risk decisions still lack sufficient financial/data evidence. No arbitrary numbers are proposed. Current tests provide no strategy-return evidence, and Phase IV is not unconditionally closed.

## Resources, preservation and remaining decision

The [final preservation audit](../../phase-iv/technical-results/preservation.json) finds no differences in 73recorded software/configuration files or 4,630regular production-environment files, and no protected scientific/source changes. Symlink targets and private runtime state are outside that baseline.

| Package | Instrumented active wall | Peak sampled RSS | Current scratch | Charged software transfer |
|---|---:|---:|---:|---:|
| M |43.50s|250.50MiB|1.16GiB|51.43MiB|
| R |0.65s|12.63MiB|0.21MiB|0|
| E |154.31s|1.56GiB|1.16GiB|264.84MiB|
| Aggregate, sequential |**198.46s**|**1.56GiB** maximum|**2.32GiB**|**316.27MiB**|

Exact [resource receipts](../../phase-iv/technical-results/resources.json) include failed setup and case invocations. Runtime memory's short sampled peaks can be missed; R's own process maximum is 14.50MiB. Scratch figures are current/after-command records, not continuous peak certification. Git/NuGet transfer allowances include bidirectional TLS bytes; nested download time is counted once. No resource stop triggered. These figures exclude unmeasured preparation/review effort and days interrupted by credits; they are not the total cost or duration of research. No services were contracted.

**Read outcome fields, not only process exit codes:** E2/E3 workers and supervisors returned 0 after collecting observations; `status`, `problems` and `full_case_admitted=false` record the failed comparisons.

Resource receipts and the final combined status are collected in the [execution checkpoint](../../phase-iv/technical-results/PROGRESS.md). Package work is serialized by one lock. CPU affinity and sampled process-group RAM/disk guards bound the work; their measurements are not kernel-enforced memory peaks or a hostile-code sandbox certification. The host did not support the requested nested filesystem isolation. Disposable copies and the final source/runtime hash audit therefore establish preservation, not OS-enforced inability to write production.

Scientific hypotheses, E1/E2, the 26 base specifications, T/D/U/V/F, original acceptance conditions, negative A/B evidence and future UX work remain unchanged. Seven financial counters remain zero. Technical passes cannot determine E3's financial research budget or E4's capital/materiality/risk choices.
