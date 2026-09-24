"""Entry point: starts the Telegram bot in long-polling mode.

Run with:  python -m app.main
"""

import asyncio
import logging

from app.bot.bot import create_bot, create_dispatcher
from app.core.config import get_settings
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info("Starting AI Marketing Agent bot (environment=%s)", settings.environment)

    bot = create_bot(settings)
    dispatcher = create_dispatcher()

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
