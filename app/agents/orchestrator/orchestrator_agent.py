import logging

from app.agents.base.base_agent import BaseAgent
from app.llm.interfaces.llm_provider import LLMProvider
from app.models.agent_state import AgentState
from app.prompts.orchestrator_prompt import SYSTEM_PROMPT


class OrchestratorAgent(BaseAgent):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        llm_provider: LLMProvider,
        data_agent_tool,
        document_agent_tool,
    ) -> None:

        super().__init__(
            logger=logger,
            llm_provider=llm_provider,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                data_agent_tool,
                document_agent_tool,
            ],
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
{state.plan_context.plan_num}

User Id:
{state.plan_context.user_id}

Conversation Summary
====================

{state.conversation_summary.summary or "No conversation summary available."}

Recent Conversation
===================

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
- Searches retirement plan documents.

Rules:

1. Read the conversation summary first.
2. Read the recent conversation.
3. Decide which specialist is required.
4. Use only the required specialist.
5. If both specialists are required, call both.
6. Combine their responses into one participant-friendly answer.
7. Never expose internal implementation details.
8. Never fabricate information.
9. If information is unavailable, clearly state that.
10. Return only the final participant-facing response.
"""

        answer = await self._execute(
            prompt=prompt,
        )

        self._logger.info(
            "OrchestratorAgent completed for session '%s'.",
            state.session_id,
        )

        return answer