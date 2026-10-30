"""Summarize already executed M checks without rerunning a test."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

root = Path('/workspace/technical-admission/M')
repo = Path('/workspace/bot_trader')
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
cases = []
for path in sorted((root / 'results').glob('*-initial.json')):
    cases.extend(json.loads(path.read_text()).get('cases', []))
assert len(cases) == 20
suites = {}
for role in ('control', 'candidate'):
    suite = ET.parse(root / 'results' / f'backend-{role}.xml').getroot().find('testsuite')
    suites[role] = {key: suite.attrib[key] for key in ('tests', 'failures', 'errors', 'skipped', 'time')}
    assert suites[role]['tests'] == '110'
    assert all(suites[role][k] == '0' for k in ('failures', 'errors', 'skipped'))
immutable_packs = []
for role in ('control', 'candidate'):
    writer = json.loads((root / 'fixtures' / f'writer-{role}.json').read_text())
    for item in writer['files']:
        actual = sha(Path(item['path']))
        assert actual == item['sha256']
        immutable_packs.append({'relative_path': str(Path(item['path']).relative_to(root)), 'sha256': actual})
source_files = []
for subdir in ('src', 'tests', 'migrations'):
    for path in sorted((root / 'control' / subdir).rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative = path.relative_to(root / 'control')
        hashes = {role: sha(root / role / relative) for role in ('control', 'candidate')}
        assert len(set(hashes.values())) == 1
        source_files.append({'path': str(relative), 'sha256': hashes['control']})
historical = repo / '.state' / 'artifacts'
eligible = sorted(path.name for path in historical.iterdir() if path.is_file())
assert not eligible, 'Unexpected old objects require provenance examination, not automatic admission'
inventory = {'inspected_directory': '.state/artifacts', 'inspected_utc_date': '2026-10-29',
             'object_names': eligible, 'optional_reads_executed': 0,
             'limitation': 'Directory is empty; generated control-writer fixtures verify old format, not historical application objects. No admin token or database content read.'}
with (root / 'results' / 'old-artifact-inventory.json').open('x') as f:
    json.dump(inventory, f, indent=2); f.write('\n')
result = {'package': 'M', 'status': 'passed_scoped_checks', 'synthetic': True,
          'financial_experiments': 0, 'custom_initial_attempts': len(cases),
          'custom_passed': sum(item['status'] == 'passed' for item in cases),
          'custom_failed': sum(item['status'] != 'passed' for item in cases),
          'correction_cycles_used': 0, 'backend_suite_invocations': 2,
          'backend_suites': suites, 'optional_old_artifact_reads': 0,
          'source_export_commit': 'fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f',
          'harness_sha256': sha(repo / 'tools/technical_admission/dependency_probe.py'),
          'source_exports_equal_files': len(source_files), 'source_files': source_files,
          'immutable_generated_objects_after_tests': immutable_packs,
          'known_negative_control': 'DuckDB1.5.6 zoned-ns projection loses submicrosecond precision in both versions. Canonical integer ticks preserve it.',
          'limitation': 'No historical application objects available; no production migration, arbitrary future schemas, market inputs or financial compatibility certified.'}
with (root / 'results' / 'summary.json').open('x') as f:
    json.dump(result, f, indent=2); f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('source_files','immutable_generated_objects_after_tests')}))
