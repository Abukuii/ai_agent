"""Application configuration.

Settings are loaded from environment variables (and a local .env file in
development). Nothing here should hold secrets by default -- see
.env.example for the variables a deployment must provide.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings.

    Values are read from the process environment first, falling back to a
    ``.env`` file if present. See ``.env.example`` for the full list of
    supported variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Cached so the environment/`.env` file is only parsed once per process.
    """
    return Settings()  # type: ignore[call-arg]
