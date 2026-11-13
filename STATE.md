# Integration checkpoint

- Recovery milestone: `kraken-ws-simulated` (D-059), based on published `dc859e8`; earlier A=`31c1b59`. [Current report EN](docs/en/integration/kraken-ws.md) / [ES](docs/es/integration/kraken-ws.md).
- Implemented/tested: simulated BTC/EUR WSv2 trade+ticker/BBO → durable raw journal → existing archive/normalizer v2 → data-only Market Replay; composition available as `services.capture`. No real socket/client, credentials, financial strategy or new dependencies.
- Executed: 70 focused tests, 260 backend regressions; strict mypy across 42 files and scoped Ruff pass. Initial type failure and two unrelated historical-tools lint findings preserved. 4,630 stable-environment files/core/science/old evidence unchanged. Eight guarded commands, 18.57 s machine time; fresh limits recorded in `docs/integration/kraken-ws/budget.json`.
- Durable receipts, config artifacts, exclusivity, duplicate/gap handling, interrupted-write recovery and causal checkpoint growth verified with invented transport. Upstream completeness remains unknown. POSIX/bounded prefix implementation; no 24/7 or native-Windows claim.
- Next only with separate scope: admit a real WS connector and approve source/rights/host/resources for the documented supervised 5–10 min pilot. Nothing is activated automatically. No need to repeat M/R/E/E1 or acquire historical data.
- E3/E4 economics, 26 specifications, C1/C3, C2, C4/C5, T/D/U/V/F, holdout and Phase V/paper/live remain unchanged/pending.
