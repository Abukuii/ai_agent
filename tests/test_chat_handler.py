from unittest.mock import AsyncMock

import pytest

from app.bot.handlers import chat as chat_handler


@pytest.mark.asyncio
async def test_handle_text_replies_with_llm_output(monkeypatch):
    fake_provider = AsyncMock()
    fake_provider.generate.return_value = "salom!"
    monkeypatch.setattr(chat_handler, "get_llm_provider", lambda: fake_provider)

    message = AsyncMock()
    message.text = "salom"

    await chat_handler.handle_text(message)

    fake_provider.generate.assert_awaited_once_with(
        "salom", system=chat_handler.SYSTEM_PROMPT
    )
    message.answer.assert_awaited_once_with("salom!")


@pytest.mark.asyncio
async def test_handle_text_replies_gracefully_on_llm_failure(monkeypatch):
    fake_provider = AsyncMock()
    fake_provider.generate.side_effect = RuntimeError("ollama unreachable")
    monkeypatch.setattr(chat_handler, "get_llm_provider", lambda: fake_provider)

    message = AsyncMock()
    message.text = "salom"

    await chat_handler.handle_text(message)

    message.answer.assert_awaited_once_with(chat_handler.LLM_UNAVAILABLE_TEXT)


@pytest.mark.asyncio
async def test_handle_text_ignores_messages_without_text(monkeypatch):
    fake_provider = AsyncMock()
    monkeypatch.setattr(chat_handler, "get_llm_provider", lambda: fake_provider)

    message = AsyncMock()
    message.text = None

    await chat_handler.handle_text(message)

    fake_provider.generate.assert_not_awaited()
    message.answer.assert_not_awaited()
