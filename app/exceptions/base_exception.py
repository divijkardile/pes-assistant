from typing import Any


class PESAssistantException(Exception):
    """Base exception for the PES Assistant application."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "PES_ASSISTANT_ERROR",
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(message)