# Using the technical platform

Canonical language: English. Revision: 2. Updated: 2026-10-20. Spanish counterpart: [usage.md](../es/usage.md).

The current platform exercises software using synthetic data. The original scientific hypotheses remain research questions. A successful technical task, a chart or an accounting invariant does not demonstrate predictive power or net profitability.

## First session

Follow [installation](installation.md), initialize the state and sign in with the private local credential. The dashboard reads actual backend records. Empty states mean that no matching records exist; they are not filled with invented results.

| View | Interpretation |
|---|---|
| Platform status | Technical mode, record counts and disabled live execution; counts are bounded and are not a worker health guarantee |
| Hypotheses | The 25 preserved H-00–H-24 records, original Spanish content and source provenance |
| Datasets | Synthetic catalog, version, input specification, partition and provenance; reserved payloads remain closed |
| Chart | Backend-provided `SYNTH-USD` candles, volume and trailing overlay; simulated clocks and prices |
| Technical attempts | Configuration, durable state, manifests, errors and generated technical reports |
| Modules | Declared dependencies, capabilities and operational/prepared/planned state |
| Audit | Persisted service events and errors with safe identifiers |

The UI is a client of the implemented services. Read module descriptions as well as their state: a working synthetic data service does not imply a market feed, and a prepared model contract does not imply financial training.

## Create a fixture and submit a technical task

Create a seeded fixture through the dataset workflow or CLI:

```bash
uv run --frozen bot-trader fixture --seed 42 --rows 120
```

The fixture instrument is `SYNTH-USD`, its currency is USD and its availability clocks are simulated. Its interval is a test configuration, not a selected trading horizon. Data generation is bounded to at most 10,000 rows. The final partition cannot be created or opened through ordinary Phase III workflows; reserved records used by security tests are denied to all roles.

Choose a recorded dataset version when submitting an attempt. The finite task catalog is:

| Task | What it verifies |
|---|---|
| `quality_check` | Artifact/schema/clock integrity and bounded aggregate queries over verified synthetic input |
| `transform_check` | A versioned trailing mean, using only observations already available to the transformation |
| `ledger_check` | Deterministic synthetic spot accounting and cost/risk contracts, with no market execution |
| `failure_fixture` | Intentional safe failure, demonstrating that failed attempts remain visible |

Run the worker in a separate process. States are `queued`, `running`, `succeeded`, `failed`, `interrupted` or `cancelled`. Cancellation fences persistence of a late result; it is not a hard process-kill mechanism. Recovery marks a stopped worker's unfinished attempts as interrupted and does not replay them automatically.

Successful tasks provide JSON and Markdown reports through the authorized artifact endpoint. Failure records keep their safe error codes. Artifact access rechecks input lineage and partition permissions; a guessed filename or old run identifier cannot open reserved data.

## Repeatability and comparisons

A run freezes its configuration, dataset version and content identity, seed, source hash, Git revision/dirty state, lockfile and selected environment versions. The worker checks that identity again before and after execution. Editing backend source, changing dependencies or committing a new revision between submission and execution can therefore invalidate a queued attempt. Finish or cancel the relevant work before development changes; retain invalidated attempts and create new ones. Restart the API and every worker after executable/dependency changes: a process retaining imported code cannot safely represent the updated files and is rejected until restarted.

Attempt identifiers and timestamps differ on repeat execution. The deterministic report digest should match for equivalent immutable inputs and code/environment. Compare two to ten distinct attempts through the comparison workflow/API. `comparable` means matching frozen configuration and manifests; `same_result` additionally requires matching successful result digests. Neither field ranks strategies or chooses a winner.

Seed capture alone is not a universal guarantee across dependency or platform changes. The platform records these differences and enforces the current identity; it does not claim arbitrary cross-platform numerical equivalence.

## Scientific and temporal records

`init` imports the source hypothesis text without rewriting its nulls or refutation conditions. Repository versions are append-only; a later source change produces a new version instead of erasing the old one. The English technical documentation does not replace the Spanish scientific source.

The API accepts an optional `hypotheses` list in `TechnicalRunSpec`. Each association uses `kind: "hypothesis"`, the persistent `id`, exact `version` and `content_hash` from the registered record. Submission resolves and freezes these references; reads and worker execution check the same historical versions. A later hypothesis version does not rewrite a previous run. Omit the list for a standalone software check. These associations document research context only: a synthetic task cannot validate the associated hypothesis. The current web exposes them in the frozen configuration/provenance, without a separate strategy-management workflow.

Temporal utilities prepare finite chronological and expanding walk-forward plans, with label availability, overlap exclusion and purge/embargo rules. They do not fit models, read the final partition or prove that historical timestamps are trustworthy. A future protocol must choose horizons, costs, search budgets and admission criteria before financial evaluation.

## Research proposals and limits

The API can record inert research proposals with rationale, null hypothesis, refutation, source references, model/prompt provenance and requested resources. Each actor is limited to 20 proposal records and 100 requested budget units in persisted state. A budget unit is a technical quota, not money or permission to spend. A stored proposal is pending review, non-executable and carries no authorized budget.

No autonomous agent reads a proposal and acts on it. Text, URLs and model output remain data; there is no shell, tool invocation, URL fetch or model training attached to them. Agent credentials can read limited metadata and submit proposals, but cannot read dataset payloads or run jobs.

All technical results retain `synthetic: true` and `financial_validation: false`. The financial experiment counter remains zero. Moving to a scientific protocol or financial experiment requires the next explicit authorization; the interface cannot grant it.
