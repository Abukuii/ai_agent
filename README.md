# AI Marketing Agent

Open-source, Telegram-based AI marketing assistant. Generates marketing
posts, campaign ideas, audience analysis and more through an agent
architecture (not a plain prompt-to-LLM wrapper), with mandatory
human-in-the-loop approval before anything is published.

Built with free/open-source components: Ollama for the LLM, LangGraph for
the agent workflow, PostgreSQL for storage, Qdrant for the knowledge base
(RAG), and SearXNG for web research.

## Status

🚧 **Phase 3 of 13 — AI Agent.** Messages now go through a LangGraph
agent (classify intent → run the matching tool) instead of a raw LLM
call. Four generation tools exist (post, ideas, audience analysis,
rewrite), but without company/product grounding — that needs PostgreSQL
(Phase 4) and the RAG knowledge base (Phase 6). No approval workflow
yet, so nothing is "published" — everything is just a chat reply.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# edit .env: set TELEGRAM_BOT_TOKEN (from @BotFather)

python -m app.main
```

### LLM (Ollama)

The bot's plain-text replies need a running Ollama server with the
configured model pulled:

```bash
# install: https://ollama.com/download
ollama pull qwen2.5:7b-instruct   # or whatever OLLAMA_MODEL is set to
ollama serve                       # if not already running
```

`OLLAMA_BASE_URL` defaults to `http://localhost:11434`. If Ollama isn't
running or the model isn't pulled, the bot catches the error and replies
with a friendly Uzbek fallback message instead of crashing.

## Testing

```bash
pytest
ruff check .
mypy app
```

## Project structure

```text
app/
├── main.py              # entry point (long polling)
├── bot/
│   ├── bot.py            # Bot + Dispatcher factories
│   └── handlers/         # /start, /help, chat (routes to the agent)
├── agent/
│   ├── state.py           # AgentState (TypedDict)
│   ├── intent.py           # LLM-based intent classification
│   ├── graph.py             # LangGraph orchestration (classify -> generate)
│   └── tools/
│       └── marketing.py     # generate_marketing_post/ideas/audience/rewrite
├── ai/
│   ├── llm.py             # provider selection (LLM_PROVIDER)
│   └── providers/         # base.py (LLMProvider ABC), ollama.py
└── core/
    ├── config.py          # pydantic-settings configuration
    └── logging.py         # structured console logging
tests/
```

## Roadmap

1. ✅ Telegram MVP (bot, config, logging)
2. ✅ Local LLM (Ollama + provider abstraction)
3. ✅ AI agent (LangGraph state + tools)
4. PostgreSQL (models, repositories, migrations)
5. Marketing engine (post/campaign/audience/rewrite generation)
6. RAG knowledge base (Qdrant)
7. Web research (SearXNG)
8. Human approval workflow
9. Telegram publishing & scheduling
10. Docker Compose (app, postgres, qdrant, ollama, searxng)
11. Security & testing pass
12. Documentation
