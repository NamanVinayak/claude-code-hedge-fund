# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A zero-cost re-implementation of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund).
Instead of paid LLM APIs and a paid data API, it uses:
- **Claude Code subagents** as the LLM (each investor persona = one Agent tool call)
- **yfinance** + **SEC EDGAR companyfacts** + **Finnhub free tier** for all financial data

The reference upstream repo lives at `reference/ai-hedge-fund/` (read-only clone). All business logic is copied verbatim from there — never rewritten.

## Running the hedge fund

When the user says "run the hedge fund on AAPL, MSFT", follow **RUN_PLAYBOOK.md** exactly.

Quick reference:
```bash
# Step 1: fetch data + build all persona facts bundles (one command does both)
python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id $(date +%Y%m%d_%H%M%S)

# Step 2: dispatch 14 LLM persona subagents IN PARALLEL (one Agent tool call per persona)

# Step 3: aggregate deterministic signals + risk manager
python -m ai_hedge.runner.aggregate --run-id <id> --tickers AAPL,MSFT

# Step 4: dispatch portfolio manager subagent

# Step 5: display results
python -m ai_hedge.runner.finalize --run-id <id>
```

The venv is `.venv/`. Use `.venv/bin/python` or activate with `source .venv/bin/activate`.

## Architecture

```
Claude Code (orchestrator)
├── python -m ai_hedge.runner.prepare   → fetches data + runs facts_builder
├── Agent × 14 (persona subagents)      → each reads facts + prompt, writes signal JSON
├── python -m ai_hedge.runner.aggregate → deterministic agents + risk manager
├── Agent × 1 (portfolio manager)       → reads combined signals, writes decisions
└── python -m ai_hedge.runner.finalize  → prints decision table
```

### Data flow

1. `prepare.py` fetches raw data per ticker → `runs/<id>/raw/<TICKER>.json`
2. `facts_builder.py` runs all deterministic helper functions for each persona × ticker → `runs/<id>/facts/<persona>__<ticker>.json`
   - `growth_analyst_agent` is fully deterministic: its signal goes directly to `runs/<id>/signals/growth_analyst_agent.json`
3. LLM persona subagents read the facts bundle + their `personas/prompts/<persona>.md` and write `runs/<id>/signals/<persona>.json`
4. `aggregate.py` loads all persona signals, runs the 5 deterministic agents (fundamentals/technicals/valuation/sentiment/risk_manager), writes `runs/<id>/signals_combined.json`
5. Portfolio manager subagent reads `signals_combined.json` + `portfolio/prompt.md`, writes `runs/<id>/decisions.json`
6. `finalize.py` pretty-prints the decisions table

### Key modules

| Module | Role |
|---|---|
| `ai_hedge/data/api.py` | 8 public functions matching upstream signatures — the only data entry point |
| `ai_hedge/data/providers/` | yfinance, SEC EDGAR, Finnhub providers |
| `ai_hedge/personas/helpers.py` | 78 deterministic helper functions (verbatim from upstream), prefixed where duplicate |
| `ai_hedge/personas/facts_builder.py` | Runs helpers for each persona × ticker, writes facts JSON |
| `ai_hedge/personas/prompts/` | 16 verbatim system prompt .md files (one per persona + portfolio_manager) |
| `ai_hedge/deterministic/` | 5 pure-math agents: fundamentals, technicals, valuation, sentiment, risk_manager |
| `ai_hedge/schemas.py` | 16 Pydantic signal schemas (verbatim from upstream) |
| `ai_hedge/portfolio/allowed_actions.py` | `compute_allowed_actions()` verbatim from upstream |

### Verbatim copy rule

All upstream business logic is copied letter-for-letter. Only import paths are changed. If a behavioral difference is ever found vs. upstream, the fix is always: copy more code verbatim from `reference/ai-hedge-fund/`.

### Duplicate function rename map

Five function names existed in multiple upstream persona files. In `helpers.py` they are prefixed with a 2-letter persona code:

| Original name | Renamed to |
|---|---|
| `analyze_management_quality` | `wb_analyze_management_quality` (Warren Buffett) |
| `analyze_management_quality` | `cm_analyze_management_quality` (Charlie Munger) |
| `calculate_intrinsic_value` | `wb_calculate_intrinsic_value` (Warren Buffett) |
| `calculate_intrinsic_value` | `rj_calculate_intrinsic_value` (Rakesh Jhunjhunwala) |
| `analyze_valuation` | `ba_analyze_valuation` (Bill Ackman) |
| `analyze_valuation` | `ga_analyze_valuation` (Growth Agent) |
| `analyze_sentiment` | `pl_analyze_sentiment` (Peter Lynch) |
| `analyze_sentiment` | `pf_analyze_sentiment` (Phil Fisher) |
| `analyze_sentiment` | `sd_analyze_sentiment` (Stanley Druckenmiller) |
| `analyze_insider_activity` | `pl_analyze_insider_activity` (Peter Lynch) |
| `analyze_insider_activity` | `pf_analyze_insider_activity` (Phil Fisher) |
| `analyze_insider_activity` | `sd_analyze_insider_activity` (Stanley Druckenmiller) |

All short codes: `wb`=warren_buffett, `cm`=charlie_munger, `bg`=ben_graham, `ba`=bill_ackman, `cw`=cathie_wood, `mb`=michael_burry, `nt`=nassim_taleb, `pl`=peter_lynch, `pf`=phil_fisher, `sd`=stanley_druckenmiller, `mp`=mohnish_pabrai, `rj`=rakesh_jhunjhunwala, `ad`=aswath_damodaran, `ga`=growth_agent, `ns`=news_sentiment

## Environment

- Python 3.14, venv at `.venv/`
- Package installed editable: `import ai_hedge` works from any directory
- `.env` file holds `FINNHUB_API_KEY` (optional — system works without it, just loses insider/news data)
- SQLite cache at `ai_hedge/data/cache.py` (sqlalchemy) — speeds up repeated API calls

## Smoke tests

```bash
# Data layer
.venv/bin/python -c "from ai_hedge.data.api import get_prices; print(get_prices('AAPL', '2024-01-01', '2024-03-01'))"

# Full prepare + facts build
.venv/bin/python -m ai_hedge.runner.prepare --tickers AAPL --run-id test

# Import check
.venv/bin/python -c "from ai_hedge.personas.facts_builder import PERSONA_BUILDERS; print(list(PERSONA_BUILDERS.keys()))"
```
