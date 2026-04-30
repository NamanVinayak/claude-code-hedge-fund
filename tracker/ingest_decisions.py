"""Decision ingester — reads decisions.json from completed runs and inserts
pending trades into Turso. Idempotent: skips runs already listed in
tracker/ingested_runs.txt and double-checks via Turso before inserting.

Run order in dashboard.yml:
  1. ingest_decisions.py   (this script — adds pending rows)
  2. simulator.py          (fills pending rows that hit price targets)
  3. dashboard/build.py    (renders latest state)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv

load_dotenv()

RUNS_DIR = Path(__file__).parent.parent / "runs"
INGESTED_FILE = Path(__file__).parent / "ingested_runs.txt"


def _load_ingested() -> set[str]:
    if not INGESTED_FILE.exists():
        return set()
    return {line.strip() for line in INGESTED_FILE.read_text().splitlines() if line.strip()}


def _mark_ingested(run_id: str) -> None:
    with INGESTED_FILE.open("a") as fh:
        fh.write(run_id + "\n")


def _get_entry_price(dec: dict) -> float | None:
    """Handle field name variations across run formats."""
    for key in ("entry_price", "entry"):
        v = dec.get(key)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    return None


def _get_target_price(dec: dict) -> float | None:
    for key in ("target_price", "target"):
        v = dec.get(key)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    return None


def _get_stop_loss(dec: dict) -> float | None:
    for key in ("stop_loss", "stop"):
        v = dec.get(key)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    return None


def _get_timeframe(dec: dict) -> str | None:
    for key in ("timeframe", "duration", "time_window"):
        v = dec.get(key)
        if v:
            return str(v)
    return None


def _existing_run_tickers(run_id: str) -> set[str]:
    """Return tickers already inserted for this run_id (Turso double-safety check)."""
    from tracker.turso_client import _execute  # internal but safe — same module
    rows = _execute(
        "SELECT ticker FROM trades WHERE run_id = ?", [run_id]
    )
    return {r["ticker"] for r in rows}


def main() -> None:
    from tracker.turso_client import create_all_tables, insert_trade

    create_all_tables()

    already_ingested = _load_ingested()

    if not RUNS_DIR.exists():
        print("No runs/ directory found — nothing to ingest.")
        return

    run_dirs = sorted(
        p for p in RUNS_DIR.iterdir()
        if p.is_dir() and (p / "decisions.json").exists()
    )

    new_runs = 0
    skipped_runs = 0
    total_trades = 0

    for run_dir in run_dirs:
        run_id = run_dir.name

        if run_id in already_ingested:
            skipped_runs += 1
            continue

        decisions_path = run_dir / "decisions.json"
        try:
            decisions_data = json.loads(decisions_path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  [WARN] {run_id}: could not read decisions.json — {exc}", file=sys.stderr)
            _mark_ingested(run_id)
            new_runs += 1
            continue

        decisions = decisions_data.get("decisions", {})
        if not decisions:
            _mark_ingested(run_id)
            new_runs += 1
            continue

        # Read mode from metadata.json (default: swing)
        mode = "swing"
        meta_path = run_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
                mode = meta.get("mode", "swing")
            except (json.JSONDecodeError, OSError):
                pass

        # Double-safety: check what's already in Turso for this run
        try:
            existing_tickers = _existing_run_tickers(run_id)
        except Exception:
            existing_tickers = set()

        run_trade_count = 0
        for ticker, dec in decisions.items():
            action = dec.get("action", "").lower()
            if action not in ("buy", "short"):
                continue

            entry_price = _get_entry_price(dec)
            if not entry_price:
                continue

            quantity = dec.get("quantity", 0)
            try:
                quantity = int(quantity)
            except (TypeError, ValueError):
                quantity = 0
            if quantity <= 0:
                continue

            if ticker in existing_tickers:
                continue

            direction = "long" if action == "buy" else "short"
            target_price = _get_target_price(dec)
            stop_loss = _get_stop_loss(dec)
            timeframe = _get_timeframe(dec)
            confidence = dec.get("confidence")
            if confidence is not None:
                try:
                    confidence = int(confidence)
                except (TypeError, ValueError):
                    confidence = None

            try:
                insert_trade({
                    "run_id": run_id,
                    "mode": mode,
                    "ticker": ticker,
                    "direction": direction,
                    "quantity": quantity,
                    "entry_price": entry_price,
                    "target_price": target_price,
                    "target_price_2": None,
                    "stop_loss": stop_loss,
                    "confidence": confidence,
                    "timeframe": timeframe,
                    "status": "pending",
                    "raw_decision": json.dumps(dec),
                })
                run_trade_count += 1
                total_trades += 1
            except Exception as exc:
                print(f"  [WARN] {run_id}/{ticker}: insert failed — {exc}", file=sys.stderr)

        _mark_ingested(run_id)
        new_runs += 1

    print(f"Ingested {total_trades} new trades from {new_runs} new runs ({skipped_runs} runs already seen)")


if __name__ == "__main__":
    main()
