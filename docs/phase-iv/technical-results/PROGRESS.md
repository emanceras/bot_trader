# M/R/E execution checkpoint

Updated: 2026-11-01. Canonical English; resumen español below. Scope commit: `fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f`. Authority: [express execution approval](../APPROVAL-M-R-E.es.md), D-046.

## Actual state and resumption

| Package | State | Evidence / remaining work |
|---|---|---|
| M | Executed, scoped checks passed | [20 custom checks, 110 backend tests per environment](M/README.md); no case corrections/reruns; no eligible pre-existing artifact reads |
| R | Executed, scoped checks passed | [160 initial runs and review](R/REVIEW.md); no case reruns; actual provider/feed and engine recovery remain outside scope |
| E — Nautilus | Setup blocked; no engine cases run | Exact Python 3.13.18 absent from uv 0.12.23's distributions; actual pinned install failed. No runtime/version substitution |
| E — LEAN | Three component cases executed; no full case admission | [E evidence](E/README.md): E1 partial, E2 required sale absent, E3-L1 fills 4 with visible 1. Remaining10 slots unexecuted; no complete engine comparison or winner |

Scratch is `/workspace/technical-admission/{M,R,E}`. Never repeat the verified Arrow 26 wheel, SDK, source acquisition, M suites or R cases after interruption. Small evidence is published here; binaries, caches, private test state and raw generated Parquet stay outside Git. `tools/technical_admission` contains the actual standalone harnesses and bounded installation helpers, not production financial adapters.

One shared execution lock serializes package jobs. The approved package and aggregate ceilings, versions, independent oracles and one affected correction-cycle policy still apply. Preserve failures before any justified retry; setup diagnosis does not retroactively turn a failed invocation into a passed case. No financial datasets, Phase V, paper/live, production migration, contracts or paid services.

M results are in `M/results/summary.json`, all execution commands in `M/runs.jsonl`, and the copied control/candidate locks under `M/locks`. R's case ledger is `R/initial/runs.jsonl`; `R/guard-runs.jsonl` additionally retains failed bootstrap/argument invocations. The older proposal checkpoints retain their original dates and are not current pending-permission instructions.

## Final preservation and resource evidence

[Preservation audit](preservation.json) compared 73recorded software/configuration files and 4,630regular production-environment files with the [original baseline](preservation-baseline.json): no mismatches, additions or protected scientific/source changes. It excludes symlink targets and private runtime state; no credential or market archive was read.

[Resources](resources.json): M 43.499912s, R 0.654550s and E 154.310455s measured active wall, total 198.464918s; 358.785783guarded CPU seconds. Maximum sampled package RSS 1,674,530,816 bytes; current aggregate scratch 2,490,763,713 bytes; transfer allowance charged 331,638,177bytes. These remain below per-package and aggregate ceilings. Git/NuGet durations are nested within guarded calls and are counted once; TLS transfer counts are conservative allowances, not exact application payload totals. No resource stop triggered. Preparation/review effort and interruption duration are unmeasured, not included as machine execution or inferred financial research cost.

No new engine runs or financial work remain hidden behind the report. E remains partial: source configuration corrected once, zero case reruns,3 component cases executed and23 case slots unexecuted. Shell exit0 is observation collection success, not mandatory admission. The report recommends no engine winner and no production migration. Reopening unavailable runtime versions or implementing new fill models requires the appropriate separate scope; do not repeat M/R or relabel missing E coverage as native failure.

## Scientific and operational status

E1/E2, 26 base specifications, C1/C3 priorities, C2 comparison, C4/C5 reserves, T/D/U/V/F and the final access restrictions remain unchanged. E3/E4 are pending; seven financial counters remain zero. Phase IV is not unconditionally closed. UX/glossary/guide improvements remain future work.

M passing does not enable Nautilus under Python 3.12, nor does it require an immediate storage upgrade. R passing is an implementation-level causal check, not provider conformance. E setup is not native execution/accounting/recovery evidence. No engine has been selected from these installation observations.

## Resumen español

M y R ya ejecutados y revisados; no repetirlos. M: 20 casos específicos y 110 pruebas backend por entorno; R: 160 comprobaciones. Se conservan límites, control adverso de precisión DuckDB, ausencia de artefactos antiguos elegibles y fallos de preparación.

Nautilus queda bloqueado por la distribución exacta de Python, sin sustituir versiones. LEAN compiló y ejecutó tres casos: E1 parcial, E2 venta requerida ausente, E3-L1 ejecución de 4 con 1 visible. Diez casos LEAN y trece Nautilus sin ejecutar; ningún caso completo admitido. Se conservan fallos de instalación, advertencias y límites del harness. No declarar E completado sin ejecutar sus casos. Producción y ciencia intactas; E3/E4 y V pendientes. Consultar [informe EN](../../en/phase-iv/technical-results.md) / [ES](../../es/phase-iv/technical-results.md) antes de continuar.

[Publication verification](verification.json) checks syntax, structured receipts, local links, hashes and status counts without new package runs. Copied upstream logs/licence preserve original whitespace and hashes; the authored-file whitespace check excludes those receipts.
