from typing import Literal

from pydantic import BaseModel, ConfigDict, JsonValue

from ..shared.types import NonEmptyText


class SimpleIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["simple"] = "simple"
    prompt: NonEmptyText
    output: NonEmptyText
    expected_output: JsonValue
