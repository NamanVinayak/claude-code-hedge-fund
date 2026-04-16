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
A Claude Code skill is also available: `/hedge-fund [--mode invest|swing|daytrade|research] AAPL,MSFT`

Quick reference:
```bash
# Step 1: fetch data + build all facts bundles
python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id $(date +%Y%m%d_%H%M%S) --mode invest

# Step 2: dispatch LLM persona subagents IN PARALLEL (varies by mode)

# Step 3: aggregate deterministic signals + risk manager
python -m ai_hedge.runner.aggregate --run-id <id> --tickers AAPL,MSFT

# Step 4: dispatch final agent (portfolio manager / head trader / research writer)

# Step 4.5: dispatch explainer agent
# (reads decisions.json + signals_combined.json, writes explanation.json)

# Step 5: display results
python -m ai_hedge.runner.finalize --run-id <id>
```

The venv is `.venv/`. Use `.venv/bin/python` or activate with `source .venv/bin/activate`.

## Modes

The system supports 4 analysis modes, selected via `--mode`:

| Mode | Purpose | Agents | Final Agent | Output |
|---|---|---|---|---|
| `invest` | Long-term portfolio decisions | 14 investor personas | Portfolio Manager | Buy/sell/hold per ticker with holding periods |
| `swing` | Multi-day trade setups (2-20 days) | 9 swing strategies | Swing Portfolio Manager | Entry/target/stop/risk-reward per ticker |
| `daytrade` | Intraday trade plans | 9 day-trade strategies | DT Portfolio Manager | Setup/entry-trigger/targets/stop/time-window |
| `research` | Comprehensive analysis | ALL agents (30+) | Research Report Writer | Bull/bear case, metrics, risks, signal grid |

### Universal pattern

All modes follow the same architecture: **multiple diverse opinions → synthesis → decision**

- **Invest**: 14 legendary investor personas each analyze independently → Portfolio Manager synthesizes
- **Swing**: 9 swing strategies (mean reversion, breakout, trend, etc.) → Head Swing Trader synthesizes → Swing PM decides
- **Day-trade**: 9 intraday strategies (VWAP, opening range, momentum, etc.) → Head Day Trader synthesizes → DT PM decides
- **Research**: All 30+ agents analyze → Research Report Writer compiles balanced report (no recommendation)

## Architecture

```
Claude Code (orchestrator)
├── python -m ai_hedge.runner.prepare   → fetches data + runs facts_builder(s)
├── Agent × N (mode-dependent)          → each reads facts + prompt, writes signal JSON
├── [Agent × 1 Head Trader]             → swing/daytrade only: synthesizes strategy signals
├── python -m ai_hedge.runner.aggregate → deterministic agents + risk manager
├── Agent × 1 (final agent)             → PM / Head Trader PM / Research Writer
├── Agent × 1 (explainer)               → reads all signals + decisions, writes educational narrative
└── python -m ai_hedge.runner.finalize  → prints explanation + mode-specific results
```

### Data flow

1. `prepare.py` fetches raw data per ticker → `runs/<id>/raw/<TICKER>.json`
2. `prepare.py` saves run metadata → `runs/<id>/metadata.json` (mode, tickers, dates)
3. `facts_builder.py` runs all deterministic helper functions for each persona × ticker → `runs/<id>/facts/<persona>__<ticker>.json`
   - `growth_analyst_agent` is fully deterministic: its signal goes directly to `runs/<id>/signals/growth_analyst_agent.json`
4. If swing/research: `swing_facts_builder.py` builds swing strategy facts
5. If daytrade/research: `dt_facts_builder.py` builds day-trade strategy facts + fetches intraday data
6. LLM subagents read facts + prompts, write `runs/<id>/signals/<agent>.json`
7. `aggregate.py` loads all signals, runs deterministic agents (fundamentals/technicals/valuation/sentiment/risk_manager, plus technicals_intraday for daytrade/research), writes `runs/<id>/signals_combined.json`
8. Final agent reads `signals_combined.json` + its prompt, writes `runs/<id>/decisions.json`
9. Explainer subagent reads `signals_combined.json` + `decisions.json`, writes `runs/<id>/explanation.json`
10. `finalize.py` pretty-prints educational explanation + mode-specific results

### Key modules

| Module | Role |
|---|---|
| `ai_hedge/data/api.py` | Public data functions (daily prices, intraday prices, financials, news, insider trades) |
| `ai_hedge/data/providers/` | yfinance (daily + intraday), SEC EDGAR, Finnhub providers |
| `ai_hedge/data/providers/yfinance_intraday.py` | Intraday price data (1m/5m/15m/1h) via yfinance |
| `ai_hedge/data/indicators.py` | pandas_ta technical indicators (RSI, MACD, Bollinger, VWAP, STC, Squeeze, SuperTrend, etc.) |
| `ai_hedge/personas/helpers.py` | 78 deterministic helper functions (verbatim from upstream) |
| `ai_hedge/personas/facts_builder.py` | Invest-mode facts: runs helpers for each persona × ticker |
| `ai_hedge/personas/swing_facts_builder.py` | Swing-mode facts: daily + hourly indicators for swing strategies |
| `ai_hedge/personas/dt_facts_builder.py` | Day-trade facts: intraday data (1mo of 5m bars) + indicators for DT strategies |
| `ai_hedge/personas/prompts/` | System prompts for all agents (invest, swing, daytrade, research) |
| `ai_hedge/personas/prompts/explainer.md` | System prompt for the explainer agent (educational output for all modes) |
| `ai_hedge/deterministic/` | Deterministic agents: fundamentals, technicals, valuation, sentiment, risk_manager |
| `ai_hedge/deterministic/technicals_intraday.py` | Intraday technicals agent (daytrade/research modes) |
| `ai_hedge/schemas.py` | Pydantic signal schemas for all agent types |
| `ai_hedge/portfolio/allowed_actions.py` | `compute_allowed_actions()` verbatim from upstream |

### New agents (beyond upstream)

**Swing strategies** (9): swing_trend_follower, swing_pullback_trader, swing_breakout_trader, swing_momentum_ranker, swing_mean_reversion, swing_catalyst_trader, swing_sector_rotation, plus stanley_druckenmiller and news_sentiment reused from invest mode.

**Day-trade strategies** (9): dt_vwap_trader, dt_momentum_scalper, dt_mean_reversion, dt_breakout_hunter, dt_gap_analyst, dt_volume_profiler, dt_pattern_reader, dt_stat_arb, dt_news_catalyst.

**Head Traders**: swing_head_trader, dt_head_trader — synthesize strategy signals before PM.

**Research Report Writer**: Compiles all signals into balanced bull/bear analysis.

### New data infrastructure

- **Intraday prices**: `get_intraday_prices()` in api.py fetches 1m/5m/15m/1h candles via yfinance
- **`intraday_to_df()`**: Converts intraday prices to pandas DataFrame
- **`indicators.py`**: pandas_ta-based technical indicators (RSI, MACD, Bollinger Bands, VWAP, ATR, OBV, Stochastic, STC, Squeeze Momentum, SuperTrend, etc.)

### Multi-timeframe analysis

- **Swing mode**: Facts bundles include both `daily_indicators` and `hourly_indicators`. Hourly indicators are computed from 1 month of 1H bars using the same `compute_daily_indicators()` function (all indicators are bar-based). This enables divergence detection (e.g., daily RSI overbought but hourly RSI neutral) and finer-grained entry timing.
- **Daytrade mode**: Intraday data extended from 5 days to ~22 trading days (`period="1mo"`) for deeper indicator history on 5-minute bars.

### holding_period and duration fields

This is the first intentional deviation from upstream verbatim copy:
- Each invest persona prompt now asks for a `holding_period` recommendation in its signal output
- The portfolio manager prompt asks for a `duration` field for the overall portfolio
- All persona schemas in `schemas.py` include an optional `holding_period` field
- Swing/daytrade schemas have mode-appropriate time fields (timeframe, time_window)

### Verbatim copy rule

All upstream business logic is copied letter-for-letter. Only import paths are changed. If a behavioral difference is ever found vs. upstream, the fix is always: copy more code verbatim from `reference/ai-hedge-fund/`.

The `holding_period`/`duration` fields are additive extensions, not modifications to upstream logic.

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

## Enhanced Pipeline (Web Research + Verification)

Two extra agent steps added between data fetch and LLM dispatch:

```
prepare.py (fetch data)
→ Step 2.5: Web Research Agent (macro context + ticker news via WebSearch)
→ build facts (now includes web_context section)
→ Step 2.8: Web Verification Agent (checks metrics against web, corrects >20% deviations)
→ LLM agents (enriched + verified data)
→ aggregate → PM → explainer → finalize
```

- Prompts: `ai_hedge/personas/prompts/web_researcher.md`, `web_verifier.md`
- Output: `runs/{id}/web_research/{TICKER}.json`, `runs/{id}/verification/{TICKER}.json`
- Facts bundles include `web_context` key when web research is available

## Paper Trading System (Moomoo) — Internal Validation

Automated paper trading to prove model accuracy. **Not part of the pip package** — `pyproject.toml` only packages `ai_hedge*`.

### Setup

- **Platform**: Moomoo (works in Canada; Alpaca is blocked, IBKR gates on income)
- **OpenD gateway**: `opend/OpenD.app` — local daemon that bridges Python API to Moomoo servers
- **Config**: `opend/OpenD.xml` — credentials stored as MD5 hash, port 11111
- **Python API**: `moomoo-api` package in .venv (`from moomoo import *`)
- **Paper trading**: `trd_env=TrdEnv.SIMULATE`, `filter_trdmarket=TrdMarket.US`
- **Account ID**: YOUR_MOOMOO_ACCOUNT_ID

### Starting OpenD

```bash
# First time after download: remove macOS quarantine
sudo bash opend/fixrun.sh

# Then launch (must be running for API to work)
open opend/OpenD.app
```

### Moomoo API quirks (paper trading)

- `OrderType.NORMAL` for limit orders (NOT `OrderType.LIMIT` — doesn't exist)
- `TimeInForce.DAY` only (paper trading rejects `GTC`)
- `TrdSide.SELL` for shorts (NOT `SELL_SHORT` — paper doesn't support it)
- `TrdSide.BUY` for covering (NOT `BUY_BACK`)
- Fractional shares NOT supported via API (only in Moomoo app)
- Orders expire end of each day — must re-place unfilled orders daily

### Tracker module (`tracker/` at project root)

```
tracker/
├── db.py              — SQLAlchemy models (Trade, DailySummary), get_available_cash()
├── moomoo_client.py   — MoomooClient wrapper (place_entry/stop/target, cancel, positions)
├── executor.py        — reads decisions.json → places Moomoo paper orders
├── monitor.py         — syncs fills, manages stops/targets, handles expiry
├── reporter.py        — accuracy dashboard (hit rate, P&L, per-mode, confidence calibration)
├── cli.py             — unified CLI
├── watchlist.json     — tickers, modes, schedule, budget config
└── tracker.db         — SQLite trade history (in .gitignore)
```

### Commands

```bash
python -m tracker execute --run-id RUN_ID    # place orders from a model run
python -m tracker monitor                     # sync fills, manage positions
python -m tracker report [--last N] [--mode M]  # accuracy dashboard
python -m tracker status                      # show open positions
python -m tracker cash                        # show available capital
```

### Daily routine (slash command)

```
/autorun [--force]     # runs everything: monitor → model → execute → dashboard
```

Reads `tracker/watchlist.json` for schedule. `--force` runs all schedules regardless of day.

### Budget system

- Budget tracked in our DB, not Moomoo (Moomoo has $2M, we enforce our own limit)
- `available_cash = paper_account_size + realized_P&L - open_exposure`
- `--cash` flag flows through SKILL.md → aggregate → PM prompt
- Default $100,000 for regular users, $5,000 for our paper trading test
- Max 25% of capital per position, max 8 concurrent trades

## Crypto Trading Mode

Separate infrastructure for crypto analysis and simulated paper trading. Does NOT touch the stock pipeline.

### Slash commands

| Command | Purpose |
|---------|---------|
| `/crypto-swing BTC-USD,ETH-USD,SOL-USD` | Crypto swing analysis (2-20 day holds) |
| `/crypto-day BTC-USD,ETH-USD,SOL-USD` | Crypto intraday analysis |
| `/crypto-autorun` | Daily crypto routine |

### How it differs from stocks

- `--asset-type crypto` flag on prepare.py and aggregate.py skips EDGAR, Finnhub, fundamentals, valuation
- Same 9 swing/9 daytrade strategy agents (purely technical, work on any OHLCV)
- **Crypto Web Research Agent** — replaces stock web research with whale movements, funding rates, Fear & Greed Index, ETF flows, regulatory news
- **Crypto Sentiment Agent** — replaces insider-based stock sentiment with crypto-native signals
- **Crypto Swing/DT PM** — crypto-aware portfolio managers (fractional positions, crypto risks)
- Simulated locally (no exchange) — `crypto_tracker/` tracks trades in SQLite, price watcher fills orders via yfinance prices

### Crypto data sources (all free)

- **yfinance** — crypto prices work with tickers like BTC-USD, ETH-USD, SOL-USD
- **Alternative.me** — Fear & Greed Index, `GET https://api.alternative.me/fng/`, no key needed
- **CoinGecko API** — developer activity, community data. Key in `.env` as `COINGECKO_API_KEY`
- **WebSearch** — whale movements, funding rates, ETF flows, regulatory news

### Crypto tracker (`crypto_tracker/` at project root)

```
crypto_tracker/
├── db.py              — SQLAlchemy models (Trade, SimOrder), supports fractional qty
├── sim_client.py      — Simulated exchange (same interface as future kraken_client)
├── executor.py        — reads decisions.json → creates simulated orders
├── price_watcher.py   — 24/7 yfinance monitoring, fills entry/stop/target orders
├── monitor.py         — position summary, calendar day expiry
├── reporter.py        — accuracy dashboard
├── cli.py             — unified CLI
├── watchlist.json     — 20 crypto tickers, budget config
└── crypto_tracker.db  — SQLite (in .gitignore)
```

### Commands

```bash
python -m crypto_tracker execute --run-id RUN_ID    # load trades from analysis
python -m crypto_tracker watch                       # start 24/7 price watcher
python -m crypto_tracker report [--last N]           # accuracy dashboard
python -m crypto_tracker status                      # show open positions
python -m crypto_tracker cash                        # show available capital
```

### Price watcher (24/7)

The crypto price watcher IS the exchange — it checks yfinance prices every 5 min and "fills" simulated orders when levels are hit. 1.5% entry tolerance (e.g., BTC entry $73,250 triggers at $74,349 or below). Runs continuously, no market hours restriction. Handles entries, stops, targets, and timeframe expiry.

### Fractional quantities

Crypto supports fractional positions (0.002 BTC, 0.055 ETH). `allowed_actions.py` uses `fractional=True` when `asset_type == "crypto"`. Stock mode still uses integer shares.

### Future: real exchange

Swap `sim_client.py` for `kraken_client.py` (Kraken works in Canada). Same interface — one import change.

## Environment

- Python 3.14, venv at `.venv/`
- Package installed editable: `import ai_hedge` works from any directory
- `.env` file holds `FINNHUB_API_KEY` (optional) and `COINGECKO_API_KEY` (for crypto sentiment)
- SQLite cache at `ai_hedge/data/cache.py` (sqlalchemy) — speeds up repeated API calls

## Smoke tests

```bash
# Data layer
.venv/bin/python -c "from ai_hedge.data.api import get_prices; print(get_prices('AAPL', '2024-01-01', '2024-03-01'))"

# Full prepare + facts build (invest mode)
.venv/bin/python -m ai_hedge.runner.prepare --tickers AAPL --run-id test --mode invest

# Full prepare + facts build (research mode — all facts)
.venv/bin/python -m ai_hedge.runner.prepare --tickers AAPL --run-id test_research --mode research

# Import check
.venv/bin/python -c "from ai_hedge.personas.facts_builder import PERSONA_BUILDERS; print(list(PERSONA_BUILDERS.keys()))"

# Mode flag check
.venv/bin/python -m ai_hedge.runner.prepare --help
.venv/bin/python -m ai_hedge.runner.aggregate --help
```