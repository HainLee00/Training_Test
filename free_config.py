# ── Free-tools configuration for TradingAgents ──────────────────────────────
#
# LLM provider : Ollama  (runs local models on your own machine, 100% free)
# Data provider: yfinance (Yahoo Finance, no API key required)
#
# Ollama must be installed and running before using this project.
# See README.md for full setup instructions.

import os
from pathlib import Path

FREE_CONFIG = {
    # ── Directories ────────────────────────────────────────────────────────
    "results_dir": str(Path("results").resolve()),
    "data_cache_dir": str(Path("data_cache").resolve()),

    # ── LLM settings ──────────────────────────────────────────────────────
    # Use "ollama" so the framework routes to the local Ollama server.
    # The OpenAI-compatible endpoint is http://localhost:11434/v1.
    "llm_provider": "ollama",

    # Model used for complex multi-step reasoning (researchers, risk debate).
    # Recommended: llama3.1:8b  |  mistral:7b  |  qwen2.5:7b
    # Smaller option for low-RAM machines: qwen2.5:3b
    "deep_think_llm": os.getenv("DEEP_THINK_MODEL", "llama3.1:8b"),

    # Model used for quick, lightweight tasks (message routing, summaries).
    # Can be the same model as deep_think_llm, or a lighter one.
    "quick_think_llm": os.getenv("QUICK_THINK_MODEL", "llama3.1:8b"),

    # Ollama serves an OpenAI-compatible REST API on this URL.
    "backend_url": "http://localhost:11434/v1",

    # Provider-specific thinking controls (not applicable to Ollama – leave None).
    "google_thinking_level": None,
    "openai_reasoning_effort": None,
    "anthropic_effort": None,

    # ── Debate / discussion settings ───────────────────────────────────────
    # Increase these for richer analysis at the cost of more LLM calls.
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,

    # ── Data vendors (all free via Yahoo Finance / yfinance) ───────────────
    # yfinance requires no API key and has generous rate limits.
    "data_vendors": {
        "core_stock_apis":      "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data":     "yfinance",
        "news_data":            "yfinance",
    },

    # Per-tool overrides (empty means every tool uses its category default).
    "tool_vendors": {},
}
