"""Execute one frozen synthetic LEAN component case and retain adverse output.

This supervisor does not create fills, change fees or implement recovery.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from engine_fixtures import check_accounting, digest

ROOT = Path('/workspace/technical-admission/E')
SOURCE = Path(__file__).parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_fixture():
    manifest = json.loads((ROOT/'fixtures/fixture-manifest.json').read_text())
    assert sha(ROOT/'fixtures/engine-cases.json') == manifest['bundle_sha256']
    assert sha(SOURCE/'engine_fixtures.py') == manifest['source_sha256']
    assert sha(ROOT/'fixtures/temporal_journals.json') == manifest['temporal_sha256']
    return manifest


def freeze():
    fixture = verify_fixture()
    paths = [SOURCE/name for name in ('lean_probe.cs', 'lean_probe.csproj', 'lean_case.py')]
    paths += sorted((ROOT/'harness-bin').glob('*.dll'))
    paths += [ROOT/'harness/packages.lock.json']
    result = {
        'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'state': 'frozen_before_native_cases', 'fixture': fixture,
        'sha256': {str(path): sha(path) for path in paths},
        'cases_to_execute': ['E1-causality', 'E2-accounting', 'E3-L1'],
        'scope_limits': [
            'Native component invocation, not a complete brokerage lifecycle.',
            'E1 lacks R-canary/prefix/unsupported-time execution and is partial regardless of its small comparison.',
            'Admission, reservation, availability and observation IDs are harness supplied.',
            'Dependent L2, duplicate/recovery and resource cases cannot pass without their actual implementation and execution.',
        ],
    }
    with (ROOT/'harness-manifest.json').open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({'status': result['state'], 'hashed_files': len(paths)}))


def run(case_id):
    verify_fixture()
    manifest = json.loads((ROOT/'harness-manifest.json').read_text())
    for path, expected in manifest['sha256'].items():
        assert sha(Path(path)) == expected, f'changed frozen source/binary: {path}'
    fixture = next(x for x in json.loads((ROOT/'fixtures/engine-cases.json').read_text())['functional'] if x['case_id'] == case_id)
    output = ROOT/'cases'/case_id
    output.mkdir(parents=True, exist_ok=False)
    command = [str(ROOT/'dotnet/dotnet'), str(ROOT/'harness-bin/lean_probe.dll'), str(ROOT/'fixtures/engine-cases.json'), case_id]
    env = {**os.environ, 'XDG_RUNTIME_DIR': str(ROOT/'runtime'), 'XDG_DATA_HOME': str(ROOT/'xdg-data'), 'DOTNET_GENERATE_ASPNET_CERTIFICATE': 'false'}
    started = time.monotonic()
    process = subprocess.run(command, env=env, cwd=output, capture_output=True, timeout=580)
    (output/'stdout.log').write_bytes(process.stdout)
    (output/'stderr.log').write_bytes(process.stderr)
    parsed = []
    for line in process.stdout.decode(errors='replace').splitlines():
        try:
            value = json.loads(line)
            if isinstance(value, dict) and value.get('engine') == 'LEAN': parsed.append(value)
        except json.JSONDecodeError:
            pass
    observed = parsed[-1] if parsed else None
    problems = []
    if process.returncode != 0 or not observed or observed.get('execution_status') != 'component_observations_emitted':
        status = 'error_before_comparison'
        problems.append('native_worker_did_not_complete')
    else:
        problems = check_accounting(fixture, observed)
        if case_id == 'E1-causality':
            expected = fixture['expected_decisions']
            actual = observed['decisions']
            def normalized(rows):
                return [{**row, **({'close': str(Decimal(row['close']).normalize())} if 'close' in row else {})} for row in rows]
            if normalized(actual) != normalized(expected): problems.append('small_fixture_decision_mismatch')
            status = 'partial_harness_guard_evidence' if not problems else 'failed_component_comparison'
        else:
            status = 'failed_mandatory_comparison' if problems else 'partial_component_evidence'
    result = {
        'engine': 'LEAN', 'case_id': case_id, 'synthetic_only': True,
        'command': command, 'native_process_exit_code': process.returncode,
        'wall_seconds': time.monotonic()-started,
        'status': status, 'full_case_admitted': False, 'problems': problems,
        'stdout_sha256': sha(output/'stdout.log'), 'stderr_sha256': sha(output/'stderr.log'),
        'fixture_sha256': manifest['fixture']['bundle_sha256'],
        'observation_sha256': digest(observed) if observed else None,
        'observed': observed,
        'limits': manifest['scope_limits'],
    }
    with (output/'result.json').open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('observed', 'limits')}))
    return 0 if process.returncode == 0 else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', action='store_true')
    parser.add_argument('--case', choices=['E1-causality', 'E2-accounting', 'E3-L1'])
    args = parser.parse_args()
    if args.freeze:
        freeze(); return 0
    if not args.case: parser.error('--freeze or --case required')
    return run(args.case)


if __name__ == '__main__':
    sys.exit(main())
