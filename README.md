# AI Marketing Agent

Open-source, Telegram-based AI marketing assistant. Generates marketing
posts, campaign ideas, audience analysis and more through an agent
architecture (not a plain prompt-to-LLM wrapper), with mandatory
human-in-the-loop approval before anything is published.

Built with free/open-source components: Ollama for the LLM, LangGraph for
the agent workflow, PostgreSQL for storage, Qdrant for the knowledge base
(RAG), and SearXNG for web research.

## Status

🚧 **Phase 1 of 13 — Telegram MVP.** Only `/start` and `/help` exist so
far; no AI, database, or agent logic yet. See the roadmap below.

## Setup (Phase 1)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN (get one from @BotFather)

python -m app.main
```

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
│   └── handlers/         # /start, /help, ...
└── core/
    ├── config.py          # pydantic-settings configuration
    └── logging.py         # structured console logging
tests/
```

## Roadmap

1. ✅ Telegram MVP (bot, config, logging)
2. Local LLM (Ollama + provider abstraction)
3. AI agent (LangGraph state + tools)
4. PostgreSQL (models, repositories, migrations)
5. Marketing engine (post/campaign/audience/rewrite generation)
6. RAG knowledge base (Qdrant)
7. Web research (SearXNG)
8. Human approval workflow
9. Telegram publishing & scheduling
10. Docker Compose (app, postgres, qdrant, ollama, searxng)
11. Security & testing pass
12. Documentation
