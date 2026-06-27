import uuid

from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)
from app.models.semantic_cache_entry import (
    SemanticCacheEntry,
)
from app.repositories.interfaces.semantic_cache_repository_interface import (
    ISemanticCacheRepository,
)


class SemanticCacheService:
    """
    Semantic cache backed by a vector repository.
    """

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_repository: ISemanticCacheRepository,
        similarity_threshold: float,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_repository = vector_repository
        self._similarity_threshold = (
            similarity_threshold
        )

    async def get(
        self,
        *,
        plan_num: str,
        user_id: str,
        question: str,
    ) -> str | None:

        embedding = await self._embedding_provider.embed(
            question,
        )

        match = await self._vector_repository.search(
            embedding=embedding,
            plan_num=plan_num,
            user_id=user_id,
            similarity_threshold=self._similarity_threshold,
        )

        if match is None:
            return None

        return match.response

    async def set(
        self,
        *,
        plan_num: str,
        user_id: str,
        question: str,
        response: str,
    ) -> None:

        embedding = await self._embedding_provider.embed(
            question,
        )

        await self._vector_repository.delete(
            plan_num=plan_num,
            user_id=user_id,
        )

        await self._vector_repository.save(
            SemanticCacheEntry(
                id=str(uuid.uuid4()),
                plan_num=plan_num,
                user_id=user_id,
                question=question,
                embedding=embedding,
                response=response,
            )
        )