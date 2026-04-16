"""
Build per-agent facts bundles for Day Trade mode from raw data + intraday data.

Each bundle contains the intraday indicators, daily context, pre-market data,
recent news, gap analysis, and previous day levels that the DT strategy
subagent needs to produce its signal.

Usage:
    python -m ai_hedge.personas.dt_facts_builder --run-id <id> --tickers AAPL,MSFT
"""
from __future__ import annotations

import argparse
import json
import math
import os
from typing import Any

import numpy as np
import pandas as pd

from ai_hedge.data.api import (
    get_intraday_prices,
    get_premarket_data,
    intraday_to_df,
    prices_to_df,
)
from ai_hedge.data.indicators import (
    compute_daily_indicators,
    compute_intraday_indicators,
)
from ai_hedge.data.models import CompanyNews, Price


# ── JSON serialisation helpers ────────────────────────────────────────────────

def _safe_val(v: Any) -> Any:
    """Coerce numpy scalars and math special values to JSON-safe Python types."""
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def _safe_serialize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _safe_serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_serialize(i) for i in obj]
    if isinstance(obj, pd.Series):
        return _safe_serialize(obj.tolist())
    if isinstance(obj, pd.DataFrame):
        return _safe_serialize(obj.to_dict("records"))
    if hasattr(obj, "model_dump"):
        return _safe_serialize(obj.model_dump())
    return _safe_val(obj)


# ── raw data loading ──────────────────────────────────────────────────────────

def _load_raw(run_id: str, ticker: str) -> dict:
    path = os.path.join("runs", run_id, "raw", f"{ticker}.json")
    with open(path) as f:
        return json.load(f)


# ── gap analysis helper ──────────────────────────────────────────────────────

def _compute_gap_analysis(
    prev_close: float | None,
    current_open: float | None,
    premarket: dict | None,
) -> dict:
    """Compute gap size, direction, and classification hints."""
    if prev_close is None or current_open is None:
        return {"gap_pct": None, "gap_direction": "unknown", "gap_size_category": "unknown"}

    gap_pct = (current_open - prev_close) / prev_close * 100.0

    if abs(gap_pct) < 0.3:
        direction = "flat"
        category = "no_gap"
    elif gap_pct > 0:
        direction = "up"
        category = "large" if gap_pct > 3.0 else ("medium" if gap_pct > 1.5 else "small")
    else:
        direction = "down"
        category = "large" if gap_pct < -3.0 else ("medium" if gap_pct < -1.5 else "small")

    result = {
        "gap_pct": round(gap_pct, 3),
        "gap_direction": direction,
        "gap_size_category": category,
        "prev_close": prev_close,
        "current_open": current_open,
    }

    if premarket:
        result["premarket_high"] = premarket.get("high")
        result["premarket_low"] = premarket.get("low")
        result["premarket_volume"] = premarket.get("volume")

    return result


# ── previous day levels ──────────────────────────────────────────────────────

def _compute_prev_day_levels(raw: dict) -> dict:
    """Extract previous day high, low, close, open from daily price data."""
    prices = raw.get("prices", [])
    if not prices:
        return {}

    # Prices are sorted most recent first typically
    try:
        price_objs = [Price(**p) if isinstance(p, dict) else p for p in prices]
        # Sort by date descending
        price_objs.sort(key=lambda p: p.time, reverse=True)
        if len(price_objs) >= 1:
            prev = price_objs[0]
            result = {
                "prev_day_high": prev.high,
                "prev_day_low": prev.low,
                "prev_day_close": prev.close,
                "prev_day_open": prev.open,
                "prev_day_volume": prev.volume,
                "prev_day_date": prev.time,
            }
            if len(price_objs) >= 2:
                two_days_ago = price_objs[1]
                result["two_days_ago_close"] = two_days_ago.close
            return result
    except Exception:
        pass
    return {}


# ── per-agent facts builder ─────────────────────────────────────────────────

DT_AGENTS = [
    "dt_vwap_trader",
    "dt_momentum_scalper",
    "dt_mean_reversion",
    "dt_breakout_hunter",
    "dt_gap_analyst",
    "dt_volume_profiler",
    "dt_pattern_reader",
    "dt_stat_arb",
    "dt_news_catalyst",
]


def _build_common_facts(
    ticker: str,
    raw: dict,
    intraday_indicators: dict,
    daily_indicators: dict,
    premarket: dict | None,
    gap_analysis: dict,
    prev_day_levels: dict,
    news_items: list[dict],
) -> dict:
    """Build the common facts bundle shared by all DT agents."""
    return {
        "ticker": ticker,
        "intraday_indicators": intraday_indicators,
        "daily_context": daily_indicators,
        "premarket": premarket,
        "gap_analysis": gap_analysis,
        "prev_day_levels": prev_day_levels,
        "recent_news": news_items[:20],
    }


def _build_agent_facts(
    agent_name: str,
    common: dict,
) -> dict:
    """Build agent-specific facts by adding agent-relevant emphasis to common data."""
    facts = dict(common)
    facts["agent"] = agent_name

    # Each agent gets the full data — the prompt tells it what to focus on.
    # We tag which data sections are most relevant for quick reference.
    relevance_map = {
        "dt_vwap_trader": ["intraday_indicators.vwap", "intraday_indicators.volume"],
        "dt_momentum_scalper": ["intraday_indicators.ema", "intraday_indicators.rsi", "intraday_indicators.macd"],
        "dt_mean_reversion": ["intraday_indicators.bollinger", "intraday_indicators.rsi", "intraday_indicators.z_score"],
        "dt_breakout_hunter": ["gap_analysis", "prev_day_levels", "premarket", "intraday_indicators.volume"],
        "dt_gap_analyst": ["gap_analysis", "premarket", "prev_day_levels", "recent_news"],
        "dt_volume_profiler": ["intraday_indicators.obv", "intraday_indicators.volume", "intraday_indicators.ad_line"],
        "dt_pattern_reader": ["intraday_indicators", "prev_day_levels", "gap_analysis"],
        "dt_stat_arb": ["intraday_indicators.hurst", "intraday_indicators.autocorrelation", "intraday_indicators.returns_distribution"],
        "dt_news_catalyst": ["recent_news", "gap_analysis", "premarket"],
    }

    facts["primary_data_sections"] = relevance_map.get(agent_name, [])
    return facts


# ── main orchestrator ──────────────────────────────────────────────────────────

def build_dt_facts(run_id: str, tickers: list[str]) -> None:
    """Build day trade facts bundles for all DT agents × tickers."""
    facts_dir = os.path.join("runs", run_id, "facts")
    os.makedirs(facts_dir, exist_ok=True)

    for ticker in tickers:
        print(f"\nBuilding day trade facts for {ticker}...")

        # Load raw daily data from prepare step
        raw = _load_raw(run_id, ticker)

        # Previous day levels from daily data
        prev_day_levels = _compute_prev_day_levels(raw)

        # Fetch intraday prices
        try:
            intraday_prices = get_intraday_prices(ticker, period="1mo")
            intraday_df = intraday_to_df(intraday_prices) if intraday_prices else pd.DataFrame()
        except Exception as exc:
            print(f"  [WARN] Could not fetch intraday prices for {ticker}: {exc}")
            intraday_df = pd.DataFrame()

        # Compute intraday indicators
        if not intraday_df.empty:
            intraday_indicators = compute_intraday_indicators(intraday_df)
        else:
            intraday_indicators = {}
            print(f"  [WARN] No intraday data for {ticker}, indicators will be empty")

        # Compute daily indicators for context
        daily_prices = raw.get("prices", [])
        if daily_prices:
            try:
                price_objs = [Price(**p) if isinstance(p, dict) else p for p in daily_prices]
                daily_df = prices_to_df(price_objs)
                daily_indicators = compute_daily_indicators(daily_df)
            except Exception as exc:
                daily_indicators = {}
                print(f"  [WARN] Could not compute daily indicators: {exc}")
        else:
            daily_indicators = {}

        # Get pre-market data
        try:
            premarket = get_premarket_data(ticker)
        except Exception as exc:
            premarket = None
            print(f"  [WARN] Could not fetch pre-market data for {ticker}: {exc}")

        # Gap analysis
        prev_close = prev_day_levels.get("prev_day_close")
        current_open = None
        if not intraday_df.empty:
            current_open = float(intraday_df["open"].iloc[0])
        gap_analysis = _compute_gap_analysis(prev_close, current_open, premarket)

        # Recent news
        news_raw = raw.get("company_news", [])
        news_items = []
        for n in news_raw[:20]:
            if isinstance(n, dict):
                news_items.append({
                    "headline": n.get("title", n.get("headline", "")),
                    "sentiment": n.get("sentiment"),
                    "date": n.get("date"),
                })
            else:
                try:
                    obj = CompanyNews(**n) if isinstance(n, dict) else n
                    news_items.append({
                        "headline": obj.title,
                        "sentiment": obj.sentiment,
                        "date": obj.date,
                    })
                except Exception:
                    pass

        # Build common facts
        common = _build_common_facts(
            ticker=ticker,
            raw=raw,
            intraday_indicators=intraday_indicators,
            daily_indicators=daily_indicators,
            premarket=premarket,
            gap_analysis=gap_analysis,
            prev_day_levels=prev_day_levels,
            news_items=news_items,
        )

        # Write per-agent facts
        for agent in DT_AGENTS:
            try:
                facts = _build_agent_facts(agent, common)
                out_path = os.path.join(facts_dir, f"{agent}__{ticker}.json")
                with open(out_path, "w") as f:
                    json.dump(_safe_serialize(facts), f, indent=2, default=str)
                print(f"  wrote facts/{agent}__{ticker}.json")
            except Exception as exc:
                print(f"  [ERROR] {agent}/{ticker}: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Build day trade facts bundles from raw + intraday data.")
    parser.add_argument("--run-id", required=True, help="Run identifier, e.g. 20240101_120000")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    build_dt_facts(args.run_id, tickers)
    print("\nDay trade facts built successfully.")


if __name__ == "__main__":
    main()
