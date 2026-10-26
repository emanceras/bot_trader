# Phase IV — consolidated feasibility and admission report

Document ID: IV-FEAS-001 · Version: 1 · Date: 2026-10-25 · English canonical. [Spanish](../../es/phase-iv/feasibility.md).

**Status update — 2026-10-26:** D-040 separately authorizes packages A/B. This report preserves the pre-acquisition assessment of 2026-10-25; the [technical audit report](admission.md) records execution, findings and limitations. Its earlier “not authorized/not installed” statements describe that historical assessment. The quarterly sample is not a constraint on future research history or source coverage.

## 1. Decision and actual status

The user approved E1 and E2 from commit `ba6c20b`: provisional fully funded spot long/cash, the conditional ceiling of 26 base specifications, three primary claims, comparator/cash gates and Holm multiplicity control. [Approval record](../../phase-iv/APPROVAL-E1-E2.es.md), D-038. E3 resources and E4 primary capital/materiality/risk remain open. No financial dataset acquisition, experiment, model training, expenditure, prospective paper or live activity is authorized. UX-01–UX-04 remain future work.

**Recommendation:** use existing local infrastructure; prepare a bounded quality audit of Kraken's public quarterly trade/bar archives and an isolated technical assessment of NautilusTrader **1.231.0**. Neither source nor engine is admitted. Binance is an alternative with material currency/licensing restrictions; LEAN direct engine is a fallback with additional integration requirements. Commercial data and cloud remain options for a demonstrated gap, not purchases needed by default.

This is documentary feasibility, not evidence that the wave is economically viable. Three blockers materially affect the recommendation: exact USD traded notional for C3; historical instrument identity/availability and realistic costs; and actual engine/accounting compatibility. A further statistical dependency cannot be settled by documentation or structural QA: precision for candidate-minus-reference returns needs expressly authorized development work. IV remains conditionally open.

| Evidence level | What exists | What it does not establish |
|---|---|---|
| Previously implemented and technically tested | Phase III local synthetic platform and its historical verification | Financial engine, market-quality admission, Windows compatibility or trading performance |
| Public documentation inspected | Official source schemas/limitations, pricing/licensing statements, engine documentation; [receipts](../../phase-iv/feasibility-sources.jsonl) | Actual files' completeness, account-specific tariffs, paid product fitness or implementation correctness |
| Metadata observed | HEAD responses for two archive URLs; PyPI release metadata | Archive contents, decompressed size, wheel installation or runtime tests |
| Proposed checks | Source QA, isolated synthetic engine cases and workload sizing below | No checks have been executed by describing them; no positive financial conclusion |

The [existing research](../../../RESEARCH.md), [Phase II feasibility](../../phase-ii/FEASIBILITY.md), [access review](../../phase-ii/ACCESS.md), [engine review](../architecture/engines.md), IV protocol and adverse findings were reused. No broad literature review or candidate selection was repeated. The academic corpus remains 53 works.

## 2. Data routes and material gaps

| Route | Documented benefit | Missing or adverse evidence | Disposition |
|---|---|---|---|
| **Kraken downloadable spot trades and OHLCVT** [S1–S3] | Public archive links, quarterly increments, per-trade price/volume/time and bar fields; direct USD pairs could simplify valuation if actually present/accessible | No audited historical universe/delistings/token units, receipt times, rights, quotes/depth or completeness. OHLCVT does not explicitly supply quote-notional/VWAP. REST OHLC gives only the latest 720 entries and includes an unfinished candle | First bounded source audit, not an approved dataset. Use trades to establish exact traded amount; do not download all history first |
| **Binance public archive** [S6–S7,S19] | Per-symbol/day/month partitions; klines include quote volume and trades include quote quantity; documented checksums and revisions | Spot timestamps change to microseconds from 2025; current rules are not historical eligibility. Quote currency may need causal USD conversion. Separate dataset terms restrict production/commercial uses; code MIT is not the data licence. No inspected spot book history | Granular alternative if it resolves an actual gap; licensing and currency treatment prevent assuming seamless research-to-production use |
| **Coinbase Exchange candles/products** [S4–S5] | Public documented candle/product interfaces and a delisted product status | Docs warn history may be incomplete and omit intervals without ticks; 300-candle request limit. No historical status/rule timeline or exact quote-notional in inspected candle schema. Exchange API documentation does not certify the operator's Advanced Trade access | Targeted alternative or consistency check, not an automatically complete multi-asset panel |
| **Tardis** [S12–S14] | Documents native WebSocket history, exchange-specific coverage/incidents and collector receipt timestamps; possible historical spread/depth evidence | Receipt precision is not accuracy or the operator's receipt. Documented reconnection gaps and generated snapshots need reconstruction checks. Delisted-exchange coverage does not prove complete disappeared-token history | Reserve for a specific execution/timing gap; no subscription recommendation now |
| **CoinAPI** [S15–S17] | Advertises normalized history, trades, bars and book products; public metered/subscription prices | Two endpoint documentation URLs redirected to the same generic overview: historical semantics, delistings, timing and completeness were not verified. Quotas and overages can dominate entry price | Conditional normalized-data alternative; no claim of equivalent coverage or lower total cost |

**C3 feature integrity is a binding dependency.** Its activity block requires traded notional in USD. `close × base-volume` is not generally `Σ(trade price × trade quantity)`. Prefer verified trade aggregation or an explicit quote-notional field with correct USD conversion. A switch to approximate activity is a prospective scientific amendment, not a parser convenience. A trade archive may resolve amount aggregation but still lack original receipt times and executable depth.

An instrument's first/last archive row is not a historically announced listing/delisting or an executable exit. Reconcile identity, units, status changes and inactive intervals without selecting only today's survivors. Do not silently drop stranded positions, fabricate a terminal fill or treat an empty candle as a missing transaction. Current archive corrections require version hashes and an explicit corrected-history limitation; hashes cannot recover original availability.

Keep data source, execution venue and legal/product access distinct. Venue A's prices do not certify venue B's execution. Current Spain/access assessments remain scoped documentary evidence, not personal account approval. Direct USD cash on a venue, USD bank cash and stablecoins have different custody, transfer, timing and conversion properties. Do not assume interest or frequent instant bank transfers.

## 3. A concrete acquisition option, not an acquisition performed

To make the next permission reviewable, two **HEAD-only** requests read response headers without reading archive bodies [M1–M2]. The objects are linked by Kraken's official archive pages:

| Proposed QA object | Advertised compressed bytes on 2026-10-25 | Intended structural use |
|---|---:|---|
| `Kraken_OHLCVT_2026Q3.zip` | 576,348,633 | Bar schema, time units, missing intervals, symbol inventory and aggregation cross-check |
| `Kraken_Trades_2026Q3.zip` | 1,596,570,274 | Trade schema/identities, amount units, duplicates, ordering and reconstruction of matching bar totals |
| **Combined transfer ceiling for these versions** | **2,172,918,907 bytes** | Approximately 2.173 decimal GB; not decompressed storage or a whole research dataset |

Both responses declared ZIP, range support and a 2026-10-16 modification date. ETags are recorded as identifiers, not assumed content hashes. Server metadata can change or be wrong; actual acquisition must verify bytes/hash and stop on version/size changes. No Kraken ZIP/sample rows or market endpoint response was downloaded; illustrative records embedded in vendor documentation are not an acquired research dataset. These sizes are evidence-derived resource facts, not an authorized budget.

Q3 is the latest common quarterly package documented at this review and offers matching trade/bar files. Selecting it is for format/reconciliation QA, **not** selection of a profitable period, decision horizon or confirmatory sample. Any inspected interval is exposed QA/development material and must never later be represented as pristine holdout. A quarter cannot establish long-history quality, independent regimes or complete historical delistings.

**Proposed package A, requiring explicit acquisition permission:** only these two objects, no automatic other quarter/provider/full-history fetch; no account, paid API or subscription. Before body download, verify applicable research/retention rights and object identity. Use existing local resources; inspect central-directory sizes after authorized download, stream bounded records and avoid whole-archive extraction. Keep originals plus small QA reports; do not expand files whose advertised size or resource need cannot fit the documented local limit. If rights or safe bounds cannot be established, or transfer/storage would incur an unapproved charge, stop and report. No hardcoded decompression capacity is asserted before it is known.

Permitted outputs would be schema/unit/timestamp/checksum/duplicate/gap checks, complete package member inventory, causal trade-to-bar consistency checks and an accept/qualified/reject report per field/instrument/interval/use. Do not compute strategy signals, returns, P&L, fit models, rank assets, select a trading horizon or open reserved data. Partial sampling cannot certify the entire archive; explicitly state audited coverage. Missing historical events/quotes can justify a focused later audit, not extra acquisition by implication.

The full archives are materially larger: documentation describes five roughly 2 GB OHLCVT parts and fourteen roughly 2 GB trade parts, plus reassembly/extraction. Actual full-history size was not checked. That is why this request names quarterly objects rather than approving an unrestricted download script. Existing website discrepancies—including archive cutoff wording and a trade reassembly example omitting a listed part—remain QA questions, not proof of corrupted files; no example command was run.

## 4. Engine alternatives and compatibility

| Route | Evidence and benefit | Cost/risk and remaining check | Recommendation |
|---|---|---|---|
| **NautilusTrader stable 1.231.0** [S8–S9,M3] | PyPI metadata declares Python `>=3.12,<3.15`, non-yanked CPython 3.12 Linux/Windows wheels and LGPL-3.0-or-later; event-driven engine behind platform-owned experiments | Current latest docs describe **2.x RC**, Python 3.13–3.14 and a different API. Stable release metadata is not dependency resolution, matching docs, maintenance or correct fills. Linux wheel requires a compatible platform baseline | First isolated technical probe, after release-matched documentation/licence review. No platform-wide Python upgrade or unpinned installation |
| **LEAN direct engine** [S10–S11; existing ENGINE-03/04] | Existing Apache 2.0 source/direct-build route; configurable multi-asset accounting/execution | .NET/Python boundary and import/account models add work. Current CLI requires a paid-tier organization and Docker; that does not establish a fee for direct engine use. Default backtest fills are full, and stale fills can occur; partial fills need a custom model | Documented fallback if first engine fails a concrete requirement; no paid CLI or automatic second installation |
| **Freqtrade** [existing engine review] | Crypto framework and useful leakage/recursive-analysis references | Its strategy/position lifecycle must reproduce pooled C3, dynamic universe and fixed-cycle policies; optimizer/live features do not help admission. Distribution obligations remain relevant | Retain, no third parallel integration now |
| Extend the current synthetic ledger | Familiar existing boundary | Its SYNTH-USD/full-fill assumptions do not constitute a financial engine; building realism into it would create substantial accounting/execution work | Do not pursue; preserve synthetic v1 and admit a versioned external-engine adapter later |

The new PyPI check narrows the earlier documentation concern: **Nautilus as a whole is not proven incompatible with Python 3.12**. Stable package metadata supports a candidate; following latest v2 examples remains inappropriate. No wheel was downloaded, installed or executed. A Windows wheel does not verify bot_trader, Windows desktop, WSL or the whole dependency stack there.

Keep research transformations, fitting, nested selection, attempt registry, inference and holdout governance in bot_trader. Feed frozen decisions and instrument/currency/time metadata into the admitted engine; receive accountable orders/fills/cash/inventory and rejections. Engine ML features are not needed for the approved C3 comparison. An isolated worker with versioned artifacts may avoid migrating the main application but adds lifecycle/serialization duties; it remains one platform, not another UI.

**Proposed package B, requiring explicit technical/dependency scope:** inspect matching stable-release docs and install only pinned Nautilus 1.231.0 and resolved dependencies in a disposable isolated environment, preserving production locks/runtime. No account/live adapter activation or automatic data downloads. Use deterministic synthetic cases for causal fill timing; USD/stablecoin conversion; fees once; minimum orders/precision; insufficient cash; partial/no fills; stale data; membership/exit failures; duplicate events; cash/inventory reconciliation; interruption and reproducibility; deny financial/live dispatch. Measure CPU/RAM/I/O only on documented synthetic shapes. Stop if release support, dependency compatibility or required semantics fail; report the LEAN alternative before further implementation. No full adapter, statistical model training, live deployment or Windows certification is included.

## 5. Costs: observed facts versus project budget

All economic comparisons ultimately use USD. Preserve original quoted currency and contract terms until verified; a `$` symbol alone is not sufficient to convert a quote to confirmed USD. No service was ordered or trial activated.

| Item | Public observation, 2026-10-25 | Interpretation and missing binding |
|---|---|---|
| Kraken spot fee page [S18] | Retrieved Spot Crypto tier-1 table shows **0.40% maker / 0.80% taker**; tiers depend on prior volume/assets. Page warns geographically inaccurate fees with VPN | Snapshot, not a confirmed Spain/account tariff or historical fee schedule. Pair/product exceptions and actual eligibility matter; never use remembered tariffs or future volume to grant a discount |
| Kraken funding page [S20] | Resolved page is **deposits**, despite the requested withdrawal-like slug. USD SWIFT examples list Customers Bank minimum USD 100/free provider fee and Bank Frick minimum USD 4/fee USD 3, with regional caveats and bank/intermediary charges | Does not establish withdrawals, Spanish availability or instantaneous cash. Do not apply one-time bank funding fees on every strategy cycle, or treat provider “free” as zero all-in cost |
| Tardis Spot Solo [S12] | Static broad-spot table **$900/month**; history access depends on billing. An order widget states a $300 minimum order | Neither a tailored one-venue quote nor proven USD currency/tax/retention/eligibility. Do not assume monthly purchase supplies the yearly plan's history or permanent rights. Academic pricing is not presumed available |
| CoinAPI [S15] | Advertised monthly tiers **$79 / $249 / $599**, with credits, data allowances and overages | Entry fee does not buy unlimited history. Bind record/credit accounting, venue/field/period coverage, currency, rights and total charges before proposing payment |
| AWS Lightsail Linux/Unix with public IPv4 [S21] | Published general-purpose examples: **USD 12/month, 2 GB RAM**; **USD 24/month, 4 GB RAM**; **USD 44/month, 8 GB RAM**, with listed storage/transfer allowances | Price references, not hardware recommendations or a project quote. Region, tax, backups, transfer and workload still matter. No cloud purchase or minimum RAM requirement follows |

Current fees can support a declared current-cost counterfactual, not exact historical net returns. Raw trades/bars do not identify bid/ask/queue or own impact: relevant cost assumptions need evidence, and an execution-sensitive mechanism may require quoted/book data or postponement. More expensive data can reduce uncertainty but cannot establish alpha.

Separate acquisition/licensing, development/validation work, and recurrent operating costs. Report personal engineering time, electricity, backup and storage even when no invoice is generated. Do not annualize a one-off historical purchase as a mandatory live feed or subtract research costs twice. No total USD cost, expected profit or completion-time estimate can be justified until package quality and engine workload are measured.

## 6. Infrastructure and complete resource sizing

Start with the existing personal/local Python 3.12 platform, SQLite metadata, immutable Parquet and worker; no GPU, cluster, database migration or always-on cloud is presently justified by the small approved model class. This says nothing about comparative economic potential. The user's actual desktop specifications are unknown; the cloud workspace is not a benchmark of that machine. A temporary priced compute job is a later alternative if measurements show local limits. Continuous operating infrastructure is a separate future budget.

There are **18 C3 estimator/ablation slots and eight rules/references**, not 26 equivalent fits. Build a ledger keyed by recipe/parameters, training window, source/transform version, seed and refit time. For inner training cuts I and later refit cuts O:

`C3 fits = Σ(i in I) variants fitted at i + Σ(o in O) retained procedures refitted at o`.

If all eighteen variants are evaluated at every inner cut, the first term is `18 × |I|`; neither the number of cuts nor the second term is invented here. Rules still require causal calibration and evaluations. Count engine runs by procedure/calendar/capital/cost case separately; reuse frozen predictions only when the changed scenario does not change selection or the policy. Failed attempts/retries remain recorded. Budget the existing 9,999 bootstrap resamples separately from model fits and market observations.

Size the panel as `M = Σ_t N_t` eligible historical asset-times, not today's asset count multiplied over nonexistent histories. Memory depends on design columns, concurrent folds, event buffers and working copies; storage includes source versions, QA, artifacts and backups. Estimate wall time from measured synthetic job shapes and I/O, preserving uncertainty. Cheap compute does not enlarge the approved search envelope. A source/engine test can estimate resources, not infer a profitable horizon or select capital.

## 7. E3/E4: economic scenarios and remaining statistical dependency

Retain USD 1,000/5,000/10,000 as user-supplied sensitivities. Select one primary research capital only after cash/fee/minimum-size/capacity evidence, before outcome-based selection. With potential allocation `K/N_t`, insufficient minimum orders cannot be repaired by retrospectively concentrating capital in winners. No primary midpoint, maximum capital or live allocation is assumed.

For applicable annual recurring fixed cost F and capital K, `F/K` is one break-even burden; variable costs, turnover, conversion and capacity remain separate. No return forecast follows from that identity. Materiality requires both net increment over the comparator and net improvement over accessible cash, after costs counted once. Required additional benefit, tolerated return sacrifice for C2, and research risk scenarios remain user decisions informed by costs and precision. Historical drawdown is not a maximum-loss guarantee; tail-risk measures need adequate tail support. No universal numerical risk/return threshold is added.

**Sequencing issue to resolve explicitly:** protocol §3 requires development-only variance/dependence estimates for precision **before validation**. Acceptance also requires full bindings before financial execution. Structural data QA and synthetic engine tests cannot estimate the distribution of *paired candidate-minus-reference net returns*. Raw asset volatility is not a substitute. Therefore the proposed packages cannot complete every statistical acceptance criterion.

Do not hide candidate pilots inside “data quality”, invent variance/power, or declare IV closed. After technical/source admission and economic choices, present a prospective clarification separating admission of bounded financial **development** from admission of **validation/final** if that is needed. It must preserve finite search, predeclared economic criteria, no validation peeking and independent final data, and requires express approval of that financial scope. **This report does not enact that amendment or authorize such runs.** Alternatively remain at conditional design readiness and postpone empirical work. No response to that later question is needed to review the present non-performance packages.

## 8. Material decisions and next gate

| Timing | Actual user decision | Recommendation and consequence of deferral |
|---|---|---|
| **Now, before acquiring files** | Authorize package A: only the two identified free Q3 archives, conditional rights/identity checks, structural QA and stated acquisition ceiling; no strategy or model evaluation | Recommended to resolve data semantics and resource facts. If deferred, keep the source provisional and stop at documentary feasibility. No vendor subscription decision is needed |
| **Now, before installing/testing an engine** | Authorize package B: isolated pinned stable Nautilus technical probe with synthetic fixtures and no production dependency change | Recommended to resolve version/accounting fit and resource estimates. If deferred, no engine can be marked admitted; no need to choose a framework permanently |
| **After those results** | If a specific gap persists: fund a quoted capability, narrow the scientific claim prospectively, or postpone; choose primary capital/materiality/risk from concrete scenarios | E3/E4 stay pending now; do not ask for arbitrary dollars, expected return or personal drawdown |
| **Before empirical development / validation** | Approve any necessary explicit sequencing clarification, the populated preregistration and precisely scoped financial authorization | Remains future and separate. Neither E1/E2 nor packages A/B authorize Phase V or final-data access |

These two present permissions can be given separately or together. Their necessity follows directly from the user's restriction on dataset acquisition and expanded technical permissions; they are not repeated design approvals. The team owns provider/format/solver details within the eventual authorized scope; escalate only material cost, scientific claim, risk or permission changes. Preserve negative results and stop a branch when its admission fails.

## 9. Sources and audit limits

All URLs below are official documentation or public package metadata. Directed reading is limited to the claims cited, not every linked page, contract or code path. Current documents are not historical vintages. Public prices are observations, not quotations accepted by the user.

| Ref / receipt ID | Source and examined scope |
|---|---|
| S1 / IV-DATA-01 | [Kraken OHLCVT archives](https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data): schema, packaging, cutoff/increments |
| S2 / IV-DATA-02 | [Kraken trades archives](https://support.kraken.com/articles/360047543791-downloadable-historical-market-data-time-and-sales-): fields, quarterly/full packaging and limitations |
| S3 / IV-DATA-03 | [Kraken OHLC API](https://docs.kraken.com/api-reference/market-data/get-ohlc-data): retrieval bound and unfinished candle |
| S4 / IV-DATA-04 | [Coinbase candles](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles): incompleteness, limits and fields |
| S5 / IV-DATA-05 | [Coinbase products](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-all-known-trading-pairs): current status and field inconsistencies |
| S6 / IV-DATA-06 | [Binance archive README](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md): partitions, amounts, timestamp change, checksums/corrections |
| S7 / IV-DATA-07 | [Binance general API documentation](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/general): current rule/status scope |
| S8 / IV-FEAS-E01 | [Nautilus installation](https://nautilustrader.io/docs/latest/getting_started/installation/): latest v2 RC/runtime versus stable v1 |
| S9 / IV-FEAS-E02 | [Nautilus backtesting](https://nautilustrader.io/docs/latest/concepts/backtesting/): overview and API levels, not deep fill/queue audit |
| S10 / IV-FEAS-E03 | [LEAN CLI getting started](https://www.quantconnect.com/docs/v2/lean-cli/key-concepts/getting-started): paid organization/Docker requirements; direct engine assessment reused |
| S11 / IV-FEAS-E04 | [LEAN fill models](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts): complete/partial and stale-fill defaults |
| S12 / IV-FEAS-TAR-PRICE | [Tardis pricing](https://tardis.dev/): static plan/history table, order minimum; no order configured |
| S13 / IV-FEAS-TAR-FAQ | [Tardis FAQ](https://docs.tardis.dev/faq): index only; no full linked terms review |
| S14 / IV-FEAS-TAR-HISTORY | [Tardis history details](https://docs.tardis.dev/historical-data-details): collection/receipt and gaps, not actual data |
| S15 / IV-FEAS-COIN-PRICE | [CoinAPI pricing](https://www.coinapi.io/products/market-data-api/pricing): plans, credits/overages |
| S16–S17 / IV-FEAS-COIN-SYMBOLS, BOOK | [CoinAPI overview](https://www.coinapi.io/products/market-data-api/docs): identical redirected generic bodies; endpoint claims remain unverified |
| S18 / IV-COST-01 | [Kraken fee schedule](https://www.kraken.com/features/fee-schedule): spot tier and geographical qualification |
| S19 / IV-LIC-01 | [Binance Vision terms](https://raw.githubusercontent.com/binance/binance-public-data/master/TERMS_AND_CONDITIONS.md): v1, updated 2026-08-26; non-commercial research and production restrictions, not a legal certification |
| S20 / IV-COST-02 | [Kraken cash deposits](https://support.kraken.com/articles/360000381846-cash-deposit-options-fees-minimums-and-processing-times-): USD examples/regional and bank-charge caveats; withdrawals unverified |
| S21 / IV-COST-03 | [Lightsail pricing](https://aws.amazon.com/lightsail/pricing/): Linux IPv4 tariff examples and separate storage/transfer costs |
| M1–M2 / IV-META-01–02 | [OHLCVT Q3 object](https://assets.kraken.com/marketing/institutions/Kraken_OHLCVT_2026Q3.zip), [trades Q3 object](https://assets.kraken.com/marketing/institutions/Kraken_Trades_2026Q3.zip): **HEAD headers only; do not download without permission** |
| M3 / IV-ENGINE-META-01 | [PyPI Nautilus metadata](https://pypi.org/pypi/nautilus_trader/json): stable release, Python requirement and wheel identities; no package installed |

The environment restarted during integration. Cached source bodies survived; temporary agent drafts and original detailed transport logs did not. The source ledger explicitly records cached reconciliation and what transport metadata could be recovered from the conversation, rather than inventing retrieval times or claiming a fresh download. Two CoinAPI responses are identical; do not count them as independent evidence. New HEAD/package-metadata receipts are preserved separately. Hashes prove snapshot identity, not completeness or truth. No academic evidence count or financial experiment counter changed.
