"""Nightly wiki daily update — fetches today's closed trades from Turso and
builds a context bundle for the wiki_daily_lesson_writer agent.

Run by the wiki-daily-update skill (nightly cron at 10pm ET).
Exits cleanly with code 0 if no trades closed today.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

import sys as _sys
if str(ROOT) not in _sys.path:
    _sys.path.insert(0, str(ROOT))


def _read_wiki_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "NOT FOUND"


def main() -> None:
    from tracker.turso_client import get_recent_trade_history

    closed_trades = get_recent_trade_history(days=1)

    close_statuses = {"target_hit", "stop_hit", "expired"}
    closed_trades = [t for t in closed_trades if t.get("status") in close_statuses]

    if not closed_trades:
        print("No trades closed today. Wiki update skipped.")
        sys.exit(0)

    summary_parts = [f"{t['ticker']} {t['status']}" for t in closed_trades]
    print(f"{len(closed_trades)} trade(s) closed today: {', '.join(summary_parts)}")

    tickers = list({t["ticker"] for t in closed_trades})
    wiki_pages: dict[str, dict[str, str]] = {}
    for ticker in tickers:
        ticker_dir = ROOT / "wiki" / "tickers" / ticker
        wiki_pages[ticker] = {
            "thesis": _read_wiki_file(ticker_dir / "thesis.md"),
            "trades": _read_wiki_file(ticker_dir / "trades.md"),
        }

    bundle = {
        "closed_trades": closed_trades,
        "wiki_pages": wiki_pages,
        "macro_regime": _read_wiki_file(ROOT / "wiki" / "macro" / "regime.md"),
        "lessons_current": _read_wiki_file(ROOT / "wiki" / "meta" / "lessons.md"),
    }

    runs_dir = ROOT / "runs"
    runs_dir.mkdir(exist_ok=True)
    today = date.today().isoformat()
    bundle_path = runs_dir / f"wiki_daily_{today}.json"
    bundle_path.write_text(json.dumps(bundle, indent=2, default=str), encoding="utf-8")

    print(f"Bundle written to {bundle_path}")


if __name__ == "__main__":
    main()
