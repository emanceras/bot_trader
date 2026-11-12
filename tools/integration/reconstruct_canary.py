"""Reconstruct only the intentional negative fixture from Git and repeat its command."""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parents[2]
    receipt_dir = Path(sys.argv[1]).resolve()
    receipt = json.loads((receipt_dir / "receipt.json").read_text())
    source = json.loads((receipt_dir / "source-manifest.json").read_text())
    name = "tests/fixtures/integration/maintenance-canary.json"
    assert not (repo / name).exists(), "Reconstruction must not read a remaining working copy."
    saved = subprocess.check_output(
        ["git", "show", source["snapshot_commit"] + ":" + name], cwd=repo,
    )
    assert hashlib.sha256(saved).hexdigest() == source["files"][name]
    assert receipt["source_commit"] == source["snapshot_commit"]
    command = receipt["command"]
    assert command[0] == ".venv/bin/python" and command[1] == "-c"
    assert command[2] == (
        'import json; from pathlib import Path; x=json.loads(Path("tests/fixtures/integration/'
        'maintenance-canary.json").read_text()); assert x["expected"] == x["actual"], '
        '"deliberate evidence canary"'
    ), "Do not execute an arbitrary receipt command."
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / name
        path.parent.mkdir(parents=True)
        path.write_bytes(saved)
        result = subprocess.run(
            [str(repo / command[0]), *command[1:]], cwd=temporary,
            capture_output=True, timeout=10,
        )
    assert result.returncode == receipt["exit_code"] == 1
    assert result.stderr.rstrip().endswith(b"AssertionError: deliberate evidence canary")
    print(json.dumps({"reconstructed": True, "same_failure": True,
                      "snapshot_commit": source["snapshot_commit"], "files_restored": 1}))


if __name__ == "__main__":
    main()
