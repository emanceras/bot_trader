# Evidence maintenance and existing Kraken historical QA

Authority: user request after `7206eb1`; two recoverable milestones. New campaign bounds: 2 hours active engineering, 900 monitored command seconds, 4 CPUs, 8 GiB RAM, 512 MiB additional temporary storage excluding existing archives. No new datasets/software, spending, engines or financial experiments. Historical integration evidence remains unchanged.

## A — maintenance completed

Published checkpoint: `kraken-historical-a` (resolve tag to commit). Ten small tests passed; three evidence tests passed again after a reviewer identified deleted-root handling. An intentional uncommitted fixture failed, was removed from the worktree, then reconstructed from its immutable Git evidence tag and reproduced the same assertion failure. No complete source tree was copied. A lint failure and its correction remain recorded. A stale local remote-tracking ref caused an earlier preflight rejection before command execution; baselines are now explicit immutable published commits.

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

## B — implementation prepared, execution pending

Original two Kraken Q3 ZIPs are available outside Git. Adapter and synthetic tests are prepared but not yet executed. Next work: bounded private selection, exact normalization, data-only replay and a closed-bar availability canary. No native engine or signal-generation path is permitted for these records. Core v2 contracts remain unchanged. Future capture is specification only and remains disabled.

## Limits and continuity

[Budget](budget.json) and [A evidence](evidence/a/) record a fresh campaign. Monotonic command timings exclude editing/publication and Git snapshot preparation; memory/disk are sampled, not hard peak certificates. Official documentation/one instrument-metadata response are small reference reads, not new financial datasets. Active engineering before the interruption is estimated, not continuously timed; the resumed session is recorded separately. Do not count interruption gaps as engineering.

E3/E4 economics remain pending. The 26 specifications, C1/C3, C2, C4/C5, USD basis, T/D/U/V/F and holdout restrictions are unchanged. Phase V, investment training, paper/live and persistent capture remain unauthorized.
