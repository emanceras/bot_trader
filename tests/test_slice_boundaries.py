"""Adversarial boundaries reuse actual receipts; no old engine case is rerun."""

import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import content_hash
from bot_trader.core.security import Policy
from bot_trader.market_data.archive import LocalArchive, SourceSpec
from bot_trader.market_data.normalization import FixtureJSONLNormalizer
from bot_trader.market_data.replay import MarketReplay
from bot_trader.market_data.storage import MemoryArtifactStore
from bot_trader.simulation.bridge import NativeSliceProcess, verify_journal
from bot_trader.simulation.slice import SliceConfiguration, SliceService, execution_request

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/integration/roundtrip.jsonl"
SOURCE = FIXTURE.with_name("roundtrip.source.json")
RECEIPT = ROOT / "docs/integration/evidence/h3/h3-native-final/native/full-a"
ADMIN = Principal(id="test", role="admin")


class ForbiddenEngine:
    def execute(self, request, directory):
        pytest.fail("Forbidden input reached the execution port")


def source():
    return SourceSpec.model_validate_json(SOURCE.read_bytes())


def test_permissions_precede_source_read_and_engine(tmp_path):
    service = SliceService(MemoryArtifactStore(), Policy())
    for role in ("agent", "viewer"):
        with pytest.raises(AccessDenied):
            service.import_file(tmp_path / "absent", source(), Principal(id="x", role=role))
    for mode in ("final", "validation"):
        reserved = SourceSpec.model_validate(source().model_dump() | {"partition": mode})
        with pytest.raises(AccessDenied):
            service.import_file(tmp_path / "absent", reserved, ADMIN)
    with pytest.raises(ValueError):
        service.run(
            "a" * 64,
            SliceConfiguration.model_construct(mode="live"),
            ADMIN,
            execution=ForbiddenEngine(),
            directory=tmp_path / "never",
        )


def test_exposed_archive_denied_before_payload_even_if_imported_elsewhere(tmp_path):
    class ReadingStore(MemoryArtifactStore):
        raw_reads = 0

        def get(self, digest, suffix):
            if suffix == "bin":
                self.raw_reads += 1
            return super().get(digest, suffix)

    store = ReadingStore()
    exposed = SourceSpec.model_validate(
        source().model_dump() | {"data_class": "exposed_structural_only"}
    )
    archive = LocalArchive(store).import_step(FIXTURE, exposed, max_chunks=1000)
    with pytest.raises(AccessDenied):
        SliceService(store, Policy()).run(
            archive.archive_hash,
            SliceConfiguration(),
            ADMIN,
            execution=ForbiddenEngine(),
            directory=tmp_path / "never",
        )
    assert store.raw_reads == 0


def test_integrated_gap_stops_before_native_execution(tmp_path):
    rows = FIXTURE.read_bytes().splitlines()
    raw = b"\n".join(rows[:2] + rows[3:]) + b"\n"
    path = tmp_path / "gap.jsonl"
    path.write_bytes(raw)
    import hashlib

    spec = SourceSpec.model_validate(
        source().model_dump()
        | {"raw_sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)}
    )
    service = SliceService(MemoryArtifactStore(), Policy())
    acquired = service.import_file(path, spec, ADMIN)
    with pytest.raises(ValueError, match="Sequence gap"):
        service.run(
            acquired.archive_hash,
            SliceConfiguration(),
            ADMIN,
            execution=ForbiddenEngine(),
            directory=tmp_path / "never",
        )


def test_no_quote_is_invented_and_ambiguous_backlog_is_rejected():
    spec = source()
    batch = FixtureJSONLNormalizer().normalize(
        FIXTURE.read_bytes(), spec, content_hash(spec.model_dump(mode="json"))
    )
    replay = MarketReplay(SliceConfiguration().replay).run(batch.events, synthetic=True)
    with pytest.raises(ValueError, match="No explicit"):
        execution_request(replay.model_copy(update={"quotes": ()}), SliceConfiguration())
    with pytest.raises(ValueError, match="Multiple signals"):
        execution_request(
            replay.model_copy(update={"quotes": replay.quotes[-1:]}), SliceConfiguration()
        )


def test_native_summary_is_bound_to_actual_journal_and_truncation_fails():
    native = json.loads((RECEIPT / "result.json").read_bytes())
    journal = (RECEIPT / "result.events.jsonl").read_bytes()
    verify_journal(journal, native)
    for field in ("cash", "orders", "fills"):
        changed = deepcopy(native)
        changed[field] = {} if field == "cash" else []
        with pytest.raises(ValueError, match="journal|summary"):
            verify_journal(journal, changed)
    with pytest.raises(ValueError, match="incomplete"):
        verify_journal(b"\n".join(journal.splitlines()[:-1]) + b"\n", native)
    duplicate = journal.splitlines()
    duplicate.insert(1, duplicate[0])
    with pytest.raises(ValueError, match="integrity|sequence"):
        verify_journal(b"\n".join(duplicate) + b"\n", native)


def test_native_timeout_keeps_unknown_state_and_does_not_retry(tmp_path, monkeypatch):
    request = json.loads((RECEIPT / "request.json").read_bytes())
    calls = []

    def timeout(*args, **kwargs):
        calls.append(args)
        raise subprocess.TimeoutExpired(args[0], 1)

    monkeypatch.setattr(subprocess, "run", timeout)
    python = Path(__import__("sys").executable)
    adapter = NativeSliceProcess(python, timeout_seconds=1)
    directory = tmp_path / "interrupted"
    with pytest.raises(subprocess.TimeoutExpired):
        adapter.execute(request, directory)
    receipt = json.loads((directory / "transport.json").read_text())
    assert receipt["status"] == "failed_or_unknown" and receipt["automatic_retry"] is False
    assert len(calls) == 1 and not (directory / "result.json").exists()
    with pytest.raises(FileExistsError):
        adapter.execute(request, directory)
    assert len(calls) == 1
