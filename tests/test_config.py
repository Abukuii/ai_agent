from app.core.config import Settings


def test_settings_loads_required_and_default_values(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:test-token")
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.telegram_bot_token == "123456:test-token"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"


def test_settings_reads_overridden_values(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "abc")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings(_env_file=None)

    assert settings.environment == "production"
    assert settings.log_level == "DEBUG"


def test_settings_raises_without_bot_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    try:
        Settings(_env_file=None)
    except Exception:
        pass
    else:
        raise AssertionError("Settings() should fail without TELEGRAM_BOT_TOKEN")
