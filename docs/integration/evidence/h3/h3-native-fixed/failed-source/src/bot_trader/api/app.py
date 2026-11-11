"""HTTP composition root. Business services remain independent of FastAPI."""

import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import Field, JsonValue, SecretStr
from starlette.middleware.trustedhost import TrustedHostMiddleware

from bot_trader.application import build_services
from bot_trader.core.contracts import DatasetSpec, FrozenContract, ModuleManifest, Principal
from bot_trader.core.errors import AccessDenied, PlatformError
from bot_trader.core.settings import Settings
from bot_trader.lab import ResearchProposal, TechnicalRunSpec
from bot_trader.persistence import DocumentRecord, RunRecord

from .auth import Sessions
from .boundary import RequestBoundary
from .credentials import load_credentials

COOKIE = "bot_trader_session"


class Login(FrozenContract):
    token: SecretStr = Field(min_length=24, max_length=1024)


class Comparison(FrozenContract):
    run_ids: list[str] = Field(min_length=2, max_length=10)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    platform = build_services(settings)
    repository = platform.repository
    sessions = Sessions(load_credentials(settings), settings.session_ttl_seconds)
    app = FastAPI(
        title="bot_trader technical platform",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.state.platform = platform
    app.state.sessions = sessions
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=list(settings.allowed_hosts))
    app.add_middleware(RequestBoundary, settings=settings)

    @app.exception_handler(PlatformError)
    async def domain_error(request: Request, error: PlatformError) -> JSONResponse:
        correlation = request.state.correlation_id
        repository.append_audit("http", "request.error", correlation, error.code)
        return JSONResponse(
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "correlation_id": correlation,
                }
            },
            status_code=error.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError) -> JSONResponse:
        # Never serialize rejected request values (they can contain credentials).
        return JSONResponse(
            {
                "error": {
                    "code": "invalid_request",
                    "message": "Request does not satisfy the declared schema.",
                    "correlation_id": request.state.correlation_id,
                }
            },
            status_code=422,
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, error: Exception) -> JSONResponse:
        correlation = request.state.correlation_id
        repository.append_audit(
            "http",
            "request.error",
            correlation,
            "internal_error",
            {"exception_type": type(error).__name__},
        )
        return JSONResponse(
            {
                "error": {
                    "code": "internal_error",
                    "message": "Request failed. Consult the audit correlation ID.",
                    "correlation_id": correlation,
                }
            },
            status_code=500,
        )

    def actor(request: Request) -> Principal:
        session = sessions.get(request.cookies.get(COOKIE))
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            if not secrets.compare_digest(request.headers.get("x-csrf-token", ""), session.csrf):
                raise AccessDenied("A valid session CSRF token is required.")
        return session.principal

    Actor = Annotated[Principal, Depends(actor)]

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "technical"}

    @app.post("/api/session")
    def login(body: Login, response: Response) -> dict[str, JsonValue]:
        identifier, session = sessions.login(body.token.get_secret_value())
        response.set_cookie(
            COOKIE,
            identifier,
            httponly=True,
            secure=settings.secure_cookies,
            samesite="strict",
            max_age=settings.session_ttl_seconds,
            path="/",
        )
        repository.append_audit(session.principal.id, "session.login", "local", "succeeded")
        return {"principal": session.principal.model_dump(mode="json"), "csrf": session.csrf}

    @app.get("/api/session")
    def session(request: Request, principal: Actor) -> dict[str, JsonValue]:
        return {
            "principal": principal.model_dump(mode="json"),
            "csrf": sessions.get(request.cookies.get(COOKIE)).csrf,
        }

    @app.delete("/api/session")
    def logout(request: Request, response: Response, principal: Actor) -> dict[str, bool]:
        sessions.revoke(request.cookies.get(COOKIE, ""))
        response.delete_cookie(
            COOKIE, path="/", httponly=True, samesite="strict", secure=settings.secure_cookies
        )
        repository.append_audit(principal.id, "session.logout", "local", "succeeded")
        return {"signed_out": True}

    @app.get("/api/modules")
    def modules(principal: Actor) -> list[ModuleManifest]:
        platform.policy.require(principal, "modules.read")
        return platform.modules.list()

    @app.get("/api/status")
    def status(principal: Actor) -> dict[str, JsonValue]:
        platform.policy.require(principal, "health.read")
        return {
            "mode": "technical",
            "phase": "III",
            "account_currency": "USD",
            "financial_experiments": 0,
            "live_execution": False,
            "hypotheses": len(repository.list("hypothesis", limit=1000)),
            "datasets": len(repository.list("dataset", limit=1000)),
            "runs": len(repository.list_runs(limit=1000)),
            "counts_limit": 1000,
            "worker": "Separate CLI process; no heartbeat monitored.",
        }

    @app.get("/api/audit")
    def audit(principal: Actor) -> list[dict[str, JsonValue]]:
        platform.policy.require(principal, "audit.read")
        return [record.model_dump(mode="json") for record in repository.list_audit()]

    @app.get("/api/hypotheses")
    def hypotheses(principal: Actor) -> list[DocumentRecord]:
        return platform.hypotheses.list(principal)

    @app.get("/api/hypotheses/{identifier}")
    def hypothesis(identifier: str, principal: Actor) -> DocumentRecord:
        return platform.hypotheses.get(identifier, principal)

    @app.get("/api/datasets")
    def datasets(principal: Actor) -> list[DocumentRecord]:
        return platform.datasets.list(principal)

    @app.post("/api/datasets", status_code=201)
    def create_dataset(body: DatasetSpec, principal: Actor) -> DocumentRecord:
        return platform.datasets.create(body, principal)

    @app.get("/api/datasets/{identifier}")
    def dataset(identifier: str, principal: Actor, version: int | None = None) -> DocumentRecord:
        return platform.datasets.get(identifier, principal, version)

    @app.get("/api/datasets/{identifier}/series")
    def series(
        identifier: str, principal: Actor, version: int | None = None, window: int = 5
    ) -> dict[str, JsonValue]:
        return platform.datasets.series(identifier, principal, version, window)

    @app.get("/api/experiments")
    def runs(principal: Actor) -> list[RunRecord]:
        return platform.lab.list(principal)

    @app.post("/api/experiments", status_code=201)
    def submit_run(body: TechnicalRunSpec, principal: Actor) -> RunRecord:
        return platform.lab.submit(body, principal)

    @app.post("/api/experiments/compare")
    def compare(body: Comparison, principal: Actor) -> dict[str, JsonValue]:
        return platform.lab.compare(body.run_ids, principal)

    @app.get("/api/experiments/{identifier}")
    def run(identifier: str, principal: Actor) -> RunRecord:
        return platform.lab.get(identifier, principal)

    @app.post("/api/experiments/{identifier}/cancel")
    def cancel(identifier: str, principal: Actor) -> RunRecord:
        platform.policy.require(principal, "runs.cancel")
        platform.lab.get(identifier, principal)
        return repository.cancel(identifier, actor_id=principal.id)

    @app.get("/api/experiments/{identifier}/artifacts/{name}")
    def artifact(identifier: str, name: str, principal: Actor) -> Response:
        payload, media_type = platform.lab.artifact(identifier, name, principal)
        return Response(
            payload,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{name}"'},
        )

    @app.get("/api/proposals")
    def proposals(principal: Actor) -> list[DocumentRecord]:
        return platform.lab.proposals(principal)

    @app.post("/api/proposals", status_code=201)
    def propose(body: ResearchProposal, principal: Actor) -> DocumentRecord:
        return platform.lab.propose(body, principal)

    frontend = settings.repository_root / "web" / "dist"
    if (frontend / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=frontend / "assets"), name="assets")

    @app.get("/THIRD_PARTY_NOTICES.txt", response_model=None)
    def third_party_notices() -> FileResponse | JSONResponse:
        path = frontend / "THIRD_PARTY_NOTICES.txt"
        if not path.is_file():
            return JSONResponse({"message": "Build the frontend notices first."}, status_code=503)
        return FileResponse(path, media_type="text/plain")

    @app.get("/", response_model=None)
    def index() -> FileResponse | JSONResponse:
        if not (frontend / "index.html").is_file():
            return JSONResponse(
                {"message": "Build the frontend before opening the dashboard."}, status_code=503
            )
        return FileResponse(frontend / "index.html")

    return app
