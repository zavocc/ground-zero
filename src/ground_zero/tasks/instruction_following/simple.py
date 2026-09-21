from typing import Literal

from pydantic import BaseModel, ConfigDict

from ..shared.types import NonEmptyText


class SimpleTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["simple"] = "simple"
    system_prompt: NonEmptyText | None = None
    prompt: NonEmptyText
    output: NonEmptyText
