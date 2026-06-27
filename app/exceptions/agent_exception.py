from app.exceptions.base_exception import PESAssistantException


class AgentException(PESAssistantException):
    """Raised when an agent fails to process a request."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="AGENT_ERROR",
        )