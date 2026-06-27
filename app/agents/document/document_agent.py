import logging

from strands import Agent
from strands.models.ollama import OllamaModel

from app.agents.base.base_agent import BaseAgent
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState
from app.prompts.document_agent_prompt import SYSTEM_PROMPT
from app.tools.search_documents_tool import SearchDocumentsTool
from app.utils.context_builder import ContextBuilder


class DocumentAgent(BaseAgent):
    """
    AI specialist responsible for answering questions
    using retrieved documents.
    """

    def __init__(
        self,
        *,
        logger: logging.Logger,
        ollama_host: str,
        model_id: str,
        search_documents_tool: SearchDocumentsTool,
    ) -> None:

        self._search_documents_tool = search_documents_tool

        agent = Agent(
            model=OllamaModel(
                host=ollama_host,
                model_id=model_id,
            ),
            system_prompt=SYSTEM_PROMPT,
        )

        super().__init__(
            logger=logger,
            agent=agent,
        )

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
        top_k: int = 5,
    ) -> AgentResponse:

        chunks = await self._search_documents_tool.invoke(
            state=state,
            query=user_message,
            top_k=top_k,
        )

        context = ContextBuilder.from_document_chunks(
            chunks,
        )

        prompt = f"""
            Context
            -------
            {context}

            User Question
            -------------
            {user_message}

            Instructions
            ------------
            Answer ONLY from the supplied documents.
            If the answer is unavailable, clearly say so.
            Return only the answer.
        """

        answer = await self._execute(prompt)

        response = AgentResponse(
            agent_name=self.__class__.__name__,
            answer=answer,
            sources=[
                chunk.document_name
                for chunk in chunks
            ],
        )

        state.add_agent_response(response)

        return response