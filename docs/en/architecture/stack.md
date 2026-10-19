# Platform stack and bounded alternatives review

Canonical language: English. Revision: 2. Original assessment: 2026-10-18. Evidence recovery: 2026-10-19. Spanish counterpart: [stack.md](../../es/architecture/stack.md). Evidence ledger: [stack-sources.jsonl](../../architecture/stack-sources.jsonl).

This is an architecture decision for Phase III, not evidence of implementation, performance or financial advantage. The authorised implementation uses synthetic fixtures. Phase IV–VI and market-connected paper/live execution remain separate gates. Exact installed versions and executable checks belong to the implementation lockfiles and verification report.

## Decision and alternatives

| Boundary | Selected foundation | Alternative and tradeoff | Reconsideration trigger |
|---|---|---|---|
| HTTP API and contracts | Python, FastAPI, Pydantic 2, explicit versioned schemas | A larger web framework brings integrated administration/authentication but increases coupling to its application model. Pydantic runtime validation complements static typing; neither proves data truth or causal availability. | Requirements for organisation-wide identity, administration or externally supported API compatibility |
| Metadata transactions | SQLAlchemy 2 repositories, Alembic migrations, SQLite on local persistent disk for the initial deployment | PostgreSQL is the intended server database option. It adds a service, credentials, backup and operational duties but is more appropriate for multiple hosts and concurrent writers. Database portability is a design objective, not proof of a working PostgreSQL adapter. | Measured write contention, multiple hosts/users, network database access or stronger deployment requirements |
| Tabular artifacts and analysis | Immutable versioned Parquet, PyArrow for materialisation, DuckDB for bounded analytical reads | Storing all series as transactional rows mixes analytical scans with jobs/state. DuckDB as the sole metadata store is not chosen for this workload. A distributed lake/catalog adds infrastructure absent from III requirements. | Data size, update semantics or concurrent analytics justify another adapter with equivalent contracts |
| Web client | React, TypeScript, Vite; static production build served with the API on one origin | Next.js supports self-hosting, static export and server rendering; it is not tied to a paid hosting vendor. Server rendering/caching would add a second application execution model without a current dashboard requirement. | Public indexable pages, server rendering or framework-level data loading demonstrably outweigh their maintenance costs |
| Long-running technical jobs | Dedicated worker process, durable database state and an allowlisted task registry | RQ requires Redis/Valkey; Celery adds a broker and powerful routing, scheduling, retry and monitoring primitives. Both can be integrated behind the job boundary later. HTTP background tasks and in-memory queues do not meet durability requirements. | Multiple workers/hosts, sophisticated routing, scheduling or throughput exceed the tested single-host worker |
| Scheduling | Explicit submission of finite technical runs; future scheduling uses the same job interface | A timer inside each API process risks duplicate execution. Neither cron nor a scheduler by itself supplies durable job semantics. | An authorised recurring workload with ownership, idempotency, timezone and missed-run policy |

Choose the monolith because these capabilities share identities, permissions and research records. Run API and worker as separate processes when work is long-running; separation does not require microservices, network calls between every module or a distributed event bus.

## Evidence and engineering consequences

### API and contracts

FastAPI deployment documentation distinguishes API worker processes, startup, restarts and memory replication [ST-01]. CPU-intensive research work must therefore not run in an API request handler or rely on process memory for shared job state. Migrations run as an explicit single deployment operation before serving traffic, not once in every API worker.

Pydantic documents Python type-driven schemas, JSON Schema, validators and strict/coercing modes [ST-02]. Public schemas should reject unknown fields where appropriate, validate finite numeric values, specify timezone/precision and separate versioned DTOs from ORM objects. Strict validation is selected per field: JSON timestamps necessarily need parsing. Do not mistake successful schema validation for a trustworthy observation timestamp, licence or dataset.

Use OpenAPI as the API contract source and check the frontend contract against it. Keep domain/application services independent of FastAPI request objects and concrete database sessions. Do not expose arbitrary Python import paths, SQL, filesystem paths or executable functions as a job submission API.

### Metadata and artifacts

SQLite's official guidance permits many readers but only one simultaneous writer; it recommends a client/server database for many writers or direct multi-host access and warns about network filesystem locking [ST-06]. Initial metadata must stay on local persistent disk, with short transactions, bounded lock waits and tested concurrent job claims. Long computations occur outside write transactions. SQLite is a deployment choice with an upgrade condition, not a temporary application to replace.

SQLAlchemy's SQLite documentation identifies legacy Python `sqlite3` transaction behaviour, transactional DDL/savepoint implications and foreign-key configuration [ST-03]. Explicitly configure and test transaction/FK behaviour; do not assume ORM use solves it. Alembic provides a migration tool for SQLAlchemy [ST-11]. Migration review, upgrades on existing stores, backups and restore checks remain application responsibilities. No tested PostgreSQL support may be advertised until migrations, repository invariants, job claims and failures pass against PostgreSQL.

Parquet contains data; metadata contains identities, schema versions, hashes, provenance, partition permissions and artifact references. Publish immutable artifacts atomically and then register them. Handle interrupted publication and orphaned artifacts explicitly; a hash is integrity evidence, not permission to access a reserved partition. Keep a consistent backup of both stores.

DuckDB supports projection/filter pushdown and direct Parquet queries [ST-12b]. Its in-process mode allows one read/write process, or multiple read-only processes; concurrent writer threads have conflict semantics [ST-08b]. The current documentation also describes Quack and DuckLake alternatives, so it would be incorrect to claim DuckDB has no multi-process options at all. III selects isolated embedded analytical connections over approved immutable files and does not adopt those distributed alternatives. Disallow arbitrary remote paths, SQL and extension loading from untrusted clients; the library's ability to read HTTP Parquet is not permission for the platform to fetch it.

### Frontend choice

React's own documentation recommends frameworks for many applications and warns that a build-tool-only application must supply routing, data fetching and error/loading behaviour [ST-04]. Vite is explicitly documented as a React/TypeScript build option. Our decision is limited to an authenticated operational dashboard whose business logic and data already live in Python. Supply stable navigation, reusable API access, request cancellation/error handling, real empty states and independent chart components; do not create an improvised second backend inside the client.

Next.js is a credible alternative, not rejected as inherently costly or proprietary. Its official self-hosting guide covers reverse proxies, caches and coordination across instances [ST-05]. Static export avoids a Node server but supplies no immediate advantage over the selected SPA for current requirements. Avoid duplicating authentication, backend logic or scientific calculations in a JavaScript server. A production Vite build requires a supported build environment; it does not require running its development server in production.

### Jobs, recovery and ownership

Celery documents dedicated workers, broker-mediated messages, retry, routing and monitoring [ST-09]. RQ is simpler but still requires Redis or Valkey and a worker [ST-10]. III has finite synthetic verification jobs, so an application-specific durable worker avoids another service without claiming equivalent general-purpose orchestration.

The worker must persist queued/running/succeeded/failed states, configuration and attempts; atomically claim a task; record worker ownership and progress; and provide an explicit recovery path after process loss. If leases/retries are implemented, stale owners must not publish over a new attempt. Exactly-once execution is not assumed. Repeated work must either be idempotent or create a distinct preserved attempt. Persist exceptions in safe structured form and keep the API responsive. Registry allowlists select installed trusted tasks, never user-supplied executable strings. Scheduling is a future adapter, not permission to start continuous research.

## Licences, security and operational cost

| Component | Primary declaration checked | Implication within this review |
|---|---|---|
| FastAPI; Pydantic; React; Vite; Next.js; DuckDB | MIT licence text, LIC-01–06 | Permissive private use; preserve relevant copyright/permission notices when redistributing |
| SQLAlchemy; Alembic | SQLAlchemy documentation footer, ST-03; Alembic licence text, LIC-09 | MIT terms; migration tooling does not remove application migration obligations |
| SQLite | Public-domain declaration, LIC-08 | SQLite core requires no licence; bundled tooling can carry separate terms |
| PostgreSQL | PostgreSQL Licence, ST-07 | Permissive use, copy, modification and distribution subject to retained notices |
| Apache Arrow / PyArrow | Apache-2.0 principal terms and bundled-components notice scope, LIC-07 | Retain applicable licence/NOTICE and third-party notices; inspect the exact installed distribution |
| Celery; RQ | BSD-3-Clause text LIC-10; RQ official page declares BSD, ST-10 | Alternatives not adopted now; broker licences and release-specific dependencies need their own check |

These are upstream snapshots, not a complete licence audit of resolved dependency trees, legal advice or a grant of rights to exchange/news datasets. Raw repository licence URLs follow moving branches; retrieval hashes preserve what was examined. Arrow's long third-party appendix was not exhaustively audited. RQ's exact BSD variant was not checked. Preserve a release-specific dependency inventory and notices during implementation; do not infer transitive licences from the top-level package.

The cited projects have accessible official documentation and established integration surfaces. That is evidence of available capabilities, not a measured security, performance or maintenance guarantee. Pin/test selected releases, review security updates and record the environment; no comparative benchmark or vulnerability audit was run in this document.

Initial software licence fees for these selected open-source components are not required by the reviewed terms. Hardware, electricity, storage, backup, engineering and maintenance still have costs. A local API/worker/database/static client can avoid a paid service now; an appropriately sized server, managed PostgreSQL or a broker is an alternative once a concrete requirement warrants its cost. No cloud purchase, account credential or paid licence is authorised by this decision.

Default deployment is local and authenticated, with explicit roles, configuration outside Git and no exchange credentials. A future remote deployment requires TLS, trusted proxy settings, secure identity/session handling, resource limits and backups. Same-origin hosting reduces CORS configuration but is not an authentication or CSRF control. A modular monolith is not a sandbox against malicious Python plugins: only trusted installed modules may execute, and a future autonomous researcher needs separate tool/process restrictions.

## Verification required in implementation

Run installation/startup, migrations/persistence, schema/API contract, frontend build/type/unit/integration, permission and failure-path checks. Demonstrate an added module, an optional internal capability, and a replacement implementation without changing unrelated domains. Verify technical-run reproducibility and inability to dispatch a real order. Test job recovery and preserve failed attempts. The implementation report must distinguish passed checks from proposed capabilities; this review does not mark any of them passed.

## Source scope

The original assessment was dated 2026-10-18. Its missing ledger and stack cache could not be recovered, so their exact retrieval history is not asserted here. A bounded recovery on 2026-10-19 retrieved and hashed twelve substantive official pages and ten licence/declaration snapshots. Four additional requests returned HTML redirect shells rather than documentation; the canonical `/docs/current/` successors for ST-08b/ST-12b supplied the DuckDB content. All 26 recovery requests returned HTTP 200, which alone did not establish substantive access. Relevant sections were inspected, not every linked page. The ledger separates new recovery receipts from directed reading and does not invent earlier events. This review introduces no academic studies, financial datasets, performance experiments or continuous research jobs.
