# Integration checkpoint

- Recovery milestone: `kraken-public-client` (D-060), based on published `a5e9997`; previous `kraken-ws-simulated` remains reproducible. [Current report EN](docs/en/integration/kraken-ws-client.md) / [ES](docs/es/integration/kraken-ws-client.md).
- Implemented: optional pinned WebSocket client → existing service/journal/archive/normalizer/Market Replay. Single-writer journal appends/checkpoints now incremental; full audits at restart/read/recovery/external changes. Core contracts and persisted v1 journal unchanged.
- Verified offline only:125 final focused tests; earlier311 backend regressions (overlap). Mypy45files/scoped Ruff pass; two type failures preserved.36prior dependency entries/4,630stable files/science/old evidence unchanged. Optional websockets17.4 installed only in disposable test target; no Kraken connections.
- Eight guarded commands:25.72s wall/19.55s CPU; sampled222.2MiB RSS/6.32MiB temporary. Evidence and budget under `docs/integration/kraken-ws-client/`; no native engine campaigns repeated.
- `capture-pilot` defaults to a local plan. Matching user approval is mandatory for connection; template false/expired. Recovery/inspection offline; terminal retry preserves outcome. Existing data-only permissions do not authorize financial use.
- Ready to request a supervised5–10min pilot, not execute it: first bind rights, host/reliable clock/private disk, pinned optional runtime, external watchdog and explicit approval. Real TLS/provider access/traffic remain untested. No24/7 or native-Windows claim; logical limits are not a filesystem quota.
- E3/E4 economics,26specifications,C1/C3,C2,C4/C5,T/D/U/V/F,holdout and Phase V/paper/live remain unchanged/pending.
