"""Bounded public Kraken WebSocket transport; construction never opens a socket.

The optional, pinned library handles TLS/WebSocket framing. This synchronous port
owns a private asyncio loop and must run outside an active asyncio loop. Application
receipt is measured by the collector after receive(), not at the network interface.
OS DNS resolution can outlive cancellation; a supervised process watchdog remains
necessary for a hard whole-process deadline.
"""

from __future__ import annotations

import asyncio
import ssl
from collections.abc import Awaitable
from typing import Any, Protocol, TypeVar, cast

from bot_trader.core.events import canonical_bytes
from bot_trader.market_data.kraken_ws import KrakenProtocol

ENDPOINT = "wss://ws.kraken.com/v2"
DEPENDENCY_VERSION = "17.4"
T = TypeVar("T")


class _Connection(Protocol):
    protocol: Any
    transport: Any

    async def send(self, message: str) -> None: ...
    async def recv(self, *, decode: bool) -> str | bytes: ...
    async def close(self, code: int = 1000, reason: str = "") -> None: ...


def _duration(value: int, maximum: int) -> int:
    if type(value) is not int or not 0 < value <= maximum:
        raise ValueError("Transport duration must be a positive bounded integer in ns.")
    return value


def _public_requests() -> frozenset[bytes]:
    protocol = KrakenProtocol()
    # These are the same fixed requests generated after admission by the collector.
    protocol.instrument_online = True
    protocol.acknowledged.add("instrument")
    return frozenset(
        canonical_bytes(request)
        for request in (*protocol.requests_for_preflight(), *protocol.market_requests())
    )


class KrakenWebSocketTransport:
    """One connection session with no private methods, redirects, proxies or auto-retry."""

    simulated = False

    def __init__(
        self,
        *,
        open_timeout_ns: int = 10_000_000_000,
        send_timeout_ns: int = 2_000_000_000,
        close_timeout_ns: int = 3_000_000_000,
        max_frame_bytes: int = 1_048_576,
    ) -> None:
        self.open_timeout_ns = _duration(open_timeout_ns, 10_000_000_000)
        self.send_timeout_ns = _duration(send_timeout_ns, 2_000_000_000)
        self.close_timeout_ns = _duration(close_timeout_ns, 3_000_000_000)
        if type(max_frame_bytes) is not int or not 0 < max_frame_bytes <= 1_048_576:
            raise ValueError("Public message limit must be between 1 byte and 1 MiB.")
        self.max_frame_bytes = max_frame_bytes
        self._loop: asyncio.AbstractEventLoop | None = None
        self._connection: _Connection | None = None
        self._attempted = False
        self.close_outcome: str | None = None

    async def _dial(self, endpoint: str, context: ssl.SSLContext) -> _Connection:
        # Optional extra: default platform import/construction does not require it.
        import websockets
        from websockets.asyncio.client import connect

        if websockets.__version__ != DEPENDENCY_VERSION:
            raise ValueError("The admitted WebSocket library version is not installed.")

        class NoRedirect(connect):
            def process_redirect(self, exc: Exception) -> Exception | str:
                return exc

        connection = await NoRedirect(
            endpoint,
            ssl=context,
            proxy=None,
            compression=None,
            open_timeout=self.open_timeout_ns / 1_000_000_000,
            close_timeout=self.close_timeout_ns / 1_000_000_000,
            ping_interval=None,
            max_size=self.max_frame_bytes,
            max_queue=1,
            write_limit=4096,
            user_agent_header="bot_trader-public-capture/1",
        )
        return cast(_Connection, connection)

    def _run(self, operation: Awaitable[T], duration_ns: int) -> T:
        if self._loop is None or self._loop.is_closed():
            raise ValueError("Transport session is not open.")
        # Float seconds schedule a timeout only; source/receipt timestamps stay exact ints.
        return self._loop.run_until_complete(
            asyncio.wait_for(operation, duration_ns / 1_000_000_000)
        )

    def connect(self, endpoint: str) -> None:
        if endpoint != ENDPOINT or self._attempted:
            raise ValueError("Only one exact public Kraken endpoint/session is admitted.")
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            raise ValueError("Synchronous capture transport requires a dedicated worker thread.")
        self._attempted = True
        self._loop = asyncio.new_event_loop()
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        try:
            self._connection = self._run(self._dial(endpoint, context), self.open_timeout_ns)
        except ImportError as error:
            self._shutdown_loop()
            raise ValueError(
                "Install the pinned optional capture extra before acquisition."
            ) from error
        except ssl.SSLCertVerificationError as error:
            self._shutdown_loop()
            raise ValueError(
                "TLS certificate verification failed; do not retry insecurely."
            ) from error
        except Exception as error:
            self._shutdown_loop()
            from websockets.exceptions import InvalidHandshake, InvalidURI, SecurityError

            if isinstance(error, (InvalidHandshake, InvalidURI, SecurityError, ValueError)):
                raise ValueError(
                    "Public WebSocket handshake or admitted endpoint rejected."
                ) from error
            if isinstance(error, (TimeoutError, OSError)):
                raise ConnectionError(
                    "Public WebSocket opening failed within its bound."
                ) from error
            raise

    def _link(self) -> _Connection:
        if self._connection is None or self._loop is None:
            raise ValueError("Transport has no connected session.")
        return self._connection

    def send(self, request: dict[str, Any]) -> None:
        wire = canonical_bytes(request)
        if wire not in _public_requests():
            raise ValueError("Only the exact public instrument/trade/ticker requests are allowed.")
        connection = self._link()
        try:
            self._run(connection.send(wire.decode("utf-8")), self.send_timeout_ns)
        except Exception as error:
            from websockets.exceptions import ConnectionClosed

            if isinstance(error, (TimeoutError, OSError, ConnectionClosed)):
                raise ConnectionError(
                    "Public subscription send failed; outcome is uncertain."
                ) from error
            raise

    def receive(self, timeout_ns: int) -> bytes:
        from bot_trader.market_data.capture_service import ReceivePollTimeout

        duration = _duration(timeout_ns, 10_000_000_000)
        connection = self._link()
        try:
            raw = self._run(connection.recv(decode=False), duration)
        except TimeoutError as error:
            raise ReceivePollTimeout("No message within this finite receive poll.") from error
        except Exception as error:
            from websockets.exceptions import ConnectionClosed

            if isinstance(error, (OSError, ConnectionClosed)):
                raise ConnectionError("Public WebSocket disconnected.") from error
            raise
        if not isinstance(raw, bytes) or not 0 < len(raw) <= self.max_frame_bytes:
            raise ValueError("Delivered WebSocket message violates the original-byte limit.")
        return raw

    def _abort(self) -> None:
        if self._connection is not None:
            self._connection.transport.abort()
            if self._loop is not None and not self._loop.is_closed():
                self._loop.run_until_complete(asyncio.sleep(0))

    def _shutdown_loop(self) -> None:
        loop, self._loop = self._loop, None
        if loop is None or loop.is_closed():
            return
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        if pending:
            # Cooperative library tasks receive cancellation; no unbounded executor join.
            loop.run_until_complete(asyncio.wait(pending, timeout=0.1))
        loop.close()

    def close(self) -> None:
        connection = self._connection
        if connection is None:
            self._shutdown_loop()
            return
        failure: Exception | None = None
        try:
            try:
                self._run(
                    connection.close(code=1000, reason="finite public capture stopped"),
                    self.close_timeout_ns,
                )
            except Exception as error:
                failure = error
                self._abort()
            closed = connection.protocol.state == 3  # websockets.protocol.State.CLOSED
            received_close = connection.protocol.close_rcvd is not None
            local_closed = closed
            if not local_closed:
                self._abort()
                local_closed = connection.protocol.state == 3
            if not local_closed:
                self.close_outcome = "unconfirmed"
                raise OSError("Local WebSocket shutdown could not be confirmed.") from failure
            self.close_outcome = (
                "graceful"
                if closed and received_close and failure is None
                else "local_closed_remote_unknown"
            )
        finally:
            self._connection = None
            self._shutdown_loop()
