from app.models.chat_message import ChatMessage
from app.models.plan_context import PlanContext
from app.models.requests.chat_request import ChatRequest
from app.models.requests.end_session_request import EndSessionRequest
from app.models.requests.start_session_request import (
    StartSessionRequest,
)
from app.models.responses.chat_response import ChatResponse
from app.models.responses.end_session_response import (
    EndSessionResponse,
)
from app.models.responses.start_session_response import (
    StartSessionResponse,
)
from app.services.interfaces.chat_service_interface import (
    IChatService,
)
from app.services.interfaces.session_manager_interface import (
    ISessionManager,
)
from app.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
)
from app.config.constants import Roles


class ChatService(IChatService):

    def __init__(
        self,
        *,
        session_manager: ISessionManager,
        orchestrator_agent: OrchestratorAgent,
    ) -> None:
        self._session_manager = session_manager
        self._orchestrator_agent = orchestrator_agent

    async def start_session(
        self,
        request: StartSessionRequest,
    ) -> StartSessionResponse:
        
        plan_context = PlanContext(
            plan_number=request.plan_number,
            user_id=request.user_id
        )

        state = await self._session_manager.create_session(
            plan_context=plan_context,
        )

        return StartSessionResponse(
            session_id=state.session_id,
            correlation_id=state.correlation_id,
            message="Session started successfully.",
        )

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        state = await self._session_manager.get_session(
            request.session_id,
        )

        state.messages.append(
            ChatMessage(
                role=Roles.USER,
                content=request.message,
            )
        )

        answer = await self._orchestrator_agent.invoke(
            state=state,
            user_message=request.message,
        )

        state.messages.append(
            ChatMessage(
                role=Roles.ASSISTANT,
                content=answer,
            )
        )

        await self._session_manager.update_session(
            state,
        )

        return ChatResponse(
            session_id=state.session_id,
            response=answer,
        )

    async def end_session(
        self,
        request: EndSessionRequest,
    ) -> EndSessionResponse:

        await self._session_manager.end_session(
            request.session_id,
        )

        return EndSessionResponse(
            message="Session ended successfully.",
        )