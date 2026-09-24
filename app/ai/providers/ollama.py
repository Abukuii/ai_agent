"""Ollama-backed LLM provider.

Talks to a local/self-hosted Ollama server over its HTTP API
(https://github.com/ollama/ollama/blob/main/docs/api.md). No API key, no
paid service -- this is the default provider for the whole project.
"""

import httpx

from app.ai.providers.base import LLMProvider

_DEFAULT_TIMEOUT_SECONDS = 60.0


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        timeout: float = _DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        payload: dict[str, object] = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(f"{self._base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()

        return data["response"]
