"""Marketing content-generation tools (roadmap section 7).

These wrap LLM calls with task-specific system prompts. They intentionally
do not touch company/product data yet -- that lands once PostgreSQL
(section 10) and the RAG knowledge base (section 11) exist. Until then,
generated content is generic; each prompt explicitly forbids inventing
prices, stats, or guarantees (section 27) rather than pretending to know
things it doesn't.
"""

from app.ai.providers.base import LLMProvider

MARKETING_POST_SYSTEM_PROMPT = (
    "You are a marketing copywriter. Given a product/topic description, "
    "produce: a headline, a short Telegram-ready post (3-5 sentences), and "
    "one clear call to action. Do not invent prices, discounts, statistics, "
    "or guarantees that were not given to you -- state clearly if such "
    "details are missing. Respond in the same language as the input."
)

MARKETING_IDEAS_SYSTEM_PROMPT = (
    "You are a marketing strategist. Given a short brief, produce 5 concise, "
    "distinct marketing campaign ideas as a numbered list. Do not invent "
    "budget figures or guaranteed results. Respond in the same language as "
    "the input."
)

AUDIENCE_ANALYSIS_SYSTEM_PROMPT = (
    "You are a market research analyst. Given a product/audience "
    "description, analyze: demographics, pain points, motivations, likely "
    "objections, buying triggers, and 2-3 messaging recommendations. Label "
    "anything you cannot know for certain as an ASSUMPTION rather than "
    "stating it as fact. Respond in the same language as the input."
)

_REWRITE_SYSTEM_TEMPLATE = (
    "Rewrite the user's text in a {style} tone. Preserve the original "
    "meaning and language; do not add facts, numbers, or claims that were "
    "not in the original text. Return only the rewritten text."
)


async def generate_marketing_post(llm: LLMProvider, brief: str) -> str:
    return await llm.generate(brief, system=MARKETING_POST_SYSTEM_PROMPT)


async def generate_marketing_ideas(llm: LLMProvider, brief: str) -> str:
    return await llm.generate(brief, system=MARKETING_IDEAS_SYSTEM_PROMPT)


async def analyze_target_audience(llm: LLMProvider, brief: str) -> str:
    return await llm.generate(brief, system=AUDIENCE_ANALYSIS_SYSTEM_PROMPT)


async def rewrite_content(llm: LLMProvider, text: str, style: str) -> str:
    system = _REWRITE_SYSTEM_TEMPLATE.format(style=style)
    return await llm.generate(text, system=system)
