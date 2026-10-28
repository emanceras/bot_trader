# Decision package — M, E and R technical checks

Document ID: IV-TECH-001 · Version: 1 · Date: 2026-10-28 · English canonical. [Spanish](../../es/phase-iv/technical-packages.md).

## Decision ready for authorization

**Recommend one bounded authorization for the isolated M/R checks and the two-engine E comparison below, with stop rules and no production migration.** Approval has not been given and no package has been installed or executed. The user's [methodological approval](../../phase-iv/APPROVAL-STAGED.es.md) is now recorded separately in [IV-AMEND-001](staged-amendment.md); T/D/U/V/F does not authorize financial access, Phase V or these new technical jobs. E3/E4 remain pending.

The current scope is a decision test, not a new platform, broad technology review or complete financial adapter. Preserve C1/C3 priorities, C2 comparison, C4/C5 reserves, 26 base specifications, approved inference, existing synthetic v1 history and all prior A/B failures. No additional market data or live stream is needed. Synthetic prices/orders here are invented accounting fixtures, not a financial backtest or evidence of alpha.

| Package | Concrete decision | Exact technical route | Passing means / does not mean |
|---|---|---|---|
| **M — storage/dependencies** | Can an Arrow upgrade preserve the current application and existing artifact semantics? | Python 3.12.14; current lock Arrow 23.0.1/DuckDB 1.5.6 versus one disposable candidate changing only Arrow to 26.0.0. Full details and fixture limits in [M/R annex](technical-packages/dependencies-temporal.md) | Applicable synthetic regressions, old-artifact immutability/readability and exact value/identity/availability checks pass. It does not approve production migration or make Nautilus v2 run under Python 3.12 |
| **E — execution engines** | Which engine, if either, meets our scoped execution/accounting/interface requirements with acceptable implementation burden? | Nautilus **2.0.0rc7**, commit `55c0e82053142bce3a5cba4de4221d3929c2d3bc`, Python **3.13.18**; LEAN commit **`22404ea28b8d3f3c9eb74d6ed9f0444426f8e417`**, .NET SDK **10.0.403**. Same synthetic input/oracle, separate runtimes and a minimal Python 3.12 supervisor; [E annex](technical-packages/engines.md) | Required semantics are demonstrated for the specified fixtures and exact versions, with native behavior versus harness protection identified. No production, live recovery or universal product certification follows |
| **R — time and decisions** | Can one causal transformation/decision specification give equal outputs from equal available information across batch, replay and a simulated streaming interface? | Current Python/lock, fixed synthetic arrival journal and calendar cases; shared fixture contract with E. Batch and streaming injection operate locally, without a market connection | Prefix, availability, aggregation and decision invariants hold under declared precision/order rules. No actual feed quality, economic predictability or real-fill equality is claimed |

## Why the exact versions change the earlier proposal

The version check is deliberately narrow and reuses existing research. Nautilus **1.231.0** remains the final stable v1 with restricted security maintenance; its Arrow dependency conflict and adverse L1/recovery findings remain historical evidence. The active v2 candidate **2.0.0rc7** instead requires Python `>=3.13,<3.15`, has no mandatory PyArrow dependency in its inspected metadata and is a **prerelease**, not a production-ready stable choice. Its exact wheel and source identities are in the E annex. Testing it now can reveal architectural incompatibility; passing cannot eliminate its release-maturity risk. If a stable maintained release is required before any prototype, defer this branch rather than mislabel rc7 stable or silently install a later version.

LEAN's latest GitHub release entry is old and unsuitable as a maintenance indicator. The proposal pins an exact recent development commit and matching .NET 10 build requirements; this is a maintained-branch snapshot, not a guaranteed supported release. Both exact versions remain candidates. A later release is a new reviewed version, not an automatic upgrade inside this authorization.

**M is therefore independent of E.** Arrow 26 may be viable for storage without being necessary for the selected engine. An M failure does not block a worker-based E comparison; an M pass does not justify updating production. The present E scope deliberately tests separate runtimes: Python 3.13 for Nautilus and .NET for LEAN differ from the stable application. This is a test boundary, not a permanent process-architecture decision. A same-process Python upgrade is excluded.

## Minimal sequence and allowed work if approved

1. Freeze fixture IDs/expected outputs, exact package/source hashes, dependency inventory and one execution manifest in a disposable directory. Verify host capacity and write/network isolation. Preserve the source checkout, locks, existing artifacts and old result hashes. No access to market archives or credentials.
2. Implement the small R fixture/oracle and M compatibility harness outside production; validate harness expectations independently before interpreting engine results. Reuse the old A/B observations without reinstalling v1 merely to accumulate passes.
3. Run M and R under their finite bounds. For E, first resolve/install/build only the pinned runtimes and source subset, then the required cases. Stop a route on an unresolved mandatory capability, unsafe data access or resource limit; do not substitute versions or relax the oracle to obtain a pass.
4. Run E's resource/transport and interruption cases only after basic accounting and semantics permit meaningful interpretation. Only configuration of existing engine fill models is included. If a new fill model is required, record that implementation gap and stop the dependent comparison; do not build it in this package. The harness cannot supply expected outcomes directly or turn unproved native recovery into a pass.
5. Report pass, adverse, unsupported and not-run states separately, exact resources, package versions, transport/accounting observations and preserved failures. Recommend an engine only for a stated admitted use; defer both if neither meets required gates. Publication of harnesses and small synthetic results is allowed within the requested scope; large binaries/caches remain outside Git.

M/E/R installation, harness implementation and execution are the **new permission requested**. Ordinary configuration and bug diagnosis within their declared limits would not require a question for each field. Changes to a version, fixture requirement, resource ceiling, data source, production environment or full adapter fall outside it. No financial development is hidden in this technical work.

## Resources, risks and stop rules

Package-specific estimates and hard ceilings are stated in the annexes. They are engineering planning choices, not measurements or financial research budgets. Use the existing host sequentially: at most **4 vCPU and 8 GiB RAM** for one package, with **12 GiB aggregate scratch/storage** including caches and retained failures. The inspected host has a 4-CPU/32-GiB cgroup and approximately 27 GiB free workspace; capacity must be rechecked after interruptions. Host availability does not authorize paid expansion. Stop before overrunning a bound; a resource-limited result is inconclusive about engine correctness.

| Package | Initial bounded work | Estimated active machine time / hard ceiling | Maximum software transfer / scratch |
|---|---|---|---|
| M | 20 custom cases, up to six old-artifact reads, two backend-suite invocations | 20–60 min / **2 h** | **512 MiB / 3 GiB** |
| R | Eight journals × five paths × four full/prefix runs = 160 | Under 10 min / **1 h** | **None / 0.5 GiB** |
| E | Nine functional plus four resource attempts per engine = 26 | 1–2 h / **4 h** | **2 GiB / 8 GiB** |

The combined ceiling is **7 hours active machine time, 2.5 GiB software transfer and 12 GiB scratch**, with the per-package limits still binding. One diagnosed harness-correction cycle is included in those same caps, with explicit attempt ceilings in the annexes. Preparing/reviewing the small harnesses is estimated separately at 0.5–1.5 person-days for M, 1–2 for R and 2–4 for E; these uncertain engineering estimates are not elapsed compute or a delivery promise. They do not authorize paid labor or subscriptions.

Download permission, if granted, is for specified software/runtime packages and transitive build dependencies only. LEAN acquisition must exclude upstream `Data/` and any bundled market samples; no full source archive, sample-history downloader, paid CLI, broker plugin, Docker image or networked market example is admitted. Install traffic and unresolved transitive sizes are bounded and logged; fixture runs use no outbound market/network access. Runtime build failures, hidden data/network dependencies or inability to enforce isolation stop the route and are reported.

No new service, subscription or USD expense is proposed. Software licence/source provenance and binary hashes must be retained; repository licences do not certify all transitive redistribution rights. Human engineering time is an estimate, not a delivery guarantee; unexpected upstream defects consume the finite repair allowance and can end the comparison. A technical pass provides no estimate of strategy returns, economic materiality or acceptable personal drawdown.

## What remains open after these checks

E3/E4, historical acquisition/source rights and coverage, production migration, a complete financial adapter, prospective feeds, paper/live, Windows certification and Phase V remain separate. M/R can establish the proposed local data-contract mechanics; they cannot choose a provider whose historical and live data have not been examined. E can justify a scoped engine recommendation, not a universal permanent winner. Preserve future UX/glossary/guide work without implementing it.

The decision needed now is whether to authorize the bounded technical scope above, including the explicit rc7 maturity limitation. **The staged methodological principle is already approved and is not being submitted again.** No further general research round is required before this technical decision. [Checkpoint and evidence](../../phase-iv/technical-packages/PROGRESS.md) distinguish documentation already completed from tests awaiting authorization.
