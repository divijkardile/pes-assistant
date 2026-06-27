from abc import ABC, abstractmethod

from app.models.document_chunk import DocumentChunk
from app.models.plan_context import PlanContext


class IDocumentService(ABC):
    """Service responsible for document search."""

    @abstractmethod
    async def search_documents(
        self,
        *,
        plan_context: PlanContext,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        raise NotImplementedError