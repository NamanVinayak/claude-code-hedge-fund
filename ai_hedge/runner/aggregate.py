"""
Aggregate persona signals + deterministic agent signals into signals_combined.json.

Usage:
    python -m ai_hedge.runner.aggregate --run-id 20240101_120000 --tickers AAPL,MSFT --cash 100000 --mode invest
    python -m ai_hedge.runner.aggregate --run-id 20240101_120000 --tickers BTC-USD,ETH-USD --cash 100000 --asset-type crypto
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
from ai_hedge.schemas import HeadTraderSignal

VALID_MODES = ("invest", "swing", "daytrade", "research")

# Maps mode → head trader signal file name. Research mode skips the head trader.
_HEAD_TRADER_AGENTS: dict[str, str] = {
    "swing": "swing_head_trader",
    "daytrade": "dt_head_trader",
}


class HeadTraderSynthesisFailed(Exception):
    """Raised when a head trader signal file exists but fails JSON parse or Pydantic validation."""


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


def _expected_agents(mode: str, asset_type: str) -> list[str]:
    """Return the agent JSON files we expect under runs/<id>/signals/ for this run.

    Imports list-of-truth from facts builders, not hardcoded — so if we add or
    remove an agent in one place, this stays in sync.
    """
    expected: list[str] = []
    if mode == "invest" or mode == "research":
        if asset_type != "crypto":
            from ai_hedge.personas.facts_builder import PERSONA_BUILDERS
            expected.extend(PERSONA_BUILDERS.keys())
            expected.append("growth_analyst_agent")
    if mode == "swing" or mode == "research":
        from ai_hedge.personas.swing_facts_builder import SWING_AGENTS
        expected.extend(SWING_AGENTS)
        if asset_type == "crypto":
            expected.append("crypto_sentiment")
    if mode == "swing":
        # Head trader is required in swing but NOT in research (research skips it).
        expected.append("swing_head_trader")
    if mode == "daytrade" or mode == "research":
        from ai_hedge.personas.dt_facts_builder import DT_AGENTS
        expected.extend(DT_AGENTS)
    if mode == "daytrade":
        # Head trader is required in daytrade but NOT in research.
        expected.append("dt_head_trader")
    return expected


def _validate_head_trader_strict(signals_dir: str, mode: str, degraded: list[str]) -> None:
    """Validate head trader signal file if one is expected for this mode.

    Does nothing for invest/research modes (no head trader step).
    If the file exists but fails JSON parse or Pydantic validation, logs a
    detailed error, adds the agent to degraded_inputs, and raises
    HeadTraderSynthesisFailed so the orchestrator can decide whether to retry.
    """
    ht_name = _HEAD_TRADER_AGENTS.get(mode)
    if not ht_name:
        return

    path = os.path.join(signals_dir, f"{ht_name}.json")
    if not os.path.exists(path):
        # Missing case is already tracked by _expected_agents / degraded_inputs.
        return

    try:
        with open(path) as f:
            raw = f.read()
    except OSError as e:
        if ht_name not in degraded:
            degraded.append(ht_name)
        raise HeadTraderSynthesisFailed(
            f"[{ht_name}] Could not read file {path}: {e}"
        ) from e

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        if ht_name not in degraded:
            degraded.append(ht_name)
        raise HeadTraderSynthesisFailed(
            f"[{ht_name}] JSON parse failed: {e}\n"
            f"File: {path}\n"
            f"Content snippet: {raw[:200]!r}"
        ) from e

    # Pydantic validation — each key is a ticker symbol mapping to HeadTraderSignal.
    errors: list[str] = []
    for ticker, ticker_data in data.items():
        if not isinstance(ticker_data, dict):
            errors.append(f"  {ticker}: expected dict, got {type(ticker_data).__name__}")
            continue
        try:
            HeadTraderSignal(**ticker_data)
        except Exception as ve:
            errors.append(f"  {ticker}: {ve}")

    if errors:
        if ht_name not in degraded:
            degraded.append(ht_name)
        raise HeadTraderSynthesisFailed(
            f"[{ht_name}] Pydantic validation failed:\n" + "\n".join(errors) +
            f"\nFile: {path}\nContent snippet: {raw[:200]!r}"
        )


def _load_persona_signals(signals_dir: str, expected: list[str]) -> tuple[dict, list[str]]:
    """Load all *.json from signals/ dir.

    Returns (merged_signals_dict, missing_agents_list). Missing agents are
    expected files that didn't appear — these get logged AND written into
    signals_combined.json so downstream agents (head trader, PM) can see the
    degraded input set instead of pretending consensus is full.
    """
    merged: dict = {}
    pattern = os.path.join(signals_dir, "*.json")
    for path in glob.glob(pattern):
        persona = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"  WARNING: failed to load {persona}.json: {e}")
            continue
        merged[persona] = data

    missing = [a for a in expected if a not in merged]
    if missing:
        print(f"  WARNING: {len(missing)} expected agent signal(s) missing — degraded run:")
        for a in missing:
            print(f"    - {a}")
    return merged, missing


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


def _load_asset_type(run_dir: str) -> str:
    """Load asset_type from metadata.json, defaulting to 'stock'."""
    meta_path = os.path.join(run_dir, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f).get("asset_type", "stock")
    return "stock"


def _load_default_cash() -> float:
    try:
        with open("tracker/watchlist.json") as f:
            return float(json.load(f).get("paper_account_size", 5000.0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 5000.0


def main():
    parser = argparse.ArgumentParser(description="Aggregate signals for hedge fund run.")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols")
    parser.add_argument("--cash", type=float, default=_load_default_cash(),
                        help="Starting cash (default: paper_account_size from tracker/watchlist.json)")
    parser.add_argument("--margin-requirement", type=float, default=0.0, help="Margin requirement (default: 0.0)")
    parser.add_argument("--mode", choices=VALID_MODES, default=None,
                        help="Analysis mode override (default: read from metadata.json)")
    parser.add_argument("--asset-type", choices=("stock",), default="stock",
                        help="Asset type: stock (default)")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    run_dir = os.path.join("runs", args.run_id)
    signals_dir = os.path.join(run_dir, "signals")
    raw_dir = os.path.join(run_dir, "raw")

    # Determine mode and asset type: CLI flags override metadata.json
    mode = args.mode or _load_mode(run_dir)
    asset_type = args.asset_type or _load_asset_type(run_dir)
    print(f"Aggregate mode: {mode}" + (f" [crypto]" if asset_type == "crypto" else ""))

    end_date = _load_end_date(raw_dir, tickers)
    start_date = _load_start_date(raw_dir, tickers)

    # Load persona signals (with explicit expected list so missing files surface)
    print("Loading persona signals...")
    expected = _expected_agents(mode, asset_type)
    analyst_signals, missing_agents = _load_persona_signals(signals_dir, expected)
    print(f"  Loaded {len(analyst_signals)} signal file(s). Expected {len(expected)}. Missing {len(missing_agents)}.")

    # Strict head trader validation — raises HeadTraderSynthesisFailed if the file
    # exists but is malformed or fails Pydantic schema. This is the most important
    # synthesis layer; a silent parse failure here means the PM runs blind.
    try:
        _validate_head_trader_strict(signals_dir, mode, missing_agents)
    except HeadTraderSynthesisFailed as e:
        print(f"\n  ERROR (HeadTraderSynthesisFailed): {e}")
        raise

    # Pull live portfolio state from the local trade DBs. The PM used to start
    # every run pretending args.cash was untouched and there were zero open
    # positions — that meant it could re-buy a ticker it was already long in,
    # and assume cash was free that was actually locked up in 12 open trades.
    # Now we read tracker.db (stocks) + crypto_tracker.db (crypto) and inject:
    #   - per-ticker long/short qty + cost basis for tickers in this run
    #   - 'other_positions': open positions in tickers NOT analyzed this run
    #     (so the PM can see locked capital + correlated risk)
    #   - cash reduced by total open exposure
    if asset_type == "crypto":
        raise NotImplementedError(
            "Crypto trading mode has been quarantined. "
            "Crypto code is preserved at .archive/crypto/. "
            "Stock swing/daytrade/invest/research modes are unaffected."
        )
    else:
        try:
            from tracker.db import get_open_positions, get_pending_trades, get_recent_trade_history
            open_positions = get_open_positions()
            pending_orders = get_pending_trades()
            recent_closed = get_recent_trade_history(days=7)
        except Exception as e:
            print(f"  WARNING: could not load stock open positions: {e}")
            open_positions = []
            pending_orders = []
            recent_closed = []

    analyzed = {t.upper() for t in tickers}
    positions: dict[str, dict] = {
        ticker: {"long": 0, "long_cost_basis": 0.0, "short": 0, "short_cost_basis": 0.0}
        for ticker in tickers
    }
    other_positions: list[dict] = []
    total_exposure = 0.0

    for p in open_positions:
        tk = (p.get("ticker") or "").upper()
        qty = float(p.get("quantity", 0) or 0)
        # Prefer fill price (what we actually paid); fall back to limit price.
        fill_price = float(p.get("entry_fill_price") or p.get("entry_price") or 0)
        total_exposure += qty * fill_price

        if tk in analyzed:
            slot = positions[tk]
            if p.get("direction") == "long":
                # Aggregate across multiple lots in the same ticker (e.g. two NVDA
                # entries from the same run). Cost basis is share-weighted average.
                prev_qty = slot.get("long", 0) or 0
                prev_basis = slot.get("long_cost_basis", 0.0) or 0.0
                new_qty = prev_qty + qty
                if new_qty > 0:
                    slot["long_cost_basis"] = (prev_qty * prev_basis + qty * fill_price) / new_qty
                slot["long"] = new_qty
            elif p.get("direction") == "short":
                prev_qty = slot.get("short", 0) or 0
                prev_basis = slot.get("short_cost_basis", 0.0) or 0.0
                new_qty = prev_qty + qty
                if new_qty > 0:
                    slot["short_cost_basis"] = (prev_qty * prev_basis + qty * fill_price) / new_qty
                slot["short"] = new_qty
        else:
            other_positions.append(p)

    cash_after_exposure = max(0.0, float(args.cash) - total_exposure)
    print(f"  Loaded {len(open_positions)} open position(s); "
          f"{len(other_positions)} in non-analyzed tickers. "
          f"Exposure ${total_exposure:,.0f} → cash ${cash_after_exposure:,.0f}. "
          f"{len(pending_orders)} pending order(s), {len(recent_closed)} recent closed trade(s) injected.")

    # Build portfolio for deterministic agents (now reflecting real state)
    portfolio = {
        "cash": cash_after_exposure,
        "margin_requirement": args.margin_requirement,
        "margin_used": 0.0,
        "positions": positions,
        "other_positions": other_positions,
        "realized_gains": {ticker: {"long": 0.0, "short": 0.0} for ticker in tickers},
        "pending_orders": pending_orders,
        "recent_closed": recent_closed,
    }

    # Build shared state for deterministic agents
    state = _build_state(tickers, start_date, end_date)
    state["data"]["analyst_signals"] = analyst_signals
    state["data"]["portfolio"] = portfolio
    state["data"]["asset_type"] = asset_type

    # Run deterministic agents (skip fundamentals/valuation/sentiment for crypto)
    if asset_type != "crypto":
        print("Running fundamentals agent...")
        state.update(fundamentals_analyst_agent(state))
    else:
        print("Skipping fundamentals agent (crypto)")

    print("Running technicals agent...")
    state.update(technical_analyst_agent(state))

    if asset_type != "crypto":
        print("Running valuation agent...")
        state.update(valuation_analyst_agent(state))
    else:
        print("Skipping valuation agent (crypto)")

    if asset_type != "crypto":
        print("Running sentiment agent...")
        state.update(sentiment_analyst_agent(state))
    else:
        print("Skipping sentiment agent (crypto — using crypto_sentiment signal)")

    # Run risk manager (needs portfolio + price data — works for both)
    print("Running risk manager...")
    state.update(risk_management_agent(state))

    # Intraday technicals: run for daytrade and research modes
    if mode in ("daytrade", "research"):
        print("Running intraday technicals agent...")
        from ai_hedge.deterministic.technicals_intraday import technical_intraday_analyst_agent
        state.update(technical_intraday_analyst_agent(state))

    all_signals = state["data"]["analyst_signals"]

    # Extract current_prices and max_shares from risk manager output
    risk_data = all_signals.get("risk_management_agent", {})
    current_prices = {
        ticker: float(risk_data.get(ticker, {}).get("current_price", 0.0))
        for ticker in tickers
    }
    fractional = asset_type == "crypto"
    max_shares = {
        ticker: risk_data.get(ticker, {}).get("remaining_position_limit", 0.0) / max(current_prices.get(ticker, 1.0), 0.01)
        if fractional else
        int(risk_data.get(ticker, {}).get("remaining_position_limit", 0.0) / max(current_prices.get(ticker, 1.0), 0.01))
        for ticker in tickers
    }

    # Compute allowed actions
    print("Computing allowed actions...")
    allowed_actions = compute_allowed_actions(
        tickers,
        current_prices,
        max_shares,
        portfolio,
        fractional=fractional,
        current_positions=open_positions,
    )

    # Write combined signals file. degraded_inputs lets the head trader / PM
    # see honestly which expected agents failed to write a signal this run.
    combined = {
        "mode": mode,
        "analyst_signals": all_signals,
        "allowed_actions": allowed_actions,
        "portfolio": portfolio,
        "tickers": tickers,
        "end_date": end_date,
        "degraded_inputs": missing_agents,
    }

    out_path = os.path.join(run_dir, "signals_combined.json")
    with open(out_path, "w") as f:
        json.dump(combined, f, indent=2, default=str)

    print("Signals combined. Ready for portfolio manager.")


if __name__ == "__main__":
    main()
