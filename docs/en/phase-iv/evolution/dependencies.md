# PyArrow, DuckDB and the engine boundary

Document ID: EV-DEPENDENCY-001 · Version: 1 · Date: 2026-10-27 · English canonical. [Spanish](../../../es/phase-iv/evolution/dependencies.md).

## Finding and provenance

The **current dependency constraints conflict** with the tested Nautilus version. That establishes an incompatibility between the present requirements, not that upgrading PyArrow is impossible or that a separate worker is necessarily better. Keep production unchanged during this documentary review; compare the two routes below before choosing an implementation.

| Evidence inspected | Finding and limit |
|---|---|
| [`pyproject.toml`](../../../../pyproject.toml), Git history | `pyarrow>=19,<24`, `duckdb>=1.2,<2` and Python `>=3.12,<3.13` were introduced in `2cf79b4` (2026-10-19); no later change to this file appears in the inspected history. The commit and inspected architecture/decision documents provide no specific reason for the `<24` boundary. Its purpose cannot be reconstructed as a known upstream defect, security restriction or permanent compatibility ceiling |
| [`uv.lock`](../../../../uv.lock) | Current resolved PyArrow **23.0.1** and DuckDB **1.5.6**. A permissible version range is distinct from the version used to reproduce the existing application |
| [A/B admission](../admission.md), D-041 | Installed Nautilus **1.231.0** metadata requires `pyarrow>=25.0.0`; the isolated probe resolved PyArrow 26. These requirements have no intersection with production `<24`. Existing installation/synthetic evidence is reused; no installation or resolver run was repeated here |
| [`market_data/service.py`](../../../../src/bot_trader/market_data/service.py) | Current synthetic artifacts explicitly use UTC microsecond timestamps, `decimal128(24,8)`, Parquet 2.6 and Zstandard. The reader validates authorization, identity and content before analytical access. This narrow implemented schema is not an admitted nanosecond market-event contract |

No source/lock or runtime change follows from this review. The [engine comparison](engines.md) also identifies a v1/v2 maintenance transition: satisfying 1.231.0's Arrow requirement would not prove that release is the best future engine, nor resolve its liquidity/recovery gaps.

## Compare the two routes on the same requirements

| Dimension | Upgrade the application's dependency set; engine in process | Separately versioned engine worker |
|---|---|---|
| Compatibility and maintenance | One tested Python/dependency set and fewer deployed components; must establish Arrow/DuckDB/application/engine compatibility together. Future upgrades remain coupled | Independent locks can accommodate conflicting package versions and different runtimes; protocol/schema compatibility and two release processes still need maintenance |
| Latency and resource use | Avoids process transport for ordinary calls; startup, conversions, engine work and memory use still need measurement | Adds scheduling, serialization, transport and possible copying. Batches may amortize overhead at the price of delay/memory; no claim that IPC is universally zero-copy or fast enough |
| Data and clocks | Direct objects can still lose precision or availability semantics through conversions | Explicit wire schema makes the boundary inspectable, but conversion bugs can multiply. Preserve event/publication/availability/receipt/decision times and sequence; use monotonic elapsed clocks for local durations, not wall-clock subtraction across processes |
| Reproducibility | Record complete resolved environment and writer/reader options; one process does not make runs deterministic automatically | Record both environments, schema/protocol versions, message order, configuration and artifact hashes. Independently versioned components must reject unsupported combinations |
| Idempotency and accounting | Durable command/fill IDs, transaction boundaries and reconciliation remain necessary across restarts | Durable outbox/inbox or equivalent protocol needs acknowledgment, duplicate detection, replay and ownership rules. A timeout means unknown outcome, not permission to resend an order with a new identity |
| Recovery and failure isolation | Fewer coordination failures; an engine exception/native crash may affect the host process. Application-level durable recovery is still required | Worker crashes can be contained, but a separate process alone does not isolate shared files, memory exhaustion or network side effects. Recover orders, fills, balances and positions across both sides before accepting new risk |
| Rollout and rollback | Revalidate existing artifacts/services, then deploy a reviewed lock migration with coherent backup/restore | Upgrade worker/protocol independently only within admitted combinations; draining, in-flight commands and checkpoint compatibility complicate rollback |
| Platform integration | Existing composition/permission boundaries can host an adapter; the synthetic v1 full-fill contract cannot be silently widened | Same platform/API/UI can supervise a worker through a typed port. A second UI/platform or automatic live capability is unnecessary |

The worker is a **credible isolation option**, not an automatic consequence of an undocumented cap. An in-process upgrade remains credible if an exact maintained engine and candidate dependency set satisfy the same semantic, resource and recovery gates with less total burden. Retain both proposals until a finite authorized comparison answers the material uncertainty; neither is implemented or admitted here.

## Interchange details that can change correctness

DuckDB 1.5 documentation supports Arrow tables, datasets, scanners and `RecordBatchReader`, with projection/filter pushdown [D5]. This describes interfaces, not certification of DuckDB 1.5.6 with each candidate PyArrow release. The cached `/docs/current/` requests [D1–D2] returned HTML redirect shells pointing to **2.0**; they are not the substantive documentation for the locked 1.5.6 build. The cached versioned 1.5 pages supply the claims here.

Precision is a decisive boundary. DuckDB 1.5 documents naive `TIMESTAMP_NS`, but timezone-aware `TIMESTAMPTZ` has microsecond precision; importing zoned nanosecond data, including Parquet with `isAdjustedToUTC=true`, can lose precision [D6]. Setting a timezone does not restore lost digits. Future high-resolution contracts should preserve the authoritative integer epoch value with explicit unit, clock meaning and ordering key; retain timezone/calendar metadata separately where needed. Any derived SQL timestamp is a declared view with checked precision. Existing synthetic v1 microsecond artifacts remain versioned as such; do not relabel them or invent source precision.

Arrow's inspected Parquet writer documentation distinguishes format version, timestamp coercion, truncation permission and stored Arrow schema metadata [D3]. Parquet 2.6 can retain nanoseconds, but that does not guarantee every downstream reader does. The stored Arrow schema can restore timezone metadata on an Arrow read; it does not override a DuckDB type limitation. Pin writer options and verify the exact reader route. Preserve Decimal scale/precision, null-versus-missing meaning, dictionaries, units and instrument/currency identifiers; never pass accounting values through binary float just to simplify interchange.

Arrow IPC offers sequential streams and random-access files; all batches within a stream use its schema [D4]. Documented zero-copy reads require an appropriate source such as a memory map or `BufferReader`. Socket transport, conversions and compression/decompression may allocate or copy; Parquet memory mapping does not provide the same memory-saving guarantee. Choose a transport from measured workload, durability and latency requirements. Immutable hashed Parquet/IPC artifacts are plausible for bounded historical batches, while a versioned command/event channel is needed for interactive lifecycle messages. Neither format supplies durable delivery, idempotency, causal ordering or financial authorization by itself.

## Finite migration proposal — documentation only

Before execution, fix one maintained engine release and at most **one candidate dependency set per route**, alongside the unchanged current-lock baseline. Use one immutable invented fixture bundle and an independent Decimal/time/order oracle. This proposal neither installs packages nor runs the checks, and does not authorize a financial adapter or new data acquisition.

| Check | Required evidence before migration |
|---|---|
| M1 — dependency and startup | Exact resolved locks, Python/platform support, licence inventory and application/engine import/startup results. Preserve resolver failures; do not repeatedly broaden versions until a preferred outcome appears |
| M2 — existing artifact/service regression | Read a fixed synthetic v1 corpus through old and candidate environments; compare schema, values, availability/partition guards, immutable references and analytical results. New serialized bytes may differ across writer versions: preserve old hashes/artifacts and record new versions rather than rewriting history |
| M3 — precision and interoperability | Invented UTC and zoned ns/us values, same-microsecond distinct events, DST boundaries, nulls and Decimal edge cases through the exact Arrow→Parquet/IPC→reader routes. Prove ordering and exact declared values or reject unsupported conversion; no tolerance fitted to observed loss |
| M4 — lifecycle and crash recovery | Fixed duplicate-command/fill cases and crashes before acknowledgment, after a fill before local checkpoint, and during cancellation. Reconcile persistent order/fill/balance/position state after restart. Fresh replay of another fixture cannot pass recovery |
| M5 — bounded resource comparison | Same finite event shapes, order density and strategy/instrument counts; measure startup, serialization, processing, peak RAM/disk and latency tails separately. Fix workload, repetitions, resource ceilings and mechanism-derived acceptable latency before execution; do not extrapolate the earlier 10k no-order smoke test |
| M6 — rollout/rollback rehearsal | Version negotiation rejection, worker failure containment where applicable, interrupted artifact writes and restore from a coherent checkpoint/manifest. Preserve failed attempts; keep disallowed modes and reserved partitions denied in both directions |

Stop a route on a decisive mandatory failure and report the limitation. Retry only for an identified implementation defect within an explicitly bounded amendment, retaining the original outcome. Any implementation, installation, production migration or further synthetic execution needs its corresponding authorization; E3/E4, Phase V, market experiments and prospective paper/live remain pending. These checks can establish technical compatibility, not economic advantage or permission to operate.

## Sources and read scope

[Dependency receipts](../../../phase-iv/evolution/dependency-sources.jsonl) preserve original 2026-10-26 fetch dates/hashes and append the actual directed-reading scope. No new web retrieval was made in this resumed review.

- **D1–D2 / EV-DEP-01–02:** cached DuckDB `current` Arrow/timestamp HTML redirect shells only; target 2.0 identified, substantive target not read.
- **D3 / EV-DEP-03:** [Arrow Parquet writer](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html), directed reading of format versions, timestamp coercion/truncation, schema metadata and Decimal representation. Moving documentation snapshot, not proof that every option exists in locked PyArrow 23.0.1.
- **D4 / EV-DEP-04:** [Arrow IPC](https://arrow.apache.org/docs/python/ipc.html), stream/file schema, sequential/random access, conditional zero-copy and memory-mapping caveats. Examples read, not executed.
- **D5 / EV-DEP-05:** [DuckDB 1.5 Arrow interfaces](https://duckdb.org/docs/1.5/guides/python/sql_on_arrow.html), tables/datasets/scanners/readers and pushdown. No version-pair benchmark.
- **D6 / EV-DEP-06:** [DuckDB 1.5 timestamps](https://duckdb.org/docs/1.5/sql/data_types/timestamp.html), precision warning, zoned/naive semantics, conversions and calendar/DST discussion. No extension installed or example executed.
- Local evidence: dependency file and introducing commit, lock entries, the current synthetic serialization/read boundary, prior architecture and A/B admission. No market artifact or isolated environment was reopened.
