# Development and extension contracts

Canonical language: English. Revision: 4. Updated: 2026-10-20. Spanish counterpart: [development.md](../es/development.md).

Read [AGENTS.md](../../AGENTS.md), the [Phase III request](../phase-iii/REQUEST.es.md) and the [architecture](architecture/platform.md) before changing scope. English is canonical for code, comments, symbols and new technical documentation. Preserve the original Spanish scientific record and update the paired technical translation in the same change.

## Dependency direction

`core` defines frozen versioned contracts, policy, registry, events and ports. `persistence` implements versioned metadata, jobs and audit. `market_data` provides the synthetic catalog and artifacts. `lab` consumes those contracts and records finite technical tasks; `simulation` supplies only a bounded synthetic ledger. `application.py` composes trusted dependencies. `api` and the CLI adapt those services to HTTP and processes; the React client consumes the HTTP contract.

Domain services do not depend on FastAPI or frontend components. The initial database is SQLite on local disk; the interface does not constitute a tested PostgreSQL implementation. Artifact adapters accept registered content identities, not caller-controlled filesystem paths. DuckDB operates over verified Arrow input with external access and extension loading disabled.

## Three extension mechanisms

| Mechanism | Procedure | Required evidence |
|---|---|---|
| A — add a module | Define its manifest, dependencies, status and interfaces; compose it explicitly in the trusted application | Existing services continue to work; duplicates, missing dependencies and cycles are rejected |
| B — add an internal capability | Register a named capability in an operational module, preserving existing contracts | Optional capability works when present; absent/inactive capability fails explicitly without changing unrelated behavior |
| C — replace an implementation | Supply another adapter satisfying the same port and inject it at composition | Equivalent contract tests pass, including failure and authorization behavior; consumers do not import implementation details |

`Registry.register`, `Registry.add_capability` and `Registry.call` are explicit extension points. `EventBus` is synchronous and in-process, not a durable distributed delivery system. There is no untrusted plugin discovery or dynamic import endpoint. Installed Python modules run with process privileges; registration does not create an operating-system sandbox.

The current storage substitution can be exercised with the local and memory artifact implementations. A future financial engine belongs behind the execution/accounting interface, with its own instrument and compatibility admission. Do not expand the synthetic ledger into an undocumented production engine.

## Data, jobs and immutable provenance

Use contract validators for UTC event/availability clocks and finite decimal quantities. Unknown availability stays unknown; never manufacture it from the observation time. Charts convert values to floats only for display. Accounting uses decimals and explicit currency identity. USD, USDT and USDC are distinct.

Documents and audit history are append-only. A changed document body creates a version; identical content is idempotent. Job configuration and manifests are immutable. Claim work atomically, execute outside the metadata transaction and finish only while the worker still owns the running attempt. Retain failures, cancelled attempts and interrupted work. Do not silently retry an uncertain task or overwrite a recorded result.

Follow the stored input lineage when enforcing permissions. Blocking a dataset route is insufficient: transformations, charts, report downloads, run lists and workers must enforce the same final-partition restriction. Authority comes from persisted metadata, not a caller's `synthetic` or partition flag.

Source provenance records the current Python tree, `pyproject.toml`, `uv.lock`, Git identity and environment versions. Loaded-code identity is checked against disk at submission/execution, and execution checks identity again before publishing a result. Restart the API and every worker after executable/dependency updates. This is reproducibility evidence, not a signed supply-chain attestation. Keep modifications and dependency changes outside pending attempts; submit a new attempt when identity changes.

## Complementary architecture boundary

The [supplementary coverage review](architecture/supplement.md) and [targeted evidence](architecture/supplement-evidence.md) distinguish essential invariants from deferred features. Preserve the existing modular monolith, source history and C1–C5 priorities. A reference platform is a comparison source, not an architectural authority. Restoring the already approved lockfiles is part of setup; adding dependencies needs the applicable authorization and a concrete requirement.

Immutable record references identify a kind, persistent ID, version and content hash. Their purpose is to resolve the exact evidence used by a run, not to imply scientific validation. Strategy/model versions, future bot identity, deployment session, account and portfolio attribution must remain conceptually distinct. They do not require empty tables or new services before a consumer needs them.

The current `Signal`/order/portfolio contracts serve the bounded technical harness. A quantity target is not a general prediction or a complete multibot portfolio policy. Before admitting an actual strategy adapter, specify how its signals, portfolio targets, risk decisions and order intentions compose, including cohesive entry/exit behavior where a rigid pipeline would distort the strategy. Account-level net positions cannot be assumed to equal virtual bot ownership. These are future adapter admission requirements, not implemented capital allocation or live authorization.

Research assessment, implementation readiness, test permission, runtime state and eligibility for capital are separate dimensions. No lifecycle label, retired-strategy reconsideration, stored AI proposal or human review record may itself grant execution permissions. Deferred review/archive/reconciliation services should reuse versioned records and explicit policy boundaries when their admitted workflows require them; they are not dependencies of today's synthetic tasks.

## Local checks

Install frozen dependencies using the [installation guide](installation.md), then run from the repository root:

```bash
uv run --frozen pytest
uv run --frozen ruff check src tests
uv run --frozen mypy src
npm --prefix web run typecheck
npm --prefix web test
npm --prefix web run build
```

Strict Python typing is configured in `pyproject.toml`. Use synthetic fixtures and temporary state for tests. Meaningful checks include real service boundaries, append-only persistence after restart, concurrent claims, stale-worker fencing, code/environment drift, record tampering, causal time constraints, conservation of synthetic cash/inventory, authorization and artifact traversal. Never download market histories to make a software test realistic.

Browser integration must use a real API, initialized temporary state and the actual worker where jobs are involved. Cover sign-in, denial, empty/error states, synthetic data/chart rendering, task transitions and report reads. Component mocks alone do not satisfy end-to-end acceptance. Record the actual command, environment and result; do not infer a passed browser check from a successful production build.

For the browser acceptance workflow, reserve loopback port 8000 for a dedicated test API and use a separate private state directory. Do not point these checks at personal research state. After building the web, initialize that directory and start the API from the repository root in one terminal:

```bash
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser init
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser credential viewer
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser serve
```

In a second terminal, start its worker:

```bash
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser worker --watch --worker-id browser-worker
```

In a third terminal, run the browser suite using that same state path:

```bash
BOT_TRADER_E2E_STATE=/workspace/.bot-trader-browser npm --prefix web run test:e2e
```

The browser configuration uses the installed Chromium executable; the managed Linux environment provides `/usr/bin/chromium`. The runner reads the private local test credential from the state directory without putting its value in a command. Keep reports, screenshots and state private; do not record the sign-in credential. The API and worker must use the same frozen source/environment throughout the run. Stop both test processes afterwards. A documented invocation is not a passed check: consult the verification report for the actual executed outcome and any outstanding prerequisite.

Alternatively, after the build, the repository helper initializes isolated state (admin and viewer), starts its own API and worker, runs Chromium and stops only those child processes:

```bash
python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-check
```

The [acceptance checklist](../phase-iii/acceptance.md) maps the requested architecture and implementation criteria, including D execution separation, E repeatability and F real web integration. The [verification report](verification.md) records the executed evidence that determines closure; a passing unit-test count alone does not.

## Changes, migrations and licenses

Add explicit Alembic revisions for schema changes; do not call `create_all` at application startup or edit an already deployed revision silently. Preserve append-only invariants and compatibility checks. Test upgrades against a copy of previous state and document recovery before release. The CLI exposes explicit upgrade, not destructive downgrade.

Review dependency upgrades against the locks, compatibility and license records in [stack](architecture/stack.md), [engines](architecture/engines.md) and [research tools](architecture/research-tools.md). The resolved Python metadata inventory is [python-dependencies.json](../licenses/python-dependencies.json); upstream licenses do not assign a license to this project's own code. Keep Lightweight Charts' license, NOTICE and visible attribution/link with the application; a chart data-source contract is separate from a renderer license. No paid data or external service is acquired by adding a dependency.

Finish with a coherent reviewed commit and update progress, decisions and translations. Report actual implemented/tested scope, failed checks and remaining limits. Technical software validation must never be written into `EXPERIMENTS.md` as a successful financial experiment.
