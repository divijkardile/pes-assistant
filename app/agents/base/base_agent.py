import logging
from abc import ABC
from typing import TypeVar

from pydantic import BaseModel
from strands import Agent

T = TypeVar("T", bound=BaseModel)


class BaseAgent(ABC):

    def __init__(
        self,
        *,
        logger: logging.Logger,
        agent: Agent,
    ) -> None:
        self._logger = logger
        self._agent = agent

    async def _execute(
        self,
        prompt: str,
    ) -> str:
        self._logger.info(
            "%s executing.",
            self.__class__.__name__,
        )

        response = self._agent(prompt)

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