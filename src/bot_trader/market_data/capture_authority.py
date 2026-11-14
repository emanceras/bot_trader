"""Finite data-pilot configuration and recorded user approval; neither is a credential."""

from typing import Literal

from pydantic import Field

from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import Digest, ImmutableV2, Nanoseconds, content_hash
from bot_trader.market_data.capture import CaptureLimits


class PilotConfiguration(ImmutableV2):
    version: Literal["kraken-public-pilot-v1"] = "kraken-public-pilot-v1"
    mode: Literal["public_data_qa"] = "public_data_qa"
    synthetic: Literal[False] = False
    symbol: Literal["BTC/EUR"] = "BTC/EUR"
    endpoint: Literal["wss://ws.kraken.com/v2"] = "wss://ws.kraken.com/v2"
    partition: Literal["development"] = "development"
    max_duration_ns: int = Field(
        default=300_000_000_000, strict=True, ge=300_000_000_000, le=600_000_000_000
    )
    receive_timeout_ns: int = Field(default=1_000_000_000, strict=True, gt=0, le=2_000_000_000)
    handshake_timeout_ns: int = Field(default=15_000_000_000, strict=True, gt=0, le=30_000_000_000)
    idle_timeout_ns: int = Field(default=15_000_000_000, strict=True, gt=0, le=30_000_000_000)
    max_reconnects: int = Field(default=2, strict=True, ge=0, le=5)
    reconnect_delay_ns: int = Field(default=5_000_000_000, strict=True, gt=0, le=10_000_000_000)
    max_market_rows: int = Field(default=8000, strict=True, ge=1, le=9000)
    rights_reference: str = Field(min_length=1, max_length=1024)
    limits: CaptureLimits = CaptureLimits(
        max_frames=10_000,
        max_records=20_000,
        max_total_bytes=67_108_864,
        min_free_disk_bytes=134_217_728,
    )

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


class PilotApproval(ImmutableV2):
    version: Literal["public-capture-approval-v1"] = "public-capture-approval-v1"
    approved: bool = Field(default=False, strict=True)
    purpose: Literal["public_data_qa"] = "public_data_qa"
    capture_id: str = Field(min_length=1, max_length=64)
    config_hash: Digest
    approved_by: str = Field(min_length=1, max_length=200)
    decision_reference: str = Field(min_length=1, max_length=1024)
    rights_reference: str = Field(min_length=1, max_length=1024)
    host_id: str = Field(min_length=1, max_length=255)
    not_before_ns: Nanoseconds
    expires_ns: Nanoseconds

    def require(
        self, capture_id: str, config: PilotConfiguration, now_ns: int, host_id: str
    ) -> None:
        approval = PilotApproval.model_validate(self.model_dump())
        if (
            not approval.approved
            or approval.capture_id != capture_id
            or approval.config_hash != config.digest
            or approval.host_id != host_id
            or approval.rights_reference != config.rights_reference
            or not approval.not_before_ns <= now_ns
            or now_ns + config.max_duration_ns + 15_000_000_000 > approval.expires_ns
        ):
            raise AccessDenied(
                "A matching, current user approval for this finite public pilot is required."
            )
