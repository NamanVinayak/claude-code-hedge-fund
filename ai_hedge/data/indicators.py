"""Advanced technical indicators via pandas_ta for swing and day trade modes."""

import pandas as pd
import numpy as np

try:
    import pandas_ta as ta
    HAS_PANDAS_TA = True
except ImportError:
    HAS_PANDAS_TA = False


def compute_daily_indicators(prices_df: pd.DataFrame) -> dict:
    """Compute comprehensive daily technical indicators for swing trading.

    Args:
        prices_df: DataFrame with columns: open, close, high, low, volume (DatetimeIndex)

    Returns dict with indicator categories and their values.
    """
    if prices_df.empty or len(prices_df) < 20:
        return {"error": "Insufficient data", "data_points": len(prices_df)}

    result = {}

    # --- Moving Averages ---
    result["moving_averages"] = {}
    for period in [5, 10, 20, 50, 200]:
        if len(prices_df) >= period:
            ema = prices_df["close"].ewm(span=period, adjust=False).mean()
            sma = prices_df["close"].rolling(window=period).mean()
            result["moving_averages"][f"ema_{period}"] = float(ema.iloc[-1])
            result["moving_averages"][f"sma_{period}"] = float(sma.iloc[-1])

    current_price = float(prices_df["close"].iloc[-1])
    result["current_price"] = current_price

    # Price vs MAs
    result["price_vs_ma"] = {}
    for key, val in result["moving_averages"].items():
        result["price_vs_ma"][f"above_{key}"] = current_price > val
        result["price_vs_ma"][f"pct_from_{key}"] = round((current_price - val) / val * 100, 2)

    # --- RSI ---
    result["rsi"] = {}
    for period in [7, 14, 21]:
        if len(prices_df) >= period + 1:
            delta = prices_df["close"].diff()
            gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0.0)).rolling(window=period).mean()
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            result["rsi"][f"rsi_{period}"] = round(float(rsi.iloc[-1]), 2) if not pd.isna(rsi.iloc[-1]) else None

    # --- MACD ---
    if len(prices_df) >= 26:
        ema12 = prices_df["close"].ewm(span=12, adjust=False).mean()
        ema26 = prices_df["close"].ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        result["macd"] = {
            "macd_line": round(float(macd_line.iloc[-1]), 4),
            "signal_line": round(float(signal_line.iloc[-1]), 4),
            "histogram": round(float(histogram.iloc[-1]), 4),
            "bullish_crossover": float(macd_line.iloc[-1]) > float(signal_line.iloc[-1]) and float(macd_line.iloc[-2]) <= float(signal_line.iloc[-2]) if len(macd_line) >= 2 else False,
        }

    # --- Bollinger Bands ---
    if len(prices_df) >= 20:
        sma20 = prices_df["close"].rolling(20).mean()
        std20 = prices_df["close"].rolling(20).std()
        upper = sma20 + 2 * std20
        lower = sma20 - 2 * std20
        bb_width = (upper - lower) / sma20
        result["bollinger"] = {
            "upper": round(float(upper.iloc[-1]), 2),
            "middle": round(float(sma20.iloc[-1]), 2),
            "lower": round(float(lower.iloc[-1]), 2),
            "width": round(float(bb_width.iloc[-1]), 4),
            "pct_b": round((current_price - float(lower.iloc[-1])) / (float(upper.iloc[-1]) - float(lower.iloc[-1])), 4) if float(upper.iloc[-1]) != float(lower.iloc[-1]) else 0.5,
        }

    # --- ATR (Average True Range) ---
    if len(prices_df) >= 14:
        high_low = prices_df["high"] - prices_df["low"]
        high_close = (prices_df["high"] - prices_df["close"].shift()).abs()
        low_close = (prices_df["low"] - prices_df["close"].shift()).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr14 = true_range.rolling(14).mean()
        result["atr"] = {
            "atr_14": round(float(atr14.iloc[-1]), 2),
            "atr_pct": round(float(atr14.iloc[-1]) / current_price * 100, 2),
        }

    # --- ADX (Average Directional Index) ---
    if len(prices_df) >= 28:
        try:
            plus_dm = prices_df["high"].diff()
            minus_dm = -prices_df["low"].diff()
            plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
            minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

            high_low = prices_df["high"] - prices_df["low"]
            high_close = (prices_df["high"] - prices_df["close"].shift()).abs()
            low_close = (prices_df["low"] - prices_df["close"].shift()).abs()
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

            atr14 = tr.rolling(14).mean()
            plus_di = 100 * (plus_dm.rolling(14).mean() / atr14)
            minus_di = 100 * (minus_dm.rolling(14).mean() / atr14)
            dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
            adx = dx.rolling(14).mean()
            result["adx"] = {
                "adx_14": round(float(adx.iloc[-1]), 2) if not pd.isna(adx.iloc[-1]) else None,
                "plus_di": round(float(plus_di.iloc[-1]), 2) if not pd.isna(plus_di.iloc[-1]) else None,
                "minus_di": round(float(minus_di.iloc[-1]), 2) if not pd.isna(minus_di.iloc[-1]) else None,
                "trend_strength": "strong" if adx.iloc[-1] > 25 else "weak" if adx.iloc[-1] < 20 else "moderate",
            }
        except Exception:
            pass

    # --- Volume Analysis ---
    if len(prices_df) >= 20:
        avg_vol_20 = prices_df["volume"].rolling(20).mean()
        result["volume"] = {
            "current_volume": int(prices_df["volume"].iloc[-1]),
            "avg_volume_20": int(avg_vol_20.iloc[-1]),
            "relative_volume": round(float(prices_df["volume"].iloc[-1] / avg_vol_20.iloc[-1]), 2) if avg_vol_20.iloc[-1] > 0 else 0,
            "obv_trend": "up" if prices_df["volume"].where(prices_df["close"].diff() > 0, 0).rolling(10).sum().iloc[-1] > prices_df["volume"].where(prices_df["close"].diff() < 0, 0).rolling(10).sum().iloc[-1] else "down",
        }

    # --- Support/Resistance (recent pivots) ---
    if len(prices_df) >= 20:
        recent = prices_df.tail(20)
        result["support_resistance"] = {
            "recent_high": round(float(recent["high"].max()), 2),
            "recent_low": round(float(recent["low"].min()), 2),
            "prev_day_high": round(float(prices_df["high"].iloc[-2]), 2) if len(prices_df) >= 2 else None,
            "prev_day_low": round(float(prices_df["low"].iloc[-2]), 2) if len(prices_df) >= 2 else None,
            "prev_day_close": round(float(prices_df["close"].iloc[-2]), 2) if len(prices_df) >= 2 else None,
        }

    # --- Fibonacci Retracement (from recent swing high to low) ---
    if len(prices_df) >= 30:
        recent_30 = prices_df.tail(30)
        swing_high = float(recent_30["high"].max())
        swing_low = float(recent_30["low"].min())
        diff = swing_high - swing_low
        result["fibonacci"] = {
            "swing_high": round(swing_high, 2),
            "swing_low": round(swing_low, 2),
            "fib_236": round(swing_high - 0.236 * diff, 2),
            "fib_382": round(swing_high - 0.382 * diff, 2),
            "fib_500": round(swing_high - 0.500 * diff, 2),
            "fib_618": round(swing_high - 0.618 * diff, 2),
        }

    # --- Momentum / Rate of Change ---
    result["momentum"] = {}
    for period in [5, 10, 21]:
        if len(prices_df) >= period + 1:
            roc = (prices_df["close"].iloc[-1] / prices_df["close"].iloc[-1 - period] - 1) * 100
            result["momentum"][f"roc_{period}d"] = round(float(roc), 2)

    # --- Z-Score ---
    if len(prices_df) >= 50:
        mean_50 = prices_df["close"].rolling(50).mean().iloc[-1]
        std_50 = prices_df["close"].rolling(50).std().iloc[-1]
        if std_50 > 0:
            result["z_score_50"] = round((current_price - mean_50) / std_50, 2)

    # --- pandas_ta extras (if available) ---
    if HAS_PANDAS_TA:
        try:
            # Stochastic
            stoch = ta.stoch(prices_df["high"], prices_df["low"], prices_df["close"])
            if stoch is not None and not stoch.empty:
                result["stochastic"] = {
                    "k": round(float(stoch.iloc[-1, 0]), 2),
                    "d": round(float(stoch.iloc[-1, 1]), 2),
                }

            # Williams %R
            willr = ta.willr(prices_df["high"], prices_df["low"], prices_df["close"])
            if willr is not None and not willr.empty:
                result["williams_r"] = round(float(willr.iloc[-1]), 2)

            # CCI (Commodity Channel Index)
            cci = ta.cci(prices_df["high"], prices_df["low"], prices_df["close"])
            if cci is not None and not cci.empty:
                result["cci"] = round(float(cci.iloc[-1]), 2)

            # MFI (Money Flow Index)
            mfi = ta.mfi(prices_df["high"], prices_df["low"], prices_df["close"], prices_df["volume"])
            if mfi is not None and not mfi.empty:
                result["mfi"] = round(float(mfi.iloc[-1]), 2)

        except Exception:
            pass

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
        except Exception:
            pass

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
        except Exception:
            pass

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
        except Exception:
            pass

    return result


def compute_intraday_indicators(intraday_df: pd.DataFrame) -> dict:
    """Compute intraday-specific technical indicators for day trading.

    Args:
        intraday_df: DataFrame with columns: open, close, high, low, volume (DatetimeIndex with times)

    Returns dict with intraday indicator values.
    """
    if intraday_df.empty or len(intraday_df) < 10:
        return {"error": "Insufficient intraday data", "data_points": len(intraday_df)}

    result = {}
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
    except Exception:
        pass

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
    except Exception:
        pass

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
    except Exception:
        pass

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
    except Exception:
        pass

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
    except Exception:
        pass

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
        except Exception:
            pass

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
        except Exception:
            pass

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
        except Exception:
            pass

    return result
