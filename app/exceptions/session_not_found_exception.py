from app.exceptions.base_exception import PESAssistantException


class SessionNotFoundException(PESAssistantException):
    """Raised when a session cannot be found."""

    def __init__(
        self,
        session_id: str,
    ) -> None:
        super().__init__(
            message=f"Session '{session_id}' was not found.",
            error_code="SESSION_NOT_FOUND",
            details={
                "session_id": session_id,
            },
        )