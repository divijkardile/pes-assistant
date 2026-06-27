import uuid
from datetime import UTC, datetime, timedelta

from app.exceptions.session_exception import SessionException
from app.exceptions.session_not_found_exception import (
    SessionNotFoundException,
)
from app.models.agent_state import AgentState
from app.models.plan_context import PlanContext
from app.services.interfaces.session_manager_interface import (
    ISessionManager,
)


class SessionManager(ISessionManager):

    def __init__(
        self,
        *,
        session_timeout_minutes: int,
    ) -> None:

        self._timeout = timedelta(
            minutes=session_timeout_minutes,
        )

        self._sessions: dict[str, AgentState] = {}

        self._last_access: dict[str, datetime] = {}

    async def create_session(
        self,
        *,
        plan_context: PlanContext,
    ) -> AgentState:

        session_id = str(uuid.uuid4())

        state = AgentState(
            session_id=session_id,
            correlation_id=str(uuid.uuid4()),
            plan_context=plan_context,
        )

        self._sessions[session_id] = state
        self._last_access[session_id] = datetime.now(UTC)

        return state

    async def get_session(
        self,
        session_id: str,
    ) -> AgentState:

        state = self._sessions.get(session_id)

        if state is None:
            raise SessionNotFoundException(
                session_id=session_id,
            )

        last_access = self._last_access.get(
            session_id,
        )

        if (
            last_access is not None
            and datetime.now(UTC) - last_access > self._timeout
        ):
            await self.end_session(
                session_id,
            )

            raise SessionException(
                f"Session '{session_id}' has expired."
            )

        self._last_access[session_id] = datetime.now(
            UTC,
        )

        return state

    async def update_session(
        self,
        state: AgentState,
    ) -> None:

        if state.session_id not in self._sessions:
            raise SessionNotFoundException(
                session_id=state.session_id,
            )

        self._sessions[state.session_id] = state
        self._last_access[state.session_id] = datetime.now(
            UTC,
        )

    async def end_session(
        self,
        session_id: str,
    ) -> None:

        if session_id not in self._sessions:
            raise SessionNotFoundException(
                session_id=session_id,
            )

        del self._sessions[session_id]
        del self._last_access[session_id]