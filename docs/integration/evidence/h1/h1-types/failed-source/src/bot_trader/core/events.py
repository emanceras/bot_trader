"""Additive exact-time v2 records. Existing datetime/v1 contracts remain unchanged."""

import hashlib
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from bot_trader.core.contracts import Currency, Identifier, MarketBar

Nanoseconds = Annotated[int, Field(strict=True, ge=0, le=2**64 - 1)]
SequenceNumber = Annotated[int, Field(strict=True, ge=1)]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Unit = Literal["s", "ms", "us", "ns"]
_UNITS = {"s": 1_000_000_000, "ms": 1_000_000, "us": 1000, "ns": 1}
_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


def exact_ns(value: int, unit: Unit = "ns") -> int:
    if type(value) is not int or unit not in _UNITS:
        raise ValueError("Timestamps require exact integer ticks and an explicit supported unit.")
    result = value * _UNITS[unit]
    if not 0 <= result < 2**64:
        raise ValueError("Timestamp is outside the unsigned nanosecond range.")
    return result


def datetime_ns(value: datetime) -> int:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Naive timestamps have no supported timezone interpretation.")
    delta = value.astimezone(UTC) - _EPOCH
    return exact_ns((delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds, "us")


def ns_datetime(value: int) -> datetime:
    value = exact_ns(value)
    if value % 1000:
        raise ValueError("v1 datetime cannot preserve submicrosecond precision.")
    return _EPOCH + timedelta(microseconds=value // 1000)


def canonical_bytes(value: object) -> bytes:
    """Only JSON-compatible values; non-finite JSON numbers are forbidden."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def content_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def decimal_text(value: object, *, positive: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError("Decimal input must be a string, never a binary float.")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError("Invalid decimal string.") from error
    if not number.is_finite() or number < 0 or (positive and number == 0):
        raise ValueError("Unsupported non-finite or negative market value.")
    # Fixed-point serialization without ambient Decimal-context rounding.
    result = format(number, "f")
    if "." in result:
        result = result.rstrip("0").rstrip(".")
    return result if number else "0"


class ImmutableV2(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)


class TradeData(ImmutableV2):
    kind: Literal["trade"] = "trade"
    price: str
    quantity: str

    @field_validator("price", "quantity", mode="before")
    @classmethod
    def numbers(cls, value: object) -> str:
        return decimal_text(value, positive=True)


class BarData(ImmutableV2):
    kind: Literal["bar"] = "bar"
    bar_id: Identifier
    start_ns: Nanoseconds
    end_ns: Nanoseconds
    status: Literal["open", "closed", "corrected"]
    label: Literal["open", "close"]
    open: str
    high: str
    low: str
    close: str
    volume: str
    revision_of: Identifier | None = None

    @field_validator("open", "high", "low", "close", mode="before")
    @classmethod
    def prices(cls, value: object) -> str:
        return decimal_text(value, positive=True)

    @field_validator("volume", mode="before")
    @classmethod
    def volumes(cls, value: object) -> str:
        return decimal_text(value)

    @model_validator(mode="after")
    def consistent(self) -> Self:
        if self.end_ns <= self.start_ns:
            raise ValueError("Bar interval must be nonempty.")
        if Decimal(self.low) > min(Decimal(self.open), Decimal(self.close)) or Decimal(
            self.high
        ) < max(Decimal(self.open), Decimal(self.close)):
            raise ValueError("Inconsistent OHLC.")
        if (self.status == "corrected") != (self.revision_of is not None):
            raise ValueError("Corrections require an explicit predecessor event identity.")
        return self


class Level(ImmutableV2):
    price: str
    quantity: str

    @field_validator("price", "quantity", mode="before")
    @classmethod
    def numbers(cls, value: object) -> str:
        return decimal_text(value, positive=True)


class QuoteData(ImmutableV2):
    kind: Literal["quote"] = "quote"
    origin: Literal["synthetic_explicit", "ohlc_assumption", "observed"]
    bids: tuple[Level, ...] = Field(min_length=1, max_length=100)
    asks: tuple[Level, ...] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def consistent(self) -> Self:
        bids = [Decimal(level.price) for level in self.bids]
        asks = [Decimal(level.price) for level in self.asks]
        if bids != sorted(set(bids), reverse=True) or asks != sorted(set(asks)):
            raise ValueError("Depth must have unique ordered price levels.")
        if bids[0] >= asks[0]:
            raise ValueError("Crossed/locked quotes are unsupported in this technical contract.")
        return self


Payload = Annotated[TradeData | BarData | QuoteData, Field(discriminator="kind")]


class MarketEventV2(ImmutableV2):
    schema_version: Literal[2] = 2
    event_id: Identifier
    source_id: Identifier
    source_version: Identifier
    stream_id: Identifier
    sequence: SequenceNumber
    instrument: Identifier
    quote_currency: Currency = "USD"
    original_tick: Nanoseconds
    original_unit: Unit
    event_ns: Nanoseconds
    available_ns: Nanoseconds
    received_ns: Nanoseconds | None = None
    published_ns: Nanoseconds | None = None
    provider_available_ns: Nanoseconds | None = None
    transformed_ns: Nanoseconds | None = None
    engine_ts_init_ns: Nanoseconds | None = None
    raw_sha256: Digest
    data: Payload

    @property
    def effective_ns(self) -> int:
        return max(self.available_ns, self.received_ns or 0, self.transformed_ns or 0)

    @property
    def identity(self) -> tuple[str, str, str]:
        return self.source_id, self.stream_id, self.event_id

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))

    @model_validator(mode="after")
    def causal(self) -> Self:
        if exact_ns(self.original_tick, self.original_unit) != self.event_ns:
            raise ValueError("Original ticks and normalized event time disagree.")
        if self.available_ns < self.event_ns:
            raise ValueError("Market observation availability precedes its event.")
        if self.published_ns is not None and self.available_ns < self.published_ns:
            raise ValueError("Availability precedes known publication.")
        if (
            self.provider_available_ns is not None
            and self.available_ns < self.provider_available_ns
        ):
            raise ValueError("Effective source availability precedes the provider clock.")
        if self.received_ns is not None and self.received_ns < self.available_ns:
            raise ValueError("Reception precedes declared availability.")
        if self.transformed_ns is not None and self.transformed_ns < max(
            self.available_ns, self.received_ns or 0
        ):
            raise ValueError("Transformation precedes source availability/reception.")
        if self.engine_ts_init_ns is not None and self.engine_ts_init_ns < self.effective_ns:
            raise ValueError("Engine initialization precedes effective information availability.")
        if isinstance(self.data, BarData):
            label = self.data.start_ns if self.data.label == "open" else self.data.end_ns
            if self.event_ns != label:
                raise ValueError("Bar event time disagrees with its explicit label convention.")
            if self.data.status != "open" and self.available_ns < self.data.end_ns:
                raise ValueError("A complete bar cannot be available before interval end.")
        return self


def from_v1(
    bar: MarketBar,
    *,
    label: Literal["open", "close"],
    event_id: str,
    raw_sha256: str,
    sequence: int = 1,
) -> MarketEventV2:
    event = datetime_ns(bar.event_time)
    duration = bar.interval_seconds * 1_000_000_000
    start, end = (event, event + duration) if label == "open" else (event - duration, event)
    publication = None if bar.published_at is None else datetime_ns(bar.published_at)
    provider = None if bar.provider_available_at is None else datetime_ns(bar.provider_available_at)
    return MarketEventV2(
        event_id=event_id,
        source_id="legacy-v1",
        source_version="1",
        stream_id="bars",
        sequence=sequence,
        instrument=bar.instrument,
        quote_currency=bar.quote_currency,
        original_tick=event,
        original_unit="ns",
        event_ns=event,
        available_ns=max(event, publication or 0, provider or 0),
        received_ns=datetime_ns(bar.received_at),
        published_ns=publication,
        provider_available_ns=provider,
        transformed_ns=None if bar.transformed_at is None else datetime_ns(bar.transformed_at),
        raw_sha256=raw_sha256,
        data=BarData(
            bar_id=event_id,
            start_ns=start,
            end_ns=end,
            status="closed",
            label=label,
            open=str(bar.open),
            high=str(bar.high),
            low=str(bar.low),
            close=str(bar.close),
            volume=str(bar.volume),
        ),
    )


def to_v1(event: MarketEventV2) -> MarketBar:
    data = event.data
    if not isinstance(data, BarData) or data.status != "closed" or event.received_ns is None:
        raise ValueError("v1 requires a closed bar and known reception; revisions are not v1.")
    duration = data.end_ns - data.start_ns
    if duration % 1_000_000_000:
        raise ValueError("v1 cannot represent a fractional-second interval.")
    # Check all clocks, including boundaries not otherwise represented by v1.
    for clock in (
        event.event_ns,
        event.available_ns,
        event.received_ns,
        data.start_ns,
        data.end_ns,
        event.published_ns,
        event.provider_available_ns,
        event.transformed_ns,
        event.engine_ts_init_ns,
    ):
        if clock is not None:
            ns_datetime(clock)
    return MarketBar(
        instrument=event.instrument,
        event_time=ns_datetime(event.event_ns),
        published_at=None if event.published_ns is None else ns_datetime(event.published_ns),
        provider_available_at=(
            None
            if event.provider_available_ns is None
            else ns_datetime(event.provider_available_ns)
        ),
        received_at=ns_datetime(event.received_ns),
        transformed_at=None if event.transformed_ns is None else ns_datetime(event.transformed_ns),
        open=Decimal(data.open),
        high=Decimal(data.high),
        low=Decimal(data.low),
        close=Decimal(data.close),
        volume=Decimal(data.volume),
        interval_seconds=duration // 10**9,
        quote_currency=event.quote_currency,
    )
