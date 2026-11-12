# Integration checkpoint

- Published checkpoint: `kraken-historical-b` (resolve tag); A=`31c1b59`/`kraken-historical-a`; previous synthetic integration=`7206eb1`.
- Complete A/B: compact immutable Git evidence, published-prefix guard, Kraken historical adapter and data-only replay. Core v2 unchanged. Existing ZIPs verified;64trades+64bars normalized/replayed privately. No financial route/engine involved.
- Executed:10 maintenance tests,3 deletion regressions, reconstructed intentional failure;41 adapter/replay tests;190 backend tests; mypy/Ruff pass. Actual close canary0before/1atclose, restart/idempotence/duplicate checks pass. Evidence and lint negatives preserved.
- Limits: two fixed prefixes, optimistic historical availability with received_ns absent; no quarter-wide completeness or financial admission. Rights-reference JSON was bound after original QA; receipt documents this limitation. Old evidence and4630 stable environment files unchanged.
- Resources: 132.427/900 monitored seconds, 186.9MiB sampledRSS, 6.85MiB sampledadditional footprint. Engineering approximately60min at release audit; earlier portion estimated. Fresh2h/4CPU/8GiB/512MiB budget; no downloads of datasets/software or costs.
- Next exact action: review `docs/integration/kraken/REPORT.md` and disabled `capture-spec.json`. Future capture needs separate source/rights/resource authorization, v2 instrument preflight and finite approved pilot. Do not start capture or repeat M/R/E/E1.
- E3/E4 economics pending;26specifications,USD,C1/C3,C2,C4/C5,T/D/U/V/F,holdout and Phase V restrictions unchanged. A/B scope complete; this budget is not permission for a new campaign.
