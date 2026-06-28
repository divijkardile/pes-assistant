from openai import AsyncOpenAI

from app.config.settings import get_settings
from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)


class OpenAIEmbeddingProvider(
    EmbeddingProvider,
):

    def __init__(self) -> None:
        settings = get_settings()

        self._model = (
            settings.openai_embedding_model
        )

        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self._client.embeddings.create(
            model=self._model,
            input=text,
        )

        return response.data[0].embedding