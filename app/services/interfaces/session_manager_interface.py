from abc import ABC, abstractmethod

from app.models.agent_state import AgentState
from app.models.plan_context import PlanContext


class ISessionManager(ABC):

    @abstractmethod
    async def create_session(
        self,
        plan_context: PlanContext,
    ) -> AgentState:
        raise NotImplementedError

    @abstractmethod
    async def get_session(
        self,
        session_id: str,
    ) -> AgentState:
        raise NotImplementedError

    @abstractmethod
    async def update_session(
        self,
        state: AgentState,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def end_session(
        self,
        session_id: str,
    ) -> None:
        raise NotImplementedError