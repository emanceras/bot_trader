# Temporal contracts, multiple resolutions and historical/live equivalence

Document ID: IV-EVOL-TIME-001 · Version: 1 · Date: 2026-10-27 · English canonical. [Spanish](../../../es/phase-iv/evolution/temporal.md).

**Documented proposal; no implementation or financial admission.** Extend the accepted modular platform through versioned event and instrument contracts, with one causal transformation specification used by historical replay and future streaming. Keep the current synthetic v1 records and their results intact. The [source comparison](sources.md), [engine assessment](engines.md), [external-information proposal](external-information.md) and [staged-admission proposal](staged-admission.md) set complementary boundaries. E3/E4 and Phase V remain pending; C1/C3 primary, C2 secondary, C4/C5 reserves and the 26 base slots are unchanged. No market stream, new dataset, installation or financial test was used for this document.

## What exists and what must change prospectively

The current [v1 contracts](../../../../src/bot_trader/core/contracts.py) use Python `datetime` normalized to UTC, positive OHLC prices, one interval in seconds, and an ordered chain of known event/publication/provider/receipt/transformation timestamps. `Instrument` is explicitly synthetic and has base/quote currencies plus a product label; listing `future`, `perpetual` or `option` does not implement their economics. Existing [temporal preparation](../../../../src/bot_trader/lab/temporal.py) and finite synthetic transformations support narrow availability/purge checks. They do not establish market-feed equivalence, arbitrary-resolution aggregation, venue calendars or recovery after an actual outage.

A future v2 should retain the useful immutable/versioned boundaries while separating source observations, instrument definitions, transformations and simulated assumptions. Real clocks can disagree; scheduled information can be published before its effective event. Do not force such facts through v1's monotone timestamp chain, silently clip their values or relabel real rows synthetic. Admission must decide whether a particular clock/identity ambiguity prevents a dependent calculation.

## Minimum event and identity contract

These are proposed record requirements, not implemented schemas or a mandate for new services.

| Component | Proposed contents and invariant |
|---|---|
| Immutable provenance | Source and channel, venue, schema/version, raw object/message digest and locator, ingestion/normalization version, rights/scope reference. Keep originals and corrections addressable; a normalization does not replace the source |
| Identity | Source-native event ID and its documented uniqueness namespace, connection/session and sequence when supplied; separate internal immutable ID. An identical timestamp/price/quantity is not sufficient for deduplication. Repeated delivery and two equal-valued trades are different cases |
| Instrument reference | Venue-qualified instrument ID plus effective and known-time version of the security master; raw symbol retained. Base/quote/settlement currencies, quantity and price units, tick/lot sizes and product subtype are explicit. Renames, migrations, contract replacements and delistings do not rewrite historical identities |
| Clocks | Distinct event/effective time, first publication, provider receipt/availability, local receipt, and transformation availability when actually known. Each carries clock domain, unit/precision, provenance and known accuracy/uncertainty or an explicit unknown. A calendar event's scheduled time is distinct from its release timestamp |
| Event meaning | Typed trade, quote, book snapshot/delta, bar update/close/correction, status, reference-data or external-information event. Preserve native fields and documented side/role, depth, sequence and finality; common names do not prove common semantics |
| Versions and missingness | Revision/cancellation relationship, known-time validity and effective-time validity, original versus corrected view, missing-data/gap reason. Unknown, unavailable, not applicable, no trades and zero measured quantity remain distinct |

Preserve source time as **integer epoch ticks plus declared unit/time scale**, with original representation and zone/offset metadata where relevant; validate range and conversion overflow. Do not convert through a floating-point epoch or Python `datetime` when that loses submicrosecond information. A display timestamp may be lower precision if labelled and never reused as the ordering key. Civil-time/calendar calculations require a named zone and pinned rule version, beyond an instant expressed in UTC. Declare leap-second/smear policy where relevant; an unsupported representation must be identified rather than silently normalized.

This is a concrete interoperability concern: DuckDB 1.5 documents microsecond `TIMESTAMPTZ`, no nanosecond zoned timestamp type, and precision loss when reading external zoned nanosecond columns [T3]. It also notes that `TIMESTAMPTZ` does not preserve the original zone. Keep canonical integer ticks/unit and zone metadata through Arrow/Parquet and the process boundary; convenience SQL timestamp views cannot be the sole source of truth. Arrow interoperability documentation [T4] establishes available object interfaces, not lossless roundtrip for the project's exact dependency pair. Later synthetic checks must inspect values, units, schema metadata and hashes across the actual versions.

Source-specific adapters must make explicit, for example, that Kraken WSv2 trade `side` denotes the taker whereas Coinbase Exchange `match.side` denotes the maker [T5,T6]. A canonical aggressor side is a derived field with a documented mapping. Binance WS time defaults to milliseconds, optionally microseconds [T7]; its spot archive's microsecond change from 2025 is retained in the [existing source assessment](sources.md). Neither numerical magnitude guessing nor an identically named timestamp establishes its unit or meaning. Kraken subscription acknowledgement `time_in/time_out` cannot fill per-trade operator receipt [T5].

## Availability, revisions and causal joins

For a decision at cutoff `t`, admit only the versions whose **specified availability to that decision process** is at or before `t`, under an explicitly declared boundary/tie policy. The event's economic date alone is insufficient. For a derived output, availability cannot precede any required input's availability or completion of the transformation. Queueing, inference and calculation time belong in the full delay path when material.

Maintain two separate tracks: measured clocks and a versioned latency/availability scenario. Historical data without operator receipt cannot be presented as observed live delivery. A documented release-time lower bound plus an assumed delay is a model with uncertainty, not recovered truth; unknown release time is not repaired by adding an arbitrary delay to an event date. If the information need cannot be supported, mark the comparison not evaluable or restrict the claim. Record whether a replay represents collector receipt, operator receipt or a stated simulation.

Use bitemporal lookup: effective time describes when a fact applies; known time describes when that version became available. A later correction can change the latest descriptive history while leaving earlier decision records unchanged. Cancellations, recovered messages and historical backfills enter the decision journal at their actual later receipt, without being backdated to the missed event. Archive acquisition time is provenance for a present download, not the original market-information receipt.

Cross-asset, FX and external-information joins must be as-of on availability with a declared maximum age/missingness rule and common decision cutoff. Never match the nearest future observation, forward-fill across an invalidated book/session without a stated rule, or treat a stale quote as current liquidity. Preserve provider versus venue identities and USD conversion lineage; USDT/USDC values are not automatically USD. Different clock precision or unsynchronized sources may leave true cross-venue event order unknown. A deterministic merge order supplies reproducibility, not evidence that this was the true global market sequence.

## Multiple resolutions without future information

Keep one admitted event history and versioned aggregation recipes. A recipe binds price basis (trade/bid/ask/mid), event type, interval boundaries, anchor/calendar, session segments, ordering, missing-data handling, quantities/units, availability and correction policy. Time bars, event-count bars and volume bars have distinct closure conditions; changing the recipe is a recorded research choice, not a free new experiment.

Use half-open intervals `[start, end)` as the common convention, with explicit mappings for provider-inclusive endpoints and separately defined auction events. A trade exactly at `end` belongs to the next interval under this convention. Interval end is not proof of data completeness or immediate availability: a closed-bar output needs the closure evidence/watermark and declared delay policy. Preserve provisional/open bars as separate evolving versions; never expose their final high/low/close/volume before those values were known. If a future strategy consumes a partial bar, replay its actual partial state and receipt schedule.

Coarser bars may be built from complete finer bars only when anchors, boundaries, session masks, price basis and units align. Otherwise use admitted underlying events or declare the result unavailable. A coarse high/low or event path cannot reconstruct finer bars. OHLC order comes from the stated sequence, volume sums use their actual unit, and exact traded notional requires the sum of trade price × quantity with the applicable contract/unit formula. Close × volume is not a substitute for C3's exact amount. Corrections and duplicates must not inflate sums; true equal-valued trades must not be discarded.

At a decision cutoff, a multi-resolution feature can use each last eligible closed bar and/or a separately specified eligible partial state. Record each input's vintage, age and completeness. A daily value joined onto intraday rows before daily completion is leakage. Lagged/as-of alignment and explicit warm-up are required; normalizers, imputation, feature selection and model fitting remain training-only under the accepted protocol.

Choosing a 5-, 15- or 30-minute interval, an opening window, lookback or decision cadence changes the scientific design and consumes its finite budget. These are possible configurations, not a grid approved here. Mechanism, availability and friction requirements from [HORIZONS](../../../phase-ii/HORIZONS.md) still precede selection; observation, formation, prediction, holding, decision, execution and risk horizons remain separate. No H-25/H-26, opening-candle strategy, new market or extra slot is added.

## Session calendars and future product scope

Bind venue/product calendar, named time zone, tzdb and calendar versions, trading date, regular/extended sessions, auctions, scheduled breaks, holidays, early closes and observed halts. Sessions spanning midnight need a trading date separate from the UTC date. Keep unscheduled status events and calendar revisions with their knowledge times; do not assume a modern calendar reproduces every historical session. A 24/7 market still has venue outages, maintenance and instrument-specific lifecycle events.

NYSE's official page gives a core 09:30–16:00 Eastern Time session and specified 13:00 early closes [T1]. It also distinguishes auctions and extended sessions. Thus an illustrative opening window anchors to the relevant actual session opening in `America/New_York`, with DST conversion, rather than one fixed UTC hour. This is a calendar illustration, not evidence that any opening strategy works or permission to add equities. IANA documents periodic updates to historical UTC offsets, zones and daylight-saving rules [T2]; the inspected page identifies release 2026e, but no tzdb package was downloaded, installed or selected. A time-zone database is not an exchange holiday/halt calendar.

| Future subtype | Additional contract/interpretation needed before use |
|---|---|
| Spot crypto | Venue listing/delisting and token/unit migrations, base/quote and fee units, transfer/custody scope; 24/7 does not imply uninterrupted observations |
| Equities / ETFs | Effective and known corporate actions, listing/share-class identity and venue sessions; separate raw, split-adjusted and total-return views with vintages. Dividends, ex/pay dates and actual cash entitlements belong in accounting, not an unlabelled corrected price |
| FX | Pair orientation, base/quote and pip/lot units, venue/feed scope, sessions/rollover and settlement convention. Decentralized feed/tick volume is not automatically global traded volume |
| Cash indices | Constituents/methodology and publication/revision clock; index levels and synthetic continuous series are informational, not directly orderable instruments. An ETF, future or other exposure has separate identity, costs and basis |
| Futures / perpetuals / options | Actual contract identity, expiry/exercise, multiplier, tick/lot, margin/collateral, settlement and funding rules as applicable; underlying and settlement currencies explicit. Contract rolls and continuous-series adjustment recipes remain distinct from executable positions and cash flows |

Price-domain constraints are product-specific. A future market contract may need zero/negative prices; globally requiring positive prices or taking log returns would then be invalid. Do not relax v1's synthetic positive-price definition to pretend that subtype support is complete. Continuous futures back-adjustments and later corporate-action adjustments can revise earlier values; their adjustment vintages cannot silently enter an as-known replay. Multiasset design readiness does not establish data rights, legal access, operational capability or a wider financial universe.

## One causal path, three distinct equivalence claims

Historical batch and future streaming should use the same versioned normalization, state transition, feature and decision functions with frozen parameters, model artifacts and numeric conventions. Batch execution may process bounded chunks, but must reproduce the same arrival journal, causal ordering and state boundaries. Sorting a complete file by event time before replay is not equivalent to observing delayed/out-of-order arrivals. Watermarks and idle-source timeouts advance only from information then available; a complete file's future maximum timestamp cannot certify a past bar.

Preserve documented source sequences and local receive order. Resolve equal timestamps with an explicit deterministic tie policy using available sequence/connection/message ordinals and stable identities; report unresolved ambiguity and materially different admissible orders. A late-event policy binds buffering allowance, provisional versus finalized output, correction emission and state invalidation. A late correction can affect future decisions under that policy; it cannot rewrite a decision already made. Freeze the output manifest, dependency versions, initial state, partition/recipe hashes and decision journal for a replay.

| Equivalence level | What a later technical pass could establish | What it cannot establish |
|---|---|---|
| Information | Given the same recorded arrivals, clocks, versions and adapters, both paths expose the same eligible information at each cutoff | That an archive contains unknown original receipt times, revisions or missing messages |
| Decision | Given equivalent information, initial state, model/configuration and permitted numerical tolerance, both paths produce matching features, risk checks and decisions | That a historical model predicts well or that live software will never fail |
| Execution / fills | The same submitted intents are accounted for consistently under a stated simulator or recorded execution journal | Identical historical/live fills, queue rank, impact or net returns; hypothetical market responses and counterfactual fills remain uncertain |

These levels must be reported separately. Replaying one's captured live journal later could support information/decision checks after separately authorized collection; this document neither starts that collection nor equates another provider's arrival history to the user's environment. Engine transport compatibility and synthetic full fills do not satisfy execution realism.

## Proposed acceptance checks and failure behavior

All checks below are **future technical acceptance work, not executed results**. Begin with small synthetic adversarial journals in a later authorized adapter scope; financial histories and actual market collection have separate permissions.

1. **Precision/identity roundtrip:** equal displayed times but different fine ticks; milliseconds versus microseconds; duplicate delivery versus distinct equal-value trades; renamed instruments and revisions. Assert lossless canonical values and deterministic IDs through actual Arrow/Parquet/SQL/process versions, and explicit failure on lossy unsupported conversion.
2. **Prefix invariance:** a run on an arrival prefix must have the same already-emitted decisions as the matching prefix of a longer run. Add future bars, corrections and delayed events; verify earlier decisions cannot change. Compare event-by-event and bounded batch/chunk execution with frozen inputs, initial state and configuration.
3. **Aggregation/calendar cases:** boundary trades, open/final/revised bars, missing intervals, unequal session lengths, DST ambiguity/nonexistent local times, early closes, midnight sessions and halts. Compare direct versus fine-to-coarse aggregation only where their declared conditions coincide.
4. **Causal multi-input cases:** delayed publication, clock skew, missing receipt, stale FX/quotes, external revisions and different resolutions. Assert that unknown or late data cannot enter earlier decisions; numeric tolerances must be justified before comparison and cannot hide availability or accounting differences.
5. **Disruption/recovery:** sequence gap, checksum mismatch, disconnect, duplicate recovery, unavailable snapshot, restart with pending state and replay from a durable checkpoint. Stop dependent decisions or apply an explicitly admitted degraded policy; invalidate stale book state and reconcile before resuming. Separate timer/heartbeat events and recovery arrivals must replay consistently. An intentional crash trace is not proof of restoration.

Future circuit checks must bind stale-feed limits, clock/sequence integrity, risk and order-state uncertainty to the relevant product and decision cadence; no universal numeric thresholds are invented here. Recovery requires known-good source state, idempotent event handling and independent position/cash/order reconciliation where applicable, with unknown outcomes retained. After an outage, queued decisions and orders need fresh eligibility/risk review; clearing a warning is not permission to replay stale intents. Keep incident/correction lineage and the conservative stop path. Exact operational policies and their technical authorization belong with the first admitted adapter, before any paper/live permission.

## Sources and limits of this review

Cached official documentation was retrieved on 2026-10-26 and examined on 2026-10-27; no new retrieval was needed. The [temporal ledger](../../../phase-iv/evolution/temporal-sources.jsonl) preserves original retrieval receipts and the actual read/reuse scopes. This is directed documentation review, not empirical evidence, a feed test or exhaustive legal/calendar verification. Source versions and hashes identify inspected snapshots; a mutable web page is not a permanent service guarantee.

| ID | Source and examined scope |
|---|---|
| T1 / EV-TIME-01 | [NYSE holidays and trading hours](https://www.nyse.com/markets/hours-calendars): core sessions, auction/extended-session distinctions, holidays and early closes shown for 2025–2027; no historical calendar dataset or rulebook examined |
| T2 / EV-TIME-02 | [IANA time zones](https://www.iana.org/time-zones): purpose, update policy and release identification; no linked tzdb release or implementation examined |
| T3 / EV-DEP-06 | [DuckDB 1.5 timestamp types](https://duckdb.org/docs/1.5/sql/data_types/timestamp.html): precision table, zoned nanosecond warning and zone-storage/binning semantics; not an installed-pair test |
| T4 / EV-DEP-05 | [DuckDB 1.5 SQL on Arrow](https://duckdb.org/docs/1.5/guides/python/sql_on_arrow.html): Arrow table/dataset/scanner/RecordBatchReader interfaces; interoperability availability does not prove exact semantic equivalence |
| T5 / EV-DATA-01 | [Kraken WSv2 trades](https://docs.kraken.com/api/docs/websocket-v2/trade/): taker side, per-book trade IDs, event timestamp and subscription acknowledgement clocks |
| T6 / EV-DATA-04 | [Coinbase Exchange channels](https://docs.cdp.coinbase.com/exchange/websocket-feed/channels): match maker-side definition and example; broader channel limits remain in the source comparison |
| T7 / EV-DATA-03 | [Binance spot streams](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md): default/optional timestamp units, raw/aggregate trade clocks and kline boundary semantics; no stream subscribed |

The proposed contracts, bitemporal treatment, replay conditions and acceptance cases are engineering recommendations from these constraints and the existing architecture. They are not claims that the sources implement the entire proposal or that future multiasset strategies have demonstrated value.
