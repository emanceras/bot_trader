"""Durable finite technical work with provenance and input-lineage authorization."""

from __future__ import annotations

import builtins
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from pydantic import JsonValue
from sqlalchemy import insert, select

from bot_trader.core.contracts import MarketBar, Principal
from bot_trader.core.errors import AccessDenied, Conflict, NotFound, PlatformError
from bot_trader.core.security import Policy
from bot_trader.core.settings import Settings
from bot_trader.persistence import DocumentRecord, Repository, RunRecord
from bot_trader.persistence.repository import canonical_json, content_hash
from bot_trader.persistence.schema import audit, documents
from bot_trader.simulation import run_technical_ledger

from .contracts import ResearchProposal, TechnicalRunSpec
from .provenance import code_identity

# Freeze once per imported process, not once per service or queued attempt.
# This checkout-based release requires a restart after changing executable code.
_LOADED_IDENTITY = code_identity(Path(__file__).resolve().parents[3])
_SOFTWARE_KEYS = ("source_sha256", "uv_lock_sha256", "python", "platform", "machine", "packages")


class ArtifactStore(Protocol):
    def put(self, data: bytes, suffix: str) -> str: ...
    def get(self, digest: str, suffix: str) -> bytes: ...


class DatasetAccess(Protocol):
    def get(self, id: str, principal: Principal, version: int | None = None) -> DocumentRecord: ...
    def bars(
        self, id: str, principal: Principal, version: int | None = None
    ) -> tuple[MarketBar, ...]: ...
    def inspect(
        self, id: str, principal: Principal, version: int | None = None
    ) -> dict[str, JsonValue]: ...
    def transform(
        self, id: str, principal: Principal, version: int | None = None, *, window: int = 5
    ) -> DocumentRecord: ...


def _object(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise Conflict("Stored technical record has an invalid object shape.")
    return value


def _text(value: JsonValue) -> str:
    if not isinstance(value, str):
        raise Conflict("Stored technical record has an invalid identifier.")
    return value


class LabService:
    def __init__(
        self,
        repo: Repository,
        datasets: DatasetAccess,
        store: ArtifactStore,
        policy: Policy,
        settings: Settings,
    ) -> None:
        self.repo, self.datasets, self.store = repo, datasets, store
        self.policy, self.settings = policy, settings

    def _current_identity(self) -> dict[str, JsonValue]:
        current = code_identity(self.settings.repository_root)
        if any(current.get(key) != _LOADED_IDENTITY.get(key) for key in _SOFTWARE_KEYS):
            raise Conflict("Executable source or environment changed; restart API and worker.")
        return current

    def _dataset(self, spec: TechnicalRunSpec, principal: Principal) -> DocumentRecord:
        record = self.repo.get("dataset", spec.dataset_id, spec.dataset_version)
        partition = record.body.get("partition")
        if partition not in {"development", "validation", "final"}:
            raise AccessDenied("Dataset has no authorized partition classification.")
        # Authoritative stored lineage, never a caller-supplied manifest flag.
        if partition == "final":
            raise AccessDenied("Final dataset inputs and all derived run payloads are reserved.")
        if record.body.get("synthetic") is not True or record.body.get("mode") != "technical":
            raise AccessDenied("Only synthetic technical dataset inputs are authorized.")
        self.policy.require(principal, "datasets.payload")
        return record

    def submit(self, spec: TechnicalRunSpec, principal: Principal) -> RunRecord:
        self.policy.require(principal, "runs.create", mode=spec.mode)
        associations = self._hypotheses(spec, principal)
        dataset = self._dataset(spec, principal)
        # Loading verifies persisted file integrity before recording an executable job.
        self.datasets.bars(dataset.id, principal, dataset.version)
        manifest: dict[str, JsonValue] = {
            "protocol_version": 1,
            "mode": "technical",
            "synthetic": True,
            "financial_validation": False,
            "hypotheses": associations,
            "hypothesis_association": "Traceability only; no scientific hypothesis is evaluated.",
            "dataset": {
                "id": dataset.id,
                "version": dataset.version,
                "document_hash": dataset.content_hash,
                "artifact": dataset.body.get("artifact"),
            },
            "code_environment": self._current_identity(),
            "seed": spec.seed,
            "task_implementation_version": 1,
            "seed_usage": "Recorded; fixture randomness belongs to the immutable dataset seed.",
        }
        return self.repo.enqueue(spec.model_dump(mode="json"), manifest, created_by=principal.id)

    def _hypotheses(self, spec: TechnicalRunSpec, principal: Principal) -> builtins.list[JsonValue]:
        result: builtins.list[JsonValue] = []
        for reference in spec.hypotheses:
            self.policy.require(principal, "hypotheses.read")
            record = self.repo.get(reference.kind, reference.id, reference.version)
            if record.content_hash != reference.content_hash:
                raise Conflict("Hypothesis reference does not match its immutable version.")
            result.append(reference.model_dump(mode="json"))
        return result

    def _authorize(self, run: RunRecord, principal: Principal, action: str) -> TechnicalRunSpec:
        self.policy.require(principal, action)
        if (
            content_hash(run.config) != run.config_hash
            or content_hash(run.manifest) != run.manifest_hash
        ):
            raise Conflict("Stored run provenance integrity check failed.")
        spec = TechnicalRunSpec.model_validate(run.config)
        if self._hypotheses(spec, principal) != run.manifest.get("hypotheses", []):
            raise Conflict("Run hypothesis lineage does not match its frozen associations.")
        record = self._dataset(spec, principal)
        lineage = _object(run.manifest.get("dataset"))
        if (
            lineage.get("id") != record.id
            or lineage.get("version") != record.version
            or lineage.get("document_hash") != record.content_hash
            or lineage.get("artifact") != record.body.get("artifact")
        ):
            raise Conflict("Run dataset lineage does not match its immutable input version.")
        if (
            run.manifest.get("mode") != "technical"
            or run.manifest.get("synthetic") is not True
            or run.manifest.get("financial_validation") is not False
        ):
            raise AccessDenied("Only synthetic technical run payloads are authorized.")
        return spec

    def get(self, id: str, principal: Principal) -> RunRecord:
        run = self.repo.get_run(id)
        self._authorize(run, principal, "runs.read")
        return run

    def list(self, principal: Principal, limit: int = 100) -> list[RunRecord]:
        self.policy.require(principal, "runs.read")
        visible = []
        for run in self.repo.list_runs(limit=limit):
            try:
                self._authorize(run, principal, "runs.read")
            except AccessDenied:
                continue
            visible.append(run)
        return visible

    def run_once(self, worker_id: str) -> RunRecord | None:
        worker = Principal(id=worker_id, role="admin")
        self.policy.require(worker, "worker.execute")
        run = self.repo.claim_next(worker_id)
        if run is None:
            return None
        try:
            spec = self._authorize(run, worker, "worker.execute")
            current_code = self._current_identity()
            frozen_code = _object(run.manifest.get("code_environment"))
            if current_code != frozen_code:
                raise Conflict(
                    "Code or environment changed since submission; submit a new attempt."
                )
            bars = self.datasets.bars(spec.dataset_id, worker, spec.dataset_version)
            if spec.task == "failure_fixture":
                raise PlatformError(
                    "intentional_fixture_failure", "Requested technical failure fixture."
                )
            if spec.task == "quality_check":
                details = self.datasets.inspect(spec.dataset_id, worker, spec.dataset_version)
            elif spec.task == "transform_check":
                transform = self.datasets.transform(
                    spec.dataset_id, worker, spec.dataset_version, window=spec.window
                )
                details = {
                    "transform_id": transform.id,
                    "transform_version": transform.version,
                    "transform_hash": transform.content_hash,
                    "transform": transform.body,
                }
            else:
                details = run_technical_ledger(bars)
            if self._current_identity() != frozen_code:
                raise Conflict("Code or environment changed during the attempt; result rejected.")
            report: dict[str, JsonValue] = {
                "task": spec.task,
                "synthetic": True,
                "financial_validation": False,
                "label": "Synthetic technical verification; no financial experiment",
                "config_hash": run.config_hash,
                "manifest_hash": run.manifest_hash,
                "details": details,
            }
            payload = canonical_json(report).encode()
            report_digest = self.store.put(payload, "json")
            markdown = (
                "# Synthetic technical report\n\n"
                "This verifies software with synthetic fixtures. It is not a financial "
                "experiment or strategy validation.\n\n```json\n"
                + json.dumps(report, indent=2, ensure_ascii=False)
                + "\n```\n"
            ).encode()
            markdown_digest = self.store.put(markdown, "md")
            result: dict[str, JsonValue] = {
                "synthetic": True,
                "financial_validation": False,
                "task": spec.task,
                "deterministic_digest": hashlib.sha256(payload).hexdigest(),
                "report": report,
                "artifacts": {
                    "report.json": {
                        "digest": report_digest,
                        "suffix": "json",
                        "media_type": "application/json",
                    },
                    "report.md": {
                        "digest": markdown_digest,
                        "suffix": "md",
                        "media_type": "text/markdown; charset=utf-8",
                    },
                },
            }
            return self.repo.complete(run.id, worker_id, result)
        except Exception as error:
            # Do not serialize exceptions or traces containing paths, SQL or external text.
            safe = (
                error
                if isinstance(error, PlatformError)
                else PlatformError(
                    "technical_task_failed",
                    "Technical task failed safely; inputs were not published.",
                )
            )
            try:
                return self.repo.fail(
                    run.id, worker_id, {"code": safe.code, "message": safe.message}
                )
            except Conflict:
                # Cancellation or explicit interruption fenced this old worker's completion.
                return self.repo.get_run(run.id)

    def artifact(self, id: str, name: str, principal: Principal) -> tuple[bytes, str]:
        run = self.repo.get_run(id)
        self._authorize(run, principal, "artifacts.read")
        if run.state != "succeeded" or run.result is None:
            raise NotFound("No successful technical artifact exists for this attempt.")
        artifacts = _object(run.result.get("artifacts"))
        if name not in {"report.json", "report.md"} or name not in artifacts:
            raise NotFound("Artifact name is not registered for this run.")
        artifact = _object(artifacts[name])
        return (
            self.store.get(_text(artifact.get("digest")), _text(artifact.get("suffix"))),
            _text(artifact.get("media_type")),
        )

    def compare(self, ids: builtins.list[str], principal: Principal) -> dict[str, JsonValue]:
        if not 2 <= len(ids) <= 10 or len(set(ids)) != len(ids):
            raise Conflict("Comparison requires 2 to 10 distinct technical attempts.")
        records = [self.get(id, principal) for id in ids]
        first = records[0]
        matching = all(
            run.config_hash == first.config_hash and run.manifest_hash == first.manifest_hash
            for run in records
        )
        digests = [
            run.result.get("deterministic_digest") if run.result else None for run in records
        ]
        return {
            "synthetic": True,
            "financial_validation": False,
            "comparable": matching,
            "basis": "Identical immutable configuration and input/code/environment manifests",
            "same_result": matching and all(d is not None and d == digests[0] for d in digests),
            "runs": [
                {
                    "id": run.id,
                    "state": run.state,
                    "config_hash": run.config_hash,
                    "manifest_hash": run.manifest_hash,
                    "deterministic_digest": digest,
                }
                for run, digest in zip(records, digests, strict=True)
            ],
            "interpretation": (
                "Technical reproducibility comparison; no strategy ranking or winner."
            ),
        }

    def propose(self, proposal: ResearchProposal, principal: Principal) -> DocumentRecord:
        self.policy.require(principal, "proposals.create")
        body: dict[str, JsonValue] = {
            "proposal": proposal.model_dump(mode="json"),
            "actor": principal.id,
            "status": "pending_review",
            "executable": False,
            "budget_authorized": False,
            "financial_validation": False,
        }
        record = DocumentRecord(
            kind="proposal",
            id=str(uuid4()),
            version=1,
            body=body,
            content_hash=content_hash(body),
            created_at=datetime.now(UTC),
        )
        # One serialized transaction prevents concurrent requests bypassing the finite quota.
        with self.repo.database.transaction() as connection:
            rows = connection.execute(
                select(documents.c.body).where(documents.c.kind == "proposal")
            )
            previous = [json.loads(row[0]) for row in rows]
            owned = [item for item in previous if item.get("actor") == principal.id]
            units = sum(int(item["proposal"]["requested_budget_units"]) for item in owned)
            if len(owned) >= 20 or units + proposal.requested_budget_units > 100:
                raise Conflict(
                    "Proposal quota exhausted: 20 records and 100 requested units per actor."
                )
            connection.execute(
                insert(documents).values(
                    kind=record.kind,
                    id=record.id,
                    version=1,
                    body=canonical_json(body),
                    content_hash=record.content_hash,
                    created_at=record.created_at.isoformat(),
                )
            )
            connection.execute(
                insert(audit).values(
                    id=str(uuid4()),
                    actor=principal.id,
                    action="proposals.create",
                    resource=record.id,
                    outcome="pending_review",
                    details=canonical_json({"executable": False}),
                    created_at=record.created_at.isoformat(),
                )
            )
        return record

    def proposals(self, principal: Principal) -> builtins.list[DocumentRecord]:
        self.policy.require(principal, "metadata.read")
        return self.repo.list("proposal")
