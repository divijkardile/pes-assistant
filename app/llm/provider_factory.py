from app.config.settings import get_settings
from app.exceptions.model_provider_exception import (
    ModelProviderException,
)
from app.llm.interfaces.llm_provider import (
    LLMProvider,
)
from app.llm.providers.bedrock_provider import (
    BedrockProvider,
)
from app.llm.providers.ollama_provider import (
    OllamaProvider,
)

from app.llm.providers.openai_provider import (
    OpenAIProvider
)


class ProviderFactory:

    @staticmethod
    def get_provider() -> LLMProvider:

        settings = get_settings()

        provider = settings.llm_provider.lower()

        match provider:

            case "ollama":
                return OllamaProvider()

            case "bedrock":
                return BedrockProvider()
            
            case "openai":
                return OpenAIProvider()

            case _:
                raise ModelProviderException(
                    provider=provider,
                )