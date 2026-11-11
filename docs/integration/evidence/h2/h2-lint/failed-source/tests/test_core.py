from collections.abc import Sequence
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from bot_trader.core.contracts import DatasetSpec, Event, MarketBar, ModuleManifest, Principal
from bot_trader.core.errors import AccessDenied, Conflict
from bot_trader.core.ports import Transformation
from bot_trader.core.registry import EventBus, Registry
from bot_trader.core.security import Policy
from bot_trader.core.settings import Settings


def bar(**overrides: object) -> MarketBar:
    values: dict[str, object] = {
        "instrument": "SYNTH-USD",
        "event_time": datetime(2020, 1, 1, tzinfo=UTC),
        "received_at": datetime(2020, 1, 1, tzinfo=UTC),
        "open": "10",
        "high": "12",
        "low": "9",
        "close": "11",
        "volume": "1",
        "interval_seconds": 60,
    }
    return MarketBar.model_validate(values | overrides)


def test_time_availability_and_finite_currency_contracts() -> None:
    value = bar(received_at=datetime(2020, 1, 1, 2, tzinfo=timezone(timedelta(hours=2))))
    assert value.received_at == value.event_time
    assert value.received_at.tzinfo is UTC
    assert bar(quote_currency="USDT").quote_currency != bar().quote_currency
    assert value.provider_available_at is None
    for invalid in (
        {"received_at": datetime(2020, 1, 1)},
        {"received_at": datetime(2019, 1, 1, tzinfo=UTC)},
        {"provider_available_at": datetime(2020, 1, 2, tzinfo=UTC)},
        {"open": "NaN"},
        {"volume": "Infinity"},
        {"high": "10"},
        {"interval_seconds": 0},
        {"volume": "-1"},
        {"unexpected": 1},
    ):
        with pytest.raises(ValidationError):
            bar(**invalid)
    with pytest.raises(ValidationError):
        value.close = Decimal("20")


def test_configuration_cannot_enable_live_or_unbounded_fixtures() -> None:
    for invalid in (
        {"mode": "live"},
        {"max_dataset_rows": 1_000_000},
        {"environment": "production"},
        {"admin_token": "short"},
    ):
        with pytest.raises(ValidationError):
            Settings.model_validate(invalid)
    for invalid in ({"mode": "paper"}, {"rows": 10_001}, {"synthetic": False}):
        with pytest.raises(ValidationError):
            DatasetSpec.model_validate(invalid)


def test_explicit_host_origin_and_tls_configuration() -> None:
    settings = Settings()
    assert settings.allowed_hosts == ("localhost", "127.0.0.1")
    assert "http://localhost:8000" in settings.allowed_origins
    for invalid in (
        {"allowed_hosts": ("*",)},
        {"allowed_hosts": ("localhost:8000",)},
        {"allowed_origins": ("http://localhost:8000/path",)},
        {"allowed_origins": ("http://user:password@localhost:8000",)},
        {"allowed_origins": ("http://localhost:65536",)},
        {"allowed_origins": ("http://localhost:8000?",)},
        {"allowed_origins": ("http://untrusted.example:8000",)},
        {"environment": "production", "secure_cookies": True},
    ):
        with pytest.raises(ValidationError):
            Settings.model_validate(invalid)
    secure = Settings(
        environment="production",
        secure_cookies=True,
        allowed_hosts=("platform.example",),
        allowed_origins=("https://platform.example",),
    )
    assert secure.secure_cookies


@pytest.mark.parametrize("role", ["admin", "researcher", "viewer", "agent"])
def test_every_role_denied_reserved_payload_and_financial_actions(role: str) -> None:
    principal = Principal.model_validate({"id": "test", "role": role})
    for action, partition, mode in (
        ("datasets.payload", "final", "technical"),
        ("runs.create", "final", "technical"),
        ("orders.create", None, "technical"),
        ("metadata.read", None, "paper"),
        ("metadata.read", None, "live"),
        ("financial.train", None, "technical"),
    ):
        with pytest.raises(AccessDenied):
            Policy().require(principal, action, partition=partition, mode=mode)  # type: ignore[arg-type]
    Policy().require(principal, "metadata.read", partition="final")


def test_role_scope_is_enforced_without_ui() -> None:
    with pytest.raises(AccessDenied):
        Policy().require(Principal(id="agent", role="agent"), "runs.create")
    with pytest.raises(AccessDenied):
        Policy().require(Principal(id="viewer", role="viewer"), "datasets.create")
    Policy().require(Principal(id="researcher", role="researcher"), "runs.create")


def test_a_add_module_and_b_extend_internal_capability() -> None:
    registry = Registry()
    registry.register(ModuleManifest(id="core", version="1", status="operational"))
    registry.add_capability("core", "echo", lambda value: value)
    registry.register(
        ModuleManifest(id="extension", version="1", dependencies=("core",), status="operational")
    )
    registry.add_capability("extension", "label", lambda value: {"label": value["name"]})
    assert registry.call("extension", "label", {"name": "synthetic"}) == {"label": "synthetic"}
    registry.add_capability("core", "optional", lambda value: [value["value"]])
    assert registry.call("core", "optional", {"value": 5}) == [5]
    assert registry.call("core", "echo", {"unchanged": True}) == {"unchanged": True}
    assert [module.id for module in registry.list()] == ["core", "extension"]
    with pytest.raises(Conflict):
        registry.register(ModuleManifest(id="core", version="2", status="operational"))
    with pytest.raises(Conflict):
        registry.add_capability("core", "echo", lambda value: value)


def test_registry_rejects_missing_cycles_and_prepared_execution() -> None:
    registry = Registry()
    registry.register(
        ModuleManifest(id="one", version="1", dependencies=("two",), status="prepared")
    )
    with pytest.raises(Conflict, match="missing"):
        registry.validate()
    registry.register(
        ModuleManifest(id="two", version="1", dependencies=("one",), status="prepared")
    )
    with pytest.raises(Conflict, match="cycle"):
        registry.validate()
    with pytest.raises(Conflict, match="Inactive"):
        registry.add_capability("one", "forbidden", lambda value: value)


class CloseProjection:
    def transform(self, bars: Sequence[MarketBar]) -> tuple[Decimal, ...]:
        return tuple(value.close for value in bars)


class BufferedProjection:
    def transform(self, bars: Sequence[MarketBar]) -> tuple[Decimal, ...]:
        buffer: list[Decimal] = []
        for value in bars:
            buffer.append(value.close)
        return tuple(buffer)


@pytest.mark.parametrize("implementation", [CloseProjection(), BufferedProjection()])
def test_c_same_consumer_with_two_contract_implementations(implementation: Transformation) -> None:
    source = [bar(), bar(close="10")]
    assert implementation.transform(source) == (Decimal("11"), Decimal("10"))
    assert implementation.transform(()) == ()
    assert source[0].close == Decimal("11")


def test_typed_event_bus_distributes_only_subscribed_events() -> None:
    events: list[Event] = []
    bus = EventBus()
    bus.subscribe("completed", events.append)
    event = Event(kind="completed", occurred_at=datetime.now(UTC), payload={"technical": True})
    bus.publish(Event(kind="unrelated", occurred_at=datetime.now(UTC)))
    bus.publish(event)
    assert events == [event]
