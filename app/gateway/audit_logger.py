import logging
from typing import Any

from app.models.agent_state import AgentState

logger = logging.getLogger("ai_gateway")


class AuditLogger:
    """
    Centralized audit logger for AI requests.
    """

    @staticmethod
    def _build_log_context(
        context: AgentState,
        **extra: Any,
    ) -> dict[str, Any]:
        return {
            "user_id": context.plan_context.user_id,
            "session_id": context.session_id,
            "correlation_id": context.correlation_id,
            "plan_num": context.plan_context.plan_num,
            "conversation_turn": len(context.messages) + 1,
            "prompt_tokens": context.token_usage.prompt_tokens,
            "completion_tokens": context.token_usage.completion_tokens,
            "total_tokens": context.token_usage.total_tokens,
            **extra,
        }

    @classmethod
    def log_request(
        cls,
        context: AgentState,
        message: str,
        **extra: Any,
    ) -> None:
        logger.info(
            message,
            extra=cls._build_log_context(
                context,
                **extra,
            ),
        )

    @classmethod
    def log_error(
        cls,
        context: AgentState,
        message: str,
        exception: Exception,
        **extra: Any,
    ) -> None:
        logger.exception(
            message,
            exc_info=exception,
            extra=cls._build_log_context(
                context,
                **extra,
            ),
        )