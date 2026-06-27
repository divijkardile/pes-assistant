from enum import StrEnum


class QdrantCollection(StrEnum):
    """
    Qdrant collections used by the application.
    """

    SEMANTIC_CACHE = "semantic_cache"

    DOCUMENTS = "documents"