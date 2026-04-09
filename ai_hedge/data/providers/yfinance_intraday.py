"""yfinance-based intraday data provider for day trading analysis."""

import yfinance as yf


def get_intraday_prices_yf(ticker: str, interval: str = "5m", period: str = "5d") -> list[dict]:
    """Returns list of intraday OHLCV dicts.

    Args:
        ticker: Stock symbol
        interval: Bar size - "1m" (7 days max), "5m" (60 days), "15m" (60 days), "30m" (60 days)
        period: Lookback period - "1d", "5d", "1mo", "2mo" etc.

    Returns list of dicts with keys: open, close, high, low, volume, time (ISO datetime string)
    """
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval)
        if df is None or df.empty:
            return []
        results = []
        for idx, row in df.iterrows():
            results.append({
                "open": float(row["Open"]),
                "close": float(row["Close"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "volume": int(row["Volume"]),
                "time": idx.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return results
    except Exception:
        return []


def get_premarket_data_yf(ticker: str) -> dict | None:
    """Returns pre-market price info if available."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        pre_price = info.get("preMarketPrice")
        pre_change = info.get("preMarketChangePercent")
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        return {
            "pre_market_price": float(pre_price) if pre_price else None,
            "pre_market_change_pct": float(pre_change) if pre_change else None,
            "previous_close": float(prev_close) if prev_close else None,
        }
    except Exception:
        return None
