from app.qdrant.qdrant_client_factory import (
    get_qdrant_client,
)
from app.qdrant.qdrant_collection_manager import (
    QdrantCollectionManager,
)


async def initialize_qdrant() -> None:
    """
    Initializes all Qdrant collections required by the application.
    """

    client = get_qdrant_client()

    manager = QdrantCollectionManager(
        client=client,
    )

    await manager.initialize()