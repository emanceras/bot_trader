# E recovery — executed results and remaining gates

**Subsequent D-050/D-051 correction:** [new executed findings](engine-correction.md) preserve this recovery record. L2 reference-price bridge now executes the original sweep; E4 duplicate corruption is prevented by the supervisor, but its second required native fill is still absent. No engine/financial admission.

Document ID: IV-E-RECOVERY-001 · Version: 1 · Date: 2026-11-02 · English canonical. [Spanish](../../es/phase-iv/engine-recovery.md).

**Nautilus now runs, but neither engine is admitted for financial research or production.** The bounded recovery produced useful accounting, execution and interruption evidence, including adverse results. It did not complete every original E requirement. [D-048 authorization](../../phase-iv/APPROVAL-E-RECOVERY.es.md) supplements the original scope; [00131bc results](technical-results.md) remain preserved. M/R and conclusive LEAN tests were not repeated.

## What actually ran

The exact approved Nautilus **2.0.0rc7** wheel was installed in a disposable environment using **standard CPython 3.13.16**, the highest compatible 3.13 patch available through existing uv 0.12.23. No free-threaded runtime, Python 3.14, optional dependencies or production migration. Runtime provenance and digests were fixed before installation in the [setup pin](../../phase-iv/technical-results/E-recovery/setup-pin.json); import/ABI and dependency checks passed. The 35,076,205-byte runtime archive has SHA256 `4595c5589fff7bf0cb158d9a88a797e0d791fa33830770fcb7bf3f4b104feeae`; the unchanged 72,042,580-byte wheel has SHA256 `b3928f37d75d57508030a421dc762186ad1f9ffc5d5420d7daf1d2c6badb8044`.

Nine original Nautilus functional slots were exercised at component scope, including the uninterrupted E5 reference and three interrupted reconstructions. Four complementary liquidity configurations also ran. There were **17 native worker processes**, counting the one E2 corrective rerun and the three reconstruction processes. These counts do not imply full admission: across the original 26-slot comparison, 12 component slots have now been exercised (9 Nautilus, 3 earlier LEAN), 14 remain unexecuted, and zero are certified against every original requirement. E6 remains blocked by functional gates; no throughput score was produced.

One bounded harness correction was used. The first E2 attempt failed before submitting orders because obtaining `engine.cache` inside an engine callback conflicted with its mutable run borrow. Capturing the same shared cache before `run()` fixed that access error. Only E2 was rerun; its failed output and both source versions remain published. No expectation, fixture, fee or engine version changed. **The corrective allowance is exhausted**; subsequent limitations were recorded without repeated harness repairs.

## Case evidence

| Case | Observed result | Interpretation and limitation |
|---|---|---|
| E1 | Closed-bar canary gives BLOCK, then OBSERVE 101, then revised OBSERVE 99 at the frozen availability times; delayed information is admitted at its availability | Native nanosecond clock, harness information/decision rule. Full native R-canary/prefix/precision parity remains unproved |
| E2 | Buy 2 at 100, taker fee 0.40; later post-only sell 1 at 102, maker fee 0.10. Final USD **901.50**, SYN **1**, USDT **40**. Bad step, minimum notional and insufficient cash are denied | Native fills, fees, rejections and account/position conservation pass the tested arithmetic. USD/USDT valuation 39.60 after the conversion event is a harness causal calculation, not native FX execution. Broader partial-fill/account behavior is not certified by this case |
| E3-L1 | With consumption enabled, a market order for 4 against ask size 1 fills **1 at 100 and 3 at 100.01** | Fails the frozen finite-visible-quantity requirement. The configured model supplies an extra-tick remainder beyond visible depth. Consumption does not universally impose a visible-size cap |
| E3-L2 | Depth-market order denied with `MARKET_PRICE_UNAVAILABLE`; cached depth exists, but there is no quote tick for the risk-price path. Resting order later fills 1 at 99, then cancellation leaves 2 unfilled; IOC fills 0 and cancels 2; cancel-before-fill order fills 0 | Market traversal not demonstrated in this configuration. Limit/partial/cancel observations are native. Do not call missing reference-price integration a universal inability to match L2 |
| E4 | First order fills 3 at 100, fee 0.60. Direct duplicate submission with the same identity leaves the cached order DENIED with filled quantity 0. Second strategy is denied for insufficient free cash. Final USD 699.40, SYN 3; **USD 300 remains reserved** | Fails required two distinct equal fills and coherent order history. Position/cash preserve the fill, but order state diverges and reservation is unresolved despite terminal cached orders. No duplicate capital was observed; that alone is insufficient. Native duplicate-fill redelivery was not exercised |
| E5 reference + three cuts | Abrupt exits 71/72/73 occurred after submission, after fill and during cancellation. Reconstruction from identical persisted source reproduces exact final fills/IDs, orders, positions, fees and cash; original journals retain hashes | **Post-hoc research recomputation only.** No checkpoint restoration or reconciliation gate before new commands; no independent venue authority. This is not a full E5 pass or prospective recovery |

E2 preserves the exact order: the sell arrives at offset 320, after quote 300 and **before** quote 500 touches its limit. Nautilus meets the frozen touch-fill expectation; LEAN's previously tested native limit model requires strict crossing and leaves the order open. Neither observation establishes the real queue's outcome. No order was moved to make the sale pass.

E3's IOC arrives at offset 420, after the resting order consumed the one unit at snapshot 300 and before snapshot 500. Its zero fill therefore differs from the external standalone IOC observation for an understandable information-state reason. The external example is not a project replication or a reason to inject new liquidity. The original full-depth market sweep remains unproved here.

## Four fixed liquidity-consumption configurations

Each fixture has one initial observation: bid 99@1, ask 100@1, followed by two separate market buys of one unit at offsets 120 and 130. No intervening or later quote/book update. A terminal `InstrumentStatus.NONE` advances the clock without requested price/depth changes; observed book snapshots remain unchanged and no terminal-marker fill occurs.

| Book / consumption | First / second native fill | Derived initial budget minus fills | Conclusion |
|---|---|---|---|
| L1 / false | 1 / 1 at 100 | −1 | Visible liquidity reused between orders |
| L1 / true | 1 / 0; second rejected, `No market` | 0 | Consumption discriminates successive orders in this example, while E3-L1 still overfills a single larger order |
| L2 / false | 0 / 0, both denied before submission | 1 | No matching effect observed; missing market reference price prevents the intended comparison |
| L2 / true | 0 / 0, same denials | 1 | Inconclusive about L2 consumption; not a liquidity pass |

The exposed native book still displays ask size 1 in both L1 configurations. It is not a certified internal consumption counter. Derived budget figures are transparent arithmetic diagnostics, never claims about hidden native remaining liquidity. One invented level/two orders cannot establish impact, queue priority or general execution realism. The diagnostic supplements E; it does not replace failed original tests.

## Research integrity versus prospective recovery

Research admission still requires correct fees/cash, stable identities, no duplicate capital/effects, coherent order/position records and reproducible causal input. E4 therefore blocks admission of the direct-submission boundary even for offline research. It should be addressed with an explicit, bounded command-idempotency boundary and reconciliation evidence, not hidden by an agreeable equity total.

E5's durable `venue-fills.jsonl` is a **native callback journal**, not an independently running exchange. Each reconstruction starts a fresh isolated simulator with the same persisted source bytes and fixture run identity; framework run UUIDs can differ. The supervisor compares durable prefixes afterwards and consolidates actual fill identities without adding a second ledger effect. It suppresses 0/1/1 repeated rows across the three cuts. This supports deterministic recomputation for an immutable synthetic research run; it does not show the resumed worker suppressing actions before reconciliation. Original E5's stronger requirement remains unmet.

Unknown external fills, outstanding exchange orders, broker attribution and safe operational resumption remain future requirements. They need not be implemented now to test offline research integrity, and this recovery does not authorize that infrastructure. Even a later offline admission would not grant paper/live permission.

## Resources and preservation

[Machine-readable receipts](../../phase-iv/technical-results/E-recovery/README.md) preserve raw observations, frozen inputs/source hashes, correction history, exact commands and original negative results. Signed public-download redirect queries are removed only from the published ledger, with original/exported hashes and explicit redaction records. No binary or financial dataset is committed.

| Measurement | Recovery increment / measurement | Cumulative M/R/E |
|---|---|---|
| Recorded active setup/test/download wall time | **21.244048 s** | **219.708965 s** of 7 h aggregate; E alone 175.554503 s of 4 h |
| Guarded CPU time | 10.281705 s | 369.067488 s |
| Charged software transfer | **107,247,021 bytes** | **438,885,198 bytes** (418.55 MiB) of 2.5 GiB; E 384,953,266 bytes of 2 GiB |
| Current scratch increment / total | 594,733,238 bytes | **3,085,496,951 bytes** (2.874 GiB) of 12 GiB; E 1,839,633,750 bytes of 8 GiB |
| Peak sampled process-group RSS | 94,113,792 bytes for recovery invocations | 1,674,530,816 bytes from earlier setup, below 8 GiB |

Jobs remained sequential with at most four CPU cores. No resource stop or paid service. Measurements exclude unmeasured engineering/review effort and credit interruptions; short runs can evade 100 ms RSS samples, so these are not exact peak-memory certificates. CPU affinity/network denial and sampled guards do not provide hostile-code filesystem confinement on this host.

[Preservation verification](../../phase-iv/technical-results/E-recovery/preservation.json) matches 73 recorded runtime/configuration files and 4,630 regular production-environment files, with no additions or protected source/scientific changes. Symlink targets and private runtime state are outside that audit. Financial counters remain zero; E3/E4 methodology decisions, Phase V and paper/live remain pending. C1–C5, 26 base specifications, E1/E2 scientific commitments, T/D/U/V/F and future UX items are unchanged.

## Recommendation and concrete next boundary

Keep **Nautilus as a technically credible candidate**, without selecting it yet: accounting/rejections and causal ordering now have actual native evidence, and the liquidity switch has a measured effect. Its RC support risk, direct duplicate-order inconsistency and L2 reference-price path remain material. LEAN remains an alternative with a different tested fill assumption and incomplete lifecycle bridge; no fair performance or full-system winner can be inferred.

The next useful work would be one separately authorized, bounded offline bridge check: derive a reference quote **causally from the same L2 snapshot**, without new liquidity or disabled risk; reject duplicate command IDs before resubmission while preserving native state; check duplicate fill identity and terminal reservations; and, if required for the research runner, reconcile the same durable run before permitting new commands. Native parity coverage also remains incomplete. This is a proposed new scope because the current corrective allowance is spent, not another execution already hidden in this delivery. No new vendor survey, market dataset, model fitting or full live adapter is needed to state those gaps.

Do not impose L2 on every strategy. A mechanism depending on queue/depth or rapid execution needs stronger data/model evidence; lower-frequency bar research could use a separately justified conservative execution contract. Neither scientific admission nor engine choice should follow solely from passing a favorable synthetic touch-fill assumption. Phase IV remains conditional.
