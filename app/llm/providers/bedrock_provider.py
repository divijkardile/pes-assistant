from strands import Agent
from strands.models.bedrock import BedrockModel

from app.config.settings import get_settings
from app.llm.interfaces.llm_provider import (
    LLMProvider,
)


class BedrockProvider(LLMProvider):

    def __init__(self) -> None:
        settings = get_settings()

        self._model = BedrockModel(
            region_name=settings.aws_region,
            model_id=settings.bedrock_model,
        )

    def create_agent(
        self,
        **kwargs,
    ) -> Agent:

        return Agent(
            model=self._model,
            **kwargs,
        )