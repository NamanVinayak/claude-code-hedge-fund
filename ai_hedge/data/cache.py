"""In-memory cache with per-entry TTL.

Each cache entry stores (data, fetched_at). On lookup, entries older than the
configured TTL return None so the caller re-fetches from the provider.

Defaults err on the side of fresh:
  - prices       300 s (5 min) — yfinance is already 15-min delayed for stocks
  - fundamentals 86400 s (24 h) — quarterly; rarely changes intraday
  - line items   86400 s (24 h)
  - insider      14400 s (4 h) — Form 4 filings come in waves
  - news         300 s (5 min) — moves fast
  - earnings     86400 s (24 h) — earnings dates rarely move
"""

import time
from typing import Any


class Cache:
    """In-memory cache for API responses with per-entry TTL."""

    def __init__(
        self,
        *,
        prices_ttl: float = 300,
        fundamentals_ttl: float = 86400,
        line_items_ttl: float = 86400,
        insider_ttl: float = 14400,
        news_ttl: float = 300,
        earnings_ttl: float = 86400,
    ) -> None:
        self.prices_ttl = prices_ttl
        self.fundamentals_ttl = fundamentals_ttl
        self.line_items_ttl = line_items_ttl
        self.insider_ttl = insider_ttl
        self.news_ttl = news_ttl
        self.earnings_ttl = earnings_ttl

        # Each cache stores key -> (data, fetched_at_unix)
        self._prices_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        self._financial_metrics_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        self._line_items_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        self._insider_trades_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        self._company_news_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        # Scalar cache: stores a single value (int days, or None for "no scheduled earnings").
        # We must distinguish "missing key" from "cached None", so callers use the (value, found)
        # tuple returned by get_earnings.
        self._earnings_cache: dict[str, tuple[Any, float]] = {}

    @staticmethod
    def _merge_data(existing: list[dict] | None, new_data: list[dict], key_field: str) -> list[dict]:
        """Merge existing and new data, deduping on key_field."""
        if not existing:
            return new_data
        existing_keys = {item[key_field] for item in existing}
        merged = existing.copy()
        merged.extend(item for item in new_data if item[key_field] not in existing_keys)
        return merged

    def _get_fresh(
        self,
        store: dict[str, tuple[list[dict[str, Any]], float]],
        key: str,
        ttl: float,
    ) -> list[dict[str, Any]] | None:
        entry = store.get(key)
        if entry is None:
            return None
        data, fetched_at = entry
        if (time.time() - fetched_at) > ttl:
            return None  # stale; caller re-fetches
        return data

    def _set(
        self,
        store: dict[str, tuple[list[dict[str, Any]], float]],
        key: str,
        data: list[dict[str, Any]],
        key_field: str,
        ttl: float,
    ) -> None:
        existing_entry = store.get(key)
        # If existing is fresh, merge; if stale or missing, replace.
        if existing_entry and (time.time() - existing_entry[1]) <= ttl:
            merged = self._merge_data(existing_entry[0], data, key_field)
        else:
            merged = data
        store[key] = (merged, time.time())

    # ── Prices ──────────────────────────────────────────────────────────────
    def get_prices(self, ticker: str) -> list[dict[str, Any]] | None:
        return self._get_fresh(self._prices_cache, ticker, self.prices_ttl)

    def set_prices(self, ticker: str, data: list[dict[str, Any]]) -> None:
        self._set(self._prices_cache, ticker, data, key_field="time", ttl=self.prices_ttl)

    # ── Financial metrics ───────────────────────────────────────────────────
    def get_financial_metrics(self, ticker: str) -> list[dict[str, Any]] | None:
        return self._get_fresh(self._financial_metrics_cache, ticker, self.fundamentals_ttl)

    def set_financial_metrics(self, ticker: str, data: list[dict[str, Any]]) -> None:
        self._set(self._financial_metrics_cache, ticker, data,
                  key_field="report_period", ttl=self.fundamentals_ttl)

    # ── Line items ──────────────────────────────────────────────────────────
    def get_line_items(self, ticker: str) -> list[dict[str, Any]] | None:
        return self._get_fresh(self._line_items_cache, ticker, self.line_items_ttl)

    def set_line_items(self, ticker: str, data: list[dict[str, Any]]) -> None:
        self._set(self._line_items_cache, ticker, data,
                  key_field="report_period", ttl=self.line_items_ttl)

    # ── Insider trades ──────────────────────────────────────────────────────
    def get_insider_trades(self, ticker: str) -> list[dict[str, Any]] | None:
        return self._get_fresh(self._insider_trades_cache, ticker, self.insider_ttl)

    def set_insider_trades(self, ticker: str, data: list[dict[str, Any]]) -> None:
        self._set(self._insider_trades_cache, ticker, data,
                  key_field="filing_date", ttl=self.insider_ttl)

    # ── Company news ────────────────────────────────────────────────────────
    def get_company_news(self, ticker: str) -> list[dict[str, Any]] | None:
        return self._get_fresh(self._company_news_cache, ticker, self.news_ttl)

    def set_company_news(self, ticker: str, data: list[dict[str, Any]]) -> None:
        self._set(self._company_news_cache, ticker, data,
                  key_field="date", ttl=self.news_ttl)

    # ── Earnings (scalar) ───────────────────────────────────────────────────
    def get_earnings(self, ticker: str) -> tuple[Any, bool]:
        """Return (value, found). value can legitimately be None when found=True
        (meaning we already looked it up and the provider had no scheduled date)."""
        entry = self._earnings_cache.get(ticker)
        if entry is None:
            return None, False
        value, fetched_at = entry
        if (time.time() - fetched_at) > self.earnings_ttl:
            return None, False
        return value, True

    def set_earnings(self, ticker: str, value: Any) -> None:
        self._earnings_cache[ticker] = (value, time.time())


_cache = Cache()


def get_cache() -> Cache:
    return _cache
