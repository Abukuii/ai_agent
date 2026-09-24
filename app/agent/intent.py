"""Intent classification.

Decides which tool (if any) should handle a user message. LLM-based
rather than keyword matching, so it also works for Uzbek/Russian input --
with a safe fallback to plain chat when the model's answer doesn't match
a known label.
"""

from app.agent.state import Intent
from app.ai.providers.base import LLMProvider

_TOOL_INTENTS: tuple[Intent, ...] = (
    "marketing_post",
    "marketing_ideas",
    "audience_analysis",
    "rewrite",
)

CLASSIFY_SYSTEM_PROMPT = (
    "Classify the user's message into exactly one label, with no other text:\n"
    "marketing_post - they want a marketing/ad post, caption, or copy written\n"
    "marketing_ideas - they want campaign or marketing ideas/suggestions\n"
    "audience_analysis - they want target audience/customer analysis\n"
    "rewrite - they want existing text rewritten/rephrased in a different style\n"
    "chat - anything else (greetings, questions, unclear requests)\n"
    "Answer with only the label."
)


async def classify_intent(llm: LLMProvider, user_message: str) -> Intent:
    raw = await llm.generate(user_message, system=CLASSIFY_SYSTEM_PROMPT)
    normalized = raw.strip().lower()

    for intent in _TOOL_INTENTS:
        if intent in normalized:
            return intent

    return "chat"
