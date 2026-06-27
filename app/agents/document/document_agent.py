import logging

from strands import Agent
from strands.models.ollama import OllamaModel

from app.agents.base.base_agent import BaseAgent
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState
from app.prompts.document_agent_prompt import SYSTEM_PROMPT
from app.tools.search_documents_tool import SearchDocumentsTool


class DocumentAgent(BaseAgent):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        ollama_host: str,
        model_id: str,
        search_documents_tool: SearchDocumentsTool,
    ) -> None:

        super().__init__(
            logger=logger,
            agent=Agent(
                model=OllamaModel(
                    host=ollama_host,
                    model_id=model_id,
                ),
                system_prompt=SYSTEM_PROMPT,
                tools=[
                    search_documents_tool.search_documents,
                ],
            ),
        )

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
    ) -> AgentResponse:

        self._logger.info(
            "Executing DocumentAgent for session '%s'.",
            state.session_id,
        )

        prompt = f"""
Participant Context
===================

Plan Number:
{state.plan_context.plan_number}

User Id:
{state.plan_context.user_id}

User Question
=============

{user_message}

Instructions
============

- Always use the search_documents tool before answering.
- Answer ONLY using the retrieved document content.
- Never invent information.
- If the requested information is unavailable, clearly state that.
- Return only the participant-facing answer.
"""

        answer = await self._execute(
            prompt=prompt,
        )

        response = AgentResponse(
            agent_name=self.__class__.__name__,
            answer=answer,
        )

        state.agent_responses.append(response)

        self._logger.info(
            "DocumentAgent completed for session '%s'.",
            state.session_id,
        )

        return response