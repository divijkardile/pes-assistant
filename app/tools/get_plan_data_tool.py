from app.models.agent_state import AgentState
from app.models.plan_data import PlanData
from app.services.interfaces.plan_service_interface import (
    IPlanService,
)


class GetPlanDataTool:
    """
    Tool responsible for retrieving structured plan data.
    """

    def __init__(
        self,
        plan_service: IPlanService,
    ) -> None:
        self._plan_service = plan_service

    async def invoke(
        self,
        *,
        state: AgentState,
        refresh: bool = False,
    ) -> PlanData:
        """
        Returns cached plan data unless refresh is requested.
        """

        if not refresh and state.plan_data is not None:
            return state.plan_data

        plan_data = await self._plan_service.get_plan_data(
            plan_context=state.plan_context,
        )

        state.plan_data = plan_data

        return plan_data