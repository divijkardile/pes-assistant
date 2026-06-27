import logging

from strands import Agent
from strands.models.ollama import OllamaModel

from app.agents.base.base_agent import BaseAgent
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState
from app.prompts.data_agent_prompt import SYSTEM_PROMPT
from app.tools.get_plan_data_tool import GetPlanDataTool
from app.utils.context_builder import ContextBuilder


class DataAgent(BaseAgent):
    """
    AI specialist responsible for answering questions
    using structured plan data.
    """

    def __init__(
        self,
        *,
        logger: logging.Logger,
        ollama_host: str,
        model_id: str,
        get_plan_data_tool: GetPlanDataTool,
    ) -> None:

        self._get_plan_data_tool = get_plan_data_tool

        agent = Agent(
            model=OllamaModel(
                host=ollama_host,
                model_id=model_id,
            ),
            system_prompt=SYSTEM_PROMPT,
        )

        super().__init__(
            logger=logger,
            agent=agent,
        )

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
        refresh: bool = False,
    ) -> AgentResponse:

        self._logger.info(
            "Invoking DataAgent."
        )

        if refresh or state.plan_data is None:
            state.plan_data = await self._get_plan_data_tool.invoke(
                state=state,
            )

        context = ContextBuilder.from_plan_data(
            state.plan_data,
        )

        prompt = f"""
            Context
            -------
            {context}

            User Question
            -------------
            {user_message}

            Instructions
            ------------
            Answer ONLY using the plan data.
            If the answer cannot be determined, say so.
            Return only the answer.
        """

        answer = await self._execute(prompt)

        response = AgentResponse(
            agent_name=self.__class__.__name__,
            answer=answer,
        )

        state.add_agent_response(response)

        return response