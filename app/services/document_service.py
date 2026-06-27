from app.models.document_chunk import DocumentChunk
from app.models.plan_context import PlanContext
from app.repositories.interfaces.document_repository_interface import (
    IDocumentRepository,
)
from app.services.interfaces.document_service_interface import (
    IDocumentService,
)


class DocumentService(IDocumentService):
    """
    Service responsible for searching plan documents.
    """

    def __init__(
        self,
        document_repository: IDocumentRepository,
    ) -> None:
        self._document_repository = document_repository

    async def search_documents(
        self,
        *,
        plan_context: PlanContext,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        return await self._document_repository.search_documents(
            plan_number=plan_context.plan_number,
            query=query,
            top_k=top_k,
        )