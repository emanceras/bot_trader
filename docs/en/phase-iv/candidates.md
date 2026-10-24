# Candidate comparison protocol

Document ID: IV-CAND-001 · Version: 1 · Updated: 2026-10-24 · Language: en (canonical).

Translation: [Spanish](../../es/phase-iv/candidates.md), synchronized with IV-CAND-001 v1. Read with the [central protocol](protocol.md) and [data/execution admission](data-execution.md). **Methodological design only: no candidate has been implemented, fitted, financially tested or validated by this document.** Phase V remains unauthorized; the current synthetic ledger is not an admitted financial engine.

## 1. Preserved questions and evidence

The accepted [Phase II selection](../../phase-ii/SELECTION.md), [horizon process](../../phase-ii/HORIZONS.md) and original [H-00–H-24](../../../HYPOTHESES.md) remain authoritative. This document narrows a first evaluable wave without rewriting those hypotheses or declaring other constructions impossible.

| Candidate | Role / estimand | Existing evidence and contrary findings | Initial disposition |
|---|---|---|---|
| C1 / H-01 | Incremental net economic value of temporal persistence over passive exposure with comparable capital/risk | DIR-001 supports conditional persistence; DIR-006 contains adverse BTC temporal test results; DIR-010 and CTR-01 limit generality. [Directional synthesis](../../research/directional.md) | Primary; no requirement that momentum beat all future mechanisms |
| C2 / H-06 | Risk/utility change from causal volatility scaling, with predictive signal held fixed | RP-01 concerns traditional markets, not a crypto replication; PORT-04 and risk studies contain exceptions. [Risk synthesis](../../research/risk-portfolio.md), [portfolio follow-up](../../research/portfolio-followup.md) | Secondary, not an independent alpha claim |
| C3-I / reference within C3 | Value of combined information relative to individual information blocks | ML-06 has favorable and negative net cases; IX-01 concerns equities, not crypto proof. [ML synthesis](../../research/ml-execution.md), [interaction evidence](../../research/evidence-variable-interactions.md) | Primary comparison; an additive improvement alone does not reject H-24 |
| C3-X / H-11/H-24 | Increment from specified interactions over a nonlinear additive model with identical information | Same evidence; predictive improvement and portfolio utility differ, costs and selection remain material | Primary; C1 success and profitable individual inputs are not prerequisites |
| C4 / H-23 | Additional information from other assets after own history and common factors | Descriptive dependencies and unstable links are not executable net alpha. [Cross-asset review](../../research/cross-asset-interactions.md) | Conditional reserve, zero initial search slots |
| C5 / H-08 | Net carry on all committed capital, including collateral and reserve requirements | Contractual flows are identifiable; funding reversal, basis persistence, fees and liquidation can remove the benefit. [Selection C5](../../phase-ii/SELECTION.md) | Conditional reserve, zero initial search slots |

These are reused project assessments, not newly read papers or independent replications. No published return is assigned to bot_trader. H-00 remains a conclusion about the alternatives actually evaluated, not a universal theorem that no opportunity exists.

## 2. Common accounting unit and first-wave scope

The inferential unit is the **paired calendar-time return of the whole account in USD**, after all specified costs, including idle cash and the same committed capital. Asset rows and trades are not independent accounts. Preserve calendar periods with no trades. Compare alternatives over identical admissible dates and information-availability rules; no favorable asset subset or active-only denominator.

For candidate `j`, define `d(j,t) = r(j,t) - r(reference_j,t)`. The primary incremental estimand is `E[d(j,t)]`; require it to exceed a prospectively frozen economic margin `delta_j >= 0`, in the same return interval. Also require net performance above the accessible USD cash alternative by its frozen margin. The central protocol specifies inference, joint decision rules and multiplicity across C1, C3-I and C3-X. Raw arithmetic mean, compounded wealth and risk are distinct; annualization must not change the inferential unit or conceal bankruptcy.

The first-wave **research specification proposal** is a fully funded spot long/flat comparison, one admitted decision horizon `H`, one point-in-time universe rule and one primary execution/capital scenario. This is neither the user's operating preference nor a permanent product/frequency restriction. A different justified product or horizon may replace this proposal **before** admission; it needs its own accounting and budget. Other capital and execution scenarios are prespecified sensitivity cases, not extra chances to select a winner.

Use a fixed decision-cycle calendar with spacing `H` and a **fixed scheduled exit cut-off per cycle**. Entry follows actual availability/latency and is allowed only before the frozen latest-entry cut-off; otherwise abstain. A late entry does not shift the exit to entry+H. Labels cover the remaining executable interval, so their duration may vary. Observation and risk/data clocks remain separate. Failed/partial exits require the frozen carry/exposure and reconciliation policy: decision spacing alone does not guarantee nonoverlapping positions, labels or capital. Do not claim nonoverlap until actual interval checks pass; apply purge and capacity rules to realized intervals. A mechanism requiring overlapping positions or conditional exits must specify ownership and capital before admission rather than silently reuse this first construction.

At each eligible decision, potential asset weight is `1/N_t`, where `N_t` is the causally eligible universe size, not a fixed asset quota. A positive long decision uses that weight; an inactive decision leaves the corresponding allocation in the declared cash vehicle. Never renormalize only profitable/active assets after outcomes. Turnover includes membership changes and drift from price movement; trades execute only after information and complete latency become available. A zero eligible universe follows the frozen unavailable-market policy. Persistent holdings during outages or delisting cannot be valued or closed at an invented executable price.

All transformations, scalers, model fits, selection and comparator scaling use the current training window only. Trading weights use the frozen rule, not out-of-sample volatility or mean exposure. Capital/exposure/risk eligibility constraints are prospective research scenarios, not accepted personal loss limits.

## 3. References and deterministic rules

| ID | Prospective rule | Purpose / boundary |
|---|---|---|
| R0 | Declared accessible USD cash vehicle, with documented accrual, custody and fees; zero nominal accrual is a separate explicit cash scenario if applicable | Required economic hurdle; USDT/USDC cannot be silently treated as USD cash |
| R1 | Fully invested passive `1/N_t` eligible-universe basket with the same universe reconstitution rule and costs | Passive exposure reference; report fixed-instrument buy and hold descriptively where applicable without selecting surviving instruments |
| R2 | Passive R1 exposure multiplied by the selected C1 rule's mean gross exposure **estimated in training**; residual in R0 | Exposes benefit due merely to lower market exposure. This is not a guarantee of equal future volatility/beta; report those differences |
| R3 | Simple temporal reversal: long when the trailing USD log return over `L1` is negative, otherwise cash; zero signal means cash | Sign-reversed control, not independent H-02 selection or tuning |
| C1-L1 / C1-L2 | Long when trailing USD log return over the respective admitted lookback is positive, otherwise cash; zero means cash | Two distinct, mechanism-justified persistence memories, no optimized signal threshold or added volatility policy |
| C2-V | Apply one causal inverse-volatility exposure rule to R1, with a floor and cap, before order planning | Secondary risk question on a fixed base, regardless of C1 profitability |
| C2-F | Constant passive R1 exposure equal to C2-V's training mean gross exposure, residual in R0 | Control for simply holding less risk; no test-period matching |

`L1`, `L2`, `H`, universe-reconstitution timing and all volatility-rule constants require actual values and reasons in the admission manifest before data-dependent evaluation. Two lookbacks are a finite local memory comparison, not evidence that two are optimal or that all other horizons are excluded forever. Existing days/weeks evidence can motivate an initial horizon; it cannot fill missing execution timestamps or establish the best value.

C1's primary reference is R2; R0 is the absolute economic gate. R1 and R3 remain mandatory reported contextual comparisons, not interchangeable primary benchmarks selected after seeing results. Risk constraints and factor/exposure diagnostics prevent interpreting higher leverage/beta as timing skill. Be explicit if a net gain passes the chosen economic test but does not establish structural or factor-adjusted alpha.

For C2-V, use `w_t = min(w_cap, sigma_target / max(sigma_hat_t, sigma_floor))` with `sigma_hat_t` estimated from the fixed trailing memory and available returns; `w_cap <= 1` in this fully funded scenario. The initial estimator is sample realized volatility, not inverse variance or a family of GARCH estimators. Unit conversion, estimation window, insufficient-history handling, floor, target, cap and rebalance timing must be frozen. A cap does not eliminate gap losses.

C2's secondary endpoint is the reduction in the registered downside-risk functional relative to C2-F, alongside a prespecified net-return noninferiority margin and all mandatory risk/cost metrics. Freeze that functional, tail/target convention, uncertainty method and allowed opportunity loss before evaluation. Lower drawdown alone, or fewer invested periods, is not a promotion criterion. No confirmed alpha claim or separate confirmatory budget is created for C2; insufficient effective tail observations yields inconclusive risk evidence.

## 4. C3 comparison ladder and transformation recipe

Initial inputs consist of three **own-asset** blocks, each defined once, using first available complete observations:

- **P — price:** trailing USD log return over `L1`.
- **V — activity:** log ratio of the latest completed decision-cycle USD traded notional to its trailing training-compatible baseline over `L2`. Zero or unavailable notional follows the frozen validity policy; no arbitrary epsilon is tuned to rescue a result. Traded volume is not depth, order imbalance or informed flow.
- **Q — volatility:** realized return volatility over `L2`, computed from the admitted observation interval; it is not a contemporaneous future-period measure.

Precise aggregation, token/quote conversions, minimum valid observations, denominator handling and baseline estimator belong in the manifest. Do not optimize several definitions of each block under one feature name. Other funding, on-chain, news or cross-asset blocks are not included automatically. A variable need not be independently profitable or individually significant; invalid timing/semantics is a reason to exclude it, not an unfavorable univariate P&L.

Fit a pooled shared-coefficient model across the eligible historical panel, with each calendar date carrying total weight one and equal conditional weights across eligible assets. No asset-ID feature, universe derived from today's listings or target-date cross-asset return enters the model. Pooling past training observations shares estimation information; C4's lagged other-asset predictors are a separate question. Split and resample whole dates jointly across assets.

Target `y(i,t)` is the USD forward excess return relative to declared cash over the executable remainder of the scheduled cycle, from the first eligible entry after availability/latency to the fixed exit cut-off; `H` is the decision spacing, not an extra holding period added after a late entry. Actual unfilled exits follow the frozen reconciliation/label-validity policy. Target construction cannot capture a price move before receiving the signal. Predictions are statistical outputs; the economic account simulation separately models quotes, order restrictions, fills, costs and cash. Never deduct execution costs twice by both redefining a label and subtracting the same cost from the ledger.

Before each fit, center/scale valid training inputs using training-only statistics. Specify zero-variance handling and out-of-support behavior; initial rule uses no result-selected winsorization or imputation. Fit finite-dimensional natural cubic-spline main effects with training quartiles as internal knots, training range boundaries and explicit outside-range continuation. Rank-deficient bases are reduced deterministically and recorded. Center spline bases on training; standardize penalized design columns using training statistics, do not penalize the intercept. Exact package/solver/basis convention must be pinned before implementation.

| Step | Model / feature set | What it identifies |
|---|---|---|
| S-P, S-V, S-Q | One block at a time, nonlinear additive univariate model, each with the same two positive penalty levels | Individual information controls; no marginal-profitability filter |
| J-L | Regularized joint linear model on P,V,Q | Simple combined baseline; a nonlinear model is not assumed superior |
| J-A | Regularized nonlinear additive model `a + fP(P) + fV(V) + fQ(Q)` | Primary combined-information procedure for C3-I and reference for C3-X |
| J-X | Same additive basis plus **two prespecified products**, standardized `P*Q` and `P*V`, with the same regularization convention | Persistence conditional on risk/activity; no all-pairs/generic deep interaction search |
| A-minus-P / V / Q | Refit J-X after removing the named block and every interaction containing it; repeat training/selection with remaining inputs | Contribution by ablation; neither zeroing an input in a trained model nor importance/SHAP replaces refitting |

Fit penalized squared-error regression. Freeze two positive penalty values, objective normalization and numerical tolerances before financial evaluation; they are shared across corresponding controls and J-A/J-X. Equal counts do not make model capacity identical: record effective degrees of freedom and compute. Knot quantiles are an ex-ante engineering choice for a small smooth comparator, not an empirically optimal crypto architecture. No testing alternative knot counts, penalties, scalers, losses or product lists outside the registry.

All forecasts pass through one frozen prediction-to-position map, including entry/exit/no-trade treatment, cost allowance, risk/capital cap and latency. Initial proposal: at each cycle, long if predicted excess return exceeds the prospectively specified round-trip cost allowance plus entry hurdle, otherwise cash. The hurdle is derived from the economic/cost policy before observing results and is not a searched probability threshold. C3 comparisons use identical mapping; held-position cost differs from opening a new position and must be handled explicitly in the frozen map. If the simple cycle map is economically inappropriate, amend it before launch and charge the amended comparison to the budget.

## 5. Selection, claims and outcomes

Within each allowed training window, the nested inner walk-forward procedure selects only among the registered alternatives, maximizing mean **paired net USD return difference**, subject first to the same data, execution and risk eligibility rules. The inner split schedule, ranking precision and tie rule are frozen. Ties use lower model complexity, then stable configuration ID; no informal preference for the user's proposed technique. A risk-ineligible configuration cannot win on return. Outer validation evaluates the whole frozen selection/refitting procedure and cannot be used to retune it. For every C3 penalty/block choice, the inner ranking reference is the same R0 cash policy on the same inner evaluation calendar; joint-versus-individual and interaction-versus-additive claims are assessed only in the outer/held-out evaluations. For C1, each lookback ranks against its own fold-local R2, calibrated from that inner training window only. Neither inner assessment exposure nor outer/final exposure enters comparator calibration; C2-F follows the same training-only rule.

- **C1:** select L1 or L2 within training; build R2 from that selected rule's training exposure. Test economic increment against R2 and the separate cash gate.
- **C3-I:** select J-A's penalty in training; select the strongest eligible individual block procedure S-P/S-V/S-Q in training. Compare their frozen policies on identical dates, cash/execution conventions and risk limits. Selecting the individual reference is part of the procedure and its budget; never choose the easiest reference in the final sample.
- **C3-X:** compare training-selected J-X and J-A at identical inputs, dates, information clocks, policy mapping and two-penalty search opportunity. C3-X may be tested even if C3-I is inconclusive: a pure conditional effect need not have profitable marginal signals. Each economic claim still requires the cash gate.

For each primary claim the null is **increment no greater than its registered economic margin OR failure to exceed the registered cash margin**. Both components must pass; the central protocol uses the intersection-union maximum component p-value and then Holm control across the three primary claims. Report confidence intervals and uncertainty, not only pass/fail. Predictive loss differences are secondary diagnostic estimands; no economic conclusion follows from lower MSE alone.

C3-I favorable / C3-X unfavorable supports a simpler combined-information procedure, not interaction superiority. C3-X favorable is conditional evidence about the tested function class and execution policy, not causal discovery or proof that all interactions generalize. If combined policies remain economically negative, their predictive or relative improvement does not justify deploying them. A negative/inconclusive result is retained even when another branch succeeds.

Distinguish combination of **inputs** from diversification of **strategy P&L**. With fixed nonnegative weights summing to one and additive costs, strategies whose true net means are all negative still have a negative weighted mean. Conditional predictors, time-varying policies, netting and shared-capital rules change the question and require their own hypothesis and accounting. None is inferred from this C3 comparison.

## 6. Finite search envelope and stop rules

The first wave has **26 unique base configuration slots**, for one admitted horizon/universe/primary execution-capital scenario:

| Group | Count | Enumeration |
|---|---:|---|
| Deterministic references and C1/C2 rules | 8 | R0, R1, R2, R3, C1-L1, C1-L2, C2-V, C2-F |
| Individual C3 blocks | 6 | S-P/S-V/S-Q × two penalties |
| Joint linear/additive/interaction | 6 | J-L/J-A/J-X × two penalties |
| Refit block ablations | 6 | Three omissions × two penalties |
| **Total** | **26** | Finite initial design, not 26 independent tests or a success probability |

This ceiling is derived from required comparisons and ablations, not optimized to a result. It does **not** bound total fits until outer/inner folds, final refit, seeds, scenarios and sensitivity matrix are enumerated. The admission manifest must compute the complete planned fit/evaluation count and CPU/time/storage budget before launch. Seeds are deterministic engineering controls; no picking a favorable seed. Bootstrap inference is budgeted separately by the central protocol.

Count every manual alternative, preprocessing choice, discarded horizon/universe, failed fit and amendment. Identical retries for infrastructure failure retain attempt history; data-informed changes are new variants. Diagnostic stress/neighboring-window cases must be named and bounded before results and cannot replace the primary scenario. Report their failures; do not select the stress scenario under which a candidate survives.

Stop a branch for unusable point-in-time data, unavailable execution/margin, invalid inference, resource exhaustion or failure of the frozen economic/risk gates. Data failure means unevaluable; valid adverse evidence means the tested construction lacks sufficient support. Neither proves the whole family impossible. Do not add boosting, a network, another horizon or another asset set to rescue the final result. A material amendment needs a new prospective version, budget and independent evaluation treatment.

## 7. Reserved comparisons and launch dependencies

C4's future ladder is own history → own history plus common factors → the same inputs plus prespecified lagged other-asset blocks. Estimate factor loadings, membership, lags and any graph inside training; exclude target contamination and stale-price artifacts, synchronize shared dates and test executable delay. Do not enumerate all directed pairs. Its primary null separates predictive increment from net economic increment. Promotion requires a bounded replacement/additional protocol and does not inherit unused C3 slots automatically.

C5 requires contract-level spot/derivative prices, contemporaneously known funding, actual settlement rules, all collateral/reserves/borrow, accessible cash yield, transfer constraints and margin/liquidation treatment. Compare USD account return on **total committed capital**, not only one leg or posted margin. An anticipated funding payment is not its eventual realized rate, and a futures basis need not converge at the assumed exit. Both legs, funding reversals, gap/margin stress and counterparty concentration must be represented before admission. Neither this protocol nor research access authorizes leverage or actual derivatives operation.

Before requesting a launchable Phase V scope, resolve and freeze: the admitted product/source/universe and coverage; `H/L1/L2` and all clocks; exact split and final interval; price/volume/volatility definitions; two penalties and spline/solver convention; prediction-to-position map; C2 risk endpoint/constants and noninferiority margin; research exposure constraints; USD cash/conversion rules; complete fees/fill/latency/capacity assumptions; economic margins; full fit/sensitivity budget; technical engine/accounting validation; immutable manifest IDs/hashes and responsible approvals. Unfilled fields block execution. Real operating capital, a final production venue and personal drawdown tolerance can remain separate until their dependent work.

No numerical dates, fees, profitable thresholds or accepted vendor are invented here. This is a completed comparison design with explicit instantiation dependencies, not a sealed financial preregistration or permission to execute it.
