#!/usr/bin/env python3
"""
LLM Multi-Agent Trading System – free-tools entry point.

Uses:
  - Ollama for local, free LLM inference (llama3.1:8b by default)
  - Yahoo Finance (yfinance) for free market data

Usage:
    python main.py [--ticker TICKER] [--date YYYY-MM-DD] [--debug]

Requires:
    Ollama running locally with at least one model pulled.
    See README.md for setup instructions.
"""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load any optional env overrides from .env (e.g. DEEP_THINK_MODEL)
load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from free_config import FREE_CONFIG


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the free-tools LLM multi-agent trading system."
    )
    parser.add_argument(
        "--ticker",
        default="AAPL",
        help="Stock ticker symbol to analyse (default: AAPL).",
    )
    parser.add_argument(
        "--date",
        default=str(date.today() - timedelta(days=1)),
        help="Trade date in YYYY-MM-DD format (default: yesterday).",
    )
    parser.add_argument(
        "--analysts",
        nargs="+",
        choices=["market", "social", "news", "fundamentals"],
        default=["market", "social", "news", "fundamentals"],
        help="Which analyst agents to include (default: all four).",
    )
    parser.add_argument(
        "--debate-rounds",
        type=int,
        default=FREE_CONFIG["max_debate_rounds"],
        help="Number of bull-vs-bear debate rounds (default: 1).",
    )
    parser.add_argument(
        "--risk-rounds",
        type=int,
        default=FREE_CONFIG["max_risk_discuss_rounds"],
        help="Number of risk-management debate rounds (default: 1).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Stream agent messages to stdout for debugging.",
    )
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> dict:
    """Merge the default config with free-tool overrides and CLI arguments."""
    config = DEFAULT_CONFIG.copy()
    config.update(FREE_CONFIG)

    # Apply CLI overrides
    config["max_debate_rounds"] = args.debate_rounds
    config["max_risk_discuss_rounds"] = args.risk_rounds

    # Ensure cache directories exist
    Path(config["results_dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["data_cache_dir"]).mkdir(parents=True, exist_ok=True)

    return config


def main() -> None:
    args = parse_args()
    config = build_config(args)

    print(f"\n{'='*60}")
    print(f"  Trading Agents – Free Tools Setup")
    print(f"{'='*60}")
    print(f"  Ticker        : {args.ticker}")
    print(f"  Trade date    : {args.date}")
    print(f"  LLM provider  : Ollama (local)")
    print(f"  Deep model    : {config['deep_think_llm']}")
    print(f"  Quick model   : {config['quick_think_llm']}")
    print(f"  Data provider : yfinance (free)")
    print(f"  Analysts      : {', '.join(args.analysts)}")
    print(f"  Debate rounds : {config['max_debate_rounds']}")
    print(f"  Risk rounds   : {config['max_risk_discuss_rounds']}")
    print(f"{'='*60}\n")

    try:
        ta = TradingAgentsGraph(
            selected_analysts=args.analysts,
            debug=args.debug,
            config=config,
        )
    except Exception as exc:
        print(f"[ERROR] Failed to initialise TradingAgentsGraph: {exc}")
        print("\nMake sure Ollama is running and the model is available:")
        print(f"  ollama serve")
        print(f"  ollama pull {config['deep_think_llm']}")
        sys.exit(1)

    print(f"Running analysis for {args.ticker} on {args.date} ...\n")

    try:
        final_state, decision = ta.propagate(args.ticker, args.date)
    except Exception as exc:
        print(f"[ERROR] Analysis failed: {exc}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("  FINAL TRADE DECISION")
    print(f"{'='*60}")
    print(decision)
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
