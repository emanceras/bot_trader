# Phase IV — executive decision review

Document ID: IV-EXEC-001 · Version: 1 · Date: 2026-10-25 · English canonical. [Spanish](../../es/phase-iv/executive-decisions.md).

## Recommendation and status

There are **two design decisions to approve now**, and two economic/resource decisions to make later with concrete evidence. They are organized below as four topics. Existing user instructions on USD, free sources when adequate, commercial alternatives and spending permission do not need reapproval. Do not choose missing numerical thresholds to complete a form. The two design choices remain proposals; this review records no new approval. Continuing it does not authorize Phase V, financial datasets, model training, spending, prospective paper trading or live operation.

The [protocol](protocol.md), [candidate annex](candidates.md), [data/execution gates](data-execution.md) and [acceptance record](acceptance.md) are reused without new literature or changes to their numerical choices. This review refines the order and responsibility of decisions; it does not relax acceptance or populate the [freeze template](../../phase-iv/freeze-template.json). The 53-work corpus, H-00–H-24, contrary findings and C1/C3 priorities, C2 secondary role and C4/C5 reserves remain intact.

| Topic / decision timing | Recommendation | What is deliberately not approved yet |
|---|---|---|
| E1. Initial research scope — approve now | Conditional fully funded spot long/cash wave, with one justified horizon and point-in-time universe rule | Venue, accessible cash vehicle, exact horizon/universe parameters or permanent product restrictions |
| E2. Questions and finite comparisons — approve now | Retain the proposed 26-slot ceiling and three primary claims, conditional on feasibility | Total fits, calendar, full compute budget, universal conclusions about ML or other strategies |
| E3. Actual resource commitment — decide after sizing | Apply the existing free-when-fit policy; compare paid alternatives through itemized proposals | Purchases, subscriptions, a guessed dollar budget or unlimited work on free resources |
| E4. Economic/risk scenario — decide after feasibility evidence | Prepare materiality and risk tradeoffs for the chosen research capital; bind their values before dependent evaluations | Primary research capital, numerical materiality/risk thresholds, personal live limits or execution permission |

E1 and E2 can be approved together or amended individually. E3 and E4 identify later decisions, not requests to repeat existing preferences. Silence and a request to continue are not approvals. Decisions on actual spending and acceptable economic/risk tradeoffs remain the user's; technical implementation choices need not become individual consultations.

## E1 — first-wave spot long/cash scope

| Alternative | Benefits | Costs and limits |
|---|---|---|
| **Conditional spot long/cash first** | Tests C1 and C3 under common capital/accounting rules; fewer borrowing, funding and liquidation assumptions | Does not assess short/derivative/carry constructions or horizons outside this wave; remains exposed to market, custody, liquidity and conversion risks |
| Include derivatives/shorts or several horizons immediately | Directly addresses different mechanisms and access to falling markets | Needs distinct data, collateral/funding/borrow, execution and accounting admission; increases comparison and engineering budgets before those dependencies are resolved |
| Postpone product selection entirely | Avoids committing before feasibility evidence | Leaves costs, reference cash, timing and engine requirements too open to finish a concrete comparison |

**Recommendation:** accept spot long/cash as a provisional research construction, with a pre-results viability check. Operational simplicity reduces assumptions; it does not imply a larger economic opportunity. One admitted horizon controls this wave's search, not the strategy's future frequency. Select it from the mechanism, information clocks and executable costs, not convenience or the best historical return. There is no arbitrary asset count: historical eligibility, delistings and liquidity govern the universe.

“Cash” must be an accessible, explicitly valued USD alternative. USD accounting does not make USDT/USDC dollars or make repeated conversion into bank USD instant or free. If the proposed cash leg or exit timing cannot actually be reproduced, amend or postpone the construction before evaluation. Fully funded exposure avoids borrowing in this proposal; it does not make spot safe or cap losses at an assumed drawdown.

**If deferred:** provider/engine requirements can be compared as scenarios, but no unique execution/cash design can be frozen. C4, C5 and other instruments remain reserves; a better justified mechanism can replace the first-wave construction prospectively with its own accounting and budget.

## E2 — what the 26 specifications buy

The proposed ceiling has an auditable origin, not statistical optimality:

| Base specifications | Count | Purpose |
|---|---:|---|
| Rules and references | 8 | Cash, passive exposure, training-calibrated exposure control, reversal, two C1 memories, C2 volatility policy and its fixed-exposure control |
| Individual C3 information blocks | 6 | Price, activity and volatility, each with two penalties |
| Joint C3 models | 6 | Linear, nonlinear additive and explicit interactions, each with two penalties |
| Refit C3 ablations | 6 | Omit each block and its associated interactions, each with two penalties |
| **Total** | **26** | Specification slots, not total fits, independent observations or 26 primary tests |

| Alternative | Benefits | Costs and limits |
|---|---|---|
| **Retain this conditional ceiling** | Distinguishes persistence, combined information and explicit interaction value with comparable controls | Nested folds, refits, sensitivity cases and inference multiply work; feasibility is still unknown |
| Reduce the questions before evaluation | Lower data/engineering/compute cost; stronger focus | Narrows conclusions. Removing an essential comparator or ablation cannot preserve the associated claim unchanged |
| Add boosting, networks, other inputs or horizons now | Broader function classes and mechanisms | More selection opportunities, data needs and maintenance; no existing evidence makes expansion necessary for this first comparison |

**Recommendation:** retain the comparison structure provisionally and require a complete attempt/resource ledger before launch. It is a ceiling, not a quota to fill. If unaffordable, reduce a question and its claims prospectively; do not keep a complex model while removing the simple comparator needed to interpret it. C3 does not depend on C1 succeeding, and individual inputs need not be profitable. No automatic right to spend unused slots on another model.

The three primary claims are C1, C3-I and C3-X, each requiring both comparator improvement and a separate net-cash gate. The existing proposal controls their family-wise false rejection rate with Holm at 5%, conditional on valid component tests; this is a conventional evidentiary policy, not a 95% probability of future profitability. C2 remains secondary risk analysis. Unrun claims stay in the planned family as p=1; do not recycle their error budget. Approval covers this evidence policy as a package, not a request to choose bootstrap seeds or solver tolerances. The existing 9,999 resamples address simulation granularity, not market sample adequacy; no new numerical rule is introduced here.

C3-X examines only the specified price–volatility and price–activity products. Failure would not reject all interactions, boosting, deep learning or weak conditional information. The same limitation applies to C1's two memories and the admitted horizon. Broader studies need a material question, a new prospective budget and appropriate independent evaluation, not failure-driven searches on the final sample.

**If deferred:** the ledger and power/precision requirements cannot be finalized because the claims remain undecided. If only resource sizing is missing, approve the conditional structure now and leave the full number of fits and calendar open.

## E3 — research and operating resources

| Alternative | Benefits | Costs and limits |
|---|---|---|
| Free sources/resources only, permanently | Avoids direct service charges | May exclude necessary historical constituents, delistings, timestamps or execution evidence; “free” can have substantial engineering cost |
| **Free when fit; paid options reviewed concretely** | Preserves data quality and future opportunity without committing funds now | Requires a later itemized choice; unsuitable free data can mean postponement |
| Approve a broad allowance now | Gives a clear affordability boundary | Without quotations, coverage and engine sizing it does not establish what can be delivered or justify expenditure |

**Recommendation:** apply the second policy, already specified by the user; it needs no new permission. Separate (a) historical acquisition/research and licence rights, (b) development, validation and compute, and (c) recurring feeds, hosting, maintenance and inference. Existing personal infrastructure is the starting point, not proof that research is costless or that it can handle all workloads. Estimate storage, fits, runtime and engineering effort after source/engine sizing. An estimate must state assumptions and uncertainty; do not infer a spending budget from reference trading capital.

A later proposal should show a fit-for-purpose free route where available, a paid route only if it resolves a material limitation, and a postpone/narrow route. Show quotations/licence scope, delivery/quality uncertainty, one-off and recurring USD costs, what each option enables, and its stopping limit. No provider is approved, no quote invented and no financial dataset is acquired in this review. An affordability ceiling the user already knows can guide that comparison, but is not needed for the current design review and is not permission to spend it.

The monetary budget and the statistical search budget are separate. Cheap compute does not justify unlimited combinations. Total fits, sensitivity runs, elapsed work and storage still require a finite ceiling, even on free infrastructure. Sunk research expenditure must not justify continuing an unsupported hypothesis.

**If deferred:** current documentary work can conclude, but no paid resource or full future experimental workload is admitted. Lack of a suitable free route must be reported, not patched with fabricated data assumptions.

## E4 — capital, materiality and risk

### Reference capital: choose the primary amount after feasibility evidence

The user's USD 1,000/5,000/10,000 scenarios remain sensitivity cases, not a range restriction or three chances to choose the most profitable outcome. Alternatives are to nominate one now, select one after feasibility evidence, or report normalized returns alone. Choosing now is simpler but may be infeasible; normalized returns aid comparison but cannot establish minimum-order, fixed-cost or capacity viability.

**Recommendation:** select the primary research capital after minimum sizes, attainable fees, conversion/cash costs and capacity are documented, and before performance-based selection. The user chooses the relevant economic scenario from that dossier; neither the midpoint nor the model's best capital is a default. For annual recurring fixed cost F and capital K, F/K describes one break-even burden; minimum orders and market impact mean returns do not generally scale linearly with K. A materially different capital requirement may justify a separately budgeted reserve. Actual funded capital can remain undecided.

**If deferred:** the monetary value of improvement and operational feasibility remain conditional; numerical economic margins and sample-precision targets cannot be fully bound.

### Economic materiality: evidence of a gain versus a worthwhile gain

| Alternative | Implication |
|---|---|
| Positive net effect only (zero materiality margin) | Valid question about a gain after modeled costs, but even convincing evidence may be too small to justify complexity, uncertainty or resources |
| **A prospectively justified minimum net effect** | Tests an improvement worth investigating further; requires an explicit user value judgment informed by costs, capital and effort; detecting it may need more data |
| Several unranked thresholds or the best capital after outcomes | Does not produce one stable acceptance decision and invites retrospective selection; do not adopt |

Recommend the second policy without inventing its value. Preserve both the incremental margin over the appropriate comparator and the absolute margin over accessible cash. Express each in USD and consistent interval returns for the primary capital; annualized summaries must state their conversion. Set them before dependent evaluations, along with development/validation selection rules. A predictive metric or statistical significance alone is insufficient, and a less negative model is not economically successful.

Modeled recurring execution and operation costs are deducted once. The materiality margin is the additional benefit required after those costs; cost-model uncertainty must be shown separately rather than counted twice. One-off acquisition/development costs belong in transparent project-payback analysis. Statistical sample adequacy constrains what can be learned: if data cannot distinguish the economically relevant effect, narrow the claim, obtain separately authorized evidence or conclude inconclusive. Do not lower the economic bar merely to make a result detectable. No upper return ceiling is proposed.

**If deferred:** comparative mechanisms can be documented, but neither “economically worthwhile” nor the required precision can be certified. A zero margin must not silently fill the gap.

### Risk: research scenarios and C2's tradeoff, not personal live limits

Possible primary downside objectives have different limitations: downside deviation describes repeated shortfalls but is not an extreme-loss limit; expected shortfall targets tail losses but needs adequate tail information; maximum drawdown captures a path-dependent loss but is particularly sample/regime dependent. Report relevant complementary measures; do not optimize the one that gives the best story or adopt a universal Sharpe, drawdown or trade-count threshold.

**Recommendation:** retain the already accepted secondary role of C2, comparing risk against its training-calibrated fixed-exposure control, with an explicit permitted return sacrifice. Select the primary risk functional from the economic objective and whether the available sample can estimate it; then approve the risk/return tradeoff and research exposure/loss scenarios before evaluation. Risk estimates and stress scenarios describe uncertainty, not guaranteed maximum loss. Merely reducing exposure or observing a smaller historical drawdown does not establish superior risk management.

Binding a research scenario now as a permanent personal tolerance would be premature. Conversely, leaving research risk unconstrained until seeing returns would undermine comparability. Personal live drawdown tolerance may remain open because no capital is being deployed; research risk constraints must be frozen before their dependent evaluations. Under this proposal no risk preference authorizes leverage or live deployment.

**If deferred:** C2 cannot support an acceptance decision, and candidate feasibility gates remain incomplete. Describe scenarios as unresolved instead of inventing a personal risk limit.

## Evidence-dependent decisions and responsibility

After approval of principles, prepare **one consolidated feasibility dossier**, without a market run. Some evidence can come from public contractual documentation; actual coverage, sample quality, engine compatibility and calibration need separately authorized source access or technical work. Do not treat this review as that authorization.

| Missing evidence | Technical responsibility | User decision when concrete |
|---|---|---|
| Provider/licence, historical constituents/events, availability and quality | Compare apt coverage and uncertainties; distinguish advertised fields from audited data | Approve any acquisition/spend or material narrowing; no permanent production exchange needed |
| Engine, order minimums, fees, cash route, delay, capacity | Demonstrate product/accounting compatibility and justify costs; current synthetic harness is insufficient | Review resulting product/horizon constraints and economically viable reference capital |
| Calendar, dependence, independent support, timing and total workload | Propose exact partitions, precision requirements, parameters, attempt count and resource ceilings; preserve inaccessible final data | Approve a materially changed scope or resource commitment; no separate consultation on each technical value |
| Costed benefit/risk scenarios | Present net USD implications, uncertainty, primary risk objective and return sacrifice, without choosing by candidate outcomes | Choose primary capital, economic margins and research risk tradeoff as one coherent scenario |
| Frozen bundle, implementation evidence, holdout custody | Resolve all required bindings and technical checks; document the limits of personal-host custody | Accept the final preregistration and, only if desired, separately authorize the exact next acquisition/technical/execution scope |

The monetary threshold, reference capital and acceptable risk sacrifice are not delegated to an optimizer. Exact provider/adapter choices, timestamp rules, solver tolerances, seeds and other technical details can be resolved and registered by the team inside a later authorized scope. Escalate only a material scientific change, cost, loss/exposure choice, irreducible uncertainty that changes the decision, or permission change. No credential request is necessary.

## Bounded wave, open research programme

Keep derivatives, short exposure, other markets, C4/C5, news/on-chain information, richer ML/DL and different horizons eligible for later consideration. Reopening requires a specific mechanism or information gain, changed access/data/resources or other material evidence, an explicit comparison and finite budget. A negative first result alone does not justify indefinite expansion, and an inconclusive narrow test does not disprove the broader family. Preserve rejected/negative outcomes and the reason for reconsideration.

Any revision is prospective and versioned. Exposure to development, validation or final results determines what can still count as independent evidence; a new document cannot make reused final data unseen. No automatic reserve promotion, horizon scan or permanent exclusion follows from approval of this first wave.

**Suggested approval scope now:** E1 and E2 as conditional methodological design choices. Apply the existing resource preferences and defer E3's concrete commitment and E4's capital/materiality/risk values to the consolidated dossier. This would not close IV unconditionally, authorize acquisition or spending, activate Phase V, or change the synthetic application. Those boundaries remain unchanged until the user expressly approves the relevant concrete next scope.
