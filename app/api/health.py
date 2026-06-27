# app/api/health.py

from fastapi import APIRouter

from app.qdrant.qdrant_client_factory import (
    get_qdrant_client,
)
from app.qdrant.qdrant_health_service import (
    QdrantHealthService,
)

router = APIRouter(
    tags=["Health"],
)


@router.get("/health")
async def health() -> dict:

    qdrant_health = QdrantHealthService(
        client=get_qdrant_client(),
    )

    qdrant_status = await qdrant_health.is_healthy()

    return {
        "status": "healthy" if qdrant_status else "degraded",
        "checks": {
            "qdrant": "UP" if qdrant_status else "DOWN",
        },
    }