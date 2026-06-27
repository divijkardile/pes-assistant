import asyncio
import logging

from strands import Agent
from strands.models.ollama import OllamaModel

from app.agents.base.base_agent import BaseAgent
from app.agents.data.data_agent import DataAgent
from app.agents.document.document_agent import DocumentAgent
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState
from app.prompts.orchestrator_prompt import SYSTEM_PROMPT
from app.utils.context_builder import ContextBuilder


class OrchestratorAgent(BaseAgent):
    """
    Lead agent responsible for coordinating specialist agents,
    reviewing their responses and generating the final answer.
    """

    def __init__(
        self,
        *,
        logger: logging.Logger,
        ollama_host: str,
        model_id: str,
        data_agent: DataAgent,
        document_agent: DocumentAgent,
    ) -> None:

        super().__init__(
            logger=logger,
            agent=Agent(
                model=OllamaModel(
                    host=ollama_host,
                    model_id=model_id,
                ),
                system_prompt=SYSTEM_PROMPT,
            ),
        )

        self._data_agent = data_agent
        self._document_agent = document_agent

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
    ) -> str:
        """
        Execute specialist agents, review their responses and
        generate the final response.
        """

        self._logger.info(
            "Executing OrchestratorAgent for session '%s'.",
            state.session_id,
        )

        # Clear previous specialist responses for the current request.
        state.agent_responses.clear()

        data_task = self._data_agent.invoke(
            state=state,
            user_message=user_message,
        )

        document_task = self._document_agent.invoke(
            state=state,
            user_message=user_message,
        )

        data_response, document_response = await asyncio.gather(
            data_task,
            document_task,
        )

        specialist_context = ContextBuilder.from_agent_responses(
            [
                data_response,
                document_response,
            ]
        )

        prompt = f"""
            You are the lead retirement plan assistant.

            Your job is to review the specialist responses below.

            Tasks:
            1. Check whether both specialists answered correctly.
            2. Resolve conflicts if they disagree.
            3. Prefer structured plan data when it conflicts with documents.
            4. If document evidence provides additional clarification, include it.
            5. Produce one complete response for the participant.

            Specialist Responses
            ====================

            {specialist_context}

            Original User Question
            ======================

            {user_message}

            Return only the final answer.
        """

        answer = await self._execute(prompt)

        self._logger.info(
            "OrchestratorAgent completed for session '%s'.",
            state.session_id,
        )

        return answer