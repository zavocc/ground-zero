from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, StringConstraints

NonEmptyText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=1,
)]

class ToolSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: NonEmptyText
    description: str | None = None
    parameters: dict[str, JsonValue] | None = None
    required: list[str] | None = None

class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: NonEmptyText
    arguments: dict[str, JsonValue] = Field(default_factory=dict)
    result: JsonValue | None = None

# max 5 tool calls
class ToolCallIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["tool_calls"] = "tool_calls"
    prompt: NonEmptyText
    tools: list[ToolSchema] = Field(min_length=1, max_length=100)
    tool_calls: list[ToolCall] = Field(min_length=1, max_length=5)
    output: NonEmptyText
