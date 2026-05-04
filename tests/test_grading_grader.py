"""Unit tests for ai_hedge.grading.grader.

Synthetic OHLC fixtures only — no network. Each test isolates one verdict
path so failures pinpoint the broken case.
"""

from __future__ import annotations

from datetime import date

import pytest

from ai_hedge.grading.grader import grade_prediction


def _bar(d: str, o: float, h: float, l: float, c: float, v: int = 1_000_000) -> dict:
    return {"time": d, "open": o, "high": h, "low": l, "close": c, "volume": v}


def _bullish_signal(**overrides) -> dict:
    base = {
        "signal": "bullish",
        "confidence": 65,
        "entry": 100.0,
        "target": 110.0,
        "stop": 95.0,
        "timeframe": "5-10 trading days",
        "reasoning": "test",
    }
    base.update(overrides)
    return base


def _bearish_signal(**overrides) -> dict:
    base = {
        "signal": "bearish",
        "confidence": 65,
        "entry": 100.0,
        "target": 90.0,
        "stop": 105.0,
        "timeframe": "5-10 trading days",
        "reasoning": "test",
    }
    base.update(overrides)
    return base


# --- Cold-start / null-input paths --------------------------------------


def test_returns_none_on_null_signal():
    assert grade_prediction(None, [], date(2026, 5, 4)) is None


def test_returns_none_on_neutral_signal():
    sig = _bullish_signal(signal="neutral")
    assert grade_prediction(sig, [], date(2026, 5, 4)) is None


def test_returns_none_when_entry_missing():
    sig = _bullish_signal(entry=None)
    assert grade_prediction(sig, [], date(2026, 5, 4)) is None


def test_accepts_pydantic_field_names():
    """SwingSignal schema uses entry_price/target_price/stop_loss; loader
    may surface either form depending on which run wrote the JSON."""
    sig = {
        "signal": "bullish",
        "confidence": 70,
        "entry_price": 100.0,
        "target_price": 110.0,
        "stop_loss": 95.0,
        "timeframe": "5-10 trading days",
        "reasoning": "test",
    }
    bars = [_bar("2026-04-25", 100, 111, 99, 110)]  # target hit day 1
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "target_hit"
    assert out["prior_entry"] == 100.0


# --- Bullish verdict paths ----------------------------------------------


def test_bullish_target_hit():
    sig = _bullish_signal()
    bars = [
        _bar("2026-04-25", 101, 102, 100, 101.5),  # day 1, no hit
        _bar("2026-04-26", 101.5, 111, 101, 110.5),  # day 2, target hit
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "target_hit"
    assert out["first_hit"] == "target"
    assert out["first_hit_date"] == "2026-04-26"
    assert out["tie_breaker_applied"] is False
    assert out["mfe_pct"] >= 11.0  # 110/100 - 1 ≈ 11%


def test_bullish_stopped_out():
    sig = _bullish_signal()
    bars = [
        _bar("2026-04-25", 100, 101, 94, 95),  # day 1, stop hit
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "stopped_out"
    assert out["first_hit"] == "stop"
    assert out["first_hit_date"] == "2026-04-25"
    assert out["mae_pct"] <= -6.0  # (94-100)/100 = -6%


def test_bullish_in_progress_below_min_days():
    sig = _bullish_signal()  # 5-10 day window
    bars = [
        _bar("2026-05-02", 101, 103, 100, 102),
        _bar("2026-05-03", 102, 104, 101, 103),
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260501_120000")
    assert out["verdict"] == "in_progress"
    assert out["min_days_elapsed"] is False


def test_bullish_expired_correct_no_hit():
    sig = _bullish_signal()  # 5-10 day window
    # 12 daily bars, price up but not enough to hit 110, never below 95.
    bars = [_bar(f"2026-04-{15+i:02d}", 100, 103, 99, 102 + i * 0.1) for i in range(12)]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260414_120000")
    assert out["verdict"] == "expired_correct"


def test_bullish_expired_wrong_no_hit():
    sig = _bullish_signal()
    # Price drifted DOWN but never breached the stop.
    bars = [_bar(f"2026-04-{15+i:02d}", 100, 100, 96, 96.5) for i in range(12)]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260414_120000")
    assert out["verdict"] == "expired_wrong"


def test_bullish_expired_neutral():
    sig = _bullish_signal()
    # Sub-1% move at last close.
    bars = [_bar(f"2026-04-{15+i:02d}", 100, 100.5, 99.5, 100.2) for i in range(12)]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260414_120000")
    assert out["verdict"] == "expired_neutral"


# --- Tie-breaker --------------------------------------------------------


def test_tie_breaker_same_bar_hits_both():
    sig = _bullish_signal()
    bars = [
        _bar("2026-04-25", 100, 111, 94, 96),  # both target and stop touched
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "stopped_out"
    assert out["first_hit"] == "stop"
    assert out["tie_breaker_applied"] is True


# --- Bearish verdict paths ----------------------------------------------


def test_bearish_target_hit():
    sig = _bearish_signal()  # entry 100, target 90, stop 105
    bars = [
        _bar("2026-04-25", 99, 100, 89, 89.5),  # target hit day 1
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "target_hit"
    assert out["first_hit"] == "target"


def test_bearish_stopped_out():
    sig = _bearish_signal()
    bars = [
        _bar("2026-04-25", 101, 106, 100, 105.5),  # stop hit day 1
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "stopped_out"
    assert out["first_hit"] == "stop"
    assert out["mae_pct"] <= -6.0  # for bearish, adverse = price up


def test_bearish_expired_correct():
    sig = _bearish_signal()
    # Price drifted DOWN over 12 days but didn't hit 90.
    bars = [_bar(f"2026-04-{15+i:02d}", 100, 100.5, 96, 97 - i * 0.1) for i in range(12)]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260414_120000")
    assert out["verdict"] == "expired_correct"


# --- First-hit ordering -------------------------------------------------


def test_target_first_then_stop_grades_as_target():
    sig = _bullish_signal()
    bars = [
        _bar("2026-04-25", 100, 111, 100, 110),  # target hit
        _bar("2026-04-26", 110, 111, 94, 95),    # stop hit later — should NOT override
    ]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    assert out["verdict"] == "target_hit"
    assert out["first_hit_date"] == "2026-04-25"
    # MFE should reflect the high; MAE should reflect the deep day-2 low.
    assert out["mfe_pct"] >= 11.0
    assert out["mae_pct"] <= -6.0


# --- Field rounding / types ---------------------------------------------


def test_verdict_keys_are_complete():
    sig = _bullish_signal()
    bars = [_bar("2026-04-25", 100, 102, 99, 101)]
    out = grade_prediction(sig, bars, date(2026, 5, 4), prior_run_id="20260424_120000")
    expected = {
        "prior_run_id", "prior_run_date", "days_elapsed", "min_days_elapsed",
        "prior_signal", "prior_confidence", "prior_entry", "prior_target",
        "prior_stop", "prior_timeframe", "first_hit", "first_hit_date",
        "direction_correct", "mfe_pct", "mae_pct", "current_price",
        "verdict", "tie_breaker_applied",
    }
    assert expected <= set(out.keys())
