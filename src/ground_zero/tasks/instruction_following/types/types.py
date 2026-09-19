from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

PromptText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=1,
)]

OutputText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=1,
)]

class MultiTurnMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: PromptText
    role: Literal["user", "assistant", "system"]
