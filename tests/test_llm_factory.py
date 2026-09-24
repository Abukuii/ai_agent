import pytest

from app.ai.llm import build_llm_provider
from app.ai.providers.ollama import OllamaProvider
from app.core.config import Settings


def test_build_llm_provider_returns_ollama_by_default(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
    settings = Settings(_env_file=None)

    provider = build_llm_provider(settings)

    assert isinstance(provider, OllamaProvider)


def test_build_llm_provider_uses_configured_model_and_url(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1:8b")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama:11434")
    settings = Settings(_env_file=None)

    provider = build_llm_provider(settings)

    assert provider._model == "llama3.1:8b"  # noqa: SLF001
    assert provider._base_url == "http://ollama:11434"  # noqa: SLF001


def test_build_llm_provider_raises_for_unknown_provider(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
    monkeypatch.setenv("LLM_PROVIDER", "unknown")
    settings = Settings(_env_file=None)

    with pytest.raises(ValueError, match="Unsupported LLM_PROVIDER"):
        build_llm_provider(settings)
