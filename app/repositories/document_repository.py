from pathlib import Path
import httpx

from app.models.document_chunk import DocumentChunk
from app.repositories.interfaces.document_repository_interface import (
    IDocumentRepository,
)


class DocumentRepository(IDocumentRepository):
    """
    Repository responsible for searching indexed plan documents.

    NOTE:
    This is the abstraction layer over the vector store.
    Replace the TODO section with Qdrant/FAISS/Azure AI Search later.
    """

    def __init__(
        self,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._http_client = http_client

    async def search_documents(
        self,
        *,
        plan_number: str,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        # ------------------------------------------------------------------
        # TODO:
        #
        # Replace this implementation with vector search.
        #
        # Example:
        #
        # 1. Generate embedding for query
        # 2. Filter by plan_number
        # 3. Retrieve top_k chunks
        # 4. Map to DocumentChunk
        #
        # return await self._vector_store.search(...)
        # ------------------------------------------------------------------

        return []