"""Invented CSVs faithful to documented schemas; never published market extracts."""

import hashlib
from decimal import localcontext
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import MarketEventV2, content_hash
from bot_trader.market_data.archive import LocalArchive, SourceSpec
from bot_trader.market_data.kraken_history import (
    BAR_SCHEMA,
    TRADE_SCHEMA,
    HistoricalAvailability,
    KrakenHistoricalNormalizer,
    KrakenSelection,
    seconds_to_ns,
    select_prefix,
    verify_archive,
)
from bot_trader.market_data.storage import MemoryArtifactStore

HEADER = b"timestamp,price,volume,type,order_type,misc,trade_id\n"
TRADE = b"1700000000.123456789,10.25,2.5,b,l,,71\n"
BAR = b"1700000040,10,12,9,11,2.5,3\n"


def prepared(raw, schema=TRADE_SCHEMA, rows=1):
    digest = hashlib.sha256(raw).hexdigest()
    selection = KrakenSelection(
        archive_sha256="a" * 64,
        archive_size_bytes=1234,
        member="XBTUSD.csv" if schema == TRADE_SCHEMA else "XBTUSD_1.csv",
        member_size_bytes=len(raw) + 100,
        member_crc32=0,
        readme_sha256="b" * 64,
        source_schema=schema,
        instrument="XBTUSD",
        base_currency="XBT",
        quote_currency="USD",
        interval_seconds=None if schema == TRADE_SCHEMA else 60,
        rows=rows,
        raw_sha256=digest,
        size_bytes=len(raw),
    )
    source = SourceSpec(
        source_id="kraken-history-fixture",
        source_version="schema-fixture-v1",
        source_schema=schema,
        locator="internal:invented-schema-fixture",
        rights="Invented test CSV; contains no historical market records.",
        acquired_ns=1700001000000000000,
        raw_sha256=digest,
        size_bytes=len(raw),
        data_class="synthetic",
    )
    return selection, source, content_hash(source.model_dump(mode="json"))


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0", 0),
        ("1.000000001", 1000000001),
        ("1.2300000000", 1230000000),
        ("1700000000.123456789", 1700000000123456789),
    ],
)
def test_decimal_seconds_exact_under_low_decimal_precision(value, expected):
    with localcontext() as context:
        context.prec = 3
        assert seconds_to_ns(value) == expected


@pytest.mark.parametrize("value", [1.2, "1e3", "NaN", "-1", "1.0000000001", "18446744074"])
def test_invalid_or_lossy_time_is_rejected(value):
    with pytest.raises(ValueError):
        seconds_to_ns(value)


def test_trade_units_source_identity_and_unknown_reception_preserved():
    raw = HEADER + TRADE
    selection, source, manifest = prepared(raw)
    result = KrakenHistoricalNormalizer(selection).normalize_with_provenance(raw, source, manifest)
    event = result.batch.events[0]
    row = result.rows[0]
    assert event.event_id == "trade-71" and event.instrument == "XBTUSD"
    assert event.event_ns == 1700000000123456789
    assert event.available_ns == event.event_ns and event.received_ns is None
    assert event.published_ns is None and event.engine_ts_init_ns is None
    assert event.original_tick == event.event_ns and event.original_unit == "ns"
    assert row.original_timestamp == "1700000000.123456789"
    assert row.original_unit == "fractional_unix_seconds" and row.physical_line == 2
    assert row.native_trade_id == "71" and row.side == "b" and row.order_type == "l"
    assert result.price_unit == "USD/XBT" and result.quantity_unit == "XBT"
    assert result.availability.optimistic_assumption is True
    assert result.batch.raw_sha256 == hashlib.sha256(raw).hexdigest()
    assert KrakenHistoricalNormalizer(selection).normalize(raw, source, manifest) == result.batch


def test_complete_open_labelled_bar_requires_end_plus_declared_delay():
    selection, source, manifest = prepared(BAR, BAR_SCHEMA)
    delay = 123
    result = KrakenHistoricalNormalizer(selection, HistoricalAvailability(delay_ns=delay))
    event = result.normalize(BAR, source, manifest).events[0]
    assert event.data.label == "open" and event.data.status == "closed"
    assert event.event_ns == 1700000040000000000
    assert event.available_ns == event.data.end_ns + delay
    assert event.received_ns is None
    with pytest.raises(ValueError, match="complete bar"):
        MarketEventV2.model_validate(event.model_dump() | {"available_ns": event.event_ns})


def test_native_identity_duplicate_gap_and_absent_ids_are_distinct():
    raw = HEADER + TRADE + TRADE + TRADE.replace(b",71", b",73")
    missing = b"1700000000.123456789,10.25,2.5,,,,\n"
    raw += missing + missing
    selection, source, manifest = prepared(raw, rows=5)
    result = KrakenHistoricalNormalizer(selection).normalize_with_provenance(raw, source, manifest)
    events = result.batch.events
    assert events[0] == events[1]
    assert [event.sequence for event in events] == [1, 1, 2, 3, 4]
    assert events[2].event_id == "trade-73"
    assert events[3].event_id != events[4].event_id
    assert any("native_id_gap_not_proven_loss" in item for item in result.batch.diagnostics)
    assert result.rows[3].native_trade_id is None
    assert len(result.rows) == 5


def test_conflicting_trade_identity_rejected_and_source_manifest_bound():
    raw = HEADER + TRADE + TRADE.replace(b"10.25", b"10.26")
    selection, source, manifest = prepared(raw, rows=2)
    adapter = KrakenHistoricalNormalizer(selection)
    with pytest.raises(ValueError, match="Conflicting native identity"):
        adapter.normalize(raw, source, manifest)
    with pytest.raises(ValueError, match="declaration hash"):
        adapter.normalize(raw, source, "c" * 64)
    reserved = SourceSpec.model_validate(source.model_dump() | {"partition": "final"})
    with pytest.raises(AccessDenied):
        adapter.normalize(raw, reserved, manifest)


def test_sparse_bar_intervals_are_not_claimed_to_be_transport_loss():
    raw = BAR + BAR.replace(b"1700000040", b"1700000160")
    selection, source, manifest = prepared(raw, BAR_SCHEMA, rows=2)
    result = KrakenHistoricalNormalizer(selection).normalize_with_provenance(raw, source, manifest)
    assert [event.sequence for event in result.batch.events] == [1, 2]
    assert any("sparse_bar_intervals_not_proven_loss" in item for item in result.batch.diagnostics)
    assert result.rows[0].trade_count == 3


def test_old_trade_column_order_is_not_silently_inferred():
    raw = HEADER.replace(b"timestamp,price,volume", b"price,volume,timestamp") + TRADE
    selection, source, manifest = prepared(raw)
    with pytest.raises(ValueError, match="header differs"):
        KrakenHistoricalNormalizer(selection).normalize(raw, source, manifest)


def test_bounded_zip_selection_archive_restart_and_idempotence(tmp_path):
    path = tmp_path / "invented.zip"
    raw = HEADER + TRADE + TRADE.replace(b",71", b",72") + TRADE.replace(b",71", b",73")
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("README.md", "Invented schema fixture, not Kraken market data.")
        archive.writestr("XBTUSD.csv", raw)
    expected = hashlib.sha256(path.read_bytes()).hexdigest()
    proof = verify_archive(path, expected_sha256=expected, expected_size=path.stat().st_size)
    parameters = dict(
        member="XBTUSD.csv",
        source_schema=TRADE_SCHEMA,
        instrument="XBTUSD",
        base_currency="XBT",
        quote_currency="USD",
        max_rows=2,
    )
    selected_raw, selected = select_prefix(path, proof, **parameters)
    assert selected_raw == HEADER + TRADE + TRADE.replace(b",71", b",72")
    assert selected.rows == 2 and selected.archive_sha256 == expected
    assert selected.whole_member_crc_verified is False
    assert select_prefix(path, proof, **parameters) == (selected_raw, selected)
    _, source, _ = prepared(selected_raw, rows=2)
    local = tmp_path / "private-prefix.csv"
    local.write_bytes(selected_raw)
    store = MemoryArtifactStore()
    importer = LocalArchive(store, chunk_size=32)
    partial = importer.import_step(local, source)
    assert not partial.complete
    restarted = LocalArchive(store, chunk_size=32)
    final = restarted.import_step(
        local, source, checkpoint_hash=partial.checkpoint_hash, max_chunks=100
    )
    assert final.complete
    repeated = restarted.import_step(local, source, max_chunks=100)
    assert final.archive_hash == repeated.archive_hash
    _, declared, restored = restarted.read(final.archive_hash)
    result = KrakenHistoricalNormalizer(selected).normalize(
        restored, declared, content_hash(declared.model_dump(mode="json"))
    )
    assert len(result.events) == 2
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="identity changed"):
        select_prefix(path, proof, **parameters)


def test_missing_original_never_triggers_download(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify_archive(tmp_path / "missing.zip", expected_sha256="0" * 64, expected_size=1)
