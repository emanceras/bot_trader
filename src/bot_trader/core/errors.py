"""Safe application errors suitable for serialization at service boundaries."""


class PlatformError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class AccessDenied(PlatformError):
    def __init__(self, message: str = "This action is not authorized.") -> None:
        super().__init__("access_denied", message, 403)


class Conflict(PlatformError):
    def __init__(self, message: str = "The requested state transition conflicts.") -> None:
        super().__init__("conflict", message, 409)


class NotFound(PlatformError):
    def __init__(self, message: str = "The requested record does not exist.") -> None:
        super().__init__("not_found", message, 404)
