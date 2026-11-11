"""Explicit dependency composition and typed in-process events; no dynamic imports."""

from collections.abc import Callable

from pydantic import JsonValue

from .contracts import Event, ModuleManifest
from .errors import Conflict, NotFound

Capability = Callable[[dict[str, JsonValue]], JsonValue]
EventHandler = Callable[[Event], None]


class Registry:
    def __init__(self) -> None:
        self._modules: dict[str, ModuleManifest] = {}
        self._capabilities: dict[tuple[str, str], Capability] = {}

    def register(self, manifest: ModuleManifest) -> None:
        if manifest.id in self._modules:
            raise Conflict("Module is already registered.")
        self._modules[manifest.id] = manifest

    def validate(self) -> None:
        visited: set[str] = set()
        active: set[str] = set()

        def visit(module_id: str) -> None:
            if module_id not in self._modules:
                raise Conflict("A declared module dependency is missing.")
            if module_id in active:
                raise Conflict("Module dependencies contain a cycle.")
            if module_id in visited:
                return
            active.add(module_id)
            for dependency in self._modules[module_id].dependencies:
                visit(dependency)
            active.remove(module_id)
            visited.add(module_id)

        for module_id in self._modules:
            visit(module_id)

    def list(self) -> list[ModuleManifest]:
        self.validate()
        return [self._modules[key] for key in sorted(self._modules)]

    def add_capability(self, module_id: str, name: str, handler: Capability) -> None:
        if module_id not in self._modules:
            raise NotFound("Module is not registered.")
        if self._modules[module_id].status != "operational":
            raise Conflict("Inactive module cannot expose an executable capability.")
        key = (module_id, name)
        if key in self._capabilities:
            raise Conflict("Capability is already registered.")
        self._capabilities[key] = handler
        module = self._modules[module_id]
        if name not in module.capabilities:
            self._modules[module_id] = module.model_copy(
                update={"capabilities": (*module.capabilities, name)}
            )

    def call(self, module_id: str, name: str, payload: dict[str, JsonValue]) -> JsonValue:
        self.validate()
        handler = self._capabilities.get((module_id, name))
        if handler is None:
            raise NotFound("Executable capability is not registered.")
        return handler(payload)


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, kind: str, handler: EventHandler) -> None:
        self._handlers.setdefault(kind, []).append(handler)

    def publish(self, event: Event) -> None:
        for handler in tuple(self._handlers.get(event.kind, ())):
            handler(event)
