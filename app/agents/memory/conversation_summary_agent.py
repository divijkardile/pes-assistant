# app/agents/memory/conversation_summary_agent.py

import logging

from app.agents.base.base_agent import BaseAgent
from app.exceptions.agent_exception import AgentException
from app.llm.interfaces.llm_provider import (
    LLMProvider,
)
from app.models.agent_state import AgentState
from app.prompts.conversation_summary_prompt import (
    SYSTEM_PROMPT,
)


class ConversationSummaryAgent(BaseAgent):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        llm_provider: LLMProvider,
    ) -> None:

        super().__init__(
            logger=logger,
            llm_provider=llm_provider,
            system_prompt=SYSTEM_PROMPT,
        )

    async def summarize(
        self,
        *,
        state: AgentState,
    ) -> str:

        self._logger.info(
            "Generating conversation summary for session '%s'.",
            state.session_id,
        )

        new_messages = state.messages[
            state.conversation_summary.summarized_message_count :
        ]

        previous_summary = (
            state.conversation_summary.summary
            or "No previous summary."
        )

        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in new_messages
        )

        prompt = f"""
Previous Summary
================

{previous_summary}

New Messages
============

{conversation}

Instructions
============

Update the previous summary using ONLY the new messages.

Preserve:
- Participant goals
- Important retirement plan details
- Decisions made
- Outstanding questions

Keep the summary concise.

Return only the updated summary.
"""

        try:
            summary = await self._execute(
                prompt=prompt,
            )

            # Validate summary is not empty
            if not summary or summary.strip() == "":
                error_msg = (
                    f"Summary generation failed for session "
                    f"{state.session_id} - empty response"
                )
                self._logger.error(error_msg)
                # Return previous summary as fallback
                return previous_summary

        except Exception as e:
            error_msg = (
                f"Summary generation error for session "
                f"{state.session_id}: {str(e)}"
            )
            self._logger.error(error_msg)
            # Return previous summary as fallback instead of crashing
            return previous_summary

        self._logger.info(
            "Conversation summary generated for session '%s'.",
            state.session_id,
        )

        return summary