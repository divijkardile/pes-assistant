from qdrant_client import AsyncQdrantClient


class QdrantHealthService:
    """
    Performs health checks against Qdrant.
    """

    def __init__(
        self,
        *,
        client: AsyncQdrantClient,
    ) -> None:
        self._client = client

    async def is_healthy(self) -> bool:
        try:
            await self._client.get_collections()
            return True
        except Exception:
            return False