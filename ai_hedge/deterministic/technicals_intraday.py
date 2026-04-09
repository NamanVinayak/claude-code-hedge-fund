"""
Intraday Technical Analyst — deterministic agent operating on 5-minute bars.

Same concept as technicals.py but adapted for intraday timeframes:
1. Trend following with EMA 9/20/50 on 5-min
2. Mean reversion with intraday Bollinger Bands
3. Momentum with intraday RSI/MACD
4. Volatility with intraday ATR
5. VWAP position analysis (replaces statistical arbitrage)
"""
import math
import json

import numpy as np
import pandas as pd
from langchain_core.messages import HumanMessage

from ai_hedge.data.api import get_intraday_prices, intraday_to_df

AgentState = dict


def show_agent_reasoning(output, agent_name):
    import json
    print(f"\n{'=' * 10} {agent_name.center(28)} {'=' * 10}")
    if isinstance(output, (dict, list)):
        print(json.dumps(output, indent=2, default=str))
    else:
        print(output)
    print("=" * 48)


class _NoopProgress:
    def update_status(self, *args, **kwargs):
        pass


progress = _NoopProgress()


def safe_float(value, default=0.0):
    try:
        if pd.isna(value) or np.isnan(value):
            return default
        return float(value)
    except (ValueError, TypeError, OverflowError):
        return default


# ── Technical indicator helpers ──────────────────────────────────────────────

def _calculate_ema(series: pd.Series, window: int) -> pd.Series:
    return series.ewm(span=window, adjust=False).mean()


def _calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _calculate_macd(series: pd.Series) -> dict:
    ema_12 = _calculate_ema(series, 12)
    ema_26 = _calculate_ema(series, 26)
    macd_line = ema_12 - ema_26
    signal_line = _calculate_ema(macd_line, 9)
    histogram = macd_line - signal_line
    return {"macd": macd_line, "signal": signal_line, "histogram": histogram}


def _calculate_bollinger_bands(series: pd.Series, window: int = 20) -> tuple:
    sma = series.rolling(window).mean()
    std = series.rolling(window).std()
    return sma + (std * 2), sma, sma - (std * 2)


def _calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(period).mean()


def _calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """Cumulative VWAP from intraday data."""
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    cum_vol = df["volume"].cumsum()
    cum_tp_vol = (typical_price * df["volume"]).cumsum()
    vwap = cum_tp_vol / cum_vol
    return vwap


# ── Strategy signals ─────────────────────────────────────────────────────────

def _intraday_trend_signals(df: pd.DataFrame) -> dict:
    """Trend following with EMA 9/20/50 on 5-min bars."""
    close = df["close"]
    ema_9 = _calculate_ema(close, 9)
    ema_20 = _calculate_ema(close, 20)
    ema_50 = _calculate_ema(close, 50)

    short_trend = ema_9.iloc[-1] > ema_20.iloc[-1]
    medium_trend = ema_20.iloc[-1] > ema_50.iloc[-1]

    # Trend strength from EMA spread
    spread = abs(ema_9.iloc[-1] - ema_50.iloc[-1]) / close.iloc[-1]
    trend_strength = min(spread * 100, 1.0)

    if short_trend and medium_trend:
        signal = "bullish"
        confidence = 0.5 + trend_strength * 0.5
    elif not short_trend and not medium_trend:
        signal = "bearish"
        confidence = 0.5 + trend_strength * 0.5
    else:
        signal = "neutral"
        confidence = 0.5

    return {
        "signal": signal,
        "confidence": min(confidence, 1.0),
        "metrics": {
            "ema_9": safe_float(ema_9.iloc[-1]),
            "ema_20": safe_float(ema_20.iloc[-1]),
            "ema_50": safe_float(ema_50.iloc[-1]),
            "trend_strength": safe_float(trend_strength),
        },
    }


def _intraday_mean_reversion_signals(df: pd.DataFrame) -> dict:
    """Mean reversion with intraday Bollinger Bands."""
    close = df["close"]
    bb_upper, bb_mid, bb_lower = _calculate_bollinger_bands(close, 20)
    rsi = _calculate_rsi(close, 14)

    # Z-score from intraday mean
    intraday_mean = close.expanding().mean()
    intraday_std = close.expanding().std()
    z_score = (close.iloc[-1] - intraday_mean.iloc[-1]) / intraday_std.iloc[-1] if intraday_std.iloc[-1] > 0 else 0

    # Position within Bollinger Bands
    bb_range = bb_upper.iloc[-1] - bb_lower.iloc[-1]
    if bb_range > 0:
        price_vs_bb = (close.iloc[-1] - bb_lower.iloc[-1]) / bb_range
    else:
        price_vs_bb = 0.5

    current_rsi = safe_float(rsi.iloc[-1], 50)

    if z_score < -2 and price_vs_bb < 0.2 and current_rsi < 25:
        signal = "bullish"
        confidence = min(abs(z_score) / 4, 1.0)
    elif z_score > 2 and price_vs_bb > 0.8 and current_rsi > 75:
        signal = "bearish"
        confidence = min(abs(z_score) / 4, 1.0)
    else:
        signal = "neutral"
        confidence = 0.5

    return {
        "signal": signal,
        "confidence": confidence,
        "metrics": {
            "z_score": safe_float(z_score),
            "price_vs_bb": safe_float(price_vs_bb),
            "rsi_14": safe_float(current_rsi),
            "bb_upper": safe_float(bb_upper.iloc[-1]),
            "bb_mid": safe_float(bb_mid.iloc[-1]),
            "bb_lower": safe_float(bb_lower.iloc[-1]),
        },
    }


def _intraday_momentum_signals(df: pd.DataFrame) -> dict:
    """Momentum with intraday RSI and MACD."""
    close = df["close"]
    rsi = _calculate_rsi(close, 14)
    macd = _calculate_macd(close)

    returns = close.pct_change()
    mom_short = returns.rolling(12).sum()  # ~1 hour of 5-min bars
    mom_medium = returns.rolling(36).sum()  # ~3 hours

    # Volume momentum
    volume_ma = df["volume"].rolling(20).mean()
    volume_momentum = df["volume"].iloc[-1] / volume_ma.iloc[-1] if volume_ma.iloc[-1] > 0 else 1.0

    current_rsi = safe_float(rsi.iloc[-1], 50)
    macd_hist = safe_float(macd["histogram"].iloc[-1])
    mom_score = safe_float(mom_short.iloc[-1]) * 0.6 + safe_float(mom_medium.iloc[-1]) * 0.4

    if mom_score > 0.005 and macd_hist > 0 and volume_momentum > 1.0:
        signal = "bullish"
        confidence = min(abs(mom_score) * 50 + 0.3, 1.0)
    elif mom_score < -0.005 and macd_hist < 0 and volume_momentum > 1.0:
        signal = "bearish"
        confidence = min(abs(mom_score) * 50 + 0.3, 1.0)
    else:
        signal = "neutral"
        confidence = 0.5

    return {
        "signal": signal,
        "confidence": confidence,
        "metrics": {
            "rsi_14": safe_float(current_rsi),
            "macd_histogram": macd_hist,
            "momentum_short": safe_float(mom_short.iloc[-1]),
            "momentum_medium": safe_float(mom_medium.iloc[-1]),
            "volume_momentum": safe_float(volume_momentum),
        },
    }


def _intraday_volatility_signals(df: pd.DataFrame) -> dict:
    """Volatility analysis with intraday ATR."""
    close = df["close"]
    returns = close.pct_change()

    # Intraday volatility
    hist_vol = returns.rolling(20).std()
    vol_ma = hist_vol.rolling(40).mean()

    atr = _calculate_atr(df, 14)
    atr_ratio = atr / close

    # Volatility regime
    if vol_ma.iloc[-1] > 0:
        vol_regime = hist_vol.iloc[-1] / vol_ma.iloc[-1]
    else:
        vol_regime = 1.0

    # Volatility z-score
    vol_std = hist_vol.rolling(40).std()
    if vol_std.iloc[-1] > 0:
        vol_z = (hist_vol.iloc[-1] - vol_ma.iloc[-1]) / vol_std.iloc[-1]
    else:
        vol_z = 0.0

    if vol_regime < 0.8 and vol_z < -1:
        signal = "bullish"  # Low vol, potential expansion
        confidence = min(abs(vol_z) / 3, 1.0)
    elif vol_regime > 1.3 and vol_z > 1:
        signal = "bearish"  # High vol, risk-off
        confidence = min(abs(vol_z) / 3, 1.0)
    else:
        signal = "neutral"
        confidence = 0.5

    return {
        "signal": signal,
        "confidence": confidence,
        "metrics": {
            "intraday_volatility": safe_float(hist_vol.iloc[-1]),
            "volatility_regime": safe_float(vol_regime),
            "volatility_z_score": safe_float(vol_z),
            "atr_ratio": safe_float(atr_ratio.iloc[-1]),
        },
    }


def _intraday_vwap_signals(df: pd.DataFrame) -> dict:
    """VWAP position analysis — replaces stat arb for intraday."""
    close = df["close"]
    vwap = _calculate_vwap(df)

    # Distance from VWAP
    vwap_dist = (close.iloc[-1] - vwap.iloc[-1]) / vwap.iloc[-1] if vwap.iloc[-1] > 0 else 0

    # VWAP bands (standard deviation around VWAP)
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    vwap_dev = ((typical_price - vwap) ** 2 * df["volume"]).cumsum() / df["volume"].cumsum()
    vwap_std = np.sqrt(vwap_dev)
    upper_band = vwap + vwap_std
    lower_band = vwap - vwap_std

    # Check price position relative to VWAP
    above_vwap = close.iloc[-1] > vwap.iloc[-1]

    # Volume-weighted direction: are recent bars above or below VWAP?
    recent_bars = min(12, len(df))
    recent_above = sum(1 for i in range(-recent_bars, 0) if close.iloc[i] > vwap.iloc[i])
    vwap_consistency = recent_above / recent_bars

    if above_vwap and vwap_consistency > 0.7 and vwap_dist > 0.001:
        signal = "bullish"
        confidence = min(0.5 + vwap_consistency * 0.3 + abs(vwap_dist) * 20, 1.0)
    elif not above_vwap and vwap_consistency < 0.3 and vwap_dist < -0.001:
        signal = "bearish"
        confidence = min(0.5 + (1 - vwap_consistency) * 0.3 + abs(vwap_dist) * 20, 1.0)
    else:
        signal = "neutral"
        confidence = 0.5

    return {
        "signal": signal,
        "confidence": confidence,
        "metrics": {
            "vwap": safe_float(vwap.iloc[-1]),
            "vwap_distance_pct": safe_float(vwap_dist * 100),
            "vwap_upper_band": safe_float(upper_band.iloc[-1]),
            "vwap_lower_band": safe_float(lower_band.iloc[-1]),
            "bars_above_vwap_pct": safe_float(vwap_consistency * 100),
        },
    }


def _weighted_signal_combination(signals: dict, weights: dict) -> dict:
    """Combine multiple trading signals using a weighted approach."""
    signal_values = {"bullish": 1, "neutral": 0, "bearish": -1}

    weighted_sum = 0
    total_confidence = 0

    for strategy, signal in signals.items():
        numeric_signal = signal_values[signal["signal"]]
        weight = weights[strategy]
        confidence = signal["confidence"]

        weighted_sum += numeric_signal * weight * confidence
        total_confidence += weight * confidence

    if total_confidence > 0:
        final_score = weighted_sum / total_confidence
    else:
        final_score = 0

    if final_score > 0.2:
        signal = "bullish"
    elif final_score < -0.2:
        signal = "bearish"
    else:
        signal = "neutral"

    return {"signal": signal, "confidence": abs(final_score)}


def _normalize_pandas(obj):
    """Convert pandas Series/DataFrames to primitive Python types."""
    if isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict("records")
    elif isinstance(obj, dict):
        return {k: _normalize_pandas(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_normalize_pandas(item) for item in obj]
    return obj


# ── Main agent function ──────────────────────────────────────────────────────

def technical_intraday_analyst_agent(
    state: AgentState,
    agent_id: str = "technical_intraday_analyst_agent",
) -> dict:
    """
    Intraday technical analysis combining 5 strategies on 5-minute bars:
    1. Trend Following (EMA 9/20/50)
    2. Mean Reversion (Bollinger Bands)
    3. Momentum (RSI/MACD)
    4. Volatility (ATR)
    5. VWAP Position Analysis
    """
    data = state["data"]
    tickers = data["tickers"]

    technical_analysis = {}

    for ticker in tickers:
        progress.update_status(agent_id, ticker, "Fetching intraday data")

        # Fetch intraday prices
        intraday_prices = get_intraday_prices(ticker)
        if not intraday_prices:
            progress.update_status(agent_id, ticker, "Failed: No intraday data found")
            continue

        df = intraday_to_df(intraday_prices)
        if df.empty or len(df) < 50:
            progress.update_status(agent_id, ticker, "Failed: Insufficient intraday data")
            continue

        progress.update_status(agent_id, ticker, "Calculating intraday trend signals")
        trend_signals = _intraday_trend_signals(df)

        progress.update_status(agent_id, ticker, "Calculating intraday mean reversion")
        mean_reversion_signals = _intraday_mean_reversion_signals(df)

        progress.update_status(agent_id, ticker, "Calculating intraday momentum")
        momentum_signals = _intraday_momentum_signals(df)

        progress.update_status(agent_id, ticker, "Analyzing intraday volatility")
        volatility_signals = _intraday_volatility_signals(df)

        progress.update_status(agent_id, ticker, "Analyzing VWAP position")
        vwap_signals = _intraday_vwap_signals(df)

        # Combine with intraday-appropriate weights
        strategy_weights = {
            "trend": 0.20,
            "mean_reversion": 0.15,
            "momentum": 0.25,
            "volatility": 0.15,
            "vwap": 0.25,
        }

        progress.update_status(agent_id, ticker, "Combining intraday signals")
        combined_signal = _weighted_signal_combination(
            {
                "trend": trend_signals,
                "mean_reversion": mean_reversion_signals,
                "momentum": momentum_signals,
                "volatility": volatility_signals,
                "vwap": vwap_signals,
            },
            strategy_weights,
        )

        technical_analysis[ticker] = {
            "signal": combined_signal["signal"],
            "confidence": round(combined_signal["confidence"] * 100),
            "reasoning": {
                "trend_following": {
                    "signal": trend_signals["signal"],
                    "confidence": round(trend_signals["confidence"] * 100),
                    "metrics": _normalize_pandas(trend_signals["metrics"]),
                },
                "mean_reversion": {
                    "signal": mean_reversion_signals["signal"],
                    "confidence": round(mean_reversion_signals["confidence"] * 100),
                    "metrics": _normalize_pandas(mean_reversion_signals["metrics"]),
                },
                "momentum": {
                    "signal": momentum_signals["signal"],
                    "confidence": round(momentum_signals["confidence"] * 100),
                    "metrics": _normalize_pandas(momentum_signals["metrics"]),
                },
                "volatility": {
                    "signal": volatility_signals["signal"],
                    "confidence": round(volatility_signals["confidence"] * 100),
                    "metrics": _normalize_pandas(volatility_signals["metrics"]),
                },
                "vwap_analysis": {
                    "signal": vwap_signals["signal"],
                    "confidence": round(vwap_signals["confidence"] * 100),
                    "metrics": _normalize_pandas(vwap_signals["metrics"]),
                },
            },
        }
        progress.update_status(agent_id, ticker, "Done", analysis=json.dumps(technical_analysis, indent=4))

    # Create the message
    message = HumanMessage(
        content=json.dumps(technical_analysis),
        name=agent_id,
    )

    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(technical_analysis, "Intraday Technical Analyst")

    state["data"]["analyst_signals"][agent_id] = technical_analysis

    progress.update_status(agent_id, None, "Done")

    return {
        "messages": state.get("messages", []) + [message],
        "data": data,
    }


# Alias for convenience
technicals_intraday_agent = technical_intraday_analyst_agent
