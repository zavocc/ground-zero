from typing import Self

import httpx

from ground_zero.tasks.correctness import MultiTurnTask, SimpleTask

from ..constants import *
from .questions import GZ_QUESTIONS_BASE, GZ_QUESTIONS_TASK_MULTITURN

TASKMODES = SimpleTask | MultiTurnTask


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

    def evaluate(self, task: TASKMODES):
        # determine question type
        question_type = GZ_QUESTIONS_TASK_MULTITURN if isinstance(task, MultiTurnTask) else GZ_QUESTIONS_BASE

        # headers
        or_headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": OR_HEADER_CONTENT_TYPE,
            "HTTP-Referer": OR_HEADER_HTTP_REFERER,
            "X-OpenRouter-Title": OR_HEADER_X_OPENROUTER_TITLE
        }

        # body
        or_body = {
            "model": OR_MODEL,
            "state": task.model_dump(mode="json"),
            "questions": question_type
        }

        # response
        or_response = self._client.post(
            url=OR_URL,
            headers=or_headers,
            json=or_body
        )

        or_response.raise_for_status()

        result = or_response.json()["answers"]
        return result

class AsyncChecker:
    def __init__(self, api_key: str, client: httpx.AsyncClient | None = None, timeout: float = 30.0) -> None:
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)
        self._api_key = api_key

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def evaluate(self, task: TASKMODES):
        # determine question type
        question_type = GZ_QUESTIONS_TASK_MULTITURN if isinstance(task, MultiTurnTask) else GZ_QUESTIONS_BASE

        # headers
        or_headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": OR_HEADER_CONTENT_TYPE,
            "HTTP-Referer": OR_HEADER_HTTP_REFERER,
            "X-OpenRouter-Title": OR_HEADER_X_OPENROUTER_TITLE
        }

        # body
        or_body = {
            "model": OR_MODEL,
            "state": task.model_dump(mode="json"),
            "questions": question_type
        }

        # response
        or_response = await self._client.post(
            url=OR_URL,
            headers=or_headers,
            json=or_body
        )

        or_response.raise_for_status()

        result = or_response.json()["answers"]
        return result
