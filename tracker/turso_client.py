"""Turso cloud database client — HTTP API implementation.

Uses Turso's Hrana-over-HTTP protocol (POST /v2/pipeline) so no native
extension is needed. Works on any Python version. Only requires `requests`,
which is already a project dependency.

Public API mirrors a simple SQLite interface so the simulator and dashboard
can stay ignorant of the transport layer.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import requests
from dotenv import load_dotenv


TRADE_COLUMNS = [
    "run_id", "mode", "ticker", "direction", "quantity",
    "entry_price", "entry_tolerance_pct", "target_price", "target_price_2", "stop_loss",
    "confidence", "account_risk_pct", "timeframe", "entry_order_id", "stop_order_id",
    "target_order_id", "status", "entry_fill_price", "exit_fill_price",
    "pnl", "created_at", "entered_at", "closed_at", "raw_decision",
    "last_checked_at",
]
TRADE_COLUMN_SET = set(TRADE_COLUMNS)

_CREATE_TABLES_SQL = [
    """CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL, mode TEXT NOT NULL, ticker TEXT NOT NULL,
        direction TEXT NOT NULL, quantity INTEGER NOT NULL,
        entry_price REAL NOT NULL, entry_tolerance_pct REAL DEFAULT 1.0,
        target_price REAL, target_price_2 REAL,
        stop_loss REAL, confidence INTEGER, account_risk_pct REAL DEFAULT 1.5,
        timeframe TEXT,
        entry_order_id TEXT, stop_order_id TEXT, target_order_id TEXT,
        status TEXT DEFAULT 'pending', entry_fill_price REAL,
        exit_fill_price REAL, pnl REAL, created_at TEXT, entered_at TEXT,
        closed_at TEXT, raw_decision TEXT, last_checked_at TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE, total_trades INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0, losses INTEGER DEFAULT 0,
        total_pnl REAL DEFAULT 0.0, open_positions INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS fills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER NOT NULL, event_type TEXT NOT NULL,
        price REAL NOT NULL, bar_timestamp TEXT, reason TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    """CREATE TABLE IF NOT EXISTS pending_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL, ticker TEXT NOT NULL, raw_json TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now')), expires_at TEXT
    )""",
]


# ---------------------------------------------------------------------------
# Internal HTTP transport
# ---------------------------------------------------------------------------

def _creds() -> tuple[str, str]:
    load_dotenv()
    url = os.getenv("TURSO_DATABASE_URL", "")
    token = os.getenv("TURSO_AUTH_TOKEN", "")
    if not url:
        raise RuntimeError("TURSO_DATABASE_URL is not set")
    if not token:
        raise RuntimeError("TURSO_AUTH_TOKEN is not set")
    return url, token


def _pipeline_url(db_url: str) -> str:
    """Convert libsql://... URL to https://.../v2/pipeline."""
    base = db_url.replace("libsql://", "https://").rstrip("/")
    return f"{base}/v2/pipeline"


def _to_arg(value: Any) -> dict:
    """Encode a Python value as a Hrana typed argument."""
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "integer", "value": str(int(value))}
    if isinstance(value, int):
        return {"type": "integer", "value": str(value)}
    if isinstance(value, float):
        return {"type": "float", "value": value}
    if isinstance(value, datetime):
        return {"type": "text", "value": value.isoformat()}
    return {"type": "text", "value": str(value)}


def _execute(sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
    """Run a single SQL statement and return rows as list of dicts."""
    db_url, token = _creds()
    body = {
        "requests": [
            {
                "type": "execute",
                "stmt": {
                    "sql": sql,
                    "args": [_to_arg(p) for p in (params or [])],
                },
            },
            {"type": "close"},
        ]
    }
    resp = requests.post(
        _pipeline_url(db_url),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    result = data["results"][0]
    if result.get("type") == "error":
        raise RuntimeError(f"Turso error: {result.get('error')}")
    rs = result["response"]["result"]
    cols = [c["name"] for c in rs["cols"]]
    return [
        {col: _from_hrana(row[i]) for i, col in enumerate(cols)}
        for row in rs["rows"]
    ]


def _execute_batch(statements: list[tuple[str, list[Any] | None]]) -> list[dict]:
    """Run multiple SQL statements in one HTTP round-trip. Returns last result rows."""
    db_url, token = _creds()
    requests_payload = []
    for sql, params in statements:
        requests_payload.append({
            "type": "execute",
            "stmt": {"sql": sql, "args": [_to_arg(p) for p in (params or [])]},
        })
    requests_payload.append({"type": "close"})

    resp = requests.post(
        _pipeline_url(db_url),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"requests": requests_payload},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    last_result = data["results"][-2]  # last execute before close
    if last_result.get("type") == "error":
        raise RuntimeError(f"Turso error: {last_result.get('error')}")
    rs = last_result["response"]["result"]
    cols = [c["name"] for c in rs["cols"]]
    return [
        {col: _from_hrana(row[i]) for i, col in enumerate(cols)}
        for row in rs["rows"]
    ]


def _from_hrana(cell: dict) -> Any:
    """Convert a Hrana typed cell back to a Python value."""
    t = cell.get("type")
    v = cell.get("value")
    if t == "null" or v is None:
        return None
    if t == "integer":
        return int(v)
    if t == "float":
        return float(v)
    return v  # text


def _insert_and_get_id(sql: str, params: list[Any]) -> int:
    """INSERT a row and return its rowid in one round-trip."""
    rows = _execute_batch([
        (sql, params),
        ("SELECT last_insert_rowid()", None),
    ])
    return rows[0]["last_insert_rowid()"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_all_tables() -> None:
    """Create all cloud tables (idempotent — safe to call on every startup)."""
    db_url, token = _creds()
    requests_payload = [
        {"type": "execute", "stmt": {"sql": sql, "args": []}}
        for sql in _CREATE_TABLES_SQL
    ]
    requests_payload.append({"type": "close"})
    resp = requests.post(
        _pipeline_url(db_url),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"requests": requests_payload},
        timeout=15,
    )
    resp.raise_for_status()


def get_all_trades() -> list[dict[str, Any]]:
    return _execute("SELECT * FROM trades ORDER BY id")


def get_open_positions() -> list[dict[str, Any]]:
    return _execute("SELECT * FROM trades WHERE status = ? ORDER BY id", ["entered"])


def get_pending_trades() -> list[dict[str, Any]]:
    return _execute("SELECT * FROM trades WHERE status = ? ORDER BY id", ["pending"])


def get_recent_trade_history(days: int = 7) -> list[dict[str, Any]]:
    """Return all closed trades from the last N days.

    Same semantics as tracker.db.get_recent_trade_history — mirrors the
    local SQLite version for cloud callers.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).replace(microsecond=0).isoformat()
    return _execute(
        "SELECT ticker, direction, status, entry_price, exit_fill_price, pnl, "
        "closed_at, timeframe FROM trades "
        "WHERE status IN ('target_hit', 'stop_hit', 'expired') "
        "AND datetime(closed_at) >= datetime(?) "
        "ORDER BY closed_at DESC",
        [cutoff],
    )


def insert_trade(d: dict[str, Any]) -> int:
    """Insert a trade row and return the new cloud id."""
    unknown = set(d) - TRADE_COLUMN_SET - {"id"}
    if unknown:
        raise ValueError(f"Unknown trade columns: {', '.join(sorted(unknown))}")
    payload = {k: _to_db_value(v) for k, v in d.items() if k in TRADE_COLUMN_SET}
    if "created_at" not in payload:
        payload["created_at"] = _now_iso()
    cols = [c for c in TRADE_COLUMNS if c in payload]
    placeholders = ", ".join("?" for _ in cols)
    sql = f"INSERT INTO trades ({', '.join(cols)}) VALUES ({placeholders})"
    return _insert_and_get_id(sql, [payload[c] for c in cols])


def update_trade(trade_id: int, **kwargs: Any) -> None:
    """Update specific columns on one trade row."""
    if not kwargs:
        raise ValueError("update_trade requires at least one column")
    unknown = set(kwargs) - TRADE_COLUMN_SET
    if unknown:
        raise ValueError(f"Unknown trade columns: {', '.join(sorted(unknown))}")
    cols = list(kwargs)
    assignments = ", ".join(f"{c} = ?" for c in cols)
    params = [_to_db_value(kwargs[c]) for c in cols] + [trade_id]
    _execute(f"UPDATE trades SET {assignments} WHERE id = ?", params)


def log_fill(
    trade_id: int,
    event_type: str,
    price: float,
    bar_timestamp: str | None,
    reason: str | None,
) -> int:
    return _insert_and_get_id(
        "INSERT INTO fills (trade_id, event_type, price, bar_timestamp, reason) VALUES (?, ?, ?, ?, ?)",
        [trade_id, event_type, price, bar_timestamp, reason],
    )


# kept for backward compat with migration script — returns a lightweight proxy
def get_connection():
    class _Proxy:
        def execute(self, sql, params=None):
            return _execute(sql, list(params) if params else None)
        def close(self):
            pass
        def commit(self):
            pass
    return _Proxy()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_db_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
