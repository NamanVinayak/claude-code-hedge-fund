"""
Public data access layer — free-source replacement for upstream src/tools/api.py.
Provides identical function signatures; api_key params are accepted but ignored.
"""

import logging
from datetime import datetime, timedelta

import pandas as pd

from ai_hedge.data.cache import get_cache
from ai_hedge.data.models import (
    CompanyNews,
    FinancialMetrics,
    InsiderTrade,
    LineItem,
    Price,
)
from ai_hedge.data.providers.yfinance_provider import (
    get_prices_yf,
    get_market_cap_yf,
    get_current_price_yf,
)
from ai_hedge.data.providers.sec_edgar_provider import (
    get_cik,
    get_company_facts,
    get_line_item_history,
    compute_ttm,
    compute_ttm_with_source,
    get_latest_annual,
    get_latest_annual_with_date,
    get_annual_series,
    GAAP_CONCEPTS,
)
from ai_hedge.data.providers.finnhub_provider import (
    get_insider_trades_fh,
    get_company_news_fh,
)

logger = logging.getLogger(__name__)

_cache = get_cache()


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------

def get_prices(ticker: str, start_date: str, end_date: str, api_key: str = None) -> list[Price]:
    """Fetch daily price data for ticker between start_date and end_date (inclusive)."""
    cache_key = f"{ticker}_{start_date}_{end_date}"
    if cached := _cache.get_prices(cache_key):
        return [Price(**p) for p in cached]

    raw = get_prices_yf(ticker, start_date, end_date)
    if not raw:
        return []

    _cache.set_prices(cache_key, raw)
    return [Price(**p) for p in raw]


def prices_to_df(prices: list[Price]) -> pd.DataFrame:
    """Convert list of Price objects to DataFrame indexed by date."""
    df = pd.DataFrame([p.model_dump() for p in prices])
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    if "time" in df.columns:
        df.drop(columns=["time"], inplace=True)
    for col in ["open", "close", "high", "low", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df


def get_price_data(ticker: str, start_date: str, end_date: str, api_key: str = None) -> pd.DataFrame:
    """Convenience: fetch prices and return as DataFrame."""
    prices = get_prices(ticker, start_date, end_date, api_key=api_key)
    return prices_to_df(prices)


# ---------------------------------------------------------------------------
# Market cap
# ---------------------------------------------------------------------------

def get_market_cap(ticker: str, end_date: str = None, api_key: str = None) -> float | None:
    """Return market cap. For historical dates, uses close_price × shares_outstanding."""
    # Current or very recent: use yfinance real-time
    try:
        if end_date is None:
            return get_market_cap_yf(ticker)
        ed = datetime.strptime(end_date, "%Y-%m-%d")
        if (datetime.now() - ed).days <= 5:
            return get_market_cap_yf(ticker)
    except (ValueError, TypeError):
        return get_market_cap_yf(ticker)

    # Historical: close_price(date) × shares_outstanding(date) from EDGAR
    start = (ed - timedelta(days=10)).strftime("%Y-%m-%d")
    prices = get_prices_yf(ticker, start, end_date)
    if not prices:
        return get_market_cap_yf(ticker)
    price = prices[-1]["close"]

    cik = get_cik(ticker)
    if not cik:
        return get_market_cap_yf(ticker)
    shares_series = get_line_item_history(cik, GAAP_CONCEPTS["outstanding_shares"], unit="shares")
    candidates = [v for v in shares_series if v["end"] <= end_date]
    if not candidates:
        return get_market_cap_yf(ticker)
    candidates.sort(key=lambda x: x["end"])
    shares = candidates[-1]["val"]

    return price * shares


def get_current_price(ticker: str) -> float | None:
    """Return real-time price via yfinance fast_info. More current than last historical close."""
    return get_current_price_yf(ticker)


# ---------------------------------------------------------------------------
# Internal helpers for SEC EDGAR data
# ---------------------------------------------------------------------------

def _safe_div(a, b):
    """Return a/b or None if either is None/zero."""
    if a is None or b is None:
        return None
    try:
        if float(b) == 0:
            return None
        return float(a) / float(b)
    except Exception:
        return None


def _growth(current, previous):
    """YoY growth rate."""
    if current is None or previous is None or previous == 0:
        return None
    return (current - previous) / abs(previous)


def _fetch_edgar_data(ticker: str) -> dict:
    """
    Fetch all needed EDGAR data for a ticker.
    Returns a dict keyed by concept name -> list[dict] of {end, val, form, accn}.
    """
    cik = get_cik(ticker)
    if not cik:
        return {}

    # Prefetch company facts (single HTTP call, cached)
    facts = get_company_facts(cik)
    if not facts:
        return {}

    results = {}
    concepts = [
        ("revenue", GAAP_CONCEPTS["revenue"], "USD"),
        ("revenue_fb", GAAP_CONCEPTS["revenue_fallback"], "USD"),
        ("gross_profit", GAAP_CONCEPTS["gross_profit"], "USD"),
        ("operating_income", GAAP_CONCEPTS["operating_income"], "USD"),
        ("net_income", GAAP_CONCEPTS["net_income"], "USD"),
        ("earnings_per_share", GAAP_CONCEPTS["earnings_per_share"], "USD/shares"),
        ("earnings_per_share_fb", GAAP_CONCEPTS["earnings_per_share_fallback"], "USD/shares"),
        ("research_and_development", GAAP_CONCEPTS["research_and_development"], "USD"),
        ("interest_expense", GAAP_CONCEPTS["interest_expense"], "USD"),
        ("depreciation_and_amortization", GAAP_CONCEPTS["depreciation_and_amortization"], "USD"),
        ("operating_expense", GAAP_CONCEPTS["operating_expense"], "USD"),
        ("total_assets", GAAP_CONCEPTS["total_assets"], "USD"),
        ("current_assets", GAAP_CONCEPTS["current_assets"], "USD"),
        ("total_liabilities", GAAP_CONCEPTS["total_liabilities"], "USD"),
        ("current_liabilities", GAAP_CONCEPTS["current_liabilities"], "USD"),
        ("cash_and_equivalents", GAAP_CONCEPTS["cash_and_equivalents"], "USD"),
        ("long_term_debt", GAAP_CONCEPTS["long_term_debt"], "USD"),
        ("short_term_borrowings", GAAP_CONCEPTS["short_term_borrowings"], "USD"),
        ("long_term_debt_current", GAAP_CONCEPTS["long_term_debt_current"], "USD"),
        ("shareholders_equity", GAAP_CONCEPTS["shareholders_equity"], "USD"),
        ("outstanding_shares", GAAP_CONCEPTS["outstanding_shares"], "shares"),
        ("goodwill", GAAP_CONCEPTS["goodwill"], "USD"),
        ("intangible_assets", GAAP_CONCEPTS["intangible_assets"], "USD"),
        ("capital_expenditure", GAAP_CONCEPTS["capital_expenditure"], "USD"),
        ("operating_cash_flow", GAAP_CONCEPTS["operating_cash_flow"], "USD"),
        ("dividends", GAAP_CONCEPTS["dividends"], "USD"),
        ("stock_issuance", GAAP_CONCEPTS["stock_issuance"], "USD"),
        ("stock_repurchase", GAAP_CONCEPTS["stock_repurchase"], "USD"),
        ("inventory", GAAP_CONCEPTS["inventory"], "USD"),
        ("accounts_receivable", GAAP_CONCEPTS["accounts_receivable"], "USD"),
    ]

    for key, concept, unit in concepts:
        try:
            results[key] = get_line_item_history(cik, concept, unit=unit)
        except Exception:
            results[key] = []

    return results


def _get_ttm_or_annual_with_source(series: list[dict], prefer_ttm: bool = True) -> tuple[float | None, str]:
    """Get TTM or annual value and which source was used.

    Returns (value, source) where source is 'ttm', 'annual', or 'none'.
    """
    if not series:
        return (None, "none")
    if prefer_ttm:
        val, src = compute_ttm_with_source(series)
        if val is not None:
            return (val, "ttm")
    annual = get_latest_annual(series)
    if annual is not None:
        return (annual, "annual")
    return (None, "none")


def _get_ttm_or_annual(series: list[dict], prefer_ttm: bool = True) -> float | None:
    """Get TTM (sum of last 4 quarters) if available, else latest annual."""
    val, _ = _get_ttm_or_annual_with_source(series, prefer_ttm)
    return val


def _get_stock_value(series: list[dict]) -> float | None:
    """Get latest value regardless of form (annual or quarterly)."""
    if not series:
        return None
    # Prefer latest annual
    annual_val = get_latest_annual(series)
    if annual_val is not None:
        return annual_val
    # Fall back to most recent quarterly
    quarters = [v for v in series if v["form"] == "10-Q"]
    if not quarters:
        return None
    quarters.sort(key=lambda x: x["end"])
    return quarters[-1]["val"]


def _historical_market_cap(date: str, price_by_date: dict, shares_series: list[dict]) -> float | None:
    """Compute market cap at a historical date: price × shares_outstanding."""
    if not price_by_date or not shares_series:
        return None
    price_dates = sorted(d for d in price_by_date if d <= date)
    if not price_dates:
        return None
    price = price_by_date[price_dates[-1]]
    candidates = [v for v in shares_series if v["end"] <= date]
    if not candidates:
        return None
    candidates.sort(key=lambda x: x["end"])
    shares = candidates[-1]["val"]
    return price * shares


def _build_metrics_for_period(
    ticker: str,
    report_period: str,
    period: str,
    edgar_data: dict,
    market_cap: float | None,
    yf_info: dict,
    is_ttm: bool,
    cutoff_date: str | None = None,
) -> FinancialMetrics:
    """Build a FinancialMetrics object from EDGAR data and yfinance info."""

    # Track period sources for consistency enforcement
    _flow_sources = {}  # key -> source ('ttm', 'annual', or 'none')

    def _best_series(key: str, fallback_key: str = None) -> list[dict]:
        """Return the better of primary/fallback series based on data freshness."""
        series = edgar_data.get(key, [])
        if cutoff_date:
            series = [v for v in series if v["end"] <= cutoff_date]
        if fallback_key:
            fb = edgar_data.get(fallback_key, [])
            if cutoff_date:
                fb = [v for v in fb if v["end"] <= cutoff_date]
            if fb:
                max_fb = max(v["end"] for v in fb)
                max_primary = max((v["end"] for v in series), default="")
                if max_fb > max_primary:
                    return fb
        return series

    def _pick(key: str, flow: bool = True, fallback_key: str = None) -> float | None:
        series = _best_series(key, fallback_key)
        if not series:
            return None
        if flow and is_ttm:
            val, src = _get_ttm_or_annual_with_source(series, prefer_ttm=True)
            _flow_sources[key] = src
            return val
        return _get_stock_value(series)

    def _pick_annual_only(key: str, fallback_key: str = None) -> float | None:
        """Force annual-only retrieval for a flow item."""
        series = _best_series(key, fallback_key)
        if not series:
            return None
        return get_latest_annual(series)

    # Flow items (sum for TTM)
    revenue = _pick("revenue", flow=True, fallback_key="revenue_fb")

    gross_profit = _pick("gross_profit", flow=True)
    operating_income = _pick("operating_income", flow=True)
    net_income = _pick("net_income", flow=True)
    r_and_d = _pick("research_and_development", flow=True)
    interest_expense = _pick("interest_expense", flow=True)
    da = _pick("depreciation_and_amortization", flow=True)
    capex = _pick("capital_expenditure", flow=True)
    ocf = _pick("operating_cash_flow", flow=True)
    dividends = _pick("dividends", flow=True)
    stock_issuance = _pick("stock_issuance", flow=True)
    stock_repurchase = _pick("stock_repurchase", flow=True)

    # Period consistency enforcement: if flow items mixed TTM and annual,
    # force all to annual to prevent meaningless ratios.
    if is_ttm:
        flow_source_values = [s for s in _flow_sources.values() if s != "none"]
        if flow_source_values and "ttm" in flow_source_values and "annual" in flow_source_values:
            logger.debug(
                "Period mismatch for %s (%s): mixed TTM/annual sources %s. "
                "Forcing all flow items to annual.",
                ticker, report_period, _flow_sources,
            )
            revenue = _pick_annual_only("revenue", fallback_key="revenue_fb")
            gross_profit = _pick_annual_only("gross_profit")
            operating_income = _pick_annual_only("operating_income")
            net_income = _pick_annual_only("net_income")
            r_and_d = _pick_annual_only("research_and_development")
            interest_expense = _pick_annual_only("interest_expense")
            da = _pick_annual_only("depreciation_and_amortization")
            capex = _pick_annual_only("capital_expenditure")
            ocf = _pick_annual_only("operating_cash_flow")
            dividends = _pick_annual_only("dividends")
            stock_issuance = _pick_annual_only("stock_issuance")
            stock_repurchase = _pick_annual_only("stock_repurchase")

    # Stock items (latest point-in-time)
    total_assets = _pick("total_assets", flow=False)
    current_assets = _pick("current_assets", flow=False)
    total_liabilities = _pick("total_liabilities", flow=False)
    current_liabilities = _pick("current_liabilities", flow=False)
    cash = _pick("cash_and_equivalents", flow=False)
    long_term_debt = _pick("long_term_debt", flow=False)
    short_term_debt = _pick("short_term_borrowings", flow=False)
    ltd_current = _pick("long_term_debt_current", flow=False)
    shareholders_equity = _pick("shareholders_equity", flow=False)
    shares_out = _pick("outstanding_shares", flow=False)
    goodwill = _pick("goodwill", flow=False)
    intangibles = _pick("intangible_assets", flow=False)
    inventory = _pick("inventory", flow=False)
    accounts_receivable = _pick("accounts_receivable", flow=False)

    # Derived values
    ebit = operating_income  # EBIT ≈ operating_income
    ebitda = None
    if operating_income is not None and da is not None:
        ebitda = operating_income + da

    total_debt = None
    if long_term_debt is not None:
        total_debt = long_term_debt
        if short_term_debt is not None:
            total_debt += short_term_debt
        elif ltd_current is not None:
            total_debt += ltd_current
    elif short_term_debt is not None:
        total_debt = short_term_debt

    goodwill_and_intangibles = None
    if goodwill is not None or intangibles is not None:
        goodwill_and_intangibles = (goodwill or 0) + (intangibles or 0)

    fcf = None
    if ocf is not None and capex is not None:
        fcf = ocf - capex

    working_capital = None
    if current_assets is not None and current_liabilities is not None:
        working_capital = current_assets - current_liabilities

    book_value_per_share = _safe_div(shareholders_equity, shares_out)

    # EPS — try EDGAR, fall back to yfinance
    eps = _pick("earnings_per_share", flow=False, fallback_key="earnings_per_share_fb")
    if eps is None and shares_out and shares_out > 0 and net_income is not None:
        eps = net_income / shares_out

    # Market-cap dependent ratios
    pe_ratio = None
    pb_ratio = None
    ps_ratio = None
    ev = None
    ev_to_ebitda = None
    ev_to_revenue = None
    fcf_yield = None
    peg = None

    if market_cap is not None:
        if eps and eps > 0:
            pe_ratio = market_cap / (eps * (shares_out or 1)) if shares_out else None
            # Better: use yfinance trailingPE if available
            pe_ratio = yf_info.get("trailingPE") or pe_ratio

        if shareholders_equity and shareholders_equity > 0 and shares_out and shares_out > 0:
            bvps = shareholders_equity / shares_out
            pb_ratio = _safe_div(market_cap / shares_out, bvps) if bvps else None

        if revenue and revenue > 0:
            ps_ratio = market_cap / revenue

        # Enterprise value
        ev = market_cap
        if total_debt:
            ev += total_debt
        if cash:
            ev -= cash

        if ebitda and ebitda > 0:
            ev_to_ebitda = _safe_div(ev, ebitda)
        if revenue and revenue > 0:
            ev_to_revenue = _safe_div(ev, revenue)
        if fcf and fcf > 0:
            fcf_yield = _safe_div(fcf, market_cap)

        # PEG ratio from yfinance
        peg = yf_info.get("pegRatio")

    # Margins
    gross_margin = _safe_div(gross_profit, revenue)
    operating_margin = _safe_div(operating_income, revenue)
    net_margin = _safe_div(net_income, revenue)

    # Returns
    roe = _safe_div(net_income, shareholders_equity)
    roa = _safe_div(net_income, total_assets)
    roic = None
    if net_income is not None and total_assets is not None and current_liabilities is not None:
        invested_capital = total_assets - current_liabilities
        roic = _safe_div(net_income, invested_capital)

    # Turnover ratios
    asset_turnover = _safe_div(revenue, total_assets)
    cogs = (revenue - gross_profit) if (revenue is not None and gross_profit is not None) else None
    inventory_turnover = _safe_div(cogs, inventory) if (cogs and inventory and inventory > 0) else None
    receivables_turnover = _safe_div(revenue, accounts_receivable) if accounts_receivable and accounts_receivable > 0 else None
    dso = None
    if receivables_turnover and receivables_turnover > 0:
        dso = 365.0 / receivables_turnover
    operating_cycle = None
    if dso is not None and inventory_turnover and inventory_turnover > 0:
        dio = 365.0 / inventory_turnover
        operating_cycle = dso + dio
    working_capital_turnover = _safe_div(revenue, working_capital) if working_capital and working_capital != 0 else None

    # Liquidity
    current_ratio = _safe_div(current_assets, current_liabilities)
    quick_ratio = None
    if current_assets is not None and inventory is not None and current_liabilities:
        quick_ratio = _safe_div(current_assets - inventory, current_liabilities)
    cash_ratio = _safe_div(cash, current_liabilities)
    ocf_ratio = _safe_div(ocf, current_liabilities)

    # Leverage
    debt_to_equity = _safe_div(total_debt, shareholders_equity)
    debt_to_assets = _safe_div(total_debt, total_assets)
    interest_coverage = _safe_div(ebit, interest_expense)

    # Payout
    payout_ratio = _safe_div(dividends, net_income) if net_income and net_income > 0 else None

    # Per share
    fcf_per_share = _safe_div(fcf, shares_out)

    return FinancialMetrics(
        ticker=ticker,
        report_period=report_period,
        period=period,
        currency="USD",
        market_cap=market_cap,
        enterprise_value=ev,
        price_to_earnings_ratio=pe_ratio,
        price_to_book_ratio=pb_ratio,
        price_to_sales_ratio=ps_ratio,
        enterprise_value_to_ebitda_ratio=ev_to_ebitda,
        enterprise_value_to_revenue_ratio=ev_to_revenue,
        free_cash_flow_yield=fcf_yield,
        peg_ratio=peg,
        gross_margin=gross_margin,
        operating_margin=operating_margin,
        net_margin=net_margin,
        return_on_equity=roe,
        return_on_assets=roa,
        return_on_invested_capital=roic,
        asset_turnover=asset_turnover,
        inventory_turnover=inventory_turnover,
        receivables_turnover=receivables_turnover,
        days_sales_outstanding=dso,
        operating_cycle=operating_cycle,
        working_capital_turnover=working_capital_turnover,
        current_ratio=current_ratio,
        quick_ratio=quick_ratio,
        cash_ratio=cash_ratio,
        operating_cash_flow_ratio=ocf_ratio,
        debt_to_equity=debt_to_equity,
        debt_to_assets=debt_to_assets,
        interest_coverage=interest_coverage,
        revenue_growth=None,  # requires prior period — computed in multi-period below
        earnings_growth=None,
        book_value_growth=None,
        earnings_per_share_growth=None,
        free_cash_flow_growth=None,
        operating_income_growth=None,
        ebitda_growth=None,
        payout_ratio=payout_ratio,
        earnings_per_share=eps,
        book_value_per_share=book_value_per_share,
        free_cash_flow_per_share=fcf_per_share,
    )


def _sanity_check_metrics(m: FinancialMetrics) -> FinancialMetrics:
    """Null out obviously implausible metric values and log warnings."""
    warnings = []

    # Margins should be between -200% and 200% for any real company
    for attr, label in [
        ("gross_margin", "Gross margin"),
        ("operating_margin", "Operating margin"),
        ("net_margin", "Net margin"),
    ]:
        val = getattr(m, attr, None)
        if val is not None and (val > 2.0 or val < -2.0):
            warnings.append(f"{label}={val:.2%} is implausible")
            setattr(m, attr, None)

    # ROE/ROA/ROIC > 500% is almost certainly wrong
    for attr, label in [
        ("return_on_equity", "ROE"),
        ("return_on_assets", "ROA"),
        ("return_on_invested_capital", "ROIC"),
    ]:
        val = getattr(m, attr, None)
        if val is not None and (val > 5.0 or val < -5.0):
            warnings.append(f"{label}={val:.2%} is implausible")
            setattr(m, attr, None)

    if warnings:
        logger.warning(
            "Sanity check for %s (%s): %s", m.ticker, m.report_period, "; ".join(warnings)
        )

    return m


def _get_annual_flow_series(edgar_data: dict, key: str, fallback_key: str = None, n: int = 5) -> list[tuple[str, float]]:
    """Get last n annual values for a flow concept."""
    series = edgar_data.get(key, [])
    if not series and fallback_key:
        series = edgar_data.get(fallback_key, [])
    return get_annual_series(series, n=n)


def get_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
    api_key: str = None,
) -> list[FinancialMetrics]:
    """Return FinancialMetrics for ticker, sorted by report_period descending."""
    cache_key = f"{ticker}_{period}_{end_date}_{limit}"
    if cached := _cache.get_financial_metrics(cache_key):
        return [FinancialMetrics(**m) for m in cached]

    try:
        edgar_data = _fetch_edgar_data(ticker)
        market_cap = get_market_cap_yf(ticker)

        import yfinance as yf
        yf_ticker = yf.Ticker(ticker)
        try:
            yf_info = yf_ticker.info or {}
        except Exception:
            yf_info = {}

        results: list[FinancialMetrics] = []

        # Pre-fetch shares series for historical market cap
        shares_series = edgar_data.get("outstanding_shares", [])

        if period == "ttm":
            # Multiple TTM snapshots — one per quarterly filing date
            # Prefer the fresher of primary/fallback revenue series
            rev_raw = edgar_data.get("revenue", [])
            rev_raw_fb = edgar_data.get("revenue_fb", [])
            if rev_raw_fb:
                max_fb = max((v["end"] for v in rev_raw_fb), default="")
                max_primary = max((v["end"] for v in rev_raw), default="") if rev_raw else ""
                if max_fb > max_primary:
                    rev_raw = rev_raw_fb
            if not rev_raw:
                rev_raw = rev_raw_fb or []
            q_dates = sorted(set(
                v["end"] for v in rev_raw if v["form"] == "10-Q" and v["end"] <= end_date
            ), reverse=True)[:limit]

            if not q_dates:
                q_dates = [end_date]

            # Pre-fetch prices for historical market cap computation
            earliest = q_dates[-1]
            price_start = (datetime.strptime(earliest, "%Y-%m-%d") - timedelta(days=10)).strftime("%Y-%m-%d")
            all_prices = get_prices_yf(ticker, price_start, end_date)
            price_by_date = {p["time"]: p["close"] for p in all_prices}

            for i, qd in enumerate(q_dates):
                if i == 0:
                    mc = market_cap
                else:
                    mc = _historical_market_cap(qd, price_by_date, shares_series)
                    if mc is None:
                        mc = market_cap

                m = _build_metrics_for_period(
                    ticker=ticker,
                    report_period=qd,
                    period="ttm",
                    edgar_data=edgar_data,
                    market_cap=mc,
                    yf_info=yf_info if i == 0 else {},
                    is_ttm=True,
                    cutoff_date=qd,
                )
                m = _sanity_check_metrics(m)
                results.append(m)
        else:
            # Annual periods — build one entry per fiscal year
            rev_series = _get_annual_flow_series(edgar_data, "revenue", "revenue_fb")
            ni_series = _get_annual_flow_series(edgar_data, "net_income")
            # Use revenue dates as the anchor for report periods
            periods_available = [d for d, _ in rev_series if d <= end_date]
            periods_available = sorted(set(periods_available), reverse=True)[:limit]

            # Pre-fetch prices for historical market cap (annual)
            if periods_available:
                _ea = periods_available[-1]
                _ps = (datetime.strptime(_ea, "%Y-%m-%d") - timedelta(days=10)).strftime("%Y-%m-%d")
                _ap = get_prices_yf(ticker, _ps, end_date)
                _apbd = {p["time"]: p["close"] for p in _ap}
            else:
                _apbd = {}

            for i, rp in enumerate(periods_available):
                mc = _historical_market_cap(rp, _apbd, shares_series)
                if mc is None:
                    mc = market_cap
                m = _build_metrics_for_period(
                    ticker=ticker,
                    report_period=rp,
                    period="annual",
                    edgar_data=edgar_data,
                    market_cap=mc,
                    yf_info=yf_info if i == 0 else {},
                    is_ttm=False,
                )
                m = _sanity_check_metrics(m)
                results.append(m)

        # Compute growth rates using consecutive periods in the revenue/NI series
        _gn = 10  # enough annual history for multiple TTM snapshots
        rev_series = _get_annual_flow_series(edgar_data, "revenue", "revenue_fb", n=_gn)
        ni_series = _get_annual_flow_series(edgar_data, "net_income", n=_gn)
        bv_series = _get_annual_flow_series(edgar_data, "shareholders_equity", n=_gn)
        eps_series = _get_annual_flow_series(edgar_data, "earnings_per_share", "earnings_per_share_fb", n=_gn)
        oi_series = _get_annual_flow_series(edgar_data, "operating_income", n=_gn)
        da_series_annual = _get_annual_flow_series(edgar_data, "depreciation_and_amortization", n=_gn)
        fcf_raw = edgar_data.get("operating_cash_flow", [])
        capex_raw = edgar_data.get("capital_expenditure", [])

        def _series_dict(series):
            return {d: v for d, v in series}

        rev_dict = _series_dict(rev_series)
        ni_dict = _series_dict(ni_series)
        bv_dict = _series_dict(bv_series)
        eps_dict = _series_dict(eps_series)
        oi_dict = _series_dict(oi_series)
        da_dict = _series_dict(da_series_annual)

        # EBITDA = operating_income + D&A
        ebitda_dict = {}
        for d in set(list(oi_dict.keys()) + list(da_dict.keys())):
            oi_v = oi_dict.get(d)
            da_v = da_dict.get(d)
            if oi_v is not None and da_v is not None:
                ebitda_dict[d] = oi_v + da_v

        def _prior_growth(dates, d_dict, current_rp):
            prior_dates = [d for d in dates if d < current_rp]
            if not prior_dates:
                return None
            prior = prior_dates[-1]
            current_dates = [d for d in dates if d <= current_rp]
            if not current_dates:
                return None
            current = current_dates[-1]
            return _growth(d_dict.get(current), d_dict.get(prior))

        # Compute per-period growth rates
        if results:
            fcf_annual = get_annual_series(fcf_raw, n=_gn)
            capex_annual = get_annual_series(capex_raw, n=_gn)
            fcf_d = {d: v for d, v in fcf_annual}
            cx_d = {d: v for d, v in capex_annual}
            all_fcf_dates = sorted(set(fcf_d.keys()) & set(cx_d.keys()))

            rev_dates = sorted(rev_dict.keys())
            ni_dates = sorted(ni_dict.keys())
            bv_dates = sorted(bv_dict.keys())
            eps_dates = sorted(eps_dict.keys())
            oi_dates = sorted(oi_dict.keys())
            ebitda_dates = sorted(ebitda_dict.keys())

            for m in results:
                rp = m.report_period

                if period == "ttm":
                    # For each TTM snapshot, use annual values on or before its report_period
                    rp_rev = [d for d in rev_dates if d <= rp]
                    if len(rp_rev) >= 2:
                        m.revenue_growth = _growth(rev_dict[rp_rev[-1]], rev_dict[rp_rev[-2]])
                    rp_ni = [d for d in ni_dates if d <= rp]
                    if len(rp_ni) >= 2:
                        m.earnings_growth = _growth(ni_dict[rp_ni[-1]], ni_dict[rp_ni[-2]])
                    rp_bv = [d for d in bv_dates if d <= rp]
                    if len(rp_bv) >= 2:
                        m.book_value_growth = _growth(bv_dict[rp_bv[-1]], bv_dict[rp_bv[-2]])
                    rp_eps = [d for d in eps_dates if d <= rp]
                    if len(rp_eps) >= 2:
                        m.earnings_per_share_growth = _growth(eps_dict[rp_eps[-1]], eps_dict[rp_eps[-2]])
                    rp_fcf = [d for d in all_fcf_dates if d <= rp]
                    if len(rp_fcf) >= 2:
                        fcf1 = fcf_d[rp_fcf[-1]] - cx_d[rp_fcf[-1]]
                        fcf0 = fcf_d[rp_fcf[-2]] - cx_d[rp_fcf[-2]]
                        m.free_cash_flow_growth = _growth(fcf1, fcf0)
                    rp_oi = [d for d in oi_dates if d <= rp]
                    if len(rp_oi) >= 2:
                        m.operating_income_growth = _growth(oi_dict[rp_oi[-1]], oi_dict[rp_oi[-2]])
                    rp_ebitda = [d for d in ebitda_dates if d <= rp]
                    if len(rp_ebitda) >= 2:
                        m.ebitda_growth = _growth(ebitda_dict[rp_ebitda[-1]], ebitda_dict[rp_ebitda[-2]])
                else:
                    m.revenue_growth = _prior_growth(rev_dates, rev_dict, rp)
                    m.earnings_growth = _prior_growth(ni_dates, ni_dict, rp)
                    m.book_value_growth = _prior_growth(bv_dates, bv_dict, rp)
                    m.earnings_per_share_growth = _prior_growth(eps_dates, eps_dict, rp)
                    m.operating_income_growth = _prior_growth(oi_dates, oi_dict, rp)
                    m.ebitda_growth = _prior_growth(ebitda_dates, ebitda_dict, rp)

                    prior_fcf_dates = [d for d in all_fcf_dates if d < rp]
                    current_fcf_dates = [d for d in all_fcf_dates if d <= rp]
                    if prior_fcf_dates and current_fcf_dates:
                        cur_d = current_fcf_dates[-1]
                        prv_d = prior_fcf_dates[-1]
                        fcf1 = fcf_d[cur_d] - cx_d[cur_d]
                        fcf0 = fcf_d[prv_d] - cx_d[prv_d]
                        m.free_cash_flow_growth = _growth(fcf1, fcf0)

        # Filter to end_date and apply limit
        results = [m for m in results if m.report_period <= end_date]
        results.sort(key=lambda m: m.report_period, reverse=True)
        results = results[:limit]

        if results:
            _cache.set_financial_metrics(cache_key, [m.model_dump() for m in results])

        return results

    except Exception as e:
        logger.warning("get_financial_metrics failed for %s: %s", ticker, e)
        return []


# ---------------------------------------------------------------------------
# search_line_items
# ---------------------------------------------------------------------------

# Mapping from line item name to (edgar_key, is_flow)
_LINE_ITEM_MAP = {
    "revenue": ("revenue", True, "revenue_fb"),
    "gross_profit": ("gross_profit", True, None),
    "operating_income": ("operating_income", True, None),
    "net_income": ("net_income", True, None),
    "earnings_per_share": ("earnings_per_share", False, "earnings_per_share_fb"),
    "research_and_development": ("research_and_development", True, None),
    "interest_expense": ("interest_expense", True, None),
    "depreciation_and_amortization": ("depreciation_and_amortization", True, None),
    "operating_expense": ("operating_expense", True, None),
    "total_assets": ("total_assets", False, None),
    "current_assets": ("current_assets", False, None),
    "total_liabilities": ("total_liabilities", False, None),
    "current_liabilities": ("current_liabilities", False, None),
    "cash_and_equivalents": ("cash_and_equivalents", False, None),
    "shareholders_equity": ("shareholders_equity", False, None),
    "outstanding_shares": ("outstanding_shares", False, None),
    "capital_expenditure": ("capital_expenditure", True, None),
    "dividends_and_other_cash_distributions": ("dividends", True, None),
    "free_cash_flow": ("operating_cash_flow", True, None),  # derived: OCF - capex
    "working_capital": ("current_assets", False, None),  # derived
    "book_value_per_share": ("shareholders_equity", False, None),  # derived
    "gross_margin": ("gross_profit", True, None),  # derived
    "operating_margin": ("operating_income", True, None),  # derived
    "debt_to_equity": ("long_term_debt", False, None),  # derived
    "return_on_invested_capital": ("net_income", True, None),  # derived
    "ebit": ("operating_income", True, None),
    "ebitda": ("operating_income", True, None),  # derived
    "total_debt": ("long_term_debt", False, None),  # derived
    "goodwill_and_intangible_assets": ("goodwill", False, None),  # derived
    "issuance_or_purchase_of_equity_shares": ("stock_issuance", True, None),  # derived
}


def search_line_items(
    ticker: str,
    line_items: list[str],
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
    api_key: str = None,
) -> list[LineItem]:
    """Return LineItem objects with requested fields populated from EDGAR + yfinance."""
    try:
        edgar_data = _fetch_edgar_data(ticker)

        # Determine report periods to cover
        # Use revenue series as anchor — prefer the fresher of primary/fallback
        rev_series = edgar_data.get("revenue", [])
        rev_fb = edgar_data.get("revenue_fb", [])
        if rev_fb:
            max_fb = max((v["end"] for v in rev_fb), default="")
            max_primary = max((v["end"] for v in rev_series), default="") if rev_series else ""
            if max_fb > max_primary:
                rev_series = rev_fb
        if not rev_series:
            rev_series = rev_fb
        annual_revs = get_annual_series(rev_series, n=limit + 1)
        annual_dates = [d for d, _ in annual_revs if d <= end_date]
        annual_dates = sorted(set(annual_dates), reverse=True)[:limit]

        results = []

        if period == "ttm":
            rev_raw = rev_series
            q_dates = sorted(set(
                v["end"] for v in rev_raw if v["form"] == "10-Q" and v["end"] <= end_date
            ), reverse=True)[:limit]
            if not q_dates:
                q_dates = [end_date]
            periods_to_process = [(d, "ttm") for d in q_dates]
        else:
            periods_to_process = [(d, "annual") for d in annual_dates]

        for rp, rp_period in periods_to_process:
            is_ttm = rp_period == "ttm"

            # Build base values
            _flow_sources_li = {}  # key -> source ('ttm', 'annual', 'none')

            def _best_series_li(key, fallback=None):
                """Return the better of primary/fallback series based on data freshness."""
                series = edgar_data.get(key, [])
                series = [v for v in series if v["end"] <= rp]
                if fallback:
                    fb = edgar_data.get(fallback, [])
                    fb = [v for v in fb if v["end"] <= rp]
                    if fb:
                        max_fb = max(v["end"] for v in fb)
                        max_primary = max((v["end"] for v in series), default="")
                        if max_fb > max_primary:
                            return fb
                return series

            def _pick_flow(key, fallback=None):
                series = _best_series_li(key, fallback)
                if not series:
                    return None
                if is_ttm:
                    val, src = _get_ttm_or_annual_with_source(series, prefer_ttm=True)
                    _flow_sources_li[key] = src
                    return val
                else:
                    annuals = [v for v in series if v["form"] == "10-K"]
                    if not annuals:
                        return None
                    annuals.sort(key=lambda x: x["end"])
                    return annuals[-1]["val"]

            def _pick_flow_annual_only(key, fallback=None):
                """Force annual-only retrieval for a flow item."""
                series = _best_series_li(key, fallback)
                if not series:
                    return None
                annuals = [v for v in series if v["form"] == "10-K"]
                if not annuals:
                    return None
                annuals.sort(key=lambda x: x["end"])
                return annuals[-1]["val"]

            def _pick_stock(key, fallback=None):
                series = edgar_data.get(key, [])
                if not series and fallback:
                    series = edgar_data.get(fallback, [])
                if not series:
                    return None
                candidates = [v for v in series if v["end"] <= rp]
                if not candidates:
                    return None
                candidates.sort(key=lambda x: x["end"])
                return candidates[-1]["val"]

            # Compute all base values
            revenue = _pick_flow("revenue", "revenue_fb")
            gross_profit = _pick_flow("gross_profit")
            operating_income = _pick_flow("operating_income")
            net_income = _pick_flow("net_income")
            r_and_d = _pick_flow("research_and_development")
            interest_expense = _pick_flow("interest_expense")
            da = _pick_flow("depreciation_and_amortization")
            capex = _pick_flow("capital_expenditure")
            ocf = _pick_flow("operating_cash_flow")
            dividends = _pick_flow("dividends")
            stock_issuance = _pick_flow("stock_issuance")
            stock_repurchase = _pick_flow("stock_repurchase")
            operating_expense = _pick_flow("operating_expense")

            # Period consistency enforcement for line items
            if is_ttm:
                flow_src_vals = [s for s in _flow_sources_li.values() if s != "none"]
                if flow_src_vals and "ttm" in flow_src_vals and "annual" in flow_src_vals:
                    logger.debug(
                        "search_line_items period mismatch for %s (%s): %s. Forcing annual.",
                        ticker, rp, _flow_sources_li,
                    )
                    revenue = _pick_flow_annual_only("revenue", "revenue_fb")
                    gross_profit = _pick_flow_annual_only("gross_profit")
                    operating_income = _pick_flow_annual_only("operating_income")
                    net_income = _pick_flow_annual_only("net_income")
                    r_and_d = _pick_flow_annual_only("research_and_development")
                    interest_expense = _pick_flow_annual_only("interest_expense")
                    da = _pick_flow_annual_only("depreciation_and_amortization")
                    capex = _pick_flow_annual_only("capital_expenditure")
                    ocf = _pick_flow_annual_only("operating_cash_flow")
                    dividends = _pick_flow_annual_only("dividends")
                    stock_issuance = _pick_flow_annual_only("stock_issuance")
                    stock_repurchase = _pick_flow_annual_only("stock_repurchase")
                    operating_expense = _pick_flow_annual_only("operating_expense")

            total_assets = _pick_stock("total_assets")
            current_assets = _pick_stock("current_assets")
            total_liabilities = _pick_stock("total_liabilities")
            current_liabilities = _pick_stock("current_liabilities")
            cash = _pick_stock("cash_and_equivalents")
            long_term_debt = _pick_stock("long_term_debt")
            short_term_debt = _pick_stock("short_term_borrowings")
            ltd_current = _pick_stock("long_term_debt_current")
            shareholders_equity = _pick_stock("shareholders_equity")
            shares_out = _pick_stock("outstanding_shares")
            goodwill = _pick_stock("goodwill")
            intangibles = _pick_stock("intangible_assets")
            eps = _pick_stock("earnings_per_share", "earnings_per_share_fb")

            # Derived
            fcf = (ocf - capex) if ocf is not None and capex is not None else None
            ebit = operating_income
            ebitda = (operating_income + da) if operating_income is not None and da is not None else None
            total_debt = None
            if long_term_debt is not None:
                total_debt = long_term_debt + (short_term_debt or ltd_current or 0)
            elif short_term_debt is not None:
                total_debt = short_term_debt
            goodwill_and_intangibles = None
            if goodwill is not None or intangibles is not None:
                goodwill_and_intangibles = (goodwill or 0) + (intangibles or 0)
            working_capital = (current_assets - current_liabilities) if current_assets is not None and current_liabilities is not None else None
            book_value_per_share = _safe_div(shareholders_equity, shares_out)
            gross_margin = _safe_div(gross_profit, revenue)
            operating_margin = _safe_div(operating_income, revenue)
            debt_to_equity = _safe_div(total_debt, shareholders_equity)
            roic = _safe_div(net_income, (total_assets - current_liabilities)) if total_assets is not None and current_liabilities is not None else None
            issuance_or_purchase = None
            if stock_issuance is not None or stock_repurchase is not None:
                issuance_or_purchase = (stock_issuance or 0) - (stock_repurchase or 0)

            VALUE_MAP = {
                "revenue": revenue,
                "gross_profit": gross_profit,
                "operating_income": operating_income,
                "net_income": net_income,
                "earnings_per_share": eps,
                "research_and_development": r_and_d,
                "interest_expense": interest_expense,
                "depreciation_and_amortization": da,
                "ebit": ebit,
                "ebitda": ebitda,
                "operating_expense": operating_expense,
                "total_assets": total_assets,
                "current_assets": current_assets,
                "total_liabilities": total_liabilities,
                "current_liabilities": current_liabilities,
                "cash_and_equivalents": cash,
                "total_debt": total_debt,
                "shareholders_equity": shareholders_equity,
                "goodwill_and_intangible_assets": goodwill_and_intangibles,
                "outstanding_shares": shares_out,
                "free_cash_flow": fcf,
                "capital_expenditure": capex,
                "dividends_and_other_cash_distributions": dividends,
                "issuance_or_purchase_of_equity_shares": issuance_or_purchase,
                "working_capital": working_capital,
                "book_value_per_share": book_value_per_share,
                "gross_margin": gross_margin,
                "operating_margin": operating_margin,
                "debt_to_equity": debt_to_equity,
                "return_on_invested_capital": roic,
            }

            extra_fields = {k: VALUE_MAP.get(k) for k in line_items}

            item = LineItem(
                ticker=ticker,
                report_period=rp,
                period=rp_period,
                currency="USD",
                **extra_fields,
            )
            results.append(item)

        results = [r for r in results if r.report_period <= end_date]
        results.sort(key=lambda r: r.report_period, reverse=True)
        return results[:limit]

    except Exception as e:
        logger.warning("search_line_items failed for %s: %s", ticker, e)
        return []


# ---------------------------------------------------------------------------
# Insider trades
# ---------------------------------------------------------------------------

def get_insider_trades(
    ticker: str,
    end_date: str,
    start_date: str | None = None,
    limit: int = 1000,
    api_key: str = None,
) -> list[InsiderTrade]:
    """Return insider trades from Finnhub. Returns [] if no API key."""
    cache_key = f"{ticker}_{start_date or 'none'}_{end_date}_{limit}"
    if cached := _cache.get_insider_trades(cache_key):
        return [InsiderTrade(**t) for t in cached]

    sd = start_date or (
        datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=365)
    ).strftime("%Y-%m-%d")

    raw = get_insider_trades_fh(ticker, sd, end_date, limit=limit)
    if not raw:
        return []

    trades = []
    for t in raw:
        try:
            trades.append(InsiderTrade(**t))
        except Exception:
            continue

    if trades:
        _cache.set_insider_trades(cache_key, [t.model_dump() for t in trades])
    return trades


# ---------------------------------------------------------------------------
# Company news
# ---------------------------------------------------------------------------

def get_company_news(
    ticker: str,
    end_date: str,
    start_date: str | None = None,
    limit: int = 1000,
    api_key: str = None,
) -> list[CompanyNews]:
    """Return company news from Finnhub. Returns [] if no API key."""
    cache_key = f"{ticker}_{start_date or 'none'}_{end_date}_{limit}"
    if cached := _cache.get_company_news(cache_key):
        return [CompanyNews(**n) for n in cached]

    sd = start_date or (
        datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=30)
    ).strftime("%Y-%m-%d")

    raw = get_company_news_fh(ticker, sd, end_date, limit=limit)
    if not raw:
        return []

    news = []
    for n in raw:
        try:
            news.append(CompanyNews(**n))
        except Exception:
            continue

    if news:
        _cache.set_company_news(cache_key, [n.model_dump() for n in news])
    return news


# ---------------------------------------------------------------------------
# Intraday prices
# ---------------------------------------------------------------------------

def get_intraday_prices(ticker: str, interval: str = "5m", period: str = "5d", api_key: str = None) -> list:
    """Get intraday OHLCV price bars.

    Args:
        ticker: Stock symbol
        interval: Bar size - "1m", "5m", "15m", "30m"
        period: Lookback - "1d", "5d", "1mo", "2mo"
        api_key: Unused, kept for API compatibility

    Returns list of dicts with: open, close, high, low, volume, time
    """
    from ai_hedge.data.providers.yfinance_intraday import get_intraday_prices_yf
    return get_intraday_prices_yf(ticker, interval=interval, period=period)


def get_premarket_data(ticker: str) -> dict | None:
    """Get pre-market price data (price, change %, previous close)."""
    from ai_hedge.data.providers.yfinance_intraday import get_premarket_data_yf
    return get_premarket_data_yf(ticker)


def intraday_to_df(bars: list) -> pd.DataFrame:
    """Convert intraday bars to DataFrame with datetime index."""
    if not bars:
        return pd.DataFrame()
    df = pd.DataFrame(bars)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time").sort_index()
    return df
