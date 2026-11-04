# E1 — executed bar timing and causal execution checks

Document ID: IV-E-BARS-001 · Version: 1 · Evidence: 2026-11-03 UTC · English canonical. [Spanish](../../es/phase-iv/bar-execution.md).

**Exact NautilusTrader 2.0.0rc7 reproduces a same-close fill after the closing-bar signal. Adding 1 ms latency moves this fixture's fill to the next bar's close, not its open. A small boundary with `bar_execution=False` preserves causal sequencing in the tested synthetic cases.** This supports conditional offline candidacy, not definitive engine selection or financial admission.

[D-052 authority](../../phase-iv/APPROVAL-E1-BARS.es.md) follows `c1d4029`. [Reproducible evidence](../../phase-iv/technical-results/E-bars/README.md) preserves the frozen fixtures, code, exact configurations, native callbacks, books, fills, checks and receipts. Six grouped technical invocations ran **15 native contexts and 135 component checks**; all checks pass, including deliberate reproduction of adverse behavior. One preparation froze inputs before execution. No corrective cycle was needed. Passing the negative control does not make its configuration acceptable. M, the 160-case R suite, E3-L2, E4 and LEAN were not rerun.

## Fixture, clocks and exact execution

Runtime: existing standard CPython **3.13.16**, exact **NautilusTrader 2.0.0rc7**, no installation or download. Venue: invented SYN-USD.SIM, cash/netting, initial USD1,000/SYN0, quantity1, price/size increments0.01, `MakerTakerFeeModel` maker0.001/taker0.002, active native risk, L1, liquidity consumption enabled, message queue enabled, deterministic IDs, no custom fill model. These are technical fixture parameters, not E3/E4 economic decisions. All commands are BUY; sell-side symmetry has not been tested here.

Time uses integer nanoseconds. Let T0=1,700,000,000,000,000,000; T1=T0+60 seconds; T2=T1+60 seconds. N has OHLC100/101/99/**100.50** and N+1 has **110**/125/108/112, each with invented volume100. The native baseline labels both bars at close: event/init/modeled availability are T1 and T2 respectively. Decision processing delay is explicitly zero. No intermediate market event was inserted to force queued-order processing. A common `InstrumentStatus.NONE` one second after the last input drains the clock without supplying a price; no observed fill depends on this final marker.

| Variant | Decision / submission | Nominal arrival | Native acceptance and fill | Actual result |
|---|---|---|---|---|
| Native, latency0, adaptive false | T1 after N callback | T1 | T1, after submission | 1 @100.50, fee0.20 USD |
| Native, latency0, adaptive true | T1 after N callback | T1 | T1, after submission | Same |
| Native, latency1 ms, adaptive false | T1 after N callback | T1+1 ms | T2, after N+1 callback | 1 @112.00, fee0.22 USD |
| Native, latency1 ms, adaptive true | T1 after N callback | T1+1 ms | T2, after N+1 callback | Same |
| Causal boundary, synthetic offer | T1 decision; T1+1 ms submission | T1+1 ms, zero order latency | T1+1 ms | 1 @110.05, fee0.22 USD |
| Delayed N availability, later eligible quote | T1+10 ms decision; T1+21 ms submission | T1+21 ms | T1+21 ms | 1 @111.05, fee0.22 USD |
| Delayed N availability, no later eligible quote | T1+10 ms decision; no submission | Not applicable | No acceptance/fill | Cash unchanged |

“Nominal arrival” is submit time plus configured latency, **not an observed exchange arrival**. `OrderAccepted` is an observed processing proxy; the API trace does not expose a separate physical arrival event. The order event and fill `ts_event`, `ts_init` and strategy clock are preserved individually in the evidence.

Native ordering observed without latency: module pre-process → N callback → decision → submit → submitted → accepted → filled → exposed book snapshot. The book ends at bid=ask100.50, size25 on each side, derived natively from the invented bar, not an observed spread. With latency, submitted occurs at T1; the next bar pre-process and callback occur at T2, then accepted/filled, then the book snapshot at bid=ask112.00. The intervening T1 snapshot still shows100.50. The observed result is consistent with the pending command being processed after the next bar has updated the executable reference to its close. We did not inspect every internal OHLC matching step and do not assert a complete hidden path.

**Interpretation:** native same-close matching conflicts with our contract requiring a subsequent eligible executable event after closed-bar information. The callback order is not itself proof of signal look-ahead, nor is this a universal engine defect. Positive latency alone is not a next-open mode. Adaptive ordering had no effect on these market-order outcomes; this does not establish irrelevance for resting orders or other event streams. No assumption was changed to force an open/high/low/close result.

## Timestamp negative control and precision

Four native timestamp-only contexts deliver one complete bar and place no orders:

| Supplied convention | Native callback clock | Finding |
|---|---|---|
| Opening label, `ts_event=T0`, incorrect `ts_init=T0` | T0 | Full OHLC arrives 60 seconds before true close: deliberately inadmissible |
| Opening label, `ts_event=T0`, corrected `ts_init=T1` | T1 | Complete bar arrives at modeled close availability |
| Closing label, `ts_event=T1`, `ts_init=T1` | T1 | No second interval added |
| Opening label with all timestamps shifted123 ns; corrected init | T1+123 ns | Event/init and callback precision preserved exactly |

Thus the inspected rc7 path schedules complete-bar delivery from the supplied initialization time; it does not protect a caller who incorrectly labels availability. The real contract must use actual availability when it is later than interval end. `open+duration` is the earliest modeled complete-bar availability in this idealized canary, not a claim of zero provider/network delay. Native `ts_init` alone also cannot preserve distinct publication, reception and revision clocks; retain those in the source envelope.

The exact integer conversion helper checks seconds/milliseconds/microseconds/nanoseconds, rejects floats, booleans, unsupported units, negative values, unsigned64 overflow and lossy nanosecond→microsecond conversion; exact narrowing succeeds. Production's datetime-based `MarketBar` was **not** migrated. A future boundary must either preserve source precision or reject unsupported precision explicitly, never silently truncate it.

Selected original **R1** delayed availability, **R2** nanosecond precision, **R3** open versus complete bar and **R7** later correction facts were reused against these helpers. The source journal, selected indices, expected records and hashes are included. This is selected predicate coverage plus the new native canaries, not a repetition of all R checks or proof of production/engine equivalence.

## Minimal causal alternative and future-information invariance

`bar_execution=False` keeps complete bars as signal inputs, without using their full OHLC to supply executable prices. The boundary retains N's decision and waits for a quote callback after the decision is ready. It checks quote event time, availability, maximum declared age and quantity. No order is sent from the complete-bar callback in this route. A received quote preceding a ready decision is not cached and reused later for retroactive execution.

Versioned policy **D052-OHLC-synthetic-v1** declares full spreadUSD0.10, zero additional slippage, zero order latency, visible quantity2, maximum submitted quantity1 and maximum quote age1 ms. The first offer uses only the independent N+1 opening value110: bid109.95/ask110.05, eventT1, deliveryT1+1 ms. At that callback the strategy receives no N+1 high, low or close; the full N+1 bar arrives atT2. The native fill is1@110.05; the boundary does not manufacture or inject fills.

This quote is **invented execution information**, not reconstructed historical bid/ask. It assumes the opening-derived offer remains executable on reception and that zero additional order latency is acceptable in this synthetic scenario. Equal event/decision boundary time is admitted only with the declared callback order and later receipt; real ambiguous ties require source sequencing or conservative exclusion. Neither opening-price executability nor offer persistence is demonstrated from OHLC. The one-unit cap keeps this probe below invented visible quantity; it does not repair or erase the previous L1 overfill finding.

When N arrives10 ms late, the opening offer at+1 ms is skipped. A separate invented quote, mid111/event+20 ms/delivery+21 ms, allows a native buy at111.05. Without it, no order or fill occurs, including when the complete N+1 bar arrives. Therefore the opening cannot be recovered retrospectively merely because its price is present in a stored bar. The changed price and the no-fill outcome are intentional consequences of the causal policy.

Four separately frozen perturbations leave the full native trace prefix throughT1+25 ms identical to the causal baseline:

- N+1 high125→135, with other OHLC unchanged.
- N+1 low108→106, with other OHLC unchanged.
- N+1 close112→113, with other OHLC unchanged.
- An additional N revision, close100.50→99.75, old eventT1 but availabilityT1+30 ms. Its later bar callback was actually observed, not silently dropped.

All bars remain OHLC-consistent. The already executed decision/order/fill prefix is unchanged, including deterministic identities and accounting. The four comparisons concern the causal route; native latency outcomes were not reclassified as invariant. This is a bounded one-intention canary, not a complete recursive-indicator, persistent-revision or strategy-history implementation.

## Contract for a first future offline runner

The contract is restricted to **spot long/cash, confirmed closed bars and market orders**. The technical boundary is a disposable proof, not that runner. No resting stop/limit whose matching depends on unknown intrabar order is admitted by this evidence.

| Required invariant | Implementation/evidence now | Remaining before dependent financial use |
|---|---|---|
| Signal knowledge | Closed/end/available gate, exact nanosecond helpers, decision trace | Production source envelope, provider conventions/delays, revisions and persistence; decision latency model |
| Earliest order eligibility | Retained decision; eligible later quote; no retroactive cached opening | Versioned processing/transport delay and tie policy integrated with actual data |
| Price formation | Native matching against explicitly synthetic quote, no future HLC at opening | Choose and predeclare OHLC-only approximation versus admitted historical quotes/trades; provenance and exact conversions |
| Costs/capacity | Fixture spread, fee schedule/rounding, zero extra slippage/latency, size caps versioned | Source/product-specific fees, spread, slippage, delay, impact and capacity sensitivities; no claim zero costs are adequate |
| Rejection/partial/cancel | This batch records native order outcomes; no new partial/rejection case. D-051 observations reused without rerun | Implement/review the lifecycle policy in the future runner; distinguish intent, acceptance, partial fills, rejection and confirmed cancellation |
| Remainder disposition | Policy says cancel-and-confirm on the next processing opportunity; it is **not implemented** in this harness | Stop new exposure until confirmed outcome; never presume automatic continuation or cash reservation; mark unresolved/unknown terminal state explicitly |
| Independent reconciliation | Decimal BUY/USD cash, fees, inventory, free+reserved and position checks pass | Validate sell/round-trip and partial/cancel integration before supporting them; identity, funding allocation and recovery obligations remain |

For all actual fills, the independent Decimal oracle checks fee rounding to USD cents, cash debit and base-unit increase, then reconciles native balances, free+reserved and positions. Baseline causal final state is USD889.73/SYN1; delayed later-quote state USD888.73/SYN1; no-event state USD1000/SYN0. This is accounting of executed synthetic transactions, not strategy return evidence or a general financial ledger certification.

The proposed remainder policy uses already observed native cancellation primitives from D-051, where a market6 against depth4 left2 unfilled and unreserved; explicit cancellation worked, a later snapshot did not automatically finish it. Those findings and E4's missing second fill remain adverse/limited. A pending cancellation is not confirmation. On uncertainty, block additional exposure and fail the offline run's reconciliation rather than invent a fill or release. No operational emergency-close policy is added here.

With **OHLC alone**, opening-derived quotes, spread, liquidity and execution delay remain assumptions. If closed-bar data does not make the opening available when the model uses it, that route needs an explicit and justified event-construction model or must wait; complete future HLC must stay inaccessible. With **historical quotes/trades**, preserve actual event/receipt/availability and gaps; a trade is not automatically a simultaneously available bid/ask or capacity guarantee. L2 is not universal, but neither data choice justifies perfect fills. Costs and robustness must later reflect the resolution actually admitted.

## Resources, audit and disposition

Guard receipts record **9.712751 seconds active machine wall time** including preparation, **6.404959 CPU seconds**, maximum sampled process-group RSS **82,489,344 bytes** (~78.7 MiB), four-core affinity, zero new downloads and zero contracted services. The result index records the final additional scratch bytes (under1 MiB, against512 MiB). Six grouped test invocations are distinct from fifteen sequential native child processes; no unreported exploratory engine run or correction occurred. There is no need to spend unused slots.

RSS sampled every100 ms can miss short peaks and is not a cgroup hard-memory certificate. The existing offline guard denies IPv4/IPv6; Landlock is unavailable on this host. The resources are measurements of these tiny synthetic probes, not production sizing. Engineering/documentation time is not included in guarded machine time. Preservation checks confirm **73 runtime/config files and 4,630 regular production-venv files unchanged**, no additions, protected scientific paths unchanged and the software-download ledger hash unchanged.

Recommend retaining Nautilus as a **conditional offline candidate with an explicit causal data/order boundary**, not relying on native `bar_execution=True` or a small positive latency as a next-open guarantee. This targeted uncertainty is now resolved for the exact cases; no further general framework review is needed to interpret them. The first financial runner still needs production temporal integration, justified execution assumptions and applicable lifecycle/accounting admission. This batch does not cover general historical/live parity, safe prospective recovery, every native order type or full E admission.

E1 here is the technical engine case, distinct from the approved scientific decision E1. Economic **E3/E4 remain pending**, the **26 specifications**, E1/E2 scientific commitments, C1–C5 priorities, T/D/U/V/F and future UX work are unchanged. Phase IV stays conditionally open. No production dependency/source change, new financial data, financial experiment, Phase V, paper or live execution occurred or is authorized by these results.
