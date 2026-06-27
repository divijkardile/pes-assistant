from abc import ABC, abstractmethod

from strands import Agent


class LLMProvider(ABC):

    @abstractmethod
    def create_agent(
        self,
        **kwargs,
    ) -> Agent:
        """
        Creates and returns a configured Strands Agent.
        """
        ...