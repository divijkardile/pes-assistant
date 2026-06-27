from app.models.agent_response import AgentResponse
from app.models.chat_message import ChatMessage


class ContextBuilder:
    """Builds reusable context for prompts."""

    @staticmethod
    def from_chat_history(
        messages: list[ChatMessage],
        max_messages: int = 10,
    ) -> str:

        if not messages:
            return "No previous conversation."

        history: list[str] = []

        for message in messages[-max_messages:]:
            history.append(
                f"{message.role}: {message.content}"
            )

        return "\n".join(history)

    @staticmethod
    def from_agent_responses(
        responses: list[AgentResponse],
    ) -> str:

        if not responses:
            return "No specialist responses."

        output: list[str] = []

        for response in responses:
            output.append(
                f"""
Agent:
{response.agent_name}

Answer:
{response.answer}
""".strip()
            )

        return "\n\n".join(output)