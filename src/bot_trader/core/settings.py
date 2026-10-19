"""Bounded process configuration. Runtime modes cannot enable market execution."""

import re
from pathlib import Path
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOT_TRADER_", extra="forbid", frozen=True)
    mode: Literal["technical"] = "technical"
    environment: Literal["development", "production"] = "development"
    repository_root: Path = Field(default_factory=Path.cwd)
    data_dir: Path = Path(".state")
    admin_token: SecretStr | None = None
    allowed_hosts: tuple[str, ...] = ("localhost", "127.0.0.1")
    allowed_origins: tuple[str, ...] = ("http://localhost:8000", "http://127.0.0.1:8000")
    secure_cookies: bool = False
    session_ttl_seconds: int = Field(default=3600, ge=60, le=86400)
    max_dataset_rows: int = Field(default=10_000, ge=2, le=10_000)
    max_request_bytes: int = Field(default=65_536, ge=1024, le=1_048_576)
    max_artifact_bytes: int = Field(default=10_485_760, ge=1024, le=104_857_600)
    max_queued_runs: int = Field(default=100, ge=1, le=1000)

    @field_validator("allowed_hosts")
    @classmethod
    def validate_hosts(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if not values or len(values) > 20:
            raise ValueError("Configure between one and twenty explicit allowed hosts.")
        for value in values:
            if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?", value):
                raise ValueError(
                    "Allowed hosts must be explicit lowercase hostnames or IPv4 addresses."
                )
            if ".." in value:
                raise ValueError("Allowed hosts cannot contain empty labels.")
        return tuple(dict.fromkeys(values))

    @field_validator("allowed_origins")
    @classmethod
    def validate_origins(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if not values or len(values) > 20:
            raise ValueError("Configure between one and twenty explicit allowed origins.")
        for value in values:
            parsed = urlsplit(value)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path
                or parsed.query
                or parsed.fragment
                or value != f"{parsed.scheme}://{parsed.netloc}"
                or parsed.hostname != parsed.hostname.lower()
                or "*" in parsed.netloc
            ):
                raise ValueError(
                    "Origins must contain only an explicit HTTP(S) scheme, host and port."
                )
            # Accessing port validates its syntax and range.
            _ = parsed.port
        return tuple(dict.fromkeys(values))

    @model_validator(mode="after")
    def validate_deployment(self) -> Self:
        if self.environment == "production" and not self.secure_cookies:
            raise ValueError("Non-development deployments require secure cookies and external TLS.")
        if any(
            urlsplit(origin).hostname not in self.allowed_hosts for origin in self.allowed_origins
        ):
            raise ValueError("Every allowed origin must use an allowed host.")
        if self.environment == "production" and any(
            urlsplit(origin).scheme != "https" for origin in self.allowed_origins
        ):
            raise ValueError("Non-development deployments require HTTPS origins.")
        if self.admin_token is not None and len(self.admin_token.get_secret_value()) < 24:
            raise ValueError("Local authentication token must contain at least 24 characters.")
        return self

    @property
    def state_path(self) -> Path:
        return (self.repository_root / self.data_dir).resolve()

    @property
    def database_path(self) -> Path:
        return self.state_path / "metadata.sqlite3"
