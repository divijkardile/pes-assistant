from app.config.settings import get_settings
from app.exceptions.embedding_provider_exception import (
    EmbeddingProviderException,
)
from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)
from app.llm.providers.bedrock_embedding_provider import (
    BedrockEmbeddingProvider,
)
from app.llm.providers.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
)


class EmbeddingProviderFactory:

    @staticmethod
    def get_provider() -> EmbeddingProvider:

        settings = get_settings()

        provider = settings.llm_provider.lower()

        match provider:

            case "ollama":
                return OllamaEmbeddingProvider()

            case "bedrock":
                return BedrockEmbeddingProvider()

            case _:
                raise EmbeddingProviderException(
                    provider=provider,
                )