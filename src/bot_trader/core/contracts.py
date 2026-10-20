"""Immutable versioned domain records; money is never implicitly USD stablecoin parity."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, JsonValue, model_validator


def utc_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timestamp must be timezone-aware.")
    return value.astimezone(UTC)


UTCDateTime = Annotated[datetime, AfterValidator(utc_time)]
Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
Currency = Annotated[str, Field(min_length=2, max_length=16, pattern=r"^[A-Z0-9]+$")]
FiniteDecimal = Annotated[Decimal, Field(allow_inf_nan=False)]
PositiveDecimal = Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]
NonnegativeDecimal = Annotated[Decimal, Field(ge=0, allow_inf_nan=False)]
Partition = Literal["development", "validation", "final"]


class FrozenContract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)
    schema_version: Literal[1] = 1


class VersionedReference(FrozenContract):
    """Provider-independent reference to one immutable catalog record."""

    kind: Identifier
    id: Identifier
    version: int = Field(ge=1)
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")


class Instrument(FrozenContract):
    id: Identifier
    venue: Identifier = "synthetic"
    base_currency: Currency
    quote_currency: Currency = "USD"
    product: Literal["spot", "future", "perpetual", "option"] = "spot"
    synthetic: Literal[True] = True


class MarketBar(FrozenContract):
    instrument: Identifier
    event_time: UTCDateTime
    published_at: UTCDateTime | None = None
    provider_available_at: UTCDateTime | None = None
    received_at: UTCDateTime
    transformed_at: UTCDateTime | None = None
    open: PositiveDecimal
    high: PositiveDecimal
    low: PositiveDecimal
    close: PositiveDecimal
    volume: NonnegativeDecimal
    quote_currency: Currency = "USD"
    interval_seconds: int = Field(gt=0, le=31_536_000)

    @model_validator(mode="after")
    def validate_bar(self) -> Self:
        times = [
            self.event_time,
            self.published_at,
            self.provider_available_at,
            self.received_at,
            self.transformed_at,
        ]
        known = [value for value in times if value is not None]
        if any(later < earlier for earlier, later in zip(known, known[1:], strict=False)):
            raise ValueError("Known timestamps must follow availability order.")
        if self.low > min(self.open, self.close) or self.high < max(self.open, self.close):
            raise ValueError("OHLC prices are inconsistent.")
        return self


class DatasetSpec(FrozenContract):
    mode: Literal["technical"] = "technical"
    synthetic: Literal[True] = True
    instrument: Identifier = "SYNTH-USD"
    seed: int = Field(default=42, ge=0, le=2**32 - 1)
    rows: int = Field(default=120, ge=2, le=10_000)
    interval_seconds: int = Field(default=60, ge=1, le=31_536_000)
    partition: Partition = "development"
    start: UTCDateTime = datetime(2020, 1, 1, tzinfo=UTC)
    quote_currency: Currency = "USD"


class SourceReference(FrozenContract):
    id: Identifier
    title: str = Field(min_length=1, max_length=1000)
    url: str | None = Field(default=None, max_length=2048)
    content_hash: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    accessed_at: UTCDateTime | None = None
    access_level: Literal["full", "partial", "metadata", "internal"] = "metadata"


class Signal(FrozenContract):
    instrument: Identifier
    observed_at: UTCDateTime
    decided_at: UTCDateTime
    target_quantity: FiniteDecimal

    @model_validator(mode="after")
    def validate_time(self) -> Self:
        if self.decided_at < self.observed_at:
            raise ValueError("Decision cannot precede observation.")
        return self


class Order(FrozenContract):
    id: Identifier
    instrument: Identifier
    side: Literal["buy", "sell"]
    quantity: PositiveDecimal
    decided_at: UTCDateTime
    submitted_at: UTCDateTime
    mode: Literal["technical"] = "technical"

    @model_validator(mode="after")
    def validate_time(self) -> Self:
        if self.submitted_at < self.decided_at:
            raise ValueError("Submission cannot precede decision.")
        return self


class Fill(FrozenContract):
    order_id: Identifier
    instrument: Identifier
    side: Literal["buy", "sell"]
    quantity: PositiveDecimal
    price: PositiveDecimal
    fee: NonnegativeDecimal
    quote_currency: Currency = "USD"
    filled_at: UTCDateTime
    mode: Literal["technical"] = "technical"


class Position(FrozenContract):
    instrument: Identifier
    quantity: FiniteDecimal


class Portfolio(FrozenContract):
    currency: Currency = "USD"
    cash: FiniteDecimal
    positions: tuple[Position, ...] = ()
    valued_at: UTCDateTime


class Principal(FrozenContract):
    id: Identifier
    role: Literal["admin", "researcher", "viewer", "agent"]


class ModuleManifest(FrozenContract):
    id: Identifier
    version: str = Field(min_length=1, max_length=64)
    dependencies: tuple[Identifier, ...] = ()
    capabilities: tuple[Identifier, ...] = ()
    status: Literal["operational", "prepared", "planned"]
    description: str = Field(default="", max_length=2000)


class Event(FrozenContract):
    kind: Identifier
    occurred_at: UTCDateTime
    payload: dict[str, JsonValue] = Field(default_factory=dict)
