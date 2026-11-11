from pathlib import Path

import pytest
from pydantic import SecretStr

from bot_trader.api.auth import Sessions
from bot_trader.api.credentials import issue_credential, load_credentials
from bot_trader.core.contracts import Principal
from bot_trader.core.errors import PlatformError
from bot_trader.core.settings import Settings


def test_session_expiration_revocation_and_token_separation(monkeypatch):
    clock = [10.0]
    monkeypatch.setattr("bot_trader.api.auth.time.monotonic", lambda: clock[0])
    principal = Principal(id="tester", role="viewer")
    sessions = Sessions({"viewer": (SecretStr("v" * 40), principal)}, ttl=60)
    token, first = sessions.login("v" * 40)
    assert sessions.get(token).principal == principal
    assert token != first.csrf
    sessions.revoke(token)
    with pytest.raises(PlatformError, match="Sign in"):
        sessions.get(token)
    token, _ = sessions.login("v" * 40)
    clock[0] = 71
    with pytest.raises(PlatformError, match="Sign in"):
        sessions.get(token)
    assert principal.role == "viewer"


def test_invalid_login_is_bounded():
    sessions = Sessions({"admin": (SecretStr("a" * 40), Principal(id="a", role="admin"))}, 60)
    for _ in range(30):
        with pytest.raises(PlatformError) as error:
            sessions.login("invalid")
        assert error.value.status_code == 401
    with pytest.raises(PlatformError) as error:
        sessions.login("a" * 40)
    assert error.value.status_code == 429


def test_credential_bootstrap_is_private_idempotent_and_never_follows_link(tmp_path: Path):
    settings = Settings(repository_root=tmp_path)
    path = issue_credential(settings, "admin")
    original = path.read_bytes()
    assert path.stat().st_mode & 0o777 == 0o600
    assert issue_credential(settings, "admin").read_bytes() == original
    assert load_credentials(settings)["admin"][1].role == "admin"
    path.chmod(0o644)
    with pytest.raises(PlatformError, match="private"):
        load_credentials(settings)
    path.unlink()
    path.symlink_to(tmp_path / "outside")
    with pytest.raises(PlatformError, match="symbolic"):
        issue_credential(settings, "admin")
