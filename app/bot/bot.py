"""Bot and Dispatcher construction.

Kept separate from ``app/main.py`` so tests can build a Dispatcher (to
inspect registered routers) without needing a real bot token or starting
polling.
"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import chat as chat_handler
from app.bot.handlers import help as help_handler
from app.bot.handlers import start as start_handler
from app.core.config import Settings


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(start_handler.router)
    dispatcher.include_router(help_handler.router)
    # chat_handler has no filter (matches any text) -- must stay last so it
    # only catches messages the command routers above didn't handle.
    dispatcher.include_router(chat_handler.router)
    return dispatcher
