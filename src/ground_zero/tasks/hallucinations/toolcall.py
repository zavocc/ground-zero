from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .types import NonEmptyText, ToolCall, ToolSchema


# max 5 tool calls
class ToolCallIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["tool_calls"] = "tool_calls"
    prompt: NonEmptyText
    tools: list[ToolSchema] = Field(min_length=1, max_length=100)
    tool_calls: list[ToolCall] = Field(min_length=1, max_length=5)
    output: NonEmptyText
