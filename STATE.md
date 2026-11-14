# Integration checkpoint

- Recovery milestone: `kraken-public-client` (D-060), based on published `a5e9997`; previous `kraken-ws-simulated` remains reproducible. [Current report EN](docs/en/integration/kraken-ws-client.md) / [ES](docs/es/integration/kraken-ws-client.md).
- Implemented: optional pinned WebSocket client → existing service/journal/archive/normalizer/Market Replay. Single-writer journal appends/checkpoints now incremental; full audits at restart/read/recovery/external changes. Core contracts and persisted v1 journal unchanged.
- Verified offline only: 127 final focused tests; earlier 311 backend regressions (overlap). Mypy over 45 files/scoped Ruff pass; two type failures preserved. 36 prior dependency entries / 4,630 stable files/science/old evidence unchanged. Optional websockets 17.4 installed only in disposable test target; no Kraken connections.
- Nine guarded commands: 30.98 s wall / 23.19 s CPU; sampled 222.2 MiB RSS / 7.09 MiB temporary. Evidence and budget under `docs/integration/kraken-ws-client/`; no native engine campaigns repeated.
- `capture-pilot` defaults to a local plan. Matching user approval is mandatory for connection; template false/expired. Recovery/inspection offline; terminal retry preserves outcome. Existing data-only permissions do not authorize financial use.
- Ready to request a supervised 5–10 min pilot, not execute it: first bind rights, host/reliable clock/private disk, pinned optional runtime, external watchdog and explicit approval. Real TLS/provider access/traffic remain untested. No 24/7 or native-Windows claim; logical limits are not a filesystem quota.
- E3/E4 economics, 26 specifications, C1/C3, C2, C4/C5, T/D/U/V/F, holdout and Phase V/paper/live remain unchanged/pending.
