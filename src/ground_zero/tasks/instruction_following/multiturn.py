from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from .types import MultiTurnMessage


class MultiTurnTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["multiturn"] = "multiturn"
    messages: list[MultiTurnMessage]

    @field_validator("messages")
    @classmethod
    def validate_last_message(cls, messages: list[MultiTurnMessage]) -> list[MultiTurnMessage]:
        if not messages:
            raise ValueError("messages must not be empty")

        if messages[-1].role != "assistant":
            raise ValueError("the last message must have the assistant role")

        return messages
