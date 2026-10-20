from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from bot_trader.core.errors import Conflict, NotFound
from bot_trader.core.settings import Settings
from bot_trader.persistence import Database, Repository, check_schema, migrate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def database(tmp_path: Path) -> Database:
    database = Database(Settings(repository_root=ROOT, data_dir=tmp_path / "state"))
    migrate(database)
    return database


def test_explicit_migration_and_restart_without_destructive_initialization(tmp_path: Path) -> None:
    settings = Settings(repository_root=ROOT, data_dir=tmp_path / "state")
    first = Database(settings)
    with pytest.raises(Conflict, match="missing"):
        Repository(first)
    assert not first.path.exists()
    migrate(first)
    repository = Repository(first)
    repository.put("hypothesis", "H-00", {"title": "preserved"})
    first.close()
    restarted = Database(settings)
    migrate(restarted)
    assert Repository(restarted).get("hypothesis", "H-00").body["title"] == "preserved"
    restarted.close()


def test_incompatible_schema_rejected(database: Database) -> None:
    with database.engine.begin() as connection:
        connection.execute(text("UPDATE alembic_version SET version_num = 'future'"))
    with pytest.raises(Conflict, match="incompatible"):
        check_schema(database)


def test_connection_invariants_and_append_only_history(database: Database) -> None:
    repository = Repository(database)
    repository.put("dataset", "fixture", {"rows": 2})
    repository.append_audit("operator", "test", "fixture", "recorded")
    run = repository.enqueue({}, {}, created_by="operator")
    with database.engine.connect() as first, database.engine.connect() as second:
        for connection in (first, second):
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
            assert connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() == 10_000
    for statement in (
        "UPDATE documents SET body = '{}'",
        "DELETE FROM documents",
        "UPDATE audit SET outcome = 'changed'",
        "DELETE FROM audit",
        "UPDATE runs SET config = '{}'",
        "DELETE FROM runs",
    ):
        with pytest.raises(IntegrityError), database.transaction() as connection:
            connection.exec_driver_sql(statement)
    assert repository.get("dataset", "fixture").body == {"rows": 2}
    assert repository.get_run(run.id).state == "queued"


def test_document_versions_idempotency_and_immutable_storage(database: Database) -> None:
    repository = Repository(database)
    first = repository.put("dataset", "synthetic", {"rows": 3, "nested": {"version": 1}})
    assert repository.put("dataset", "synthetic", first.body) == first
    first.body["rows"] = 99
    assert repository.get("dataset", "synthetic").body["rows"] == 3
    second = repository.put("dataset", "synthetic", {"rows": 4}, expected_version=1)
    assert second.version == 2
    assert repository.get("dataset", "synthetic", 1).body["rows"] == 3
    assert len(repository.list("dataset")) == 1
    assert len(repository.list("dataset", all_versions=True)) == 2
    with pytest.raises(Conflict):
        repository.put("dataset", "synthetic", {"rows": 5}, expected_version=1)
    with pytest.raises(NotFound):
        repository.get("missing", "missing")
    with pytest.raises(ValueError):
        repository.put("invalid", "number", {"value": float("nan")})


def test_atomic_concurrent_claim_completion_and_safe_failure(database: Database) -> None:
    repository = Repository(database)
    queued = repository.enqueue(
        {"mode": "technical", "seed": 42}, {"revision": "test"}, created_by="test"
    )
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(repository.claim, queued.id, owner) for owner in ("one", "two")]
        claims = [future.result() for future in futures]
    claimed = [claim for claim in claims if claim is not None]
    assert len(claimed) == 1
    owner = claimed[0].owner
    assert owner is not None
    with pytest.raises(Conflict):
        repository.complete(queued.id, "other", {"technical": True})
    result = repository.complete(queued.id, owner, {"technical": True})
    assert result.state == "succeeded"
    assert result.config_hash == queued.config_hash
    with pytest.raises(Conflict):
        repository.complete(queued.id, owner, {"replacement": True})
    assert repository.get_run(queued.id).result == {"technical": True}
    failed = repository.enqueue({"mode": "technical"}, {}, created_by="test")
    assert repository.claim(failed.id, "one") is not None
    repository.fail(failed.id, "one", {"code": "synthetic_failure", "message": "Fixture failure."})
    assert repository.get_run(failed.id).state == "failed"
    assert len(repository.list_runs()) == 2
    assert any(event.action == "runs.finish" for event in repository.list_audit())


def test_restart_recovery_is_explicit_and_fences_stale_completion(database: Database) -> None:
    repository = Repository(database)
    queued = repository.enqueue({"mode": "technical"}, {}, created_by="test")
    assert repository.claim_next("dead-worker") is not None
    database.close()
    restarted = Repository(Database(database.settings))
    assert restarted.get_run(queued.id).state == "running"
    assert restarted.claim_next("replacement") is None
    assert restarted.recover_interrupted("dead-worker", actor_id="operator") == [queued.id]
    assert restarted.get_run(queued.id).state == "interrupted"
    assert restarted.claim_next("replacement") is None
    with pytest.raises(Conflict):
        restarted.complete(queued.id, "dead-worker", {"too_late": True})
    retry = restarted.enqueue(
        queued.config, queued.manifest, created_by="operator", parent_run_id=queued.id
    )
    assert retry.id != queued.id and retry.config_hash == queued.config_hash
    assert restarted.get_run(queued.id).state == "interrupted"


def test_queue_budget_and_cancellation_are_atomic(tmp_path: Path) -> None:
    database = Database(Settings(repository_root=ROOT, data_dir=tmp_path, max_queued_runs=1))
    migrate(database)
    repository = Repository(database)

    def enqueue() -> str:
        try:
            return repository.enqueue({}, {}, created_by="test").id
        except Conflict:
            return "full"

    with ThreadPoolExecutor(max_workers=2) as executor:
        values = list(executor.map(lambda _: enqueue(), range(2)))
    assert values.count("full") == 1
    run = repository.list_runs()[0]
    repository.claim(run.id, "worker")
    repository.cancel(run.id, actor_id="operator")
    with pytest.raises(Conflict):
        repository.complete(run.id, "worker", {})
    assert repository.enqueue({}, {}, created_by="test").state == "queued"


def test_content_corruption_is_detected_even_for_valid_json(database: Database) -> None:
    repository = Repository(database)
    repository.put("fixture", "corrupted", {"rows": 2})
    # Simulate external corruption, bypassing the normal append-only SQL protection.
    with database.transaction() as connection:
        connection.exec_driver_sql("DROP TRIGGER documents_deny_update")
        connection.exec_driver_sql("UPDATE documents SET body = '{\"rows\":3}'")
    with pytest.raises(Conflict, match="content hash"):
        repository.get("fixture", "corrupted")
