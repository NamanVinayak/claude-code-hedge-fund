"""yfinance-based data provider for prices, market cap, and financial statements."""

import yfinance as yf


def get_prices_yf(ticker: str, start_date: str, end_date: str) -> list[dict]:
    """Returns list of dicts with keys: open, close, high, low, volume, time (YYYY-MM-DD string)."""
    try:
        t = yf.Ticker(ticker)
        df = t.history(start=start_date, end=end_date, auto_adjust=True)
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
                "time": idx.strftime("%Y-%m-%d"),
            })
        return results
    except Exception:
        return []


def get_market_cap_yf(ticker: str) -> float | None:
    """Returns current market cap from yfinance info."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        mc = info.get("marketCap")
        if mc is not None:
            return float(mc)
        return None
    except Exception:
        return None


def _stmt_to_dict(df) -> dict:
    """Convert a yfinance statement DataFrame to dict mapping field_name -> list of (period_str, value) tuples."""
    if df is None or df.empty:
        return {}
    result = {}
    for field in df.index:
        entries = []
        for col in df.columns:
            val = df.loc[field, col]
            try:
                import pandas as pd
                if pd.isna(val):
                    continue
                period_str = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)[:10]
                entries.append((period_str, float(val)))
            except Exception:
                continue
        if entries:
            result[str(field)] = entries
    return result


def get_income_stmt_yf(ticker: str) -> dict:
    """Returns dict mapping field_name -> list of (period_str, value) tuples, annual statements."""
    try:
        t = yf.Ticker(ticker)
        df = t.income_stmt  # annual
        return _stmt_to_dict(df)
    except Exception:
        return {}


def get_balance_sheet_yf(ticker: str) -> dict:
    """Returns dict mapping field_name -> list of (period_str, value) tuples, annual statements."""
    try:
        t = yf.Ticker(ticker)
        df = t.balance_sheet  # annual
        return _stmt_to_dict(df)
    except Exception:
        return {}


def get_cash_flow_yf(ticker: str) -> dict:
    """Returns dict mapping field_name -> list of (period_str, value) tuples, annual statements."""
    try:
        t = yf.Ticker(ticker)
        df = t.cash_flow  # annual
        return _stmt_to_dict(df)
    except Exception:
        return {}
