import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import json
import glob
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

from tracker.turso_client import get_all_trades, get_open_positions, get_pending_trades

def get_current_prices(tickers):
    if not tickers:
        return {}
    try:
        data = yf.download(" ".join(tickers), period="1d", progress=False)['Close']
        if data.empty:
            return {}
        prices = {}
        if len(tickers) == 1:
            if not data.isna().iloc[-1]:
                prices[tickers[0]] = float(data.iloc[-1])
        else:
            for ticker in tickers:
                if ticker in data.columns and not data[ticker].isna().iloc[-1]:
                    prices[ticker] = float(data[ticker].iloc[-1])
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

def calculate_next_update():
    now = datetime.now(ZoneInfo("America/Vancouver"))
    minutes = now.minute
    next_5 = ((minutes // 5) + 1) * 5
    return next_5 - minutes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dashboard/dist")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Initialize Jinja2
    env = Environment(loader=FileSystemLoader("dashboard/templates"))
    base_context = {
        "last_updated": datetime.now(ZoneInfo("America/Vancouver")).strftime("%I:%M %p"),
        "next_update_min": calculate_next_update()
    }

    # Fetch all open positions
    open_positions_data = get_open_positions()
    open_tickers = list(set([p['ticker'] for p in open_positions_data]))
    live_prices = get_current_prices(open_tickers)

    positions = []
    for p in open_positions_data:
        ticker = p['ticker']
        curr_price = live_prices.get(ticker, float(p.get('entry_fill_price') or p.get('entry_price') or 0))
        
        # Calculate PnL
        entry = float(p.get('entry_fill_price') or p.get('entry_price') or 0)
        qty = float(p['quantity'])
        direction = p['direction'].lower()
        
        pnl_dollar = 0
        pnl_percent = 0
        if entry > 0:
            if direction == 'long':
                pnl_dollar = (curr_price - entry) * qty
                pnl_percent = (curr_price - entry) / entry * 100
            else:
                pnl_dollar = (entry - curr_price) * qty
                pnl_percent = (entry - curr_price) / entry * 100
            
        # Target/Stop RR
        rr = "N/A"
        try:
            target = float(p['target_price'])
            stop = float(p['stop_loss'])
            risk = abs(entry - stop)
            reward = abs(target - entry)
            if risk > 0:
                rr = f"1:{reward/risk:.1f}"
        except:
            pass

        # Days held
        days_held = 0
        if p.get('entered_at'):
            try:
                # 'entered_at' might be ISO format
                entered = datetime.fromisoformat(p['entered_at'].replace('Z', '+00:00'))
                days_held = (datetime.now(ZoneInfo("UTC")) - entered).days
            except:
                pass

        positions.append({
            "ticker": ticker,
            "direction": p['direction'],
            "entry_fill_price": entry,
            "current_price": curr_price,
            "pnl_dollar": pnl_dollar,
            "pnl_percent": pnl_percent,
            "stop_loss": p.get('stop_loss', '-'),
            "target_price": p.get('target_price', '-'),
            "rr": rr,
            "days_held": days_held
        })

    # Render index.html
    index_template = env.get_template("index.html")
    index_html = index_template.render(**base_context, title="Live Positions", positions=positions)
    with open(os.path.join(args.output, "index.html"), "w") as f:
        f.write(index_html)

    # Fetch today's runs — use UTC for folder matching (run folders are named in UTC)
    today_str = datetime.now(ZoneInfo("UTC")).strftime("%Y%m%d")
    run_folders = glob.glob(f"runs/{today_str}_*")
    runs = []
    for folder in sorted(run_folders, reverse=True):
        run_id = os.path.basename(folder)
        meta_path = os.path.join(folder, "metadata.json")
        exp_path = os.path.join(folder, "explanation.json")
        dec_path = os.path.join(folder, "decisions.json")
        
        mode = "unknown"
        tickers = []
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                try:
                    meta = json.load(f)
                    mode = meta.get("mode", "unknown")
                    tickers = meta.get("tickers", [])
                except:
                    pass
                
        summary = ""
        if os.path.exists(exp_path):
            with open(exp_path) as f:
                try:
                    exp = json.load(f)
                    summary = exp.get("tldr", exp.get("summary", exp.get("short_explanation", "")))
                except:
                    pass
                
        decisions = []
        if os.path.exists(dec_path):
            with open(dec_path) as f:
                try:
                    dec_data = json.load(f)
                    decs = dec_data.get("decisions", {})
                    for t, d in decs.items():
                        decisions.append({
                            "ticker": t,
                            "action": d.get("action", ""),
                            "confidence": d.get("confidence", ""),
                            "entry_price": d.get("entry_price"),
                            "target_price": d.get("target_price"),
                            "stop_loss": d.get("stop_loss"),
                        })
                except:
                    pass
                    
        runs.append({
            "run_id": run_id,
            "mode": mode,
            "tickers": tickers,
            "summary": summary,
            "decisions": decisions
        })

    # Build ticker status sets for the today page
    open_tickers = set(p['ticker'] for p in positions)
    pending_data = get_pending_trades()
    pending_tickers = set(t['ticker'] for t in pending_data)

    today_template = env.get_template("today.html")
    today_html = today_template.render(
        **base_context,
        title="Today's Decisions",
        runs=runs,
        open_tickers=open_tickers,
        pending_tickers=pending_tickers,
    )
    with open(os.path.join(args.output, "today.html"), "w") as f:
        f.write(today_html)

    # Closed trades
    all_trades = get_all_trades()
    closed_trades = [t for t in all_trades if t.get("status") in ("target_hit", "stop_hit", "expired", "closed")]
    # sort most recent first
    closed_trades.sort(key=lambda x: x.get("closed_at") or "", reverse=True)
    
    total_trades = len(closed_trades)
    wins = sum(1 for t in closed_trades if float(t.get("pnl", 0) or 0) > 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0
    total_pnl = sum(float(t.get("pnl", 0) or 0) for t in closed_trades)
    
    formatted_closed = []
    for t in closed_trades:
        entry = float(t.get('entry_fill_price') or t.get('entry_price') or 0)
        exit_price = float(t.get('exit_fill_price') or 0)
        pnl_dollar = float(t.get('pnl') or 0)
        pnl_percent = 0.0
        if entry > 0:
            if t.get('direction', 'long').lower() == 'long':
                pnl_percent = (exit_price - entry) / entry * 100 if exit_price else 0
            else:
                pnl_percent = (entry - exit_price) / entry * 100 if exit_price else 0
                
        formatted_closed.append({
            "ticker": t['ticker'],
            "status": t['status'],
            "entry_fill_price": entry,
            "exit_fill_price": exit_price,
            "pnl_dollar": pnl_dollar,
            "pnl_percent": pnl_percent,
            "entered_at": t.get('entered_at', '').split('T')[0] if t.get('entered_at') else '',
            "closed_at": t.get('closed_at', '').split('T')[0] if t.get('closed_at') else ''
        })

    closed_template = env.get_template("closed.html")
    closed_html = closed_template.render(**base_context, title="Closed Trades", trades=formatted_closed, total_trades=total_trades, win_rate=win_rate, total_pnl=total_pnl)
    with open(os.path.join(args.output, "closed.html"), "w") as f:
        f.write(closed_html)

    # All runs page
    all_run_folders = sorted(glob.glob("runs/*"), reverse=True)
    all_runs_list = []
    for folder in all_run_folders:
        run_id = os.path.basename(folder)
        # Parse timestamp from folder name (YYYYMMDD_HHMMSS)
        formatted_date = run_id
        try:
            dt = datetime.strptime(run_id, "%Y%m%d_%H%M%S").replace(tzinfo=ZoneInfo("UTC"))
            dt = dt.astimezone(ZoneInfo("America/Vancouver"))
            formatted_date = dt.strftime("%b %-d, %Y · %-I:%M %p PT")
        except ValueError:
            pass

        meta_path = os.path.join(folder, "metadata.json")
        dec_path = os.path.join(folder, "decisions.json")

        mode = "unknown"
        tickers = []
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                try:
                    meta = json.load(f)
                    mode = meta.get("mode", "unknown")
                    tickers = meta.get("tickers", [])
                except Exception:
                    pass

        decisions = []
        if os.path.exists(dec_path):
            with open(dec_path) as f:
                try:
                    dec_data = json.load(f)
                    decs = dec_data.get("decisions", {})
                    for t, d in decs.items():
                        decisions.append({
                            "ticker": t,
                            "action": d.get("action", ""),
                            "confidence": d.get("confidence", ""),
                            "entry_price": d.get("entry_price"),
                            "target_price": d.get("target_price"),
                            "stop_loss": d.get("stop_loss"),
                        })
                except Exception:
                    pass

        all_runs_list.append({
            "run_id": run_id,
            "formatted_date": formatted_date,
            "mode": mode,
            "tickers": tickers,
            "decisions": decisions,
        })

    runs_template = env.get_template("runs.html")
    runs_html = runs_template.render(
        **base_context,
        title="All Runs",
        runs=all_runs_list,
        open_tickers=open_tickers,
        pending_tickers=pending_tickers,
    )
    with open(os.path.join(args.output, "runs.html"), "w") as f:
        f.write(runs_html)

    # Per-ticker pages
    all_tickers = set()
    try:
        with open("tracker/watchlist.json") as f:
            watchlist = json.load(f)
            for schedule in watchlist.get("schedules", []):
                all_tickers.update(schedule.get("tickers", []))
    except:
        pass

    ticker_template = env.get_template("ticker.html")
    
    # get all runs to extract recent decisions per ticker
    all_runs = glob.glob("runs/*")
    all_runs.sort(reverse=True) # most recent first
    all_runs_data = []
    for r in all_runs[:50]: # limit to last 50 runs to save time
        run_id = os.path.basename(r)
        date_str = run_id.split('_')[0] if '_' in run_id else run_id
        dec_path = os.path.join(r, "decisions.json")
        if os.path.exists(dec_path):
            with open(dec_path) as f:
                try:
                    dec_data = json.load(f)
                    all_runs_data.append({"date": date_str, "decs": dec_data.get("decisions", {})})
                except:
                    pass

    pages_built = 4  # index, today, closed, runs
    for ticker in all_tickers:
        # Open position
        pos = next((p for p in positions if p["ticker"] == ticker), None)
        
        # Wiki thesis
        wiki_thesis = ""
        wiki_path = f"wiki/tickers/{ticker}/thesis.md"
        if os.path.exists(wiki_path):
            with open(wiki_path) as f:
                content = f.read()
                # Skip frontmatter if present
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                
                # Split into paragraphs and take first 3
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                selected = []
                for p in paragraphs:
                    if p.startswith("#") or p.startswith("!"): # Skip headers or images
                        continue
                    selected.append(p)
                    if len(selected) >= 3:
                        break
                
                wiki_thesis = "".join([f"<p>{p}</p>" for p in selected])

        # Recent decisions
        recent_decs = []
        for r in all_runs_data:
            if ticker in r["decs"]:
                d = r["decs"][ticker]
                recent_decs.append({
                    "date": r["date"],
                    "action": d.get("action", ""),
                    "confidence": d.get("confidence", ""),
                    "reason": d.get("reasoning", "")
                })
                if len(recent_decs) >= 3:
                    break

        # Recent closed trades
        ticker_closed = [t for t in formatted_closed if t["ticker"] == ticker][:5]

        ticker_html = ticker_template.render(
            **base_context, 
            title=ticker,
            ticker=ticker, 
            open_position=pos,
            wiki_thesis=wiki_thesis,
            decisions=recent_decs,
            closed_trades=ticker_closed
        )
        with open(os.path.join(args.output, f"{ticker}.html"), "w") as f:
            f.write(ticker_html)
        pages_built += 1

    print(f"Built {pages_built} pages -> {args.output}")

if __name__ == "__main__":
    main()