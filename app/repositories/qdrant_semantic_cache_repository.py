from datetime import UTC, datetime
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
    PointIdsList,
    PointStruct,
)

from app.models.semantic_cache_entry import (
    SemanticCacheEntry,
)
from app.repositories.interfaces.semantic_cache_repository_interface import (
    ISemanticCacheRepository,
)


class QdrantSemanticCacheRepository(
    ISemanticCacheRepository,
):

    def __init__(
        self,
        *,
        client: AsyncQdrantClient,
        collection_name: str,
    ) -> None:
        self._client = client
        self._collection_name = collection_name

    async def search(
        self,
        *,
        embedding: list[float],
        plan_num: str,
        user_id: str,
        similarity_threshold: float,
    ) -> SemanticCacheEntry | None:

        response = await self._client.query_points(
            collection_name=self._collection_name,
            query=embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="plan_num",
                        match=MatchValue(
                            value=plan_num,
                        ),
                    ),
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(
                            value=user_id,
                        ),
                    ),
                ],
            ),
            limit=1,
            score_threshold=similarity_threshold,
        )

        if not response.points:
            return None

        point = response.points[0]
        payload = point.payload

        if payload is None:
            return None

        created_at_value = payload.get("created_at")

        if not isinstance(created_at_value, str):
            created_at = datetime.now(UTC)
        else:
            created_at = datetime.fromisoformat(
                created_at_value,
            )

        return SemanticCacheEntry(
            id=str(payload.get("id", "")),
            plan_num=str(payload.get("plan_num", "")),
            user_id=str(payload.get("user_id", "")),
            question=str(payload.get("question", "")),
            embedding=[],
            response=str(payload.get("response", "")),
            created_at=created_at,
        )

    async def save(
        self,
        entry: SemanticCacheEntry,
    ) -> None:

        await self._client.upsert(
            collection_name=self._collection_name,
            points=[
                PointStruct(
                    id=entry.id,
                    vector=entry.embedding,
                    payload={
                        "id": entry.id,
                        "plan_num": entry.plan_num,
                        "user_id": entry.user_id,
                        "question": entry.question,
                        "response": entry.response,
                        "created_at": entry.created_at.isoformat(),
                    },
                )
            ],
        )

    async def delete(
        self,
        *,
        plan_num: str,
        user_id: str,
    ) -> None:

        records, _ = await self._client.scroll(
            collection_name=self._collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="plan_num",
                        match=MatchValue(
                            value=plan_num,
                        ),
                    ),
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(
                            value=user_id,
                        ),
                    ),
                ],
            ),
            with_vectors=False,
            with_payload=False,
        )

        if not records:
            return

        await self._client.delete(
            collection_name=self._collection_name,
            points_selector=PointIdsList(
                points=[
                    point.id
                    for point in records
                ],
            ),
        )