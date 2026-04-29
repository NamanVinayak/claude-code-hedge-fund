"""Maintain runs/index.json — a single source of truth listing every run.

Each entry is a dict with: run_id, started_at, ended_at (None until close),
mode, asset_type, tickers, status (in_progress | completed | failed),
decision_count (None until close), notes (free-form, optional).

Read-modify-write; atomic enough for our once-per-run cadence.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

INDEX_PATH = Path("runs") / "index.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    try:
        return json.loads(INDEX_PATH.read_text())
    except json.JSONDecodeError:
        return []


def _save(entries: list[dict]) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(entries, indent=2))


def open_run(run_id: str, *, mode: str, asset_type: str, tickers: list[str]) -> None:
    """Add a new in-progress entry. No-op if run_id already present."""
    entries = _load()
    if any(e.get("run_id") == run_id for e in entries):
        return
    entries.append({
        "run_id": run_id,
        "started_at": _now_iso(),
        "ended_at": None,
        "mode": mode,
        "asset_type": asset_type,
        "tickers": tickers,
        "status": "in_progress",
        "decision_count": None,
        "notes": "",
    })
    _save(entries)


def close_run(run_id: str, *, status: str = "completed",
              decision_count: int | None = None, notes: str = "") -> None:
    """Mark a run completed/failed. Creates the entry if missing (defensive)."""
    entries = _load()
    for e in entries:
        if e.get("run_id") == run_id:
            e["ended_at"] = _now_iso()
            e["status"] = status
            if decision_count is not None:
                e["decision_count"] = decision_count
            if notes:
                e["notes"] = notes
            _save(entries)
            return
    # Defensive: index entry was never opened
    entries.append({
        "run_id": run_id,
        "started_at": None,
        "ended_at": _now_iso(),
        "mode": None,
        "asset_type": None,
        "tickers": [],
        "status": status,
        "decision_count": decision_count,
        "notes": notes or "entry was not opened by prepare.py",
    })
    _save(entries)
