# Security and local operations

Canonical language: English. Revision: 2. Updated: 2026-10-20. Spanish counterpart: [security.md](../es/security.md).

This is a local single-host technical deployment with trusted source code and a trusted operating-system account. Application controls separate roles and research boundaries; they do not protect files from the host administrator, a malicious installed dependency or arbitrary code executed under the same account. A production or multi-tenant deployment needs a separate threat review.

## Credentials, sessions and permissions

`init` creates `.state/admin.token` with private file permissions and prints only its path. Additional role credentials are created explicitly:

```bash
uv run --frozen bot-trader credential researcher
uv run --frozen bot-trader credential viewer
uv run --frozen bot-trader credential agent
```

The commands return existing valid files rather than overwrite credentials. Restart the server after adding or changing credentials because it loads them at startup. Keep files private and outside version control; the loader rejects symbolic links and group/world-readable credential files. Custom state paths require the same protection as `.state`.

| Role | Allowed application scope |
|---|---|
| `viewer` | Read authorized technical datasets/results, hypotheses, modules, status and audit |
| `researcher` | Viewer scope plus synthetic dataset creation, finite task submission/cancellation and proposals |
| `admin` | Researcher scope plus worker/recovery/session-management policy; still no reserved payload or financial mode |
| `agent` | Limited metadata, hypotheses/modules and inert proposals; no dataset payload, technical jobs or live execution |

Sessions are random, bounded, revocable and held in API-process memory. Cookies are HttpOnly, SameSite Strict and expire after the configured lifetime. Logging out revokes the session; restarting the API revokes all sessions. Use one API process for this deployment. Session sharing across replicated API processes is not implemented.

Authenticated mutations require the session CSRF token. All mutations, including login, require an explicitly allowed origin; allowed-host checks apply separately. No permissive cross-origin API access is configured. Login attempts and active sessions are bounded. Error responses omit rejected credential values, raw traces and arbitrary external text; use correlation identifiers when investigating failures.

The supplied CLI binds to loopback. Development HTTP cookies are not marked Secure because the local endpoint uses HTTP. Production configuration requires HTTPS origins and secure cookies, but these flags do not themselves install TLS, a reverse proxy, hardened identity or deployment monitoring. Do not expose this development configuration publicly.

## Research and execution boundaries

Only `technical` mode is valid. There is no exchange adapter, live order transport, prospective paper service, arbitrary code job, market-data upload or autonomous model loop. An administrator cannot turn those on with a request field.

Final-partition payloads remain denied for every role. Restricted metadata hides seeds, artifact descriptors, quality summaries and payload hashes. Dataset access, chart/transform paths and derived run/artifact access recheck stored lineage. These controls are meaningful within the application trust boundary; direct host/database access can bypass the application and must be treated as privileged access.

Artifacts use bounded registered suffixes and content hashes, are published atomically and are integrity-checked on retrieval. Caller-controlled filesystem paths and arbitrary SQL/URLs are not accepted. DuckDB external access and extension loading are disabled. Incoming HTTP bodies, fixture sizes, queue depth and artifact sizes have finite limits. This is resource bounding, not comprehensive hostile multi-tenant isolation.

Proposals and source text are untrusted data, never instructions. Proposal quotas are persisted and checked transactionally: at most 20 records and 100 requested budget units per actor. They do not authorize financial expenditure or tool execution. No quota reset or autonomous proposal-to-job mechanism is provided.

Checksums detect mismatches within the recorded content; they do not prove that a source was correct, that all events were observed, or that external balances and positions reconcile. An approved recommendation would still need separately authorized execution and effective confirmation. The [supplementary review](architecture/supplement.md) defines these future decision and reconciliation boundaries without activating them.

## Stop, recover and investigate

Stop the API and worker with the normal process interrupt. A worker crash may leave an attempt marked `running`; jobs and audit records survive API restarts. There is no automatic heartbeat-based takeover or automatic replay.

First confirm that the worker with the recorded identity has stopped. Then, from the same state directory:

```bash
uv run --frozen bot-trader recover local-worker
```

Recovery records the affected attempts as `interrupted` without executing them again. A stale worker cannot subsequently finalize an interrupted or cancelled attempt. Nevertheless, recovery is not a process-kill command: recovering a still-active process can interrupt legitimate work. Inspect the attempt and safe error record before submitting a new attempt. Preserve the prior record.

The dashboard and CLI are local supervision tools. External alerts, on-call escalation, worker heartbeat monitoring, production kill switches and automatic service recovery are future operational capabilities. Their absence is one reason the current platform is not admitted for market execution.

## Backup and restore

For a coherent local backup, stop **all writers**: API, workers and modifying CLI commands. Wait until they have exited, then copy the entire state directory to a private backup location, preserving permissions. Include the SQLite database, any SQLite companion files, immutable artifacts and the private credential files. Record the source commit, lockfiles and schema revision alongside the backup. Do not publish this directory; it contains credentials and research state.

A raw file copy while writers remain active is not a supported backup procedure. This release does not supply an online backup service or tested cross-host migration tool. Use an encrypted/private backup destination appropriate to the host and retain the original until restoration is verified.

Restore while all writers are stopped into a separate private directory, with the matching source revision and frozen dependencies. Check schema compatibility before any upgrade. Start against the restored directory and verify hypothesis/dataset/run records and representative artifact hashes through the application. Sessions will need fresh login. If a snapshot contains running attempts, first establish that the old workers are stopped, then mark those attempts interrupted explicitly. Never run the original and restored writers concurrently against the same directory.

The actual recovery/restore tests and their limits are recorded in [Phase III verification](verification.md). These instructions do not claim recovery from disk loss without a usable backup, corruption outside the checks, or a malicious host. Append-only application/database rules preserve history within their trust boundary; they are not external tamper-proof audit storage.
