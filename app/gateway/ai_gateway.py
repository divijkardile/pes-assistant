from app.gateway.audit_logger import AuditLogger
from app.gateway.prompt_guard import PromptGuard
from app.gateway.request_validator import RequestValidator
from app.gateway.retry_policy import RetryPolicy
from app.models.requests.chat_request import ChatRequest
from app.services.chat_service import ChatService
from app.services.interfaces.session_manager_interface import (
    ISessionManager,
)
from app.gateway.metrics import Metrics


class AIGateway:
    """
    Entry point for all AI chat requests.
    """

    def __init__(
        self,
        *,
        chat_service: ChatService,
        session_manager: ISessionManager,
        retry_policy: RetryPolicy,
    ) -> None:
        self._chat_service = chat_service
        self._session_manager = session_manager
        self._retry_policy = retry_policy

    
    async def handle_chat(
        self,
        request: ChatRequest,
    ):
        start_time = Metrics.start_timer()
        await RequestValidator.validate(request)

        await PromptGuard.validate(request.message)

        agent_state = await self._session_manager.get_session(
            request.session_id,
        )

        AuditLogger.log_request(
            context=agent_state,
            message="Incoming chat request.",
        )

        response = await self._retry_policy.execute(
            self._chat_service.chat,
            request,
        )

        AuditLogger.log_request(
            context=agent_state,
            message="Chat request completed successfully.",
            latency_ms=Metrics.elapsed_ms(start_time),
        )

        return response