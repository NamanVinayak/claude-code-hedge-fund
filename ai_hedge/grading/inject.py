"""Run grading over a single run directory.

Mirrors `ai_hedge/wiki/inject.py`: walks the run's swing facts files, loads
each persona's prior signal for that ticker, grades it against yfinance daily
OHLC, writes per-(persona, ticker) verdicts to `runs/<id>/grading/`, and
merges the verdict into the existing facts JSON as `prediction_grading`.
"""

from __future__ import annotations

import glob
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from ai_hedge.data.api import get_prices
from ai_hedge.grading.grader import grade_prediction
from ai_hedge.grading.loader import load_prior_signal


_FACTS_NAME_RE = re.compile(r"^(swing_[a-z0-9_]+)__([A-Z0-9.\-]+)\.json$")


def _swing_persona_ticker_pairs(run_id: str, runs_root: Path) -> list[tuple[str, str]]:
    """Find every (persona, ticker) with a facts file in this run."""
    facts_dir = runs_root / run_id / "facts"
    if not facts_dir.exists():
        return []
    pairs: list[tuple[str, str]] = []
    for path in sorted(facts_dir.glob("swing_*__*.json")):
        m = _FACTS_NAME_RE.match(path.name)
        if not m:
            continue
        pairs.append((m.group(1), m.group(2)))
    return pairs


def _parse_run_date(run_id: str) -> date | None:
    m = re.match(r"(\d{8})_\d{6}", run_id)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%d").date()
    except ValueError:
        return None


def _fetch_ohlc_from(ticker: str, start: date, end: date) -> list[Any]:
    """Get daily OHLC from start through end inclusive. Cached upstream."""
    if start >= end:
        end = start + timedelta(days=1)
    try:
        return get_prices(ticker, start.isoformat(), end.isoformat())
    except Exception:
        return []


def inject_grading(
    run_id: str,
    tickers: list[str],
    runs_root: str | Path = "runs",
    today: date | None = None,
) -> dict[str, Any]:
    """Grade each persona's prior signal for each ticker in this run.

    Idempotent. Failures on one (persona, ticker) don't block others.
    """
    runs_root = Path(runs_root)
    today = today or date.today()

    pairs = _swing_persona_ticker_pairs(run_id, runs_root)
    if not pairs:
        return {"skipped": True, "reason": "no swing facts files", "written": 0, "cold_start": 0}

    # Honor the explicit ticker list (uppercase) — the run config is the source of truth.
    requested = {t.upper() for t in tickers}
    pairs = [(p, t) for p, t in pairs if t.upper() in requested]

    grading_dir = runs_root / run_id / "grading"
    grading_dir.mkdir(parents=True, exist_ok=True)

    facts_dir = runs_root / run_id / "facts"

    written = 0
    cold_start = 0
    errors: list[str] = []

    for persona, ticker in pairs:
        try:
            prior = load_prior_signal(persona, ticker, run_id, runs_root=runs_root)
        except Exception as exc:
            errors.append(f"loader {persona}/{ticker}: {exc}")
            prior = None

        verdict: dict | None = None

        if prior is not None:
            prior_run_id, prior_signal = prior
            prior_date = _parse_run_date(prior_run_id)
            if prior_date is not None:
                ohlc = _fetch_ohlc_from(ticker, prior_date, today)
                try:
                    verdict = grade_prediction(
                        prior_signal=prior_signal,
                        ohlc=ohlc,
                        today=today,
                        prior_run_id=prior_run_id,
                    )
                except Exception as exc:
                    errors.append(f"grader {persona}/{ticker}: {exc}")
                    verdict = None

        # Write per-pair grading file (only when we have a verdict — keeps
        # the directory clean of empty cold-start files).
        if verdict is not None:
            out_path = grading_dir / f"{persona}__{ticker}.json"
            payload = {
                "persona": persona,
                "ticker": ticker,
                "run_id": run_id,
                "graded_at": today.isoformat(),
                **verdict,
            }
            out_path.write_text(json.dumps(payload, indent=2, default=str))
            written += 1
        else:
            cold_start += 1

        # Always merge into facts (null if no verdict) so the persona prompt
        # block reads a consistent key.
        facts_path = facts_dir / f"{persona}__{ticker}.json"
        if facts_path.exists():
            try:
                facts = json.loads(facts_path.read_text())
                facts["prediction_grading"] = verdict
                facts_path.write_text(json.dumps(facts, indent=2, default=str))
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"facts merge {persona}/{ticker}: {exc}")

    return {
        "skipped": False,
        "written": written,
        "cold_start": cold_start,
        "errors": errors,
    }


__all__ = ["inject_grading"]
