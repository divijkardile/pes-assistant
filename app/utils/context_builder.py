from app.models.agent_response import AgentResponse
from app.models.document_chunk import DocumentChunk
from app.models.plan_data import PlanData


class ContextBuilder:
    """Builds LLM-friendly context from application models."""

    @staticmethod
    def from_plan_data(plan_data: PlanData) -> str:
        """Build context from structured plan data."""

        sections: list[str] = [
            "# PLAN DATA",
            "",
        ]

        sections.append(f"Plan Number: {plan_data.plan_number}")
        sections.append(f"User Id: {plan_data.user_id}")
        sections.append("")

        for section_name, section_value in plan_data.data.items():
            sections.append(f"## {section_name}")
            sections.append(str(section_value))
            sections.append("")

        return "\n".join(sections)

    @staticmethod
    def from_document_chunks(
        document_chunks: list[DocumentChunk],
    ) -> str:
        """Build context from retrieved document chunks."""

        sections: list[str] = [
            "# DOCUMENT SEARCH RESULTS",
            "",
        ]

        for index, chunk in enumerate(document_chunks, start=1):
            sections.append(f"## Document {index}")
            sections.append(f"Document Name: {chunk.document_name}")

            if chunk.page_number is not None:
                sections.append(f"Page Number: {chunk.page_number}")

            if chunk.score is not None:
                sections.append(f"Relevance Score: {chunk.score:.2f}")

            sections.append("")
            sections.append(chunk.content)
            sections.append("")

        return "\n".join(sections)

    @staticmethod
    def from_agent_responses(
        responses: list[AgentResponse],
    ) -> str:
        """Build context from specialist agent responses."""

        sections: list[str] = [
            "# SPECIALIST AGENT RESPONSES",
            "",
        ]

        for response in responses:
            sections.append(f"## {response.agent_name}")
            sections.append(f"Answer: {response.answer}")
            sections.append(f"Confidence: {response.confidence}")

            if response.sources:
                sections.append(
                    f"Sources: {', '.join(response.sources)}"
                )

            sections.append(
                f"Requires Review: {response.requires_review}"
            )

            sections.append(
                f"Needs More Information: {response.needs_more_information}"
            )

            if response.metadata:
                sections.append("Metadata:")
                for key, value in response.metadata.items():
                    sections.append(f"- {key}: {value}")

            sections.append("")

        return "\n".join(sections)