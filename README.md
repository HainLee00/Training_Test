# LLM Multi-Agent Trading System (Free Tools Edition)

An AI-powered multi-agent trading analysis framework built on top of [TradingAgents](https://github.com/TauricResearch/TradingAgents), configured to run **entirely with free, open-source tools** — no paid API keys required.

| Component | Technology | Cost |
|---|---|---|
| LLM inference | [Ollama](https://ollama.com) (local models) | **Free** |
| Market data | [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance) | **Free** |
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) | **Free** |
| Technical indicators | [StockStats](https://github.com/jealous/stockstats) | **Free** |
| Trading simulation | [Backtrader](https://github.com/mementum/backtrader) | **Free** |

> **Disclaimer**: This project is for educational and research purposes only. It does not constitute financial or investment advice.

---

## Architecture

The system mirrors a real-world trading firm with specialized AI agents that collaborate through a structured pipeline:

```
┌──────────────────────────────────────────────────────────────┐
│                     ANALYST TEAM                             │
│  (parallel execution – each analyst queries free market data)│
│                                                              │
│  ┌─────────────┐ ┌───────────────┐ ┌──────┐ ┌────────────┐  │
│  │   Market    │ │ Social Media  │ │ News │ │Fundamentals│  │
│  │  Analyst    │ │   Analyst     │ │Anal. │ │  Analyst   │  │
│  │(MACD/RSI…)  │ │ (sentiment)   │ │(news)│ │(financials)│  │
│  └──────┬──────┘ └──────┬────────┘ └──┬───┘ └─────┬──────┘  │
└─────────┼───────────────┼─────────────┼───────────┼──────────┘
          └───────────────┴─────────────┴───────────┘
                              │
                   ┌──────────▼──────────┐
                   │   RESEARCH DEBATE   │
                   │  Bull ◄──────► Bear │
                   │  (configurable N    │
                   │   rounds)           │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │  Research Manager   │
                   │  (synthesizes the   │
                   │   debate)           │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │      TRADER         │
                   │ (trade decision)    │
                   └──────────┬──────────┘
                              │
                ┌─────────────▼──────────────┐
                │      RISK MANAGEMENT       │
                │ Aggressive ◄──► Conservative│
                │         Neutral            │
                └─────────────┬──────────────┘
                              │
                   ┌──────────▼──────────┐
                   │  Portfolio Manager  │
                   │  (final decision)   │
                   └─────────────────────┘
```

### Agent Roles

| Agent | Role |
|---|---|
| **Market Analyst** | Technical analysis – MACD, RSI, Bollinger Bands, VWMA, ATR, SMA |
| **Social Media Analyst** | Sentiment analysis from news headlines |
| **News Analyst** | Global news, macro events, insider transactions |
| **Fundamentals Analyst** | Balance sheets, income statements, cash flows, P/E ratios |
| **Bull Researcher** | Constructs the bullish investment thesis |
| **Bear Researcher** | Constructs the bearish investment thesis |
| **Research Manager** | Synthesizes the bull-vs-bear debate |
| **Trader** | Produces a trade proposal from all analyst reports |
| **Aggressive / Conservative / Neutral Risk Agents** | Debate risk-management constraints |
| **Portfolio Manager** | Issues the final BUY / SELL / HOLD decision |

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | Check with `python --version` |
| [Ollama](https://ollama.com/download) | latest | Runs local LLMs for free |
| RAM | ≥ 8 GB | For `llama3.1:8b`; 4 GB for lighter models |
| Disk | ≥ 6 GB | For the default model |

---

## Quick Start

### 1 — Install Ollama

Follow the official instructions for your OS: <https://ollama.com/download>

```bash
# macOS (Homebrew)
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2 — Start Ollama and pull a model

```bash
# Start the local server (keep this terminal open)
ollama serve

# In a new terminal, pull the default model (~4.7 GB)
ollama pull llama3.1:8b
```

**Lower-RAM alternatives:**

| Model | RAM needed | Pull command |
|---|---|---|
| `qwen2.5:3b` | ~2 GB | `ollama pull qwen2.5:3b` |
| `mistral:7b` | ~5 GB | `ollama pull mistral:7b` |
| `qwen2.5:7b` | ~5 GB | `ollama pull qwen2.5:7b` |
| `llama3.1:8b` | ~6 GB | `ollama pull llama3.1:8b` (default) |

### 3 — Clone and set up this repository

```bash
git clone https://github.com/HainLee00/Training_Test.git
cd Training_Test

# Run the automated setup script
bash setup.sh

# Activate the virtual environment
source .venv/bin/activate
```

The setup script will:
- Check your Python version
- Create a virtual environment
- Install all dependencies (including `tradingagents` from GitHub)
- Copy `.env.example` → `.env`
- Verify Ollama is running and pull the model

### 4 — Run an analysis

```bash
# Analyse Apple on a specific date (debug mode streams agent messages)
python main.py --ticker AAPL --date 2024-05-10 --debug

# Analyse NVIDIA with default date (yesterday)
python main.py --ticker NVDA

# Use only some analysts and more debate rounds
python main.py --ticker TSLA --analysts market fundamentals --debate-rounds 2
```

---

## Configuration

### Environment Variables (`.env`)

Copy `.env.example` to `.env` and customise:

```bash
# Change models (must be pulled locally first)
DEEP_THINK_MODEL=llama3.1:8b    # used for complex reasoning tasks
QUICK_THINK_MODEL=llama3.1:8b   # used for lighter tasks (can be smaller)
```

### `free_config.py`

The central configuration file for the free-tools setup. Key settings:

```python
FREE_CONFIG = {
    "llm_provider": "ollama",           # Local Ollama server
    "deep_think_llm": "llama3.1:8b",    # Override via DEEP_THINK_MODEL env var
    "quick_think_llm": "llama3.1:8b",   # Override via QUICK_THINK_MODEL env var
    "backend_url": "http://localhost:11434/v1",  # Ollama OpenAI-compatible API

    "max_debate_rounds": 1,             # Bull-vs-bear rounds (more = richer analysis)
    "max_risk_discuss_rounds": 1,       # Risk team rounds

    "data_vendors": {                   # All free via Yahoo Finance
        "core_stock_apis":      "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data":     "yfinance",
        "news_data":            "yfinance",
    },
}
```

### CLI Options

```
python main.py [OPTIONS]

Options:
  --ticker TEXT          Stock ticker symbol (default: AAPL)
  --date TEXT            Trade date YYYY-MM-DD (default: yesterday)
  --analysts [market|social|news|fundamentals]...
                         Which analysts to include (default: all four)
  --debate-rounds INT    Bull-vs-bear debate rounds (default: 1)
  --risk-rounds INT      Risk management rounds (default: 1)
  --debug                Stream all agent messages to stdout
```

---

## Project Structure

```
Training_Test/
├── main.py              # Entry point – run an analysis
├── free_config.py       # Free-tools configuration (Ollama + yfinance)
├── setup.sh             # One-shot setup script
├── pyproject.toml       # Python package metadata and dependencies
├── .env.example         # Environment variable template
├── .env                 # Your local settings (not committed)
├── results/             # Analysis results (auto-created)
└── data_cache/          # Cached market data (auto-created)
```

---

## How It Works

1. **Analyst phase (parallel):** Each analyst agent calls the appropriate yfinance tool to fetch market data, then uses the local Ollama LLM to write a detailed report.

2. **Research debate:** The Bull and Bear researcher agents read all analyst reports and debate the investment thesis over one or more rounds.

3. **Research Manager synthesizes** the debate and produces an investment recommendation.

4. **Trader** translates the research output into a concrete trade proposal (BUY/SELL/HOLD with rationale).

5. **Risk Management debate:** Three risk agents (aggressive, conservative, neutral) debate the appropriate position size and risk limits.

6. **Portfolio Manager** reviews all inputs and issues the final trade decision.

State is managed by [LangGraph](https://github.com/langchain-ai/langgraph), which handles the message routing and debate termination conditions automatically.

---

## Troubleshooting

### `Connection refused` or `Ollama not reachable`
Make sure Ollama is running: `ollama serve`

### Model not found
Pull the model first: `ollama pull llama3.1:8b`

### `Error initialising TradingAgentsGraph`
- Confirm Ollama is running on port 11434
- Confirm the model name in `.env` matches an installed model (`ollama list`)

### Slow responses
- Use a smaller/faster model: `QUICK_THINK_MODEL=qwen2.5:3b` in `.env`
- Reduce debate rounds: `--debate-rounds 1 --risk-rounds 1`

### yfinance data errors
- Some tickers may have limited data on Yahoo Finance
- Try a major ticker (AAPL, MSFT, GOOGL) to verify the setup

---

## Credits

Built on [TradingAgents](https://github.com/TauricResearch/TradingAgents) by [TauricResearch](https://github.com/TauricResearch), which provides the multi-agent orchestration framework. This repository adapts it to use **only free and open-source tools**.

---

## License

This project inherits the [AGPL-3.0](https://github.com/TauricResearch/TradingAgents/blob/main/LICENSE) license from the upstream TradingAgents framework.
