# app/qdrant/qdrant_collection_manager.py

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PayloadSchemaType,
    VectorParams,
)

from app.qdrant.collections import QdrantCollection
from app.qdrant.constants import (
    DOCUMENT_VECTOR_SIZE,
    SEMANTIC_CACHE_VECTOR_SIZE,
)


class QdrantCollectionManager:

    def __init__(
        self,
        *,
        client: AsyncQdrantClient,
    ) -> None:
        self._client = client

    async def initialize(self) -> None:

        await self._create_semantic_cache_collection()

        await self._create_document_collection()

    async def _create_semantic_cache_collection(
        self,
    ) -> None:

        exists = await self._client.collection_exists(
            QdrantCollection.SEMANTIC_CACHE,
        )

        if exists:
            return

        await self._client.create_collection(
            collection_name=QdrantCollection.SEMANTIC_CACHE,
            vectors_config=VectorParams(
                size=SEMANTIC_CACHE_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        await self._client.create_payload_index(
            collection_name=QdrantCollection.SEMANTIC_CACHE,
            field_name="plan_num",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        await self._client.create_payload_index(
            collection_name=QdrantCollection.SEMANTIC_CACHE,
            field_name="user_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

    async def _create_document_collection(
        self,
    ) -> None:

        exists = await self._client.collection_exists(
            QdrantCollection.DOCUMENTS,
        )

        if exists:
            return

        await self._client.create_collection(
            collection_name=QdrantCollection.DOCUMENTS,
            vectors_config=VectorParams(
                size=DOCUMENT_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )