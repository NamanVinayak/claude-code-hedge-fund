"""
Aggregate persona signals + deterministic agent signals into signals_combined.json.

Usage:
    python -m ai_hedge.runner.aggregate --run-id 20240101_120000 --tickers AAPL,MSFT --cash 100000 --mode invest
"""
import argparse
import glob
import json
import os
from datetime import datetime, timedelta

from ai_hedge.deterministic.fundamentals import fundamentals_analyst_agent
from ai_hedge.deterministic.technicals import technical_analyst_agent
from ai_hedge.deterministic.valuation import valuation_analyst_agent
from ai_hedge.deterministic.sentiment import sentiment_analyst_agent
from ai_hedge.deterministic.risk_manager import risk_management_agent
from ai_hedge.portfolio.allowed_actions import compute_allowed_actions

VALID_MODES = ("invest", "swing", "daytrade", "research")


def _build_state(tickers: list[str], start_date: str, end_date: str) -> dict:
    return {
        "data": {
            "tickers": tickers,
            "start_date": start_date,
            "end_date": end_date,
            "analyst_signals": {},
            "portfolio": {},
        },
        "metadata": {"show_reasoning": False},
        "messages": [],
    }


def _load_persona_signals(signals_dir: str) -> dict:
    """Load all *.json files from signals/ dir. Returns merged analyst_signals dict."""
    merged = {}
    pattern = os.path.join(signals_dir, "*.json")
    for path in glob.glob(pattern):
        persona = os.path.splitext(os.path.basename(path))[0]
        with open(path) as f:
            data = json.load(f)
        # Each file: {"TICKER": {"signal": ..., "confidence": ..., "reasoning": ...}}
        merged[persona] = data
    return merged


def _load_end_date(raw_dir: str, tickers: list[str]) -> str:
    """Read end_date from raw data file."""
    for ticker in tickers:
        path = os.path.join(raw_dir, f"{ticker}.json")
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            return data.get("end_date", datetime.today().strftime("%Y-%m-%d"))
    return datetime.today().strftime("%Y-%m-%d")


def _load_start_date(raw_dir: str, tickers: list[str]) -> str:
    """Read start_date from raw data file."""
    for ticker in tickers:
        path = os.path.join(raw_dir, f"{ticker}.json")
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            return data.get("start_date", (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"))
    return (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")


def _load_mode(run_dir: str) -> str:
    """Load mode from metadata.json, defaulting to 'invest'."""
    meta_path = os.path.join(run_dir, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f).get("mode", "invest")
    return "invest"


def main():
    parser = argparse.ArgumentParser(description="Aggregate signals for hedge fund run.")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols")
    parser.add_argument("--cash", type=float, default=100000.0, help="Starting cash (default: 100000)")
    parser.add_argument("--margin-requirement", type=float, default=0.0, help="Margin requirement (default: 0.0)")
    parser.add_argument("--mode", choices=VALID_MODES, default=None,
                        help="Analysis mode override (default: read from metadata.json)")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    run_dir = os.path.join("runs", args.run_id)
    signals_dir = os.path.join(run_dir, "signals")
    raw_dir = os.path.join(run_dir, "raw")

    # Determine mode: CLI flag overrides metadata.json
    mode = args.mode or _load_mode(run_dir)
    print(f"Aggregate mode: {mode}")

    end_date = _load_end_date(raw_dir, tickers)
    start_date = _load_start_date(raw_dir, tickers)

    # Load persona signals
    print("Loading persona signals...")
    analyst_signals = _load_persona_signals(signals_dir)
    print(f"  Loaded {len(analyst_signals)} persona signal file(s).")

    # Build portfolio for deterministic agents (empty positions)
    portfolio = {
        "cash": args.cash,
        "margin_requirement": args.margin_requirement,
        "margin_used": 0.0,
        "positions": {
            ticker: {"long": 0, "long_cost_basis": 0.0, "short": 0, "short_cost_basis": 0.0}
            for ticker in tickers
        },
        "realized_gains": {ticker: {"long": 0.0, "short": 0.0} for ticker in tickers},
    }

    # Build shared state for deterministic agents
    state = _build_state(tickers, start_date, end_date)
    state["data"]["analyst_signals"] = analyst_signals
    state["data"]["portfolio"] = portfolio

    # Run deterministic agents
    print("Running fundamentals agent...")
    state.update(fundamentals_analyst_agent(state))

    print("Running technicals agent...")
    state.update(technical_analyst_agent(state))

    print("Running valuation agent...")
    state.update(valuation_analyst_agent(state))

    print("Running sentiment agent...")
    state.update(sentiment_analyst_agent(state))

    # Run risk manager (needs portfolio + price data)
    print("Running risk manager...")
    state.update(risk_management_agent(state))

    # Intraday technicals: run for daytrade and research modes
    if mode in ("daytrade", "research"):
        print("Running intraday technicals agent...")
        from ai_hedge.deterministic.technicals_intraday import technical_intraday_agent
        state.update(technical_intraday_agent(state))

    all_signals = state["data"]["analyst_signals"]

    # Extract current_prices and max_shares from risk manager output
    risk_data = all_signals.get("risk_management_agent", {})
    current_prices = {
        ticker: float(risk_data.get(ticker, {}).get("current_price", 0.0))
        for ticker in tickers
    }
    max_shares = {
        ticker: int(risk_data.get(ticker, {}).get("remaining_position_limit", 0.0) / max(current_prices.get(ticker, 1.0), 0.01))
        for ticker in tickers
    }

    # Compute allowed actions
    print("Computing allowed actions...")
    allowed_actions = compute_allowed_actions(tickers, current_prices, max_shares, portfolio)

    # Write combined signals file
    combined = {
        "mode": mode,
        "analyst_signals": all_signals,
        "allowed_actions": allowed_actions,
        "portfolio": portfolio,
        "tickers": tickers,
        "end_date": end_date,
    }

    out_path = os.path.join(run_dir, "signals_combined.json")
    with open(out_path, "w") as f:
        json.dump(combined, f, indent=2, default=str)

    print("Signals combined. Ready for portfolio manager.")


if __name__ == "__main__":
    main()
