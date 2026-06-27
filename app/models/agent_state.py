from typing import Any

from pydantic import BaseModel, Field

from app.gateway.token_usage import TokenUsage
from app.models.agent_response import AgentResponse
from app.models.chat_message import ChatMessage
from app.models.conversation_summary import (
    ConversationSummary,
)
from app.models.plan_context import PlanContext


class AgentState(BaseModel):
    """
    Shared state for the lifetime of a chat session.
    """

    session_id: str

    correlation_id: str

    plan_context: PlanContext

    conversation_summary: ConversationSummary = Field(
        default_factory=ConversationSummary,
    )

    messages: list[ChatMessage] = Field(
        default_factory=list,
    )

    agent_responses: list[AgentResponse] = Field(
        default_factory=list,
    )

    plan_data: Any = None

    tool_results: dict[str, Any] = Field(
        default_factory=dict,
    )

    token_usage: TokenUsage = Field(
        default_factory=TokenUsage,
    )