"""Invented Kraken wire messages only; no socket, credential or market dataset."""

import hashlib
from decimal import Decimal

import pytest

from bot_trader.core.events import QuoteData, TradeData, canonical_bytes, content_hash
from bot_trader.market_data.archive import SourceSpec
from bot_trader.market_data.kraken_ws import (
    SCHEMA,
    FrameReference,
    KrakenProtocol,
    KrakenWSNormalizer,
    exact_ws_json,
    rfc3339_ns,
)
from bot_trader.market_data.storage import MemoryArtifactStore

BASE = 1_794_441_600_000_000_000  # 2026-11-12T00:00:00Z
STAMP = "2026-11-12T00:00:00.000000123Z"
MANIFEST = "a" * 64


def ack(channel):
    result = {"channel": channel, "snapshot": True}
    if channel != "instrument":
        result["symbol"] = "BTC/EUR"
    return {
        "method": "subscribe",
        "success": True,
        "result": result,
        "req_id": {"instrument": 1, "trade": 2, "ticker": 3}[channel],
    }


def instrument():
    return {
        "channel": "instrument",
        "type": "snapshot",
        "data": {
            "pairs": [
                {"symbol": "BTC/EUR", "base": "BTC", "quote": "EUR", "status": "online"},
            ]
        },
    }


def handshake():
    return [ack("instrument"), instrument(), ack("trade"), ack("ticker")]


def trade(identity=1, *, snapshot=False, price="100.123456789123456789"):
    return {
        "channel": "trade",
        "type": "snapshot" if snapshot else "update",
        "data": [
            {
                "symbol": "BTC/EUR",
                "timestamp": STAMP,
                "trade_id": identity,
                "side": "buy",
                "ord_type": "limit",
                "price": price,
                "qty": "0.123456789123456789",
            }
        ],
    }


def ticker():
    return {
        "channel": "ticker",
        "type": "update",
        "data": [
            {
                "symbol": "BTC/EUR",
                "timestamp": STAMP,
                "bid": "100",
                "bid_qty": "2",
                "ask": "101",
                "ask_qty": "3",
            }
        ],
    }


def frames(messages):
    """Every raw control frame is included; sessions are supplied explicitly."""
    store = MemoryArtifactStore()
    references = []
    for sequence, (session, message) in enumerate(messages, 1):
        raw = message if isinstance(message, bytes) else canonical_bytes(message)
        references.append(
            FrameReference(
                capture_id="test-capture",
                session_id=session,
                local_sequence=sequence,
                raw_sha256=store.put(raw, "bin"),
                received_ns=BASE + 1_000_000 + sequence,
                monotonic_ns=sequence,
                config_hash="b" * 64,
                source_id="kraken-ws-v2",
                source_version="1",
            )
        )
    return store, references


def session(messages, identity="session-1"):
    return [(identity, message) for message in messages]


def test_exact_timestamp_decimal_and_json_canaries():
    assert rfc3339_ns(STAMP) == BASE + 123
    assert rfc3339_ns("2026-11-12T01:00:00.000000123+01:00") == BASE + 123
    assert rfc3339_ns("1970-01-01T00:00:00.000000001Z") == 1
    parsed = exact_ws_json(b'{"price":100.123456789123456789}')
    assert parsed["price"] == Decimal("100.123456789123456789")
    for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b"[]", b"{invalid"):
        with pytest.raises(ValueError):
            exact_ws_json(raw)
    for timestamp in (
        "2026-11-12T00:00:00.0000000001Z",
        "2026-11-12T00:00:00",
        "2026-11-12T00:00:00+01:60",
        "2026-11-12T00:00:00-00:00",
        1.0,
    ):
        with pytest.raises(ValueError):
            rfc3339_ns(timestamp)


def test_protocol_preflight_and_interleaved_market_acknowledgements():
    protocol = KrakenProtocol()
    assert protocol.requests_for_preflight()[0]["params"]["channel"] == "instrument"
    with pytest.raises(ValueError):
        protocol.market_requests()
    for message in handshake()[:3]:
        protocol.accept(canonical_bytes(message))
    assert protocol.preflight_ready and not protocol.ready
    assert protocol.market_requests()[1]["params"]["event_trigger"] == "bbo"
    # Trade snapshot may precede the independent ticker acknowledgement.
    assert protocol.accept(canonical_bytes(trade())).kind == "market"
    with pytest.raises(ValueError, match="handshake"):
        protocol.accept(canonical_bytes(ticker()))
    result = protocol.accept(canonical_bytes(ack("ticker")))
    assert result.ready and "not_echoed" in result.diagnostics[0]
    assert protocol.accept(canonical_bytes(ticker())).kind == "market"


@pytest.mark.parametrize("fault", ["symbol", "trigger", "request", "offline", "schema"])
def test_protocol_rejects_incompatible_or_ambiguous_context(fault):
    protocol = KrakenProtocol()
    for message in handshake():
        protocol.accept(canonical_bytes(message))
    message = ack("ticker")
    if fault == "symbol":
        message["result"]["symbol"] = "ETH/EUR"
    elif fault == "trigger":
        message["result"]["event_trigger"] = "trades"
    elif fault == "request":
        message["req_id"] = True
    elif fault == "offline":
        message = instrument()
        message["data"]["pairs"][0]["status"] = "cancel_only"
    else:
        message = {"channel": "unrecognized"}
    with pytest.raises(ValueError):
        protocol.accept(canonical_bytes(message))


def test_normalizer_preserves_exact_identity_mapping_first_receipt_and_ticker_deliveries():
    messages = session(handshake() + [trade(snapshot=True), ticker(), ticker()])
    messages += session(handshake() + [trade(), trade(2)], "session-2")
    store, references = frames(messages)
    result = KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)
    assert len(result.events) == 4
    first = result.events[0]
    assert isinstance(first.data, TradeData)
    assert first.data.price == "100.123456789123456789"
    assert first.data.quantity == "0.123456789123456789"
    assert first.event_ns == BASE + 123
    assert first.available_ns == first.received_ns == references[4].received_ns
    assert first.raw_sha256 == references[4].raw_sha256
    assert first.instrument == "BTC-EUR" and first.quote_currency == "EUR"
    assert result.rows[0].original_symbol == "BTC/EUR"
    assert result.rows[0].mapping_version == "kraken-symbol-map-v1"
    assert result.rows[3].duplicate_delivery
    assert result.rows[3].event_id == first.event_id
    assert result.rows[3].received_ns > first.received_ns
    quotes = [event for event in result.events if isinstance(event.data, QuoteData)]
    assert len(quotes) == 2 and quotes[0].event_id != quotes[1].event_id
    assert quotes[0].data.origin == "synthetic_explicit"
    assert [event.sequence for event in result.events if isinstance(event.data, TradeData)] == [
        1,
        2,
    ]
    assert result == KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)
    observed = KrakenWSNormalizer(store, synthetic=False).normalize_frames(references, MANIFEST)
    assert observed.events[1].data.origin == "observed"


def test_normalizer_requires_handshake_each_session_and_retains_bad_raw():
    for messages in (
        session([trade()]),
        session(handshake() + [trade()]) + session([ticker()], "session-2"),
        session(handshake()) + session(handshake(), "session-2") + session([ticker()]),
        session(handshake() + [b'{"channel":"unknown"}']),
    ):
        store, references = frames(messages)
        with pytest.raises(ValueError):
            KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)
        assert store.get(references[-1].raw_sha256, "bin")
    messages = handshake()[:3] + [trade(), ack("ticker"), ticker()]
    store, references = frames(session(messages))
    assert len(KrakenWSNormalizer(store).normalize_frames(references, MANIFEST).events) == 2


@pytest.mark.parametrize(
    "fault",
    [
        "future",
        "missing_timestamp",
        "precision",
        "conflict",
        "float_id",
        "crossed_quote",
        "numeric",
    ],
)
def test_normalizer_rejects_unsupported_values_without_silent_conversion(fault):
    message = trade()
    before = []
    if fault == "future":
        message["data"][0]["timestamp"] = "2026-11-13T00:00:00Z"
    elif fault == "missing_timestamp":
        message = ticker()
        del message["data"][0]["timestamp"]
    elif fault == "precision":
        message["data"][0]["timestamp"] = "2026-11-12T00:00:00.0000000123Z"
    elif fault == "conflict":
        before = [trade()]
        message["data"][0]["qty"] = "999"
    elif fault == "float_id":
        message["data"][0]["trade_id"] = 1.0
    elif fault == "crossed_quote":
        message = ticker()
        message["data"][0]["bid"] = "102"
    else:
        message["data"][0]["price"] = "invalid"
    store, references = frames(session(handshake() + before + [message]))
    with pytest.raises(ValueError):
        KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)


def test_clock_and_manifest_integrity_and_port_compatibility():
    store, references = frames(session(handshake() + [trade(), ticker()]))
    normalizer = KrakenWSNormalizer(store)
    for fields in (
        {"received_ns": 1},
        {"monotonic_ns": 0},
        {"local_sequence": 1},
        {"config_hash": "c" * 64},
    ):
        changed = references[:-1] + [references[-1].model_copy(update=fields)]
        with pytest.raises(ValueError):
            normalizer.normalize_frames(changed, MANIFEST)
    raw = canonical_bytes(
        {
            "schema_version": 1,
            "capture_id": "test-capture",
            "frames": [frame.model_dump(mode="json") for frame in references],
        }
    )
    source = SourceSpec(
        source_id="kraken-ws-v2",
        source_version="1",
        source_schema=SCHEMA,
        locator="synthetic:test-capture",
        rights="Entirely invented test fixture",
        acquired_ns=references[-1].received_ns,
        size_bytes=len(raw),
        raw_sha256=hashlib.sha256(raw).hexdigest(),
        data_class="synthetic",
    )
    digest = content_hash(source.model_dump(mode="json"))
    result = normalizer.normalize_with_provenance(raw, source, digest)
    assert normalizer.normalize(raw, source, digest) == result.batch
    assert result.batch.raw_sha256 == source.raw_sha256
    with pytest.raises(ValueError, match="identity"):
        normalizer.normalize_with_provenance(raw + b" ", source, digest)
    with pytest.raises(ValueError, match="data class"):
        KrakenWSNormalizer(store, synthetic=False).normalize_with_provenance(raw, source, digest)


def test_control_only_capture_and_trade_gap_diagnostics_do_not_invent_market_data():
    store, references = frames(session(handshake()))
    result = KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)
    assert result.events == () and result.batch is None
    store, references = frames(session(handshake() + [trade(2), trade(4), trade(1)]))
    result = KrakenWSNormalizer(store).normalize_frames(references, MANIFEST)
    assert len(result.events) == 3
    assert any("gap_not_proven_loss" in item for item in result.diagnostics)
    assert any("late_native_trade_not_retroactive" in item for item in result.diagnostics)
