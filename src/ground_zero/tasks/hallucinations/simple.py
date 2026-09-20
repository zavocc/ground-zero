from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

from ..shared.types import NonEmptyText

PromptText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=512,
)]


class SimpleIOTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["simple"] = "simple"
    prompt: PromptText
    output: NonEmptyText
