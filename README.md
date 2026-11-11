# bot_trader

Latest implementation: [synthetic integration report](docs/integration/REPORT.md) and [resumable checkpoint](STATE.md). The platform now connects immutable local inputs, exact-time events, causal replay, fixed synthetic signals, isolated native buy/sell execution and independent accounting. Full/partial/cancel/rejection paths pass the bounded integration checks. This is technical evidence only; Nautilus remains conditional and Phase V is not authorized.

Earlier technical evidence: [E1 causal bar execution](docs/en/phase-iv/bar-execution.md) ([español](docs/es/phase-iv/bar-execution.md)). Exact rc7 reproduces same-close execution; 1 ms latency reaches the next close, not its open. The tested causal boundary passes 135 component checks across 15 native contexts, with explicit synthetic pricing assumptions. At that checkpoint, production integration and financial admission remained pending.

Previous bounded correction: [E3-L2 / E4 findings](docs/en/phase-iv/engine-correction.md) ([español](docs/es/phase-iv/engine-correction.md)). Causal L2 execution works in the tested fixture; supervisor duplicate protection preserves state, while original E4 still lacks its required second native fill. At that checkpoint, E1/bar execution and financial admission remained pending.

Earlier technical evidence: [bounded E recovery](docs/en/phase-iv/engine-recovery.md) ([español](docs/es/phase-iv/engine-recovery.md)), 2026-11-02. Nautilus now executes in isolation; accounting components pass, while liquidity, duplicate-order state and integration/recovery gaps prevent full engine admission. Production and financial permissions are unchanged.

A modular cryptocurrency research platform with a documented scientific history. The current implementation provides a **local, synthetic technical laboratory**: versioned data, preserved hypotheses, durable jobs, reports, an authenticated API and a web interface. It does not establish a profitable strategy.

Phase I closed with documented limitations; Phases II and III were accepted. Phase IV E1/E2 design decisions are conditionally approved; E3/E4, empirical bindings and final preregistration remain pending. The authorized **A/B technical audit** acquired only two Kraken Q3 archives for external structural QA and tested NautilusTrader 1.231.0 in a disposable synthetic environment. See the [results and limitations](docs/en/phase-iv/admission.md), [Spanish report](docs/es/phase-iv/admission.md) and [acceptance gate](docs/en/phase-iv/acceptance.md). The quarter and venue do not limit future research coverage. Production remains the verified Phase III synthetic platform: no financial backtests, investment-model training, prospective paper/live activity, spending or additional data acquisition is authorized. See [current IV progress](docs/phase-iv/PROGRESS.md) and [III verification](docs/en/verification.md).

The [staged-admission amendment](docs/en/phase-iv/staged-amendment.md) ([español](docs/es/phase-iv/staged-amendment.md)) records the user-approved T/D/U/V/F methodology while financial permissions remain absent. The [M/E/R decision package](docs/en/phase-iv/technical-packages.md) ([español](docs/es/phase-iv/technical-packages.md)) specifies isolated dependency, engine and causal-equivalence checks expressly authorized in D-046. Their [executed results and limitations](docs/en/phase-iv/technical-results.md) ([español](docs/es/phase-iv/technical-results.md)) distinguish successful synthetic checks from blocked or unexecuted engine cases. Production and financial permissions remain unchanged.

## Start locally

Requirements: a source checkout, Python 3.12, `uv`, Node.js 24 and npm. Run from the repository root:

```bash
uv sync --frozen
npm --prefix web ci
npm --prefix web run build
uv run --frozen bot-trader init
uv run --frozen bot-trader fixture --seed 42 --rows 120
uv run --frozen bot-trader serve
```

The server listens on loopback port 8000. Open that local address in your own browser. `init` prints the **path** to `.state/admin.token`; read that private file locally and use its contents to sign in. Do not paste it into chat, logs, Git or screenshots. This is an application credential, not an exchange key.

In managed cloud environments, use the writable `UV_CACHE_DIR` and `NPM_CONFIG_CACHE` settings documented in [installation](docs/en/installation.md). Preserve dependency checksums when diagnosing installation failures.

Run the finite technical worker in a second terminal:

```bash
uv run --frozen bot-trader worker --watch --worker-id local-worker
```

The web interface submits bounded technical tasks; the worker executes them separately. An empty queue produces no financial activity. See the installation guide before changing paths, upgrading or exposing a service beyond this local configuration.

## Documentation

| Topic | English, canonical technical documentation | Español |
|---|---|---|
| Installation and configuration | [Installation](docs/en/installation.md) | [Instalación](docs/es/installation.md) |
| Everyday use and technical tasks | [Usage](docs/en/usage.md) | [Uso](docs/es/usage.md) |
| Contracts, extensions and checks | [Development](docs/en/development.md) | [Desarrollo](docs/es/development.md) |
| Permissions, recovery and backups | [Security and operations](docs/en/security.md) | [Seguridad y operación](docs/es/security.md) |
| Architecture and module boundaries | [Platform](docs/en/architecture/platform.md) | [Plataforma](docs/es/architecture/platform.md) |
| Executed verification and limits | [Verification](docs/en/verification.md) | [Verificación](docs/es/verification.md) |
| Complementary architecture review | [Coverage and minimal changes](docs/en/architecture/supplement.md), [targeted evidence](docs/en/architecture/supplement-evidence.md) | [Cobertura y cambios mínimos](docs/es/architecture/supplement.md), [evidencia dirigida](docs/es/architecture/supplement-evidence.md) |
| Phase IV design | [Protocol and dependencies](docs/en/phase-iv/protocol.md), [acceptance](docs/en/phase-iv/acceptance.md) | [Protocolo y dependencias](docs/es/phase-iv/protocol.md), [aceptación](docs/es/phase-iv/acceptance.md) |
| Phase IV pending choices | [Executive decision review](docs/en/phase-iv/executive-decisions.md) | [Revisión ejecutiva de decisiones](docs/es/phase-iv/executive-decisions.md) |
| Phase IV feasibility | [Data, engine, costs and admission](docs/en/phase-iv/feasibility.md) | [Datos, motor, costes y admisión](docs/es/phase-iv/feasibility.md) |
| Phase IV technical evolution | [Sources, temporal contracts, engines and staged admission](docs/en/phase-iv/evolution.md) | [Fuentes, contratos temporales, motores y admisión por etapas](docs/es/phase-iv/evolution.md) |
| Staged admission amendment | [Approved methodology and access gates](docs/en/phase-iv/staged-amendment.md) | [Metodología aprobada y accesos](docs/es/phase-iv/staged-amendment.md) |
| Authorized technical package specifications | [M, E and R scope](docs/en/phase-iv/technical-packages.md) | [Alcance M, E y R](docs/es/phase-iv/technical-packages.md) |
| Actual M/R/E execution | [Results and limitations](docs/en/phase-iv/technical-results.md) | [Resultados y limitaciones](docs/es/phase-iv/technical-results.md) |
| Planned UX, glossary and help | [Future plan](docs/en/ux-evolution.md) | [Plan futuro](docs/es/ux-evolution.md) |
| Technology alternatives | [Stack](docs/en/architecture/stack.md), [engines](docs/en/architecture/engines.md), [research tools](docs/en/architecture/research-tools.md) | [Stack](docs/es/architecture/stack.md), [motores](docs/es/architecture/engines.md), [herramientas](docs/es/architecture/research-tools.md) |

The original scientific record remains in Spanish: [ROADMAP.md](ROADMAP.md), [RESEARCH.md](RESEARCH.md), [HYPOTHESES.md](HYPOTHESES.md), [EXPERIMENTS.md](EXPERIMENTS.md) and [DECISIONS.md](DECISIONS.md). It includes H-00–H-24, adverse evidence and conditional candidate selection. [AGENTS.md](AGENTS.md) governs continued work; [translation policy](docs/TRANSLATIONS.md) prevents an untranslated history from being mistaken for new evidence.

## Scope of the implementation

| Scope | What exists |
|---|---|
| Technical services | Typed contracts, explicit module registry, SQLite migrations and append-only records, content-addressed artifacts, synthetic Parquet fixtures, bounded quality queries and causal transformation checks |
| Research records and jobs | Import of the 25 original hypotheses, immutable run configuration and provenance, separate worker, persisted failures, explicit interruption recovery, JSON/Markdown reports and technical repeatability comparisons |
| API and web | Local authentication and roles, dataset catalog, synthetic charts, hypotheses, technical attempts, module states and audit records; final verification is recorded in the acceptance documents |
| Prepared interfaces | Strategy/model/risk/portfolio contracts, temporal partition and walk-forward preparation, inert research proposals and a replaceable synthetic spot ledger |
| Future work requiring its own admission | Financial engines and experiments, market feeds, financial ML training, derivatives accounting, prospective paper trading, live execution, autonomous agents, external alerts and multi-host deployment |

The architectural supplement preserves the current modular monolith and C1–C5 priorities. Multibot allocation, strategy promotion, statistical monitoring, autonomous retrieval and execution decisions remain future capabilities with separate admission gates; a dashboard entry or research record does not enable them.

USD is the research account currency. USDT and USDC are distinct instruments with additional risks, not implicit USD substitutes. The fixture instrument `SYNTH-USD` is invented test data. Its charts and ledger values are not market observations or strategy returns.

## Development checks

```bash
uv run --frozen pytest
uv run --frozen ruff check src tests
uv run --frozen mypy src
npm --prefix web run typecheck
npm --prefix web test
npm --prefix web run build
```

These are software checks. They do not increment the project's financial experiment counter or validate H-00–H-24. The [development guide](docs/en/development.md) describes the separate real-backend browser workflow. Installation and browser evidence belong to the Phase III verification record.
