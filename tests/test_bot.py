from app.bot.bot import create_bot, create_dispatcher
from app.core.config import Settings


def test_create_dispatcher_registers_start_and_help_routers():
    dispatcher = create_dispatcher()

    router_names = {router.name for router in dispatcher.sub_routers}

    assert "start" in router_names
    assert "help" in router_names
    assert "chat" in router_names


def test_create_bot_uses_token_from_settings(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:test-token")
    settings = Settings(_env_file=None)

    bot = create_bot(settings)

    assert bot.token == "123456:test-token"
