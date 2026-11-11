"""One integrated technical path, composed from existing storage and permission ports."""

from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, JsonValue, field_validator

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import AccessDenied
from bot_trader.core.events import (
    ImmutableV2,
    Nanoseconds,
    QuoteData,
    canonical_bytes,
    content_hash,
    decimal_text,
)
from bot_trader.core.security import Policy
from bot_trader.market_data.archive import ImportProgress, LocalArchive, SourceSpec
from bot_trader.market_data.normalization import (
    FixtureJSONLNormalizer,
    Normalizer,
    store_normalized,
)
from bot_trader.market_data.replay import MarketReplay, ReplayPolicy, ReplayResult
from bot_trader.market_data.storage import ArtifactStore
from bot_trader.simulation.bridge import SliceExecution
from bot_trader.simulation.reconciliation import reconcile


class ExecutionAssumptions(ImmutableV2):
    version: Literal["slice-execution-v1"] = "slice-execution-v1"
    fee_rate: str = "0.002"
    slippage_usd: Literal["0"] = "0"
    latency_ns: Nanoseconds = Field(default=0, le=0)
    max_quote_age_ns: Nanoseconds = 1_000_000
    cancel_remainder_on_next_quote: Literal[True] = True
    quote_model: Literal["explicit_synthetic_depth"] = "explicit_synthetic_depth"

    @field_validator("fee_rate", mode="before")
    @classmethod
    def fees(cls, value: object) -> str:
        text = decimal_text(value)
        if Decimal(text) > 1:
            raise ValueError("Synthetic fee fraction cannot exceed one.")
        return text


class SliceConfiguration(ImmutableV2):
    schema_version: Literal[1] = 1
    mode: Literal["technical"] = "technical"
    synthetic: Literal[True] = True
    partition: Literal["development"] = "development"
    initial_cash_usd: str = "1000"
    replay: ReplayPolicy = ReplayPolicy(complete_trade_coverage=True)
    execution: ExecutionAssumptions = ExecutionAssumptions()

    @field_validator("initial_cash_usd", mode="before")
    @classmethod
    def cash(cls, value: object) -> str:
        return decimal_text(value)


def execution_request(replay: ReplayResult, config: SliceConfiguration) -> dict[str, Any]:
    """Bind intentions to later eligible inputs; matching remains the engine's job."""
    quotes: list[dict[str, Any]] = []
    for event in replay.quotes:
        data = event.data
        if (
            event.instrument != "SYNTH-USD"
            or event.quote_currency != "USD"
            or (not isinstance(data, QuoteData) or data.origin != "synthetic_explicit")
        ):
            raise ValueError(
                "First slice execution admits only explicit synthetic SYNTH-USD depth."
            )
        init = event.effective_ns if event.engine_ts_init_ns is None else event.engine_ts_init_ns
        quotes.append(
            dict(
                id=event.event_id,
                event_ns=event.event_ns,
                available_ns=event.effective_ns,
                engine_init_ns=init,
                source_event_id=event.event_id,
                source_hash=event.digest,
                source_available_ns=event.available_ns,
                source_received_ns=event.received_ns,
                mapping="effective-availability-to-engine-v1",
                bids=[[level.price, level.quantity] for level in data.bids],
                asks=[[level.price, level.quantity] for level in data.asks],
            )
        )
    if not quotes:
        raise ValueError(
            "No explicit executable quote; OHLC is not silently converted to liquidity."
        )
    commands: list[dict[str, Any]] = []
    unexecuted = []
    for signal in replay.signals:
        if signal.instrument != "SYNTH-USD":
            raise ValueError("Signal instrument is not admitted by the synthetic native adapter.")
        eligible = [
            q
            for q in quotes
            if q["event_ns"] >= signal.decision_ns
            and q["available_ns"] >= signal.decision_ns
            and q["engine_init_ns"] > signal.decision_ns
            and q["engine_init_ns"] - q["event_ns"] <= config.execution.max_quote_age_ns
        ]
        if not eligible:
            unexecuted.append(signal.id)
            continue
        quote = eligible[0]
        order = dict(
            id="order-" + signal.id,
            kind="market",
            side=signal.side,
            quantity=signal.quantity,
            signal_id=signal.id,
            decision_ns=signal.decision_ns,
            submitted_ns=quote["engine_init_ns"],
            quote_id=quote["id"],
        )
        commands.append(order)
        later = [
            q
            for q in quotes
            if q["engine_init_ns"] > quote["engine_init_ns"]
            and q["event_ns"] >= quote["engine_init_ns"]
            and q["engine_init_ns"] - q["event_ns"] <= config.execution.max_quote_age_ns
        ]
        if later:
            commands.append(
                dict(
                    id="cancel-" + order["id"],
                    kind="cancel",
                    target=order["id"],
                    signal_id=signal.id,
                    decision_ns=quote["engine_init_ns"],
                    submitted_ns=later[0]["engine_init_ns"],
                    quote_id=later[0]["id"],
                )
            )
    commands.sort(key=lambda c: (c["submitted_ns"], c["kind"] != "cancel", c["id"]))
    return dict(
        schema_version=1,
        mode="technical",
        synthetic=True,
        partition="development",
        instrument="SYNTH-USD",
        initial_cash_usd=config.initial_cash_usd,
        policy=config.execution.model_dump(mode="json"),
        quotes=quotes,
        commands=commands,
        unexecuted_signal_ids=unexecuted,
        replay_checkpoint=replay.checkpoint.model_dump(mode="json"),
    )


class SliceService:
    """Composable application service; same store and role policy as the existing platform."""

    def __init__(
        self, store: ArtifactStore, policy: Policy, normalizer: Normalizer | None = None
    ) -> None:
        self.store = store
        self.policy = policy
        self.archive = LocalArchive(store)
        self.normalizer = normalizer or FixtureJSONLNormalizer()

    def import_file(
        self,
        path: Path,
        source: SourceSpec,
        principal: Principal,
        *,
        checkpoint_hash: str | None = None,
        max_chunks: int = 1000,
    ) -> ImportProgress:
        self.policy.require(principal, "datasets.create", partition=source.partition)
        if source.data_class != "synthetic" or source.partition != "development":
            raise AccessDenied("Only synthetic development archives enter this integration.")
        return self.archive.import_step(
            path, source, checkpoint_hash=checkpoint_hash, max_chunks=max_chunks
        )

    def run(
        self,
        archive_hash: str,
        config: SliceConfiguration,
        principal: Principal,
        *,
        execution: SliceExecution,
        directory: Path,
    ) -> dict[str, JsonValue]:
        config = SliceConfiguration.model_validate(config.model_dump())
        self.policy.require(
            principal, "worker.execute", partition=config.partition, mode=config.mode
        )
        # Metadata/permissions precede raw payload access and subprocess creation.
        metadata, source = self.archive.inspect(archive_hash)
        if source.data_class != "synthetic" or source.partition != "development":
            raise AccessDenied(
                "Market/exposed/reserved archives cannot generate signals or orders."
            )
        _, _, raw = self.archive.read(archive_hash)
        batch = self.normalizer.normalize(raw, source, metadata.source_manifest_hash)
        normalized_hash = store_normalized(batch, self.store)
        replay = MarketReplay(config.replay).run(batch.events, synthetic=True)
        replay_hash = self.store.put(canonical_bytes(replay.model_dump(mode="json")), "json")
        request = execution_request(replay, config)
        request_hash = self.store.put(canonical_bytes(request), "json")
        native = execution.execute(request, directory)
        if native.get("request_hash") != request_hash or native.get("status") != "completed":
            raise ValueError("Execution port returned unbound or incomplete evidence.")
        native_hash = self.store.put(canonical_bytes(native), "json")
        accounting = reconcile(request, native)
        accounting_hash = self.store.put(canonical_bytes(accounting), "json")
        report: dict[str, JsonValue] = dict(
            schema_version=1,
            synthetic=True,
            financial_validation=False,
            status="reconciled" if accounting["passed"] else "unresolved",
            archive_hash=archive_hash,
            raw_sha256=metadata.raw_sha256,
            source_manifest_hash=metadata.source_manifest_hash,
            normalized_hash=normalized_hash,
            replay_hash=replay_hash,
            request_hash=request_hash,
            native_hash=native_hash,
            accounting_hash=accounting_hash,
            configuration=config.model_dump(mode="json"),
            signal_count=len(replay.signals),
            fill_count=len(native.get("fills", [])),
            implementation="integrated-synthetic-slice-v1",
        )
        report["canonical_hash"] = content_hash(report)
        self.store.put(canonical_bytes(report), "json")
        return report
