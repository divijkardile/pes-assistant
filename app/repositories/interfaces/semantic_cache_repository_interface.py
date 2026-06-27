from abc import ABC, abstractmethod

from app.models.semantic_cache_entry import (
    SemanticCacheEntry,
)


class ISemanticCacheRepository(ABC):

    @abstractmethod
    async def search(
        self,
        *,
        embedding: list[float],
        plan_num: str,
        user_id: str,
        similarity_threshold: float,
    ) -> SemanticCacheEntry | None:
        ...

    @abstractmethod
    async def save(
        self,
        entry: SemanticCacheEntry,
    ) -> None:
        ...

    @abstractmethod
    async def delete(
        self,
        *,
        plan_num: str,
        user_id: str,
    ) -> None:
        ...