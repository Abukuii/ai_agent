import pytest

from app.agent.intent import classify_intent


class _FakeLLM:
    def __init__(self, response: str) -> None:
        self._response = response

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        return self._response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("raw_response", "expected"),
    [
        ("marketing_post", "marketing_post"),
        ("Marketing_Post\n", "marketing_post"),
        ("audience_analysis", "audience_analysis"),
        ("rewrite", "rewrite"),
        ("marketing_ideas", "marketing_ideas"),
        ("i am not sure what this is", "chat"),
        ("", "chat"),
        ("chat", "chat"),
    ],
)
async def test_classify_intent_normalizes_known_labels_and_falls_back(
    raw_response: str, expected: str
) -> None:
    llm = _FakeLLM(raw_response)

    result = await classify_intent(llm, "some message")

    assert result == expected
