# Phase IV — technical audit of packages A and B

Document ID: IV-ADMISSION-001 · Version: 1 · Date: 2026-10-26 · English canonical. [Spanish](../../es/phase-iv/admission.md).

## Scope and disposition

[D-040 authorization](../../phase-iv/APPROVAL-A-B.es.md) covers exactly two Kraken quarterly archives for private structural QA and an isolated NautilusTrader 1.231.0 probe using invented synthetic fixtures. This report supersedes the **current status**, not the historical findings, of [feasibility](feasibility.md). Production source, dependencies, synthetic-only guards and financial experiment counters remain unchanged. No financial strategy test, investment-model training, prospective paper/live activity or paid service was performed.

**Disposition:** A and B completed within their bounded technical scope, with qualified source suitability, a same-environment dependency conflict, an adverse L1 fill assumption and unverified recovery. Neither source nor engine is admitted for financial execution. E1/E2 retain their conditional approval; E3/E4 remain pending, `execution_ready=false` and `phase_v_authorized=false`. Phase IV is not unconditionally closed.

## A — rights, acquisition and actual coverage

The [rights receipts](../../phase-iv/admission/kraken-rights-sources.jsonl) record four new official pages and reuse of prior archive documentation. Kraken's archive invitation explicitly allows files to be “used in code, converted into other formats”; its EEA terms permit approved uses for the user's own benefit while retaining broad copying/automation restrictions. This supports the narrow offered download/private code-inspection workflow, **not** an open-data licence, commercial/redistribution permission or legal certification. [Scoped assessment](../../phase-iv/admission/kraken-rights-assessment.json). No access-control circumvention, account, external contact or extra dataset was used.

| Approved object | Acquired bytes | SHA-256 of acquired body |
|---|---:|---|
| `Kraken_OHLCVT_2026Q3.zip` | 576,348,633 | `96daae63c7b3acb522892e1f602f9c564d1a3fb659089d9b0699282f30d41226` |
| `Kraken_Trades_2026Q3.zip` | 1,596,570,274 | `67aa726be17a0f3ed14e4737030c777e1aa522e568090e72aa950415d66bce25` |
| Total | **2,172,918,907** | Two bodies only; originals outside Git |

Current HEAD and GET identity/size checks matched the reviewed manifest. [Acquisition receipts](../../phase-iv/admission/kraken-acquisition.jsonl) preserve the initial HTTP 403 failure before any archive body, and the successful ordinary User-Agent retry with TLS verification unchanged. No extra endpoint or quarter was fetched. A local hash establishes content identity; multipart ETags and ZIP CRC do not independently certify provider truth.

[Primary result](../../phase-iv/admission/kraken-results.json), [separate volume diagnostic](../../phase-iv/admission/kraken-volume-diagnostic.json) and [pair-label review](../../phase-iv/admission/kraken-pair-review.json) preserve denominators and adverse outcomes.

| Check | Observed result | Disposition / boundary |
|---|---|---|
| Complete member inventory and CRC | 10,054 OHLCVT + 1,438 trade members; **11,492/11,492** streamed successfully, 8,380,534,210 uncompressed bytes; no extraction | Internal byte integrity passes; no independent provider checksum or completeness guarantee |
| File/line-count manifests | 10,052 bar CSVs with 36,966,491 rows; 1,436 trade CSVs with 116,477,432 rows; both have identical sets of 1,436 pair labels | Counts reconcile; labels do not certify historical identities, delistings or an operable universe |
| Bounded numerical checks | First/last 64 rows per CSV, overlap removed: **1,190,284 bar rows / 182,180 trade rows**; no tested schema/numeric/OHLC/time/ID errors | Only sampled rows; not random sampling, global ordering validation or an error-rate estimate. Sparse/unsampled gaps are not declared missing trades |
| Schemas/notices | OHLCVT schema 1 has no header; trade schema 2 has seven named fields, timestamp first. README documents older order/header differences and absent metadata for some delisted pairs | Version-specific parsing required. No absent metadata occurred in the inspected edge sample, so the optional third diagnostic pair was not selected. This does not prove delisted coverage |
| Duplicate candidates | 1,241 sampled adjacent identical timestamp/price/quantity triples; no duplicated IDs in the sampled records | Equal values alone must **not** be deduplicated; no full-archive trade-ID uniqueness test |
| Trade/bar reconciliation | XBTUSD/ETHUSD labels, three fixed complete UTC days (July 2, August 15, September 29), all seven supplied intervals; 9,661,747 trade rows scanned for time order, 331,121 trades within windows, **11,105 bars** compared | OHLC and counts match exactly; no unmatched populated bins. Overlapping interval aggregates are not independent observations or selected research horizons |
| Exact volume | **7,011/11,105 mismatches** against Decimal sums retained | Separate diagnostic reproduces all 11,105 reported volumes with ordered binary-float summation. This explains sampled representation differences; no fitted tolerance or retroactive “exact pass”. Maximum absolute differences: 5.22e-10 and 2.62e-9 respective base units |
| Exact traded amount | `close × volume` differs from `Σ(price × quantity)` in **10,774/11,105** compared aggregates | C3 must retain trade-based amount reconstruction or a verified quote-amount field. This concerns the reported trade values; independent true USD identities/conversion and source accuracy remain unverified |

Both READMEs refer to `SHA256SUMS.txt`, absent from both ZIPs. No extra checksum file was acquired. The archive notices added no conflicting use restriction. The volume diagnostic is an explanation of this sample, not proof of the provider's implementation, missing-trade absence or a global data-quality certificate.

**Recommendation A: qualified structural suitability, not financial dataset admission.** Continue to consider this archive format as one possible source. Its lack of independently verified historical eligibility, original receipt times, executable bid/ask/depth, provider checksums and a complete-history/delisting audit prevents certifying costs, C3 availability or research coverage. The approved quarter has served its QA purpose; do not expand acquisition automatically.


## B — isolated engine evidence and compatibility

The pinned stable version was installed in `/workspace/admission/nautilus-1.231.0/venv`, separate from bot_trader. Resolved package versions and actual synthetic results accompany the probe. No latest-v2 example is assumed compatible with this stable API. Synthetic fees/prices/order quantities are fixture inputs, not recommended market costs, capital or economic criteria.

[Actual results](../../phase-iv/admission/nautilus-results.json), [installation/attempt provenance and review clarifications](../../phase-iv/admission/nautilus-provenance.json), and the [resolved isolated versions](../../phase-iv/admission/nautilus-requirements-resolved.txt) are retained. The final suite contains **15 child-process cases: 14 meet their stated checks and one retains an adverse result**. These are technical cases, not independent financial experiments.

| Capability | Evidence | Conclusion |
|---|---|---|
| Runtime/dependencies | Python 3.12.14 on Linux actually executes 1.231.0. Installed metadata requires `pyarrow>=25.0.0`; production requires `>=19,<24` | **Current single-environment integration is incompatible.** Installed PyArrow 26 is isolated; do not change production locks. Prefer a separately versioned worker if later admitted |
| Orders/timing | Mechanical buy/sell sequence and native denial of sale before bought inventory arrives; queued positive latency resolves on a later data tick | Causal fixture passes; sparse ticks do not resolve exact sub-tick execution. No realistic latency calibration |
| Accounting/fees | Independent Decimal reconstruction of cash, inventory, positions and per-fill maker/taker fees; free + locked = total; cancel releases locked cash | Pass within invented spot/USD fixture and fixed rounding assumptions; no external venue statement or stablecoin conversion certification |
| Partial/no fills and rejection | Native IOC fills 1 of 4 units, cancels remaining 3; nonmarketable limit remains unfilled then cancels; marketable post-only rejected; cash/minimum/quantity-precision denials | Native cases pass. Changing a future execution policy to IOC requires its own scientific/economic justification |
| Finite visible liquidity | L1 market fixture displays one unit; engine fills 1 at 104 and remaining 3 at 104.01 | **Fails conservative finite-visible-liquidity requirement.** Model extrapolation beyond L1 is not observed depth. Neither full rejection of Nautilus nor admission of default execution realism follows; L2/queue/impact calibration remains untested |
| Duplicates | Duplicate submission adds no second order/fill; reinjecting the same native fill event leaves accounts/orders/positions unchanged | Narrow native execution-engine idempotency passes; reinjection is not another matching/liquidity test or proof against every external duplicate |
| Failure/replay | Deliberate exit 23 preserves external trace after a filled buy with an open position; separate roundtrip fixture repeats in a fresh process | **Recovery is not demonstrated:** no pending-order crash, durable checkpoint restore, continuation/reconstruction of the interrupted fixture or external reconciliation. The provenance note narrows overly broad wording in the original result |
| Resource smoke test | 10,000 invented ticks processed without orders | Technical scale check only; no training, strategy workload or throughput/capacity guarantee |

Stablecoin conversion, stale-feed admission, membership/exit failures, deeper-book realism, external account reconciliation and production authorization dispatch were **not tested** by this isolated probe. Future adapter-specific tests must cover them before dependent financial use. No new networking/authentication path, live client, scheduler or paper process was activated. Installed metadata declares LGPL-3.0-or-later; future distribution/integration obligations require review for the actual use.

**Recommendation B: retain Nautilus as a conditional isolated-engine candidate; reject immediate in-process installation and default L1 market-fill admission.** The bounded probe is complete with documented limits, not an engine admission certificate. No need to rebuild the platform or install another engine merely to increase coverage.


**Architecture consequence:** the present platform's `Execution.execute(...) -> Fill` and v1 ledger intentionally require a single complete synthetic fill. Native partial fills and asynchronous order outcomes require a separately versioned event/state boundary, accountable cash/inventory and idempotent reconciliation. Do not retrofit real rows under synthetic labels, remove the guard or claim that engine events already pass through production. Preserve experiment governance, transformations, inference and holdout custody in bot_trader. A later isolated engine worker with versioned inputs/outputs remains a coherent one-platform option; no full adapter was built now.

LEAN direct engine remains the documented fallback if a concrete Nautilus limitation blocks the required mechanism; it was not installed or benchmarked. Freqtrade remains a methodological/reference alternative. Neither swapping engines nor extending the existing synthetic ledger resolves missing historical source/quote/eligibility evidence. An approved fallback installation would have its own bounded scope.

## Resources and reproducibility

| Measured task | Wall / CPU | Peak RAM or retained storage |
|---|---|---|
| A successful acquisition | 32.65 s wall / 4.94 CPU s; initial failed HEAD separately preserved | 19.25 MiB RSS; 2,172,918,907 archive bytes retained |
| A full byte inventory + edge QA + reconciliation | 69.04 s / 68.92 CPU s | 25.52 MiB RSS; ~5.34 MB private inventory, no whole extraction |
| A separate volume diagnostic | 26.27 s / 26.26 CPU s | 23.75 MiB RSS; same files/windows, no new download |
| B install | 7.38 s; installer user + system 4.21 CPU s | 51.38 MiB installer RSS; this is not runtime RAM |
| B final 15-process suite | 9.52 s wall / 13.84 summed child CPU s | 411.60 MiB maximum child RSS |
| B all four preserved suites | 37.60 s wall / 49.49 summed child CPU s | Maximum 412.54 MiB child RSS; 935,501,824 allocated disk bytes for environment/cache/logs at consolidation |

CPU can exceed elapsed time because processes/libraries use multiple threads; RSS is a per-process high-water mark, not simultaneous total memory. Exploratory script time and documentation work were not fully metered. Initial B measurement-wrapper failure (`/usr/bin/time` unavailable) happened before installation and is preserved. Only successful isolated installation is claimed.


These are measured technical fixtures and archive-processing costs on this Linux cloud host, not an estimate of the 26-specification financial workload, personal Windows performance or ongoing service availability. Downloaded package sizes in installer output are rounded; no invented exact total network traffic or invoice is reported. No new paid service or billed subscription was arranged. Existing host/electricity and human engineering costs were not metered in USD. E3's complete fits/refits/seeds/stresses/uncertainty ledger remains unbound.

All raw archive bodies, detailed inventory and disposable environments stay outside Git under `/workspace/admission`. Versioned outputs contain methods, receipts, aggregate findings and synthetic results; no reconstructive market price series. Reproduction commands appear below. Re-running against already acquired files requires no fresh acquisition; acquisition refuses existing artifacts. A future environment that lacks the raw files must inspect permissions and recorded identities before re-acquisition, rather than silently downloading additional material.

## Future historical coverage and source extensibility

The quarter and Kraken are **technical sampling choices only**. The eventual research dataset should maximize scientifically useful, reliable and economically reasonable history across market cycles, subject to the hypothesis and observed data fitness. There is no fixed starting date, number of coins or exclusive provider. More history is useful only with comparable units, identities, timestamps and changing market structure; it does not automatically provide independent evidence.

| Future comparison dimension | Required evidence before dependent research |
|---|---|
| Historical depth and changing universe | Coverage by instrument/time; historical listing, delisting, migration and denomination records; inclusion of disappeared assets where obtainable; disclose survivorship gaps |
| Observation granularity and execution | Actual trades/bars/quotes/depth, time precision and availability; costs, liquidity, latency and product rules appropriate to the mechanism |
| Quality and revisions | Source versions, schema changes, independent cross-checks, gap/duplicate/correction handling; current corrected history is not a first-publication archive |
| Rights and economics | Permitted historical retention/research/model/derived-output uses, real-time access, acquisition and recurrent costs; free is preferred only when fit |
| Additional information | News/sentiment vintages and receipt times, on-chain finality/reorganizations, derivatives funding/margin/position definitions; separate typed adapters and source-specific QA |

Reuse the existing source comparison before targeted new research. Propose a finite acquisition manifest with purpose, marginal coverage gained, rights, sizes, storage/processing costs and exposed versus reserved intervals. **Every additional acquisition needs separate authorization.** No full-history download, new provider, premium licence or financial admission follows from this report. The inspected Q3 interval is exposed QA material, never a pristine final holdout.

## Material next decisions

1. **Do not choose E3/E4 numbers from these tests.** The tests provide source and engineering evidence, not a full research budget, attainable net advantage, suitable primary capital, materiality margin or risk limit. Retain USD 1,000/5,000/10,000 as sensitivities only. Historical fee/minimum/quote/capacity and source coverage evidence still condition the economic package.
2. **Next acquisition, if proceeding:** review a concrete, bounded comparative historical-coverage proposal addressing the observed gaps, rather than authorize all history or pick a permanent vendor. No purchase is currently recommended. Data access/use, any spending and additional technical scope must be explicit before action.
3. **Before empirical development:** review a prospective staged-admission clarification and the precise financial scope. Structural QA and synthetic order/accounting tests cannot estimate variance/dependence of paired candidate-minus-reference net returns. Development admission must therefore be distinguished explicitly from validation/final admission if that path is chosen. Keep finite search, prospective economic criteria, one validation admission and protected final data; no pilot is hidden in QA. Alternatively retain conditional methodological readiness and defer all empirical work.

Technical schema/parser choices and compatible adapters should be owned by the project within a later authorized scope; the user need not approve each field or library call. E1/E2 and A/B do not require repeat approval. UX, glossary and guide improvements remain recorded future work. The [acceptance gate](acceptance.md) continues to govern closure and any transition to Phase V.

## Evidence limits and preservation

The scientific corpus, H-00–H-24, C1/C3 priorities, C2 comparison, C4/C5 reserves and all seven zero financial counters are unchanged. Source documentation, observed structural facts, native engine behavior, harness-side controls and untested capabilities are distinguished. Negative findings are preserved; no economic strategy is accepted or rejected by these engineering checks.

## Reproduction and verification receipt

Use the existing approved local archives and isolated environment; these commands perform no downloads. Choose new scratch/result paths: the harnesses preserve prior artifacts. The engine suite exits **1** for the retained adverse L1 assertion; do not remove that check to obtain a green suite.

```bash
python -m unittest discover -s tools/admission -p 'test_kraken*.py' -v
python tools/admission/kraken_qa.py --archives /workspace/admission/kraken/archives --output /workspace/admission/kraken/qa-repeat --result /workspace/admission/kraken/qa-repeat-result.json
/workspace/admission/nautilus-1.231.0/venv/bin/python tools/admission/nautilus_probe.py --output /workspace/admission/nautilus-1.231.0/probe-repeat
```

These are reproducibility instructions, not additional repetitions performed for this delivery. The initial executed Kraken harness is preserved in commit `f548ed0`; the current harness adds explicit acquired-body binding and the separately recorded volume diagnostic. Both hashes and the original result digest are retained. The final Nautilus source matches its executed hash; earlier evolving harness snapshots were not retained, although their outcomes/digests remain in provenance. Resolved dependency versions and installed RECORD digests are not wheel hashes or a fully reproducible supply-chain lock.

[Verification receipt](../../phase-iv/admission/verification.json): nine offline guard/QA regression tests pass; executed-source hashes match; local document paths and JSON/JSONL parse checks pass. Scientific hypothesis/research bodies, protocol/candidate/data annexes, future UX, production code/tests/web/locks and financial freeze bindings are unchanged. Independent internal review identified and corrected the recovery overclaim, dependency-conflict interpretation and pair-set cardinality gap. This was internal review, not independent financial validation. The historical production test suite was not rerun or recounted.
