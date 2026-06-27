from pydantic import BaseModel


class DocumentChunk(BaseModel):
    """A retrieved document chunk."""

    document_name: str
    content: str
    page_number: int | None = None
    score: float | None = None