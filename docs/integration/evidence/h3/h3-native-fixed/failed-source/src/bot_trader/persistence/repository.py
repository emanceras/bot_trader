"""Append-only document versions and durable, conditionally updated job attempts."""

import builtins
import hashlib
import json
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import Field, JsonValue
from sqlalchemy import Connection, and_, desc, func, insert, select, update

from bot_trader.core.contracts import FrozenContract, Identifier, UTCDateTime
from bot_trader.core.errors import Conflict, NotFound

from .database import Database, check_schema
from .schema import audit, documents, runs

RunState = Literal["queued", "running", "succeeded", "failed", "interrupted", "cancelled"]


def canonical_json(value: dict[str, JsonValue]) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def content_hash(value: dict[str, JsonValue]) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def _now() -> str:
    return datetime.now(UTC).isoformat()


class DocumentRecord(FrozenContract):
    kind: Identifier
    id: Identifier
    version: int = Field(ge=1)
    body: dict[str, JsonValue]
    content_hash: str
    created_at: UTCDateTime


class AuditRecord(FrozenContract):
    id: str
    actor: str
    action: str
    resource: str
    outcome: str
    details: dict[str, JsonValue]
    created_at: UTCDateTime


class RunRecord(FrozenContract):
    id: str
    state: RunState
    config: dict[str, JsonValue]
    config_hash: str
    manifest: dict[str, JsonValue]
    manifest_hash: str
    result: dict[str, JsonValue] | None = None
    error: dict[str, JsonValue] | None = None
    owner: str | None = None
    created_by: str
    parent_run_id: str | None = None
    created_at: UTCDateTime
    started_at: UTCDateTime | None = None
    finished_at: UTCDateTime | None = None


def _document(row: dict[str, object]) -> DocumentRecord:
    row["body"] = json.loads(str(row["body"]))
    record = DocumentRecord.model_validate(row)
    if content_hash(record.body) != record.content_hash:
        raise Conflict("Stored document content hash does not match its body.")
    return record


def _run(row: dict[str, object]) -> RunRecord:
    for field in ("config", "manifest", "result", "error"):
        if row[field] is not None:
            row[field] = json.loads(str(row[field]))
    return RunRecord.model_validate(row)


class Repository:
    def __init__(self, database: Database) -> None:
        check_schema(database)
        self.database = database

    def put(
        self,
        kind: str,
        id: str,
        body: dict[str, JsonValue],
        *,
        expected_version: int | None = None,
    ) -> DocumentRecord:
        serialized = canonical_json(body)
        digest = hashlib.sha256(serialized.encode()).hexdigest()
        with self.database.transaction() as connection:
            row = (
                connection.execute(
                    select(documents)
                    .where(documents.c.kind == kind, documents.c.id == id)
                    .order_by(desc(documents.c.version))
                    .limit(1)
                )
                .mappings()
                .first()
            )
            previous = _document(dict(row)) if row is not None else None
            if expected_version is not None and expected_version != (
                previous.version if previous else 0
            ):
                raise Conflict("Document version changed.")
            if previous is not None and previous.content_hash == digest:
                return previous
            record = DocumentRecord(
                kind=kind,
                id=id,
                version=previous.version + 1 if previous else 1,
                body=body,
                content_hash=digest,
                created_at=datetime.now(UTC),
            )
            connection.execute(
                insert(documents).values(
                    kind=kind,
                    id=id,
                    version=record.version,
                    body=serialized,
                    content_hash=digest,
                    created_at=record.created_at.isoformat(),
                )
            )
            return record

    def get(self, kind: str, id: str, version: int | None = None) -> DocumentRecord:
        query = select(documents).where(documents.c.kind == kind, documents.c.id == id)
        if version is not None:
            query = query.where(documents.c.version == version)
        with self.database.engine.connect() as connection:
            row = (
                connection.execute(query.order_by(desc(documents.c.version)).limit(1))
                .mappings()
                .first()
            )
        if row is None:
            raise NotFound()
        return _document(dict(row))

    def list(
        self, kind: str, *, limit: int = 100, all_versions: bool = False
    ) -> list[DocumentRecord]:
        if not 1 <= limit <= 1000:
            raise ValueError("List limit must be between 1 and 1000.")
        query = select(documents).where(documents.c.kind == kind)
        if not all_versions:
            latest = (
                select(documents.c.id, func.max(documents.c.version).label("version"))
                .where(documents.c.kind == kind)
                .group_by(documents.c.id)
                .subquery()
            )
            query = query.join(
                latest, and_(documents.c.id == latest.c.id, documents.c.version == latest.c.version)
            )
        with self.database.engine.connect() as connection:
            rows = connection.execute(
                query.order_by(documents.c.id, documents.c.version).limit(limit)
            )
            return [_document(dict(row)) for row in rows.mappings()]

    def append_audit(
        self,
        actor: str,
        action: str,
        resource: str,
        outcome: str,
        details: dict[str, JsonValue] | None = None,
    ) -> AuditRecord:
        with self.database.transaction() as connection:
            return self._audit(connection, actor, action, resource, outcome, details or {})

    def _audit(
        self,
        connection: Connection,
        actor: str,
        action: str,
        resource: str,
        outcome: str,
        details: dict[str, JsonValue],
    ) -> AuditRecord:
        record = AuditRecord(
            id=str(uuid4()),
            actor=actor,
            action=action,
            resource=resource,
            outcome=outcome,
            details=details,
            created_at=datetime.now(UTC),
        )
        connection.execute(
            insert(audit).values(
                id=record.id,
                actor=actor,
                action=action,
                resource=resource,
                outcome=outcome,
                details=canonical_json(details),
                created_at=record.created_at.isoformat(),
            )
        )
        return record

    def list_audit(self, *, limit: int = 100) -> builtins.list[AuditRecord]:
        if not 1 <= limit <= 1000:
            raise ValueError("List limit must be between 1 and 1000.")
        with self.database.engine.connect() as connection:
            rows = connection.execute(select(audit).order_by(desc(audit.c.created_at)).limit(limit))
            result = []
            for row in rows.mappings():
                value = dict(row)
                value["details"] = json.loads(str(value["details"]))
                result.append(AuditRecord.model_validate(value))
            return result

    def enqueue(
        self,
        config: dict[str, JsonValue],
        manifest: dict[str, JsonValue],
        *,
        created_by: str,
        parent_run_id: str | None = None,
    ) -> RunRecord:
        if config.get("mode", "technical") != "technical":
            raise Conflict("Only technical runs can be queued.")
        record = RunRecord(
            id=str(uuid4()),
            state="queued",
            config=config,
            config_hash=content_hash(config),
            manifest=manifest,
            manifest_hash=content_hash(manifest),
            created_by=created_by,
            parent_run_id=parent_run_id,
            created_at=datetime.now(UTC),
        )
        with self.database.transaction() as connection:
            count = connection.execute(
                select(func.count())
                .select_from(runs)
                .where(runs.c.state.in_(["queued", "running"]))
            ).scalar_one()
            if count >= self.database.settings.max_queued_runs:
                raise Conflict("Technical job queue limit reached.")
            if parent_run_id is not None:
                parent = connection.execute(
                    select(runs.c.state).where(runs.c.id == parent_run_id)
                ).first()
                if parent is None or parent[0] not in {"failed", "interrupted", "cancelled"}:
                    raise Conflict("Retry parent must be an unsuccessful completed attempt.")
            values = record.model_dump(mode="json", exclude={"schema_version"})
            values["config"] = canonical_json(config)
            values["manifest"] = canonical_json(manifest)
            connection.execute(insert(runs).values(**values))
            self._audit(connection, created_by, "runs.enqueue", record.id, "queued", {})
        return record

    def get_run(self, run_id: str) -> RunRecord:
        with self.database.engine.connect() as connection:
            row = connection.execute(select(runs).where(runs.c.id == run_id)).mappings().first()
        if row is None:
            raise NotFound("Run does not exist.")
        return _run(dict(row))

    def list_runs(self, *, limit: int = 100) -> builtins.list[RunRecord]:
        if not 1 <= limit <= 1000:
            raise ValueError("List limit must be between 1 and 1000.")
        with self.database.engine.connect() as connection:
            rows = connection.execute(select(runs).order_by(desc(runs.c.created_at)).limit(limit))
            return [_run(dict(row)) for row in rows.mappings()]

    def claim_next(self, worker_id: str) -> RunRecord | None:
        return self._claim(worker_id)

    def claim(self, run_id: str, worker_id: str) -> RunRecord | None:
        return self._claim(worker_id, run_id)

    def _claim(self, worker_id: str, run_id: str | None = None) -> RunRecord | None:
        if not worker_id or len(worker_id) > 128:
            raise ValueError("Worker identity must contain 1 to 128 characters.")
        with self.database.transaction() as connection:
            query = select(runs).where(runs.c.state == "queued")
            if run_id is not None:
                query = query.where(runs.c.id == run_id)
            row = connection.execute(query.order_by(runs.c.created_at).limit(1)).mappings().first()
            if row is None:
                return None
            started = _now()
            connection.execute(
                update(runs)
                .where(runs.c.id == row["id"], runs.c.state == "queued")
                .values(state="running", owner=worker_id, started_at=started)
            )
            self._audit(connection, worker_id, "runs.claim", str(row["id"]), "running", {})
            value = dict(row)
            value.update(state="running", owner=worker_id, started_at=started)
            return _run(value)

    def complete(self, run_id: str, worker_id: str, result: dict[str, JsonValue]) -> RunRecord:
        return self._finish(run_id, worker_id, "succeeded", result=result)

    def fail(self, run_id: str, worker_id: str, error: dict[str, JsonValue]) -> RunRecord:
        return self._finish(run_id, worker_id, "failed", error=error)

    def _finish(
        self,
        run_id: str,
        worker_id: str,
        state: Literal["succeeded", "failed"],
        *,
        result: dict[str, JsonValue] | None = None,
        error: dict[str, JsonValue] | None = None,
    ) -> RunRecord:
        with self.database.transaction() as connection:
            changed = connection.execute(
                update(runs)
                .where(
                    runs.c.id == run_id,
                    runs.c.state == "running",
                    runs.c.owner == worker_id,
                )
                .values(
                    state=state,
                    result=canonical_json(result) if result is not None else None,
                    error=canonical_json(error) if error is not None else None,
                    finished_at=_now(),
                )
            )
            if changed.rowcount != 1:
                raise Conflict("Only the owning worker can finish a running attempt once.")
            self._audit(connection, worker_id, "runs.finish", run_id, state, {})
        return self.get_run(run_id)

    def recover_interrupted(self, worker_id: str, *, actor_id: str) -> builtins.list[str]:
        """Explicitly abandon one confirmed-dead worker; never replay its attempts."""
        recovered: builtins.list[str] = []
        with self.database.transaction() as connection:
            ids: Sequence[str] = (
                connection.execute(
                    select(runs.c.id).where(runs.c.state == "running", runs.c.owner == worker_id)
                )
                .scalars()
                .all()
            )
            for run_id in ids:
                connection.execute(
                    update(runs)
                    .where(runs.c.id == run_id)
                    .values(
                        state="interrupted",
                        finished_at=_now(),
                        error=canonical_json(
                            {
                                "code": "worker_interrupted",
                                "message": "Worker interruption explicitly recorded.",
                            }
                        ),
                    )
                )
                self._audit(connection, actor_id, "runs.recover", run_id, "interrupted", {})
                recovered.append(run_id)
        return recovered

    def cancel(self, run_id: str, *, actor_id: str) -> RunRecord:
        with self.database.transaction() as connection:
            changed = connection.execute(
                update(runs)
                .where(runs.c.id == run_id, runs.c.state.in_(["queued", "running"]))
                .values(state="cancelled", finished_at=_now())
            )
            if changed.rowcount != 1:
                raise Conflict("Only queued or running attempts can be cancelled.")
            self._audit(connection, actor_id, "runs.cancel", run_id, "cancelled", {})
        return self.get_run(run_id)
