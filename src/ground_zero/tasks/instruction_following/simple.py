from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

PromptText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=10,
)]

OutputText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=1,
)]


class SimpleIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["simple"] = "simple"
    prompt: PromptText
    output: OutputText
