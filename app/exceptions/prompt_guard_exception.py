from app.exceptions.base_exception import PESAssistantException


class PromptGuardException(PESAssistantException):
    """Raised when prompt injection is detected."""

    def __init__(
        self,
        message: str = "Potential prompt injection detected.",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="PROMPT_GUARD_ERROR",
            details=details,
        )