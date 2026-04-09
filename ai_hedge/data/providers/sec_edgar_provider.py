"""SEC EDGAR XBRL companyfacts API provider for US-GAAP financial data."""

import time
import requests

# Rate limiting: SEC allows 10 req/sec, we use ~9/sec to be safe
_SEC_SLEEP = 0.11

_HEADERS = {
    "User-Agent": "ai-hedge-fund research@example.com",
    "Accept-Encoding": "gzip, deflate",
}

# In-memory cache keyed by CIK
_cik_map: dict[str, str] | None = None  # ticker -> CIK (zero-padded to 10 digits)
_company_facts_cache: dict[str, dict] = {}  # CIK -> facts json


def _load_cik_map() -> dict[str, str]:
    """Load ticker->CIK map from SEC. Cached globally."""
    global _cik_map
    if _cik_map is not None:
        return _cik_map
    try:
        url = "https://www.sec.gov/files/company_tickers.json"
        resp = requests.get(url, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # data: {index: {cik_str, ticker, title}}
        mapping = {}
        for entry in data.values():
            tkr = entry.get("ticker", "").upper()
            cik = str(entry.get("cik_str", "")).zfill(10)
            if tkr:
                mapping[tkr] = cik
        _cik_map = mapping
        time.sleep(_SEC_SLEEP)
        return _cik_map
    except Exception:
        _cik_map = {}
        return _cik_map


def get_cik(ticker: str) -> str | None:
    """Look up CIK for ticker. Returns zero-padded 10-digit string or None."""
    mapping = _load_cik_map()
    return mapping.get(ticker.upper())


def get_company_facts(cik: str) -> dict | None:
    """Fetch companyfacts JSON from SEC EDGAR. Cached per CIK."""
    if cik in _company_facts_cache:
        return _company_facts_cache[cik]
    try:
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        resp = requests.get(url, headers=_HEADERS, timeout=30)
        if resp.status_code != 200:
            return None
        data = resp.json()
        _company_facts_cache[cik] = data
        time.sleep(_SEC_SLEEP)
        return data
    except Exception:
        return None


def get_line_item_history(cik: str, concept: str, unit: str = "USD") -> list[dict]:
    """
    Returns list of {end: 'YYYY-MM-DD', val: float, form: str, accn: str}
    from companyfacts for a given US-GAAP concept.
    Filters to 10-K and 10-Q forms. Sorted by end date ascending.
    """
    facts = get_company_facts(cik)
    if not facts:
        return []
    try:
        units_data = facts["facts"]["us-gaap"][concept]["units"][unit]
    except (KeyError, TypeError):
        return []

    seen = {}  # (end, form) -> dict, prefer 10-K over 10-Q
    for entry in units_data:
        form = entry.get("form", "")
        if form not in ("10-K", "10-Q", "10-K/A", "10-Q/A"):
            continue
        end = entry.get("end", "")
        if not end:
            continue
        # Normalize form
        norm_form = "10-K" if "10-K" in form else "10-Q"
        key = (end, norm_form)
        val = entry.get("val")
        if val is None:
            continue
        # Keep the entry with the largest accn (amended filings have a higher accn)
        existing = seen.get(key)
        if existing is None or entry.get("accn", "") > existing.get("accn", ""):
            seen[key] = {
                "end": end,
                "val": float(val),
                "form": norm_form,
                "accn": entry.get("accn", ""),
            }

    results = list(seen.values())
    results.sort(key=lambda x: x["end"])
    return results


def compute_ttm(quarterly_values: list[dict]) -> float | None:
    """Sum the last 4 quarterly values (by end date). Returns None if fewer than 4."""
    # Filter to 10-Q only
    quarters = [v for v in quarterly_values if v["form"] == "10-Q"]
    quarters.sort(key=lambda x: x["end"])
    if len(quarters) < 4:
        return None
    last4 = quarters[-4:]
    return sum(q["val"] for q in last4)


def get_latest_annual(annual_values: list[dict]) -> float | None:
    """Get the most recent annual (10-K) value."""
    annuals = [v for v in annual_values if v["form"] == "10-K"]
    if not annuals:
        return None
    annuals.sort(key=lambda x: x["end"])
    return annuals[-1]["val"]


def get_latest_annual_with_date(annual_values: list[dict]) -> tuple[str, float] | None:
    """Get (end_date, value) for most recent 10-K entry."""
    annuals = [v for v in annual_values if v["form"] == "10-K"]
    if not annuals:
        return None
    annuals.sort(key=lambda x: x["end"])
    last = annuals[-1]
    return (last["end"], last["val"])


def get_annual_series(annual_values: list[dict], n: int = 4) -> list[tuple[str, float]]:
    """Get last n annual (10-K) values as (end_date, value) sorted by date ascending."""
    annuals = [v for v in annual_values if v["form"] == "10-K"]
    annuals.sort(key=lambda x: x["end"])
    return [(v["end"], v["val"]) for v in annuals[-n:]]


# GAAP concept mapping
GAAP_CONCEPTS = {
    "revenue": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "revenue_fallback": "Revenues",
    "gross_profit": "GrossProfit",
    "operating_income": "OperatingIncomeLoss",
    "net_income": "NetIncomeLoss",
    "earnings_per_share": "EarningsPerShareBasic",
    "earnings_per_share_fallback": "EarningsPerShareDiluted",
    "research_and_development": "ResearchAndDevelopmentExpense",
    "interest_expense": "InterestExpense",
    "depreciation_and_amortization": "DepreciationDepletionAndAmortization",
    "operating_expense": "OperatingExpenses",
    "total_assets": "Assets",
    "current_assets": "AssetsCurrent",
    "total_liabilities": "Liabilities",
    "current_liabilities": "LiabilitiesCurrent",
    "cash_and_equivalents": "CashAndCashEquivalentsAtCarryingValue",
    "long_term_debt": "LongTermDebt",
    "short_term_borrowings": "ShortTermBorrowings",
    "long_term_debt_current": "LongTermDebtCurrent",
    "shareholders_equity": "StockholdersEquity",
    "outstanding_shares": "CommonStockSharesOutstanding",  # unit: shares
    "goodwill": "Goodwill",
    "intangible_assets": "IntangibleAssetsNetExcludingGoodwill",
    "capital_expenditure": "PaymentsToAcquirePropertyPlantAndEquipment",
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities",
    "dividends": "PaymentsOfDividends",
    "stock_issuance": "ProceedsFromIssuanceOfCommonStock",
    "stock_repurchase": "PaymentsForRepurchaseOfCommonStock",
    "inventory": "InventoryNet",
    "accounts_receivable": "AccountsReceivableNetCurrent",
}


def fetch_concept(cik: str, concept: str, unit: str = "USD") -> list[dict]:
    """Fetch a single concept from EDGAR, with rate limiting already handled in get_company_facts."""
    return get_line_item_history(cik, concept, unit=unit)
