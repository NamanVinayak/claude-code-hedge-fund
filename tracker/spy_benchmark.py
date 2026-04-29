"""Compute a passive SPY (S&P 500 ETF) benchmark over an audit window.

Used by both `tracker/backtest.py` and `scripts/swing_audit.py` to answer
"if you'd put the same capital into SPY and slept, how would you have done?"
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

import yfinance as yf


def compute_spy_benchmark(
    start_date: str,
    end_date: str,
    capital: float,
) -> dict:
    """Buy-and-hold SPY over [start_date, end_date], deploying `capital` USD.

    `start_date` / `end_date` are ISO-format dates (YYYY-MM-DD) in UTC.
    Returns ``{spy_pct, spy_dollar, spy_start, spy_end, available}``.
    `available` is False when SPY data couldn't be fetched (weekend-only window,
    bad date, network failure) — callers should suppress the headline gracefully.
    """

    out = {
        "spy_pct": 0.0,
        "spy_dollar": 0.0,
        "spy_start": None,
        "spy_end": None,
        "available": False,
    }

    if capital <= 0:
        return out

    try:
        # Pad end_date by 1 day so today's bars are included.
        end_dt = datetime.fromisoformat(end_date).date()
        fetch_end = end_dt.isoformat()
        df = yf.Ticker("SPY").history(
            start=start_date,
            end=fetch_end,
            interval="1h",
            auto_adjust=True,
        )
    except Exception:
        return out

    if df is None or df.empty:
        return out

    try:
        spy_start = float(df["Open"].iloc[0])
        spy_end = float(df["Close"].iloc[-1])
    except (KeyError, IndexError, ValueError):
        return out

    # Try to upgrade end-of-window to live last price for an honest "vs SPY today".
    try:
        live = yf.Ticker("SPY").fast_info.last_price
        if live and live == live:  # not None, not NaN
            spy_end = float(live)
    except Exception:
        pass

    if spy_start <= 0:
        return out

    pct = (spy_end - spy_start) / spy_start * 100.0
    out.update({
        "spy_pct": pct,
        "spy_dollar": capital * pct / 100.0,
        "spy_start": spy_start,
        "spy_end": spy_end,
        "available": True,
    })
    return out


def _money(v: float) -> str:
    if v >= 0:
        return f"+${v:,.2f}"
    return f"-${abs(v):,.2f}"


def _pct(v: float) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"


def format_headline(
    you_dollar: float,
    you_pct: float,
    spy: dict,
    *,
    caveat: Optional[str] = None,
) -> str:
    """Return a one-line "you vs SPY" headline. Empty string if SPY unavailable."""

    if not spy.get("available"):
        return ""

    spy_dollar = spy["spy_dollar"]
    spy_pct = spy["spy_pct"]
    delta_dollar = you_dollar - spy_dollar
    delta_pts = you_pct - spy_pct
    trail_or_lead = "lead" if delta_dollar >= 0 else "trail"

    line = (
        f"**Performance vs SPY**: {_money(you_dollar)} / {_pct(you_pct)} (you) — "
        f"SPY: {_money(spy_dollar)} / {_pct(spy_pct)} — "
        f"you {trail_or_lead} SPY by ${abs(delta_dollar):,.2f} ({_pct(delta_pts)[:-1]} pts)"
    )
    if caveat:
        line = f"{line}\n\n_{caveat}_"
    return line


if __name__ == "__main__":
    # Quick sanity check
    from datetime import timedelta

    today = date.today()
    two_weeks_ago = (today - timedelta(days=14)).isoformat()
    bench = compute_spy_benchmark(two_weeks_ago, today.isoformat(), 5000.0)
    print(bench)
    print(format_headline(125.50, 0.42, bench))
