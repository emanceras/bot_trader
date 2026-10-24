# Phase IV — Data, universe, horizons and execution admission

Document ID: IV-DATA-001 · Version: 1 · Updated: 2026-10-24 · Language: en (canonical).

Translation: [Spanish](../../es/phase-iv/data-execution.md), synchronized with IV-DATA-001 v1. This methodological annex addresses ROADMAP IV.1, IV.6, IV.9 and IV.11. It reuses the accepted [feasibility assessment](../../phase-ii/FEASIBILITY.md), [horizon process](../../phase-ii/HORIZONS.md), [access assessment](../../phase-ii/ACCESS.md) and scientific evidence below. Their dated phase/approval statements are historical; the new authorization permits Phase IV methodology only.

**Present state:** specification documented; no market dataset, provider, contract, fee schedule or financial execution engine has passed admission. `ready_to_execute = false`. No historical market data were acquired, no feed was tested and no financial experiment was performed for this annex. A missing binding value below is an explicit blocker, not an invitation to choose it after seeing strategy returns.

## 1. Scope, units and binding record

C1/C3 remain primary, C2 a secondary risk comparison, C4/C5 conditional reserves. Initial spot-without-borrowing is a feasible scenario to assess, not a permanent product restriction or a claim of access. An information source need not be an instrument the system can trade. Spain is the initial jurisdiction; a foreign exchange does not change residence or legal obligations. Product/entity/client accessibility must be checked before treating an opportunity as available to this operator. A legitimately different future jurisdiction is a separate versioned scenario, not a VPN assumption. Historical legal availability and present access are distinct questions.

Before a financial run is admitted, bind a versioned record with the following field names. This is a documentary contract, not an implemented schema or populated dataset manifest. All unresolved fields currently have value `null`; an empty string or fabricated default cannot satisfy admission.

| Field group | Required binding fields | Who/what resolves it before use |
|---|---|---|
| Scope | `protocol_id`, `protocol_version`, `candidate_id`, `product_scenario`, `account_currency`, `jurisdiction_scenario`, `research_only_instruments` | Protocol owner; account currency is already **USD**. Actual scenario and instruments need an explicit decision |
| Source | `source_id`, `source_version`, `source_url`, `retrieved_at_utc`, `licence_scope`, `retention_policy`, `acquisition_cost_usd`, `approval_reference`, `raw_manifest_hash`, `coverage_start`, `coverage_end` | Source-admission review and applicable acquisition permission; metadata claim is not actual verified coverage |
| Identity/universe | `instrument_master_version`, `universe_rule_version`, `eligibility_asof_rule`, `venue_entity`, `product_class`, `listing_history_source`, `token_event_policy` | Historical instrument inventory and eligibility specification |
| Clocks/quality | `timestamp_semantics`, `timestamp_precision`, `clock_error_bound`, `availability_policy`, `max_age_by_field`, `gap_policy`, `duplicate_policy`, `correction_policy`, `quality_report_hash` | Time/quality audit, before calculating financial results |
| Execution | `engine_adapter_version`, `order_policy_version`, `fill_model_version`, `fee_schedule_version`, `latency_model_version`, `capacity_rule`, `borrow_margin_policy`, `funding_rule_version`, `usd_conversion_policy`, `cash_return_policy` | Instrument-specific engineering/admission; no assumption that the technical ledger satisfies this requirement |
| Financial binding | `capital_scenarios_usd`, `cost_budget_usd`, `fixed_cost_allocation`, `minimum_economic_effect`, `period_partition_manifest`, `stress_plan_version` | Data-supported protocol instantiation and resource approval; statistical rules reside in the main protocol |

`approval_reference` distinguishes method approval, data acquisition, financial execution and expenses. Filling a record does not grant any of these permissions. Preserve a record's versions, source receipts, amendments and rejected alternatives. Exact calendar boundaries, numerical thresholds, fees and latency assumptions remain unbound until their evidence exists; they must be frozen before dependent selection or evaluation.

## 2. Point-in-time universe and source admission (IV.1)

The unit is **asset identity / contract / venue / pair / interval of existence**, not a ticker string. Preserve quote, settlement and collateral currencies, multiplier, precision, lot/minimum-notional rules and their effective dates. Distinguish a rename from a new asset, a redenomination from a return, and a wrapped claim from its underlying. Chain, contract address or provider identifiers are associated references, not universal identities.

Define at each decision time `t`:

- `U_I(t)`: instruments whose required observations and identity metadata are known by `t`, including possible nontradable predictors. Do not require survival to the study end.
- `U_O(t; K)`: the subset eligible for the selected legal/product scenario, currency conversion, size/precision, funding/borrow if relevant, and accessible liquidity at capital `K`.
- Inclusion uses only lagged information available at `t`: sufficient warm-up, usable coverage, price/volume semantics, spread/depth or a validated capacity proxy, and a frozen selection rule. Declare the update cadence and decision cut-off. No fixed count of coins and no ranking by subsequent returns.

A representative first scope is all historically eligible instruments from one admitted venue/product dataset, with its limitations. A broader multi-venue scope is admitted only if identity, duplicates, clocks, accessible balances and execution can be reconciled. A smaller high-liquidity scope may be defensible under a frozen liquidity rule but cannot be called representative of all crypto. Large/medium/small strata may use lagged liquidity and, only if historically available, supply/capitalization; strata are descriptions, not a retrospective search for the profitable segment. Do not require every asset to have data throughout the full sample: that discards new entrants and failures.

Source admission is specific to **field × instrument × time range × intended use**. First obtain the permission, licensing and cost decision applicable to a later data-quality audit; Phase IV does not itself perform that acquisition. A future audit must inspect raw/derived identity, historical listings and closures, timestamp meaning, units, corrections, missingness, sample reconstruction and integrity. Record acceptance, qualified use or rejection with the affected claim. A publicly documented endpoint, paper citation, current symbol list or checksum alone does not establish historical fitness. Historical tariff/volume-tier rules cannot be reconstructed from today's price page by assumption.

### Missingness, closures and corrections

| Condition | Prespecified treatment |
|---|---|
| Duplicate message/bar | Use provider-scoped event identity plus version/sequence where supplied; exact duplicates are idempotent. Conflicting duplicates remain flagged and block affected calculations until resolved; never pick the more profitable observation |
| Late/corrected record | Preserve original and receipt/revision times. Research reconstruction uses the vintage knowable then; a corrected research view is distinct from what a trader could know |
| Gap or stale observation | Set a quality/availability flag. No synthetic tradable bar, fabricated zero return or silent interpolation. A last-known price may support explicitly provisional valuation under a frozen age limit, but never proves executable liquidity |
| Missing predictor | Apply the frozen missing-input policy fitted only within development, or abstain; do not choose between imputation and exclusion using validation/final results. Report exclusions by cause and candidate |
| Delisting, halt, bankruptcy | Retain the instrument and event. Block new entries when that restriction was knowable; simulate closure only with supported execution/settlement evidence. An unknown recovery is not an exit at the last close, nor automatic zero recovery |
| Unknown terminal position value | Report the unresolved position and economically defensible bounds separately; if it can change the conclusion, classify that evaluation as inconclusive/inadmissible rather than delete the asset |
| Fork, migration, redenomination | Apply a versioned entitlement/unit rule with known announcement/effective/receipt times and actual access conditions. Avoid treating duplicated claims or unit changes as profit |

Candidate comparisons use the same eligible target timestamps and execution conventions wherever the comparison requires common information. Report the full universe and every exclusion, plus a paired common-support comparison; changing support may itself change the estimand. Common support must not become a covert end-of-sample survivor filter. If a candidate needs a shorter history, report that limitation and compare all relevant baselines on that same interval.

## 3. USD accounting and capital

All comparable wealth, returns and costs use USD. USDT, USDC, BTC and other numeraires remain separate instruments. For each asset/liability or cash movement bind the valuation source, quote currency, USD conversion path, available-at time, age limit and fallback/abstention rule. Do not convert an entire history at its final FX rate or assume a stablecoin is always one USD.

Separate marking a balance from actually converting it. Executed conversion incurs its own bid/ask/fee/latency only when performed. A depeg already present in USD valuation is not subtracted again as a separate loss. Derivative equity uses its contractual value/P&L and liabilities; notional exposure is not an asset to add to equity. Collateral accepted in several roles is still counted once. Restricted/reserved capital, balances on different venues, guarantees and operational reserves are included in committed capital; a return on minimum margin alone is not the platform's capital return.

Use `K = 1,000 / 5,000 / 10,000 USD` as the user-requested sensitivity scenarios, not bounds or actual funding decisions. At each `K`, recompute minimum sizes, feasible allocations, fees/tier, capacity and margin rather than scale P&L linearly. If another capital is needed, explain the instrument/resource reason without inferring it from a desired return. Real leverage and personal drawdown limits remain unapproved. No numerical risk sensitivity is a personal acceptance threshold.

Show cash and buy-and-hold benchmarks under the same account, conversion and cost conventions. The base idle-cash convention may be non-interest-bearing USD when accessible in the scenario; otherwise use an explicitly defined accessible cash instrument. Neither Treasury yield nor stablecoin yield is assigned automatically. Cash/benchmark choice is frozen with the scenario. External deposits/withdrawals are separate from investment profit; an identical funded ledger with no external flows is the simplest initial research convention.

## 4. Causal clocks and finite horizon selection (IV.11)

Bind observation resolution, information availability, formation lookback, prediction interval, holding/exit rule, decision/rebalance schedule, model refit cadence, execution delay and operational risk checks separately. A close-of-bar signal is available after that bar, not at its opening or an earlier close. A prediction label must start no earlier than the executable entry specified by the experiment; a diagnostic mid-price target must be explicitly separated from its later trading mapping.

For an input value `x`, select the last **eligible vintage** whose reliable availability/receipt upper bound is no later than the decision cut-off. Transformation availability is at least the maximum input availability plus its computation/receipt delay. Normalize timestamps to UTC while preserving original timezone, DST, precision, clock source and uncertainty. An unknown timestamp stays unknown. A documented conservative availability bound can support a slower question only when it is genuinely supported and precedes the decision; inventing a delay does not repair missing provenance.

For cross-asset/exchange variables use as-of joins, explicit freshness tolerances and common UTC partition boundaries. Do not join nearest timestamps if that selects a later value. A timestamp match does not eliminate different reporting delays, unsynchronized clocks or stale prices. Future factors/normalization/universe/graph fitting use only the permitted training window. Borrowing another asset's contemporaneous future observation across a chronological boundary is leakage.

Use the accepted horizon process in this order:

1. Specify the economic question and information lifetime, reusing the evidence and its contrary findings. C1 has a documented days/weeks motivation; C3's target is justified independently; C2's risk memory is distinct from its rebalance clock. These are starting arguments, not a universal frequency restriction.
2. Check whether source timing/resolution and achievable delay can resolve that question. C4's rapid lead–lag evidence cannot be turned into an hourly signal merely because hourly data are easy. C5's funding schedule is contractual and is not necessarily its holding interval.
3. Bind one principal clock specification per admitted comparison and its justified finite alternatives/sensitivities in the central search ledger. No automatic cross-product of coins, windows, models and frequencies. If two clocks cannot be distinguished before research, both consume the same declared selection budget.
4. Select only inside development and validate the entire selection procedure. Sensitivity neighbours are not replacements for a failed final specification. Reconsider a deferred horizon only for changed data, attainable latency, mechanism evidence or resources, with a prospective amendment and explicit budget.

For fast variants, require the distribution/tail of end-to-end delay, executable prices after receipt and adequate depth/sequence information; an inference-time benchmark alone is insufficient. If measured or conservatively supported delay consumes the purported opportunity, postpone that variant; this is not universal rejection of its mechanism. No calendar durations, frequencies or latency numbers are invented by this annex.

## 5. Execution and cost policy (IV.6)

A future financial engine must pass the relevant contract/adaptor gate from [Phase III architecture](../architecture/engines.md) and [supplement](../architecture/supplement.md). The current synthetic ledger is not that engine. Simulate orders only after information is available and computation, submission and acceptance delays have elapsed. Respect price/size precision, minimum notional, capacity, rejected/partial fills, cancellations and unavailable markets. Unsupported behavior must fail admission, not become a perfect fill.

Choose one explicitly reconciled fill-cost representation for each run:

- **Executable-quote route:** use the bid/ask and accessible depth at the simulated acceptance/fill time, plus separately supported residual impact beyond what that depth already captures. Spread and swept depth are already inside fill price. Add explicit fees and actual financing/cash flows once.
- **Reference-price route:** if adequate quotes are unavailable, start from a clearly defined contemporaneous reference and add an empirically supported spread/liquidity/impact model with uncertainty. Label results conditional on that model. An OHLC bar cannot identify intrabar order priority, stop/limit order sequence or the ability to fill its extrema. If these facts determine the claim, reject that experiment's execution specification rather than assign zero friction.

Signed fill quantities and actual fill prices update cash/inventory; fees and settlement payments update cash. Net trading P&L is change in consistently marked equity minus external cash flows, with those charges already booked. Attribution to spread, timing, impact, adverse selection and fees must reconcile to the same ledger; attribution is not another debit. Terminal liquidation or continued holding has a frozen policy; a mark-to-mid report alone does not prove an executable exit.

| Cost/risk component | Required evidence and treatment |
|---|---|
| Fees/rebates | Versioned effective dates, venue/product and attainable tier, maker/taker status, fee currency and token requirements. Do not grant an institutional rebate or know the full month's future volume at its start |
| Spread/depth/impact | Correct route above, size-dependent capacity, stale quote rejection and bounded participation; reported volume is not guaranteed accessible economic volume |
| Latency/unfilled orders | Receipt-to-decision-to-acceptance-to-fill policy, outages and missed/partial fills. Maker price touch is not a fill; L2 snapshots do not establish queue priority |
| Financing/borrow | Accessible lending rate, accrual convention, available inventory, recalls, rollover and collateral. An instrument requiring unavailable borrow is not admitted |
| Funding | Contract-specific payer/receiver sign, mark/notional base, eligibility and payment time. Estimated, announced and settled rates are distinct: future realized funding cannot enter the earlier entry signal |
| Margin/liquidation | Initial/maintenance rules, haircuts, collateral valuation, funding deductions, liquidation/insurance/default outcomes and joint leg capital. Delta neutrality does not guarantee solvency; end-of-bar marks can miss intrabar liquidation |
| Multiple legs/venues | No atomic hedge or instant transfer assumption. Model legging exposure, prefunding, transfer delays/costs, interruptions and missing state. Full committed capital is the denominator |
| Fixed/research costs | Separate historical-data purchase and development from recurring feeds/inference/hosting/support. Show cash outlay and economic allocation. Never amortize and debit the same purchase in full in the same reported P&L |

Historical and current-accessible-cost scenarios have different meanings. If historical fee vintages cannot be obtained, a current-fee counterfactual may be useful if predeclared, but cannot claim exact historical net returns. If economic conclusions depend on an unidentifiable cost, retain uncertainty or postpone instead of silently imputing the cheapest case. No current venue/tariff is certified here; the regulatory/source reviews are not refreshed provider approvals.

For annual recurring fixed cost `F` and committed capital `K`, `F/K` is the fixed break-even burden before variable frictions. The existing Phase II table contains hypothetical costs, not quotations. Incremental economic value is `ΔΠ_net = ΔΠ_before_incremental_costs − ΔC_variable − ΔF`; do not subtract a cost already included in the first term. A useful predictor may fail this economic comparison; a lower-complexity model may have a lower hurdle, without proving higher gross potential. Evaluate uncertainty, tails and capacity alongside the effect. No maximum possible return is imposed.

## 6. Prespecified stress and impossibility checks

Freeze base assumptions, documented alternatives and uncertainty before examining candidate outcomes. Use the same scenario definitions for paired comparators, allowing actual turnover/size and execution to differ. The following axes define required relevant checks, not a licence for an unlimited Cartesian search:

| Axis | What the binding stress plan must specify |
|---|---|
| Fee/access | Attainable base tier and a worse documented applicable tier; loss of rebates/discount eligibility where relevant |
| Liquidity/capacity | Wider spread, thinner accessible depth and impact uncertainty supported by development-period market properties or explicit structural scenarios; participation/order rejection limits |
| Delay/continuity | Longer receipt/execution delay, stale/missing input, unavailable venue, partial or missed fills; a defined stopping/abstention policy |
| Currency/custody | Depeg/conversion illiquidity, transfer blockage and exposure to issuer/venue loss where material; distinguish observed historical replay from hypothetical loss scenarios |
| Derivatives, if admitted | Negative funding, basis widening, borrow recall, collateral haircut, margin pressure and loss of one hedge leg; do not assume an immediate close is always possible |

Record scenario IDs, construction data, parameter values/ranges, source uncertainty, duration, cross-variable consistency, capital and comparison rule. Calibrate only from permitted development data or independent contractual/engineering evidence, never from the reserved final performance. No universal “double slippage” or guaranteed drawdown limit is adopted. Report all prespecified scenarios, including non-estimable ones; failure can justify economic rejection, conditional use or postponement according to the protocol, not a new search for a favourable stress set.

## 7. News/events gate (IV.9; conditional, not activated)

The textual/news reserves remain deferred. If later admitted, bind `event_id`, `event_group_id`, `instrument_mapping_version`, `publication_time_original`, `publication_timezone`, `publication_precision`, `provider_first_seen_at`, `received_at`, `revision_id`, `revision_available_at`, `content_hash`, `licence_scope`, and a frozen causal clustering rule. Original content, translations, duplicates, edits and later debunking are different vintages. Preserve missing/uncertain times and rights-limited retention; the system cannot promise perpetual storage where the licence requires deletion.

For macro surprise, use the first released value minus a unit-consistent consensus snapshot available before that release; bind its cut-off, contributor definition, version and source. A provider's own forecast is not interchangeable with consensus. ALFRED date vintages alone do not prove intraday reception; a `LastUpdate` field is not necessarily first observation. Current calendars cannot stand in for historically known schedules. Publication, local receipt, decision and fill clocks remain distinct.

Partition all copies/groups and overlapping outcome windows consistently across assets. Causal grouping used by a signal cannot use later text; a conservative offline contamination audit may discover links and invalidate a split, but cannot feed those later links into a historical predictor. Freeze NLP/LLM snapshot, tokenizer, feature extraction, prompts, tools, training/knowledge cut-off known or unknown, latency and inference costs. Chronological splits and anonymization cannot prove absence of pretrained-model contamination. If this cannot be excluded, narrow the retrospective claim and require a separately authorized later prospective evaluation.

Predeclare price-only, calendar-only, text-only and hybrid comparisons with equal eligible information/target/risk/cost/search budgets; include a simple lexical/statistical text reference. Test delay, stale/corrected news and removal of each information block through development-fitted ablations. Separate anticipatory information, reaction to information already released and event-risk reduction; each has a different target and opportunity cost. There is no authority here to acquire the corpus, run model inference or activate the reserve.

## 8. Evidence reused and unresolved admission

This is a methodological synthesis, not a new empirical study or renewed vendor audit. Source identity/access limitations remain in the existing fiches:

| Existing evidence | Decision supported, with limit |
|---|---|
| [Directional evidence](../../research/evidence-directional.md), DIR-001/DIR-006; [horizons](../../phase-ii/HORIZONS.md) | C1 horizon motivation and contrary test findings; no prescribed profitable interval |
| [Execution synthesis](../../research/execution.md), EX-01/02/05 | Accessible fees, depth, queue and latency matter; predictive accuracy and favourable rebates do not certify retail net value |
| [Funding review](../../research/gap-funding.md), FUND-01/02 | Distinguish funding/convergence, known/settled rates and full capital; favourable published results retain omitted-cost/margin limitations |
| [Cross-asset synthesis](../../research/cross-asset-interactions.md) | Synchronization, factors and common-date partitions precede incremental claims; correlation is not tradable lead–lag |
| [News data assessment](../../research/news-data-sources.md), [coverage audit](../../research/coverage-audit.md) | First versions, reception/consensus, licence and optional on-chain/derivative fields need admission; documented products are not tested feeds |
| [Access](../../phase-ii/ACCESS.md), [feasibility](../../phase-ii/FEASIBILITY.md) | Entity/product/residence and USD/full capital require explicit binding; dated source reviews certify no current account/product |

The unresolved decisions are a reference dataset/venue/product and its rights/cost, actual historical coverage and instrument events, executable cost/latency/capacity evidence, capital/resource assumptions and numerical economic-effect threshold, and exact clock/partition bindings. Real capital, personal drawdown tolerance and the eventual trading venue may remain open if they do not affect the narrowly proposed research scenario. They must not be silently inferred from whichever scenario later performs best. Source-quality approval, engine admission and explicit Phase V authorization remain separate gates.
