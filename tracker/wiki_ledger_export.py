"""Export Turso trade ledger as JSON for the wiki curator.

The wiki curator agent has historically inferred trade history from
indirect signals (signals_combined.json portfolio state, decisions.json
intent), which produced hallucinated positions when a decision existed
but was never ingested. This module dumps the canonical Turso ledger to
runs/<run_id>/trade_ledger.json so the curator has authoritative ground
truth for "what trades actually exist."

Usage:
    python -m tracker.wiki_ledger_export --run-id 20260501_124529 --tickers NVDA,AMD
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from tracker.turso_client import (
    get_all_trades,
    get_open_positions,
    get_pending_trades,
    get_recent_trade_history,
)


def export_ledger(run_id: str, tickers: list[str]) -> Path:
    open_positions = get_open_positions()
    pending_orders = get_pending_trades()
    recent_closures = get_recent_trade_history(days=30)
    all_trades = get_all_trades()

    per_ticker = {
        t: [row for row in all_trades if row.get("ticker") == t]
        for t in tickers
    }

    payload = {
        "run_id": run_id,
        "tickers_in_scope": tickers,
        "open_positions": open_positions,
        "pending_orders": pending_orders,
        "recent_closures_30d": recent_closures,
        "per_ticker_history": per_ticker,
        "totals": {
            "open_position_count": len(open_positions),
            "pending_order_count": len(pending_orders),
            "recent_closure_count": len(recent_closures),
            "lifetime_trade_count": len(all_trades),
        },
    }

    out_dir = Path("runs") / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "trade_ledger.json"
    out_path.write_text(json.dumps(payload, indent=2, default=str))
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Dump Turso ledger for the wiki curator.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--tickers", required=True, help="Comma-separated tickers in scope")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    out_path = export_ledger(args.run_id, tickers)
    payload = json.loads(out_path.read_text())
    print(f"Wrote {out_path}")
    print(
        f"  open={payload['totals']['open_position_count']} "
        f"pending={payload['totals']['pending_order_count']} "
        f"recent_closures={payload['totals']['recent_closure_count']} "
        f"lifetime={payload['totals']['lifetime_trade_count']}"
    )
    for t in tickers:
        n = len(payload["per_ticker_history"].get(t, []))
        print(f"  {t}: {n} historical trade(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
