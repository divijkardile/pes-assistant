import asyncio
import logging
from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

from app.config.settings import get_settings
from app.exceptions.agent_exception import AgentException
from app.exceptions.agent_timeout_exception import (
    AgentTimeoutException,
)
from app.llm.interfaces.llm_provider import (
    LLMProvider,
)

T = TypeVar("T", bound=BaseModel)


class BaseAgent(ABC):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        llm_provider: LLMProvider,
        system_prompt: str,
        tools: list | None = None,
    ) -> None:
        self._logger = logger

        self._agent = llm_provider.create_agent(
            system_prompt=system_prompt,
            tools=tools or [],
        )

    async def _execute(
        self,
        prompt: str,
    ) -> str:

        self._logger.info(
            "%s executing.",
            self.__class__.__name__,
        )

        settings = get_settings()
        timeout_seconds = settings.agent_timeout_seconds

        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(self._agent, prompt),
                timeout=timeout_seconds,
            )
            return str(response)

        except asyncio.TimeoutError:
            error_msg = (
                f"{self.__class__.__name__} execution timeout "
                f"after {timeout_seconds} seconds"
            )
            self._logger.error(error_msg)
            raise AgentTimeoutException(error_msg)

        except Exception as e:
            error_msg = (
                f"{self.__class__.__name__} execution failed: {str(e)}"
            )
            self._logger.error(error_msg)
            raise AgentException(error_msg)

    async def _execute_structured(
        self,
        *,
        prompt: str,
        response_model: type[T],
    ) -> T:

        self._logger.info(
            "%s executing structured output.",
            self.__class__.__name__,
        )

        settings = get_settings()
        timeout_seconds = settings.agent_timeout_seconds

        try:
            return await asyncio.wait_for(
                asyncio.to_thread(
                    self._agent.structured_output,
                    response_model,
                    prompt,
                ),
                timeout=timeout_seconds,
            )

        except asyncio.TimeoutError:
            error_msg = (
                f"{self.__class__.__name__} structured execution timeout "
                f"after {timeout_seconds} seconds"
            )
            self._logger.error(error_msg)
            raise AgentTimeoutException(error_msg)

        except Exception as e:
            error_msg = (
                f"{self.__class__.__name__} structured execution failed: "
                f"{str(e)}"
            )
            self._logger.error(error_msg)
            raise AgentException(error_msg)