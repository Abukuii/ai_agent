"""LangGraph-based agent orchestrator (roadmap section 6).

Replaces the Phase 2 "send everything straight to the LLM" fallback with
an explicit workflow: classify intent -> run the matching tool (or plain
chat). This is what the project goal means by "must use an AI agent
architecture rather than simply sending every message directly to an
LLM" -- there is now an explicit state and a routing decision in between.

Tool selection here is intent-to-function dispatch rather than
LLM-driven function calling: with a small local model, native function
calling is unreliable, so the LLM only classifies intent (a single
label) and a fixed table decides which tool that maps to. Revisit this
if a larger/more capable model becomes the default.

No loops exist yet (classify -> generate -> END), so `recursion_limit`
is currently just a defensive ceiling for when regenerate/review loops
are added in Phase 8 (human approval).
"""

from langgraph.graph import END, StateGraph

from app.agent.intent import classify_intent
from app.agent.state import AgentState
from app.agent.tools import marketing
from app.ai.providers.base import LLMProvider

_RECURSION_LIMIT = 6

CHAT_SYSTEM_PROMPT = (
    "You are the assistant behind an in-development marketing AI agent. "
    "The full toolset (company/product-grounded post generation, "
    "campaigns, audience analysis) is being built incrementally -- keep "
    "replies short and honest about current limitations. Respond in the "
    "same language as the user."
)


def build_agent_graph(llm: LLMProvider):
    async def classify_node(state: AgentState) -> AgentState:
        intent = await classify_intent(llm, state["user_message"])
        return {**state, "intent": intent}

    async def generate_node(state: AgentState) -> AgentState:
        intent = state["intent"]
        message = state["user_message"]

        if intent == "marketing_post":
            result = await marketing.generate_marketing_post(llm, message)
        elif intent == "marketing_ideas":
            result = await marketing.generate_marketing_ideas(llm, message)
        elif intent == "audience_analysis":
            result = await marketing.analyze_target_audience(llm, message)
        elif intent == "rewrite":
            # Phase 3 defaults to a "professional" style until Telegram
            # button-based style selection lands with the marketing UI.
            result = await marketing.rewrite_content(llm, message, style="professional")
        else:
            result = await llm.generate(message, system=CHAT_SYSTEM_PROMPT)

        return {**state, "tool_result": result, "final_response": result}

    graph = StateGraph(AgentState)
    graph.add_node("classify_intent", classify_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


async def run_agent(llm: LLMProvider, user_message: str) -> AgentState:
    graph = build_agent_graph(llm)
    result: AgentState = await graph.ainvoke(
        {"user_message": user_message},
        config={"recursion_limit": _RECURSION_LIMIT},
    )
    return result
