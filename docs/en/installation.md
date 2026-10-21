# Installation and configuration

Canonical language: English. Revision: 3. Updated: 2026-10-20. Spanish counterpart: [installation.md](../es/installation.md).

This guide installs the local Phase III technical platform from a source checkout. It creates no exchange connection, purchases no service and downloads no historical market dataset. Verification status is recorded in [Phase III progress](../phase-iii/PROGRESS.md); the commands here are the supported procedure, not an independent acceptance claim.

## Requirements and dependencies

Use Python 3.12, `uv`, Node.js 24 and npm. The implementation was developed in a Linux environment. Windows permissions, alternative operating systems and multi-host deployments have not been certified. Python 3.13 is outside the current package requirement. A source checkout is necessary because migrations, original hypotheses, provenance files and the compiled web application are loaded relative to its root.

From the repository root:

```bash
uv sync --frozen
npm --prefix web ci
npm --prefix web run build
```

`uv.lock` and `web/package-lock.json` fix the resolved dependencies. Installing them requires access to the package registries unless they are cached. Do not replace the frozen install with an unreviewed dependency upgrade. The default SQLite deployment needs no database server, Redis or Docker. PostgreSQL is an architecture option; there is no implemented PostgreSQL adapter to configure here.

In a managed cloud workspace where default user caches are not writable, configure writable workspace caches before installing or running checks:

```bash
export UV_CACHE_DIR=/workspace/.cache/uv
export NPM_CONFIG_CACHE=/workspace/.cache/npm
uv sync --frozen
npm --prefix web ci
```

A cache permission failure is not evidence that the package archive is invalid. Preserve TLS/checksum verification and diagnose the cache location before retrying. These cache locations contain development dependencies, not application credentials. Keep the variables set in terminals used for the commands below, or configure them in the managed environment.

## Initialize and start

```bash
uv run --frozen bot-trader init
uv run --frozen bot-trader fixture --seed 42 --rows 120
uv run --frozen bot-trader serve
```

`init` explicitly migrates the metadata database, creates a private local administrator credential once and imports H-00–H-24 from `HYPOTHESES.md`. Repeating initialization does not replace the credential or erase existing records. The fixture command creates seeded synthetic bars and prints the registered dataset identifier. It does not run a financial experiment.

The API serves the compiled web application on `127.0.0.1`, port `8000`. Open that address in your local browser. A missing frontend build produces an explicit 503 response at the root page; run the build before starting the server. A missing or incompatible database schema also requires explicit initialization/migration; server startup does not repair it silently.

The credential path is printed by initialization, normally `.state/admin.token`. Read it privately on your machine and enter the value into the sign-in screen. Never copy it into a shared terminal transcript, issue, chat or repository. The file is local application authentication; no API key from an exchange is needed.

Start a separate worker from the same checkout and state directory:

```bash
uv run --frozen bot-trader worker --watch --worker-id local-worker
```

Without `--watch`, the worker processes at most one queued technical task and exits. The server does not launch a worker automatically. Keep its printed identity for interruption recovery. A queued task may remain queued while the worker is stopped; the dashboard does not provide a heartbeat monitor.

## State paths and configuration

Default state lives under `.state/`, ignored by Git. It contains `metadata.sqlite3`, immutable artifacts and private role credentials. The database and its artifacts form one logical record; retaining only one part is insufficient for restoration.

The global `--state-dir` argument must appear **before** the subcommand. Use the same value for all processes:

```bash
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state init
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state serve
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state worker --watch --worker-id local-worker
```

Keep a custom state directory outside tracked files and accessible only to the local operator. `.gitignore` protects the default state directory; it cannot protect every arbitrary path a user chooses.

Settings accept the `BOT_TRADER_` environment prefix. `.env` files are **not automatically loaded** by `Settings`; configure the process environment deliberately. Important settings are:

| Setting | Default | Meaning |
|---|---|---|
| `BOT_TRADER_REPOSITORY_ROOT` | Current directory | Source, migrations, hypotheses and `web/dist` root |
| `BOT_TRADER_DATA_DIR` | `.state` | State directory, relative to the repository root unless absolute |
| `BOT_TRADER_MODE` | `technical` | Only accepted runtime mode; it cannot enable trading |
| `BOT_TRADER_ENVIRONMENT` | `development` | Deployment configuration, not financial permission |
| `BOT_TRADER_ALLOWED_HOSTS` | `["localhost","127.0.0.1"]` | Explicit accepted HTTP hosts; no wildcard |
| `BOT_TRADER_ALLOWED_ORIGINS` | Loopback HTTP origins on port 8000 | Explicit origins required for mutations, including login |
| `BOT_TRADER_SECURE_COOKIES` | `false` | Local HTTP default; production configuration requires true and HTTPS origins |
| `BOT_TRADER_SESSION_TTL_SECONDS` | `3600` | Session lifetime, bounded to 60–86,400 seconds |
| `BOT_TRADER_MAX_DATASET_ROWS` | `10000` | Synthetic fixture row bound |
| `BOT_TRADER_MAX_QUEUED_RUNS` | `100` | Queue bound |

Array-valued environment settings use JSON. Every origin must name an allowed host. `BOT_TRADER_ADMIN_TOKEN` can override the administrator credential in a controlled process environment, but the private file generated by `init` avoids placing a secret in command history. Do not put tokens directly into shell commands.

## Upgrade and troubleshooting

Stop the API and every worker; take a coherent private backup before changing code or schema. Install the reviewed lockfiles, rebuild the frontend, then run:

```bash
uv run --frozen bot-trader migrate
```

Migrations are explicit upgrades. There is no supported destructive downgrade workflow. Restart **both the API and every worker** after executable code or dependency updates and only after the schema check passes. Long-lived Python processes retain imported code: the platform compares the loaded-code identity with the source on disk and rejects drift instead of attributing old code to new files. It also rechecks identity after computation. Existing queued attempts freeze code and environment identity; if those changed, the worker records a failure rather than silently running new code under an old manifest. Submit a new attempt when appropriate and retain the old failure.

If login fails, confirm the correct state directory, private credential permissions and chosen host/origin. Restarting the server logs out existing sessions. If a task remains queued, inspect the separate worker. If it is `running` after a confirmed worker crash, use the recovery procedure in [security and operations](security.md). Do not edit SQLite rows to force a success state.
