# E3/E4 — proposed resource and economic decisions

Document ID IV-E34-001 · Revision 1 · 2026-11-16 · English canonical. [Español](../../es/phase-iv/economics.md).

**Proposal for approval, not an approved budget or financial authorization.** Based on `d1abdde` and the existing [protocol](protocol.md), [candidates](candidates.md), [staged amendment](staged-amendment.md) and [freeze template](../../phase-iv/freeze-template.json). Those scientific documents and their null bindings remain unchanged. E1/E2, the 26 specifications, three primary claims, Holm, 9,999 bootstrap replications and protected holdout are not reopened. This is a documentary decision package, not another infrastructure project.

## 1. Recommended E3 package

**Start with free suitable data and existing local computing. Propose a USD 400 total incremental cash ceiling for the first bounded wave, not a target to spend.** Paid data, GPU, paid LLM inference and permanent hosting are not initial requirements. This ceiling is independent of hypothetical trading capital. Approving it would not authorize purchases, downloads, implementation or D/U/V/F execution without their separate concrete scope.

| Coherent resource option | Cash and benefit | Drawback / recommendation |
|---|---|---|
| Strict existing-resource route | USD 0 new vendor/cloud subscriptions; existing machine/storage and free suitable archives | Electricity, existing-plan allocation and unpaid work are not zero economic costs. Stop if local resources or data are inadequate. An alternative if no cash contingency is desired. |
| **Local first, bounded fallback** | **USD 400 maximum incremental research cash**, initially USD 0 vendor/cloud commitment; local work first, itemized fallback only if a measured constraint justifies it | Recommended: preserves a practical escape from local capacity limits without buying premium data speculatively. Every purchase still needs a concrete quote/scope and explicit permission; no automatic renewal. |
| Premium historical-data route | A paid bundle only for a demonstrated missing field/vintage/coverage right | Not recommended now. Existing advertised Tardis Spot Solo `$900/month` and CoinAPI Startup `$79/month` are not comparable project quotations, verified USD/tax totals or complete-history licences. Obtain an exact narrow quote before proposing any budget increase. |

**Why USD 400:** the only new external check was the official static [AWS Lightsail pricing page](https://aws.amazon.com/lightsail/pricing/), not an exchange connection. It lists Linux/public-IPv4 **16 GB RAM, 4 vCPU, 320 GB SSD at USD 84/month**, and snapshots at **USD 0.05/GB-month** [E34-PRICE-01]. A fallback of at most three billed months plus at most 320 GB of billed snapshot storage is `3 × (84 + 320 × 0.05) = USD 300` before tax. A **conditional 21% VAT planning scenario** gives USD 363, leaving USD 37 within the proposed ceiling. This is not a tax determination or a promise about the invoice. Region, FX/payment charges, actual tax, backup retention, transfer allowances/overages and total invoice must fit the ceiling before activation. Do not rely on a free trial. Burstable advertised vCPUs do not guarantee sustained throughput. Three billed months limit a possible service purchase, **not historical coverage or the statistical duration of V/F**; preserve licensed evidence in approved durable storage before decommissioning, with retention costs included rather than silently discarded.

### Needed data and provider choice

| Need | First route and necessary qualification |
|---|---|
| C1 prices and C3 P/V/Q blocks | Prefer a **single admitted venue's historical spot trades**, with native price, quantity, exact time and source version. Archive/member/row identity preserves provenance; an absent exchange trade ID remains absent and limits duplicate verification. Build closed bars and exact `Σ(price × quantity)` activity. Kraken's downloadable archive is the first candidate because its schema/streaming path has been tested and no access fee was charged for the prior objects. This does not select Kraken permanently or certify a complete research panel. |
| USD valuation and tradable universe | Start by assessing historically eligible **USD-quoted pairs** of that venue, including inactive/delisted instruments and token changes. No fixed number of assets or current-survivor list. Other quotes need causal FX/stablecoin valuation and actual conversion costs; the BTC/EUR pilot does not admit a USD financial universe. |
| Metadata and exclusions | Listing/delisting/halts/migrations, units and historically effective minimums/precision, fees and availability must be documented. First/last trade is not a listing notice or supported exit. Unknown terminal values cannot be deleted or filled at a convenient last price. |
| Execution evidence | Trades/OHLC are not observed bid/ask or depth. The first closed-bar/market-order offline contract may use explicitly modeled spread/slippage/latency/capacity only after a justified prospective cost envelope is bound. If a conclusion depends on unmeasured tight spreads or fast execution, postpone that claim or obtain a separately approved quote/history bundle. Five minutes of BTC/EUR BBO cannot calibrate every asset, year or regime. |
| Independent checks / fallback | Reuse existing Kraken OHLCVT for structural comparison; do not acquire all redundant bar resolutions automatically. Binance's explicit quote-volume fields are an alternative conditional on USD conversion, rights and historical membership; its examined data terms do not guarantee production use. Coinbase candles alone do not supply the verified complete exact-notional panel C3 needs. Tardis/CoinAPI remain targeted reserves, not additional feeds to buy now. |

Use the **earliest reliable, legally usable history per instrument**, across scientifically useful cycles, through an exact frozen release cutoff. No arbitrary year cap; no automatic open-ended acquisition either. The next acquisition request must identify objects/versions, bytes, purpose, rights and a finite coverage manifest. Preserve source vintages and expand in authorized tranches. The exposed Q3 QA material and November pilot remain recorded exposure, never relabeled pristine holdout. Historical disappearance coverage and suitable later independent data are still unproved. Free data can be rejected; missing essential C3 notional cannot be replaced with `close × volume` without a scientific amendment.

### Resource envelope and its evidential basis

These are **proposed stopping ceilings and effort allocations**, not measured requirements, completion promises or prescribed fold counts:

| Resource | Proposed first-wave envelope |
|---|---|
| Human/engineering effort | **80 hours total:** 24 data/cost admission, 32 narrowly scoped financial implementation and statistical/custody checks, 16 D/U analysis, 8 V/F/report review. Reallocate inside the total by recorded decision; no infrastructure expansion or endless repair cycle. |
| Compute | **100 CPU-hours**, at most **4 concurrent vCPU**, **16 GiB RAM** working target; no GPU. Reserve 20 CPU-h for ingestion/technical admission, 60 for D/U, 20 for V/F/inference; exact jobs must fit before launch. The cloud vendor's advertised 16 GB is not a certification of 16 GiB usable memory: check actual available RAM and bound working sets below it. No estimate that current tests prove this workload will fit. |
| Storage | **256 GiB working ceiling** on available local storage: planning allowances 48 raw compressed + 32 normalized/features + 16 temporary + 16 results + 112 backup + 32 headroom. These are caps, not a requirement to materialize every row. OS/runtime space is additional. No claim that the current cloud workspace has this free capacity or an independent backup. |
| Finite attempts | **10,000 estimator-fit attempts**, **5,000 non-fit account/replay evaluation attempts**, **30 inferential batches of the already approved 9,999 draws**. They include failures, sensitivity/calibration/revision work, not only successful jobs. No extra base recipe or inferential claim follows from spare capacity. |

The exact attempt ledger is still required before D: all 26 slots, fold/refit/seed identifiers, three capital cases, mandatory comparators/ablations, stress evaluations, D/U revisions and later V/F must fit these ceilings. For sizing only, `18 × fit-contexts` counts a complete C3 ladder per context: 500 contexts would use 9,000 fits, leaving 1,000 for explicitly registered retry/sensitivity needs. **500 contexts is not a selected fold/refit design.** Inference batches must enumerate shared time resampling, block sensitivities and null calibration, rather than multiplying outcomes opportunistically. If needed precision/admission cannot fit, stop and propose a justified change; do not omit an essential control or quietly shrink inference. A data-informed repair consumes the finite scope and may invalidate its calibration sample.

Measured evidence [E34-MEASURE-01]: the two Q3 archives total **2,172,918,907 compressed bytes** and **8,380,534,210 uncompressed bytes**, containing 116,477,432 trade rows and 36,966,491 bar rows. Streaming structural QA used about **25.5 MiB RSS and 69.04 seconds wall**; it did not fit C3 or validate all numerical rows. Advertised full-history packaging is approximately fourteen 2 GB trade parts and five 2 GB OHLCVT parts, **not verified full-history bytes** [E34-DATA-01/02]. Streaming the necessary trade partitions and retaining compressed originals avoids extracting that entire expansion. Do not extrapolate Q3 compression, activity or timing linearly into a promised full-history footprint.

For a shape calculation only, one million asset-times × 24 numeric columns × 8 bytes is 192 MB; six such working copies are 1.152 GB before indexes, text, engine buffers and runtime. Actual `M=ΣN_t` depends on history/resolution. A huge minute-level universe can exceed the envelope: resource admission must precede processing, not retroactively choose profitable assets or a convenient horizon. The actual pilot's **306.72 s wall / 11.04 s child CPU / 133.2 MiB sampled RSS** proves only that finite data route; its failed-run resource unknowns remain explicit [E34-MEASURE-02/03]. No financial fit throughput has been measured.

### One-off versus recurring economic cost

- **Research acquisition/software:** propose USD 0 vendor fees initially; rights/quality and further acquisition still need permission. One-off outsourced work, extra AI credits or hardware have **no verified quote** and are not silently included as free.
- **Development/research/validation:** the 80-hour effort ceiling is not an invoice estimate. If the operator values an hour at `v USD`, disclose `80v` at the ceiling separately from incremental cash. Meter electricity as `incremental kW × wall-hours × USD/kWh`; power and the user's tariff are unknown. Charge actual incremental expenses to the USD 400 ceiling; re-scope if the total would exceed it.
- **Recurring research storage:** local electricity/backup or the bounded cloud fallback are real costs. Retaining a licensed dataset beyond a service period needs an explicit storage/rights arrangement; no perpetual subscription is approved.
- **Future operation:** not part of this three-month research purchase and not authorized. Use separate sensitivity anchors of USD 0 incremental hosting (not zero total cost), USD 144/year (`12/month`) and USD 528/year (`44/month`) from documented smaller Lightsail tiers. Their suitability for operation has not been tested; no paid feed, labour, tax or transfer fee is implied included. Bind the actual recurring-cost model before D. Each comparator gets its own achievable costs; do not burden cash with a trading server it does not require.

## 2. Recommended E4: hypothetical capital and materiality

**Recommend USD 10,000 as the primary hypothetical research account**, with USD 1,000 and 5,000 retained as prespecified sensitivities. This follows fixed-cost absorption and the dollar value of an incremental improvement, not the best historical return or simply taking the largest offered value. It is not actual funded capital, a minimum project size or a permanent ceiling.

| Hypothetical capital | USD 144/year fixed-cost drag | USD 528/year drag | Recommended cash / comparator surplus in USD/year |
|---|---:|---:|---:|
| 1,000 | 14.40% | 52.80% | 50 / 20 |
| 5,000 | 2.88% | 10.56% | 250 / 100 |
| **10,000** | **1.44%** | **5.28%** | **500 / 200** |

Choosing USD 1,000 best represents small-account feasibility but leaves little dollar surplus for maintenance; USD 5,000 halves the primary capital requirement but doubles fixed-cost drag relative to 10,000. Retain both without selecting a winner after results. Larger capital could require a separate capacity scenario; it is not excluded.

Minimums do **not** yet certify any scenario. At inception, potential allocation is `K/N_t`; subsequently it is `E_t/N_t` against then-current account equity (`E_0=K`), subject to the prescribed signal/exposure rule. Bind enough cash for fee-inclusive minimum quantity/notional and precision, otherwise apply the frozen operability rule. Do not concentrate rejected allocations into winners or assume the same universe at every capital. No current/historical minimum-order API was called in this review. Before D, the actual metadata must show which allocations are feasible at each K; if 10,000 cannot support the declared universe, return the concrete incompatibility rather than silently changing K/universe.

### Proposed minimum economic effects (not forecasts)

| Coherent hurdle option | Above accessible cash | Above the specified comparator | Extra USD/year at K=10,000; consequence |
|---|---:|---:|---|
| Lower materiality | 3 percentage points | 1 percentage point | 300 / 100; accepts less dollar benefit for complexity; lowers the economic hurdle, without removing uncertainty requirements |
| **Recommended** | **5 percentage points** | **2 percentage points for each primary claim** | **500 / 200**; a modest but explicit required benefit, independent of published backtest profits |
| Higher required benefit | 8 percentage points | 3 percentage points | 800 / 300; rejects more small advantages, does not make large effects likely or forbid research on them |

These are transparent **reservation-value proposals for the user's approval**, not empirical optima, confidence levels or expected returns. Recommendation: require an additional USD 500 over cash and USD 200 over the appropriate comparator each year at the primary capital, **after** all modeled recurring execution/operation costs. USD 200 is the minimum surplus accepted for added complexity/uncertainty; whether it compensates the user's future time is a value judgment. A USD 400 one-off research outlay equals two years of that comparator-surplus threshold (four at K=5,000, twenty at K=1,000), **a simple payback illustration, not a promised recovery period**. Record research labour and one-off spending separately; do not subtract them again inside recurring net returns or lower the hurdle because the project has sunk costs.

Apply the same prospective 2-point increment to C1 versus R2, C3-I versus its training-selected individual-block reference, and C3-X versus J-A; retain each separate cash gate. All actual fees, spread, slippage, conversion, capacity and realistic recurring costs are deducted once first. Do not subsidize complex models with cash/comparator costs they do not incur. No return ceiling is imposed.

The approved estimand is an **arithmetic mean paired simple-return difference**, not CAGR. With `m` equally spaced reporting intervals per year fixed before D, propose `δ_cash=0.05/m` and `δ_increment=0.02/m`. Annual figures above are arithmetic annual equivalents. For calendar-day reporting only as an illustration (`m=365`), these are 1.369863 and 0.547945 basis points per day. This does not select the reporting interval, horizon or imply independent days. Report compounded wealth/CAGR separately. Do not use `(1+a)^(1/m)-1` to change the approved estimand. Return uncertainty/valid component tests, `max(p_gain,p_cash)` and Holm across the original three claims remain mandatory; exceeding a point threshold alone is not acceptance.

**Cash:** recommend assessing an actually accessible, liquid nominal-USD balance first. Accrual is its documented attainable rate net of custody/transfer costs, not an invented Treasury yield. Zero yield is permissible only for an explicitly unremunerated USD vehicle; it is not a default for missing data or a way to soften the cash gate. USDT/USDC are not USD and bank transfers are not instantaneous. Exact cash vehicle, historical accrual, conversion and Spain/product eligibility remain pre-D bindings; approve the surplus **over** that benchmark now without inventing its level.

**Fee sensitivity matters more than small-account minimums alone.** The preserved October official-page snapshot shows an initial taker rate of **0.80% per side**, unconfirmed for this user's account/jurisdiction or historical periods [E34-FEE-01]. At that documentary scenario, fees are `0.008 × one-way turnover`: ten times capital traded in a year costs approximately 8% of capital before spread/impact, at constant notional/tariff; an equal-notional round trip costs approximately 1.6%. This is neither the selected fee schedule nor a financial backtest. No future-volume discount, maker fill or low fee is assumed. Larger K dilutes fixed costs, **not proportional fees**. Exact attainable/historical tariffs and liquidity can still make a construction unevaluable or unattractive, regardless of these proposed margins.

## 3. Research risk and C2

Keep fully funded spot long/cash, no borrowing/shorting, and **gross exposure at most 100% of committed capital**, with fee reserves and the existing `1/N_t` allocation. These are first-wave controls already inherent in E1, not permanent restrictions or leverage permission.

| Research drawdown screen | Loss at K=10,000 from its starting peak | Gain needed to recover that percentage loss | Choice |
|---|---:|---:|---|
| 20% | USD 2,000 | 25.00% | Stricter feasibility requirement; more constructions may be ineligible |
| **30%** | **USD 3,000** | **42.86%** | Recommended primary research screen, reflecting a materially risky crypto study rather than a claim of safe trading |
| 40% | USD 4,000 | 66.67% | More permissive alternative; larger loss exposure is the cost, not evidence of higher return |

Thirty percent is a **proposed loss-tolerance scenario**, not a data-derived safe limit or the user's personal tolerance. The table's dollars refer to a USD 10,000 peak; a later higher peak changes the dollar loss. In the primary scenario, a candidate breaching 30% observed maximum drawdown on an applicable evaluation is risk-ineligible under the frozen rule; retain its full results. Report 20%/40% eligibility sensitivities without using a looser threshold to rescue the primary decision. This is an evaluation screen, **not a newly added stop-loss trading rule** or a guarantee that future losses cannot exceed it. Report drawdown duration, expected shortfall with uncertainty, concentration, execution/custody incidents and stress outcomes. Fully funded positions and exchange cash can still suffer extreme or total loss. Freeze named adverse liquidity/gap/delisting/counterparty scenarios before D; unsupported liquidation/recovery prices make the relevant conclusion inconclusive, not safe.

**C2 recommendation:** use cash-relative downside deviation at the common reporting interval,
`ρ(S)=sqrt(E[min(r(S,t)-r(cash,t),0)^2])`, as its primary secondary-risk functional. It uses all dates and avoids requiring a sufficiently large extreme-tail sample merely to define the main comparison. It does not replace tail/drawdown reporting or prove control of rare losses. Compare C2-V with its training-exposure-matched C2-F, with R1 unchanged.

| C2 package | Required downside-deviation reduction versus C2-F | Largest permitted annual arithmetic net-return sacrifice | Implication at K=10,000 |
|---|---:|---:|---|
| No-sacrifice alternative | 10% | 0 points | Risk reduction must retain all comparator return; may be inconclusive |
| **Recommended compromise** | **10%** | **1 percentage point** | At most USD 100/year sacrificed for a 10% reduction in downside deviation (19% in its square) |
| Stronger risk preference | 20% | 2 percentage points | At most USD 200/year for greater risk reduction; a different preference, not a predicted outcome |

These preferences are chosen before results, not optimized risk targets. The recommended requirements are `ρ(C2-V) ≤ 0.90ρ(C2-F)` and `E[r(C2-V)-r(C2-F)] ≥ -0.01/m`. Evaluate paired, dependent uncertainty for **both**, using the registered secondary-inference method; if uncertainty cannot support the joint conclusion, call it inconclusive. A zero/near-zero comparator downside makes a relative reduction uninformative; do not divide by zero or invent benefit. Exact applicability/tolerance/uncertainty rules, volatility memory/target/floor and timing must be frozen before their dependent evaluation; they cannot be tuned using V/F. C2 remains secondary, with no fourth primary alpha claim, promotion to funded trading, or automatic allocation. Less invested time or a smaller historical drawdown alone does not satisfy it.

## 4. What can be approved now and what remains

Three grouped decisions suffice:

1. **E3:** local-first/free-when-fit route, USD 400 incremental cash ceiling, 80-hour effort / 100 CPU-hour / 256 GiB envelope and finite attempt caps. Purchases/acquisition and financial execution remain separately gated. Strict-zero-new-spend is the alternative; premium data needs a concrete material justification and revised quote.
2. **E4 capital/materiality:** USD 10,000 hypothetical primary account, 1,000/5,000 sensitivities, annual arithmetic surplus of 5 points over accessible cash and 2 points over each prescribed primary comparator, after costs once. User may choose the listed alternatives or modify the reservation values before results.
3. **E4 risk:** 30% research drawdown screen with 20%/40% reported sensitivities; C2 downside reduction of 10% with no more than 1-point return sacrifice. No personal live-loss limit or real investment is approved.

| Timing | Remaining work / approval |
|---|---|
| Before a first financial implementation scope | User confirmation/modification of this proposal; a narrow scope for the offline financial runner using the already studied engine boundary and causal closed-bar/market-order contract. No reopening of engines or general infrastructure. Any synthetic admission/implementation needs its applicable scope; this document implements nothing. |
| **Before D — financial development** | Separate acquisition/use rights and exact source/version/byte/retention manifest; historical identities/rules and USD/cash/cost/capacity admission; one mechanism-justified H and L1/L2, exact recipes/penalties/position map/C2 constants; exact development folds/refits and complete fit/stress/inference ledger within E3; financial accounting/engine adapter and access/custody admission; protected later envelope, prior-exposure record and deterministic split/stop rule. Set desired precision, relevant alternatives and adequacy-planning rule before U outcomes. Explicit Phase V/D authorization remains indispensable. |
| U, only after its financial authorization | Estimate paired dependence/uncertainty from eligible frozen-procedure development evidence, or untouched development calibration if revised. Decide whether available independent support meets the preregistered precision/power requirement. Do not derive precision from structural QA or change economic margins to make them detectable. |
| Before V/F | Freeze exact subdivision by the approved metadata+D/U rule without viewing later values; complete inference/technical/economic/resource bindings, independent custody and explicit stage permissions; F still requires its one-time opening. If an independent envelope cannot be formed, wait/defer under a finite plan, never recycle exposed QA or extend until significant. |

E3/E4 approval would remove important **policy** gaps, not certify source completeness, sample adequacy or unconditional Phase IV closure. Some detailed bindings can be delegated and reviewed as one manifest; they do not each need a new user preference. Real funded capital, personal live tolerance, leverage, production venue, 24/7 service and future ML/DL/news/other markets remain outside this wave and this permission. Stop after this documentary delivery.

## Evidence and limitations

[Directed source ledger](../../phase-iv/economics/sources.json): one new official static cloud-pricing page; prior source hashes and technical receipts reused. No exchange connection, dataset download, financial computation, installation or purchase occurred. The **same hashed Kraken snapshot** contains a Spot table with maker 0.38% and a futures cross-platform comparison with Spot maker 0.40%; both show Spot taker 0.80%. Earlier feasibility prose reported 0.40%: the coexistence of these table contexts does not establish that earlier figure was a transcription error. Preserve the discrepancy without rewriting history; only the taker scenario is used, and actual tariffs remain unbound. Provider list prices are not accepted quotes. Effort/resource/risk/materiality proposals are explicitly normative or conditional; none is evidence of profitability.

[Documentary verification](../../phase-iv/economics/verification.json): nine source hashes, planning arithmetic, local links and bilingual tables reviewed; ten scientific/history files unchanged and both published history prefixes preserved. No runtime regression was repeated for this documentation-only change.
