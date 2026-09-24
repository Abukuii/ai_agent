"""LLM provider abstraction.

The rest of the application (agent, tools, handlers) must depend only on
this interface, never on a specific backend. This is what lets Ollama be
swapped for OpenAI/Anthropic/Gemini/vLLM later without touching business
logic (roadmap section 13).
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Minimal interface every LLM backend must implement."""

    @abstractmethod
    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        """Generate a completion for ``prompt``.

        Args:
            prompt: The user-facing prompt/message.
            system: Optional system instruction to steer the model.

        Returns:
            The model's text response.
        """
        raise NotImplementedError
