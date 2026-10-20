"""Explicit trusted dependency composition, shared by HTTP and the finite worker."""

from dataclasses import dataclass

from bot_trader.core.contracts import ModuleManifest
from bot_trader.core.registry import Registry
from bot_trader.core.security import Policy
from bot_trader.core.settings import Settings
from bot_trader.lab import HypothesisService, LabService
from bot_trader.market_data import DatasetService, LocalArtifactStore
from bot_trader.persistence import Database, Repository


@dataclass
class Services:
    settings: Settings
    database: Database
    repository: Repository
    policy: Policy
    modules: Registry
    datasets: DatasetService
    lab: LabService
    hypotheses: HypothesisService


def build_registry() -> Registry:
    registry = Registry()
    definitions = [
        ("core", "operational", (), "Typed contracts, policy, configuration and module registry."),
        ("market-data", "operational", ("core",), "Synthetic catalog, provenance and validation."),
        (
            "research-lab",
            "operational",
            ("market-data",),
            "Hypotheses and synthetic technical lab.",
        ),
        ("ml-models", "prepared", ("core",), "Model interfaces; no financial training adapter."),
        (
            "experiments",
            "operational",
            ("research-lab",),
            "Durable technical attempts and provenance.",
        ),
        ("backtesting", "prepared", ("core",), "Bounded synthetic ledger; no financial engine."),
        ("paper-trading", "planned", ("core",), "First-class future module; no market connection."),
        ("trading-engine", "planned", ("core",), "Inactive; no order transport or exchange keys."),
        ("risk", "prepared", ("core",), "Risk contract and synthetic cash/inventory checks only."),
        ("portfolio", "prepared", ("core",), "Position/portfolio contracts; no return analytics."),
        ("charting", "prepared", ("market-data",), "Renderer integration under verification."),
        ("news", "planned", ("core",), "No feed or sentiment execution implemented."),
        (
            "ai-researcher",
            "prepared",
            ("research-lab",),
            "Inert proposals only; no autonomous tools.",
        ),
        ("alerts", "prepared", ("core",), "Local audit; external notifications are future work."),
        ("web", "prepared", ("core",), "Authenticated same-origin interface integration."),
    ]
    for identifier, status, dependencies, description in definitions:
        registry.register(
            ModuleManifest.model_validate(
                {
                    "id": identifier,
                    "version": "0.1.0",
                    "status": status,
                    "dependencies": dependencies,
                    "description": description,
                }
            )
        )
    registry.add_capability("core", "runtime-status", lambda _: {"mode": "technical"})
    registry.validate()
    return registry


def build_services(settings: Settings) -> Services:
    database = Database(settings)
    repo = Repository(database)
    policy = Policy()
    store = LocalArtifactStore(settings.state_path / "artifacts", settings.max_artifact_bytes)
    datasets = DatasetService(repo, store, policy, settings)
    return Services(
        settings,
        database,
        repo,
        policy,
        build_registry(),
        datasets,
        LabService(repo, datasets, store, policy, settings),
        HypothesisService(repo, policy),
    )
