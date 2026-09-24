from unittest.mock import AsyncMock

import pytest

from app.bot.handlers import chat as chat_handler


@pytest.mark.asyncio
async def test_handle_text_replies_with_agent_final_response(monkeypatch):
    monkeypatch.setattr(chat_handler, "get_llm_provider", lambda: object())
    fake_run_agent = AsyncMock(return_value={"final_response": "salom!", "intent": "chat"})
    monkeypatch.setattr(chat_handler, "run_agent", fake_run_agent)

    message = AsyncMock()
    message.text = "salom"

    await chat_handler.handle_text(message)

    fake_run_agent.assert_awaited_once()
    message.answer.assert_awaited_once_with("salom!")


@pytest.mark.asyncio
async def test_handle_text_replies_gracefully_on_agent_failure(monkeypatch):
    monkeypatch.setattr(chat_handler, "get_llm_provider", lambda: object())
    fake_run_agent = AsyncMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr(chat_handler, "run_agent", fake_run_agent)

    message = AsyncMock()
    message.text = "salom"

    await chat_handler.handle_text(message)

    message.answer.assert_awaited_once_with(chat_handler.LLM_UNAVAILABLE_TEXT)


@pytest.mark.asyncio
async def test_handle_text_ignores_messages_without_text(monkeypatch):
    fake_run_agent = AsyncMock()
    monkeypatch.setattr(chat_handler, "run_agent", fake_run_agent)

    message = AsyncMock()
    message.text = None

    await chat_handler.handle_text(message)

    fake_run_agent.assert_not_awaited()
    message.answer.assert_not_awaited()
