from app.models.agent_state import AgentState
from app.models.document_chunk import DocumentChunk
from app.services.interfaces.document_service_interface import (
    IDocumentService,
)


class SearchDocumentsTool:
    """
    Tool responsible for retrieving relevant document chunks
    for a user's question.
    """

    def __init__(
        self,
        document_service: IDocumentService,
    ) -> None:
        self._document_service = document_service

    async def invoke(
        self,
        *,
        state: AgentState,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        """
        Search plan documents relevant to the user's query.
        """

        return await self._document_service.search_documents(
            plan_context=state.plan_context,
            query=query,
            top_k=top_k,
        )