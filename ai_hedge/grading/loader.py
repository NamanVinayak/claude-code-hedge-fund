"""Find the most recent prior signal for (persona, ticker)."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


_RUN_ID_RE = re.compile(r"^\d{8}_\d{6}$")


def _list_run_ids(runs_root: Path, before: str) -> list[str]:
    """All run_ids strictly before `before`, sorted descending (newest first)."""
    if not runs_root.exists():
        return []
    out: list[str] = []
    for name in os.listdir(runs_root):
        if not _RUN_ID_RE.match(name):
            continue
        if name >= before:
            continue
        out.append(name)
    out.sort(reverse=True)
    return out


def load_prior_signal(
    persona: str,
    ticker: str,
    current_run_id: str,
    runs_root: str | Path = "runs",
    max_scan: int = 60,
) -> tuple[str, dict] | None:
    """Walk recent runs in reverse-time order; return first (run_id, signal_dict)
    where `runs/<id>/signals/<persona>.json` contains `ticker`.

    Returns None if nothing found within `max_scan` runs. Cold start path.
    """
    runs_root = Path(runs_root)
    candidates = _list_run_ids(runs_root, current_run_id)
    ticker_up = ticker.upper()

    for run_id in candidates[:max_scan]:
        signal_path = runs_root / run_id / "signals" / f"{persona}.json"
        if not signal_path.exists():
            continue
        try:
            data: dict[str, Any] = json.loads(signal_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        # Signals JSONs are dicts keyed by ticker (uppercase). Be tolerant.
        for key, value in data.items():
            if str(key).upper() != ticker_up:
                continue
            if not isinstance(value, dict):
                continue
            return run_id, value

    return None


__all__ = ["load_prior_signal"]
