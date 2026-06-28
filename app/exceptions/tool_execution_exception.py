from app.exceptions.base_exception import PESAssistantException


class ToolExecutionException(PESAssistantException):
    """Raised when a tool execution fails or returns invalid data."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="TOOL_EXECUTION_ERROR",
        )
