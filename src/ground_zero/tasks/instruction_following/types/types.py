from typing import Annotated

from pydantic import StringConstraints

PromptText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=10,
)]

OutputText = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=1,
)]
