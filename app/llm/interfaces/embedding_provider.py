from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Interface for generating text embeddings.
    """

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for the given text.
        """
        raise NotImplementedError