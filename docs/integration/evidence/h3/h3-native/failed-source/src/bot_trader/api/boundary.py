"""Bounded HTTP input and same-origin mutation boundary."""

from uuid import uuid4

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from bot_trader.core.settings import Settings


class RequestBoundary:
    def __init__(self, app: ASGIApp, settings: Settings) -> None:
        self.app = app
        self.settings = settings

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        correlation = str(uuid4())
        scope.setdefault("state", {})["correlation_id"] = correlation
        headers = dict(scope["headers"])

        async def reject(code: str, message: str, status: int) -> None:
            response = JSONResponse(
                {"error": {"code": code, "message": message, "correlation_id": correlation}},
                status_code=status,
            )
            await response(scope, receive, secured_send)

        async def secured_send(message: Message) -> None:
            if message["type"] == "http.response.start":
                message["headers"] = list(message.get("headers", [])) + [
                    (b"x-content-type-options", b"nosniff"),
                    (b"x-frame-options", b"DENY"),
                    (b"referrer-policy", b"no-referrer"),
                    (b"cache-control", b"no-store"),
                    (b"x-correlation-id", correlation.encode()),
                    (
                        b"content-security-policy",
                        b"default-src 'self'; script-src 'self'; "
                        b"style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                        b"connect-src 'self'; "
                        b"frame-ancestors 'none'; object-src 'none'; base-uri 'self'",
                    ),
                ]
            await send(message)

        if scope["method"] not in {"GET", "HEAD", "OPTIONS"}:
            origin = headers.get(b"origin", b"").decode("latin1")
            if origin not in self.settings.allowed_origins:
                await reject("origin_denied", "Mutation requires an allowed browser origin.", 403)
                return
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError:
                declared_size = -1
            if declared_size < 0 or declared_size > self.settings.max_request_bytes:
                await reject(
                    "request_too_large", "Request body is outside the allowed bounds.", 413
                )
                return
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            if len(body) > self.settings.max_request_bytes:
                await reject(
                    "request_too_large", "Request body is outside the allowed bounds.", 413
                )
                return
            if not message.get("more_body", False):
                break
        delivered = False

        async def buffered_receive() -> Message:
            nonlocal delivered
            if delivered:
                return await receive()
            delivered = True
            return {"type": "http.request", "body": bytes(body), "more_body": False}

        await self.app(scope, buffered_receive, secured_send)
