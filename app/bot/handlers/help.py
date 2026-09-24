"""``/help`` command handler."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="help")

HELP_TEXT = (
    "<b>Mavjud buyruqlar:</b>\n"
    "/start — botni ishga tushirish\n"
    "/help — shu yordam xabari\n\n"
    "Oddiy xabar yozsangiz ham bo'ladi — hozircha test rejimida LLM javob "
    "beradi (marketing vositalarisiz).\n\n"
    "<b>Keyingi bosqichlarda qo'shiladi:</b>\n"
    "/menu, /campaign, /post, /ideas, /history, /knowledge, /settings"
)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)
