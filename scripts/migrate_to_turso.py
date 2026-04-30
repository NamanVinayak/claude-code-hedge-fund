"""Migrate local tracker SQLite rows into Turso.

This is intentionally one-way: tracker/tracker.db is read through the existing
SQLAlchemy models, while Turso is written through tracker.turso_client.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tracker.db import DailySummary, Session, Trade
from tracker.turso_client import create_all_tables, get_all_trades, get_connection, insert_trade


TRADE_FIELDS = [
    "run_id",
    "mode",
    "ticker",
    "direction",
    "quantity",
    "entry_price",
    "target_price",
    "target_price_2",
    "stop_loss",
    "confidence",
    "timeframe",
    "entry_order_id",
    "stop_order_id",
    "target_order_id",
    "status",
    "entry_fill_price",
    "exit_fill_price",
    "pnl",
    "created_at",
    "entered_at",
    "closed_at",
    "raw_decision",
]

DAILY_SUMMARY_FIELDS = [
    "date",
    "total_trades",
    "wins",
    "losses",
    "total_pnl",
    "open_positions",
]


def trade_to_dict(trade: Trade) -> dict[str, Any]:
    """Convert a local SQLAlchemy Trade row to the Turso trade payload."""
    out = {field: _to_text_if_datetime(getattr(trade, field)) for field in TRADE_FIELDS}
    out["last_checked_at"] = _to_text_if_datetime(getattr(trade, "last_checked_at", None))
    return out


def daily_summary_to_dict(summary: DailySummary) -> dict[str, Any]:
    """Convert a local SQLAlchemy DailySummary row to plain DB values."""
    return {field: getattr(summary, field) for field in DAILY_SUMMARY_FIELDS}


def migrate_trades(session) -> tuple[int, int]:
    existing = {(row["run_id"], row["ticker"]) for row in get_all_trades()}

    migrated = 0
    skipped = 0
    for trade in session.query(Trade).order_by(Trade.id).all():
        key = (trade.run_id, trade.ticker)
        if key in existing:
            skipped += 1
            continue

        insert_trade(trade_to_dict(trade))
        existing.add(key)
        migrated += 1

    return migrated, skipped


def migrate_daily_summaries(session) -> tuple[int, int]:
    summaries = session.query(DailySummary).order_by(DailySummary.id).all()
    if not summaries:
        return 0, 0

    conn = get_connection()
    try:
        result = conn.execute("SELECT date FROM daily_summary")
        existing_dates = {_first_column(row) for row in result.fetchall()}

        migrated = 0
        skipped = 0
        for summary in summaries:
            payload = daily_summary_to_dict(summary)
            if payload["date"] in existing_dates:
                skipped += 1
                continue

            columns = DAILY_SUMMARY_FIELDS
            placeholders = ", ".join("?" for _ in columns)
            conn.execute(
                f"INSERT INTO daily_summary ({', '.join(columns)}) VALUES ({placeholders})",
                tuple(payload[column] for column in columns),
            )
            existing_dates.add(payload["date"])
            migrated += 1

        if hasattr(conn, "commit"):
            conn.commit()
        return migrated, skipped
    finally:
        conn.close()


def main() -> None:
    load_dotenv()
    create_all_tables()

    session = Session()
    try:
        migrated, skipped = migrate_trades(session)
        summary_migrated, summary_skipped = migrate_daily_summaries(session)
    finally:
        session.close()

    print(f"Migrated {migrated} trades, skipped {skipped} duplicates")
    print(f"Migrated {summary_migrated} daily summaries, skipped {summary_skipped} duplicates")


def _to_text_if_datetime(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _first_column(row) -> Any:
    if isinstance(row, dict):
        return next(iter(row.values()))
    return row[0]


if __name__ == "__main__":
    main()
