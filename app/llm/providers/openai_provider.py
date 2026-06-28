from strands import Agent
from strands.models.openai import OpenAIModel

from app.config.settings import get_settings
from app.llm.interfaces.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):

    def __init__(self):
        settings = get_settings()

        self._model = OpenAIModel(
            client_args={
                "api_key": settings.openai_api_key,
            },
            model_id=settings.openai_model,
        )

    def create_agent(self, **kwargs):
        return Agent(
            model=self._model,
            **kwargs,
        )