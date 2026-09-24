# AI Marketing Agent

Open-source, Telegram-based AI marketing assistant. Generates marketing
posts, campaign ideas, audience analysis and more through an agent
architecture (not a plain prompt-to-LLM wrapper), with mandatory
human-in-the-loop approval before anything is published.

Built with free/open-source components: Ollama for the LLM, LangGraph for
the agent workflow, PostgreSQL for storage, Qdrant for the knowledge base
(RAG), and SearXNG for web research.

## Status

🚧 **Phase 2 of 13 — Local LLM.** Bot has `/start`, `/help`, and replies
to plain text via a local Ollama model through a provider abstraction.
No agent, tools, database, or approval flow yet. See the roadmap below.

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
│   └── handlers/         # /start, /help, chat (LLM fallback), ...
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
