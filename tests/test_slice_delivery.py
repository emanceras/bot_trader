"""Final entry-point and new future-information integration canary."""

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest
from test_slice_native import ADMIN, FIXTURES, PYTHON
from test_slice_native import platform as platform

from bot_trader.core.events import canonical_bytes
from bot_trader.market_data.archive import SourceSpec
from bot_trader.simulation.bridge import NativeSliceProcess
from bot_trader.simulation.slice import SliceConfiguration

pytestmark = pytest.mark.skipif(
    not PYTHON.is_file() or "SLICE_EVIDENCE_DIR" not in os.environ,
    reason="Optional isolated native delivery checks require a guarded artifact directory.",
)


def test_future_source_values_preserve_earlier_native_decision_and_fill(platform, tmp_path):
    baseline = Path("docs/integration/evidence/h3/h3-native-final/native/full-a")
    rows = [json.loads(row) for row in (FIXTURES / "roundtrip.jsonl").read_bytes().splitlines()]
    for row in rows:
        if row["event_id"] == "trade-3-2":
            row["data"]["price"] = "108"
        if row["event_id"] == "bar-3-closed":
            row["data"].update(high="108", close="108")
    raw = b"\n".join(canonical_bytes(row) for row in rows) + b"\n"
    path = tmp_path / "future.jsonl"
    path.write_bytes(raw)
    spec = SourceSpec.model_validate_json((FIXTURES / "roundtrip.source.json").read_bytes())
    spec = SourceSpec.model_validate(
        spec.model_dump()
        | {
            "locator": "internal:future-canary",
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
        }
    )
    archive = platform.slice.import_file(path, spec, ADMIN)
    output = Path(os.environ["SLICE_EVIDENCE_DIR"]) / "future-canary"
    report = platform.slice.run(
        archive.archive_hash,
        SliceConfiguration(),
        ADMIN,
        execution=NativeSliceProcess(PYTHON),
        directory=output,
    )
    assert report["status"] == "reconciled"
    replay = json.loads(platform.slice.store.get(report["replay_hash"], "json"))
    old_replay = json.loads((baseline / "replay.json").read_text())
    native = json.loads((output / "result.json").read_text())
    old_native = json.loads((baseline / "result.json").read_text())
    assert replay["signals"][0] == old_replay["signals"][0]
    assert native["fills"][0] == old_native["fills"][0]
    assert replay["signals"][1] != old_replay["signals"][1]
    assert replay["records"][0]["event_hash"] != old_replay["records"][0]["event_hash"]
    (output / "platform-report.json").write_bytes(canonical_bytes(report))
    (output / "replay.json").write_bytes(canonical_bytes(replay))


def test_real_platform_cli_persists_auditable_synthetic_result(tmp_path):
    output = Path(os.environ["SLICE_EVIDENCE_DIR"]) / "cli"
    output.mkdir(parents=True)
    state = tmp_path / "platform-state"
    command = [
        str(Path.cwd() / ".venv/bin/python"),
        "-m",
        "bot_trader.cli",
        "--state-dir",
        str(state),
    ]
    init = subprocess.run([*command, "init"], capture_output=True, text=True, timeout=30)
    (output / "init.log").write_text(init.stdout + init.stderr)
    assert init.returncode == 0
    run = subprocess.run(
        [
            *command,
            "slice",
            "--source",
            str(FIXTURES / "roundtrip.jsonl"),
            "--manifest",
            str(FIXTURES / "roundtrip.source.json"),
            "--native-python",
            str(PYTHON),
            "--run-dir",
            str(output / "engine"),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    (output / "cli.log").write_text(run.stdout + run.stderr)
    assert run.returncode == 0, run.stderr
    report = json.loads(run.stdout)
    assert report["status"] == "reconciled" and report["financial_validation"] is False
    assert report["signal_count"] == 2 and report["fill_count"] == 2
    import sqlite3

    with sqlite3.connect(state / "metadata.sqlite3") as db:
        assert (
            db.execute("select count(*) from documents where kind='technical-slice'").fetchone()[0]
            == 1
        )
        assert (
            db.execute("select count(*) from audit where action='technical-slice.run'").fetchone()[
                0
            ]
            == 1
        )
