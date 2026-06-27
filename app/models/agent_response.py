from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """
    Standard response returned by every specialist agent.
    """

    agent_name: str

    answer: str

    sources: list[str] = Field(default_factory=list)

    metadata: dict[str, str] = Field(default_factory=dict)