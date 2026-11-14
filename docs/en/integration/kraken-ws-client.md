# Kraken public client and incremental journal

Canonical English. Revision 1, updated 2026-11-14. [Español](../../es/integration/kraken-ws-client.md).

This delivery continues `a5e9997`: a real-client implementation feeds the existing `KrakenCaptureService` → `CaptureJournal` → archive → normalizer → Market Replay path. Execution remains restricted to simulated tests. No Kraken connection, market acquisition, strategy, financial backtest or continuous service has been started. The [previous simulated report](kraken-ws.md) remains historical evidence.

## Implemented boundaries

`KrakenWebSocketTransport` uses the optional, pinned `websockets==17.4` package. The library handles WebSocket framing and TLS; the adapter admits only `wss://ws.kraken.com/v2` and the existing public instrument, trade and ticker subscription requests. Certificate/hostname verification is enabled. Redirects, proxies, compression and private/order methods are disabled. The adapter owns a private asyncio loop behind the existing synchronous transport port; import and construction do not open a connection.

Opening, sending and closing are bounded to 10, 2 and 3 seconds respectively. Messages are limited to 1 MiB, with a one-frame queue high-water mark and library flow control. This is not a claim that every network buffer contains at most one frame. Short receive polls do not themselves cause reconnection. Independent handshake and idle deadlines default to 15 seconds. Reconnection remains the existing bounded service policy, with new session identity and instrument/channel admission each time.

The initial instrument snapshot must establish the exact online `BTC/EUR` pair. Sparse updates preserve omitted metadata; explicit identity changes or offline status reject. The ticker request uses `event_trigger=bbo`; absent acknowledgement echo is recorded, while an explicit conflicting trigger rejects. BBO means price-level changes, not complete order flow or guaranteed size-only updates.

UTC and monotonic receipt times are sampled immediately after delivery to the collector and before parsing. They are **application delivery/dequeue times**, not exchange or NIC receipt times. Original application-message bytes, exact source timestamps and native identities remain preserved. The normalizer's receipt-based availability convention does not include an independently measured processing delay. EUR and BTC units remain native; no implicit USD conversion is added.

Close outcomes distinguish a graceful acknowledgement from confirmed local closure with unknown remote acknowledgement. The latter may allow a fresh session without claiming the old session ended gracefully. An unconfirmed local close is a failure. OS DNS work can outlive asynchronous cancellation; the finite command therefore requires an external process watchdog for a hard wall-time bound.

## Journal improvement and integrity

The persisted `raw-receipt-journal-v1` schema is unchanged. A single active writer caches validated counters, session clocks and the committed boundary. Appends/checkpoints no longer scan or hash the entire preceding history; normal capture work is linear in the number of records, with constant work per append for bounded message size.

Full content verification still runs at open, explicit audit, inspection, recovery and an externally changed index. Writer handover may therefore require a full audit. Earlier immutable content is trusted between audits: historical in-place corruption is detected by the next full audit/restart, rather than by every append. Latest-boundary corruption is checked immediately. This is a stated verification tradeoff, not protection against a malicious administrator. The existing exclusive capture lease, append-only indexes, pending-write intents, hashes and explicit recovery remain in use.

This removes the demonstrated O(N²) hot path; it does not establish 24/7 throughput, native Windows durability or unlimited retention. POSIX filesystem/locking assumptions remain.

## Approval, command and pilot limits

`capture-pilot` defaults to a local plan with `network_contacted=false`. Execution requires a separate approval record matching capture identity, exact configuration hash, host, rights reference and time window. The supplied [approval template](../../integration/kraken-ws-client/approval.template.json) has `approved=false` and an expired window. It is not an authorization. An approval record is a traceable declaration by the local operator, not a cryptographic proof that the user approved it.

Use a dedicated private directory outside Git in place of `PRIVATE`. The following command only prepares the plan:

```bash
.venv/bin/python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id kraken-btc-eur-001 \
  --config docs/integration/kraken-ws-client/pilot.json
```

Before an authorized pilot, provision the pinned optional extra in the intended isolated environment with `uv sync --frozen --extra capture`; initialize metadata there with `bot-trader --state-dir PRIVATE migrate` when needed. This delivery installed the extra only under `/workspace/kraken-ws-real-dev/deps` for tests. Existing installed platform dependencies were not replaced; the optional extra and its hashes are recorded in `pyproject.toml`/`uv.lock` and [the dependency receipt](../../integration/kraken-ws-client/dependency.json).

The [pilot configuration](../../integration/kraken-ws-client/pilot.json) proposes 300 seconds; 600 seconds is also supported after freezing a new configuration and approval. It stops at the first applicable boundary:

| Limit | Initial value |
|---|---:|
| Intake duration | 300–600 seconds |
| Raw messages / journal records | 10,000 / 20,000 |
| Message size | 1 MiB |
| Conservative journal charge | 64 MiB |
| Required free-disk reserve during journal writes | 128 MiB |
| Market-row stopping threshold | 8,000 |
| Normalization/replay artifact size | 32 MiB per artifact |
| Reconnects | 2 |

A message is not truncated to meet the market-row threshold: the final indivisible message can contain up to 1,000 rows. The normalizer/replay ceilings still apply. Limits may stop acquisition before five minutes; this is an incomplete pilot duration, not successful completion of the target window. Journal and bounded derived artifacts fit a conservative logical envelope below 256 MiB for this finite path; this is not a filesystem quota or a bound on concurrent disk users. Monitor actual free space and keep outputs private.

**Future command only, after separate approval and host/rights checks:**

```bash
timeout --signal=TERM --kill-after=5s 320s \
  .venv/bin/python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id kraken-btc-eur-001 \
  --config docs/integration/kraken-ws-client/pilot.json \
  --approval PRIVATE/approved-pilot.json --execute
```

Use a 620-second outer watchdog for a 600-second configuration. Confirm GNU `timeout` behavior on the actual host before activation. SIGINT/SIGTERM request controlled stopping; forced termination can leave an unresolved intent, which must not be silently discarded.

Adding `--inspect` to the plan command performs offline integrity/normalization/replay inspection. `--recover-stopped-writer` performs offline journal recovery only after explicitly confirming the former writer is stopped. Offline recovery does not require a renewed execution window and does not reconnect. Starting or resuming acquisition still requires a currently valid approval. Keep the configuration and approval records with the private capture evidence. The approval artifact hash is recorded durably before intake; terminal retries add no new authority or messages.

## Verification and readiness

**Executed:** 127 focused tests pass on the final functional revision; the earlier full backend regression passed 311 tests before the last six focused cases and their fixes were added. These suites overlap and are not additive. Strict mypy passes across 45 source files, and Ruff passes for source/tests and changed tools. Two failed typing checks remain preserved: six initial findings, then eight after an incomplete annotation correction. No behavioral expectations were relaxed. The backend's existing Starlette/httpx warning remains; no existing package version was changed.

The tests include the actual transport class composed end to end with invented asynchronous peers; there is no real server, TCP/TLS negotiation or Kraken subscription. Doubling the journal workload from 20 to 40 records keeps artifact reads below 2.2 times and performs no directory rescan per append; full audit still verifies each record. Corruption, writer handover, interrupted writes, restart, approvals, row/time limits, disconnects, private-request denial and causal replay are covered. Successful terminal retries preserve their acceptance result; cancellation during opening sends no subscription; offline recovery needs no renewed network permission. Rejected TLS/opening is recorded without falsely claiming an offending raw message was received; decoding failures retain their actual original bytes.

[Reproducible evidence](../../integration/kraken-ws-client/evidence/client/), [resources](../../integration/kraken-ws-client/resources.json) and [fresh bounded check budget](../../integration/kraken-ws-client/budget.json): nine guarded commands, **30.98 s wall / 23.19 s CPU**, peak sampled **222.2 MiB RSS / 7.09 MiB temporary files**. Engineering is approximately 45 active minutes across interrupted sessions, not precisely instrumented. Check children denied IPv4/IPv6 sockets. The optional wheel was installed earlier in the isolated target; guard receipts describe their own offline execution, not the entire delivery's software acquisition. Zero financial datasets, Kraken connections or financial experiments. Sampling and exported evidence/Git overhead are distinguished in the resource record.

The preservation audit confirms all 36 prior third-party lock entries, 4,630 installed environment files, central contracts, scientific files and prior evidence unchanged. Published decision/experiment prefixes remain exact. Only the optional client extra was added to the lock.

Reproduce the current focused suite after installing the pinned optional extra in an isolated development environment:

```bash
.venv/bin/pytest -q tests/test_capture_archive.py tests/test_kraken_ws.py \
  tests/test_capture_service.py tests/test_capture_replay.py tests/test_public_capture.py \
  tests/test_capture_cli.py tests/test_kraken_transport.py
```


The technical acceptance report separately checks archive/replay integrity, observations from both trade and ticker, completion of the target duration, and confirmed local shutdown. `technical_qa` alone is not a completed pilot: an empty valid prefix after a failed handshake cannot satisfy those criteria. Disconnects, missing coverage and unknown provider completeness remain explicit; replay determinism does not repair them. No returns or financial admission are evaluated.

The implementation has passed the authorized simulated validation and is technically prepared to request a first supervised pilot. No material code blocker remains identified within this tested scope; this is not permission or evidence of successful live connectivity. Execution still depends on applicable private-retention rights, the actual host's clock synchronization and storage, the pinned runtime, an effective watchdog and explicit user approval. Actual TLS negotiation, host access, provider schema/traffic and observed latency can only be checked during that separately authorized pilot. Do not execute while those prerequisites remain unbound; the shipped approval template deliberately cannot authorize a connection.

E3/E4 economic decisions, the 26 specifications, C1/C3, C2, C4/C5, T/D/U/V/F and holdout restrictions are unchanged. Phase V, paper/live trading and financial experiments remain unauthorized.
