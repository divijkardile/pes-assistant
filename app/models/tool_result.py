from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    """Represents the result of a tool execution."""

    tool_name: str
    success: bool
    result: Any = None
    execution_time_ms: float