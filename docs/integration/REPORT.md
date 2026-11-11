# First integrated synthetic path

Completed within the bounded technical scope on 2026-11-11. The existing platform now runs **immutable local archive → normalization → causal replay → incremental analytics → fixed synthetic signal → native execution → ledger and independent Decimal oracle**. This is neither evidence of investment performance nor unconditional engine admission.

| Milestone | Published revision | Delivered |
|---|---|---|
| H1 | `889ef23` / `slice-h1` | Immutable local import/resumption, provenance and exact-time v2 contracts alongside v1 |
| H2 | `64929d6` / `slice-h2` | Availability-ordered replay, incremental trade buckets, closed-bar indicator and fixed synthetic signals |
| H3 | `d3048f7` / `slice-h3` | Integrated service/CLI, isolated native lifecycle, ledger and independent oracle |
| H4 | `slice-h4` (resolves to this milestone's commit) | Adversarial boundaries, future-information native canary, CLI persistence and final regression |

The service reuses the existing artifact store, access policy, metadata database and audit log. Source, normalized batch, replay, immutable configuration, native request/journal and accounting result have separate identities and links. Replay orders information; Nautilus performs matching. No parallel matching engine was introduced.

## Executed results

The final backend suite passed **159 tests**. Three H3 integration tests passed in four native contexts: identical full runs twice, partial/cancel/sell, and insufficient-balance rejection. Two H4 tests passed in two additional native contexts: changed future information and the actual CLI path with persisted document/audit entries. These counts describe overlapping test layers, not independent financial observations. Host Ruff and mypy passed; the dynamic native API worker is explicitly excluded from mypy error checking. One existing Starlette/httpx deprecation warning remains; no dependency was changed to suppress it.

| Synthetic case | Native observation | Independent reconciliation |
|---|---|---|
| Full round-trip, repeated | Buy 1 at 105.05, sell 1 at 106.95; each fee 0.21 USD | Cash 1001.48 USD from 1000; inventory and reservations zero; identical canonical native results |
| Partial buy and cancellation | Buy request 2 fills 1; remaining 1 is canceled with native confirmation; later sell 1 | Same cash/inventory as above; quantity, remnant and terminal states agree |
| Insufficient cash/inventory | Both market requests denied; no fills | Cash 50 USD unchanged, inventory and reservations zero |
| Future-data perturbation | Future trade/closed-bar values change; earlier BUY signal and native fill remain identical | Earlier semantic result preserved; later signal and full source hashes correctly change |
| Platform CLI | Import, replay, native execution and reconciliation return `reconciled` | Result document and audit entry persisted in the platform database |

These are accounting identities on invented prices, not returns or economic results. Native fills are bound to journal events; final balances, positions and orders are bound to journaled snapshots. The oracle independently sums raw fills rather than reusing ledger totals. A hash chain detects specified mutations; it does not prove source truth, completeness against an exchange or resistance to a malicious administrator.

## Acceptance against the eight requested criteria

| Criterion | Implemented and executed evidence | Boundary of the conclusion |
|---|---|---|
| 1. Determinism | H3 full-a/full-b canonical equality; replay/checkpoint tests | Same frozen synthetic input/configuration/runtime; logs and filesystem paths need not be identical |
| 2. Causal availability | Closed/open/revised bar tests, eligibility checks, prefix replay and H4 native future-value canary | No historical/direct-feed parity claim; provenance hashes may change when an enclosing raw file changes |
| 3. Original integrity and provenance | Chunk hash/resume/source-manifest checks, separate normalized/replay/native artifacts | Local bounded import only; rights are declared and retained, not legally certified by a hash |
| 4. Exact time and identity | Integer ns/unit/range rejection, explicit label conventions, v1 round-trip, native precision gate | v1 → v2 → v1 is tested; v1 cannot represent every v2 field. Retain the original v2 envelope when exporting a legacy view |
| 5. Traceable accounting | Native full/partial/cancel/rejection, bound journals, posting ledger and independent Decimal oracle | Synthetic SYNTH-USD and the declared execution assumptions only |
| 6. Adverse events and interruptions | Duplicate suppression/conflict rejection, gap/disorder/corruption checks, resumed local import; real journal truncation and mocked transport timeout | Timeout leaves execution unknown and prevents automatic same-attempt retry. Actual native crash recovery is **not demonstrated** |
| 7. Replaceable contracts | Existing ArtifactStore, Normalizer and SliceExecution boundaries composed through Services; alternative in-memory storage tested | A second provider and a second financial engine are **not integrated** |
| 8. Preserved negatives | Failed source snapshots, receipts, logs and correction diffs; rejected permissions/partitions/ambiguous dispatch | Negative controls remain inadmissible; no criteria or native fills changed to obtain a pass |

All eight criteria are demonstrated at this bounded level; the limitations above remain explicit. Native preparations initially failed on the strategy-ID format and exact quantity precision. Both failures occurred before orders/fills. Two permitted focused corrections fixed those bindings; the original failures remain in [H3 evidence](evidence/h3/). H1's missing type annotation and H2's line-length failure also remain preserved. Final review restored the decision history accidentally replaced in H3, byte-for-byte from H2 before appending new entries (D-056); published commits were not rewritten.

## Reproduction and evidence

Use the already admitted runtime; these commands do not install anything. From the repository root, choose unused output directories:

```bash
NATIVE_PYTHON=/workspace/technical-admission/E/recovery/venv/bin/python
.venv/bin/python -m bot_trader.cli --state-dir /tmp/bot-trader-slice init
.venv/bin/python -m bot_trader.cli --state-dir /tmp/bot-trader-slice slice \
  --source tests/fixtures/integration/roundtrip.jsonl \
  --manifest tests/fixtures/integration/roundtrip.source.json \
  --native-python "$NATIVE_PYTHON" --run-dir /tmp/bot-trader-slice-native
```

The host uses CPython 3.12 with its unchanged lockfile; the optional process uses existing standard CPython 3.13.16 and NautilusTrader 2.0.0rc7, verified by the worker. The platform does not install or select that engine automatically. Native test execution is optional and requires the guarded evidence directory; ordinary CI can run host checks without Nautilus. Linux was exercised; this new isolated-worker route has not been verified on Windows.

Per-milestone `evidence/h*/summary.json` contains the exact commands and resource receipts; `manifest.json` hashes the preserved evidence. Successful and failed sources are identified by source manifests; failed snapshots/diffs are retained. [H3 native files](evidence/h3/h3-native-final/native/) and [H4 native files](evidence/h4/h4-delivery/native/) contain requests, results, journals and transport status. Final preservation verification confirms 4,630 recorded production-environment files unchanged, the restored decision-history prefix exact, and protected scientific/dependency/previous-package paths unchanged. The host regression deliberately excludes the already executed native test module; no completed M/R/E/E1 battery was repeated.

**Resources:** 25 guarded commands, 112.179 seconds elapsed and 103.542 CPU seconds; maximum sampled process-group RSS 267,812,864 bytes (255.4 MiB). Scratch/source snapshots occupy 10,529,299 logical bytes at the final check. Four-CPU affinity, bounded commands and offline IPv4/IPv6 denial were active. Sampling is not continuous peak certification. No downloads, purchases or service activation. File editing, publication and small integrity reads are outside these command timings; active engineering was not continuously instrumented, so the multi-session elapsed time must not be reported as active work or as an exact four-hour compliance certificate. Credit interruptions are excluded from active work. Receipt field `started_utc` was mistakenly populated at command completion; use it as a completion timestamp. Duration measurements use the monotonic clock; native event timestamps are independent and unaffected.

## Remaining limits and next integration

- Execution is explicitly synthetic depth plus a same-snapshot best bid/ask risk reference, with `bar_execution=False`, declared fee fraction 0.002, zero additional slippage/latency and a maximum quote age. These values are fixture assumptions, not approved empirical costs. OHLC is never silently converted to executable liquidity. No retrospective next-open guarantee.
- The current fixture normalizer admits a single versioned JSONL schema and complete source sequences starting at 1. Native dispatch supports SYNTH-USD at exact 0.01 price/quantity steps, spot long/cash market orders and explicit cancellation; multiple signals binding to one quote are rejected pending an arbitration policy. Real providers, negative-price instruments, other currencies and shared-capital execution require justified versioned extensions, not implicit coercion.
- Replay/checkpoint reconstruction is not native restart reconciliation. Positive latency/slippage, observed liquidity, prospective recovery and realistic capacity remain unadmitted. The old adverse engine evidence is retained; Nautilus remains a conditional, replaceable candidate.
- **A:** add a second source adapter through the existing contracts. **B:** prepare minimal read-only trades/best-bid-ask capture with receipt times, gaps and reconnect provenance. B has temporal priority, but activation needs separate source/rights/resources authorization. Neither is activated by this delivery.

The 26 scientific specifications, C1/C3 priorities, C2 comparison, C4/C5 reserves, USD basis, T/D/U/V/F and reserved-data access remain intact. Economic E3/E4 are pending. Phase IV is not unconditionally closed; Phase V, financial backtests/training and paper/live remain unauthorized.
