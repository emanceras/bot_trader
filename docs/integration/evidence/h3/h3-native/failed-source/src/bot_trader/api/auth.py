"""Local credentials and bounded revocable sessions; no external identity provider."""

import hashlib
import secrets
import threading
import time
from dataclasses import dataclass

from pydantic import SecretStr

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import PlatformError


@dataclass(frozen=True)
class Session:
    principal: Principal
    csrf: str
    expires_at: float


class Sessions:
    def __init__(self, credentials: dict[str, tuple[SecretStr, Principal]], ttl: int) -> None:
        if not credentials:
            raise ValueError("At least one local credential is required.")
        self._credentials = credentials
        self._ttl = ttl
        self._sessions: dict[str, Session] = {}
        self._attempts: list[float] = []
        self._lock = threading.Lock()

    @staticmethod
    def _key(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    def login(self, token: str) -> tuple[str, Session]:
        now = time.monotonic()
        with self._lock:
            self._attempts = [value for value in self._attempts if now - value < 60]
            if len(self._attempts) >= 30:
                raise PlatformError(
                    "rate_limited", "Too many login attempts. Try again later.", 429
                )
            self._attempts.append(now)
            principal = None
            for credential, candidate in self._credentials.values():
                if secrets.compare_digest(
                    self._key(token), self._key(credential.get_secret_value())
                ):
                    principal = candidate
            if principal is None:
                raise PlatformError("unauthenticated", "Invalid local credential.", 401)
            self._sessions = {
                key: value for key, value in self._sessions.items() if value.expires_at > now
            }
            if len(self._sessions) >= 100:
                raise PlatformError("session_limit", "Active session limit reached.", 429)
            identifier = secrets.token_urlsafe(32)
            session = Session(principal, secrets.token_urlsafe(32), now + self._ttl)
            self._sessions[self._key(identifier)] = session
            return identifier, session

    def get(self, identifier: str | None) -> Session:
        with self._lock:
            session = self._sessions.get(self._key(identifier or ""))
            if session is None or session.expires_at <= time.monotonic():
                self._sessions.pop(self._key(identifier or ""), None)
                raise PlatformError("unauthenticated", "Sign in to access the platform.", 401)
            return session

    def revoke(self, identifier: str) -> None:
        with self._lock:
            self._sessions.pop(self._key(identifier), None)
