import logging
from abc import ABC

from strands import Agent


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

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
        """
        Executes the configured Strands agent.
        """

        self._logger.info(
            "Executing agent '%s'.",
            self.__class__.__name__,
        )

        response = self._agent(prompt)

        if response is None:
            raise RuntimeError(
                f"{self.__class__.__name__} returned no response."
            )

        return str(response)