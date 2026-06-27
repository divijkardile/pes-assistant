from datetime import UTC, datetime, timedelta

from app.exceptions.session_not_found_exception import (
    SessionNotFoundException,
)
from app.models.agent_state import AgentState
from app.models.plan_context import PlanContext
from app.services.interfaces.session_manager_interface import (
    ISessionManager,
)
from app.utils.id_generator import (
    generate_correlation_id,
    generate_session_id,
)


class SessionManager(ISessionManager):
    """In-memory session manager."""

    def __init__(
        self,
        session_timeout_minutes: int,
    ) -> None:
        self._session_timeout = timedelta(
            minutes=session_timeout_minutes,
        )

        self._sessions: dict[str, AgentState] = {}

    async def create_session(
        self,
        plan_context: PlanContext,
    ) -> AgentState:

        state = AgentState(
            session_id=generate_session_id(),
            correlation_id=generate_correlation_id(),
            plan_context=plan_context,
        )

        self._sessions[state.session_id] = state

        return state

    async def get_session(
        self,
        session_id: str,
    ) -> AgentState:

        state = self._sessions.get(session_id)

        if state is None:
            raise SessionNotFoundException(session_id)

        if self._is_expired(state):
            await self.end_session(session_id)
            raise SessionNotFoundException(session_id)

        state.updated_at = datetime.now(UTC)

        return state

    async def update_session(
        self,
        state: AgentState,
    ) -> None:

        state.updated_at = datetime.now(UTC)

        self._sessions[state.session_id] = state

    async def end_session(
        self,
        session_id: str,
    ) -> None:

        self._sessions.pop(session_id, None)

    def _is_expired(
        self,
        state: AgentState,
    ) -> bool:

        return (
            datetime.now(UTC) - state.updated_at
        ) > self._session_timeout