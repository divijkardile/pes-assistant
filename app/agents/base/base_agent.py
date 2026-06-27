import logging
from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

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

        response = self._agent(
            prompt,
        )

        return str(response)

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

        return self._agent.structured_output(
            output_model=response_model,
            prompt=prompt,
        )