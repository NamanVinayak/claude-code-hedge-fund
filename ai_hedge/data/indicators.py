"""Advanced technical indicators via pandas_ta for swing and day trade modes."""

import pandas as pd
import numpy as np

try:
    import pandas_ta as ta
    HAS_PANDAS_TA = True
except ImportError:
    HAS_PANDAS_TA = False


def _find_swing_points(series: pd.Series, window: int = 5):
    """Return indices of local highs and lows using a rolling window."""
    highs, lows = [], []
    for i in range(window, len(series) - window):
        if series.iloc[i] == series.iloc[i - window:i + window + 1].max():
            highs.append(i)
        if series.iloc[i] == series.iloc[i - window:i + window + 1].min():
            lows.append(i)
    return highs, lows


def _find_pivot_levels(prices_df: pd.DataFrame, window: int = 5,
                       lookback: int = 60, touch_tolerance: float = 0.005) -> dict:
    """Find pivot high/low levels with test counts and volume confirmation.

    window: bars on each side to qualify as a local extreme
    lookback: how many bars back to search
    touch_tolerance: how close price must come to "test" a level (0.5% default)
    """
    recent = prices_df.tail(lookback).copy().reset_index(drop=True)
    if len(recent) < window * 2 + 1:
        return {}

    avg_vol = recent["volume"].mean()
    high = recent["high"]
    low = recent["low"]

    pivot_highs = []
    pivot_lows = []

    for i in range(window, len(recent) - window):
        # Pivot high
        if high.iloc[i] == high.iloc[i - window:i + window + 1].max():
            vol_confirmed = recent["volume"].iloc[i] > 1.5 * avg_vol
            level = float(high.iloc[i])
            tests = int(((high >= level * (1 - touch_tolerance)) &
                         (low <= level * (1 + touch_tolerance))).sum())
            pivot_highs.append({
                "price": round(level, 2),
                "tests": tests,
                "volume_confirmed": bool(vol_confirmed),
            })

        # Pivot low
        if low.iloc[i] == low.iloc[i - window:i + window + 1].min():
            vol_confirmed = recent["volume"].iloc[i] > 1.5 * avg_vol
            level = float(low.iloc[i])
            tests = int(((low <= level * (1 + touch_tolerance)) &
                         (high >= level * (1 - touch_tolerance))).sum())
            pivot_lows.append({
                "price": round(level, 2),
                "tests": tests,
                "volume_confirmed": bool(vol_confirmed),
            })

    # Deduplicate levels within 1% of each other (keep the most-tested one)
    def dedup(levels, pct=0.01):
        if not levels:
            return []
        levels = sorted(levels, key=lambda x: -x["tests"])
        kept = [levels[0]]
        for lv in levels[1:]:
            if all(abs(lv["price"] - k["price"]) / k["price"] > pct for k in kept):
                kept.append(lv)
        return sorted(kept, key=lambda x: x["price"])

    pivot_highs = dedup(pivot_highs)
    pivot_lows = dedup(pivot_lows)

    current_price = float(prices_df["close"].iloc[-1])
    nearest_res = min((p for p in pivot_highs if p["price"] > current_price),
                      key=lambda x: x["price"], default=None)
    nearest_sup = max((p for p in pivot_lows if p["price"] < current_price),
                      key=lambda x: x["price"], default=None)

    return {
        "pivot_highs": pivot_highs[-5:],   # top 5 resistance levels
        "pivot_lows": pivot_lows[:5],      # top 5 support levels
        "nearest_resistance": nearest_res["price"] if nearest_res else None,
        "nearest_support": nearest_sup["price"] if nearest_sup else None,
    }


def compute_daily_indicators(prices_df: pd.DataFrame, timeframe: str = "daily") -> dict:
    """Compute comprehensive daily technical indicators for swing trading.

    Args:
        prices_df: DataFrame with columns: open, close, high, low, volume (DatetimeIndex)
        timeframe: bar timeframe ("daily" or "hourly"). Hourly uses scaled
            indicator periods (RSI 21, MACD 24/52/18, BB 48, etc.) so that
            signal depth on hourly bars matches what daily bars give.

    Returns dict with indicator categories and their values.
    """
    if prices_df.empty or len(prices_df) < 20:
        return {"error": "Insufficient data", "data_points": len(prices_df), "timeframe": timeframe}

    result: dict = {"timeframe": timeframe}
    degraded: list[dict] = []

    # Hourly timeframes need longer lookback windows to match daily signal depth
    if timeframe == "hourly":
        rsi_period = 21        # ~3 trading days on 1h bars
        macd_fast, macd_slow, macd_signal_period = 24, 52, 18  # doubled from daily
        bb_window = 48         # ~1 week of hourly bars
        atr_period = 24        # ~3 trading days
        ema_short = 24         # ~3 days
        ema_medium = 48        # ~1 week
        ema_long = 120         # ~3 weeks (replaces 50)
        z_window = 120         # ~3 weeks
        adx_period = 24
    else:  # daily
        rsi_period = 14
        macd_fast, macd_slow, macd_signal_period = 12, 26, 9
        bb_window = 20
        atr_period = 14
        ema_short = 10
        ema_medium = 21
        ema_long = 50
        z_window = 50
        adx_period = 14

    # --- Moving Averages ---
    result["moving_averages"] = {}
    ma_periods = [5, 10, 20, 21, 50, 200] if timeframe == "daily" else [ema_short, ema_medium, ema_long, 200]
    for period in ma_periods:
        if len(prices_df) >= period:
            ema = prices_df["close"].ewm(span=period, adjust=False).mean()
            sma = prices_df["close"].rolling(window=period).mean()
            result["moving_averages"][f"ema_{period}"] = float(ema.iloc[-1])
            result["moving_averages"][f"sma_{period}"] = float(sma.iloc[-1])

    # EMA alignment (short > medium > long = uptrend; reversed = downtrend)
    ma = result["moving_averages"]
    short_key = f"ema_{ema_short}"
    medium_key = f"ema_{ema_medium}"
    long_key = f"ema_{ema_long}"
    if short_key in ma and medium_key in ma and long_key in ma:
        ma["ema_aligned_uptrend"] = ma[short_key] > ma[medium_key] > ma[long_key]
        ma["ema_aligned_downtrend"] = ma[short_key] < ma[medium_key] < ma[long_key]
    else:
        ma["ema_aligned_uptrend"] = None
        ma["ema_aligned_downtrend"] = None

    current_price = float(prices_df["close"].iloc[-1])
    result["current_price"] = current_price

    # Distance from long-SMA (percent) — uses sma_50 on daily, sma_120 on hourly
    long_sma_key = f"sma_{ema_long}"
    if long_sma_key in ma and ma[long_sma_key]:
        result["dist_from_50sma_pct"] = round((current_price - ma[long_sma_key]) / ma[long_sma_key] * 100, 2)
    else:
        result["dist_from_50sma_pct"] = None

    # Price vs MAs
    result["price_vs_ma"] = {}
    for key, val in result["moving_averages"].items():
        if not isinstance(val, (int, float)) or val is None or not val:
            continue
        result["price_vs_ma"][f"above_{key}"] = current_price > val
        result["price_vs_ma"][f"pct_from_{key}"] = round((current_price - val) / val * 100, 2)

    # --- RSI ---
    result["rsi"] = {}
    rsi_periods = [7, 14, 21] if timeframe == "daily" else [rsi_period]
    for period in rsi_periods:
        if len(prices_df) >= period + 1:
            delta = prices_df["close"].diff()
            gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0.0)).rolling(window=period).mean()
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            result["rsi"][f"rsi_{period}"] = round(float(rsi.iloc[-1]), 2) if not pd.isna(rsi.iloc[-1]) else None

    # --- RSI divergence detection ---
    try:
        close = prices_df["close"]
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0).rolling(rsi_period).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(rsi_period).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi_series = 100 - (100 / (1 + rs))

        price_highs, price_lows = _find_swing_points(close, window=5)
        rsi_highs, rsi_lows = _find_swing_points(rsi_series, window=5)

        bearish_div = False
        bullish_div = False

        # Bearish: last 2 price highs go up, last 2 RSI highs go down
        if len(price_highs) >= 2 and len(rsi_highs) >= 2:
            ph1, ph2 = price_highs[-2], price_highs[-1]
            rh1, rh2 = rsi_highs[-2], rsi_highs[-1]
            if close.iloc[ph2] > close.iloc[ph1] and rsi_series.iloc[rh2] < rsi_series.iloc[rh1]:
                bearish_div = True

        # Bullish: last 2 price lows go down, last 2 RSI lows go up
        if len(price_lows) >= 2 and len(rsi_lows) >= 2:
            pl1, pl2 = price_lows[-2], price_lows[-1]
            rl1, rl2 = rsi_lows[-2], rsi_lows[-1]
            if close.iloc[pl2] < close.iloc[pl1] and rsi_series.iloc[rl2] > rsi_series.iloc[rl1]:
                bullish_div = True

        result["rsi_divergence"] = {
            "bullish": bullish_div,
            "bearish": bearish_div,
            "lookback_bars": min(len(close), 60),
        }
    except Exception as e:
        degraded.append({"indicator": "rsi_divergence", "error": str(e)[:100]})

    # --- MACD ---
    if len(prices_df) >= macd_slow:
        ema_fast = prices_df["close"].ewm(span=macd_fast, adjust=False).mean()
        ema_slow = prices_df["close"].ewm(span=macd_slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=macd_signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        result["macd"] = {
            "macd_line": round(float(macd_line.iloc[-1]), 4),
            "signal_line": round(float(signal_line.iloc[-1]), 4),
            "histogram": round(float(histogram.iloc[-1]), 4),
            "bullish_crossover": float(macd_line.iloc[-1]) > float(signal_line.iloc[-1]) and float(macd_line.iloc[-2]) <= float(signal_line.iloc[-2]) if len(macd_line) >= 2 else False,
        }

    # --- Bollinger Bands ---
    if len(prices_df) >= bb_window:
        sma_bb = prices_df["close"].rolling(bb_window).mean()
        std_bb = prices_df["close"].rolling(bb_window).std()
        upper = sma_bb + 2 * std_bb
        lower = sma_bb - 2 * std_bb
        bb_width = (upper - lower) / sma_bb
        result["bollinger"] = {
            "upper": round(float(upper.iloc[-1]), 2),
            "middle": round(float(sma_bb.iloc[-1]), 2),
            "lower": round(float(lower.iloc[-1]), 2),
            "width": round(float(bb_width.iloc[-1]), 4),
            "pct_b": round((current_price - float(lower.iloc[-1])) / (float(upper.iloc[-1]) - float(lower.iloc[-1])), 4) if float(upper.iloc[-1]) != float(lower.iloc[-1]) else 0.5,
        }

    # --- ATR (Average True Range) ---
    if len(prices_df) >= atr_period:
        high_low = prices_df["high"] - prices_df["low"]
        high_close = (prices_df["high"] - prices_df["close"].shift()).abs()
        low_close = (prices_df["low"] - prices_df["close"].shift()).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr_series = true_range.rolling(atr_period).mean()
        result["atr"] = {
            f"atr_{atr_period}": round(float(atr_series.iloc[-1]), 2),
            "atr_pct": round(float(atr_series.iloc[-1]) / current_price * 100, 2),
        }

    # --- ADX (Average Directional Index) ---
    if len(prices_df) >= adx_period * 2:
        try:
            plus_dm = prices_df["high"].diff()
            minus_dm = -prices_df["low"].diff()
            plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
            minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

            high_low = prices_df["high"] - prices_df["low"]
            high_close = (prices_df["high"] - prices_df["close"].shift()).abs()
            low_close = (prices_df["low"] - prices_df["close"].shift()).abs()
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

            atr_adx = tr.rolling(adx_period).mean()
            plus_di = 100 * (plus_dm.rolling(adx_period).mean() / atr_adx)
            minus_di = 100 * (minus_dm.rolling(adx_period).mean() / atr_adx)
            dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
            adx = dx.rolling(adx_period).mean()
            result["adx"] = {
                f"adx_{adx_period}": round(float(adx.iloc[-1]), 2) if not pd.isna(adx.iloc[-1]) else None,
                "plus_di": round(float(plus_di.iloc[-1]), 2) if not pd.isna(plus_di.iloc[-1]) else None,
                "minus_di": round(float(minus_di.iloc[-1]), 2) if not pd.isna(minus_di.iloc[-1]) else None,
                "trend_strength": "strong" if adx.iloc[-1] > 25 else "weak" if adx.iloc[-1] < 20 else "moderate",
            }
        except Exception as e:
            degraded.append({"indicator": "adx", "error": str(e)[:100]})

    # --- Volume Analysis ---
    if len(prices_df) >= 20:
        avg_vol_20 = prices_df["volume"].rolling(20).mean()
        result["volume"] = {
            "current_volume": int(prices_df["volume"].iloc[-1]),
            "avg_volume_20": int(avg_vol_20.iloc[-1]),
            "relative_volume": round(float(prices_df["volume"].iloc[-1] / avg_vol_20.iloc[-1]), 2) if avg_vol_20.iloc[-1] > 0 else 0,
            # Renamed from obv_trend: this is a 10-bar up-volume vs down-volume bias, NOT OBV.
            "volume_bias_10d": "up" if prices_df["volume"].where(prices_df["close"].diff() > 0, 0).rolling(10).sum().iloc[-1] > prices_df["volume"].where(prices_df["close"].diff() < 0, 0).rolling(10).sum().iloc[-1] else "down",
        }

        # Real On-Balance Volume: cumulative sum, +volume on up closes, -volume on down closes.
        price_direction = prices_df["close"].diff()
        obv_series = (prices_df["volume"] * price_direction.apply(
            lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
        )).cumsum()
        if len(obv_series) >= 10 and len(prices_df) >= 10:
            obv_slope = float(obv_series.iloc[-1] - obv_series.iloc[-10])
            price_slope = float(prices_df["close"].iloc[-1] - prices_df["close"].iloc[-10])
            result["volume"]["obv"] = {
                "trend": "up" if obv_slope > 0 else ("down" if obv_slope < 0 else "flat"),
                "diverging_from_price": (obv_slope > 0) != (price_slope > 0),
            }
        else:
            result["volume"]["obv"] = {"trend": "flat", "diverging_from_price": False}

    # --- Support/Resistance (pivot points with test counts and volume confirmation) ---
    try:
        result["support_resistance"] = _find_pivot_levels(prices_df) or {}
        recent = prices_df.tail(20)
        result["support_resistance"]["recent_high"] = round(float(recent["high"].max()), 2)
        result["support_resistance"]["recent_low"] = round(float(recent["low"].min()), 2)
        # Keep simple prev-day levels alongside (still useful for intraday reference)
        if len(prices_df) >= 2:
            result["support_resistance"]["prev_day_high"] = round(float(prices_df["high"].iloc[-2]), 2)
            result["support_resistance"]["prev_day_low"] = round(float(prices_df["low"].iloc[-2]), 2)
            result["support_resistance"]["prev_day_close"] = round(float(prices_df["close"].iloc[-2]), 2)
    except Exception as e:
        degraded.append({"indicator": "support_resistance", "error": str(e)[:100]})
        result["support_resistance"] = {}

    # --- Fibonacci Retracement + Extension (from recent swing high to low) ---
    if len(prices_df) >= 30:
        recent_30 = prices_df.tail(30)
        swing_high = float(recent_30["high"].max())
        swing_low = float(recent_30["low"].min())
        diff = swing_high - swing_low
        result["fibonacci"] = {
            "swing_high": round(swing_high, 2),
            "swing_low": round(swing_low, 2),
            # Retracements (pullback support, below the swing high)
            "fib_236": round(swing_high - 0.236 * diff, 2),
            "fib_382": round(swing_high - 0.382 * diff, 2),
            "fib_500": round(swing_high - 0.500 * diff, 2),
            "fib_618": round(swing_high - 0.618 * diff, 2),
            "fib_786": round(swing_high - 0.786 * diff, 2),
            # Bullish extensions above the swing high (price targets on breakout)
            "fib_ext_1272": round(swing_high + 0.272 * diff, 2),
            "fib_ext_1618": round(swing_high + 0.618 * diff, 2),
            "fib_ext_2000": round(swing_high + 1.000 * diff, 2),
            # Bearish extensions below the swing low (downside targets on breakdown)
            "fib_ext_low_1272": round(swing_low - 0.272 * diff, 2),
            "fib_ext_low_1618": round(swing_low - 0.618 * diff, 2),
        }

    # --- Momentum / Rate of Change ---
    result["momentum"] = {}
    for period in [5, 10, 21]:
        if len(prices_df) >= period + 1:
            roc = (prices_df["close"].iloc[-1] / prices_df["close"].iloc[-1 - period] - 1) * 100
            result["momentum"][f"roc_{period}d"] = round(float(roc), 2)

    # --- Z-Score ---
    if len(prices_df) >= z_window:
        mean_z = prices_df["close"].rolling(z_window).mean().iloc[-1]
        std_z = prices_df["close"].rolling(z_window).std().iloc[-1]
        if std_z > 0:
            result[f"z_score_{z_window}"] = round((current_price - mean_z) / std_z, 2)

    # --- pandas_ta extras (if available) ---
    if HAS_PANDAS_TA:
        # Stochastic
        try:
            stoch = ta.stoch(prices_df["high"], prices_df["low"], prices_df["close"])
            if stoch is not None and not stoch.empty:
                result["stochastic"] = {
                    "k": round(float(stoch.iloc[-1, 0]), 2),
                    "d": round(float(stoch.iloc[-1, 1]), 2),
                }
        except Exception as e:
            degraded.append({"indicator": "stochastic", "error": str(e)[:100]})

        # Williams %R
        try:
            willr = ta.willr(prices_df["high"], prices_df["low"], prices_df["close"])
            if willr is not None and not willr.empty:
                result["williams_r"] = round(float(willr.iloc[-1]), 2)
        except Exception as e:
            degraded.append({"indicator": "williams_r", "error": str(e)[:100]})

        # CCI (Commodity Channel Index)
        try:
            cci = ta.cci(prices_df["high"], prices_df["low"], prices_df["close"])
            if cci is not None and not cci.empty:
                result["cci"] = round(float(cci.iloc[-1]), 2)
        except Exception as e:
            degraded.append({"indicator": "cci", "error": str(e)[:100]})

        # MFI (Money Flow Index)
        try:
            mfi = ta.mfi(prices_df["high"], prices_df["low"], prices_df["close"], prices_df["volume"])
            if mfi is not None and not mfi.empty:
                result["mfi"] = round(float(mfi.iloc[-1]), 2)
        except Exception as e:
            degraded.append({"indicator": "mfi", "error": str(e)[:100]})

        # Schaff Trend Cycle
        try:
            stc_df = ta.stc(prices_df["close"], tclength=10, fast=23, slow=50, factor=0.5)
            if stc_df is not None and not stc_df.empty:
                result["stc"] = {
                    "value": round(float(stc_df.iloc[-1, 0]), 2),
                    "signal": "overbought" if float(stc_df.iloc[-1, 0]) > 75 else "oversold" if float(stc_df.iloc[-1, 0]) < 25 else "neutral",
                    "prev_value": round(float(stc_df.iloc[-2, 0]), 2) if len(stc_df) > 1 else None,
                    "crossed_above_25": float(stc_df.iloc[-1, 0]) > 25 and float(stc_df.iloc[-2, 0]) <= 25 if len(stc_df) > 1 else False,
                    "crossed_below_75": float(stc_df.iloc[-1, 0]) < 75 and float(stc_df.iloc[-2, 0]) >= 75 if len(stc_df) > 1 else False,
                }
        except Exception as e:
            degraded.append({"indicator": "stc", "error": str(e)[:100]})

        # Squeeze Momentum
        try:
            squeeze_df = ta.squeeze(prices_df["high"], prices_df["low"], prices_df["close"], lazybear=True)
            if squeeze_df is not None and not squeeze_df.empty:
                cols = squeeze_df.columns.tolist()
                sqz_on_col = [c for c in cols if 'SQZ' in c and 'ON' in c.upper()]
                sqz_off_col = [c for c in cols if 'SQZ' in c and 'OFF' in c.upper()]
                mom_col = [c for c in cols if 'LB' in c]

                mom_val = float(squeeze_df[mom_col[0]].iloc[-1]) if mom_col else 0.0
                prev_mom = float(squeeze_df[mom_col[0]].iloc[-2]) if mom_col and len(squeeze_df) > 1 else 0.0
                is_off = sqz_off_col and bool(squeeze_df[sqz_off_col[0]].iloc[-1])
                is_on = sqz_on_col and bool(squeeze_df[sqz_on_col[0]].iloc[-1])

                result["squeeze"] = {
                    "squeeze_on": bool(squeeze_df[sqz_on_col[0]].iloc[-1]) if sqz_on_col else None,
                    "squeeze_off": bool(squeeze_df[sqz_off_col[0]].iloc[-1]) if sqz_off_col else None,
                    "momentum": round(mom_val, 4),
                    "momentum_increasing": mom_val > prev_mom if len(squeeze_df) > 1 else None,
                    "signal": "bullish_breakout" if (is_off and mom_val > 0) else
                              "bearish_breakout" if (is_off and mom_val < 0) else
                              "squeeze_building" if is_on else "no_squeeze",
                }
        except Exception as e:
            degraded.append({"indicator": "squeeze", "error": str(e)[:100]})

        # SuperTrend
        try:
            st_df = ta.supertrend(prices_df["high"], prices_df["low"], prices_df["close"], length=10, multiplier=3.0)
            if st_df is not None and not st_df.empty:
                cols = st_df.columns.tolist()
                trend_col = [c for c in cols if 'SUPERTd' in c][0]
                value_col = [c for c in cols if 'SUPERT_' in c and 'SUPERTd' not in c][0]

                direction = int(st_df[trend_col].iloc[-1])
                supertrend_value = float(st_df[value_col].iloc[-1])
                prev_direction = int(st_df[trend_col].iloc[-2]) if len(st_df) > 1 else direction

                result["supertrend"] = {
                    "value": round(supertrend_value, 2),
                    "direction": "bullish" if direction == 1 else "bearish",
                    "trend_changed": direction != prev_direction,
                    "distance_pct": round((current_price - supertrend_value) / supertrend_value * 100, 2),
                }
        except Exception as e:
            degraded.append({"indicator": "supertrend", "error": str(e)[:100]})

    result["degraded_indicators"] = degraded
    return result


def compute_intraday_indicators(intraday_df: pd.DataFrame) -> dict:
    """Compute intraday-specific technical indicators for day trading.

    Args:
        intraday_df: DataFrame with columns: open, close, high, low, volume (DatetimeIndex with times)

    Returns dict with intraday indicator values.
    """
    if intraday_df.empty or len(intraday_df) < 10:
        return {"error": "Insufficient intraday data", "data_points": len(intraday_df)}

    result: dict = {}
    degraded: list[dict] = []
    current_price = float(intraday_df["close"].iloc[-1])
    result["current_price"] = current_price
    result["last_bar_time"] = str(intraday_df.index[-1])

    # --- VWAP (Volume Weighted Average Price) ---
    # VWAP resets each day, so compute for the most recent trading day
    try:
        intraday_df_copy = intraday_df.copy()
        intraday_df_copy["typical_price"] = (intraday_df_copy["high"] + intraday_df_copy["low"] + intraday_df_copy["close"]) / 3
        intraday_df_copy["tp_volume"] = intraday_df_copy["typical_price"] * intraday_df_copy["volume"]

        # Get today's data (or most recent day)
        dates = intraday_df_copy.index.date
        latest_date = dates[-1]
        today_mask = dates == latest_date
        today_data = intraday_df_copy[today_mask]

        if len(today_data) > 0 and today_data["volume"].sum() > 0:
            cumulative_tp_vol = today_data["tp_volume"].cumsum()
            cumulative_vol = today_data["volume"].cumsum()
            vwap = cumulative_tp_vol / cumulative_vol

            # VWAP bands (1 and 2 standard deviations)
            vwap_val = float(vwap.iloc[-1])
            sq_diff = ((today_data["typical_price"] - vwap) ** 2 * today_data["volume"]).cumsum() / cumulative_vol
            vwap_std = np.sqrt(sq_diff)

            result["vwap"] = {
                "vwap": round(vwap_val, 2),
                "upper_band_1": round(vwap_val + float(vwap_std.iloc[-1]), 2),
                "lower_band_1": round(vwap_val - float(vwap_std.iloc[-1]), 2),
                "upper_band_2": round(vwap_val + 2 * float(vwap_std.iloc[-1]), 2),
                "lower_band_2": round(vwap_val - 2 * float(vwap_std.iloc[-1]), 2),
                "price_vs_vwap": round((current_price - vwap_val) / vwap_val * 100, 2),
                "above_vwap": current_price > vwap_val,
            }
    except Exception as e:
        degraded.append({"indicator": "vwap", "error": str(e)[:100]})

    # --- Opening Range (first 30 min) ---
    try:
        dates = intraday_df.index.date
        latest_date = dates[-1]
        today_data = intraday_df[dates == latest_date]

        if len(today_data) >= 6:  # At least 30 min of 5-min bars
            first_30 = today_data.head(6)  # First 6 bars = 30 minutes
            or_high = float(first_30["high"].max())
            or_low = float(first_30["low"].min())
            result["opening_range"] = {
                "or_high": round(or_high, 2),
                "or_low": round(or_low, 2),
                "or_range": round(or_high - or_low, 2),
                "above_or_high": current_price > or_high,
                "below_or_low": current_price < or_low,
                "within_range": or_low <= current_price <= or_high,
            }
    except Exception as e:
        degraded.append({"indicator": "opening_range", "error": str(e)[:100]})

    # --- Gap Analysis ---
    try:
        dates = sorted(set(intraday_df.index.date))
        if len(dates) >= 2:
            prev_date = dates[-2]
            curr_date = dates[-1]
            prev_data = intraday_df[intraday_df.index.date == prev_date]
            curr_data = intraday_df[intraday_df.index.date == curr_date]

            if len(prev_data) > 0 and len(curr_data) > 0:
                prev_close = float(prev_data["close"].iloc[-1])
                curr_open = float(curr_data["open"].iloc[0])
                gap_pct = (curr_open - prev_close) / prev_close * 100

                result["gap"] = {
                    "previous_close": round(prev_close, 2),
                    "today_open": round(curr_open, 2),
                    "gap_pct": round(gap_pct, 2),
                    "gap_direction": "up" if gap_pct > 0.1 else "down" if gap_pct < -0.1 else "flat",
                    "gap_filled": (current_price <= prev_close) if gap_pct > 0 else (current_price >= prev_close) if gap_pct < 0 else True,
                }
    except Exception as e:
        degraded.append({"indicator": "gap", "error": str(e)[:100]})

    # --- Intraday EMAs ---
    result["ema"] = {}
    for period in [9, 20, 50]:
        if len(intraday_df) >= period:
            ema = intraday_df["close"].ewm(span=period, adjust=False).mean()
            result["ema"][f"ema_{period}"] = round(float(ema.iloc[-1]), 2)
            result["ema"][f"above_ema_{period}"] = current_price > float(ema.iloc[-1])

    # EMA crossover detection
    if "ema_9" in result["ema"] and "ema_20" in result["ema"]:
        ema9 = intraday_df["close"].ewm(span=9, adjust=False).mean()
        ema20 = intraday_df["close"].ewm(span=20, adjust=False).mean()
        if len(ema9) >= 2 and len(ema20) >= 2:
            result["ema"]["ema_9_20_crossover"] = (
                "bullish" if float(ema9.iloc[-1]) > float(ema20.iloc[-1]) and float(ema9.iloc[-2]) <= float(ema20.iloc[-2])
                else "bearish" if float(ema9.iloc[-1]) < float(ema20.iloc[-1]) and float(ema9.iloc[-2]) >= float(ema20.iloc[-2])
                else "none"
            )

    # --- Intraday RSI ---
    if len(intraday_df) >= 15:
        delta = intraday_df["close"].diff()
        gain = delta.where(delta > 0, 0.0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        result["rsi_14"] = round(float(rsi.iloc[-1]), 2) if not pd.isna(rsi.iloc[-1]) else None

    # --- Intraday MACD ---
    if len(intraday_df) >= 26:
        ema12 = intraday_df["close"].ewm(span=12, adjust=False).mean()
        ema26 = intraday_df["close"].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        result["macd"] = {
            "macd_line": round(float(macd.iloc[-1]), 4),
            "signal_line": round(float(signal.iloc[-1]), 4),
            "histogram": round(float((macd - signal).iloc[-1]), 4),
        }

    # --- Intraday Volume Profile ---
    try:
        dates = intraday_df.index.date
        latest_date = dates[-1]
        today_data = intraday_df[dates == latest_date]

        if len(today_data) > 0:
            avg_bar_vol = today_data["volume"].mean()
            result["volume_profile"] = {
                "total_volume_today": int(today_data["volume"].sum()),
                "avg_bar_volume": int(avg_bar_vol),
                "current_bar_volume": int(intraday_df["volume"].iloc[-1]),
                "relative_bar_volume": round(float(intraday_df["volume"].iloc[-1] / avg_bar_vol), 2) if avg_bar_vol > 0 else 0,
                "volume_trend": "increasing" if today_data["volume"].tail(5).mean() > avg_bar_vol else "decreasing",
            }
    except Exception as e:
        degraded.append({"indicator": "volume_profile", "error": str(e)[:100]})

    # --- Bollinger Bands (intraday) ---
    if len(intraday_df) >= 20:
        sma20 = intraday_df["close"].rolling(20).mean()
        std20 = intraday_df["close"].rolling(20).std()
        upper = sma20 + 2 * std20
        lower = sma20 - 2 * std20
        result["bollinger"] = {
            "upper": round(float(upper.iloc[-1]), 2),
            "middle": round(float(sma20.iloc[-1]), 2),
            "lower": round(float(lower.iloc[-1]), 2),
            "pct_b": round((current_price - float(lower.iloc[-1])) / (float(upper.iloc[-1]) - float(lower.iloc[-1])), 4) if float(upper.iloc[-1]) != float(lower.iloc[-1]) else 0.5,
        }

    # --- Previous Day Levels ---
    try:
        dates = sorted(set(intraday_df.index.date))
        if len(dates) >= 2:
            prev_date = dates[-2]
            prev_data = intraday_df[intraday_df.index.date == prev_date]
            if len(prev_data) > 0:
                result["prev_day"] = {
                    "high": round(float(prev_data["high"].max()), 2),
                    "low": round(float(prev_data["low"].min()), 2),
                    "close": round(float(prev_data["close"].iloc[-1]), 2),
                    "above_prev_high": current_price > float(prev_data["high"].max()),
                    "below_prev_low": current_price < float(prev_data["low"].min()),
                }
    except Exception as e:
        degraded.append({"indicator": "prev_day", "error": str(e)[:100]})

    # --- pandas_ta extras (if available) ---
    if HAS_PANDAS_TA:
        close = intraday_df["close"]
        high = intraday_df["high"]
        low = intraday_df["low"]

        # Schaff Trend Cycle
        try:
            stc_df = ta.stc(close, tclength=10, fast=23, slow=50, factor=0.5)
            if stc_df is not None and not stc_df.empty:
                result["stc"] = {
                    "value": round(float(stc_df.iloc[-1, 0]), 2),
                    "signal": "overbought" if float(stc_df.iloc[-1, 0]) > 75 else "oversold" if float(stc_df.iloc[-1, 0]) < 25 else "neutral",
                    "prev_value": round(float(stc_df.iloc[-2, 0]), 2) if len(stc_df) > 1 else None,
                    "crossed_above_25": float(stc_df.iloc[-1, 0]) > 25 and float(stc_df.iloc[-2, 0]) <= 25 if len(stc_df) > 1 else False,
                    "crossed_below_75": float(stc_df.iloc[-1, 0]) < 75 and float(stc_df.iloc[-2, 0]) >= 75 if len(stc_df) > 1 else False,
                }
        except Exception as e:
            degraded.append({"indicator": "stc", "error": str(e)[:100]})

        # Squeeze Momentum
        try:
            squeeze_df = ta.squeeze(high, low, close, lazybear=True)
            if squeeze_df is not None and not squeeze_df.empty:
                cols = squeeze_df.columns.tolist()
                sqz_on_col = [c for c in cols if 'SQZ' in c and 'ON' in c.upper()]
                sqz_off_col = [c for c in cols if 'SQZ' in c and 'OFF' in c.upper()]
                mom_col = [c for c in cols if 'LB' in c]

                mom_val = float(squeeze_df[mom_col[0]].iloc[-1]) if mom_col else 0.0
                prev_mom = float(squeeze_df[mom_col[0]].iloc[-2]) if mom_col and len(squeeze_df) > 1 else 0.0
                is_off = sqz_off_col and bool(squeeze_df[sqz_off_col[0]].iloc[-1])
                is_on = sqz_on_col and bool(squeeze_df[sqz_on_col[0]].iloc[-1])

                result["squeeze"] = {
                    "squeeze_on": bool(squeeze_df[sqz_on_col[0]].iloc[-1]) if sqz_on_col else None,
                    "squeeze_off": bool(squeeze_df[sqz_off_col[0]].iloc[-1]) if sqz_off_col else None,
                    "momentum": round(mom_val, 4),
                    "momentum_increasing": mom_val > prev_mom if len(squeeze_df) > 1 else None,
                    "signal": "bullish_breakout" if (is_off and mom_val > 0) else
                              "bearish_breakout" if (is_off and mom_val < 0) else
                              "squeeze_building" if is_on else "no_squeeze",
                }
        except Exception as e:
            degraded.append({"indicator": "squeeze", "error": str(e)[:100]})

        # SuperTrend
        try:
            st_df = ta.supertrend(high, low, close, length=10, multiplier=3.0)
            if st_df is not None and not st_df.empty:
                cols = st_df.columns.tolist()
                trend_col = [c for c in cols if 'SUPERTd' in c][0]
                value_col = [c for c in cols if 'SUPERT_' in c and 'SUPERTd' not in c][0]

                direction = int(st_df[trend_col].iloc[-1])
                supertrend_value = float(st_df[value_col].iloc[-1])
                prev_direction = int(st_df[trend_col].iloc[-2]) if len(st_df) > 1 else direction

                result["supertrend"] = {
                    "value": round(supertrend_value, 2),
                    "direction": "bullish" if direction == 1 else "bearish",
                    "trend_changed": direction != prev_direction,
                    "distance_pct": round((current_price - supertrend_value) / supertrend_value * 100, 2),
                }
        except Exception as e:
            degraded.append({"indicator": "supertrend", "error": str(e)[:100]})

    result["degraded_indicators"] = degraded
    return result
