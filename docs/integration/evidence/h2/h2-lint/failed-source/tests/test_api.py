from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from bot_trader.api.app import create_app
from bot_trader.core.settings import Settings
from bot_trader.persistence import Database, migrate

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "local-test-only-credential-" + "x" * 24
ORIGIN = "http://testserver"


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        repository_root=ROOT,
        data_dir=tmp_path,
        admin_token=SecretStr(TOKEN),
        allowed_hosts=("testserver",),
        allowed_origins=(ORIGIN,),
    )
    database = Database(settings)
    migrate(database)
    with TestClient(create_app(settings), raise_server_exceptions=False) as value:
        yield value
    database.close()


def sign_in(client):
    response = client.post("/api/session", json={"token": TOKEN}, headers={"origin": ORIGIN})
    assert response.status_code == 200, response.text
    return {"origin": ORIGIN, "x-csrf-token": response.json()["csrf"]}


def test_authentication_host_origin_csrf_revocation_and_safe_validation(client):
    assert client.get("/api/status").status_code == 401
    assert client.get("/api/health", headers={"host": "evil.example"}).status_code == 400
    assert client.post("/api/session", json={"token": TOKEN}).status_code == 403
    response = client.post(
        "/api/session", json={"token": TOKEN, "role": "admin"}, headers={"origin": ORIGIN}
    )
    assert response.status_code == 422
    assert TOKEN not in response.text
    assert "x-correlation-id" in response.headers
    headers = sign_in(client)
    assert client.get("/api/session").json()["principal"]["role"] == "admin"
    assert client.get("/api/status").json()["financial_experiments"] == 0
    assert len(client.get("/api/modules").json()) == 15
    assert client.delete("/api/session", headers={"origin": ORIGIN}).status_code == 403
    assert client.delete("/api/session", headers=headers).status_code == 200
    assert client.get("/api/status").status_code == 401


def test_input_limits_cookie_flags_and_absent_execution_routes(client):
    response = client.post("/api/session", json={"token": TOKEN}, headers={"origin": ORIGIN})
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    assert (
        client.post("/api/session", content=b"x" * 70000, headers={"origin": ORIGIN}).status_code
        == 413
    )
    for path in ("/api/orders", "/api/live", "/api/market/import", "/api/sql", "/api/tools"):
        assert client.get(path).status_code == 404
    assert client.get("/api/health").headers["x-content-type-options"] == "nosniff"
    assert client.get("/api/health").headers["cache-control"] == "no-store"


def test_real_catalog_run_chart_report_and_failure_workflow(client):
    headers = sign_in(client)
    platform = client.app.state.platform
    from bot_trader.core.contracts import Principal

    platform.hypotheses.import_file(ROOT / "HYPOTHESES.md", Principal(id="admin", role="admin"))
    assert len(client.get("/api/hypotheses").json()) == 25
    created = client.post("/api/datasets", json={"rows": 12, "seed": 23}, headers=headers)
    assert created.status_code == 201, created.text
    dataset = created.json()
    series = client.get(f"/api/datasets/{dataset['id']}/series").json()
    assert len(series["candles"]) == 12 and len(series["overlay"]) == 8
    assert series["synthetic"] is True
    spec = {"task": "ledger_check", "dataset_id": dataset["id"], "dataset_version": 1}
    attempts = [
        client.post("/api/experiments", json=spec, headers=headers).json() for _ in range(2)
    ]
    for _ in attempts:
        assert platform.lab.run_once("api-test-worker").state == "succeeded"
    comparison = client.post(
        "/api/experiments/compare",
        json={"run_ids": [run["id"] for run in attempts]},
        headers=headers,
    )
    assert comparison.json()["same_result"] is True
    report = client.get(f"/api/experiments/{attempts[0]['id']}/artifacts/report.json")
    assert report.status_code == 200
    assert report.headers["content-disposition"] == 'attachment; filename="report.json"'
    assert report.json()["financial_validation"] is False
    failure = client.post(
        "/api/experiments", json={**spec, "task": "failure_fixture"}, headers=headers
    ).json()
    platform.lab.run_once("api-test-worker")
    record = client.get(f"/api/experiments/{failure['id']}").json()
    assert record["state"] == "failed" and record["error"]["code"] == "intentional_fixture_failure"
    assert TOKEN not in client.get("/api/audit").text
    assert (
        client.post(
            "/api/datasets", json={"rows": 12, "partition": "final"}, headers=headers
        ).status_code
        == 403
    )
    assert (
        client.post("/api/experiments", json={**spec, "mode": "live"}, headers=headers).status_code
        == 422
    )


@pytest.mark.parametrize("role", ["viewer", "researcher", "agent"])
def test_role_authority_comes_from_server_credential_files(tmp_path, role):
    from bot_trader.api.credentials import issue_credential

    settings = Settings(
        repository_root=ROOT,
        data_dir=tmp_path,
        admin_token=SecretStr(TOKEN),
        allowed_hosts=("testserver",),
        allowed_origins=(ORIGIN,),
    )
    db = Database(settings)
    migrate(db)
    path = issue_credential(settings, role)
    with TestClient(create_app(settings)) as client:
        login = client.post(
            "/api/session", json={"token": path.read_text().strip()}, headers={"origin": ORIGIN}
        )
        assert login.json()["principal"]["role"] == role
        headers = {"origin": ORIGIN, "x-csrf-token": login.json()["csrf"]}
        response = client.post("/api/datasets", json={"rows": 4}, headers=headers)
        assert response.status_code == (201 if role == "researcher" else 403)
        assert client.get("/api/modules").status_code == 200
        assert client.get("/api/hypotheses").status_code == 200
        if role == "agent":
            assert client.get("/api/experiments").status_code == 403
    db.close()
