# Kraken WebSocket capture and Market Replay

Canonical English. Revision 1, updated 2026-11-13. [Español](../../es/integration/kraken-ws.md).

This delivery implements a finite, simulated Kraken WebSocket v2 path for `BTC/EUR`: injected transport → raw journal → existing archive → normalization → data-only Market Replay. It continues `31c1b59` and `dc859e8`; it does not reopen engine selection. No actual socket connection, market acquisition, order, strategy, financial metric or new dependency is part of this delivery.

## Implementation and provenance

| Component | Implemented responsibility | Boundary |
|---|---|---|
| `CaptureJournal` | Original message bytes, receipt clocks, immutable receipt ordinals, hashes, source/configuration identity, bounded storage and explicit interrupted-write recovery | Local integrity does not certify upstream completeness or source truth |
| `KrakenProtocol` | Public instrument preflight; separate `trade` and `ticker` acknowledgements; explicit `event_trigger=bbo` request | Injected transport only; no admitted real WebSocket connector |
| `KrakenWSNormalizer` | Exact source timestamps/numbers, native trade identities, explicit symbol mapping, duplicate/conflict rules and provenance sidecars | Only the admitted BTC/EUR schema; unknown or ambiguous input fails closed |
| `KrakenCaptureService` | Existing artifact store, policy, archive and normalization composition | Technical development partition and simulated configuration only |
| `MarketReplay.inspect_capture` | Receipt-aware information ordering, deterministic prefixes and versioned replay checkpoints | No analytical signals, matching engine, PnL or financial admission |

Raw messages are retained before protocol interpretation, within the frame/storage limits. Every receipt preserves UTC and monotonic clock values; these represent delivery to the application, not the exchange or network interface. RFC3339 timestamps are converted exactly to integer nanoseconds. Binary floats, unsupported sub-nanosecond timestamps, conflicting trade identities, missing required event timestamps and event times after receipt are rejected rather than rounded, invented or clamped. A receipt-clock regression blocks normalization. Version `kraken-ws-v2-normalizer-v1` models information availability at application receipt, with zero extra decoding/processing delay; this is not a measured prospective decision latency. A frame delivered at the duration boundary is retained, then intake stops; a limit can end the pilot before its target duration.

The explicit mapping is source `BTC/EUR` → internal `BTC-EUR`. Source spelling, taker side/order type, exact timestamp text, frame/item identity and snapshot status remain in provenance. Prices remain EUR per BTC; quantities remain BTC. No EUR/USD conversion is implied, and the project's USD accounting basis is unchanged. Fixture quotes carry `synthetic_explicit`, not `observed` liquidity. Trades never become bid/ask observations.

Repeated identical native trade IDs retain each delivery but produce one logical event at its first receipt. Conflicting contents reject. Equal prices/timestamps with different IDs remain distinct. Ticker deliveries retain separate identities because the inspected schema provides no native sequence/checksum that proves duplication. Local receipt ordinals are not provider sequence numbers.

Reconnects use a new session and repeat instrument/channel admission. They leave an explicit unknown-coverage gap; the latest-50-trades snapshot cannot establish complete backfill. Trade-ID jumps are diagnostics, not proof of loss. Interrupted writes retain their intent and require explicit confirmation that the previous writer stopped before recovery. Recovery does not manufacture a missing frame or silently truncate history. Terminal capture retries do not open another transport.

A capture lease rejects concurrent collectors/inspectors for the same identity. The complete immutable configuration is stored under its content hash; reports link the durable journal checkpoint, archived manifest, normalization and replay artifacts. Upstream completeness remains explicitly unknown.

Capture replay uses the existing v2 contracts and shared ordering/identity logic. It has its own versioned checkpoint and data-class binding. The historical OHLC/trade QA route still rejects quotes. Receipt cutoffs and prefix reconstruction allow earlier information to be checked independently of later deliveries; this is information coherence, not a guarantee of market execution.

## Verification status

Executed: **70 focused tests pass**, including the final source revision; **260 backend regressions pass** (the focused tests are included, not additive). No native engine tests were rerun. Strict mypy passes across 42 source files after five annotation errors were corrected; the initial failing snapshot, output and diff remain evidence. The backend emitted one existing Starlette/httpx deprecation warning; no dependency was changed. A preparatory Ruff line-length finding in the new preservation script was corrected before its final check.

The final checks and resource receipts are in [the evidence directory](../../integration/kraken-ws/evidence/ws/). The [fresh technical budget](../../integration/kraken-ws/budget.json) is a self-imposed ceiling for this delivery, not a renewal of completed M/R/E permissions. Eight guarded commands used 18.57 s wall / 14.25 s CPU; peak sampled RSS 187.8 MiB and temporary storage 4.74 MiB (sampling is not a hard peak certificate). Active engineering is approximately 55 min across interrupted sessions, not precisely instrumented. Downloads, real connections and financial experiments: zero. [Resource summary](../../integration/kraken-ws/resources.json). Exported evidence and Git publication add a small footprint outside the execution samples.

To reproduce the focused tests in the existing locked environment, without any capture or dependency installation:

```bash
.venv/bin/pytest -q tests/test_capture_archive.py tests/test_capture_service.py tests/test_capture_replay.py tests/test_kraken_ws.py
```

The platform composition exposes `services.capture`; its only collector entry point is `run_simulated`, with injected finite transport and clock. `inspect` reconstructs archive/normalization/replay and can verify an earlier `CaptureReplayCheckpoint`. There is no live command or dashboard capture switch. Tests exercise composition with the existing platform store as well as isolated components. Ruff passes for src/tests and changed tools; the broader tools check retains two pre-existing findings in make_fixtures.py/verify_delivery.py. Neither historical file was rewritten. Preservation checks confirm 4,630 stable-environment files, core/scientific contracts and old evidence unchanged; published DECISIONS/EXPERIMENTS prefixes remain exact.

## Known limits

The transport and receipt clock are trusted injected interfaces, not a sandbox for hostile connector code. No real connector is shipped or admitted; there is no supported command that activates a live capture. Timeout/close behavior of an eventual socket client still needs separate admission. Current local durability relies on POSIX filesystem/locking primitives; Windows-native durability has not been demonstrated.

The bounded journal verifies prior raw content on append, producing cumulative O(N²) read work. This is acceptable for the small synthetic scope, not evidence of 24/7 throughput. Normalization/replay are bounded prefix operations, not unbounded streaming consumers. Record charging is a conservative local bound, not a measured traffic rate or a complete capacity forecast for all derived artifacts. A later sustained collector needs measured sizing, segmentation, storage lifecycle and recovery/load tests before deployment. The previous 24-hour proposal remains historical design, not implemented or authorized operation.

## Conditional procedure for a future supervised 5–10 minute capture

This procedure is **not executed or authorized by this delivery**. It depends on an admitted public WebSocket connector and separate approval of source, rights, host and finite resources. Do not enable live operation by changing a fixture's synthetic flag.

1. Recheck applicable Kraken terms for private public-feed retention from the actual host/jurisdiction. Preserve the terms/version and scoped conclusion; public access is not a blanket storage or redistribution licence. Resolve any material ambiguity before acquisition. No keys or funded accounts are required.
2. Implement/admit the minimal connector separately: TLS verification, bounded receive timeout/message size, immediate UTC/monotonic receipt stamping, close confirmation and recoverable disconnect behavior. Preserve raw frames privately. Verify host clock synchronization, persistent disk and process shutdown; no 24/7 purchase is necessary for a supervised pilot.
3. Freeze one duration, 300 or 600 seconds, and finite frame, record, disk/free-space and reconnect ceilings before activation. Current simulated defaults are 1,000 frames, 2,000 receipts, 1 MiB/frame and 64 MiB conservative journal charge; these are starting bounds to assess, not evidence that ten minutes will fit. Stop at the first limit. Approve a total private-workspace ceiling covering raw, metadata and derived outputs, not only journal charge. Use measured pilot rates for later sizing; no subscription/cloud fee has been quoted or authorized.
4. Perform the public v2 instrument preflight from that host. Require the exact online `BTC/EUR` pair with BTC/EUR base/quote metadata, then acknowledge `trade` and `ticker` subscriptions separately. Preserve the request for `event_trigger=bbo`. An explicit conflicting trigger rejects; the documented acknowledgement does not guarantee an echo of that parameter, so absence must be recorded, not invented as confirmation.
5. Supervise the finite capture. Record receipt clocks, hashes, session transitions, acknowledgements, unsupported messages, disconnects and stops. `bbo` describes best bid/offer **price-level changes**, not every size-only update or complete order flow. Never repair an unknown gap by inference or an unapproved REST download.
6. Close intake, confirm transport shutdown, flush durable metadata and preserve any unresolved intent. Verify raw hashes and replay checkpoint reconstruction after restart. Normalize using a distinct real-data declaration and observed quote provenance, not the simulated service's mode. Keep all market contents private; publish only approved technical aggregates. Evaluate clocks, coverage, resource use and recoverability, without strategies, PnL or financial statistics.

A later 24/7 deployment requires an always-on supervised process, reliable outbound TLS, synchronized clocks, persistent disk, explicit retention, disk/clock/connectivity alerts and measured recovery behavior. A personal computer can pause or lose connectivity; a VM introduces costs and operational dependencies. Neither is selected here.

## Sources and scientific boundaries

This delivery reuses the directed official-document findings and hashes in [the source record](../../integration/kraken/sources.json), inspected 2026-11-11, and the [historical capture specification](../../integration/kraken/capture-spec.json). No new broad research is needed. Relevant originals: [ticker](https://docs.kraken.com/api/docs/websocket-v2/ticker/), [trade](https://docs.kraken.com/api/docs/websocket-v2/trade/), [instrument](https://docs.kraken.com/api/docs/websocket-v2/instrument/), [WebSocket introduction](https://docs.kraken.com/api/docs/guides/spot-ws-intro/) and [EEA terms](https://www.kraken.com/legal/eea-terms). REST's previously observed spot listing is not a successful v2 subscription or proof of access from the future host.

E3/E4 economic decisions remain pending. C1/C3, C2, reserves C4/C5, the 26 specifications, T/D/U/V/F and holdout restrictions are unchanged. Phase V, paper/live trading and financial training remain unauthorized.
