from pydantic import BaseModel


class EvaluationResult(BaseModel):
    """
    Result returned by the Orchestrator after reviewing
    specialist agent responses.
    """

    approved: bool

    confidence: float

    feedback: str