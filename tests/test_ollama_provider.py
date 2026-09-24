import httpx
import pytest

from app.ai.providers.ollama import OllamaProvider


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self._payload


@pytest.mark.asyncio
async def test_generate_returns_response_text_and_calls_correct_endpoint(monkeypatch):
    captured = {}

    async def fake_post(self, url, json):
        captured["url"] = url
        captured["json"] = json
        return _FakeResponse({"response": "hello there"})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    provider = OllamaProvider(base_url="http://localhost:11434/", model="qwen2.5:7b-instruct")
    result = await provider.generate("hi", system="be nice")

    assert result == "hello there"
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["json"] == {
        "model": "qwen2.5:7b-instruct",
        "prompt": "hi",
        "stream": False,
        "system": "be nice",
    }


@pytest.mark.asyncio
async def test_generate_omits_system_key_when_not_given(monkeypatch):
    captured = {}

    async def fake_post(self, url, json):
        captured["json"] = json
        return _FakeResponse({"response": "ok"})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    provider = OllamaProvider(base_url="http://localhost:11434", model="qwen2.5:7b-instruct")
    await provider.generate("hi")

    assert "system" not in captured["json"]


@pytest.mark.asyncio
async def test_generate_raises_on_http_error(monkeypatch):
    class _FailingResponse(_FakeResponse):
        def raise_for_status(self) -> None:
            raise httpx.HTTPStatusError("boom", request=None, response=None)

    async def fake_post(self, url, json):
        return _FailingResponse({})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    provider = OllamaProvider(base_url="http://localhost:11434", model="qwen2.5:7b-instruct")

    with pytest.raises(httpx.HTTPStatusError):
        await provider.generate("hi")
