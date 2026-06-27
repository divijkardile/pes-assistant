from strands import tool

from app.models.agent_state import AgentState
from app.services.plan_service import (
    PlanAssistantService,
)


class GetPlanDataTool:

    def __init__(
        self,
        *,
        plan_service: PlanAssistantService,
    ) -> None:
        self._plan_service = plan_service

    @tool
    async def get_plan_data(
        self,
        state: AgentState,
    ):
        """
        Retrieves structured participant and plan information
        for the current conversation.
        """

        return await self._plan_service.get_plan_data(
            plan_context=state.plan_context,
        )