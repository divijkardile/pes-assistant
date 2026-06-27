from app.exceptions.base_exception import PESAssistantException


class ServiceException(PESAssistantException):
    """Raised when a service operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="SERVICE_ERROR",
        )