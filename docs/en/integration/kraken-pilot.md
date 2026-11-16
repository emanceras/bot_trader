# Finite Kraken pilot and Market Replay validation

Canonical English. Revision 1, updated 2026-11-16. [Español](../../es/integration/kraken-pilot.md).

**Validated within the first finite data-QA version:** a real five-minute capture completed and all 20 offline acceptance checks passed, including comparison with the original result after restart. This delivery continues `2316029`; D-061 records the user's explicit finite public-feed permission. It does not authorize financial experimentation, orders, permanent capture or Phase V.

## Scope and implementation

The existing route is unchanged: Kraken WebSocket v2 → `KrakenCaptureService` → `CaptureJournal` → local archive → exact normalization → Market Replay. BTC/EUR public `trade` and `ticker` with `event_trigger=bbo` are the only market subscriptions. The public instrument snapshot establishes instrument availability. Market Replay orders available information; it does not match financial orders.

Direct TCP opening was refused by this environment. A short diagnostic completed the verified TLS/WebSocket handshake through the environment's configured proxy without subscribing. The client now permits an **explicit** `HTTPS_PROXY` route only when its exact URL hash is bound to the immutable pilot configuration and approval. Credential-bearing proxy URLs are rejected; certificate/hostname verification and redirect denial remain enabled. Direct mode remains the default and ignores proxy environment variables. Omitted optional fields preserve previous configuration hashes. No dependencies or central contracts changed.

The existing `PilotApproval` mechanism records the user's instruction, actual host, configuration, private-use restriction and finite validity window. It is an operator declaration, not independent legal certification or a cryptographic user signature. After the interruption between November 15 and 16, a new host/window binding was recorded under the existing authorization; old records were retained. No new licensing research was performed. Original market messages, extracts and normalized artifacts remain outside Git in private workspace state.

The CLI now exits unsuccessfully when pilot acceptance fails, even when a valid partial archive can be inspected. The supervisor retains offline network denial by default; explicit public-pilot mode admits only the existing finite capture command. Its process-group watchdog reserves five seconds for controlled shutdown inside the outer bound. A discovered disk-sampling race is fixed: disappearing atomic temporary names are tolerated, and an unexpected monitoring failure terminates the owned child and preserves a failure receipt without private exception text.

## Attempts and retained failures

| Attempt | Observed outcome | Interpretation |
|---|---|---|
| `pilot-live-01`, November 15 | Three refused direct openings; zero frames; reconnect limit | Real attempted connection, no market capture. Original CLI exit 0 was misleading; acceptance was already false and remains preserved. |
| `pilot-live-02`, November 16 | 3,465 original messages; 3,288 market events; approximately 214 seconds of channel coverage | Incomplete. Original supervisor raised `FileNotFoundError` while sampling disappearing `pending.json`. Child reported `storage_failure`, confirmed local closure, unknown remote acknowledgement. Its original storage errno was not retained: the causal link between both errors is not established. |
| `pilot-live-03`, November 16 | Target duration reached; 2,449 original messages / 2,175 market events; acceptance passed | Same data/route configuration, fresh identity after the verified supervisor fix. Local closure confirmed; remote close acknowledgement unknown. |

The first concurrent inspection of attempt 02 failed and remains evidence. Offline inspection after closure verifies its committed prefix, original artifact hashes, exact timestamps, causal boundaries and restart determinism. It still fails overall pilot admission because it lacks the target duration/terminal completion. No original record was modified or removed. No pending write intent or corrupted committed record was found. Explicit offline recovery on the confirmed stopped partial writer returned no pending intent and did not reconnect. The corrected service records future storage-error type/errno without paths or payloads.

The failed supervisor did not write its resource receipt. Its source Git ref and command output survive; the reconstructed receipt marks unknown CPU/RSS/disk counters explicitly and charges the full 320-second allowance conservatively. This charge is not a measured execution duration.

## Verification and limits

The final run stopped automatically after its 300-second intake target. It retained **1,284,814 original application-message bytes**, 168 trade observations and 2,007 BBO observations. Effective observed channel spans were 297.010 s (trade) and 298.899 s (ticker); handshake time and a quiet tail are not market coverage. There were no recorded reconnects, duplicate trade deliveries, corrupted committed records or unresolved intents in this final run. These zeros do not prove upstream completeness. The offline report [records all 20 passing checks](../../integration/kraken-pilot/final-qa.json).

The latest full host regression passed **352 tests**. After the storage diagnostic/parser adjustment, 61 affected checks passed; a final serialization-compatibility check preserves the declared dependency range and existing configuration identities. Web unit tests (7), browser integration tests (2), web type checking/build, strict Python typing (45 source files) and scoped lint passed. Initial lint findings were corrected and preserved; the existing Starlette/httpx deprecation warning remains. Optional native engine/strategy-order campaigns are excluded from this data-QA task. Their prior evidence remains unchanged.

The offline verifier compares the original capture report with a fresh CLI process and a reconstructed service. It verifies the raw/envelope/index chain, configuration and approval binding, exact source timestamps, native EUR units, original-to-normalized provenance, trade duplicate semantics, observed BBO origin and unchanged checkpoints. It tests first/middle/last information boundaries, then resumes replay from those checkpoints. Market values are never printed. A partial or empty stream cannot pass merely because its hash is deterministic.

The completed pilot consumed **306.72 s wall / 11.04 s child CPU**, with **133.2 MiB sampled child RSS**. [Campaign resources](../../integration/kraken-pilot/resources.json) distinguish measured commands from the conservative 320-second charge for the failed supervisor and the two short connection diagnostics. The measured campaign RSS peak was 663.1 MiB (browser regression); temporary storage was about 55 MiB before public export. Failed-run peak counters and supervisor overhead are unknown, so these are not certified whole-campaign maxima. No software was downloaded and no paid service was used.

Observed update source-to-application ages had sample medians of 74.25 ms (trade) and 113.05 ms (ticker), and maxima of 203.86 ms and 5.644 s respectively. These are technical timing observations, not an execution-latency guarantee; neither network transit, local backlog nor clock offset is separately identified. The 50 trade snapshot observations were older, up to 91.03 seconds, and were admitted only at receipt.

Provider completeness remains unknown: no exchange-wide sequence or independent reference feed proves that every upstream event arrived. Ticker BBO price-trigger updates are not full order-book data or guaranteed size-only updates. Source-to-application-receipt age is not network latency; snapshots can contain old events. Kernel clock discipline reported synchronized, without an independent UTC-offset/error bound. Availability uses the existing application-receipt convention, not NIC arrival or a measured transformation delay.

Fault/reconnect/duplicate/corruption cases absent from the final real stream must remain identified as synthetic test coverage. First-version validation does not certify 24/7 operation, native Windows durability, crisis throughput, execution quality or financial merit. Private retention depends on this workspace; no paid hosting or external backup was activated.

## Reproduction and stop boundary

Use the already pinned optional `websockets==17.4` runtime. Default `capture-pilot` is a plan and opens no socket. A future capture still needs its own applicable scope and finite approval binding; this completed campaign does not start an ongoing service.

Offline inspection uses the retained private configuration and capture ID:

```bash
python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id CAPTURE_ID --config PRIVATE/config.json --inspect
python tools/integration/verify_pilot.py --state-dir PRIVATE \
  --capture-id CAPTURE_ID --config PRIVATE/config.json \
  --capture-report PRIVATE/original-command.log --output PRIVATE/new-qa.json
```

For a confirmed stopped writer, `--recover-stopped-writer` uses the existing recovery path without reconnecting. Never recover while another writer is active. Evidence snapshots contain code/configuration hashes, compact diffs and immutable Git refs, not copies of market data. [Budget](../../integration/kraken-pilot/budget.json) and [evidence](../../integration/kraken-pilot/evidence/pilot/) preserve executed successes and failures.

After this delivery, stop infrastructure expansion. E3/E4 economic decisions are the next objective; they remain pending. The 26 specifications, C1/C3, C2, C4/C5, staged admission and final holdout remain unchanged. No Phase V, paper/live trading or financial experiment was executed.
