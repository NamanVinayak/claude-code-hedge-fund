"""Build facts bundles for swing mode strategy agents.

Each swing agent gets the same base indicators (EMAs, RSI, MACD, Bollinger,
ATR, ADX, volume, support/resistance, Fibonacci, momentum, Z-score,
stochastic, Williams %R, CCI, MFI, STC, Squeeze, SuperTrend) plus recent
price action, insider activity, and news. The agent prompts tell each one
what to focus on. Indicator math lives in ai_hedge.data.indicators — this
module is just orchestration.

The Head Trader reads the 9 strategy signals directly — no facts bundle needed.

Usage:
    python -m ai_hedge.personas.swing_facts_builder --run-id <id> --tickers AAPL,MSFT
"""
from __future__ import annotations

import argparse
import json
import os

import pandas as pd

from ai_hedge.data.api import get_intraday_prices, intraday_to_df, prices_to_df
from ai_hedge.data.indicators import compute_daily_indicators
from ai_hedge.data.models import Price


# ── swing agent list ─────────────────────────────────────────────────────────

SWING_AGENTS = [
    "swing_trend_momentum",
    "swing_mean_reversion",
    "swing_breakout",
    "swing_catalyst_news",
    "swing_macro_context",
]


# ── main builder ─────────────────────────────────────────────────────────────

def build_swing_facts(run_id: str, tickers: list[str]):
    """Build facts bundles for all swing strategy agents."""
    raw_dir = os.path.join("runs", run_id, "raw")
    facts_dir = os.path.join("runs", run_id, "facts")
    os.makedirs(facts_dir, exist_ok=True)

    for ticker in tickers:
        print(f"\nBuilding swing facts for {ticker}...")
        raw_path = os.path.join(raw_dir, f"{ticker}.json")
        with open(raw_path) as f:
            raw = json.load(f)

        # Convert prices to DataFrame and compute indicators
        prices_raw = raw.get("prices", [])
        prices = [Price(**p) for p in prices_raw] if prices_raw else []
        prices_df = prices_to_df(prices) if prices else pd.DataFrame()

        daily_indicators = compute_daily_indicators(prices_df, timeframe="daily") if not prices_df.empty else {}

        # Fetch hourly bars and compute hourly indicators (multi-timeframe analysis)
        hourly_indicators = {}
        try:
            hourly_prices = get_intraday_prices(ticker, interval="1h", period="1mo")
            hourly_df = intraday_to_df(hourly_prices) if hourly_prices else pd.DataFrame()
            if not hourly_df.empty and len(hourly_df) >= 21:
                hourly_indicators = compute_daily_indicators(hourly_df, timeframe="hourly")
                print(f"  Computed hourly indicators ({len(hourly_df)} bars)")
            elif not hourly_df.empty:
                print(f"  [WARN] Only {len(hourly_df)} hourly bars for {ticker}, need >= 21")
        except Exception as exc:
            print(f"  [WARN] Could not fetch hourly data for {ticker}: {exc}")

        # Recent price action (last 5 days OHLCV)
        recent_prices = prices_raw[-5:] if len(prices_raw) >= 5 else prices_raw

        # Recent insider trades (last 30 days, up to 20)
        insider_trades = raw.get("insider_trades", [])
        recent_insiders = insider_trades[:20] if insider_trades else []

        # News for catalyst detection
        news = raw.get("company_news", [])
        recent_news = news[:15] if news else []

        # Base facts bundle (all swing agents get the same indicators)
        base_facts = {
            "ticker": ticker,
            "daily_indicators": daily_indicators,
            "hourly_indicators": hourly_indicators,
            "recent_prices": recent_prices,
            "recent_insider_trades": recent_insiders,
            "recent_news": recent_news,
            "current_price": raw.get("current_price"),
            "market_cap": raw.get("market_cap"),
        }

        # Write per-agent facts (all get same base; agent prompts tell them what to focus on)
        for agent_name in SWING_AGENTS:
            out_path = os.path.join(facts_dir, f"{agent_name}__{ticker}.json")
            with open(out_path, "w") as f:
                json.dump(base_facts, f, indent=2, default=str)
            print(f"  Built swing facts: {agent_name}__{ticker}")


def main():
    parser = argparse.ArgumentParser(description="Build swing mode facts bundles from raw data.")
    parser.add_argument("--run-id", required=True, help="Run identifier, e.g. 20240101_120000")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    build_swing_facts(args.run_id, tickers)
    print("\nSwing facts built successfully.")


if __name__ == "__main__":
    main()
