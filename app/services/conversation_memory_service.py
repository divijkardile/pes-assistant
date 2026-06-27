# app/services/conversation_memory_service.py

from datetime import UTC, datetime

from app.agents.memory.conversation_summary_agent import (
    ConversationSummaryAgent,
)
from app.models.agent_state import AgentState


class ConversationMemoryService:

    SUMMARY_INTERVAL = 10

    def __init__(
        self,
        *,
        summary_agent: ConversationSummaryAgent,
    ) -> None:
        self._summary_agent = summary_agent

    async def update_summary(
        self,
        *,
        state: AgentState,
    ) -> None:
        """
        Incrementally updates the conversation summary every
        SUMMARY_INTERVAL new messages.
        """

        new_message_count = (
            len(state.messages)
            - state.conversation_summary.summarized_message_count
        )

        if new_message_count < self.SUMMARY_INTERVAL:
            return

        summary = await self._summary_agent.summarize(
            state=state,
        )

        state.conversation_summary.summary = summary

        state.conversation_summary.summarized_message_count = (
            len(state.messages)
        )

        state.conversation_summary.last_updated = datetime.now(
            UTC,
        )

    async def force_update(
        self,
        *,
        state: AgentState,
    ) -> None:
        """
        Forces a summary refresh regardless of the number of
        new messages.
        """

        summary = await self._summary_agent.summarize(
            state=state,
        )

        state.conversation_summary.summary = summary

        state.conversation_summary.summarized_message_count = (
            len(state.messages)
        )

        state.conversation_summary.last_updated = datetime.now(
            UTC,
        )

    async def get_summary(
        self,
        *,
        state: AgentState,
    ) -> str:
        return state.conversation_summary.summary