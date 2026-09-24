"""LLM provider selection.

Reads ``LLM_PROVIDER`` from settings and builds the matching provider.
Only "ollama" exists today; adding a new backend means adding a branch
here (and a new class under app/ai/providers/) -- nothing else in the
codebase should need to change.
"""

from functools import lru_cache

from app.ai.providers.base import LLMProvider
from app.ai.providers.ollama import OllamaProvider
from app.core.config import Settings, get_settings


def build_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "ollama":
        return OllamaProvider(base_url=settings.ollama_base_url, model=settings.ollama_model)

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider!r}")


@lru_cache
def get_llm_provider() -> LLMProvider:
    return build_llm_provider(get_settings())
