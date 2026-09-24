import pytest

from app.agent.graph import run_agent
from app.ai.providers.base import LLMProvider


class _ScriptedLLM(LLMProvider):
    """Returns a fixed intent label when asked to classify, and a fixed
    tool response otherwise -- lets us exercise the real LangGraph graph
    end-to-end without mocking internal functions."""

    def __init__(self, intent_label: str, tool_response: str) -> None:
        self._intent_label = intent_label
        self._tool_response = tool_response
        self.calls: list[tuple[str, str | None]] = []

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        self.calls.append((prompt, system))
        if system and "Classify" in system:
            return self._intent_label
        return self._tool_response


@pytest.mark.asyncio
async def test_run_agent_routes_marketing_post_intent_to_the_matching_tool():
    llm = _ScriptedLLM(intent_label="marketing_post", tool_response="Generated post text")

    result = await run_agent(llm, "yangi somsa uchun post yoz")

    assert result["intent"] == "marketing_post"
    assert result["tool_result"] == "Generated post text"
    assert result["final_response"] == "Generated post text"
    assert len(llm.calls) == 2  # classify, then generate


@pytest.mark.asyncio
async def test_run_agent_falls_back_to_chat_for_unrecognized_intent():
    llm = _ScriptedLLM(intent_label="something-unrecognized", tool_response="hi there")

    result = await run_agent(llm, "salom")

    assert result["intent"] == "chat"
    assert result["final_response"] == "hi there"


@pytest.mark.asyncio
async def test_run_agent_preserves_the_original_user_message():
    llm = _ScriptedLLM(intent_label="chat", tool_response="ok")

    result = await run_agent(llm, "hello world")

    assert result["user_message"] == "hello world"
