# tracker/ — Cloud DB + Autonomous Simulator + Legacy Local Code

This subsystem manages all trade state for the autonomous AI hedge fund. As of 2026-04-30 the architecture is **fully cloud** — no Mac dependency. Moomoo + OpenD are retired.

## Cloud architecture (current)

```
Anthropic Routine                  Auto-merge workflow              GitHub Actions cron (every 5 min)
  /swing TICKER          push      claude/* branches    fast-fwd     ingest_decisions.py → simulator.py
  produces decisions.json   ─►     into main on push    to main  ─►   → dashboard/build.py
                                                                       → push to gh-pages
                                                                       │
        Turso (cloud SQLite) ◄─── reads/writes ──┘                     │
        libsql://hedge-fund-namanvinayak.aws-us-east-1.turso.io        │
                                                                       ▼
                                                      GitHub Pages
                                                      https://namanvinayak.github.io/claude-code-hedge-fund/
```

No part of this requires the user's Mac to be on. Everything runs in GitHub Actions and Turso.

## Module layout (current — cloud-first)

```
tracker/
├── turso_client.py        — HTTP-based Turso client (Hrana over HTTP, no native ext)
├── simulator.py           — autonomous fill engine (replaces Moomoo)
├── ingest_decisions.py    — reads runs/*/decisions.json → inserts pending trades into Turso
├── ingested_runs.txt      — run_id list of already-ingested runs (idempotency)
├── watchlist.json         — tickers, schedule, budget, wiki_enabled flag
├── backtest.py            — swing predictions backtest (works with Turso via tracker.turso_client)
├── spy_benchmark.py       — "you vs SPY" comparison helper
├── TRADING_LOG.md         — persistent trading journal
│
├── db.py                  — LEGACY SQLAlchemy local SQLite layer; still used by ai_hedge.runner.aggregate
├── moomoo_client.py       — LEGACY Moomoo wrapper (no longer called)
├── executor.py            — LEGACY Moomoo paper order placer (no longer called)
├── monitor.py             — LEGACY Moomoo fill sync (no longer called)
├── reporter.py            — accuracy dashboard (legacy CLI)
├── cli.py                 — unified CLI for legacy commands
└── tracker.db             — local SQLite (gitignored). Historical data kept as a backup; production state is in Turso.
```

## Turso (cloud DB)

Free tier database used as the live trade ledger. Schema mirrors local `db.py`'s `Trade` and `DailySummary` plus two new tables:

- `trades` — same columns as local schema + `last_checked_at TEXT`
- `daily_summary` — unchanged
- `fills` — `(trade_id, event_type, price, bar_timestamp, reason, created_at)` audit log of every state change
- `pending_decisions` — reserved for future use

Credentials live in `.env` (local) and GitHub Actions secrets (`TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`).

**Public API of `turso_client.py`:**
```python
create_all_tables()
get_all_trades() -> list[dict]
get_open_positions() -> list[dict]   # status='entered'
get_pending_trades() -> list[dict]   # status='pending'
insert_trade(d: dict) -> int
update_trade(trade_id: int, **kwargs)
log_fill(trade_id, event_type, price, bar_timestamp, reason) -> int
```

## Simulator (replaces Moomoo)

`tracker/simulator.py` — runs on GitHub Actions cron every 5 min. Logic:

1. Pull pending + entered positions from Turso
2. Download 1-min yfinance bars for all involved tickers (single batched call)
3. For each position, walk bars after `last_checked_at` (during 9:30-16:00 ET only)
4. For pending trades: if bar.low ≤ entry (long) or bar.high ≥ entry (short) → fill at entry, mark `entered`
5. For entered trades: check stop and target intra-bar; fill at the trigger price (not the bar extreme)
6. Trailing stop on `target_price_2`: when first target hits, move stop to `entry_price` and replace target with `target_price_2`
7. Update `last_checked_at` on every cycle whether or not a fill happened (idempotent — no double-process)
8. Write every fill event to `fills` table

`--dry-run` flag prints what would happen without writing.

## Decision Ingester (closes the loop)

`tracker/ingest_decisions.py` — runs immediately before the simulator in the workflow:

1. Read `tracker/ingested_runs.txt` to know which run IDs have already been processed
2. For each `runs/<run_id>/` folder NOT already seen and that has `decisions.json`:
   - Skip if action is `hold` or `neutral`
   - Skip if entry_price is null/0 or quantity ≤ 0
   - Insert pending trade into Turso (double-safety check: skip if `(run_id, ticker)` already exists)
   - Append `run_id` to `ingested_runs.txt`
3. Print `Ingested N new trades from M new runs (K runs already seen)`

Idempotent. Safe to re-run any time. The 41 historical run folders existing on 2026-04-30 are pre-marked as ingested so only future routine runs flow into the simulator.

## Dashboard

`dashboard/build.py` reads Turso + `runs/` + `wiki/` + yfinance, renders 4 page types via Jinja2:
- Live positions (open trades with current P&L)
- Today's decisions (feed of routine outputs)
- Closed trades history (with win rate + total P&L)
- Per-ticker drill-down (one HTML per ticker in watchlist)

Output: `dashboard/dist/`. Pushed to gh-pages branch every 5 min by the workflow.

## Watchlist + budget

`watchlist.json` config keys:
- `tickers` — universe analyzed
- `schedules` — routine schedule definitions
- `paper_account_size` — virtual cash for budget enforcement
- `wiki_enabled: true` — wiki memory layer (currently ON)

Budget logic still lives in legacy `db.py` for the **ai_hedge.runner.aggregate** pipeline (PM sees portfolio state from local SQLite). The simulator/ingester do NOT enforce budget — that's the PM's job upstream.

## Legacy code (still present, no longer the primary path)

- `db.py` — SQLAlchemy local SQLite. Still used by `ai_hedge.runner.aggregate.py` and CLI tools. Keep as-is.
- `moomoo_client.py`, `executor.py`, `monitor.py` — Moomoo paper trading. The autonomous flow does NOT call these. Kept for backward compat with the old `python -m tracker execute` CLI.
- `python -m tracker` CLI commands (`execute`, `monitor`, `report`, `status`, `cash`) still work locally if someone wants the old Moomoo flow. Not used in production.

## Conventions

- **Production trade state lives in Turso, not `tracker.db`.** Local SQLite is now a backup and a backward-compat layer.
- The simulator gracefully handles "no yfinance data" (weekends, halts, delisted tickers) — logs a warning and skips.
- Don't manually `INSERT INTO trades` — use `tracker.turso_client.insert_trade()`. It validates columns.
- Don't add a `tracker execute` step to the swing skill — paper-order placement is the simulator's job (autonomous, not human-triggered).
