from strands import tool

from app.models.agent_state import AgentState
from app.services.interfaces.document_service_interface import (
    IDocumentService,
)


class SearchDocumentsTool:

    def __init__(
        self,
        document_service: IDocumentService,
    ) -> None:
        self._document_service = document_service

    @tool(
        name="search_documents",
        description="""
Search retirement plan documents.

Use this tool whenever information is required from:
- Summary Plan Description (SPD)
- Plan rules
- Notices
- Policies
- Legal wording
- PDFs
- Any other plan documents
""",
    )
    async def search_documents(
        self,
        state: AgentState,
        query: str,
        top_k: int = 5,
    ) -> str:

        chunks = await self._document_service.search_documents(
            plan_context=state.plan_context,
            query=query,
            top_k=top_k,
        )

        if not chunks:
            return "No relevant documents found."

        results: list[str] = []

        for chunk in chunks:
            results.append(
                f"""
Document: {chunk.document_name}
Page: {chunk.page_number}

{chunk.content}
""".strip()
            )

        return "\n\n".join(results)