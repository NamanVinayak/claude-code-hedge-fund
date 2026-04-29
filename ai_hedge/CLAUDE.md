# ai_hedge/ — Pipeline Internals

Detail for agents working inside `ai_hedge/`. The root `CLAUDE.md` has the high-level pipeline.

## Data flow

1. `prepare.py` fetches raw data per ticker → `runs/<id>/raw/<TICKER>.json`
2. `prepare.py` saves run metadata → `runs/<id>/metadata.json` (mode, tickers, dates)
3. `facts_builder.py` runs deterministic helpers per persona × ticker → `runs/<id>/facts/<persona>__<ticker>.json`
   - `growth_analyst_agent` is fully deterministic — its signal goes straight to `runs/<id>/signals/growth_analyst_agent.json`
4. If swing/research: `swing_facts_builder.py` builds swing facts (daily + hourly indicators)
5. If daytrade/research: `dt_facts_builder.py` builds DT facts + intraday data
6. LLM subagents read facts + prompts, write `runs/<id>/signals/<agent>.json`
7. `aggregate.py` runs deterministic agents (fundamentals/technicals/valuation/sentiment/risk_manager + technicals_intraday for daytrade/research), writes `runs/<id>/signals_combined.json`
8. Final agent writes `runs/<id>/decisions.json`
9. Explainer writes `runs/<id>/explanation.json`
10. `finalize.py` prints + writes `runs/<id>/summary.json`

## Key modules

| Module | Role |
|---|---|
| `data/api.py` | Public data functions (daily/intraday prices, financials, news, insider trades) |
| `data/providers/` | yfinance, SEC EDGAR, Finnhub providers |
| `data/providers/yfinance_intraday.py` | Intraday 1m/5m/15m/1h candles |
| `data/indicators.py` | pandas_ta indicators — single source of truth (RSI, MACD, Bollinger, VWAP, STC, Squeeze, SuperTrend, real OBV, RSI divergence, Fib extensions, pivot S/R). Takes `timeframe="daily"|"hourly"` for scaled params. |
| `data/earnings_calendar.py` | `days_until_next_earnings(ticker)` — yfinance, 24h cache. Risk manager uses this for 3-day blackout. |
| `data/cache.py` | SQLite cache with per-entry TTL (no stale prices) |
| `personas/helpers.py` | 79 deterministic helper functions (adapted from upstream, NOT verbatim — verify before claiming so) |
| `personas/facts_builder.py` | Invest-mode facts builder |
| `personas/swing_facts_builder.py` | Swing-mode facts (delegates indicator math to `data/indicators.py`) |
| `personas/dt_facts_builder.py` | Day-trade facts (1mo of 5m bars + indicators) |
| `personas/prompts/` | System prompts for all agents |
| `personas/prompts/explainer.md` | Explainer prompt (educational output, all modes) |
| `personas/prompts/wiki_curator.md`, `wiki_bootstrap.md` | Wiki memory layer prompts |
| `wiki/` | Wiki memory package: `inject.py`, `loader.py`, `manifest.py`, `templates.py`, `lint.py` |
| `deterministic/` | fundamentals, technicals, valuation, sentiment, risk_manager |
| `deterministic/technicals_intraday.py` | Intraday technicals (daytrade/research) |
| `schemas.py` | Pydantic signal schemas |
| `portfolio/allowed_actions.py` | `compute_allowed_actions()` — same-direction stacking blocked via `current_positions` kwarg |
| `runner/run_index.py` | Single source of truth for runs at `runs/index.json` |

## Agents (beyond upstream)

Swing strategies (5): swing_trend_momentum, swing_mean_reversion, swing_breakout, swing_catalyst_news, swing_macro_context. Each owns a distinct angle — no overlap. Old 9-agent set archived at `personas/prompts/_archive/` (Apr 2026, Sin #3 fix).

Day-trade strategies (9): dt_vwap_trader, dt_momentum_scalper, dt_mean_reversion, dt_breakout_hunter, dt_gap_analyst, dt_volume_profiler, dt_pattern_reader, dt_stat_arb, dt_news_catalyst.

**Head Traders**: swing_head_trader, dt_head_trader — synthesize strategy signals before PM. Pydantic-guarded so silent JSON parse failures crash loud (Sin #20).

**Research Report Writer**: balanced bull/bear, no recommendation.

## Multi-timeframe analysis

- **Swing**: facts bundles include `daily_indicators` AND `hourly_indicators`. Hourly uses scaled params (RSI 21 not 14, MACD 24/52/18, etc.) via `compute_daily_indicators(df, timeframe="hourly")`. `degraded_indicators[]` tracks any silent pandas_ta failures so agents see the gap honestly.
- **Daytrade**: intraday extended from 5 days to ~22 trading days (`period="1mo"`) for deeper 5-min indicator history.

## Wiki memory layer (Phase 1)

- **Purpose**: persistent per-ticker thesis/catalyst/technicals/trades notes under `wiki/`, injected as `wiki_context` into swing facts so the head trader sees prior history across runs.
- **Gate**: `tracker/watchlist.json:settings.wiki_enabled` (currently TRUE — flipped 2026-04-29).
- **Bootstrap**: `scripts/wiki_bootstrap.py` populated 96 pages across 23 tickers.
- **Maintenance**: `scripts/wiki_compactor.py` invoked by `.agents/skills/wiki_maintenance/` skill (Sunday routine).

## Enhanced Pipeline (Web Research + Verification)

```
prepare.py
→ Step 2.5: Web Research Agent (macro + ticker news via WebSearch)
→ build facts (now includes web_context)
→ Step 2.8: Web Verification Agent (corrects metric deviations >20%)
→ LLM agents (enriched + verified)
→ aggregate → PM → explainer → finalize
```

- Prompts: `personas/prompts/web_researcher.md`, `web_verifier.md`
- Output: `runs/<id>/web_research/<TICKER>.json`, `runs/<id>/verification/<TICKER>.json`
- Facts bundles include `web_context` when web research is available

## holding_period and duration fields

First intentional deviation from upstream:
- Each invest persona prompt asks for `holding_period`
- Portfolio manager asks for `duration` for the overall portfolio
- All persona schemas in `schemas.py` include optional `holding_period`
- Swing/daytrade schemas have mode-appropriate time fields (`timeframe`, `time_window`)

## Upstream copy rule (HISTORICAL — partially obsolete)

Original intent was verbatim copy from `reference/ai-hedge-fund/`. The codebase has drifted: helper functions added/renamed/adapted; upstream has no `helpers.py`. **Do not assume any function is verbatim from upstream — verify.** Use `reference/` as inspiration, not ground truth.
