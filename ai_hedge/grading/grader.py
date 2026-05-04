"""Pure grading logic — no I/O.

Given a prior persona signal and a list of daily OHLC bars that came after,
returns a verdict dict scoring whether target hit, stop hit, or neither.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any


_NEUTRAL_MOVE_PCT = 1.0  # |close-entry|/entry < 1% counts as expired_neutral


def _coerce_field(signal: dict, *names: str) -> float | None:
    """Return the first non-None float-ish value for any of the given keys.

    Handles drift between persona JSONs (`entry`) and the pydantic schema
    (`entry_price`). Tolerates string numerics in case anything was serialized
    awkwardly. Returns None if no key holds a usable value.
    """
    for name in names:
        v = signal.get(name)
        if v is None:
            continue
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return None


def _parse_run_date(run_id: str) -> date | None:
    """Extract YYYYMMDD from a run id like '20260430_212526'."""
    m = re.match(r"(\d{8})_\d{6}", run_id)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%d").date()
    except ValueError:
        return None


def _parse_timeframe(timeframe: str | None) -> tuple[int, int]:
    """Parse '5-10 trading days' → (5, 10). Defaults (3, 14) on parse failure."""
    if not timeframe:
        return (3, 14)
    nums = [int(n) for n in re.findall(r"\d+", timeframe)]
    if len(nums) >= 2:
        return (nums[0], nums[1])
    if len(nums) == 1:
        return (nums[0], nums[0])
    return (3, 14)


def _bar_date(bar: Any) -> date | None:
    """Pull a date out of a Price-like object or dict."""
    t = getattr(bar, "time", None)
    if t is None and isinstance(bar, dict):
        t = bar.get("time")
    if not t:
        return None
    try:
        return datetime.fromisoformat(str(t)[:10]).date()
    except ValueError:
        return None


def _bar_field(bar: Any, name: str) -> float | None:
    v = getattr(bar, name, None)
    if v is None and isinstance(bar, dict):
        v = bar.get(name)
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def grade_prediction(
    prior_signal: dict | None,
    ohlc: list[Any],
    today: date,
    prior_run_id: str | None = None,
) -> dict | None:
    """Score a prior signal against subsequent daily OHLC bars.

    Returns None if `prior_signal` is None or the signal is `neutral` (no
    prediction to grade) or the signal lacks entry/target/stop. Caller
    no-ops on None.

    Same-bar tie (high>=target AND low<=stop) is scored as `stopped_out`
    with `tie_breaker_applied: true` — matches OCO behavior with no
    intrabar info.
    """
    if not prior_signal:
        return None

    direction = prior_signal.get("signal")
    if direction not in ("bullish", "bearish"):
        return None  # neutral or malformed — nothing to grade

    entry = _coerce_field(prior_signal, "entry", "entry_price")
    target = _coerce_field(prior_signal, "target", "target_price")
    stop = _coerce_field(prior_signal, "stop", "stop_loss")
    if entry is None or target is None or stop is None:
        return None

    prior_run_date = _parse_run_date(prior_run_id) if prior_run_id else None

    bars = [b for b in (ohlc or []) if _bar_date(b) is not None]
    bars.sort(key=lambda b: _bar_date(b))  # ascending
    if prior_run_date:
        # `>=` not `>`: signals are typically generated pre-market or near
        # the open and the entry is intended to fill same-day. Including
        # the run date itself catches same-day stop-outs (e.g. NVDA
        # 2026-04-30 ran at 06:04 ET, low $198.70 broke a $205.30 stop on
        # the same trading day). This costs a small bias when a signal is
        # generated mid-session, but daily bars can't fix that without
        # intraday data — flag in the persona prompt block instead.
        bars = [b for b in bars if _bar_date(b) >= prior_run_date]

    is_bull = direction == "bullish"
    sign = 1.0 if is_bull else -1.0

    first_hit: str = "neither"
    first_hit_date: date | None = None
    tie_breaker_applied = False
    mfe = 0.0  # always non-negative — best move in the signal direction
    mae = 0.0  # always non-positive — worst move against the signal

    for bar in bars:
        d = _bar_date(bar)
        hi = _bar_field(bar, "high")
        lo = _bar_field(bar, "low")
        if d is None or hi is None or lo is None:
            continue

        # MFE / MAE update — pct of entry, signed by direction.
        bar_best = (hi - entry) / entry * 100.0 if is_bull else (entry - lo) / entry * 100.0
        bar_worst = (lo - entry) / entry * 100.0 if is_bull else (entry - hi) / entry * 100.0
        if bar_best > mfe:
            mfe = bar_best
        if bar_worst < mae:
            mae = bar_worst

        # First-hit detection — only check until something hits.
        if first_hit == "neither":
            if is_bull:
                target_touched = hi >= target
                stop_touched = lo <= stop
            else:
                target_touched = lo <= target
                stop_touched = hi >= stop

            if target_touched and stop_touched:
                tie_breaker_applied = True
                first_hit = "stop"
                first_hit_date = d
            elif target_touched:
                first_hit = "target"
                first_hit_date = d
            elif stop_touched:
                first_hit = "stop"
                first_hit_date = d

    # Verdict.
    last_close = None
    for bar in reversed(bars):
        last_close = _bar_field(bar, "close")
        if last_close is not None:
            break

    days_elapsed = (today - prior_run_date).days if prior_run_date else len(bars)
    tf_min, tf_max = _parse_timeframe(prior_signal.get("timeframe"))

    if first_hit == "target":
        verdict = "target_hit"
    elif first_hit == "stop":
        verdict = "stopped_out"
    elif days_elapsed < tf_min:
        verdict = "in_progress"
    else:
        # Either past max or in the [min, max] window with no hit. Grade by close.
        if last_close is None:
            verdict = "in_progress"
        else:
            move_pct = (last_close - entry) / entry * 100.0
            move_in_dir = move_pct if is_bull else -move_pct
            if abs(move_pct) < _NEUTRAL_MOVE_PCT:
                verdict = "expired_neutral"
            elif move_in_dir > 0:
                verdict = "expired_correct"
            else:
                verdict = "expired_wrong"

    direction_correct = False
    if last_close is not None:
        move = (last_close - entry) * (1 if is_bull else -1)
        direction_correct = move > 0

    return {
        "prior_run_id": prior_run_id,
        "prior_run_date": prior_run_date.isoformat() if prior_run_date else None,
        "days_elapsed": days_elapsed,
        "min_days_elapsed": days_elapsed >= tf_min,
        "prior_signal": direction,
        "prior_confidence": prior_signal.get("confidence"),
        "prior_entry": round(entry, 4),
        "prior_target": round(target, 4),
        "prior_stop": round(stop, 4),
        "prior_timeframe": prior_signal.get("timeframe"),
        "first_hit": first_hit,
        "first_hit_date": first_hit_date.isoformat() if first_hit_date else None,
        "direction_correct": direction_correct,
        "mfe_pct": round(mfe, 2),
        "mae_pct": round(mae, 2),
        "current_price": round(last_close, 4) if last_close is not None else None,
        "verdict": verdict,
        "tie_breaker_applied": tie_breaker_applied,
    }


__all__ = ["grade_prediction"]
