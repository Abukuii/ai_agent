"""Fallback handler for plain text messages.

Routes every non-command message through the agent (app/agent/graph.py)
instead of calling the LLM directly -- see project goal: the system
"must use an AI agent architecture rather than simply sending every
message directly to an LLM."
"""

import logging

from aiogram import Router
from aiogram.types import Message

from app.agent.graph import run_agent
from app.ai.llm import get_llm_provider

router = Router(name="chat")
logger = logging.getLogger(__name__)

LLM_UNAVAILABLE_TEXT = (
    "Kechirasiz, hozir AI javob bera olmadi (LLM mavjud emas yoki xatolik yuz berdi)."
)


@router.message()
async def handle_text(message: Message) -> None:
    if not message.text:
        return

    provider = get_llm_provider()
    try:
        state = await run_agent(provider, message.text)
    except Exception:
        logger.exception("Agent run failed")
        await message.answer(LLM_UNAVAILABLE_TEXT)
        return

    await message.answer(state["final_response"])
