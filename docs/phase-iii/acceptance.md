# Phase III acceptance and requirements traceability

Document ID: ACCEPT-III-001 · Version: 1 · Updated: 2026-10-18 · Language: en (canonical checklist, Spanish summary below).

Baseline: [user request](REQUEST.es.md), sections 18–22, and [architecture ARCH-001](../en/architecture/platform.md). Initial state: **documented targets, not implemented/verified claims**. The integration owner records actual evidence before closing gates. Technical test passes are not financial validation. Preserve failures and link reruns rather than replacing them silently.

## State vocabulary and gate order

`documented` = specification exists; `implemented` = executable component exists; `tested` = identified checks passed; `prepared` = contract/inactive future integration; `blocked` = unresolved essential criterion. “Operational” applies only to an implemented and tested capability within its declared scope. III.A must be reviewed before dependent III.B implementation. III.A→III.B is already authorized; IV is not.

For every gate, record command/test ID, date, environment, outcome and remaining limitation in the technical verification report. A table mapping a requirement is not evidence that it passed.

## III.A: nineteen architecture deliverables

| Request §19 | Deliverable | Reference/required evidence |
|---|---|---|
| 1 | Repository diagnosis | ARCH §1; inspect real Git/files, preserve baseline scientific records |
| 2 | Functional/nonfunctional requirements | ARCH §1 and this acceptance register |
| 3 | Target architecture | ARCH §§2–3, all fifteen requested domains |
| 4 | Compared alternatives | Technical research with official URLs, consulted dates, limits and license evidence |
| 5 | Recommended stack | ARCH §2; pinned-version compatibility confirmed before implementation |
| 6 | Component diagrams | ARCH §2; process/storage separation reconciled with implementation |
| 7 | Module contracts | ARCH §§3–4; concrete typed public boundaries |
| 8 | Extensibility strategy | ARCH §3; manifests, capability registry, injection and tests A–C |
| 9 | Data model | ARCH §4; provenance, time, units, versions and reserved partitions |
| 10 | Frontend/backend architecture | ARCH §§2,6; real API, reusable chart and section boundaries |
| 11 | Simulation/execution engine research | Official comparisons of adoption vs integration vs patterns; explicit engine admission gate |
| 12 | Laboratory design | ARCH §5; immutable inputs, deterministic technical lifecycle and failures |
| 13 | Paper trading design | ARCH §§3,7; first-class inactive module, independent future authorization |
| 14 | Autonomous researcher design | ARCH §7; proposals, evidence, budgets, permissions and injection isolation |
| 15 | Chart analysis design | ARCH §6; renderer separate from scientific transforms; license/attribution checked |
| 16 | Security/isolation | ARCH §7; default deny, no live adapter, holdout enforcement |
| 17 | Costs/resources | ARCH §8; personal baseline, cost classes, no purchases |
| 18 | Technical decisions | DECISIONS records alternatives/consequences and official research basis |
| 19 | Implementation plan | ARCH §8; dependency-ordered work, test evidence and resumption checkpoint |

III.A exit requires consistency among research, decisions, architecture and implementable contracts; no material unresolved license/compatibility issue for adopted components; and a bounded III.B plan. Deferred market-engine selection is acceptable only with a concrete later protocol gate and a deliberately limited technical harness.

## III.B: twenty implementation deliverables

| Request §20 | Deliverable | Acceptance evidence required |
|---|---|---|
| 1 | Durable repository structure | Backend/frontend/tests/migrations/docs established; no disposable parallel application |
| 2 | Modular core | Registry/dependency/capability checks and A–C; reject missing dependencies/cycles |
| 3 | Configuration | Validated settings, safe defaults, bounded paths/resources and invalid-config test |
| 4 | Shared schemas/contracts | Typed versioned time/data/order/risk/model contracts; invalid inputs rejected |
| 5 | Functional backend | Real authenticated endpoints, safe errors and API integration checks |
| 6 | Persistence/migrations | Fresh database migration, restart persistence, upgrade discipline and job recovery |
| 7 | Data/validation infrastructure | Synthetic content-addressed dataset, schema/quality checks, provenance and holdout denial |
| 8 | Hypothesis/experiment registers | H-00–H-24 preserved; immutable run config/history, success and failure retrieval |
| 9 | Base quantitative laboratory | Execute a bounded synthetic run, transform data, compare runs, produce persisted artifacts/report |
| 10 | Model/strategy contracts | Versioned input/output interfaces and meaningful substitute implementation check; no claimed financial training |
| 11 | Technical simulation | Deterministic synthetic orders/fills/spot balances/costs with accounting assertions and no market adapter |
| 12 | Functional web | Browser exercises overview, hypotheses, datasets, experiments/results, capabilities and errors against real backend |
| 13 | Reusable chart | Real synthetic series fetched and rendered; adapter boundary, lifecycle handling and attribution |
| 14 | Module registry/status | Actual registry exposed through API/UI; operational/prepared/future states accurate |
| 15 | Observability/errors | Correlation IDs, safe API failures, persisted job error and inspectable audit/health |
| 16 | Automated tests | Appropriate type/quality/backend/frontend/API/security/integration checks with exact outcomes |
| 17 | Modularity checks | A/B/C are behavioral tests, not assertions that folders exist |
| 18 | Reproducible environment | Locked dependencies; clean install/build/start path, fresh storage and documented worker |
| 19 | EN/ES documentation | Architecture/install/development/use synchronized with version metadata; history translation plan preserves originals |
| 20 | Next-phase plan | ROADMAP states actual completion/limits and IV dependencies; no IV execution |

## Mandatory demonstrators A–F

| Test | Concrete demonstration | Passing condition |
|---|---|---|
| A — Add module | Register a test extension through the public manifest/composition API, with declared dependency and service/capability | Extension is discoverable and callable without editing unrelated modules; invalid dependency/cycle rejected |
| B — Internal extension | Add an optional transform/chart or equivalent capability to an existing module using its public extension point | New capability runs; existing capabilities and unrelated consumers remain unchanged |
| C — Substitute implementation | Run the same consumer/contract suite with two storage/model/transform or execution implementations | Observable contract behavior remains valid; no consumer-specific implementation branching |
| D — Environment isolation | Attempt unauthorized runtime mode, external/live adapter, reserved payload and prohibited agent action | Fail closed through service/API/worker paths; no exchange/network order capability exists |
| E — Reproducibility | Execute two technical attempts with identical synthetic data/specification/seed/code/environment identity | Stable result/content hashes match; attempt IDs/times differ without replacing history; failure is also persisted |
| F — Web integration | Start built frontend/API and use a browser to read actual hypotheses, dataset/series, technical result and module states | Visible content corresponds to backend records; chart renders; synthetic labels, empty/error/unauthorized states honest |

## Cross-cutting checks and closure rules

- Installation: resolve from committed locks, migrate an empty database, initialize local authentication, build and start; record exact supported runtimes.
- Contract/persistence: UTC/availability and money/unit invariants; reject malformed/extra fields, missing artifacts and incompatible schemas; persist across restart.
- Security: unauthenticated/unauthorized requests, CSRF, session expiry/revocation, path traversal, bounded payloads, holdout/agent restrictions and no secrets in repository/logs. No financial live route or market-import bypass.
- Work lifecycle: competing claims, execution failure, interrupted recovery and duplicate completion cannot silently mark success or lose provenance.
- Quality/UI: appropriate Python static/type checks, TypeScript/build and frontend tests; real browser validation supplements unit tests.
- Documentation: local links/translation versions, source/license records, actual capability states, financial experiment counters unchanged and historical hypotheses preserved.
- Release: review diff, retain failures/limits, coherent commits, authorized normal push, verify remote commit and clean/explicitly explained Git state.

Essential failures in installation, actual laboratory execution, persistence, UI integration, security isolation or A–F keep III open. Optional future capabilities can remain prepared/planned if labelled and tied to an admission gate. Do not redefine a failed essential criterion as optional simply to close the phase.

Final report must distinguish operational software, prepared contracts and future functions; list executed checks and unresolved issues; state resources/decisions needed next. IV, financial datasets/experiments, prospective paper and live operation remain separately authorized work.

## Resumen español

Esta matriz vincula los **19 entregables de III.A**, **20 de III.B** y **pruebas A–F** con evidencia concreta. Su redacción inicial no certifica implementación. La aceptación de arquitectura precede al desarrollo dependiente, sin pedir otra autorización entre III.A y III.B.

Para cerrar III deben funcionar instalación/arranque, persistencia/migraciones, laboratorio sintético, API y web reales; comprobarse sustitución/ampliación/incorporación de módulos, reproducibilidad y denegación de operativa real/holdout. Se registran comandos, entorno, resultados y limitaciones; los fallos y resultados negativos no se borran. Las funcionalidades preparadas y futuras se diferencian de las operativas. Pruebas técnicas no validan rentabilidad y IV sigue requiriendo aprobación explícita.
