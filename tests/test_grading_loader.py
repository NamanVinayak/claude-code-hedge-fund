"""Unit tests for ai_hedge.grading.loader.

Builds a temp `runs/` tree per test — no real run data is touched.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_hedge.grading.loader import load_prior_signal


def _write_signal(tmp_path: Path, run_id: str, persona: str, payload: dict) -> Path:
    sig_dir = tmp_path / run_id / "signals"
    sig_dir.mkdir(parents=True, exist_ok=True)
    p = sig_dir / f"{persona}.json"
    p.write_text(json.dumps(payload))
    return p


def test_returns_none_when_no_prior_runs(tmp_path):
    out = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                            runs_root=tmp_path)
    assert out is None


def test_finds_most_recent_prior(tmp_path):
    _write_signal(tmp_path, "20260420_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 150}})
    _write_signal(tmp_path, "20260425_100000", "swing_breakout",
                  {"AAPL": {"signal": "bearish", "entry": 160}})
    _write_signal(tmp_path, "20260430_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 170}})

    run_id, sig = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                                    runs_root=tmp_path)
    assert run_id == "20260430_100000"
    assert sig["entry"] == 170


def test_skips_runs_without_this_ticker(tmp_path):
    _write_signal(tmp_path, "20260420_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 150}})
    _write_signal(tmp_path, "20260430_100000", "swing_breakout",
                  {"MSFT": {"signal": "bullish", "entry": 400}})

    run_id, sig = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                                    runs_root=tmp_path)
    assert run_id == "20260420_100000"
    assert sig["entry"] == 150


def test_excludes_current_and_future_runs(tmp_path):
    _write_signal(tmp_path, "20260501_120000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 999}})
    _write_signal(tmp_path, "20260502_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 999}})
    _write_signal(tmp_path, "20260430_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 170}})

    run_id, sig = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                                    runs_root=tmp_path)
    assert run_id == "20260430_100000"
    assert sig["entry"] == 170


def test_ticker_match_is_case_insensitive(tmp_path):
    _write_signal(tmp_path, "20260430_100000", "swing_breakout",
                  {"aapl": {"signal": "bullish", "entry": 170}})
    out = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                            runs_root=tmp_path)
    assert out is not None
    assert out[0] == "20260430_100000"


def test_ignores_non_run_id_dirs(tmp_path):
    (tmp_path / "smoke_test_dir").mkdir()
    (tmp_path / "index.json").write_text("{}")
    _write_signal(tmp_path, "20260430_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 170}})
    out = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                            runs_root=tmp_path)
    assert out is not None


def test_ignores_corrupt_signal_json(tmp_path):
    sig_dir = tmp_path / "20260430_100000" / "signals"
    sig_dir.mkdir(parents=True)
    (sig_dir / "swing_breakout.json").write_text("not valid json {")
    _write_signal(tmp_path, "20260420_100000", "swing_breakout",
                  {"AAPL": {"signal": "bullish", "entry": 150}})

    run_id, sig = load_prior_signal("swing_breakout", "AAPL", "20260501_120000",
                                    runs_root=tmp_path)
    assert run_id == "20260420_100000"
