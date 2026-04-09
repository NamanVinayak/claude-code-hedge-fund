"""
Fetch all raw financial data for given tickers and save to disk.

Usage:
    python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id 20240101_120000 --mode invest
"""
import argparse
import json
import os
from datetime import datetime, timedelta

from ai_hedge.data.api import (
    get_financial_metrics,
    get_market_cap,
    get_current_price,
    get_insider_trades,
    get_company_news,
    get_prices,
    search_line_items,
)

VALID_MODES = ("invest", "swing", "daytrade", "research")

ALL_LINE_ITEMS = [
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "earnings_per_share",
    "research_and_development",
    "interest_expense",
    "depreciation_and_amortization",
    "ebit",
    "ebitda",
    "operating_expense",
    "total_assets",
    "current_assets",
    "total_liabilities",
    "current_liabilities",
    "cash_and_equivalents",
    "total_debt",
    "shareholders_equity",
    "goodwill_and_intangible_assets",
    "outstanding_shares",
    "free_cash_flow",
    "capital_expenditure",
    "dividends_and_other_cash_distributions",
    "issuance_or_purchase_of_equity_shares",
    "working_capital",
    "book_value_per_share",
    "gross_margin",
    "operating_margin",
    "debt_to_equity",
    "return_on_invested_capital",
]


def _to_json_serializable(obj):
    """Recursively convert Pydantic models and other non-serializable objects."""
    if hasattr(obj, "model_dump"):
        return _to_json_serializable(obj.model_dump())
    if isinstance(obj, list):
        return [_to_json_serializable(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _to_json_serializable(v) for k, v in obj.items()}
    return obj


def main():
    parser = argparse.ArgumentParser(description="Fetch raw financial data for hedge fund run.")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols, e.g. AAPL,MSFT")
    parser.add_argument("--start-date", default=None, help="Start date YYYY-MM-DD (default: 1 year ago)")
    parser.add_argument("--end-date", default=None, help="End date YYYY-MM-DD (default: today)")
    parser.add_argument("--run-id", required=True, help="Unique run identifier, e.g. 20240101_120000")
    parser.add_argument("--mode", choices=VALID_MODES, default="invest",
                        help="Analysis mode: invest (default), swing, daytrade, or research")
    args = parser.parse_args()
    mode = args.mode

    tickers = [t.strip().upper() for t in args.tickers.split(",")]

    today = datetime.today()
    end_date = args.end_date or today.strftime("%Y-%m-%d")
    start_date = args.start_date or (today - timedelta(days=365)).strftime("%Y-%m-%d")

    raw_dir = os.path.join("runs", args.run_id, "raw")
    facts_dir = os.path.join("runs", args.run_id, "facts")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(facts_dir, exist_ok=True)

    for ticker in tickers:
        print(f"Fetching data for {ticker}...")

        metrics = get_financial_metrics(ticker, end_date=end_date, period="ttm", limit=10)
        line_items = search_line_items(ticker, ALL_LINE_ITEMS, end_date=end_date, period="ttm", limit=10)
        market_cap = get_market_cap(ticker, end_date=end_date)
        current_price = get_current_price(ticker)
        insider_trades = get_insider_trades(ticker, end_date=end_date, start_date=start_date, limit=1000)
        company_news = get_company_news(ticker, end_date=end_date, start_date=start_date, limit=1000)
        prices = get_prices(ticker, start_date=start_date, end_date=end_date)

        print(f"  Current price (real-time): ${current_price:.2f}" if current_price else "  Current price: unavailable")

        raw = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "financial_metrics": _to_json_serializable(metrics),
            "line_items": _to_json_serializable(line_items),
            "market_cap": market_cap,
            "current_price": current_price,
            "insider_trades": _to_json_serializable(insider_trades),
            "company_news": _to_json_serializable(company_news),
            "prices": _to_json_serializable(prices),
        }

        out_path = os.path.join(raw_dir, f"{ticker}.json")
        with open(out_path, "w") as f:
            json.dump(raw, f, indent=2, default=str)

    print(f"Data ready in runs/{args.run_id}/raw/")

    # Save run metadata
    metadata = {
        "mode": mode,
        "tickers": tickers,
        "start_date": start_date,
        "end_date": end_date,
    }
    meta_path = os.path.join("runs", args.run_id, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata ({mode} mode) → runs/{args.run_id}/metadata.json")

    # Always build invest-mode persona facts (all modes need this foundational data)
    print("\nBuilding persona facts bundles...")
    from ai_hedge.personas.facts_builder import build_all_facts
    build_all_facts(args.run_id, tickers)

    # Swing facts: needed for swing and research modes
    if mode in ("swing", "research"):
        print("\nBuilding swing strategy facts...")
        from ai_hedge.personas.swing_facts_builder import build_swing_facts
        build_swing_facts(args.run_id, tickers)

    # Day-trade facts: needed for daytrade and research modes
    if mode in ("daytrade", "research"):
        print("\nBuilding day-trade strategy facts...")
        from ai_hedge.personas.dt_facts_builder import build_dt_facts
        build_dt_facts(args.run_id, tickers)

    print("Prepare complete.")


if __name__ == "__main__":
    main()
