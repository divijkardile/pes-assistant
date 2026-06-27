from abc import ABC, abstractmethod

from app.models.document_chunk import DocumentChunk


class IDocumentRepository(ABC):
    """Repository responsible for searching indexed plan documents."""

    @abstractmethod
    async def search_documents(
        self,
        *,
        plan_number: str,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        raise NotImplementedError