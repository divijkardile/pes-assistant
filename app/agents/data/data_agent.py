import logging

from app.agents.base.base_agent import BaseAgent
from app.exceptions.tool_execution_exception import (
    ToolExecutionException,
)
from app.llm.interfaces.llm_provider import LLMProvider
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState
from app.prompts.data_agent_prompt import SYSTEM_PROMPT
from app.tools.get_plan_data_tool import GetPlanDataTool


class DataAgent(BaseAgent):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        llm_provider: LLMProvider,
        get_plan_data_tool: GetPlanDataTool,
    ) -> None:

        super().__init__(
            logger=logger,
            llm_provider=llm_provider,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                get_plan_data_tool.get_plan_data,
            ],
        )

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
    ) -> AgentResponse:

        self._logger.info(
            "Executing DataAgent for session '%s'.",
            state.session_id,
        )

        prompt = f"""
Participant Context
===================

Plan Number:
{state.plan_context.plan_num}

User Id:
{state.plan_context.user_id}

User Question
=============

{user_message}

Instructions
============

- Always use the get_plan_data tool.
- Use only the structured plan data returned by the tool.
- Never invent information.
- If the requested information is unavailable, clearly state that.
- Return only the participant-facing response.
"""

        try:
            answer = await self._execute(
                prompt=prompt,
            )

            # Validate answer is not empty
            if not answer or answer.strip() == "":
                error_msg = (
                    f"DataAgent returned empty response for "
                    f"session {state.session_id}"
                )
                self._logger.warning(error_msg)
                raise ToolExecutionException(error_msg)

        except ToolExecutionException:
            raise

        except Exception as e:
            error_msg = (
                f"DataAgent execution error for session "
                f"{state.session_id}: {str(e)}"
            )
            self._logger.error(error_msg)
            raise ToolExecutionException(error_msg)

        response = AgentResponse(
            agent_name=self.__class__.__name__,
            answer=answer,
        )

        state.agent_responses.append(
            response,
        )

        self._logger.info(
            "DataAgent completed for session '%s'.",
            state.session_id,
        )

        return response