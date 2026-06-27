from app.exceptions.base_exception import (
    PESAssistantException,
)


class EmbeddingProviderException(
    PESAssistantException,
):
    """
    Raised when an unsupported embedding provider is configured.
    """

    def __init__(
        self,
        provider: str,
    ) -> None:
        super().__init__(
            message=(
                f"Unsupported embedding provider: '{provider}'."
            ),
            error_code="INVALID_EMBEDDING_PROVIDER",
        )