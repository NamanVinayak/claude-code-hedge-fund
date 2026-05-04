"""Persona self-grading: score each persona's prior call against yfinance reality.

Public surface:
- `grader.grade_prediction(prior_signal, ohlc, today)` — pure logic.
- `loader.load_prior_signal(persona, ticker, current_run_id)` — filesystem lookup.
- `inject.inject_grading(run_id, tickers)` — runs grader over a run dir, mutates facts.
- `wiki_writer.append_track_records(run_id)` — appends verdicts to wiki/agents/.

V1 is swing-only; daytrade has different timeframe semantics and is deferred.
"""
