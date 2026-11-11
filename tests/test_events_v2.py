from datetime import UTC, datetime, timedelta

import pytest

from bot_trader.core.contracts import MarketBar
from bot_trader.core.events import (
    MarketEventV2,
    datetime_ns,
    exact_ns,
    from_v1,
    ns_datetime,
    to_v1,
)
from bot_trader.market_data.normalization import exact_json


def legacy(**overrides):
    close = datetime(2020, 1, 1, 0, 1, tzinfo=UTC)
    fields = dict(
        instrument="SYNTH-USD",
        event_time=close,
        received_at=close + timedelta(milliseconds=700),
        open="100",
        high="101",
        low="99",
        close="100.5",
        volume="2",
        interval_seconds=60,
    )
    return MarketBar(**(fields | overrides))


@pytest.mark.parametrize("provider", [None, datetime(2020, 1, 1, 0, 1, tzinfo=UTC)])
def test_additive_v1_exact_compatibility(provider):
    old = legacy(provider_available_at=provider, quote_currency="USDT")
    new = from_v1(old, label="close", event_id="bar-1", raw_sha256="a" * 64)
    assert to_v1(new) == old
    assert new.engine_ts_init_ns is None
    assert new.effective_ns == datetime_ns(old.received_at)
    assert new.data.start_ns == new.event_ns - 60_000_000_000


def test_precision_and_incompatible_timestamps_fail_explicitly():
    old = legacy()
    event = from_v1(old, label="close", event_id="bar-1", raw_sha256="a" * 64)
    fields = event.model_dump(mode="json")
    fields["received_ns"] += 1
    fractional = MarketEventV2.model_validate(fields)
    assert fractional.received_ns % 1000 == 1
    with pytest.raises(ValueError, match="submicrosecond"):
        to_v1(fractional)
    for value in [True, 1.0, "1", -1, 2**64]:
        with pytest.raises(ValueError):
            exact_ns(value)
        with pytest.raises(ValueError):
            MarketEventV2.model_validate(fields | {"available_ns": value})
    assert exact_ns(1, "ms") == 1_000_000
    assert ns_datetime(datetime_ns(old.event_time)) == old.event_time


def test_open_label_requires_actual_close_availability():
    old = legacy()
    with pytest.raises(ValueError, match="complete bar"):
        from_v1(old, label="open", event_id="bad", raw_sha256="a" * 64)
    available = old.event_time + timedelta(seconds=60)
    old = legacy(provider_available_at=available, received_at=available)
    event = from_v1(old, label="open", event_id="ok", raw_sha256="a" * 64)
    assert event.event_ns < event.available_ns == event.data.end_ns
    assert to_v1(event) == old
    fields = event.model_dump(mode="json")
    with pytest.raises(ValueError, match="initialization"):
        MarketEventV2.model_validate(fields | {"engine_ts_init_ns": event.event_ns})


def test_immutable_payload_and_ambiguous_json():
    event = from_v1(legacy(), label="close", event_id="one", raw_sha256="a" * 64)
    digest = event.digest
    with pytest.raises(ValueError):
        event.data.close = "42"
    assert digest == event.digest
    for raw in [b'{"x":1,"x":2}', b'{"price":100.1}', b'{"price":NaN}']:
        with pytest.raises(ValueError):
            exact_json(raw)
