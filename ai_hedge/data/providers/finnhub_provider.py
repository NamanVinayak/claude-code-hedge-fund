"""Finnhub data provider for insider trades and company news."""

import os
from dotenv import load_dotenv

try:
    import finnhub as _finnhub_lib
    _FINNHUB_AVAILABLE = True
except ImportError:
    _finnhub_lib = None
    _FINNHUB_AVAILABLE = False

load_dotenv()


def _client():
    if not _FINNHUB_AVAILABLE:
        return None
    key = os.getenv("FINNHUB_API_KEY", "")
    if not key:
        return None
    return _finnhub_lib.Client(api_key=key)


def get_insider_trades_fh(ticker: str, start_date: str, end_date: str, limit: int = 1000) -> list[dict]:
    """
    Returns list of insider trade dicts matching InsiderTrade model fields.
    Returns [] if no API key or any error.
    """
    try:
        client = _client()
        if client is None:
            return []
        data = client.stock_insider_transactions(ticker, start_date, end_date)
        transactions = data.get("data", []) if data else []
        results = []
        for t in transactions[:limit]:
            results.append({
                "ticker": ticker,
                "issuer": None,
                "name": t.get("name"),
                "title": None,  # Finnhub doesn't provide job titles
                "is_board_director": None,
                "transaction_date": t.get("transactionDate"),
                "transaction_shares": float(t.get("change", 0)) if t.get("change") is not None else None,
                "transaction_price_per_share": None,  # Finnhub doesn't provide this directly
                "transaction_value": None,
                "shares_owned_before_transaction": None,
                "shares_owned_after_transaction": float(t.get("share", 0)) if t.get("share") is not None else None,
                "security_title": None,
                "filing_date": t.get("filingDate") or t.get("transactionDate") or "",
            })
        return results
    except Exception:
        return []


def get_company_news_fh(ticker: str, start_date: str, end_date: str, limit: int = 100) -> list[dict]:
    """
    Returns list of news dicts matching CompanyNews model fields.
    Returns [] if no API key or any error.
    """
    try:
        client = _client()
        if client is None:
            return []
        news_list = client.company_news(ticker, _from=start_date, to=end_date)
        if not news_list:
            return []
        results = []
        for n in news_list[:limit]:
            # Convert unix timestamp to YYYY-MM-DD
            dt = n.get("datetime")
            if dt:
                import datetime
                date_str = datetime.datetime.fromtimestamp(dt, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
            else:
                date_str = ""
            results.append({
                "ticker": ticker,
                "title": n.get("headline", ""),
                "author": None,
                "source": n.get("source", ""),
                "date": date_str,
                "url": n.get("url", ""),
                "sentiment": None,
            })
        return results
    except Exception:
        return []
