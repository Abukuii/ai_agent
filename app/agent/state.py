"""Agent state definition (roadmap section 6).

Kept minimal on purpose: only fields the graph actually reads or writes
today. The full conceptual state from the spec also has ``user_id`` /
``conversation_id`` (needs PostgreSQL -- Phase 4), ``company_context`` /
``retrieved_documents`` (needs the RAG knowledge base -- Phase 6), and
``review_result`` / ``approval_status`` (needs the approval workflow --
Phase 8). Those get added when the phase that produces them lands;
carrying unused fields now would just be dead code.
"""

from typing import Literal, NotRequired, TypedDict

Intent = Literal[
    "marketing_post",
    "marketing_ideas",
    "audience_analysis",
    "rewrite",
    "chat",
]


class AgentState(TypedDict):
    user_message: str
    intent: NotRequired[Intent]
    tool_result: NotRequired[str]
    final_response: NotRequired[str]
