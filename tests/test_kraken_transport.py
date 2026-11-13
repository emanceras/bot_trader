"""Real connector code with invented peers only: no network connection is made."""

import asyncio
import ssl
from types import SimpleNamespace

import pytest

from bot_trader.core.events import canonical_bytes
from bot_trader.market_data.kraken_transport import (
    ENDPOINT,
    KrakenWebSocketTransport,
)
from bot_trader.market_data.kraken_ws import KrakenProtocol


pytest.importorskip("websockets", reason="Pinned optional capture extra is required.")


class FakeConnection:
    def __init__(self, messages=()):
        self.messages = iter(messages)
        self.sent = []
        self.received_decode = []
        self.protocol = SimpleNamespace(state=1, close_rcvd=None)
        self.transport = SimpleNamespace(abort=self.abort)
        self.abort_count = 0
        self.close_arguments = None
        self.send_delay = self.close_delay = False
        self.confirm_close = True
        self.abort_completes = True

    async def send(self, message):
        if self.send_delay:
            await asyncio.Event().wait()
        self.sent.append(message)

    async def recv(self, *, decode):
        self.received_decode.append(decode)
        value = next(self.messages, None)
        if value is None:
            await asyncio.Event().wait()
        if isinstance(value, BaseException):
            raise value
        return value

    async def close(self, *, code, reason):
        self.close_arguments = code, reason
        if self.close_delay:
            await asyncio.Event().wait()
        if self.confirm_close:
            self.protocol.state = 3
            self.protocol.close_rcvd = SimpleNamespace(code=1000)

    def abort(self):
        self.abort_count += 1
        if self.abort_completes:
            self.protocol.state = 3


def attach(monkeypatch, connection, **kwargs):
    client = KrakenWebSocketTransport(**kwargs)
    calls = []

    async def dial(endpoint, context):
        calls.append((endpoint, context))
        return connection

    monkeypatch.setattr(client, "_dial", dial)
    client.connect(ENDPOINT)
    return client, calls


def test_construction_has_no_connection_and_refuses_other_endpoints(monkeypatch):
    import socket

    monkeypatch.setattr(socket, "create_connection", lambda *_a, **_k: pytest.fail("network"))
    client = KrakenWebSocketTransport()
    assert client._loop is None and client._connection is None
    for endpoint in (
        "ws://ws.kraken.com/v2",
        "wss://evil.invalid/v2",
        ENDPOINT + "?token=secret",
        "wss://ws.kraken.com/v2/",
    ):
        with pytest.raises(ValueError, match="exact public"):
            client.connect(endpoint)
    client.close()


def test_secure_dial_parameters_redirect_denial_and_version(monkeypatch):
    import websockets
    from websockets.asyncio import client as library

    assert websockets.__version__ == "17.4"
    peer = FakeConnection()
    seen = {}

    class Dial:
        def __init__(self, endpoint, **kwargs):
            seen.update(endpoint=endpoint, kwargs=kwargs, dial=self)

        def __await__(self):
            async def answer():
                return peer

            return answer().__await__()

    monkeypatch.setattr(library, "connect", Dial)
    transport = KrakenWebSocketTransport(max_frame_bytes=1024)
    transport.connect(ENDPOINT)
    try:
        settings = seen["kwargs"]
        assert seen["endpoint"] == ENDPOINT
        assert settings["ssl"].verify_mode == ssl.CERT_REQUIRED
        assert settings["ssl"].check_hostname is True
        assert settings["proxy"] is settings["compression"] is settings["ping_interval"] is None
        assert settings["max_size"] == 1024 and settings["max_queue"] == 1
        assert settings["write_limit"] == 4096
        assert settings["open_timeout"] == 10 and settings["close_timeout"] == 3
        rejection = ValueError("redirect must not be followed")
        assert seen["dial"].process_redirect(rejection) is rejection
        with pytest.raises(ValueError, match="one exact"):
            transport.connect(ENDPOINT)
    finally:
        transport.close()
    assert transport.close_outcome == "graceful" and transport._loop is None


def test_only_exact_public_subscriptions_can_be_sent(monkeypatch):
    peer = FakeConnection()
    transport, _ = attach(monkeypatch, peer)
    try:
        protocol = KrakenProtocol()
        protocol.instrument_online = True
        protocol.acknowledged.add("instrument")
        requests = (*protocol.requests_for_preflight(), *protocol.market_requests())
        for request in requests:
            transport.send(request)
        assert peer.sent == [canonical_bytes(request).decode() for request in requests]
        for invalid in (
            {"method": "add_order", "params": {}},
            {"method": "subscribe", "params": {"channel": "executions"}},
            requests[0] | {"token": "private"},
            requests[0] | {"req_id": True},
            {"method": "subscribe", "params": {"channel": "trade", "symbol": ["ETH/EUR"]}},
        ):
            with pytest.raises(ValueError, match="exact public"):
                transport.send(invalid)
        assert len(peer.sent) == 3
    finally:
        transport.close()


def test_raw_message_bytes_return_unmodified_and_poll_timeout_is_not_disconnect(monkeypatch):
    from bot_trader.market_data.capture_service import ReceivePollTimeout

    raw = b'{ "channel" : "heartbeat", "synthetic_unicode":"\xc3\xb1" }'
    peer = FakeConnection([raw, None, raw])
    transport, _ = attach(monkeypatch, peer)
    try:
        assert transport.receive(1_000_000) == raw
        with pytest.raises(ReceivePollTimeout):
            transport.receive(1_000_000)
        assert transport.receive(1_000_000) == raw
        assert peer.received_decode == [False, False, False]
    finally:
        transport.close()


@pytest.mark.parametrize("raw", [b"", b"abcde", '{"decoded":true}'])
def test_invalid_raw_return_or_size_is_rejected(monkeypatch, raw):
    peer = FakeConnection([raw])
    transport, _ = attach(monkeypatch, peer, max_frame_bytes=4)
    try:
        with pytest.raises(ValueError, match="original-byte"):
            transport.receive(1_000_000)
    finally:
        transport.close()


def test_receive_disconnect_and_send_timeout_are_recoverable_errors(monkeypatch):
    peer = FakeConnection([ConnectionResetError("invented disconnect")])
    transport, _ = attach(monkeypatch, peer, send_timeout_ns=1_000_000)
    try:
        with pytest.raises(ConnectionError, match="disconnected"):
            transport.receive(1_000_000)
        peer.send_delay = True
        with pytest.raises(ConnectionError, match="uncertain"):
            transport.send(KrakenProtocol.preflight_request())
    finally:
        transport.close()


@pytest.mark.parametrize(
    "failure", [ssl.SSLCertVerificationError("fixture"), ValueError("fixture")]
)
def test_security_handshake_failure_is_permanent_and_cleans_loop(monkeypatch, failure):
    transport = KrakenWebSocketTransport()

    async def dial(*_):
        raise failure

    monkeypatch.setattr(transport, "_dial", dial)
    with pytest.raises(ValueError):
        transport.connect(ENDPOINT)
    assert transport._loop is None
    transport.close()


def test_open_timeout_cleans_loop_without_real_dns(monkeypatch):
    transport = KrakenWebSocketTransport(open_timeout_ns=1_000_000)

    async def dial(*_):
        await asyncio.Event().wait()

    monkeypatch.setattr(transport, "_dial", dial)
    with pytest.raises(ConnectionError, match="opening failed"):
        transport.connect(ENDPOINT)
    assert transport._loop is None


def test_close_timeout_aborts_locally_without_claiming_remote_ack(monkeypatch):
    peer = FakeConnection()
    peer.close_delay = True
    transport, _ = attach(monkeypatch, peer, close_timeout_ns=1_000_000)
    transport.close()
    assert peer.abort_count == 1 and peer.protocol.state == 3
    assert peer.protocol.close_rcvd is None
    assert transport.close_outcome == "local_closed_remote_unknown"
    assert transport._loop is None
    transport.close()


def test_failed_local_shutdown_is_not_reported_closed(monkeypatch):
    peer = FakeConnection()
    peer.confirm_close = peer.abort_completes = False
    transport, _ = attach(monkeypatch, peer)
    with pytest.raises(OSError, match="could not be confirmed"):
        transport.close()
    assert transport.close_outcome == "unconfirmed"
    assert transport._loop is None


def test_remote_drop_allows_new_session_but_preserves_unknown_ack(monkeypatch):
    peer = FakeConnection()
    peer.protocol.state = 3
    peer.confirm_close = False
    transport, _ = attach(monkeypatch, peer)
    transport.close()
    assert transport.close_outcome == "local_closed_remote_unknown"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"open_timeout_ns": 0},
        {"open_timeout_ns": 11_000_000_000},
        {"send_timeout_ns": True},
        {"close_timeout_ns": 3.1},
        {"max_frame_bytes": 1_048_577},
        {"max_frame_bytes": 0},
    ],
)
def test_constructor_bounds_are_strict(kwargs):
    with pytest.raises(ValueError):
        KrakenWebSocketTransport(**kwargs)


def test_active_async_loop_rejected_before_dial(monkeypatch):
    transport = KrakenWebSocketTransport()

    async def operation():
        with pytest.raises(ValueError, match="dedicated worker"):
            transport.connect(ENDPOINT)

    asyncio.run(operation())
    assert transport._loop is None
