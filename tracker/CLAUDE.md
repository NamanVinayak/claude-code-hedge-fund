# tracker/ — Paper Trading + Accuracy Tracking

This subsystem places paper trades on Moomoo based on model decisions and tracks accuracy. It is internal validation only — **not part of the pip package** (`pyproject.toml` only packages `ai_hedge*`).

> **READ FIRST for any trade-related work:** `tracker/TRADING_LOG.md` — full history of every trade, position, run, known bugs, and lessons learned.

## Setup

- **Platform**: Moomoo paper trading (Alpaca blocked in Canada; IBKR gates on income)
- **OpenD gateway**: `opend/OpenD.app` — local daemon bridging Python API to Moomoo servers
- **Config**: `opend/OpenD.xml` — credentials stored as MD5 hash, port 11111
- **Python API**: `moomoo-api` package in `.venv` (`from moomoo import *`)
- **Paper env**: `trd_env=TrdEnv.SIMULATE`, `filter_trdmarket=TrdMarket.US`
- **Account ID**: 76568910

## Starting OpenD

```bash
sudo bash opend/fixrun.sh   # first time only — remove macOS quarantine
open opend/OpenD.app        # must be running for API to work
```

## Moomoo API quirks (paper trading)

- `OrderType.NORMAL` for limit orders (NOT `OrderType.LIMIT` — doesn't exist)
- `TimeInForce.DAY` only (paper rejects `GTC`)
- `TrdSide.SELL` for shorts (NOT `SELL_SHORT`)
- `TrdSide.BUY` for covering (NOT `BUY_BACK`)
- Fractional shares NOT supported via API (only in Moomoo app)
- Orders expire end of each day — re-place unfilled orders daily

## Module layout

```
tracker/
├── TRADING_LOG.md     — Persistent trading journal (READ FIRST)
├── db.py              — SQLAlchemy models (Trade, DailySummary), get_available_cash()
├── moomoo_client.py   — MoomooClient wrapper
├── executor.py        — reads decisions.json → places Moomoo paper orders
├── monitor.py         — syncs fills, manages stops/targets, handles expiry
├── reporter.py        — accuracy dashboard
├── backtest.py        — swing predictions backtest
├── spy_benchmark.py   — "you vs SPY" comparison helper
├── cli.py             — unified CLI
├── watchlist.json     — tickers, modes, schedule, budget config
└── tracker.db         — SQLite (gitignored)
```

## Commands

```bash
python -m tracker execute --run-id RUN_ID      # place orders from a model run
python -m tracker monitor                       # sync fills, manage positions
python -m tracker report [--last N] [--mode M]  # accuracy dashboard
python -m tracker status                        # show open positions
python -m tracker cash                          # show available capital
```

## Daily routine slash command

```
/autorun [--force]   # monitor → model → execute → dashboard
```

Reads `tracker/watchlist.json` for schedule. `--force` runs all schedules regardless of day.

## Budget system

- Tracked in our DB, NOT Moomoo (Moomoo paper has $2M; we enforce our own limit)
- `available_cash = paper_account_size + realized_P&L - open_exposure`
- `--cash` flag flows through SKILL.md → aggregate → PM prompt
- Default $100,000 for regular users, $5,000 for our paper trading test
- Max 25% of capital per position, max 8 concurrent trades
