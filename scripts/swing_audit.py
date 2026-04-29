#!/usr/bin/env python3
"""
Read scripts/all_swing_predictions.json, evaluate every prediction against
real market data via yfinance, and emit two markdown reports:
  - scripts/swing_audit_stock.md
  - scripts/swing_audit_crypto.md

For each prediction we use 1-hour bars (matching tracker/backtest.py) so
"did entry get hit?" is answered at intraday precision. Bars are filtered
to those AFTER rec_time_utc (the actual moment the model emitted the trade).
"""

import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
INPUT = SCRIPTS / "all_swing_predictions.json"
POSITION_SIZE_USD = 500.0

# Allow `python scripts/swing_audit.py` to import from tracker/.
sys.path.insert(0, str(ROOT))
from tracker.spy_benchmark import compute_spy_benchmark, format_headline  # noqa: E402


# ── Price fetching ─────────────────────────────────────────────────────────


def fetch_hourly(ticker: str, start_date: str, end_date: str) -> list[dict]:
    """1h bars between start and end (UTC). yfinance allows 1h up to 730 days."""
    tk = yf.Ticker(ticker)
    df = tk.history(start=start_date, end=end_date, interval="1h")
    if df.empty:
        return []
    bars = []
    for idx, row in df.iterrows():
        ts = idx.to_pydatetime()
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        bars.append({
            "ts": ts,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        })
    return bars


def get_current_price(ticker: str, fallback: float | None) -> float | None:
    try:
        p = yf.Ticker(ticker).fast_info.last_price
        if p and p == p:  # not None and not NaN
            return float(p)
    except Exception:
        pass
    return fallback


# ── Trade evaluation ───────────────────────────────────────────────────────


def evaluate(trade: dict, bars: list[dict]) -> dict:
    """Return a copy of `trade` with status, exit_dt, pnl_pct, pnl_usd added."""
    out = dict(trade)
    out.update({"status": "not_triggered", "exit_dt": None, "exit_price": None,
                "pnl_pct": 0.0, "pnl_usd": 0.0})

    rec_dt = datetime.fromisoformat(trade["rec_time_utc"].replace("Z", "+00:00"))
    direction = trade["direction"]
    entry, target, stop = trade["entry"], trade["target"], trade["stop"]

    future = [b for b in bars if b["ts"] > rec_dt]
    if not future:
        out["status"] = "no_data"
        return out

    entry_idx = None
    for i, b in enumerate(future):
        if direction == "long" and b["low"] <= entry:
            entry_idx = i
            break
        if direction == "short" and b["high"] >= entry:
            entry_idx = i
            break

    if entry_idx is None:
        return out  # not_triggered

    for b in future[entry_idx:]:
        if direction == "long":
            tgt_hit = b["high"] >= target
            stp_hit = b["low"] <= stop
        else:
            tgt_hit = b["low"] <= target
            stp_hit = b["high"] >= stop

        if tgt_hit and stp_hit:
            # Both in the same bar: if open already past target it's a win, else loss (conservative)
            if direction == "long":
                if b["open"] >= target:
                    out["status"], out["exit_price"] = "win", target
                else:
                    out["status"], out["exit_price"] = "loss", stop
            else:
                if b["open"] <= target:
                    out["status"], out["exit_price"] = "win", target
                else:
                    out["status"], out["exit_price"] = "loss", stop
            out["exit_dt"] = b["ts"].isoformat()
            break
        if tgt_hit:
            out["status"], out["exit_price"], out["exit_dt"] = "win", target, b["ts"].isoformat()
            break
        if stp_hit:
            out["status"], out["exit_price"], out["exit_dt"] = "loss", stop, b["ts"].isoformat()
            break

    if out["status"] == "not_triggered":
        out["status"] = "open"
        last = future[-1]
        out["exit_price"] = last["close"]
        out["exit_dt"] = last["ts"].isoformat()

    if out["status"] in ("win", "loss", "open"):
        if direction == "long":
            out["pnl_pct"] = (out["exit_price"] - entry) / entry * 100
        else:
            out["pnl_pct"] = (entry - out["exit_price"]) / entry * 100
        out["pnl_usd"] = POSITION_SIZE_USD * out["pnl_pct"] / 100

    return out


# ── Markdown formatting ────────────────────────────────────────────────────


def fmt_money(v: float) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}${v:,.2f}"


def fmt_pct(v: float) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"


def build_report(asset_label: str, results: list[dict]) -> str:
    if not results:
        return f"# {asset_label} Swing Audit\n\n_No predictions found for this asset class._\n"

    wins = [r for r in results if r["status"] == "win"]
    losses = [r for r in results if r["status"] == "loss"]
    opens = [r for r in results if r["status"] == "open"]
    not_trig = [r for r in results if r["status"] == "not_triggered"]
    no_data = [r for r in results if r["status"] == "no_data"]

    resolved = len(wins) + len(losses)
    win_rate = len(wins) / resolved * 100 if resolved else 0.0
    triggered = resolved + len(opens)
    eligible = len(results) - len(no_data)
    entry_rate = (triggered / eligible * 100) if eligible else 0.0

    realized = sum(r["pnl_usd"] for r in wins + losses)
    unrealized = sum(r["pnl_usd"] for r in opens)
    deployed = POSITION_SIZE_USD * triggered
    net_pnl = realized + unrealized
    net_pct = (net_pnl / deployed * 100) if deployed else 0.0

    # ── SPY benchmark ──────────────────────────────────────────────────────
    filled_dates = [r["rec_date"] for r in results
                    if r["status"] in ("win", "loss", "open")]
    spy_line = ""
    if filled_dates and deployed > 0:
        spy_start_date = min(filled_dates)
        spy_end_date = datetime.now(timezone.utc).date().isoformat()
        spy_bench = compute_spy_benchmark(spy_start_date, spy_end_date, deployed)
        is_crypto = bool(results[0].get("is_crypto"))
        caveat = ("Note: SPY is not a meaningful benchmark for crypto; "
                  "shown for context only.") if is_crypto else None
        spy_line = format_headline(net_pnl, net_pct, spy_bench, caveat=caveat)

    md = []
    md.append(f"# {asset_label} Swing Audit\n")
    if spy_line:
        md.append(spy_line + "\n")
    md.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
              f"position size ${POSITION_SIZE_USD:,.0f}/trade · 1-hour bars._\n")

    md.append("## Plain-English summary\n")
    md.append(f"- **Total predictions:** {len(results)}")
    md.append(f"- **Entry actually filled:** {triggered} of {eligible} ({entry_rate:.1f}%)")
    md.append(f"- **Wins:** {len(wins)} · **Losses:** {len(losses)} · **Still open:** {len(opens)} "
              f"· **Never entered:** {len(not_trig)}"
              + (f" · **No price data:** {len(no_data)}" if no_data else ""))
    md.append(f"- **Win rate (resolved):** {win_rate:.1f}% ({len(wins)}W / {len(losses)}L)")
    md.append(f"- **Realized P&L:** {fmt_money(realized)}")
    md.append(f"- **Unrealized P&L (open):** {fmt_money(unrealized)}")
    md.append(f"- **Net P&L:** {fmt_money(realized + unrealized)}")
    md.append(f"- **Capital deployed:** ${deployed:,.0f}\n")

    # Day-by-day
    md.append("## Day-by-day\n")
    md.append("| Date | Total | Filled | Wins | Losses | Open | Missed | Win rate | P&L |")
    md.append("|------|------:|------:|-----:|-------:|-----:|------:|---------:|----:|")
    by_date: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_date[r["rec_date"]].append(r)
    for date in sorted(by_date):
        rs = by_date[date]
        w = sum(1 for r in rs if r["status"] == "win")
        l = sum(1 for r in rs if r["status"] == "loss")
        o = sum(1 for r in rs if r["status"] == "open")
        n = sum(1 for r in rs if r["status"] == "not_triggered")
        nd = sum(1 for r in rs if r["status"] == "no_data")
        filled = w + l + o
        eligible_d = len(rs) - nd
        wr_d = w / (w + l) * 100 if (w + l) else None
        pnl_d = sum(r["pnl_usd"] for r in rs if r["status"] in ("win", "loss", "open"))
        wr_str = f"{wr_d:.0f}%" if wr_d is not None else "—"
        md.append(f"| {date} | {len(rs)} | {filled}/{eligible_d} | {w} | {l} | {o} | {n} "
                  f"| {wr_str} | {fmt_money(pnl_d)} |")
    md.append("")

    # Per-ticker
    md.append("## Per-ticker\n")
    md.append("| Ticker | Trades | Wins | Losses | Open | Missed | Win rate | P&L |")
    md.append("|--------|------:|-----:|-------:|-----:|------:|---------:|----:|")
    by_tkr: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_tkr[r["ticker"]].append(r)
    for tkr in sorted(by_tkr):
        rs = by_tkr[tkr]
        w = sum(1 for r in rs if r["status"] == "win")
        l = sum(1 for r in rs if r["status"] == "loss")
        o = sum(1 for r in rs if r["status"] == "open")
        n = sum(1 for r in rs if r["status"] == "not_triggered")
        wr_t = w / (w + l) * 100 if (w + l) else None
        pnl_t = sum(r["pnl_usd"] for r in rs if r["status"] in ("win", "loss", "open"))
        wr_str = f"{wr_t:.0f}%" if wr_t is not None else "—"
        md.append(f"| {tkr} | {len(rs)} | {w} | {l} | {o} | {n} | {wr_str} | {fmt_money(pnl_t)} |")
    md.append("")

    # Confidence calibration
    resolved_trades = [r for r in results if r["status"] in ("win", "loss")]
    if resolved_trades:
        md.append("## Confidence calibration\n")
        md.append("Does a 70%-confidence trade actually win 70% of the time?\n")
        md.append("| Confidence bucket | Trades | Wins | Win rate |")
        md.append("|------------------:|------:|-----:|---------:|")
        buckets: dict[str, dict] = defaultdict(lambda: {"wins": 0, "total": 0})
        for r in resolved_trades:
            c = r.get("confidence") or 0
            try:
                c = int(c)
            except (TypeError, ValueError):
                c = 0
            bk = f"{(c // 10) * 10}-{(c // 10) * 10 + 9}%"
            buckets[bk]["total"] += 1
            if r["status"] == "win":
                buckets[bk]["wins"] += 1
        for bk in sorted(buckets):
            b = buckets[bk]
            wr_b = b["wins"] / b["total"] * 100 if b["total"] else 0
            md.append(f"| {bk} | {b['total']} | {b['wins']} | {wr_b:.0f}% |")
        md.append("")

    # By source
    md.append("## Source split\n")
    md.append("Which input source contributed each prediction (after dedup):\n")
    md.append("| Source | Count |")
    md.append("|--------|------:|")
    by_src: dict[str, int] = defaultdict(int)
    for r in results:
        by_src[r["source"]] += 1
    for src, cnt in sorted(by_src.items()):
        md.append(f"| {src} | {cnt} |")
    md.append("")

    # Detailed log
    md.append("## Detailed trade log\n")
    md.append("| Date | Ticker | Dir | Entry | Stop | Target | Status | P&L | Conf | Source |")
    md.append("|------|--------|-----|------:|-----:|-------:|--------|----:|-----:|--------|")
    for r in sorted(results, key=lambda x: (x["rec_date"], x["ticker"])):
        st = r["status"]
        if st == "open" and r["exit_price"]:
            st_disp = f"open @{r['exit_price']:.2f}"
        elif st in ("win", "loss") and r.get("exit_dt"):
            st_disp = f"{st} {r['exit_dt'][:10]}"
        else:
            st_disp = st
        pnl = fmt_money(r["pnl_usd"]) if st in ("win", "loss", "open") else "—"
        conf = f"{r['confidence']}%" if r.get("confidence") else "—"
        md.append(f"| {r['rec_date']} | {r['ticker']} | {r['direction']} "
                  f"| ${r['entry']:.2f} | ${r['stop']:.2f} | ${r['target']:.2f} "
                  f"| {st_disp} | {pnl} | {conf} | {r['source']} |")
    md.append("")

    return "\n".join(md)


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    preds = json.loads(INPUT.read_text())
    print(f"Loaded {len(preds)} predictions from {INPUT.name}")

    today = datetime.now(timezone.utc).date()
    earliest = min(datetime.fromisoformat(p["rec_date"]).date() for p in preds)
    fetch_start = (earliest - timedelta(days=1)).isoformat()
    fetch_end = (today + timedelta(days=2)).isoformat()

    tickers = sorted({p["ticker"] for p in preds})
    print(f"Fetching 1h bars for {len(tickers)} tickers, {fetch_start} -> {fetch_end}")
    bars_cache: dict[str, list[dict]] = {}
    for i, t in enumerate(tickers, 1):
        try:
            bars_cache[t] = fetch_hourly(t, fetch_start, fetch_end)
            print(f"  [{i}/{len(tickers)}] {t}: {len(bars_cache[t])} bars")
        except Exception as e:
            print(f"  [{i}/{len(tickers)}] {t}: ERROR {e}")
            bars_cache[t] = []
        time.sleep(0.2)

    results = [evaluate(p, bars_cache.get(p["ticker"], [])) for p in preds]

    stock = [r for r in results if not r["is_crypto"]]
    crypto = [r for r in results if r["is_crypto"]]
    print(f"Stock: {len(stock)}  Crypto: {len(crypto)}")

    (SCRIPTS / "swing_audit_stock.md").write_text(build_report("Stock", stock))
    (SCRIPTS / "swing_audit_crypto.md").write_text(build_report("Crypto", crypto))
    print("Wrote swing_audit_stock.md and swing_audit_crypto.md")


if __name__ == "__main__":
    main()
