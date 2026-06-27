from app.exceptions.base_exception import PESAssistantException


class SessionException(PESAssistantException):
    """Raised when a chat session is invalid or unavailable."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="SESSION_ERROR",
        )