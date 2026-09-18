from typing import Self

import httpx

from .models.simple import SimpleIOTask
from .models.toolcall import ToolCallIOTask
from .schema import GZ_QUESTIONS

EVAL_TASK = SimpleIOTask | ToolCallIOTask


class Checker:
    def __init__(self, api_key: str, client: httpx.Client | None = None, timeout: float = 30.0) -> None:
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout)
        self._api_key = api_key

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def evaluate(self, task: EVAL_TASK):
        # headers
        or_headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/zavocc/ground-zero",
            "X-OpenRouter-Title": "Ground Zero"
        }

        # body
        or_body = {
            "model": "~typesafe/jev-latest",
            "state": task.model_dump(mode="json"),
            "questions": GZ_QUESTIONS
        }

        # response
        or_response = self._client.post(
            url="https://openrouter.ai/api/alpha/decisions",
            headers=or_headers,
            json=or_body
        )

        or_response.raise_for_status()

        return or_response.json()
