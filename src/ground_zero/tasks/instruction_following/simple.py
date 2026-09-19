from typing import Literal

from pydantic import BaseModel, ConfigDict

from .types import OutputText, PromptText


class SimpleIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["simple"] = "simple"
    system_prompt: PromptText | None = None
    prompt: PromptText
    output: OutputText
