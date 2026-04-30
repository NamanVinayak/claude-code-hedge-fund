"""Tests for local tracker.db to Turso migration helpers."""
from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace


def test_trade_to_dict_serializes_local_trade_without_local_id():
    from scripts.migrate_to_turso import trade_to_dict

    trade = SimpleNamespace(
        id=7,
        run_id="run-1",
        mode="swing",
        ticker="AAPL",
        direction="long",
        quantity=3,
        entry_price=190.5,
        target_price=210.0,
        target_price_2=None,
        stop_loss=180.0,
        confidence=72,
        timeframe="2-20 days",
        entry_order_id=None,
        stop_order_id=None,
        target_order_id=None,
        status="entered",
        entry_fill_price=191.0,
        exit_fill_price=None,
        pnl=None,
        created_at=datetime(2026, 4, 29, 12, 0, 0),
        entered_at=datetime(2026, 4, 29, 12, 5, 0),
        closed_at=None,
        raw_decision='{"ticker": "AAPL"}',
    )

    out = trade_to_dict(trade)

    assert "id" not in out
    assert out["run_id"] == "run-1"
    assert out["ticker"] == "AAPL"
    assert out["created_at"] == "2026-04-29T12:00:00"
    assert out["entered_at"] == "2026-04-29T12:05:00"
    assert out["last_checked_at"] is None


def test_daily_summary_to_dict_serializes_summary_row():
    from scripts.migrate_to_turso import daily_summary_to_dict

    row = SimpleNamespace(
        id=2,
        date="2026-04-29",
        total_trades=4,
        wins=3,
        losses=1,
        total_pnl=125.5,
        open_positions=2,
    )

    out = daily_summary_to_dict(row)

    assert out == {
        "date": "2026-04-29",
        "total_trades": 4,
        "wins": 3,
        "losses": 1,
        "total_pnl": 125.5,
        "open_positions": 2,
    }
