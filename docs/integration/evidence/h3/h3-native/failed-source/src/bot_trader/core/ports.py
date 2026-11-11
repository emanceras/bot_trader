"""Small replaceable contracts; prepared ports do not imply operational adapters."""

from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol

from .contracts import Fill, MarketBar, Order, Portfolio, Signal


class Transformation(Protocol):
    def transform(self, bars: Sequence[MarketBar]) -> tuple[Decimal, ...]: ...


class Model(Protocol):
    def fit(self, features: Sequence[tuple[Decimal, ...]], targets: Sequence[Decimal]) -> None: ...
    def predict(self, features: Sequence[tuple[Decimal, ...]]) -> tuple[Decimal, ...]: ...


class Strategy(Protocol):
    def decide(self, bars: Sequence[MarketBar], portfolio: Portfolio) -> Signal: ...


class Cost(Protocol):
    def calculate(self, order: Order, price: Decimal) -> Decimal: ...


class Execution(Protocol):
    def execute(self, order: Order, observation: MarketBar) -> Fill: ...


class Risk(Protocol):
    def check(self, order: Order, portfolio: Portfolio) -> None: ...


class FinancingMargin(Protocol):
    def required_margin(self, order: Order, price: Decimal) -> Decimal: ...
    def financing_cost(self, portfolio: Portfolio, elapsed_seconds: int) -> Decimal: ...
