"""Bounded synthetic accounting checks, never a financial backtesting engine."""

from .ledger import (
    ClosePriceExecution,
    ProportionalCost,
    SyntheticSpotLedger,
    TechnicalSpotRisk,
    run_technical_ledger,
)

__all__ = [
    "ClosePriceExecution",
    "ProportionalCost",
    "SyntheticSpotLedger",
    "TechnicalSpotRisk",
    "run_technical_ledger",
]
