import math
from datetime import UTC, datetime, timedelta

from app.models.semantic_cache_entry import (
    SemanticCacheEntry,
)
from app.repositories.interfaces.semantic_cache_repository_interface import (
    ISemanticCacheRepository,
)


class InMemoryVectorRepository(ISemanticCacheRepository):

    def __init__(
        self,
        *,
        ttl_minutes: int,
    ) -> None:
        self._ttl = timedelta(
            minutes=ttl_minutes,
        )

        self._entries: list[
            SemanticCacheEntry
        ] = []

    async def search(
        self,
        *,
        embedding: list[float],
        plan_num: str,
        user_id: str,
        similarity_threshold: float,
    ) -> SemanticCacheEntry | None:

        now = datetime.now(UTC)

        self._entries = [
            entry
            for entry in self._entries
            if now - entry.created_at <= self._ttl
        ]

        best_match = None
        best_score = 0.0

        for entry in self._entries:

            if (
                entry.plan_num != plan_num
                or entry.user_id != user_id
            ):
                continue

            score = self._cosine_similarity(
                embedding,
                entry.embedding,
            )

            if score > best_score:
                best_score = score
                best_match = entry

        if (
            best_match is not None
            and best_score >= similarity_threshold
        ):
            return best_match

        return None

    async def save(
        self,
        entry: SemanticCacheEntry,
    ) -> None:

        self._entries.append(
            entry,
        )

    async def delete(
        self,
        *,
        plan_num: str,
        user_id: str,
    ) -> None:

        self._entries = [
            entry
            for entry in self._entries
            if not (
                entry.plan_num == plan_num
                and entry.user_id == user_id
            )
        ]

    @staticmethod
    def _cosine_similarity(
        left: list[float],
        right: list[float],
    ) -> float:

        dot = sum(
            l * r
            for l, r in zip(left, right)
        )

        left_norm = math.sqrt(
            sum(v * v for v in left)
        )

        right_norm = math.sqrt(
            sum(v * v for v in right)
        )

        if left_norm == 0 or right_norm == 0:
            return 0.0

        return dot / (
            left_norm * right_norm
        )