from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.agent_response import AgentResponse
from app.models.chat_message import ChatMessage
from app.models.plan_context import PlanContext
from app.models.plan_data import PlanData
from app.models.tool_result import ToolResult


class AgentState(BaseModel):
    """Shared state across the complete agent workflow."""

    session_id: str

    correlation_id: str

    plan_context: PlanContext

    plan_data: PlanData | None = None

    messages: list[ChatMessage] = Field(default_factory=list)

    tool_results: list[ToolResult] = Field(default_factory=list)

    agent_responses: list[AgentResponse] = Field(default_factory=list)

    current_agent: str | None = None

    conversation_summary: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def add_message(
        self,
        message: ChatMessage,
    ) -> None:
        self.messages.append(message)

    def add_agent_response(
        self,
        response: AgentResponse,
    ) -> None:
        self.agent_responses.append(response)