"""Tests for the Turso tracker client."""
from __future__ import annotations

import json


class FakeResult:
    def __init__(self, rows=None, columns=None, last_insert_rowid=None):
        self.rows = rows or []
        self.columns = columns or []
        self.last_insert_rowid = last_insert_rowid


class FakeConnection:
    def __init__(self):
        self.statements = []
        self.closed = False
        self.table = [
            (
                1,
                "run-1",
                "swing",
                "AAPL",
                "long",
                3,
                190.5,
                210.0,
                None,
                180.0,
                72,
                "2-20 days",
                None,
                None,
                None,
                "entered",
                191.0,
                None,
                None,
                "2026-04-29T12:00:00",
                "2026-04-29T12:05:00",
                None,
                json.dumps({"ticker": "AAPL"}),
                None,
            ),
            (
                2,
                "run-2",
                "daytrade",
                "MSFT",
                "short",
                2,
                405.0,
                390.0,
                None,
                412.0,
                61,
                "intraday",
                None,
                None,
                None,
                "pending",
                None,
                None,
                None,
                "2026-04-29T12:10:00",
                None,
                None,
                json.dumps({"ticker": "MSFT"}),
                None,
            ),
        ]
        self.columns = [
            "id",
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
            "last_checked_at",
        ]

    def execute(self, sql, params=None):
        if params is not None and not isinstance(params, tuple):
            raise TypeError("fake libsql requires tuple params")
        self.statements.append((sql, params))
        normalized = " ".join(sql.lower().split())
        if normalized.startswith("select * from trades"):
            if "where status = ?" in normalized:
                rows = [row for row in self.table if row[15] == params[0]]
            else:
                rows = list(self.table)
            return FakeResult(rows, self.columns)
        if normalized.startswith("insert into trades"):
            return FakeResult(last_insert_rowid=42)
        if normalized.startswith("insert into fills"):
            return FakeResult(last_insert_rowid=99)
        return FakeResult()

    def close(self):
        self.closed = True


def test_create_all_tables_creates_required_schema(monkeypatch):
    from tracker import turso_client

    fake = FakeConnection()
    monkeypatch.setattr(turso_client, "get_connection", lambda: fake)

    turso_client.create_all_tables()

    sql = "\n".join(statement for statement, _ in fake.statements)
    assert "CREATE TABLE IF NOT EXISTS trades" in sql
    assert "last_checked_at TEXT" in sql
    assert "CREATE TABLE IF NOT EXISTS daily_summary" in sql
    assert "CREATE TABLE IF NOT EXISTS fills" in sql
    assert "CREATE TABLE IF NOT EXISTS pending_decisions" in sql
    assert fake.closed is True


def test_trade_queries_return_dicts_and_filter_by_status(monkeypatch):
    from tracker import turso_client

    monkeypatch.setattr(turso_client, "get_connection", lambda: FakeConnection())

    all_trades = turso_client.get_all_trades()
    open_positions = turso_client.get_open_positions()
    pending_trades = turso_client.get_pending_trades()

    assert [trade["ticker"] for trade in all_trades] == ["AAPL", "MSFT"]
    assert [trade["ticker"] for trade in open_positions] == ["AAPL"]
    assert [trade["ticker"] for trade in pending_trades] == ["MSFT"]
    assert open_positions[0]["status"] == "entered"


def test_insert_update_and_log_fill_use_parameterized_sql(monkeypatch):
    from tracker import turso_client

    fake = FakeConnection()
    monkeypatch.setattr(turso_client, "get_connection", lambda: fake)

    trade_id = turso_client.insert_trade(
        {
            "run_id": "run-3",
            "mode": "swing",
            "ticker": "NVDA",
            "direction": "long",
            "quantity": 1,
            "entry_price": 850.0,
        }
    )
    turso_client.update_trade(42, status="entered", entry_fill_price=851.0)
    fill_id = turso_client.log_fill(42, "entry_filled", 851.0, "2026-04-29T13:00:00", "entry crossed")

    assert trade_id == 42
    assert fill_id == 99
    update_sql, update_params = fake.statements[-2]
    assert update_sql == "UPDATE trades SET status = ?, entry_fill_price = ? WHERE id = ?"
    assert update_params == ("entered", 851.0, 42)
    assert "INSERT INTO fills" in fake.statements[-1][0]
