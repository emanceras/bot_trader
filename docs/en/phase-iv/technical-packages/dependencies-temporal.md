# M and R — bounded dependency and temporal checks

Document ID: IV-PKG-MR-001 · Version: 1 · Date: 2026-10-28 · English canonical. [Spanish](../../../es/phase-iv/technical-packages/dependencies-temporal.md).

> **Execution update, 2026-10-29:** D-046 subsequently authorized this exact scope. See [actual results](../technical-results.md). The proposal below is retained as the pre-execution specification; its earlier pending-approval statements are historical.

**Execution proposal, not approval or a test result.** These two packages answer separate technical questions. M checks one Arrow upgrade against the existing application; R checks causal information/decision equivalence through a small standalone prototype. They neither implement a production financial adapter nor execute a trading hypothesis. E3/E4, Phase V and market-data acquisition remain pending. Existing [dependency](../evolution/dependencies.md) and [temporal](../evolution/temporal.md) reviews supply the rationale; no additional general survey is needed.

## Decisions enabled and dependencies

| Package | Decision enabled by a pass | What a pass does not decide |
|---|---|---|
| M | Whether Arrow 26.0.0 can replace 23.0.1 in the current Python 3.12 application without the tested semantic, persistence or permission regressions | A production upgrade, compatibility with arbitrary future versions, or the engine/process boundary |
| R | Whether one frozen causal transformation/decision specification produces equivalent outputs for the same available information through batch, replay and an offline streaming injector | A real provider's historical/live equivalence, market prediction, identical fills or permission to collect a stream |

M and R can be authorized together but are independently interpretable. R uses the current lock and standard library; it does not depend on M passing. [E](engines.md) can examine independent engine processes even if M fails. The inspected active Nautilus v2 candidate requires Python 3.13 and does not declare PyArrow as a mandatory dependency: **upgrading Arrow alone would not enable that engine in the application's Python 3.12 environment.** M is a storage-compatibility option, not a prerequisite imposed by an obsolete engine dependency assumption. No Python upgrade is included in M.

All future work remains outside production: an explicit source export of the application at the approved package commit into a disposable directory; separate environments and test state; no worktree rebuild of the existing checkout. Copy no private `.state/admin.token`, credentials or real Q3 QA archives. Temporary authentication fixtures created by existing tests stay private and are not published. Preserve production source/locks/state and record before/after hashes for any selected read-only artifacts.

## M — exact environment and finite installation scope

| Item | Control | Candidate |
|---|---|---|
| Platform | Linux x86_64, current host; Python **3.12.14**, `uv` **0.12.23** | Same host, interpreter and installer |
| Dependency set | Exact repository `uv.lock` at the approved scope commit; PyArrow **23.0.1**, DuckDB **1.5.6** | Change PyArrow only to **26.0.0** in the disposable source copy; constrain every other package to its control lock version, including DuckDB **1.5.6** |
| Source and guards | Export of the unchanged application and tests; original source digest recorded | Same exported source/tests except the disposable package constraint/lock needed to admit Arrow 26; no relaxation of synthetic-only or reserved-data guards |
| Network | Reuse verified cached artifacts where available; otherwise exact locked software packages only | One candidate resolver attempt, then the exact admitted wheel and any already-locked packages within the cap below; no alternate Arrow/DuckDB versions |

The candidate lock must be produced and diffed **before installing it** as part of the authorized package. If the resolver requires changing another package, record the failure and stop M; do not broaden constraints or substitute a version silently. Import success alone is insufficient. Run the full dependency consistency check and retain exact locks, wheels/hashes and install receipts. No installer or resolver was run to prepare this proposal.

PyPI metadata [M-S1] identifies `pyarrow-26.0.0-cp312-cp312-manylinux_2_28_x86_64.whl`, **53,931,932 bytes**, SHA256 `6a628922ba20705fa964ca73e4ef959c2fb2f14b9bbec5589a6a1e68e6257c85`, Python requirement `>=3.11`. The body has not been acquired. If this exact wheel is unavailable or the platform is incompatible, stop rather than build Arrow from source. Reusing a cache still requires identity/hash verification. The source-export commit and unchanged control lock digest are bound in the execution receipt; selecting that commit does not authorize future code changes outside this scope.

## M — cases and acceptance

Prepare three small synthetic packs under the control writer: the existing v1 fixture recipe with **120 rows, seed 42**; a **32-row** Decimal/null/schema boundary pack; and a **32-event** precision pack with explicit integer nanosecond ticks, time-unit metadata and separately marked display timestamps. These are software test sizes, not strategy horizons or sample-adequacy assumptions. The last two packs exercise proposed interchange behavior outside v1; do not label them as production market contracts already supported. Freeze exact inputs and expected outputs before either candidate run.

Where the local application already contains eligible synthetic v1 artifacts, inventory their identifiers/digests without modifying them and include read-only copies of up to three distinct schema/writer versions, selected by version then identifier rather than outcomes. Exclude real, unknown-provenance or secret-bearing objects. If no eligible old artifact exists, report that limit: control-writer generation tests the old format but cannot claim to verify absent historical objects. These optional historical copies add at most six read checks, not a search for passing examples.

| Group | Finite checks | Mandatory acceptance |
|---|---|---|
| M1 — application and guard regression | Existing backend pytest suite once under each environment, using disposable state; imports and dependency consistency once per environment | Both controls and candidate satisfy existing assertions. A baseline failure invalidates attribution; retain it and stop dependent comparison. No frontend/browser rerun or market integration is required |
| M2 — old/new interchange | Three packs × two writers × two readers = **12 cases**. In each case inspect Parquet/IPC values and metadata plus the corresponding DuckDB projection; the two writers are control/candidate, never edits to original objects | Exact declared Decimal values, nulls, IDs, units, row order and availability; old v1 readable by candidate, candidate output readable by control where the admitted schema promises it. Preserve old byte hashes; changed new serialization bytes get new immutable artifacts |
| M3 — corruption and access | Corrupt digest, reserved partition and real-data label rejected in both environments = **6 cases** | Each fails closed before analytical access. Candidate results cannot excuse a bypass or a changed guard |
| M4 — interrupted artifact publication | One controlled writer interruption per environment = **2 cases**, with incomplete temp artifact and preserved original reference | No partial object becomes an admitted result; original artifact/manifest survives and restores consistently. This checks the artifact boundary, not order recovery |

Thus M contains **20 custom cases**, up to six explicitly logged old-artifact reads, and two existing-suite invocations. Generation, install/import/consistency checks and measurements also count toward its resource cap. Each custom case runs once; deterministic reruns require an identified harness defect, retain the original result and fit within the retry rule below.

The known DuckDB zoned-nanosecond precision loss is a **negative control**, not a surprise to erase. An unsafe native conversion must be rejected or reported as lossy; the admitted canonical route must preserve integer ticks/unit and all exact values. Display timestamp truncation may be explicit but cannot become the sort/join key. No numerical tolerance may hide accounting, availability or precision changes. Compare semantic values separately from serialized bytes. The outcome may be “Arrow compatible with tested v1, future precision route blocked”; this does not declare either version universally safe.

## R — one frozen specification, five delivery paths

Use Python **3.12.14**, the unchanged application lock where needed, and standard-library `decimal`, `json`, `hashlib` and `zoneinfo`. R installs no new package. It creates only a small isolated test module plus hand-authored fixtures; no production schema migration, source connector, scheduler, service or general aggregation framework. Existing v1 stays unchanged.

The shared fixture envelope contains integer `event_ns`, `available_ns`, receive ordinal, source-native ID/sequence, revision parent, explicit time unit, instrument/currency identifiers and Decimal strings. Unknown availability is explicit, never inferred from the final file. E can reuse these clock/identity canaries; matching the envelope does not imply that all engines support every precision/product subtype.

One pure state transition applies the same fixed rules in every path: receive order first; only inputs available by the current cutoff; deduplicate by scoped event identity; apply revisions only after receipt; invalidate state on a gap until the scripted resnapshot; finalize a bar only on the fixture's explicit closing event. The technical decision is `OBSERVE` or `BLOCK` with reason, eligible input IDs, latest complete-bar ID and state digest. It is not an order, strategy, return or portfolio target. Decimal/count checks and a hand-calculated expected journal form an independent oracle; agreement between two equally faulty paths cannot pass it.

Execute each of eight fixed journals, each **4–256 events**, through: batch chunks of **1**, **7** and **64** events; individual event replay; and an **offline in-memory queued injector** with prescribed arrivals. No socket, exchange connection, wall-clock sleep or prospective collection is needed. All paths use the same arrival order and logical clock. Repeat each at three prefix cuts—after event 1, at `floor(N/2)` and before event N—alongside its complete run: **8 × 5 × 4 = 160 bounded runs**. No random search or stochastic seed is used. The odd chunk size intentionally crosses closure/revision boundaries; these sizes are transport tests, not approved financial bar intervals.

| Case | Counterexample and expected behavior |
|---|---|
| R1 — availability and clock disagreement | Scheduled effective time, earlier publication, delayed receipt, equal cutoff and unknown availability. Only the declared available version enters the decision; a monotone economic-clock chain is not imposed |
| R2 — precision and identity | Two events within one microsecond, mixed explicit ms/us/ns units, equal-valued distinct IDs and duplicate deliveries. Preserve order/identity or reject unsupported representation; never guess a unit from magnitude |
| R3 — open/closed bars and aggregation | Boundary events, provisional/final/corrected bars, direct versus fine-to-coarse aggregation with aligned anchors, and deliberately misaligned anchors. Final values wait for the close event; only compatible aggregation paths may match |
| R4 — gaps and recovery arrivals | Sequence gap, duplicate recovery, unavailable snapshot and later valid resnapshot. Block dependent decisions while invalid; recovered data cannot rewrite previously emitted decisions |
| R5 — calendar boundary | New York DST fold/gap, an invented early close and overnight session. Ambiguous local time requires explicit fold/offset; nonexistent local time is rejected; session dates differ from UTC dates where prescribed |
| R6 — causal multi-input join | Two invented instruments and a conversion observation arriving late/stale. As-of join uses availability and a fixture-declared age rule; missing conversion blocks the dependent observation. Stablecoin labels do not silently become USD |
| R7 — revisions and prefix stability | Later correction, backfill, delayed external release and insufficient warm-up. Append future material without changing already-emitted decisions; a corrected-history view is separately labelled |
| R8 — state continuation and source mapping | Restore a small synthetic transformation checkpoint with last processed identity; deliver duplicate and next events. Match the uninterrupted journal exactly. Preserve source-native maker/taker meaning via an explicit fixture mapping, without pretending that a live adapter exists |

For R5, reuse the existing host TZif `America/New_York` snapshot, system tzdata label **2026b**, SHA256 `e9ed07d7bee0c76a9d442d091ef1f01668fee7c4f26014c0a868b19fe6c18a95` [M-S2]. Load an isolated read-only copy with `ZoneInfo.from_file`, not whatever timezone database happens to become current later. This pins a test dependency; it does not claim current IANA release or certify exchange calendars. The early-close/session table is explicitly invented. If the snapshot is unavailable, preserve the blocked calendar case rather than install another timezone package or silently change its hash.

R passes only if every admitted path matches the independent expected journal and its corresponding full-run prefix, with exact IDs, availability, reasons, Decimal values and canonical state. Different delivery content or a lossy/unavailable source must produce the expected explicit block/difference, not forced equality. These checks support an implementation invariant for the given prototype. Real feed capture/replay, provider reconciliation and scientific strategy equivalence remain later, separately scoped work. No result here would promise identical simulated/live fills.

## Resources, stops and requested execution boundary

These are **engineering planning estimates and authorization ceilings**, not measured results, financial budgets or required personal-machine specifications. Runs are sequential; the ceilings prevent a small compatibility probe becoming an open-ended engineering project. CPU/RAM/disk caps apply to each package's subprocess tree, not just its main interpreter. Existing-host use carries no new service purchase; electricity, staff time and provider billing are not inferred to be zero.

| Package | Planning estimate | Hard execution envelope proposed |
|---|---|---|
| M | 20–60 minutes setup/test compute; 0.5–1.5 person working days to prepare/review harness; about 0.5–2 GiB RAM and 0.5–2 GiB scratch, assuming compatible wheels | **2 vCPU, 4 GiB RAM, 3 GiB scratch, 512 MiB software transfer, 2 hours cumulative active setup/build/test time**. Exact Arrow wheel ~51.4 MiB; remaining allowance covers already-locked packages if the cache is incomplete. No source build |
| R | Under 10 minutes test compute; 1–2 person working days to implement/review the small fixture harness; small journals below 1 MiB before reports | **1 vCPU, 1 GiB RAM, 0.5 GiB scratch, no network, 1 hour cumulative active test time**. Same-host timezone copy and existing software only |

Record wall/CPU time, peak process-tree RAM, scratch high-water mark, software bytes and engineering effort separately. Human estimates are not delivery promises. Exceeding a cap yields `blocked_resource_limit`; do not rent capacity, expand versions, remove cases or weaken acceptance. A crash, timeout or missing fixture is not a pass. Do not interpret a short smoke-test time as the cost of the 26-specification financial wave.

One documented correction cycle per package is allowed only for a demonstrated harness/fixture transcription defect, within the same resource ceiling and frozen economic-free acceptance rules; preserve original evidence. A product limitation, baseline incompatibility, unsupported precision or changed acceptance is not such a defect. Stop for unintended network/market access, secret exposure, production write, hash mismatch, dependency drift, resource exhaustion or a decisive unmet mandatory invariant. Final status distinguishes passed, failed, blocked and not run; no “pass” through dropping a case.

The requested future authorization is limited to: verified software acquisition/install for M within the exact version/byte scope; disposable source exports and local harness code; the synthetic cases above; read-only copying of explicitly identified synthetic artifacts/timezone file; and publication of small source/receipt/result files with no secrets or real market series. R has no new installation. **Nothing has been installed or executed under these packages now.** No production upgrade, financial adapter, new data source, market dataset, strategy optimization, model training, paper/live or Phase V follows from approval or a pass. A successful M enables a separately reviewed production-migration decision; it does not perform that migration.

The correction ceiling is explicit: M may repeat each directly affected custom/read case at most once (maximum 52 custom/read attempts including the optional old-artifact reads) and each existing-suite environment invocation at most once (maximum four suite invocations). R allows at most one repeat of each directly affected path/prefix case, maximum 320 runs including the initial 160. All retries consume the original resource ceilings; no second correction cycle.

## Evidence reused and newly checked

- **M-S1 / PKG-M-01:** [PyPI metadata for PyArrow 26.0.0](https://pypi.org/pypi/pyarrow/26.0.0/json), previously retrieved on 2026-10-27 and reused from cache: release/Python requirement, exact CPython 3.12 Linux wheel name, size and SHA256. Metadata only; wheel not downloaded or imported.
- **M-S2:** current local timezone-version label and TZif hash, plus repository lock/source identities, read on 2026-10-27. [Dependency version receipts](../../../phase-iv/technical-packages/dependency-version-sources.jsonl) distinguish this local inspection from package execution. The frozen library facts and known precision limitations remain in the linked evolution review.
- New sizes, fixture counts and resource bounds above are explicit design choices for bounded software checks. They are not empirical estimates of market behavior, data sufficiency, return materiality or acceptable financial risk.
