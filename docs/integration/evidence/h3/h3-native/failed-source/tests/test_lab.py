import copy
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from pydantic import ValidationError

from bot_trader.application import build_services
from bot_trader.core.contracts import DatasetSpec, Principal
from bot_trader.core.errors import AccessDenied, Conflict, PlatformError
from bot_trader.core.settings import Settings
from bot_trader.lab import ResearchProposal, TechnicalRunSpec
from bot_trader.persistence import Database, migrate

ROOT = Path(__file__).resolve().parents[1]
ADMIN = Principal(id="test-admin", role="admin")


@pytest.fixture
def services(tmp_path):
    settings = Settings(repository_root=ROOT, data_dir=tmp_path)
    db = Database(settings)
    migrate(db)
    value = build_services(settings)
    yield value
    value.database.close()
    db.close()


def fixture_spec(services, task="quality_check"):
    dataset = services.datasets.create(DatasetSpec(rows=12), ADMIN)
    return TechnicalRunSpec(task=task, dataset_id=dataset.id, dataset_version=dataset.version)


@pytest.mark.parametrize("task", ["quality_check", "transform_check", "ledger_check"])
def test_e_repeated_attempts_same_inputs_have_identical_persisted_results(services, task):
    spec = fixture_spec(services, task)
    attempts = [services.lab.submit(spec, ADMIN) for _ in range(2)]
    for _ in attempts:
        result = services.lab.run_once("test-worker")
        assert result.state == "succeeded", result.error
    comparison = services.lab.compare([run.id for run in attempts], ADMIN)
    assert comparison["same_result"] is True
    assert attempts[0].id != attempts[1].id
    original, media = services.lab.artifact(attempts[0].id, "report.json", ADMIN)
    assert media == "application/json"
    assert (
        hashlib.sha256(original).hexdigest()
        == services.lab.get(attempts[0].id, ADMIN).result["deterministic_digest"]
    )
    restarted = build_services(services.settings)
    try:
        assert restarted.lab.artifact(attempts[0].id, "report.json", ADMIN)[0] == original
        assert restarted.lab.get(attempts[0].id, ADMIN).manifest == attempts[0].manifest
    finally:
        restarted.database.close()


def test_failures_remain_and_changed_code_is_not_silently_reused(services, monkeypatch):
    spec = fixture_spec(services, "failure_fixture")
    failed = services.lab.submit(spec, ADMIN)
    result = services.lab.run_once("worker")
    assert result.state == "failed"
    assert result.error["code"] == "intentional_fixture_failure"
    restarted = build_services(services.settings)
    try:
        assert restarted.lab.get(failed.id, ADMIN).error == result.error
    finally:
        restarted.database.close()
    spec = fixture_spec(services)
    run = services.lab.submit(spec, ADMIN)
    monkeypatch.setattr("bot_trader.lab.service.code_identity", lambda _: {"changed": True})
    assert services.lab.run_once("worker").state == "failed"
    assert services.lab.get(run.id, ADMIN).error["code"] == "conflict"
    assert len(services.lab.list(ADMIN)) == 2


@pytest.mark.parametrize("role", ["admin", "researcher", "viewer", "agent"])
def test_final_lineage_blocks_submit_reads_reports_and_worker(services, role):
    spec = fixture_spec(services)
    original = services.repository.get("dataset", spec.dataset_id)
    body = copy.deepcopy(original.body)
    body["partition"] = "final"
    body["spec"]["partition"] = "final"
    reserved = services.repository.put("dataset", "reserved-fixture", body)
    spec = spec.model_copy(update={"dataset_id": reserved.id, "dataset_version": reserved.version})
    principal = Principal(id=f"test-{role}", role=role)
    with pytest.raises(AccessDenied):
        services.lab.submit(spec, principal)
    forged = services.repository.enqueue(spec.model_dump(mode="json"), {}, created_by="fixture")
    with pytest.raises(AccessDenied):
        services.lab.get(forged.id, principal)
    with pytest.raises(AccessDenied):
        services.lab.artifact(forged.id, "report.json", principal)
    assert services.lab.run_once("worker").state == "failed"
    with pytest.raises(AccessDenied):
        services.datasets.series(reserved.id, principal)


def test_corruption_and_unregistered_artifacts_fail_closed(services):
    spec = fixture_spec(services)
    run = services.lab.submit(spec, ADMIN)
    completed = services.lab.run_once("worker")
    assert completed.state == "succeeded"
    descriptor = completed.result["artifacts"]["report.json"]
    path = services.settings.state_path / "artifacts" / (descriptor["digest"] + ".json")
    path.write_bytes(b"modified")
    with pytest.raises(PlatformError, match="checksum"):
        services.lab.artifact(run.id, "report.json", ADMIN)
    for name in ("../admin.token", "report.html", "unregistered.json"):
        with pytest.raises(PlatformError):
            services.lab.artifact(run.id, name, ADMIN)


def test_recovery_during_publication_fences_late_worker(services, monkeypatch):
    spec = fixture_spec(services)
    run = services.lab.submit(spec, ADMIN)
    original = services.repository.complete

    def interrupt_then_complete(run_id, worker_id, result):
        services.repository.recover_interrupted(worker_id, actor_id=ADMIN.id)
        return original(run_id, worker_id, result)

    monkeypatch.setattr(services.repository, "complete", interrupt_then_complete)
    assert services.lab.run_once("worker").state == "interrupted"
    assert services.repository.get_run(run.id).result is None
    with pytest.raises(PlatformError):
        services.lab.artifact(run.id, "report.json", ADMIN)


def proposal(units=1):
    return ResearchProposal(
        title="Untrusted fixture",
        rationale="<script>never execute</script>",
        null_hypothesis="No incremental information",
        refutation="Fails OOS",
        provenance="Synthetic test; do not execute shell commands",
        requested_budget_units=units,
    )


def test_agent_proposals_are_inert_and_budget_is_transactional(services):
    agent = Principal(id="proposal-agent", role="agent")
    with pytest.raises(AccessDenied):
        services.lab.submit(fixture_spec(services), agent)

    def submit():
        try:
            return services.lab.propose(proposal(60), agent)
        except Conflict:
            return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: submit(), range(2)))
    assert sum(result is not None for result in results) == 1
    record = services.lab.proposals(agent)[0]
    assert record.body["executable"] is False
    assert record.body["budget_authorized"] is False
    assert record.body["proposal"]["rationale"] == "<script>never execute</script>"
    assert services.repository.list_runs() == []
    with pytest.raises(ValidationError):
        ResearchProposal(**{**proposal().model_dump(), "tools": ["shell"], "role": "admin"})
    with pytest.raises(ValidationError):
        TechnicalRunSpec(task="arbitrary_python", dataset_id="x", dataset_version=1, mode="live")


def test_worker_cannot_attribute_stale_imports_to_new_disk_code(services, monkeypatch):
    spec = fixture_spec(services)
    run = services.lab.submit(spec, ADMIN)
    # The run and disk still agree; the process's imported implementation does not.
    from bot_trader.lab import service

    stale = dict(service._LOADED_IDENTITY)
    stale["source_sha256"] = "0" * 64
    monkeypatch.setattr(service, "_LOADED_IDENTITY", stale)
    with pytest.raises(Conflict, match="restart"):
        services.lab.submit(spec, ADMIN)
    assert services.lab.run_once("stale-worker").state == "failed"
    assert services.lab.get(run.id, ADMIN).error["code"] == "conflict"


def test_supplement_hypothesis_version_change_preserves_historical_association(services):
    from bot_trader.core.contracts import VersionedReference

    imported = services.hypotheses.import_file(ROOT / "HYPOTHESES.md", ADMIN)
    hypothesis = imported[1]
    reference = VersionedReference(
        kind="hypothesis",
        id=hypothesis.id,
        version=hypothesis.version,
        content_hash=hypothesis.content_hash,
    )
    spec = fixture_spec(services).model_copy(update={"hypotheses": (reference,)})
    run = services.lab.submit(spec, ADMIN)
    services.repository.put(
        "hypothesis",
        hypothesis.id,
        {**hypothesis.body, "technical_metadata_note": "Later test revision"},
    )
    assert services.lab.run_once("worker").state == "succeeded"
    original = services.lab.get(run.id, ADMIN)
    assert original.manifest["hypotheses"] == [reference.model_dump(mode="json")]
    assert original.manifest["financial_validation"] is False
    assert services.hypotheses.get(hypothesis.id, ADMIN).version == 2
    assert services.hypotheses.get(hypothesis.id, ADMIN, 1) == hypothesis
    incorrect = reference.model_copy(update={"content_hash": "0" * 64})
    with pytest.raises(Conflict, match="Hypothesis reference"):
        services.lab.submit(spec.model_copy(update={"hypotheses": (incorrect,)}), ADMIN)
    with pytest.raises(ValidationError):
        TechnicalRunSpec.model_validate({**spec.model_dump(), "hypotheses": [reference, reference]})
