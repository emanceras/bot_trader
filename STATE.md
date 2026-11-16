# Integration checkpoint

- Published base: `2316029` (`kraken-public-client`). D-061 authorizes a finite real public BTC/EUR trade+ticker QA pilot; financial execution remains prohibited.
- In-progress campaign: `/workspace/kraken-replay-pilot`, budget and source refs under `docs/integration/kraken-pilot/`. Do not restart completed checks. 317 backend + 7 web unit + 2 browser checks passed; web types/build pass. 72 focused proxy/CLI/verifier checks pass; strict mypy passes.
- Original direct attempt `pilot-live-01`: three failed connections, zero market frames, acceptance false. Evidence preserved. Direct TCP refused; configured environment proxy completed verified TLS/WebSocket diagnostic without subscriptions.
- Minimal fixes: explicit hash-bound optional proxy, unchanged direct defaults/digests; failed pilot returns nonzero. No new dependencies/core contracts.
- Active pilot `pilot-live-02`, capture ID `kraken-btc-eur-pilot-proxy-20261116`, started 2026-11-16 09:25 UTC. Existing supervised guard, 300-second target / 320-second outer bound. Actual messages are arriving; do not claim success until receipt and offline QA complete. Private approval/config rebound to resumed host under existing user authority; no renewed permission requested.
- Next: inspect actual completion, offline original/restart/hash/causality checks; only necessary fixes/retests; EN/ES report and publication. Preserve all raw data privately, including failures. Guard race fix under review. No permanent collector.
- Stop after delivery; E3/E4 economics next, 26 specifications/scientific gates/holdout and Phase V/paper/live unchanged.
