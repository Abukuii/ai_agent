"""``/start`` command handler.

Static text for now. Once the multilingual agent (roadmap section 26)
exists, this should detect/store the user's preferred language instead of
hardcoding Uzbek.
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")

WELCOME_TEXT = (
    "Salom! Men <b>AI Marketing Agent</b> botiman.\n\n"
    "Hozircha ishga tushirish bosqichidaman — tez orada marketing posti "
    "yaratish, kampaniya g'oyalari, auditoriya tahlili va boshqa "
    "imkoniyatlar qo'shiladi.\n\n"
    "Mavjud buyruqlar ro'yxati uchun /help yozing."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT)
