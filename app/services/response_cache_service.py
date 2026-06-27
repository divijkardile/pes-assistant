import hashlib
from datetime import UTC, datetime, timedelta

from app.models.cached_response import CachedResponse


class ResponseCacheService:
    """
    In-memory cache for AI responses.

    Can later be replaced with Redis without changing callers.
    """

    def __init__(
        self,
        *,
        ttl_minutes: int = 30,
    ) -> None:
        self._ttl = timedelta(minutes=ttl_minutes)
        self._cache: dict[str, CachedResponse] = {}

    def _hash(
        self,
        *,
        plan_num: str,
        user_id: str,
        question: str,
    ) -> str:
        value = (
            f"{plan_num}|"
            f"{user_id}|"
            f"{question.strip().lower()}"
        )

        return hashlib.sha256(
            value.encode("utf-8"),
        ).hexdigest()

    async def get(
        self,
        *,
        plan_num: str,
        user_id: str,
        question: str,
    ) -> str | None:

        key = self._hash(
            plan_num=plan_num,
            user_id=user_id,
            question=question,
        )

        cached = self._cache.get(key)

        if cached is None:
            return None

        if datetime.now(UTC) - cached.created_at > self._ttl:
            del self._cache[key]
            return None

        return cached.response

    async def set(
        self,
        *,
        plan_num: str,
        user_id: str,
        question: str,
        response: str,
    ) -> None:

        key = self._hash(
            plan_num=plan_num,
            user_id=user_id,
            question=question,
        )

        self._cache[key] = CachedResponse(
            question_hash=key,
            response=response,
        )