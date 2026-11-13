# Integration checkpoint

- Last published: `dc859e8` / `kraken-historical-b`; A=`31c1b59`. Historical adapter and previous tests remain complete.
- Current authority: simulated Kraken WSv2 BTC/EUR trade+ticker/BBO → archive → normalization → data-only replay. No real connections, financial strategies, credentials, new dependencies or engine research.
- In progress: reusable durable raw capture journal, exact WS normalizer/protocol, bounded injected transport orchestration and separate capture QA profile. Contracts v2 remain unchanged.
- Not yet executed: new tests or capture. Next: finish composition, run synthetic faults/restart/causality tests under `docs/integration/kraken-ws/budget.json`, publish one recoverable commit and synchronized EN/ES report/procedure.
- Self-imposed fresh technical ceilings:900 guarded seconds,4CPU,8GiB,512MiB extra; do not reuse completed historical-package resources/permissions. Engineering checkpoint outside Git in campaign scratch.
- Future5–10min live pilot requires separate rights/source/resources approval, transport implementation/admission and BTC/EUR v2 preflight. Stable environment has no admitted WS client. E3/E4,26specifications,holdout and Phase V/paper/live remain unchanged.
