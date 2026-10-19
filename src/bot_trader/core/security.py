"""Explicit allowlists. Administrator status cannot bypass phase boundaries."""

from .contracts import Partition, Principal
from .errors import AccessDenied

_READ = frozenset(
    {
        "metadata.read",
        "hypotheses.read",
        "datasets.read",
        "datasets.payload",
        "runs.read",
        "artifacts.read",
        "modules.read",
        "audit.read",
        "health.read",
    }
)
_RESEARCH = _READ | {"datasets.create", "runs.create", "runs.cancel", "proposals.create"}
_ALLOWED = {
    "viewer": _READ,
    "researcher": _RESEARCH,
    "admin": _RESEARCH | {"worker.execute", "runs.recover", "sessions.manage"},
    "agent": frozenset({"metadata.read", "hypotheses.read", "modules.read", "proposals.create"}),
}


class Policy:
    def require(
        self,
        principal: Principal,
        action: str,
        *,
        partition: Partition | None = None,
        mode: str = "technical",
    ) -> None:
        if mode != "technical":
            raise AccessDenied("Only technical mode is authorized.")
        if partition == "final" and action not in {"metadata.read", "datasets.read"}:
            raise AccessDenied("Final partition payload is reserved for every role.")
        if action not in _ALLOWED[principal.role]:
            raise AccessDenied()
