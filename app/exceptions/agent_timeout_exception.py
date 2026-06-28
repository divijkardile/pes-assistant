from app.exceptions.base_exception import PESAssistantException


class AgentTimeoutException(PESAssistantException):
    """Raised when an agent execution exceeds the timeout threshold."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="AGENT_TIMEOUT_ERROR",
        )
