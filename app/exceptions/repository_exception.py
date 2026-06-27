from app.exceptions.base_exception import PESAssistantException


class RepositoryException(PESAssistantException):
    """Raised when a repository operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code="REPOSITORY_ERROR",
        )