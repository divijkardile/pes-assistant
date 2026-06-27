from app.exceptions.base_exception import PESAssistantException


class ValidationException(PESAssistantException):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str,
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=details,
        )