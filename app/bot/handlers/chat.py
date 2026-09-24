"""Fallback handler for plain text messages.

Phase 3 scope only: proves the LLM abstraction works end-to-end through
Telegram. No intent detection, tools, memory, or approval flow yet --
that begins in Phase 4 (agent).
"""

import logging

from aiogram import Router
from aiogram.types import Message

from app.ai.llm import get_llm_provider

router = Router(name="chat")
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the assistant behind an in-development marketing AI agent. "
    "The full toolset (post generation, campaigns, audience analysis) "
    "is not wired up yet -- keep replies short and honest about that."
)

LLM_UNAVAILABLE_TEXT = (
    "Kechirasiz, hozir AI javob bera olmadi (LLM mavjud emas yoki xatolik yuz berdi)."
)


@router.message()
async def handle_text(message: Message) -> None:
    if not message.text:
        return

    provider = get_llm_provider()
    try:
        reply = await provider.generate(message.text, system=SYSTEM_PROMPT)
    except Exception:
        logger.exception("LLM call failed")
        await message.answer(LLM_UNAVAILABLE_TEXT)
        return

    await message.answer(reply)
