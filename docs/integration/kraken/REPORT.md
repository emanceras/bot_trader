# Evidence maintenance and existing Kraken historical QA

Authority: user request after `7206eb1`; two recoverable milestones. New campaign bounds: 2 hours active engineering, 900 monitored command seconds, 4 CPUs, 8 GiB RAM, 512 MiB additional temporary storage excluding existing archives. No new datasets/software, spending, engines or financial experiments. Historical integration evidence remains unchanged.

## A — maintenance completed

Published checkpoint: `31c1b59` / `kraken-historical-a`. Ten small tests passed; three evidence tests passed again after a reviewer identified deleted-root handling. An intentional uncommitted fixture failed, was removed from the worktree, then reconstructed from its immutable Git evidence tag and reproduced the same assertion failure. No complete source tree was copied. A lint failure and its correction remain recorded. A stale local remote-tracking ref caused an earlier preflight rejection before command execution; baselines are now explicit immutable published commits.

`check.py` uses a temporary Git index, preserving HEAD, the user's index and worktree. Each check records the parent commit, exact source tree/commit, SHA-256 source hashes, binary diff, command, configuration, history-prefix check, log and measured resources. Evidence tags under `evidence/kraken-*` must be published with the milestone. Deletions are included. Git reuses existing objects; no failed-source directory is created. The snapshot scope is explicit; private market files never belong in the repository or snapshot source paths.

`export_evidence.py` copies only an explicit public receipt/log/diff allowlist. New invocation sets receive new immutable indices. Private result directories are excluded; actual-data logs still require inspection because an exception could otherwise reveal market values. Previously published evidence is not rewritten. Failed/successful commit IDs also permit exact correction diffs with `git diff FAILED SUCCESS -- PATH`.

The reusable `append_only.py` verifies that the bytes of DECISIONS.md and EXPERIMENTS.md in a pinned published commit remain exact prefixes. It runs before guarded commands and publication. Exceptional replacements require a separately declared amendment bound to original/replacement hashes, immutable baseline, reason and authority reference; metadata does not authenticate that authority. No exception was used here.

Reproduce the already preserved negative without restoring a full tree:

```bash
git fetch origin refs/tags/evidence/kraken-a-negative
.venv/bin/python tools/integration/reconstruct_canary.py docs/integration/kraken/evidence/a/a-negative
```

Ordinary guarded checks require an explicit new budget; do not reuse old permissions:

```bash
python tools/integration/check.py --budget docs/integration/kraken/budget.json LABEL -- COMMAND
python tools/integration/append_only.py --baseline-commit FULL_LATEST_PUBLISHED_COMMIT
```

## B — existing historical data integrated and tested

Published checkpoint: `kraken-historical-b` (resolve tag to this milestone's commit). Both original ZIP bodies match the prior acquisition SHA-256 and size: 2,172,918,907 compressed bytes read with a 4 MiB buffer, without download or full extraction. Fixed prefix selection, chosen before results, reads only the first 64 data rows of XBTUSD trades and one-minute OHLCVT. This is a technical fixture scope, not a research-universe or historical-depth decision.

| Existing member | Schema | Private selected bytes / rows | Executed result |
|---|---|---|---|
| Trades `XBTUSD.csv` | Headered `timestamp,price,volume,type,order_type,misc,trade_id`, v2 | 3,683 / 64 | Exact normalization; 64 unique replayed events |
| Bars `XBTUSD_1.csv` | Headerless OHLCVT, v1 | 4,069 / 64 | Exact normalization; 64 unique replayed events; 0 before first close, 1 at first close |

Both pass repeated selection, interrupted local chunk import/restart, import idempotence, normalization equality, replay equality/checkpoint reconstruction and duplicate suppression. The first sampled trade falls within the first opening-labelled interval. Embedded READMEs explicitly identify bar timestamps as openings; actual bars align with their interval. Earlier full trade/bar structural findings remain preserved, not repeated. Full member CRC, quarter-wide ordering/completeness and representative coverage are not claimed from these prefixes.

The versioned adapter implements the existing Normalizer port and uses LocalArchive/ArtifactStore. Central v1/v2 contracts are unchanged. `MarketReplay.inspect_history` is an explicit data-only route sharing ordering/identity checks; it has no indicators, signal generation or execution port. The original synthetic route and reserved-partition gates remain effective. The adapter is usable through the technical QA tool, not enabled as a financial runner or dashboard feature.

Fractional Unix seconds are parsed from strings through exact decimal coefficients into integer ns, with sub-ns loss rejected, independent of ambient Decimal precision. v2 receives the exact derived ns tick; a private versioned sidecar preserves the original timestamp spelling/unit, native instrument label, trade ID, side/order metadata, trade count, row position/hash and archive/member/selection identity. This explicit normalization avoids pretending that an integer v2 tick can retain fractional-seconds spelling by itself. Original `XBTUSD`, XBT quantity and USD/XBT price units are retained; no alias or currency conversion.

Availability convention `kraken-history-optimistic-v1` is event time for trades and opening+interval for bars, plus a declared delay (zero in the actual QA). `received_ns` and engine init remain absent. This is an optimistic assumption, not observed reception or first publication. Final archive revisions are not proven point-in-time; financial admissibility remains unresolved. Trades/OHLC are never treated as observed bid/ask liquidity.

Equal values are not sufficient for deduplication. Repeated native IDs with identical records retain one logical effect; conflicting identities reject. Missing IDs retain row provenance. Provider ID jumps and empty-bar intervals are diagnostics, not proof of missing data; adapter sequence is a local selected-row ordinal. Missing-ID, precision, corruption, conflict, gap and restricted-access cases are checked with invented fixtures, not falsely attributed to the real prefixes.

**Executed verification:** 41 focused adapter/QA/replay tests; final backend regression **190 passed**; host mypy and Ruff pass. Native integration test modules were excluded; no motor or M/R/E/E1 battery ran. One existing Starlette/httpx deprecation warning remains. Lint negatives and bounded fixes are retained. The publication audit verifies all protected scientific/history/core paths and 4,630 recorded stable-environment files unchanged.

A review found that the original-data snapshot omitted an untracked rights-reference JSON. Its exact contents/hash are bound in subsequent evidence commit `51751338c25d846728660bc0f9a4a55405cfb057`; [binding receipt](evidence/b/b-preservation/output.log) explicitly records the post-execution timing. File metadata predates the run but cannot independently certify past content. The original receipt is untouched, subsequent snapshots include both documentation/config JSONs, and no real-data rerun was performed to conceal the omission.

[Original-data aggregate receipt](evidence/b/b-originals/output.log) publishes only hashes, counts and technical outcomes. Original ZIPs, 7,752 selected CSV bytes, normalized market events and provenance sidecars remain private outside Git. Scoped rights reuse the offered archive/code-conversion assessment for private technical QA; no redistribution or production/live licence is inferred. [Sources](sources.json) distinguish current documentation, reused rights and embedded notices.

Reproduction requires the already acquired local ZIPs and an unused private output directory; the command does not download missing inputs:

```bash
python tools/integration/check.py --budget docs/integration/kraken/budget.json LABEL -- \
  .venv/bin/python tools/integration/kraken_qa.py
```

A missing original yields an explicit unavailable result; faithful invented schema fixtures remain independently testable. Do not repeat completed checks merely to consume the remaining budget.

## Future capture — specification only

[Disabled executable configuration/specification](capture-spec.json) proposes public WebSocket v2 trade and ticker/bbo for BTC/EUR, without keys or orders. REST confirms the spot listing online; exact v2 instrument eligibility and Spanish deployment access remain preflight requirements. Official ticker documentation defaults to trade-triggered updates; `bbo` refers to changes in best bid/offer **price levels**, not guaranteed every quantity-only change. No ticker sequence/checksum or complete reconnect backfill is assumed.

The specification defines application UTC/monotonic receipt clocks, raw hashes, duplicate/conflict handling, explicit gaps/reconnect sessions, finite disk/retention limits, safe stop/recovery and 24/7 host requirements. Resource and traffic sensitivities are proposals, not measured feed rates or purchased services. Public-feed retention rights are not established by API accessibility; rights, source and resource approval remain activation gates. No WebSocket connection or capture was started.

## Limits and continuity

[Budget](budget.json), [A evidence](evidence/a/) and [B evidence](evidence/b/) record a fresh campaign: **20 guarded commands, 132.427 elapsed seconds, 115.140 CPU seconds**, maximum sampled RSS 195,940,352 bytes (186.9 MiB), sampled temporary footprint 7,186,295 bytes including scratch, documentation cache and additional Git objects. Private scratch is 4,682,037 logical bytes; existing 2.17 GB archives are excluded. No resource stop, dataset/software download or expense. Active engineering estimate at release audit: approximately 60 minutes (35 estimated before interruption plus 25.4 measured after resumption); this is not an exact time certificate. [Release audit](release-audit.json) records 7,189,692 additional temporary/reference bytes and 1,562,985 public delivery bytes before commit, far below the512MiB envelope. Monotonic command timings exclude editing/publication and Git snapshot preparation; memory/disk are sampled, not hard peak certificates. Official documentation/one instrument-metadata response are small reference reads, not new financial datasets. Active engineering before the interruption is estimated, not continuously timed; the resumed session is recorded separately. Do not count interruption gaps as engineering.

E3/E4 economics remain pending. The 26 specifications, C1/C3, C2, C4/C5, USD basis, T/D/U/V/F and holdout restrictions are unchanged. Phase V, investment training, paper/live and persistent capture remain unauthorized.
