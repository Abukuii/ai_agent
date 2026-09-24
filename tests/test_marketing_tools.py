import pytest

from app.agent.tools import marketing


class _RecordingLLM:
    def __init__(self, response: str = "ok") -> None:
        self.response = response
        self.calls: list[tuple[str, str | None]] = []

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        self.calls.append((prompt, system))
        return self.response


@pytest.mark.asyncio
async def test_generate_marketing_post_passes_brief_and_system_prompt():
    llm = _RecordingLLM(response="Headline: ...")

    result = await marketing.generate_marketing_post(llm, "yangi somsa")

    assert result == "Headline: ..."
    prompt, system = llm.calls[0]
    assert prompt == "yangi somsa"
    assert system == marketing.MARKETING_POST_SYSTEM_PROMPT
    assert "headline" in system.lower()


@pytest.mark.asyncio
async def test_generate_marketing_ideas_uses_ideas_system_prompt():
    llm = _RecordingLLM(response="1. ...")

    result = await marketing.generate_marketing_ideas(llm, "brief")

    assert result == "1. ..."
    _, system = llm.calls[0]
    assert system == marketing.MARKETING_IDEAS_SYSTEM_PROMPT
    assert "campaign ideas" in system.lower()


@pytest.mark.asyncio
async def test_analyze_target_audience_uses_audience_system_prompt():
    llm = _RecordingLLM(response="Demographics: ...")

    result = await marketing.analyze_target_audience(llm, "brief")

    assert result == "Demographics: ..."
    _, system = llm.calls[0]
    assert system == marketing.AUDIENCE_ANALYSIS_SYSTEM_PROMPT
    assert "demographics" in system.lower()


@pytest.mark.asyncio
async def test_rewrite_content_injects_style_into_system_prompt():
    llm = _RecordingLLM(response="Rewritten text")

    result = await marketing.rewrite_content(llm, "original text", style="friendly")

    assert result == "Rewritten text"
    prompt, system = llm.calls[0]
    assert prompt == "original text"
    assert "friendly" in system.lower()


@pytest.mark.asyncio
async def test_all_tools_forbid_inventing_facts():
    """Every generation prompt must explicitly guard against fabricated
    prices/stats/guarantees (roadmap section 27: marketing safety) --
    phrased differently per tool, so check for any of the safety cues."""
    llm = _RecordingLLM()
    safety_markers = ("invent", "not in the original", "assumption", "cannot know for certain")

    await marketing.generate_marketing_post(llm, "brief")
    await marketing.generate_marketing_ideas(llm, "brief")
    await marketing.analyze_target_audience(llm, "brief")
    await marketing.rewrite_content(llm, "brief", style="premium")

    for _, system in llm.calls:
        lowered = system.lower()
        assert any(marker in lowered for marker in safety_markers), system
