# app/llm/providers/ollama_embedding_provider.py

from ollama import AsyncClient

from app.config.settings import get_settings
from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Generates embeddings using Ollama.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._client = AsyncClient(
            host=settings.ollama_host,
        )

        self._model = settings.ollama_embedding_model

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        response = await self._client.embeddings(
            model=self._model,
            prompt=text,
        )

        return response["embedding"]