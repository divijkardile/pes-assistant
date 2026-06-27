import logging

from strands import Agent
from strands.models.ollama import OllamaModel

from app.agents.base.base_agent import BaseAgent
from app.models.agent_state import AgentState
from app.prompts.orchestrator_prompt import SYSTEM_PROMPT


class OrchestratorAgent(BaseAgent):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        ollama_host: str,
        model_id: str,
        data_agent_tool,
        document_agent_tool,
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
                    data_agent_tool,
                    document_agent_tool,
                ],
            ),
        )

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
    ) -> str:

        self._logger.info(
            "Executing OrchestratorAgent for session '%s'.",
            state.session_id,
        )

        state.agent_responses.clear()

        prompt = f"""
Session Context
===============

Session Id:
{state.session_id}

Plan Number:
{state.plan_context.plan_number}

User Id:
{state.plan_context.user_id}

Conversation History
====================

{state.messages}

Current User Question
=====================

{user_message}

Instructions
============

You are the lead retirement assistant.

You have access to two specialist tools.

Tool 1:
- data_agent
- Retrieves structured participant and plan information.

Tool 2:
- document_agent
- Searches plan documents and explains plan rules.

Rules:

1. Decide yourself which tool(s) are required.
2. Use ONLY the required tool(s).
3. If one tool is sufficient, do not call the other.
4. If both are needed, call both.
5. Review the returned responses.
6. Combine them into one complete answer.
7. Never expose internal implementation.
8. Return only the participant-facing response.
"""

        answer = await self._execute(
            prompt=prompt,
        )

        self._logger.info(
            "OrchestratorAgent completed for session '%s'.",
            state.session_id,
        )

        return answer