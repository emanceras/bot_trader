"""Synthetic raw receipts: durable prefixes, bounded storage and explicit recovery."""

import hashlib
import json
from types import SimpleNamespace

import pytest

from bot_trader.core.errors import PlatformError
from bot_trader.market_data.capture import CaptureJournal, CaptureLimitError, CaptureLimits
from bot_trader.market_data.storage import LocalArtifactStore, MemoryArtifactStore


def journal(tmp_path, *, store=None, limits=None, **changes):
    parameters = {"capture_id": "capture-1", "config_hash": "a" * 64, **changes}
    return CaptureJournal(
        store or MemoryArtifactStore(), tmp_path / "journal", limits=limits, **parameters
    )


def frame(capture, raw=b'{"synthetic":true}', *, utc=123456789, mono=10, session="session-1"):
    return capture.append_frame(raw, session_id=session, received_ns=utc, monotonic_ns=mono)


def test_duplicate_deliveries_remain_independent_and_restart_is_exact(tmp_path):
    store = LocalArtifactStore(tmp_path / "blobs")
    capture = journal(tmp_path, store=store)
    first = frame(capture)
    second = frame(capture, utc=123456790, mono=11)
    assert first.raw_sha256 == second.raw_sha256
    assert first.digest != second.digest and second.previous_hash == first.digest
    assert first.received_ns == 123456789
    before = capture.checkpoint
    reopened = journal(tmp_path, store=store)
    assert reopened.checkpoint == before
    assert reopened.records() == (first, second)
    assert reopened.read_frame(first) == b'{"synthetic":true}'
    assert len(list((tmp_path / "blobs").glob("*.bin"))) == 1
    assert len(list((tmp_path / "journal/records").glob("*.json"))) == 2
    assert before.total_charged_bytes == 2 * (8192 + first.raw_size)


def test_control_details_cannot_mutate_committed_envelopes(tmp_path):
    capture = journal(tmp_path)
    details = {"nested": {"cause": "synthetic"}}
    record = capture.append_control(
        "gap", session_id="s", received_ns=1, monotonic_ns=1, details=details
    )
    details["nested"]["cause"] = "changed"
    record.details["nested"]["cause"] = "also-changed"
    assert capture.records()[0].details == {"nested": {"cause": "synthetic"}}


@pytest.mark.parametrize("corruption", ["raw", "envelope", "index", "missing"])
def test_corruption_never_silently_repaired(tmp_path, corruption):
    store = LocalArtifactStore(tmp_path / "blobs")
    capture = journal(tmp_path, store=store)
    first = frame(capture)
    frame(capture, utc=123456790, mono=11)
    if corruption == "raw":
        (store.root / f"{first.raw_sha256}.bin").write_bytes(b"corrupt")
    elif corruption == "envelope":
        (store.root / f"{first.digest}.json").write_bytes(b"{}")
    elif corruption == "index":
        (capture.directory / "records/000000000001.json").write_text("{}")
    else:
        (capture.directory / "records/000000000001.json").unlink()
    with pytest.raises((ValueError, PlatformError)):
        journal(tmp_path, store=store)


def test_failed_blob_write_preserves_prefix_and_requires_explicit_recovery(tmp_path, monkeypatch):
    store = MemoryArtifactStore()
    capture = journal(tmp_path, store=store)
    first = frame(capture)
    original = store.put

    def fail(data, suffix):
        if suffix == "bin":
            raise OSError("injected disk failure")
        return original(data, suffix)

    monkeypatch.setattr(store, "put", fail)
    with pytest.raises(OSError, match="injected"):
        frame(capture, b"uncommitted", utc=123456790, mono=11)
    monkeypatch.setattr(store, "put", original)
    reopened = journal(tmp_path, store=store)
    assert reopened.records() == (first,)
    assert reopened.checkpoint.pending_intent
    pending_bytes = (reopened.directory / "pending.json").read_bytes()
    with pytest.raises(ValueError, match="Pending"):
        frame(reopened, utc=123456791, mono=12)
    with pytest.raises(ValueError, match="confirmation"):
        reopened.recover(
            writer_stopped=False, session_id="recovery", received_ns=123456791, monotonic_ns=0
        )
    interruption = reopened.recover(
        writer_stopped=True, session_id="recovery", received_ns=123456791, monotonic_ns=0
    )
    assert interruption.kind == "interruption"
    assert interruption.details["coverage"] == "unknown"
    assert interruption.details["intent_already_committed"] is False
    preserved = list(reopened.directory.glob("interrupted-*.json"))
    assert len(preserved) == 1 and preserved[0].read_bytes() == pending_bytes
    assert reopened.frames() == (first,) and not reopened.checkpoint.pending_intent
    assert reopened.checkpoint.total_charged_bytes == 3 * 8192 + first.raw_size + len(
        b"uncommitted"
    )
    frame(reopened, utc=123456792, mono=1, session="restarted")
    assert len(reopened.frames()) == 2


def test_crash_after_index_commit_does_not_repeat_frame(tmp_path, monkeypatch):
    store = MemoryArtifactStore()
    capture = journal(tmp_path, store=store)

    def fail():
        raise OSError("injected pre-unlink failure")

    monkeypatch.setattr(capture, "_clear_pending", fail)
    with pytest.raises(OSError, match="pre-unlink"):
        frame(capture)
    reopened = journal(tmp_path, store=store)
    assert len(reopened.frames()) == 1 and reopened.checkpoint.pending_intent
    result = reopened.recover(
        writer_stopped=True, session_id="restart", received_ns=123456790, monotonic_ns=0
    )
    assert result.details["intent_already_committed"] is True
    assert len(reopened.frames()) == 1 and not reopened.checkpoint.pending_intent


def test_recovery_write_failure_is_itself_recoverable(tmp_path, monkeypatch):
    store = MemoryArtifactStore()
    capture = journal(tmp_path, store=store)
    original = store.put
    monkeypatch.setattr(store, "put", lambda *_: (_ for _ in ()).throw(OSError("injected")))
    with pytest.raises(OSError):
        frame(capture)
    with pytest.raises(OSError):
        capture.recover(
            writer_stopped=True, session_id="restart", received_ns=123456790, monotonic_ns=0
        )
    monkeypatch.setattr(store, "put", original)
    reopened = journal(tmp_path, store=store)
    recovered = reopened.recover(
        writer_stopped=True, session_id="restart-2", received_ns=123456791, monotonic_ns=0
    )
    assert recovered.kind == "interruption"
    assert len(reopened.records()) == 1 and not reopened.frames()
    assert not reopened.checkpoint.pending_intent


@pytest.mark.parametrize(
    "limits,first_allowed",
    [
        (CaptureLimits(max_frames=1), True),
        (CaptureLimits(max_records=1), True),
        (CaptureLimits(max_frame_bytes=1), False),
        (CaptureLimits(max_total_bytes=8193), False),
    ],
)
def test_limits_stop_before_new_intent(tmp_path, limits, first_allowed):
    capture = journal(tmp_path, limits=limits)
    if first_allowed:
        frame(capture)
    before = capture.checkpoint
    with pytest.raises(CaptureLimitError):
        frame(capture, utc=123456790, mono=11)
    assert capture.checkpoint == before and not capture.checkpoint.pending_intent


def test_free_space_reserve_stops_before_write(tmp_path, monkeypatch):
    capture = journal(tmp_path, limits=CaptureLimits(min_free_disk_bytes=100))
    monkeypatch.setattr(
        "bot_trader.market_data.capture.shutil.disk_usage", lambda _: SimpleNamespace(free=100)
    )
    with pytest.raises(CaptureLimitError, match="free-disk"):
        frame(capture)
    assert capture.records() == ()


def test_clock_reversals_are_not_clamped_or_erased(tmp_path):
    capture = journal(tmp_path)
    first = frame(capture)
    with pytest.raises(ValueError, match="Monotonic"):
        frame(capture, utc=first.received_ns + 1, mono=9)
    reverse = frame(capture, utc=first.received_ns - 1, mono=11)
    assert reverse.received_ns == first.received_ns - 1
    assert capture.diagnostics == ("utc_receipt_regression:2",)
    frame(capture, utc=first.received_ns + 2, mono=0, session="new-session")
    with pytest.raises(ValueError):
        frame(capture, utc=1.5, mono=12)
    assert len(capture.frames()) == 3


@pytest.mark.parametrize(
    "change",
    [
        {"config_hash": "b" * 64},
        {"source_id": "other"},
        {"source_version": "2"},
        {"rights_reference": "different"},
        {"synthetic": False},
    ],
)
def test_reopen_cannot_change_provenance(tmp_path, change):
    capture = journal(tmp_path)
    with pytest.raises(ValueError, match="changed"):
        journal(tmp_path, store=capture.store, **change)


def test_empty_original_frame_retained_without_fake_payload(tmp_path):
    capture = journal(tmp_path)
    receipt = frame(capture, b"")
    assert receipt.raw_sha256 == hashlib.sha256(b"").hexdigest()
    assert capture.read_frame(receipt) == b"" and receipt.raw_size == 0


def test_metadata_limit_and_symlink_are_rejected(tmp_path):
    capture = journal(tmp_path)
    with pytest.raises(CaptureLimitError):
        capture.append_control(
            "gap", session_id="s", received_ns=1, monotonic_ns=1, details={"oversize": "x" * 4096}
        )
    target = tmp_path / "target.json"
    target.write_text(json.dumps({"record_hash": "a" * 64}))
    (capture.directory / "records/000000000001.json").symlink_to(target)
    with pytest.raises((ValueError, OSError)):
        capture.records()


class CountingStore(MemoryArtifactStore):
    def __init__(self):
        super().__init__()
        self.reads = 0

    def get(self, digest, suffix):
        self.reads += 1
        return super().get(digest, suffix)


def test_single_writer_append_and_checkpoint_work_scales_linearly(tmp_path, monkeypatch):
    from pathlib import Path

    directory_scans = []
    original_iterdir = Path.iterdir

    def counted_iterdir(path):
        if path.name == "records":
            directory_scans.append(path)
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", counted_iterdir)

    def measured(size, name):
        store = CountingStore()
        capture = journal(tmp_path / name, store=store)
        scans_before = len(directory_scans)
        store.reads = 0
        for index in range(size):
            frame(capture, str(index).encode(), utc=index, mono=index)
            assert capture.checkpoint.frames == index + 1
        append_reads = store.reads
        # A single active collector must not rescan the growing directory per frame.
        assert len(directory_scans) == scans_before
        capture.audit()
        audit_reads = store.reads - append_reads
        assert len(directory_scans) == scans_before + 1
        assert size <= audit_reads <= 2 * size + 4
        return append_reads

    small = measured(20, "small")
    large = measured(40, "large")
    assert small > 0
    assert large <= small * 2.2


def test_alternating_instances_audit_handover_and_share_exact_prefix(tmp_path):
    store = MemoryArtifactStore()
    first = journal(tmp_path, store=store)
    second = journal(tmp_path, store=store)
    expected = []
    for index in range(8):
        writer = first if index % 2 == 0 else second
        expected.append(frame(writer, str(index).encode(), utc=index, mono=index))
        assert writer.checkpoint.committed_records == index + 1
    assert first.audit() == second.audit()
    assert first.records() == second.records() == tuple(expected)
    assert journal(tmp_path, store=store).records() == tuple(expected)


def test_old_same_size_corruption_is_found_at_audit_not_silently_admitted(tmp_path):
    store = LocalArtifactStore(tmp_path / "blobs")
    capture = journal(tmp_path, store=store)
    first = frame(capture, b"first", utc=1, mono=1)
    frame(capture, b"second", utc=2, mono=2)
    (store.root / f"{first.raw_sha256}.bin").write_bytes(b"FIRST")
    # Cached old immutable objects aren't reread per append. This is not a hostile
    # administrator boundary; downstream admission always requests a full audit.
    frame(capture, b"third", utc=3, mono=3)
    with pytest.raises(PlatformError, match="checksum"):
        capture.audit()
    with pytest.raises(PlatformError, match="checksum"):
        capture.records()
    with pytest.raises(PlatformError, match="checksum"):
        journal(tmp_path, store=store)


def test_latest_boundary_corruption_blocks_append_before_intent(tmp_path):
    store = LocalArtifactStore(tmp_path / "blobs")
    capture = journal(tmp_path, store=store)
    latest = frame(capture, b"latest", utc=1, mono=1)
    (store.root / f"{latest.raw_sha256}.bin").write_bytes(b"LATEST")
    with pytest.raises(PlatformError):
        frame(capture, b"next", utc=2, mono=2)
    assert not (capture.directory / "pending.json").exists()


def test_deleted_boundary_blocks_without_recreating_index(tmp_path):
    capture = journal(tmp_path)
    frame(capture, utc=1, mono=1)
    last = capture.directory / "records/000000000001.json"
    last.unlink()
    # Deleting the entire one-record index is indistinguishable from an empty
    # on-disk journal unless the verified in-memory prefix is compared explicitly.
    with pytest.raises(ValueError, match="prefix"):
        frame(capture, utc=2, mono=2)
    assert not last.exists() and not (capture.directory / "pending.json").exists()


def test_external_valid_tail_plus_gap_never_gets_silently_filled(tmp_path):
    store = MemoryArtifactStore()
    first = journal(tmp_path, store=store)
    frame(first, utc=1, mono=1)
    second = journal(tmp_path, store=store)
    frame(second, utc=2, mono=2)
    frame(second, utc=3, mono=3)
    frame(second, utc=4, mono=4)
    missing = first.directory / "records/000000000003.json"
    missing.unlink()
    with pytest.raises(ValueError, match="missing"):
        frame(first, utc=5, mono=5)
    assert not missing.exists() and not (first.directory / "pending.json").exists()
