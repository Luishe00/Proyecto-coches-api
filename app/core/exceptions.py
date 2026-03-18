class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


class EntityNotFoundError(AppException):
    """Target entity not found in the system."""
    def __init__(self, detail: str = "Entity not found"):
        super().__init__(detail=detail, status_code=404)


class CredentialsError(AppException):
    """Authentication failed."""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(detail=detail, status_code=401)


class PermissionDeniedError(AppException):
    """User does not have required permissions."""
    def __init__(self, detail: str = "The user doesn't have enough privileges"):
        super().__init__(detail=detail, status_code=403)


class ConflictError(AppException):
    """Operation conflicts with the current state (e.g., duplicate)."""
    def __init__(self, detail: str = "Entity already exists"):
        super().__init__(detail=detail, status_code=400)
