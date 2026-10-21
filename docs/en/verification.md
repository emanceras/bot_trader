# Phase III technical verification

Document ID: VERIFY-III-001 · Version: 1 · Updated: 2026-10-21 · Language: en (canonical).

Translation: [Spanish](../es/verification.md), synchronized with VERIFY-III-001 v1. This report supplies execution evidence for the [acceptance register](../phase-iii/acceptance.md), the original [request](../phase-iii/REQUEST.es.md) and the [architectural supplement](architecture/supplement.md). Technical acceptance does not validate a financial hypothesis.

## Scope and current disposition

The implemented release is a local modular research platform with authenticated HTTP services, persistent versioned records, synthetic data, bounded technical jobs, reports and a built web client. Its accounting harness is a deterministic software test instrument, not an admitted financial backtesting engine. H-00–H-24 and the 53-work scientific corpus are preserved. Financial experiments, financial model training, prospective paper trading and live operations remain **zero**.

**Disposition: III.A and III.B technically complete within the authorized synthetic scope**, recorded in D-034 and the acceptance register. All essential checks below passed; no financial validation or next-phase authorization is implied.

## Environment and executed checks

Backend/install/unit checks ran on 2026-10-20, with final browser/default-startup and release reconciliation on 2026-10-21, in the managed Linux workspace, from `/workspace/bot_trader`, using Python **3.12.14**, Node.js **24.19.0**, npm **11.9.0**, frozen `uv.lock`/`web/package-lock.json` and the installed Chromium executable at `/usr/bin/chromium`. The source checkout is required; this does not certify a standalone wheel, Windows installation, a production server or a fresh-task environment restoration.

Writable cache settings were `UV_CACHE_DIR=/workspace/.cache/uv` and `NPM_CONFIG_CACHE=/workspace/.cache/npm`. Commands retained their real exit status; a build or zero-test invocation was not counted as a passed test suite.

| Check | Executed command / evidence | Recorded outcome |
|---|---|---|
| Clean Python installation | `UV_PROJECT_ENVIRONMENT=/workspace/.bot-trader-clean-venv uv sync --frozen` with the writable UV cache | 36 distributions installed into a fresh environment |
| Backend suite in that environment | `UV_PROJECT_ENVIRONMENT=/workspace/.bot-trader-clean-venv uv run --frozen pytest -q` | **110 passed**, one warning, 32.49 seconds; no skipped/expected failures reported |
| Final backend rerun after capability-status alignment | `uv run --frozen pytest -q` | **110 passed**, the same warning, 2.63 seconds |
| Python lint | `uv run --frozen ruff check src tests` | Passed |
| Strict Python typing | `uv run --frozen mypy src` | Passed, 30 source files |
| Locked frontend installation | `npm ci --cache /workspace/.cache/npm --no-audit --no-fund`, working directory `web` | 110 packages installed; inventory records 152 resolved packages including optional platform packages |
| TypeScript | `npm run typecheck`, working directory `web` | Passed |
| Production frontend build | `npm run build`, working directory `web` | Passed; built assets served by the API |
| Frontend unit/component checks | `npm test`, working directory `web` | **7 passed in 3 files**, final rerun 1.53 seconds |
| Real browser F | `python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-final3` | **2 passed in 18.2 seconds**, no skipped tests; actual API, storage, worker and Chromium, not mocked endpoints |
| Final browser after capability-status alignment | `python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-release` | **2 passed in 19.5 seconds** on 2026-10-21; owned processes stopped afterwards |
| Reusable installation/default startup | Exact saved install script; repeated `bot-trader init`; actual `serve` and finite `worker` | Passed: locked install/build/init, unchanged private credential, authenticated 25-hypothesis/15-module reads, built HTML and notices; no queued financial work |
| Stopped-writer restore | Copy coherent private state after stopping owned API/worker processes; verify records and artifacts through application services | **Passed**: 12 identical file hashes; 25 hypotheses, one dataset/24 bars, three preserved attempts and verified report hashes |

For the restore check, the browser harness had stopped its own API and worker. A Python check invoked with `uv run --frozen python` copied `/workspace/.bot-trader-browser-final3` to the separate new `/workspace/.bot-trader-restore-check` using `shutil.copytree`. All 12 file SHA-256 values matched before opening the copy. The application schema check and `build_services` read the restored 25 hypotheses, one dataset with 24 bars, and three attempts: two succeeded and one retained `intentional_fixture_failure`. Each successful JSON report matched its recorded digest. The original state was untouched and no attempt was replayed. This verifies one coherent local stopped-writer restore, not online backup, cross-host recovery or recovery without a usable snapshot.

After the browser pass, the module inventory was aligned with the tested scope: `web` and `charting` are operational within the synthetic platform. The final backend rerun, Ruff, strict Mypy, TypeScript, frontend unit suite and production build passed after that change. The code release is `70761ad` (dashboard/chart, following `eabbd8e` backend and `2cf79b4` core). Technical evidence was collected against the same executable source with local documentation changes; run manifests retain their actual Git/dirty identity. Documentation closure is versioned separately. Publication uses the authorized normal push and remote-HEAD check, not a force push.

The single backend warning is the FastAPI/Starlette test client's deprecation warning about its current `httpx` integration and a future dependency transition. Tests executed successfully. The warning was not hidden, and no dependency was added merely to suppress it. Exact resolved package versions and archive identities remain in the lockfiles.

## Mandatory demonstrators A–F

| Gate | Concrete executed evidence | Interpretation and limits |
|---|---|---|
| A — new module | `tests/test_core.py::test_a_add_module_and_b_extend_internal_capability`; `test_registry_rejects_missing_cycles_and_prepared_execution` | An explicit extension is callable without changing the consumer; duplicate registration, missing dependencies, cycles and inactive capabilities are rejected. No untrusted plugin sandbox is claimed. |
| B — internal capability | The same test adds a separate optional capability and checks that the existing capability remains unchanged; `web/src/chart/SeriesChart.test.tsx` verifies renderer input and cleanup | Public composition/renderer boundaries work. This is not a claim that every possible future module is already implemented. |
| C — implementation replacement | `tests/test_market_data.py::test_repeatability_provenance_and_memory_substitution`, `test_memory_store_and_local_store_share_missing_and_format_failures`; `tests/test_simulation.py::test_c_same_ledger_consumer_accepts_execution_and_cost_substitution`; the core transformation substitution test | Real local/memory artifact adapters and execution/cost adapters satisfy common consumers and failure contracts. No PostgreSQL, external storage or mature financial-engine adapter is certified. |
| D — isolation | Core mode/role tests; `tests/test_lab.py::test_final_lineage_blocks_submit_reads_reports_and_worker`; market-data reserved-partition tests; API absent-route and role tests | Every role, including admin, is denied final payloads and financial actions. Reads, transforms, reports and workers follow stored lineage. No paper/live/order/market-import/tool route is supplied. Host-administrator isolation is outside scope. |
| E — reproducibility | `tests/test_lab.py::test_e_repeated_attempts_same_inputs_have_identical_persisted_results`, parametrized over quality, transformation and ledger tasks; persisted failure, restart, drift and stale-import tests | Separate attempt IDs retain matching stable report digests under the same frozen inputs and identity. A seed alone is not a cross-platform reproducibility guarantee; changed source/environment is rejected. |
| F — actual web | `web/e2e/platform.spec.ts`, real backend/worker harness `scripts/browser-check.py` | **Passed.** The actual path covered 25 hypotheses, fixture/chart/attribution, two completed jobs and comparison, report retrieval, preserved intentional failure, 15 module states, audit, mobile layout/logout, revoked session and server-side viewer denial. |

Frontend unit checks additionally cover empty states without fabricated data, viewer controls, reserved metadata without chart access, safely rendered untrusted hypothesis text, selected immutable dataset versions, CSRF behavior and safe authorization errors. They supplement F rather than replace it.

## Persistence, temporal integrity and security evidence

- **Persistence and recovery:** `tests/test_persistence.py` verifies explicit fresh migration, schema incompatibility rejection, database connection invariants, append-only/versioned history, idempotent identical content, concurrent atomic claims, bounded queues, cancellation and recovery fencing. `test_recovery_during_publication_fences_late_worker` rejects late publication after recovery. Restart does not erase failed or successful attempts. This is not automatic worker failover.
- **Content identity:** document reads recompute hashes; artifact reads reject missing, modified or unregistered content and traversal/symlink/size violations. Tests distinguish integrity from source truth or external accounting reconciliation.
- **Causality:** market-data tests preserve availability across prior transformations and verify prefix/future-input perturbation invariance for the finite-window transform. `tests/test_temporal.py` checks chronological partitions, label availability, overlap/purge/embargo boundaries, immutable plans and one untouched final interval. These tests do not prove correctness of an unavailable market dataset or detect every form of research leakage.
- **Synthetic accounting:** `tests/test_simulation.py` checks cash/inventory/fee conservation, injected execution/cost/risk behavior, atomic rejection, duplicate IDs, chronological inputs, fill compatibility and prohibited short sales. It does not model venue queue priority, market impact, margin, liquidation, partial-fill reconciliation or market capacity.
- **Authentication and authority:** `tests/test_auth.py` and `tests/test_api.py` verify private idempotent credential creation, no symlink following, session expiry/revocation, bounded login, server-derived roles, Host/Origin/CSRF checks, bounded bodies, safe errors and absence of execution routes. Restart intentionally revokes API sessions. This is a trusted-local application assessment, not an independent penetration test or multi-tenant security certification.
- **AI boundary:** `test_agent_proposals_are_inert_and_budget_is_transactional` checks finite persisted quotas, rejected escalation fields and no job creation. Stored proposals are non-executable and do not authorize resources. No model call, RAG agent or autonomous loop ran.

## Original deliverables and supplement disposition

The [acceptance register](../phase-iii/acceptance.md) retains all **19 III.A** and **20 III.B** criteria. Their implementation/evidence map is:

| Original deliverables | Delivered material and verification |
|---|---|
| III.A 1–3, 6–10 | Repository diagnosis, requirements, diagrams, domain boundaries, public contracts, data model and web/backend design in [platform architecture](architecture/platform.md), reconciled with `core`, `application.py`, persistence and API code |
| III.A 4–5, 11, 15 | [Stack](architecture/stack.md), [engines](architecture/engines.md), [research/chart tools](architecture/research-tools.md); official-source receipts, license inventories, frozen installs and adapter tests |
| III.A 12–14 | Durable synthetic laboratory; first-class inactive paper design; inert AI records/permissions and future activation gates |
| III.A 16–19 | Security boundaries, cost classes, D-031–D-033 decisions and dependency-ordered implementation/acceptance plan; no expenses or later-phase activation |
| III.B 1–4 | Single repository, explicit registry, validated settings and typed frozen contracts; core checks A–D |
| III.B 5–8 | Actual authenticated API, explicit migrations, synthetic Parquet/Arrow/DuckDB path, preserved hypotheses and durable versioned attempts; API/data/persistence/hypothesis tests |
| III.B 9–11 | Finite laboratory, persisted reports/comparison, replaceable model/strategy/execution contracts and bounded accounting harness; E and accounting tests |
| III.B 12–14 | Built six-section web, reusable chart, actual 15-module registry; frontend checks and **F passed** |
| III.B 15–18 | Safe errors/correlation IDs/audit, static and automated tests, A–E, clean installation and explicit API/worker; real browser and stopped-writer restore evidence as stated above |
| III.B 19–20 | Paired EN/ES technical documents, [translation policy](../TRANSLATIONS.md), current roadmap and explicit next-phase authorization gate; historical science is preserved rather than silently translated/replaced |

The [supplement matrix](architecture/supplement.md) maps all 28 user sections, 21 capabilities, eight identity scenarios and fourteen requested test dispositions. Its minimal implemented addition is `VersionedReference` plus optional exact historical hypothesis references in technical runs. `test_supplement_hypothesis_version_change_preserves_historical_association` proves a new hypothesis version does not rewrite a prior run, a wrong hash is rejected and duplicate references are invalid. It does **not** validate the hypothesis or prove bot identity isolation.

Supplement tests 4, 5, 7, 10, 11, 13 and 14 have the bounded technical evidence specified in that matrix. Test 12 is covered by the actual F run. Test 9 covers only injected synthetic risk and denied modes; global/account/portfolio precedence is deferred. Tests 1–3, 6 and 8 require future instance/capital/signal/authorization/confirmation services and are not passed by analogy. No empty tables or operational services were introduced to make those rows appear complete.

## Failures, corrections and independent review

These outcomes are retained rather than omitted from the successful-check summary:

1. Initial npm installation encountered an unwritable default cache and misleading archive/integrity warnings. A writable workspace cache resolved installation; the relevant upstream archive identity was checked. TLS, package checksums and expected integrity values were not weakened or bypassed.
2. Initial frontend testing discovered zero tests and reported three suite failures because Vitest globals were not enabled. The explicit test configuration was corrected; the rerun executed and passed all seven tests.
3. An independent internal backend review identified stale imported-code attribution and omitted prior-transformation availability. The implementation now binds loaded code identity, requires restart after source/dependency drift and propagates transformation availability. Regression tests passed. Document hash verification and causal prefix/future-perturbation coverage were also added. This review is internal code scrutiny, not external scientific replication or certification.
4. The first real-browser run had one passed and one failed test. Its dataset selector used an ID parsed from visible text that also contained the version. The harness was corrected to obtain the ID from the real POST response and await each completed attempt. A second run still failed one test because the exact label locator did not select the intended wrapped control; the harness now addresses its accessible combobox role/name and asserts the returned dataset ID. The corrected real-browser run passed both tests. Product behavior was not bypassed or mocked to resolve these test-locator defects; the original failures remain recorded.

5. Final status-description formatting briefly failed Ruff's line-length rule; wrapping the line restored the unchanged behavior and the full static/backend checks passed. The separate default-startup smoke check initially expected HTTP 201 for login, while the declared session endpoint returns 200; the assertion was corrected and the authenticated read/startup workflow passed. Neither correction changed an acceptance rule or a product authorization.

## Reusable cloud configuration

The `cloud-environment-onboarding:setup` workflow was applied. On 2026-10-21 the configuration tool confirmed **saved** `install_script` and `start_skill`, draft `019aa6d4-0bc4-451f-a76d-4710c22ef91b~cecfgdraft_6ad82485ac748192a28b7e07eb9e777a`, with `requires_publish=true`. No repository membership, network policy or secret requirement was changed. The tested install script is:

```bash
set -euo pipefail
cd /workspace/bot_trader
export UV_CACHE_DIR=/workspace/.cache/uv
export NPM_CONFIG_CACHE=/workspace/.cache/npm
uv sync --frozen
npm --prefix web ci --no-audit --no-fund
npm --prefix web run build
uv run --frozen bot-trader init
```

Saved startup instructions name the same checkout, API/worker commands, liveness versus authenticated readiness checks, private credentials, isolated browser helper and restart/recovery boundaries. They create no user-facing cloud preview. The current instance is verified; publishing the environment still requires reviewing/saving its settings and publishing in the environment UI. Saving this draft does not publish the environment or certify restoration in a new cloud task. Application test processes were stopped after verification.

## Licenses, remaining limits and next gate

The [Python inventory](../licenses/python-dependencies.json) records 36 installed distributions, including the project; the [npm inventory](../licenses/npm-dependencies.json) records 152 resolved packages, distinguishing optional packages not installed on this platform. These metadata inventories are not legal certification or a security vulnerability scan. No license for this project's own source is inferred from dependency licenses.

Runtime frontend licenses/notices are collected in `web/public/THIRD_PARTY_NOTICES.txt` and served by a fixed application route. Lightweight Charts' upstream LICENSE/NOTICE and visible TradingView attribution/link are retained. The missing `fancy-canvas` package license file was recovered from the official version-tag commit; `web/licenses/fancy-canvas/provenance.json` records its origin and content identity. No dependency was added for the architectural supplement.

Known boundaries remain single-host SQLite, one API process with in-memory sessions, finite synthetic tasks, explicit interrupted-worker recovery, no live data connector, no production trading engine, no multibot capital allocator, no external reconciliation or continuous monitoring. A future module needs its own meaningful contract, execution, temporal and permission checks. An integrity hash cannot prove complete/correct external events or resist a malicious host administrator.

Phase IV requires separate explicit approval. Its work would define preregistered financial protocols, data admission/licensing, market-engine compatibility, costs, uncertainty, finite search budgets and holdout governance for the accepted candidates. No such financial evaluation is authorized or implied by this software release. Current scientific selection remains C1/C3 primary, C2 secondary, C4/C5 conditional; no strategy has been declared profitable.
