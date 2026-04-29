#!/usr/bin/env python3
"""
Swing Routine Backtest — Audits automated stock swing trade recommendations
against actual market data.

Primary data source: scripts/routine_raw_results.json (extracted from Claude routines UI).
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

import yfinance as yf

# ── Configuration ──────────────────────────────────────────────────────────

POSITION_SIZE_USD = 500  # hypothetical $ per trade
RAW_RESULTS_PATH = Path(__file__).parent / "routine_raw_results.json"


# ── Data fetching ──────────────────────────────────────────────────────────


def load_all_runs() -> list[dict]:
    """Load all trade recommendations from routine_raw_results.json."""
    with open(RAW_RESULTS_PATH) as f:
        data = json.load(f)

    all_trades = []

    for run in data["runs"]:
        # Use created_at date as the recommendation date
        rec_date = datetime.strptime(run["created_at"][:10], "%Y-%m-%d").date()
        batch_label = run["batch"]
        run_status = run["status"]
        session_id = run.get("session_id", "")

        decisions = run.get("decisions", {})
        if not decisions:
            continue

        for ticker, decision in decisions.items():
            action = decision.get("action", decision.get("direction", "hold"))
            if action is None:
                continue
            action = action.lower()

            if action in ("hold", "no_trade", "neutral", "—", ""):
                continue

            if action in ("buy", "cover", "long"):
                direction = "long"
            elif action in ("sell", "short"):
                direction = "short"
            else:
                continue

            # Flexible field parsing (same pattern as tracker/executor.py)
            entry_price = decision.get("entry_price", decision.get("entry"))
            target_price = decision.get("target_price",
                           decision.get("target",
                           decision.get("target_1")))
            stop_loss = decision.get("stop_loss", decision.get("stop"))

            targets = decision.get("targets", [])
            if targets and not target_price:
                target_price = targets[0] if len(targets) > 0 else None

            if not entry_price or not stop_loss or not target_price:
                continue

            try:
                entry_price = float(entry_price)
                target_price = float(target_price)
                stop_loss = float(stop_loss)
            except (ValueError, TypeError):
                continue

            if entry_price <= 0:
                continue

            confidence = decision.get("confidence", 0)
            timeframe = decision.get("timeframe", "")

            all_trades.append({
                "ticker": ticker,
                "direction": direction,
                "entry_price": entry_price,
                "target_price": target_price,
                "stop_loss": stop_loss,
                "confidence": confidence,
                "timeframe": timeframe,
                "rec_date": rec_date,
                "source": f"{batch_label} ({run_status})",
                "run_date": str(rec_date),
                "session_id": session_id,
            })

    return all_trades


# ── Deduplication ─────────────────────────────────────────────────────────

def deduplicate_trades(trades: list[dict]) -> list[dict]:
    """
    If the same ticker appears in multiple runs on the same date from the same batch,
    keep only the LATEST run. Different batches on the same date are kept (different tickers).
    Apr 17 has two runs that both cover all 14 tickers — keep the later one per ticker.
    """
    # Group by (ticker, rec_date, batch) — batch is derived from source
    seen = {}
    for t in trades:
        # Extract batch from source label
        batch = "B1" if "Batch 1" in t["source"] else "B2"
        key = (t["ticker"], t["rec_date"], batch)
        # Later entries override earlier ones (they appear later in the JSON)
        seen[key] = t
    return list(seen.values())


# ── Price fetching ────────────────────────────────────────────────────────


def fetch_ohlc(ticker: str, start_date, end_date) -> list[dict]:
    """Fetch daily OHLC from yfinance."""
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = (end_date + timedelta(days=1)).strftime("%Y-%m-%d")

    tk = yf.Ticker(ticker)
    df = tk.history(start=start_str, end=end_str, interval="1d")

    if df.empty:
        return []

    bars = []
    for idx, row in df.iterrows():
        bars.append({
            "date": idx.date(),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })
    return bars


# ── Trade evaluation ─────────────────────────────────────────────────────


def evaluate_trade(trade: dict, bars: list[dict]) -> dict:
    """
    Evaluate a single trade recommendation against actual OHLC data.
    Returns trade dict augmented with status and P&L.
    """
    result = trade.copy()
    result["status"] = "not_triggered"
    result["pnl_pct"] = 0.0
    result["pnl_usd"] = 0.0
    result["exit_date"] = None
    result["exit_price"] = None

    direction = trade["direction"]
    entry = trade["entry_price"]
    target = trade["target_price"]
    stop = trade["stop_loss"]

    # Filter bars to only those AFTER the recommendation date
    future_bars = [b for b in bars if b["date"] > trade["rec_date"]]

    if not future_bars:
        return result

    # Check if entry was triggered
    entry_bar_idx = None
    for i, bar in enumerate(future_bars):
        if direction == "long":
            # Entry hit if price dipped to entry level or below
            if bar["low"] <= entry:
                entry_bar_idx = i
                break
        else:  # short
            # Entry hit if price rose to entry level or above
            if bar["high"] >= entry:
                entry_bar_idx = i
                break

    if entry_bar_idx is None:
        result["status"] = "not_triggered"
        return result

    # Entry was hit — now check target vs stop from the entry bar onward
    # On the entry bar itself, price could also hit target or stop
    for bar in future_bars[entry_bar_idx:]:
        if direction == "long":
            target_hit = bar["high"] >= target
            stop_hit = bar["low"] <= stop
        else:  # short
            target_hit = bar["low"] <= target
            stop_hit = bar["high"] >= stop

        if target_hit and stop_hit:
            # Both hit on same bar — use conservative assumption (loss)
            # Unless open was already past target (win)
            if direction == "long":
                if bar["open"] >= target:
                    result["status"] = "win"
                    result["exit_price"] = target
                else:
                    result["status"] = "loss"
                    result["exit_price"] = stop
            else:
                if bar["open"] <= target:
                    result["status"] = "win"
                    result["exit_price"] = target
                else:
                    result["status"] = "loss"
                    result["exit_price"] = stop
            result["exit_date"] = bar["date"]
            break
        elif target_hit:
            result["status"] = "win"
            result["exit_price"] = target
            result["exit_date"] = bar["date"]
            break
        elif stop_hit:
            result["status"] = "loss"
            result["exit_price"] = stop
            result["exit_date"] = bar["date"]
            break

    if result["status"] not in ("win", "loss"):
        result["status"] = "open"
        # Mark current unrealized P&L based on last close
        last_close = future_bars[-1]["close"]
        if direction == "long":
            result["pnl_pct"] = (last_close - entry) / entry * 100
        else:
            result["pnl_pct"] = (entry - last_close) / entry * 100
        result["pnl_usd"] = POSITION_SIZE_USD * result["pnl_pct"] / 100
        result["exit_price"] = last_close
        result["exit_date"] = future_bars[-1]["date"]
        return result

    # Calculate P&L for resolved trades
    if direction == "long":
        result["pnl_pct"] = (result["exit_price"] - entry) / entry * 100
    else:
        result["pnl_pct"] = (entry - result["exit_price"]) / entry * 100
    result["pnl_usd"] = POSITION_SIZE_USD * result["pnl_pct"] / 100

    return result


# ── Report formatting ────────────────────────────────────────────────────


def format_report(results: list[dict]) -> str:
    """Format the full backtest report."""
    lines = []

    wins = [r for r in results if r["status"] == "win"]
    losses = [r for r in results if r["status"] == "loss"]
    opens = [r for r in results if r["status"] == "open"]
    not_triggered = [r for r in results if r["status"] == "not_triggered"]

    total_trades = len(results)
    resolved = len(wins) + len(losses)
    win_rate = len(wins) / resolved * 100 if resolved else 0
    entry_hit_rate = (len(wins) + len(losses) + len(opens)) / total_trades * 100 if total_trades else 0

    total_pnl = sum(r["pnl_usd"] for r in results if r["status"] in ("win", "loss"))
    realized_pnl = total_pnl
    unrealized_pnl = sum(r["pnl_usd"] for r in opens)

    # Header
    lines.append("=" * 56)
    lines.append("STOCK SWING ROUTINE — ACCURACY REPORT")
    lines.append("April 17-24, 2026 (12 routine sessions)")
    lines.append("=" * 56)
    lines.append("")
    lines.append(f"OVERALL: {len(wins)} wins / {len(losses)} losses / {len(opens)} open / {len(not_triggered)} not triggered")
    lines.append(f"TOTAL RECOMMENDATIONS: {total_trades} (from {len(set(r['run_date'] for r in results))} run dates)")
    lines.append(f"WIN RATE: {win_rate:.1f}% (of {resolved} resolved trades)")
    lines.append(f"ENTRY HIT RATE: {entry_hit_rate:.1f}% (entries that actually triggered)")
    lines.append(f"REALIZED P&L: {'+'if realized_pnl>=0 else ''}${realized_pnl:,.2f} (assuming ${POSITION_SIZE_USD}/trade)")
    lines.append(f"UNREALIZED P&L: {'+'if unrealized_pnl>=0 else ''}${unrealized_pnl:,.2f} ({len(opens)} open positions)")
    lines.append(f"TOTAL P&L: {'+'if (realized_pnl+unrealized_pnl)>=0 else ''}${realized_pnl+unrealized_pnl:,.2f}")
    lines.append("")

    # Per-ticker breakdown
    lines.append("─" * 56)
    lines.append("PER-TICKER BREAKDOWN")
    lines.append("─" * 56)
    header = f"{'Ticker':<7} {'Trades':>6} {'Wins':>5} {'Loss':>5} {'Open':>5} {'NoHit':>5} {'WinR':>6} {'P&L':>10}"
    lines.append(header)
    lines.append("-" * len(header))

    ticker_groups = defaultdict(list)
    for r in results:
        ticker_groups[r["ticker"]].append(r)

    for ticker in sorted(ticker_groups.keys()):
        trades = ticker_groups[ticker]
        tw = sum(1 for t in trades if t["status"] == "win")
        tl = sum(1 for t in trades if t["status"] == "loss")
        to = sum(1 for t in trades if t["status"] == "open")
        tn = sum(1 for t in trades if t["status"] == "not_triggered")
        resolved_t = tw + tl
        wr = f"{tw/resolved_t*100:.0f}%" if resolved_t else "N/A"
        pnl = sum(t["pnl_usd"] for t in trades if t["status"] in ("win", "loss"))
        pnl_str = f"{'+'if pnl>=0 else ''}${pnl:,.2f}" if resolved_t else "—"
        lines.append(f"{ticker:<7} {len(trades):>6} {tw:>5} {tl:>5} {to:>5} {tn:>5} {wr:>6} {pnl_str:>10}")

    lines.append("")

    # Per-date breakdown
    lines.append("─" * 56)
    lines.append("PER-DATE BREAKDOWN")
    lines.append("─" * 56)
    header2 = f"{'Date':<12} {'Trades':>6} {'Wins':>5} {'Loss':>5} {'Open':>5} {'NoHit':>5} {'WinR':>6}"
    lines.append(header2)
    lines.append("-" * len(header2))

    date_groups = defaultdict(list)
    for r in results:
        date_groups[r["run_date"]].append(r)

    for date in sorted(date_groups.keys()):
        trades = date_groups[date]
        tw = sum(1 for t in trades if t["status"] == "win")
        tl = sum(1 for t in trades if t["status"] == "loss")
        to = sum(1 for t in trades if t["status"] == "open")
        tn = sum(1 for t in trades if t["status"] == "not_triggered")
        resolved_t = tw + tl
        wr = f"{tw/resolved_t*100:.0f}%" if resolved_t else "N/A"
        lines.append(f"{date:<12} {len(trades):>6} {tw:>5} {tl:>5} {to:>5} {tn:>5} {wr:>6}")

    lines.append("")

    # Detailed trade log
    lines.append("─" * 56)
    lines.append("DETAILED TRADE LOG")
    lines.append("─" * 56)
    log_header = f"{'Date':<12} {'Ticker':<6} {'Dir':<6} {'Entry':>8} {'Stop':>8} {'Target':>8} {'Status':<13} {'P&L':>9} {'Conf':>4}"
    lines.append(log_header)
    lines.append("-" * len(log_header))

    sorted_results = sorted(results, key=lambda r: (r["run_date"], r["ticker"]))
    for r in sorted_results:
        pnl_str = f"{'+'if r['pnl_usd']>=0 else ''}${r['pnl_usd']:,.2f}" if r["status"] in ("win", "loss", "open") else "—"
        status_str = r["status"]
        if r["status"] == "open" and r["exit_price"]:
            status_str = f"open @{r['exit_price']:.2f}"
        elif r["status"] in ("win", "loss") and r["exit_date"]:
            status_str = f"{r['status']} {r['exit_date']}"
        conf_str = f"{r['confidence']}%" if r['confidence'] else "—"
        lines.append(
            f"{r['run_date']:<12} {r['ticker']:<6} {r['direction']:<6} "
            f"${r['entry_price']:>7.2f} ${r['stop_loss']:>7.2f} ${r['target_price']:>7.2f} "
            f"{status_str:<13} {pnl_str:>9} {conf_str:>4}"
        )

    lines.append("")

    # Confidence calibration
    lines.append("─" * 56)
    lines.append("CONFIDENCE CALIBRATION")
    lines.append("─" * 56)

    resolved_trades = [r for r in results if r["status"] in ("win", "loss")]
    if resolved_trades:
        conf_buckets = defaultdict(lambda: {"wins": 0, "total": 0})
        for r in resolved_trades:
            bucket = f"{(r['confidence'] // 10) * 10}-{(r['confidence'] // 10) * 10 + 9}%"
            conf_buckets[bucket]["total"] += 1
            if r["status"] == "win":
                conf_buckets[bucket]["wins"] += 1

        header3 = f"{'Confidence':>12} {'Trades':>7} {'Wins':>5} {'Win Rate':>9}"
        lines.append(header3)
        lines.append("-" * len(header3))
        for bucket in sorted(conf_buckets.keys()):
            data = conf_buckets[bucket]
            wr = f"{data['wins']/data['total']*100:.0f}%" if data["total"] else "N/A"
            lines.append(f"{bucket:>12} {data['total']:>7} {data['wins']:>5} {wr:>9}")
    else:
        lines.append("No resolved trades yet for calibration analysis.")

    lines.append("")

    # Direction breakdown
    lines.append("─" * 56)
    lines.append("DIRECTION BREAKDOWN")
    lines.append("─" * 56)

    for dir_name in ("long", "short"):
        dir_trades = [r for r in results if r["direction"] == dir_name]
        dir_resolved = [r for r in dir_trades if r["status"] in ("win", "loss")]
        dir_wins = sum(1 for r in dir_resolved if r["status"] == "win")
        dir_total = len(dir_resolved)
        dir_wr = f"{dir_wins/dir_total*100:.0f}%" if dir_total else "N/A"
        dir_pnl = sum(r["pnl_usd"] for r in dir_resolved)
        lines.append(f"{dir_name.upper()}: {len(dir_trades)} trades, {dir_wins}/{dir_total} resolved wins ({dir_wr}), P&L: {'+'if dir_pnl>=0 else ''}${dir_pnl:,.2f}")

    lines.append("")
    lines.append("=" * 56)
    lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Data source: routine_raw_results.json (Claude routines UI)")
    lines.append(f"Position sizing: ${POSITION_SIZE_USD} per trade")
    lines.append("=" * 56)

    return "\n".join(lines)


def save_markdown_report(results: list[dict], report_text: str, output_path: Path):
    """Save the report as a markdown file."""
    md = []
    md.append("# Stock Swing Routine — Accuracy Report\n")
    md.append(f"**Period:** April 17–24, 2026 (12 routine sessions)  ")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Data source:** `routine_raw_results.json` (Claude routines UI)  ")
    md.append(f"**Position sizing:** ${POSITION_SIZE_USD} per trade\n")
    md.append("```")
    md.append(report_text)
    md.append("```\n")

    # Add a summary section
    wins = sum(1 for r in results if r["status"] == "win")
    losses = sum(1 for r in results if r["status"] == "loss")
    opens = sum(1 for r in results if r["status"] == "open")
    not_triggered = sum(1 for r in results if r["status"] == "not_triggered")
    resolved = wins + losses
    win_rate = wins / resolved * 100 if resolved else 0
    realized_pnl = sum(r["pnl_usd"] for r in results if r["status"] in ("win", "loss"))

    md.append("## Summary\n")
    md.append(f"- **Win rate:** {win_rate:.1f}% ({wins} wins / {losses} losses)")
    md.append(f"- **Open trades:** {opens}")
    md.append(f"- **Not triggered:** {not_triggered}")
    md.append(f"- **Realized P&L:** {'+'if realized_pnl>=0 else ''}${realized_pnl:,.2f}\n")

    md.append("## Data Sources\n")
    md.append("Extracted from 12 Claude routine sessions via Playwright MCP scraping.")
    md.append("")

    output_path.write_text("\n".join(md))
    print(f"\nMarkdown report saved to: {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────


def main():
    print("Loading trade recommendations from GitHub branches...\n")
    all_trades = load_all_runs()
    print(f"  Found {len(all_trades)} actionable trades (before dedup)\n")

    trades = deduplicate_trades(all_trades)
    print(f"  After dedup: {len(trades)} unique trades\n")

    # Collect unique tickers and date range
    tickers = sorted(set(t["ticker"] for t in trades))
    min_date = min(t["rec_date"] for t in trades)
    max_date = datetime.now().date()

    print(f"  Tickers: {', '.join(tickers)}")
    print(f"  Date range: {min_date} to {max_date}\n")

    # Fetch OHLC for all tickers
    print("Fetching price data from yfinance...\n")
    ohlc_cache = {}
    for ticker in tickers:
        bars = fetch_ohlc(ticker, min_date, max_date)
        ohlc_cache[ticker] = bars
        if bars:
            print(f"  {ticker}: {len(bars)} bars ({bars[0]['date']} to {bars[-1]['date']})")
        else:
            print(f"  {ticker}: NO DATA")

    print()

    # Evaluate each trade
    print("Evaluating trades...\n")
    results = []
    for trade in trades:
        bars = ohlc_cache.get(trade["ticker"], [])
        result = evaluate_trade(trade, bars)
        results.append(result)
        status_emoji = {"win": "W", "loss": "L", "open": "O", "not_triggered": "-"}
        print(f"  [{status_emoji.get(result['status'], '?')}] {trade['run_date']} {trade['ticker']:>5} "
              f"{trade['direction']:<5} entry=${trade['entry_price']:.2f} → {result['status']}")

    print()

    # Generate and print report
    report_text = format_report(results)
    print(report_text)

    # Save markdown
    output_path = Path(__file__).parent / "swing_routine_report.md"
    save_markdown_report(results, report_text, output_path)


if __name__ == "__main__":
    main()
