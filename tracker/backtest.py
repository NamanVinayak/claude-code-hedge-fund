#!/usr/bin/env python3
"""
Swing trade accuracy checker.
Reads tracker/swing_predictions.json, fetches 1h yfinance bars,
and prints a plain-English portfolio dashboard.

Usage:
    .venv/bin/python tracker/backtest.py
    .venv/bin/python tracker/backtest.py --json   # machine-readable output
"""

import json, sys, time, argparse
from pathlib import Path
from datetime import date
import yfinance as yf

# Support running as both `python tracker/backtest.py` and `python -m tracker.backtest`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tracker.spy_benchmark import compute_spy_benchmark, format_headline  # noqa: E402

BUDGET = 1000  # $ per trade
PREDICTIONS_FILE = Path(__file__).parent / "swing_predictions.json"


def check_trade(ticker, direction, entry, target, stop, start_date):
    df = yf.Ticker(ticker).history(start=start_date, interval="1h")
    if df.empty:
        return "NO DATA", None, 0

    entered = False
    for _, row in df.iterrows():
        h, l = row["High"], row["Low"]
        if not entered:
            if (direction == "long" and l <= entry) or (direction == "short" and h >= entry):
                entered = True
        else:
            if direction == "long":
                if h >= target: return "TARGET HIT", target, round((target - entry) / entry * 100, 2)
                if l <= stop:   return "STOP HIT",   stop,   round((stop   - entry) / entry * 100, 2)
            else:
                if l <= target: return "TARGET HIT", target, round((entry - target) / entry * 100, 2)
                if h >= stop:   return "STOP HIT",   stop,   round((entry - stop)   / entry * 100, 2)

    if not entered:
        return "NOT ENTERED", None, 0

    try:
        cur = yf.Ticker(ticker).fast_info.last_price
        if not cur or cur != cur:  # None or NaN
            cur = df["Close"].iloc[-1]
    except Exception:
        cur = df["Close"].iloc[-1]

    unr = round(((cur - entry) / entry * 100) if direction == "long" else ((entry - cur) / entry * 100), 2)
    return "STILL OPEN", cur, unr


def calc_position(entry, is_crypto):
    if is_crypto:
        qty = round(BUDGET / entry, 4)
    else:
        qty = max(1, int(BUDGET / entry))
    return qty, round(qty * entry, 2)


def run(verbose=False):
    preds = json.loads(PREDICTIONS_FILE.read_text())

    results = []
    for t in preds:
        if date.fromisoformat(t["start_date"]) > date.today():
            status, exit_px, pnl_pct = "FUTURE", None, 0
            qty, invested = calc_position(t["entry"], t["is_crypto"])
            results.append({**t, "status": status, "exit_px": exit_px,
                            "pnl_pct": pnl_pct, "pnl_dollar": 0,
                            "qty": qty, "invested": invested})
            continue

        status, exit_px, pnl_pct = check_trade(
            t["ticker"], t["direction"], t["entry"],
            t["target"], t["stop"], t["start_date"]
        )
        qty, invested = calc_position(t["entry"], t["is_crypto"])
        pnl_dollar = round(invested * pnl_pct / 100, 2) if status != "NOT ENTERED" else 0
        results.append({**t, "status": status, "exit_px": exit_px,
                        "pnl_pct": pnl_pct, "pnl_dollar": pnl_dollar,
                        "qty": qty, "invested": invested})
        if verbose:
            print(f"  {t['ticker']:10s} {status}", flush=True)
        time.sleep(0.25)

    # ── Categorise ─────────────────────────────────────────────────────────
    entered   = [r for r in results if r["status"] not in ("NOT ENTERED", "NO DATA", "FUTURE")]
    not_enter = [r for r in results if r["status"] == "NOT ENTERED"]
    no_data   = [r for r in results if r["status"] == "NO DATA"]
    future    = [r for r in results if r["status"] == "FUTURE"]
    targets   = [r for r in entered  if r["status"] == "TARGET HIT"]
    stops     = [r for r in entered  if r["status"] == "STOP HIT"]
    open_pos  = [r for r in entered  if r["status"] == "STILL OPEN"]

    stock_entered  = [r for r in entered if not r["is_crypto"]]
    crypto_entered = [r for r in entered if r["is_crypto"]]

    realized_pnl   = sum(r["pnl_dollar"] for r in targets + stops)
    unrealized_pnl = sum(r["pnl_dollar"] for r in open_pos)
    total_pnl      = realized_pnl + unrealized_pnl
    total_invested = sum(r["invested"] for r in entered)

    win_rate = round(len(targets) / len(targets + stops) * 100, 1) if (targets or stops) else 0
    entry_rate = round(len(entered) / len([r for r in results if r["status"] not in ("NO DATA","FUTURE")]) * 100, 1) if results else 0

    stock_wins  = [r for r in targets if not r["is_crypto"]]
    crypto_wins = [r for r in targets if r["is_crypto"]]
    stock_resolved  = [r for r in stock_entered  if r["status"] in ("TARGET HIT","STOP HIT")]
    crypto_resolved = [r for r in crypto_entered if r["status"] in ("TARGET HIT","STOP HIT")]
    stock_wr  = round(len(stock_wins)  / len(stock_resolved)  * 100, 1) if stock_resolved  else 0
    crypto_wr = round(len(crypto_wins) / len(crypto_resolved) * 100, 1) if crypto_resolved else 0

    sign = "+" if total_pnl >= 0 else ""
    r_sign = "+" if realized_pnl >= 0 else ""
    u_sign = "+" if unrealized_pnl >= 0 else ""

    # ── SPY benchmark (deployed-capital buy-and-hold) ──────────────────────
    spy_capital = sum(r["invested"] for r in entered if not r["is_crypto"])
    spy_line = ""
    if entered and spy_capital > 0:
        starts = [r["start_date"] for r in entered if not r["is_crypto"]]
        if starts:
            spy_start_date = min(starts)
            spy_end_date = date.today().isoformat()
            spy_bench = compute_spy_benchmark(spy_start_date, spy_end_date, spy_capital)
            you_pnl_stock = sum(r["pnl_dollar"] for r in entered if not r["is_crypto"])
            you_pct_stock = (you_pnl_stock / spy_capital * 100) if spy_capital else 0.0
            spy_line = format_headline(you_pnl_stock, you_pct_stock, spy_bench)

    # ── Plain-English Dashboard ────────────────────────────────────────────
    print("\n" + "═" * 62)
    print("  AI HEDGE FUND · SWING TRADE DASHBOARD")
    print("═" * 62)
    if spy_line:
        # Strip markdown bold for a plain-text terminal line
        print("  " + spy_line.replace("**", ""))
        print("─" * 62)
    print(f"\n  PORTFOLIO SUMMARY")
    print(f"  {'Total predictions tracked:':<32} {len(results)}")
    print(f"  {'Entry reached:':<32} {len(entered)} of {len(results) - len(no_data)}  ({entry_rate}%)")
    print(f"  {'Currently open:':<32} {len(open_pos)}")
    print(f"  {'Targets hit ✓:':<32} {len(targets)}")
    print(f"  {'Stops hit ✗:':<32} {len(stops)}")
    print(f"  {'Not entered:':<32} {len(not_enter)}")
    if no_data:
        print(f"  {'No data:':<32} {len(no_data)}")
    if future:
        print(f"  {'Future (not started yet):':<32} {len(future)}")

    print(f"\n  P&L  (@ ${BUDGET:,}/trade allocation)")
    print(f"  {'Realized P&L:':<32} {r_sign}${realized_pnl:,.2f}")
    print(f"  {'Unrealized P&L:':<32} {u_sign}${unrealized_pnl:,.2f}")
    print(f"  {'NET TOTAL:':<32} {sign}${total_pnl:,.2f}  ({sign}{round(total_pnl/total_invested*100,2) if total_invested else 0}%)")
    print(f"  {'Capital deployed:':<32} ${total_invested:,.2f}")

    print(f"\n  ACCURACY")
    print(f"  {'Win rate (resolved trades):':<32} {win_rate}%  ({len(targets)}W / {len(stops)}L)")
    print(f"  {'Stock win rate:':<32} {stock_wr}%")
    print(f"  {'Crypto win rate:':<32} {crypto_wr}%")

    if open_pos:
        print(f"\n  OPEN POSITIONS")
        for r in open_pos:
            label = "CRYPTO" if r["is_crypto"] else "STOCK"
            sign2 = "+" if r["pnl_pct"] >= 0 else ""
            print(f"  [{label}] {r['ticker']:10s} {r['direction'].upper():5s}  "
                  f"entry ${r['entry']:>10,.3f}  now ${r['exit_px']:>10,.3f}  "
                  f"{sign2}{r['pnl_pct']:.2f}%  ({sign2}${r['pnl_dollar']:,.2f})")

    print("\n" + "═" * 62 + "\n")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    run(verbose=args.verbose)
