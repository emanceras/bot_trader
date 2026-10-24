# Future result presentation and contextual help

Document ID: UX-PLAN-001 · Version: 1 · Updated: 2026-10-24 · Language: en (canonical).

Translation: [Spanish](../es/ux-evolution.md), synchronized with UX-PLAN-001 v1. Status: **documented future work, not implemented by this plan**. The Phase IV request asks for this backlog before methodological work and explicitly excludes implementing these improvements now. None is a prerequisite for completing IV. Existing scientific priorities, permissions and the [architectural supplement](architecture/supplement.md) remain unchanged.

## Inspected baseline and decision

This is a bounded internal design review, not external UX research or a claim of user-tested usability. It inspected `web/src/sections.ts`, `views.tsx`, `components.tsx`, the existing [usage guide](usage.md), and the supplement's navigation recommendations. Six functional sections already exist. The technical-attempt view shows job states, JSON results, downloadable reports, and expandable configuration/provenance. `JsonDetails` is reusable. Dataset charts already separate backend calculation from rendering. The usage guide covers current tasks and their limits, but no integrated glossary, comprehensive contextual guide or financial summary service exists.

**Recommendation:** enhance existing result views, maintain one versioned help content set, and expose it through contextual links plus a small shared Help entry when useful content is ready. Preserve the current visual identity and six working sections. A glossary and guide can share help navigation; they do not require separate primary tabs. Search should start within help content and grow only if actual navigation needs justify it. No new application, frontend framework, dependency, database service or empty page is needed by this proposal.

| Alternative | Benefit | Cost or limitation | Disposition |
|---|---|---|---|
| Repository documentation only | Already available, versionable, inexpensive | Users must leave the workflow; terms and exact parameters are harder to find | Retain as canonical content and fallback, improve contextual access later |
| Dedicated primary tabs for results, glossary and guide | Easy to discover | Competes with functional navigation; duplicates existing result/detail views | Do not add three tabs; revisit only for demonstrated navigation needs |
| Tooltips only | Compact explanation at point of use | Poor for long explanations, keyboard/touch access and durable linking | Use only optional short hints, never the sole access to a definition or critical caveat |
| Shared Help area with contextual links and expandable detail | Explanation without abandoning the task; one content source | Needs stable anchors, focus handling and content maintenance | Preferred incremental approach |
| Global search, tours or conversational help first | Broad discovery or guided onboarding | Index permissions, stale answers, tour maintenance, inference cost and distraction | Defer; start with static help navigation/search, no AI assistant required |

## Result presentation contract

Use progressive disclosure: a short statement of what was checked, a compact table or suitable chart, comparison meaning and limitations, followed by expandable raw records and report downloads. A technical ledger check should summarize its accounting assertions and synthetic units; it must not show invented Sharpe, profitability or a strategy recommendation. An unavailable statistic is `not applicable`, `not computed` or `insufficient evidence` with a reason, never a fabricated zero.

Keep distinct dimensions visible instead of encoding them in one badge:

| Dimension | Example future representation | Interpretation |
|---|---|---|
| Data/result scope | Synthetic technical check; historical financial evaluation; prospective observation | Describes the evidence source and task, not its quality |
| Execution state | Queued, running, succeeded, failed, interrupted, cancelled | A completed computation is not a successful hypothesis |
| Scientific disposition | Not assessed, provisional, evidence against the claim, inconclusive, supports the preregistered claim within scope | Requires the actual protocol, comparator, uncertainty and review record; no automatic label from P&L or job success |
| Review/validation scope | Technically verified for named checks; reviewed on named out-of-sample data | “Validated” must name what was validated and its limits; it never means guaranteed profitability or live permission |

These are display semantics for future records, not a new executable lifecycle or a migration in IV. Negative financial evidence, an intentional software failure and a failed infrastructure task have different meanings. Preserve all three in their appropriate histories. A provisional result can also be adverse or inconclusive; these labels need not be mutually exclusive.

Every future metric/plot must identify its source record and version, dataset scope, period/timezone, units and account currency, calculation version, benchmark, treatment of costs and uncertainty when relevant. Historical versus prospective, gross versus net, USD versus a stablecoin, and observed versus modeled values must be explicit. Use the backend's governed statistics and comparable-run criteria; do not recompute research statistics or invent ranking rules in the frontend. Incomparable or unsuccessful runs must not be rendered as proved numerical differences. Raw JSON, hashes, configurations and manifests remain reachable without exposing reserved or unauthorized payloads.

## Glossary and guide content model

Create terms when they appear in a current feature, an admitted protocol or a recurring user question. Initial content should explain fixture, dataset/version, availability time, seed, manifest/hash, job/worker, comparison, holdout, leakage, benchmark, net costs and uncertainty. Extend to orders/liquidity/risk, performance metrics, portfolio concepts and ML only when the corresponding functionality or protocol uses them. Do not attempt a generic financial dictionary.

Each term needs a stable language-independent ID, Spanish/English preferred labels and synonyms, concise definition, scope/caveat, links to related terms and the relevant workflow, revision, and a small bot_trader example where useful. A hash example must explain integrity rather than truth; a seed example must not promise reproducibility across every environment. Cite the existing scientific or technical source where a definition's meaning depends on it. Link to longer methodological material instead of duplicating it. Translations share the same ID and scientific meaning; untranslated content must be labelled rather than silently substituted.

Evolve the existing usage guide into task-oriented help: purpose and current capabilities; first session; section-by-section tasks; field/parameter meanings and valid ranges; state/graph/result interpretation; common errors and recovery; limitations; and how data, jobs, worker, results and audit relate. Each task should state prerequisites, role/permission, exact steps, expected visible outcome, errors and where to inspect evidence. Match instructions to the actual application version and capability state. Keep installation/development internals linked separately; the guide should explain enough to understand behavior without duplicating implementation documentation. Do not publish future operational instructions as though a button or service existed.

## Bounded backlog

All items are **planned, unimplemented**, with no new dependency approved. They can be admitted as later software work alongside the relevant authorized phase; financial presentation also depends on a separately admitted calculation/evaluation service. Their order does not delay IV.

| ID | Deliverable and smallest useful increment | Dependencies | Acceptance criteria | Reconsideration / future timing |
|---|---|---|---|---|
| UX-01 | Readable result summary inside the existing attempt detail; begin with current technical tasks, retain expandable audit records | Existing immutable reports and typed result semantics; financial summaries require approved protocol and backend metric service | User can identify what ran, its scope/outcome and limitations; displayed values reconcile with the same report/version; failures, missing metrics and incomparable runs remain explicit; raw evidence still accessible; no permission bypass | Later authorized UI maintenance for technical summaries; financial visuals only when that service exists, not by fabricating samples |
| UX-02 | Small bilingual glossary with stable term anchors and contextual links | Inventory of terms actually used; reviewed definitions and translation mapping | Same term resolves from guide and UI; keyboard/touch access; terms include scope and examples where useful; no contradictory duplicate definitions or unsupported scientific claims | Start with one current workflow; expand only on feature/protocol demand |
| UX-03 | Extend the existing usage guide with complete task explanations, parameters, expected states, troubleshooting and limitations | Actual capability registry, existing usage/installation/security guides; reviewed UX-02 terms where referenced | Each available section/task is covered; role constraints and worker requirements match the software; screenshots/examples are versioned and labelled; planned modules remain planned; no secrets in examples | Increment per implemented workflow; maintain with the same release that changes behavior |
| UX-04 | Shared help entry and contextual navigation, then bounded help search if useful | Useful UX-02/03 content first, stable anchors; reusable UI components | Links open the exact definition/task; browser back and focus restoration work; no empty destinations; clear language selection and mobile behavior; search indexes only permitted help content | Admit after content exists; add broader search or tours only after a concrete discovery problem is observed |

No item requires changing the scientific protocol, C1–C5 priorities or phase authorization. Future effort must be scoped per item rather than treating this backlog as permission to implement everything simultaneously. No calendar promise, dependency purchase or paid service is implied.

## Accessibility, verification and maintenance

Preserve the current visual identity while using semantic headings/tables, visible keyboard focus, descriptive labels and text alternatives for plots. Communicate state through words as well as color. Essential explanations must work on touch and keyboard; a hover-only tooltip is insufficient. Long definitions belong in a linkable panel/page, with explicit close/back behavior and restored focus. Respect reduced motion, readable contrast and narrow screens; do not add animation as a substitute for explaining a result.

On later implementation, verify a technical success, an intentional failure, an interrupted task, missing/not-applicable values and an incomparable pair against real service records. Financial negative/inconclusive examples may use clearly labelled UI test fixtures without being presented as project evidence. Check that expanding audit details does not fetch a reserved payload, that links and translation versions remain valid, and that keyboard navigation reaches and leaves help predictably. Charts need an equivalent readable summary/table; exact accessibility requirements should be checked against the standards adopted for that implementation rather than claiming certification from this review.

Content ownership follows the relevant module and canonical documentation: scientific wording is reviewed with protocol changes, technical task instructions with service changes, and translations in the same documentation revision. Prefer reusing versioned Markdown or another small reviewed content structure; choose a renderer/index only when implementation requirements justify it. Avoid rendering raw external HTML or executing instructions from help or research text. No tutorial should mutate state or trigger a job without an explicit user action and the normal service permissions.

The plan is complete as a future-work record. No frontend/backend files, dependencies, controls, sections, experiments or authorization policies are changed by it; usability and accessibility checks above remain future acceptance work, not tests already passed.
