from typing import Annotated

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
