# M — executed dependency evidence

Execution date: 2026-10-29. Source export: `fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f`. This is synthetic technical evidence, not a financial experiment or permission to migrate production.

`results/summary.json` records **20 initial custom passes** and **110 backend tests passing in each environment**. No custom case, suite or correction cycle was repeated. The two `consistency-*.log` files record successful installed dependency checks. `lock-comparison.json` identifies Arrow 23.0.1 → 26.0.0 as the sole package-version delta; DuckDB remains 1.5.6, Python 3.12.14 and uv 0.12.23. The same Starlette/httpx deprecation warning occurs in both backend suites; it is retained without an unrelated dependency change.

`setup-manifest.json` is an immutable earlier preparation receipt, so its state correctly says installation had not happened **then**. Later install logs, exact candidate/control locks and `runs.jsonl` prove the subsequent resolution/install/check sequence. Source and test exports are equal across 41 files recorded in the summary. The parent execution report separately audits unchanged production files.

The generated packs contain 120 v1 rows (seed 42), 32 boundary rows and 32 precision events. Frozen values and schemas preceded either reader run. All 12 writer/reader combinations pass exact Parquet/IPC values/metadata and DuckDB projections. Both environments reject corrupt digests, reserved data and real-data labels; both actually kill an artifact writer after fsync and before publication, preserving the original manifest while the incomplete object remains unadmitted. This is artifact publication recovery, not trading-engine recovery.

The negative control confirms the already known **loss of submicrosecond precision in DuckDB's zoned timestamp projection** for both Arrow versions. Explicit integer epoch-nanosecond columns remain exact. Display timestamps are not admitted as canonical sort/join keys. Optional historical-object reads were not possible: `.state/artifacts` was empty. Generated old-format fixtures must not be described as historical application objects.

## Reproduction boundary

Do not run these commands against production or overwrite existing evidence. `runs.jsonl` preserves every exact executed command and finite execution limits; `downloads.jsonl` binds the acquired wheel URL, body size and SHA256. `prepare_environments.py` is the actual setup script, including its refusal to replace environments. It assumes the original locked software cache and the exact wheel already verified in a fresh disposable workspace. The copied lock files are receipts, not a change to the production lock. Where the original cache is unavailable, separately acquire only the same verified locked artifacts within the approved transfer envelope.

All package commands used [the shared guard](../../../../tools/technical_admission/runtime_guard.py), with option arguments before the `M` positional argument. Their sequence is:

1. Export the pinned source twice, copy the existing cache, install the frozen control, resolve the candidate once with all other versions constrained, compare locks, then install the frozen candidate.
2. Run `uv pip check` once for each isolated interpreter.
3. Invoke [dependency_probe.py](../../../../tools/technical_admission/dependency_probe.py) with `freeze` under the control interpreter; then `write` for each role. Supply `--source`, `--workspace`, `--result` and the exact `--role` shown in the run ledger.
4. Run `read`, `guards` and `crash` once per role; keep every output. Each reader covers both writers, so 12 cross-reader cases are represented by two invocations.
5. Run each unchanged exported backend suite once, with a unique disposable `--basetemp` and JUnit output. The XML records preserve per-test outcomes.
6. Run `summarize_results.py` over existing results only; it does not rerun cases. It checks original writer hashes remain unchanged and records the empty historical-artifact inventory.

Raw Parquet/IPC packs, environments, wheel and private pytest state stay outside Git. The frozen JSON and source reproduce the synthetic objects. The evidence directory contains no production credential or financial dataset.

## Measured resources and interpretation

The 18 guarded invocations consumed 41.612727927 seconds wall and 35.152106 CPU seconds; the exact wheel transfer consumed 1.887184506 seconds and 53,931,932 body bytes. Total recorded active time is 43.499912433 seconds. Maximum sampled process-group RSS was 262,672,384 bytes; maximum recorded scratch after a command was 1,244,985,455 bytes. Interruption time between sessions is not compute time, and these measurements do not predict future financial research cost.

RSS is sampled, not a kernel-enforced peak measurement; scratch is periodically watched and recorded after commands, not a proven continuous high-water mark. Offline IPv4/IPv6 socket denial was enabled. Landlock was unavailable on this host: disposable exports/environments plus production integrity audits provide the filesystem separation, not a demonstrated hostile-code sandbox. Retain those limitations when interpreting the pass.

**Recommendation:** Arrow 26.0.0 is compatible with the tested application/fixture scope. A separately authorized production migration is technically supportable with the same version constraints and rollback discipline. This result neither requires that migration nor enables Nautilus v2 under Python 3.12. It certifies no arbitrary future schema, provider, engine, platform or financial behavior.
