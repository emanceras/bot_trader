"""Local application credential bootstrap; no exchange keys or remote secrets."""

import os
import secrets
from pathlib import Path
from typing import Literal

from pydantic import SecretStr

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import Conflict
from bot_trader.core.settings import Settings

Role = Literal["admin", "researcher", "viewer", "agent"]
ROLES: tuple[Role, ...] = ("admin", "researcher", "viewer", "agent")


def issue_credential(settings: Settings, role: Role) -> Path:
    """Create once, without printing secrets or overwriting existing credentials."""
    settings.state_path.mkdir(parents=True, exist_ok=True, mode=0o700)
    destination = settings.state_path / f"{role}.token"
    if destination.is_symlink():
        raise Conflict("Credential path cannot be a symbolic link.")
    if destination.exists():
        _read_credential(destination)
        return destination
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as handle:
        handle.write(secrets.token_urlsafe(36) + "\n")
    return destination


def _read_credential(path: Path) -> SecretStr:
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
        raise Conflict("Credential must be a regular private file with mode 0600.")
    if path.stat().st_size > 1024:
        raise Conflict("Credential file exceeds its size limit.")
    value = path.read_text().strip()
    if len(value) < 24:
        raise Conflict("Credential is too short.")
    return SecretStr(value)


def load_credentials(settings: Settings) -> dict[str, tuple[SecretStr, Principal]]:
    credentials: dict[str, tuple[SecretStr, Principal]] = {}
    for role in ROLES:
        path = settings.state_path / f"{role}.token"
        if path.exists() or path.is_symlink():
            credentials[role] = (_read_credential(path), Principal(id=f"local-{role}", role=role))
    if settings.admin_token is not None:
        credentials["admin"] = (settings.admin_token, Principal(id="local-admin", role="admin"))
    if "admin" not in credentials:
        raise Conflict("Initialize local authentication before starting the API.")
    return credentials
