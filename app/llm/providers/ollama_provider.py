from strands import Agent
from strands.models.ollama import OllamaModel

from app.config.settings import get_settings
from app.llm.interfaces.llm_provider import (
    LLMProvider,
)


class OllamaProvider(LLMProvider):

    def __init__(self) -> None:
        settings = get_settings()

        self._model = OllamaModel(
            host=settings.ollama_host,
            model_id=settings.ollama_model,
        )

    def create_agent(
        self,
        **kwargs,
    ) -> Agent:

        return Agent(
            model=self._model,
            **kwargs,
        )