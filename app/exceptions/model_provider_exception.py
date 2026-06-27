from app.exceptions.base_exception import (
    PESAssistantException,
)


class ModelProviderException(
    PESAssistantException,
):
    """
    Raised when an unsupported LLM provider is configured.
    """

    def __init__(
        self,
        provider: str,
    ) -> None:
        super().__init__(
            message=(
                f"Unsupported LLM provider: '{provider}'."
            ),
            error_code="INVALID_LLM_PROVIDER",
        )