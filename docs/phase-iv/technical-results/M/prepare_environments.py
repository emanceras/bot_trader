"""Prepare only the authorized isolated M control and one Arrow candidate."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tomllib

ROOT = Path('/workspace/technical-admission/M')
REPO = Path('/workspace/bot_trader')
BASE = 'fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    control = ROOT/'control'
    candidate = ROOT/'candidate'
    cache = ROOT/'uv-cache'
    if control.exists() or candidate.exists() or cache.exists():
        raise RuntimeError('Refusing to replace an existing setup')
    original_lock = tomllib.loads((REPO/'uv.lock').read_text())
    wheel = ROOT/'downloads/pyarrow-26.0.0-cp312-cp312-manylinux_2_28_x86_64.whl'
    assert sha(wheel) == '6a628922ba20705fa964ca73e4ef959c2fb2f14b9bbec5589a6a1e68e6257c85'
    archive = ROOT/'source-fa435a4.tar'
    with archive.open('xb') as f:
        subprocess.run(['git','archive','--format=tar',BASE],cwd=REPO,stdout=f,check=True)
    for path in (control,candidate):
        path.mkdir()
        with tarfile.open(archive) as tar:
            tar.extractall(path,filter='data')
    shutil.copytree('/workspace/.cache/uv',cache,symlinks=True)
    external_cache_links = []
    for path in cache.rglob('*'):
        if path.is_symlink() and not path.resolve().is_relative_to(cache):
            external_cache_links.append(str(path))
    if external_cache_links:
        raise RuntimeError(f'Cache contains external links: {external_cache_links}')
    project = candidate/'pyproject.toml'
    text = project.read_text()
    assert text.count('pyarrow>=19,<24') == 1
    text = text.replace('pyarrow>=19,<24','pyarrow==26.0.0')
    constraints = sorted(f"{p['name']}=={p['version']}" for p in original_lock['package']
                         if p['name'] not in ('bot-trader','pyarrow'))
    text += '\n[tool.uv]\nconstraint-dependencies = '+json.dumps(constraints)+'\n'
    text += '\n[tool.uv.sources]\npyarrow = { path = '+json.dumps(str(wheel))+' }\n'
    project.write_text(text)
    manifest = {'base_commit':BASE,'archive_sha256':sha(archive),
                'control_lock_sha256':sha(control/'uv.lock'),
                'control_project_sha256':sha(control/'pyproject.toml'),
                'candidate_project_sha256':sha(project),
                'all_other_versions':constraints,
                'candidate_wheel_sha256':sha(wheel),
                'cache_external_symlinks':external_cache_links,
                'production_source_mutated':False,'network_used':False,
                'setup_state':'sources_and_cache_prepared_no_resolver_or_install_yet'}
    (ROOT/'setup-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':
    main()
