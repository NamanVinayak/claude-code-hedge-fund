"""Earnings calendar helper.

Public API: ``days_until_next_earnings(ticker) -> int | None``.

Powered by yfinance's ``Ticker.calendar`` field. Crypto tickers and unknown
symbols cleanly return ``None`` so callers can treat "no earnings" as a
non-event. Results are cached for 24 h via ``ai_hedge.data.cache`` because
earnings dates rarely move and yfinance's quoteSummary endpoint is rate-limited.
"""

from __future__ import annotations

import logging
from datetime import date, datetime

from ai_hedge.data.cache import get_cache

logger = logging.getLogger(__name__)
_cache = get_cache()

# Tickers ending in one of these quote-currency suffixes are treated as crypto
# pairs (yfinance uses "BTC-USD", "ETH-USD", etc.). Crypto has no earnings.
_CRYPTO_QUOTE_SUFFIXES = ("-USD", "-USDT", "-USDC", "-BTC", "-ETH")


def _is_crypto(ticker: str) -> bool:
    t = ticker.upper()
    return any(t.endswith(suf) for suf in _CRYPTO_QUOTE_SUFFIXES)


def days_until_next_earnings(ticker: str) -> int | None:
    """Return number of calendar days until the next scheduled earnings.

    Returns ``None`` if no earnings date is found, the ticker is a crypto pair,
    or yfinance lookup fails. A return value of ``0`` means earnings are today;
    negative values are filtered out (only future or same-day dates qualify).
    """
    if _is_crypto(ticker):
        return None

    cached, found = _cache.get_earnings(ticker)
    if found:
        return cached

    result = _fetch_earnings_days(ticker)
    _cache.set_earnings(ticker, result)
    return result


def _fetch_earnings_days(ticker: str) -> int | None:
    try:
        import yfinance as yf

        cal = yf.Ticker(ticker).calendar
    except Exception as exc:
        logger.debug("earnings calendar fetch failed for %s: %s", ticker, exc)
        return None

    if not isinstance(cal, dict):
        return None

    raw = cal.get("Earnings Date")
    if not raw:
        return None

    candidates = raw if isinstance(raw, (list, tuple)) else [raw]
    today = date.today()
    future: list[date] = []
    for d in candidates:
        if isinstance(d, datetime):
            d = d.date()
        if isinstance(d, date) and d >= today:
            future.append(d)

    if not future:
        return None

    next_date = min(future)
    return (next_date - today).days
