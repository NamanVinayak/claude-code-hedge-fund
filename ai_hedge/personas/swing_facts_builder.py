"""Build facts bundles for swing mode strategy agents.

Each swing agent gets the same base indicators (EMAs, RSI, MACD, Bollinger,
ATR, ADX, volume, support/resistance, Fibonacci, momentum, Z-score,
stochastic, Williams %R, CCI, MFI) plus recent price action, insider
activity, and news.  The agent prompts tell each one what to focus on.

The Head Trader reads the 9 strategy signals directly — no facts bundle needed.

Usage:
    python -m ai_hedge.personas.swing_facts_builder --run-id <id> --tickers AAPL,MSFT
"""
from __future__ import annotations

import argparse
import json
import math
import os
from typing import Any

import numpy as np
import pandas as pd

from ai_hedge.data.api import prices_to_df
from ai_hedge.data.models import Price

try:
    import pandas_ta as _ta
    _HAS_PANDAS_TA = True
except ImportError:
    _HAS_PANDAS_TA = False


# ── indicator helpers ────────────────────────────────────────────────────────

def _safe(v: Any) -> Any:
    """Coerce numpy/float specials to JSON-safe types."""
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else round(f, 4)
    if isinstance(v, float):
        return None if (math.isnan(v) or math.isinf(v)) else round(v, 4)
    return v


def _ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def _sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()


def _compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def _compute_macd(close: pd.Series):
    ema12 = _ema(close, 12)
    ema26 = _ema(close, 26)
    macd_line = ema12 - ema26
    signal_line = _ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def _compute_bollinger(close: pd.Series, window: int = 20, num_std: float = 2.0):
    sma = _sma(close, window)
    std = close.rolling(window=window).std()
    upper = sma + num_std * std
    lower = sma - num_std * std
    width = (upper - lower) / sma
    return upper, sma, lower, width


def _compute_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def _compute_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Compute ADX (Average Directional Index)."""
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

    atr = _compute_atr(high, low, close, period)
    plus_di = 100 * _ema(plus_dm, period) / atr
    minus_di = 100 * _ema(minus_dm, period) / atr

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = _ema(dx, period)
    return adx


def _compute_stochastic(high: pd.Series, low: pd.Series, close: pd.Series,
                         k_period: int = 14, d_period: int = 3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d


def _compute_williams_r(high: pd.Series, low: pd.Series, close: pd.Series,
                         period: int = 14) -> pd.Series:
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    return -100 * (highest_high - close) / (highest_high - lowest_low)


def _compute_cci(high: pd.Series, low: pd.Series, close: pd.Series,
                  period: int = 20) -> pd.Series:
    tp = (high + low + close) / 3
    sma_tp = _sma(tp, period)
    mean_dev = tp.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    return (tp - sma_tp) / (0.015 * mean_dev)


def _compute_mfi(high: pd.Series, low: pd.Series, close: pd.Series,
                  volume: pd.Series, period: int = 14) -> pd.Series:
    tp = (high + low + close) / 3
    raw_mf = tp * volume
    positive_mf = raw_mf.where(tp > tp.shift(), 0.0).rolling(window=period).sum()
    negative_mf = raw_mf.where(tp < tp.shift(), 0.0).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi


def _find_support_resistance(close: pd.Series, window: int = 20) -> dict:
    """Find simple support/resistance from recent highs and lows."""
    recent = close.tail(window)
    if recent.empty:
        return {"support": None, "resistance": None}
    return {
        "support": _safe(recent.min()),
        "resistance": _safe(recent.max()),
    }


def _compute_fibonacci(close: pd.Series, window: int = 50) -> dict:
    """Compute Fibonacci retracement levels from the recent swing range."""
    recent = close.tail(window)
    if recent.empty:
        return {}
    high = recent.max()
    low = recent.min()
    diff = high - low
    return {
        "swing_high": _safe(high),
        "swing_low": _safe(low),
        "fib_236": _safe(high - 0.236 * diff),
        "fib_382": _safe(high - 0.382 * diff),
        "fib_500": _safe(high - 0.500 * diff),
        "fib_618": _safe(high - 0.618 * diff),
        "fib_786": _safe(high - 0.786 * diff),
    }


def compute_daily_indicators(df: pd.DataFrame) -> dict:
    """Compute all swing-relevant daily technical indicators from a prices DataFrame.

    Expects columns: open, high, low, close, volume (and a DatetimeIndex or 'date' column).
    Returns a dict of the latest values for all indicators.
    """
    if df.empty or len(df) < 21:
        return {}

    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    # EMAs
    ema10 = _ema(close, 10)
    ema21 = _ema(close, 21)
    ema50 = _ema(close, 50)
    sma50 = _sma(close, 50)
    sma200 = _sma(close, 200)

    # RSI
    rsi = _compute_rsi(close, 14)

    # MACD
    macd_line, macd_signal, macd_hist = _compute_macd(close)

    # Bollinger Bands
    bb_upper, bb_mid, bb_lower, bb_width = _compute_bollinger(close, 20, 2.0)

    # ATR
    atr = _compute_atr(high, low, close, 14)

    # ADX
    adx = _compute_adx(high, low, close, 14)

    # Volume averages
    vol_avg20 = _sma(volume, 20)

    # Momentum / ROC
    roc5 = close.pct_change(5) * 100
    roc10 = close.pct_change(10) * 100
    roc21 = close.pct_change(21) * 100

    # Z-score (price vs 50-day mean/std)
    z_mean = _sma(close, 50)
    z_std = close.rolling(window=50).std()
    z_score = (close - z_mean) / z_std

    # Stochastic
    stoch_k, stoch_d = _compute_stochastic(high, low, close)

    # Williams %R
    williams_r = _compute_williams_r(high, low, close)

    # CCI
    cci = _compute_cci(high, low, close)

    # MFI
    mfi = _compute_mfi(high, low, close, volume)

    # Support / Resistance
    sr = _find_support_resistance(close, 20)

    # Fibonacci
    fib = _compute_fibonacci(close, 50)

    # EMA alignment
    latest_ema10 = ema10.iloc[-1]
    latest_ema21 = ema21.iloc[-1]
    latest_ema50 = ema50.iloc[-1] if len(ema50.dropna()) > 0 else None
    if latest_ema50 is not None:
        ema_aligned_up = latest_ema10 > latest_ema21 > latest_ema50
        ema_aligned_down = latest_ema10 < latest_ema21 < latest_ema50
    else:
        ema_aligned_up = None
        ema_aligned_down = None

    # Bollinger Band position
    latest_close = close.iloc[-1]
    bb_position = None
    if bb_upper.iloc[-1] and bb_lower.iloc[-1]:
        bb_range = bb_upper.iloc[-1] - bb_lower.iloc[-1]
        if bb_range > 0:
            bb_position = (latest_close - bb_lower.iloc[-1]) / bb_range

    # Distance from 50-SMA
    dist_from_50sma = None
    if sma50.iloc[-1] and sma50.iloc[-1] > 0:
        dist_from_50sma = ((latest_close - sma50.iloc[-1]) / sma50.iloc[-1]) * 100

    # Volume ratio (today vs 20-day avg)
    vol_ratio = None
    if vol_avg20.iloc[-1] and vol_avg20.iloc[-1] > 0:
        vol_ratio = volume.iloc[-1] / vol_avg20.iloc[-1]

    indicators = {
        "moving_averages": {
            "ema_10": _safe(ema10.iloc[-1]),
            "ema_21": _safe(ema21.iloc[-1]),
            "ema_50": _safe(ema50.iloc[-1]) if len(ema50.dropna()) > 0 else None,
            "sma_50": _safe(sma50.iloc[-1]) if len(sma50.dropna()) > 0 else None,
            "sma_200": _safe(sma200.iloc[-1]) if len(sma200.dropna()) > 0 else None,
            "ema_aligned_uptrend": ema_aligned_up,
            "ema_aligned_downtrend": ema_aligned_down,
        },
        "rsi": _safe(rsi.iloc[-1]),
        "macd": {
            "macd_line": _safe(macd_line.iloc[-1]),
            "signal_line": _safe(macd_signal.iloc[-1]),
            "histogram": _safe(macd_hist.iloc[-1]),
        },
        "bollinger_bands": {
            "upper": _safe(bb_upper.iloc[-1]),
            "middle": _safe(bb_mid.iloc[-1]),
            "lower": _safe(bb_lower.iloc[-1]),
            "width": _safe(bb_width.iloc[-1]),
            "position": _safe(bb_position),
        },
        "atr": _safe(atr.iloc[-1]),
        "adx": _safe(adx.iloc[-1]),
        "volume": {
            "current": _safe(volume.iloc[-1]),
            "avg_20": _safe(vol_avg20.iloc[-1]),
            "ratio_vs_avg": _safe(vol_ratio),
        },
        "support_resistance": sr,
        "fibonacci": fib,
        "momentum": {
            "roc_5": _safe(roc5.iloc[-1]),
            "roc_10": _safe(roc10.iloc[-1]),
            "roc_21": _safe(roc21.iloc[-1]),
        },
        "z_score": _safe(z_score.iloc[-1]),
        "dist_from_50sma_pct": _safe(dist_from_50sma),
        "stochastic": {
            "k": _safe(stoch_k.iloc[-1]),
            "d": _safe(stoch_d.iloc[-1]),
        },
        "williams_r": _safe(williams_r.iloc[-1]),
        "cci": _safe(cci.iloc[-1]),
        "mfi": _safe(mfi.iloc[-1]),
    }

    # pandas_ta extras: STC, Squeeze Momentum, SuperTrend
    # (added after building base dict so we can return with or without them)
    if _HAS_PANDAS_TA:
        # Schaff Trend Cycle
        try:
            stc_df = _ta.stc(close, tclength=10, fast=23, slow=50, factor=0.5)
            if stc_df is not None and not stc_df.empty:
                indicators["stc"] = {
                    "value": _safe(float(stc_df.iloc[-1, 0])),
                    "signal": "overbought" if float(stc_df.iloc[-1, 0]) > 75 else "oversold" if float(stc_df.iloc[-1, 0]) < 25 else "neutral",
                    "prev_value": _safe(float(stc_df.iloc[-2, 0])) if len(stc_df) > 1 else None,
                    "crossed_above_25": float(stc_df.iloc[-1, 0]) > 25 and float(stc_df.iloc[-2, 0]) <= 25 if len(stc_df) > 1 else False,
                    "crossed_below_75": float(stc_df.iloc[-1, 0]) < 75 and float(stc_df.iloc[-2, 0]) >= 75 if len(stc_df) > 1 else False,
                }
        except Exception:
            pass

        # Squeeze Momentum
        try:
            squeeze_df = _ta.squeeze(high, low, close, lazybear=True)
            if squeeze_df is not None and not squeeze_df.empty:
                cols = squeeze_df.columns.tolist()
                sqz_on_col = [c for c in cols if 'SQZ' in c and 'ON' in c.upper()]
                sqz_off_col = [c for c in cols if 'SQZ' in c and 'OFF' in c.upper()]
                mom_col = [c for c in cols if 'LB' in c]

                mom_val = float(squeeze_df[mom_col[0]].iloc[-1]) if mom_col else 0.0
                prev_mom = float(squeeze_df[mom_col[0]].iloc[-2]) if mom_col and len(squeeze_df) > 1 else 0.0
                is_off = sqz_off_col and bool(squeeze_df[sqz_off_col[0]].iloc[-1])
                is_on = sqz_on_col and bool(squeeze_df[sqz_on_col[0]].iloc[-1])

                indicators["squeeze"] = {
                    "squeeze_on": bool(squeeze_df[sqz_on_col[0]].iloc[-1]) if sqz_on_col else None,
                    "squeeze_off": bool(squeeze_df[sqz_off_col[0]].iloc[-1]) if sqz_off_col else None,
                    "momentum": _safe(mom_val),
                    "momentum_increasing": mom_val > prev_mom if len(squeeze_df) > 1 else None,
                    "signal": "bullish_breakout" if (is_off and mom_val > 0) else
                              "bearish_breakout" if (is_off and mom_val < 0) else
                              "squeeze_building" if is_on else "no_squeeze",
                }
        except Exception:
            pass

        # SuperTrend
        try:
            st_df = _ta.supertrend(high, low, close, length=10, multiplier=3.0)
            if st_df is not None and not st_df.empty:
                cols = st_df.columns.tolist()
                trend_col = [c for c in cols if 'SUPERTd' in c][0]
                value_col = [c for c in cols if 'SUPERT_' in c and 'SUPERTd' not in c][0]

                direction = int(st_df[trend_col].iloc[-1])
                supertrend_value = float(st_df[value_col].iloc[-1])
                prev_direction = int(st_df[trend_col].iloc[-2]) if len(st_df) > 1 else direction

                indicators["supertrend"] = {
                    "value": _safe(supertrend_value),
                    "direction": "bullish" if direction == 1 else "bearish",
                    "trend_changed": direction != prev_direction,
                    "distance_pct": _safe((float(close.iloc[-1]) - supertrend_value) / supertrend_value * 100),
                }
        except Exception:
            pass

    return indicators


# ── swing agent list ─────────────────────────────────────────────────────────

SWING_AGENTS = [
    "swing_trend_follower",
    "swing_pullback_trader",
    "swing_breakout_trader",
    "swing_momentum_ranker",
    "swing_mean_reversion",
    "swing_catalyst_trader",
    "swing_sector_rotation",
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

        daily_indicators = compute_daily_indicators(prices_df) if not prices_df.empty else {}

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
