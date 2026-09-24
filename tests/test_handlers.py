from unittest.mock import AsyncMock

import pytest

from app.bot.handlers.help import HELP_TEXT, cmd_help
from app.bot.handlers.start import WELCOME_TEXT, cmd_start


@pytest.mark.asyncio
async def test_cmd_start_sends_welcome_text():
    message = AsyncMock()

    await cmd_start(message)

    message.answer.assert_awaited_once_with(WELCOME_TEXT)


@pytest.mark.asyncio
async def test_cmd_help_sends_help_text():
    message = AsyncMock()

    await cmd_help(message)

    message.answer.assert_awaited_once_with(HELP_TEXT)
