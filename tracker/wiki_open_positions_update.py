"""Nightly open-position context bundle — fetches current open and pending
trades from Turso, snapshots current price + derived fields, and writes a
bundle for the wiki_open_position_writer agent.

Sibling of `tracker/wiki_daily_update.py`. Different scope:
  - daily_update     → trades that closed today (post-mortems → lessons.md)
  - open_positions   → trades currently in flight (snapshot → open_positions.md)

Run by the wiki-maintenance skill after the daily lesson writer.
Exits cleanly with code 0 if the portfolio is empty.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent

import sys as _sys
if str(ROOT) not in _sys.path:
    _sys.path.insert(0, str(ROOT))


def _parse_iso(value) -> datetime | None:
    if not value:
        return None
    try:
        s = str(value).replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _days_between(start: datetime | None, end: datetime) -> int | None:
    if start is None:
        return None
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return max(0, (end.date() - start.date()).days)


def _unrealized_pnl(direction: str, entry: float | None, current: float | None, qty: int | None) -> float | None:
    if entry is None or current is None or qty is None:
        return None
    if direction == "long":
        return round((current - entry) * qty, 2)
    if direction == "short":
        return round((entry - current) * qty, 2)
    return None


def _unrealized_pnl_pct(direction: str, entry: float | None, current: float | None) -> float | None:
    if entry is None or current is None or entry == 0:
        return None
    if direction == "long":
        return round((current - entry) / entry * 100, 2)
    if direction == "short":
        return round((entry - current) / entry * 100, 2)
    return None


def _enrich(trade: dict, current_price: float | None, now: datetime) -> dict:
    """Add snapshot fields. Pure data — no editorial framing."""
    direction = trade.get("direction") or ""
    entry = trade.get("entry_fill_price") or trade.get("entry_price")
    qty = trade.get("quantity")
    stop = trade.get("stop_loss")
    target = trade.get("target_price")
    entered_at = _parse_iso(trade.get("entered_at"))
    created_at = _parse_iso(trade.get("created_at"))

    return {
        "id": trade.get("id"),
        "run_id": trade.get("run_id"),
        "ticker": trade.get("ticker"),
        "direction": direction,
        "quantity": qty,
        "status": trade.get("status"),
        "entry_price": entry,
        "current_price": current_price,
        "stop_loss": stop,
        "target_price": target,
        "target_price_2": trade.get("target_price_2"),
        "timeframe": trade.get("timeframe"),
        "confidence_at_entry": trade.get("confidence"),
        "entered_at": str(trade.get("entered_at") or ""),
        "created_at": str(trade.get("created_at") or ""),
        "days_held": _days_between(entered_at or created_at, now),
        "unrealized_pnl_dollars": _unrealized_pnl(direction, entry, current_price, qty),
        "unrealized_pnl_pct": _unrealized_pnl_pct(direction, entry, current_price),
    }


def main() -> None:
    from tracker.turso_client import get_open_positions, get_pending_trades
    from ai_hedge.data.api import get_current_price

    open_positions = get_open_positions()
    pending = get_pending_trades()

    if not open_positions and not pending:
        print("Portfolio is empty (no open or pending positions). Wiki update skipped.")
        sys.exit(0)

    print(f"{len(open_positions)} open, {len(pending)} pending")

    tickers = list({t["ticker"] for t in open_positions + pending if t.get("ticker")})
    prices: dict[str, float | None] = {}
    for ticker in tickers:
        try:
            prices[ticker] = get_current_price(ticker)
        except Exception as e:
            print(f"  warning: price fetch failed for {ticker}: {e}", file=sys.stderr)
            prices[ticker] = None

    now = datetime.now(timezone.utc)

    bundle = {
        "snapshot_at": now.isoformat(),
        "snapshot_at_pt": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
        "open_positions": [_enrich(t, prices.get(t["ticker"]), now) for t in open_positions],
        "pending_orders": [_enrich(t, prices.get(t["ticker"]), now) for t in pending],
    }

    runs_dir = ROOT / "runs"
    runs_dir.mkdir(exist_ok=True)
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    bundle_path = runs_dir / f"wiki_open_positions_{today}.json"
    bundle_path.write_text(json.dumps(bundle, indent=2, default=str), encoding="utf-8")

    print(f"Bundle written to {bundle_path}")


if __name__ == "__main__":
    main()
