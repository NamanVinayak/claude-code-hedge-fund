# ARCHITECTURE.md — Historical Audit + Roadmap

This file holds the architectural audit history and roadmap. Read it on demand — NOT auto-loaded by Claude Code. The root `CLAUDE.md` and per-folder `CLAUDE.md` files have everything needed for routine work.

## Architectural audit + Wave-1/2 fixes (Apr 2026)

The codebase had 18 confirmed architectural issues, captured in `scripts/architecture_audit.md`. That doc explains the *why* behind recent changes.

### Already shipped (Wave 1 + most of Wave 2)

- **Cache TTL** (`ai_hedge/data/cache.py`) — per-entry expiry, no more stale prices
- **Run index** (`runs/index.json`) — single source of truth for runs; `prepare.py` opens an entry on start, `finalize.py` closes it
- **Silent-failure detection** (`aggregate.py`) — `_expected_agents()` enumerates required signal files per mode; missing ones log a warning AND get written into `signals_combined.json` as `degraded_inputs`
- **Doc-drift CI** (`scripts/check_docs_drift.py`) — counts helpers + agents and fails the build if docs disagree with code
- **PM portfolio state** — `aggregate.py` reads open positions from `tracker.db` (and historically `crypto_tracker.db`) and injects them into `state["data"]["portfolio"]`. PM sees `positions`, `other_positions`, and `cash` already net of open exposure. `compute_allowed_actions()` blocks same-direction stacking via `current_positions` kwarg. All PM prompts have a "Current portfolio state" section.
- **Earnings blackout** (`risk_manager.py`) — rejects any candidate with earnings within 3 days
- **Correlation cap** (`risk_manager.py`) — `MAX_CORRELATION_THRESHOLD = 0.7`, `MAX_CLUSTER_EXPOSURE_PCT = 0.30`. Per-candidate rejection AND single-linkage cluster cap.
- **SPY benchmark** — every audit report leads with "Performance vs SPY: ..."
- **Indicator consolidation** (Apr 2026) — `swing_facts_builder.py` no longer duplicates indicator math; calls `data/indicators.py` with `timeframe="hourly"|"daily"`. Real cumulative OBV, RSI divergence, Fib extensions, pivot S/R, hourly-scaled params, `degraded_indicators[]` tracking.
- **Sin #3 collapse** — 9 swing strategy agents → 5 distinct viewpoints. Old prompts archived at `ai_hedge/personas/prompts/_archive/`.
- **Sin #20 fix** — head trader Pydantic guard; all Agent dispatches pin `model: sonnet`.
- **Wiki Phase 1** — feature-flagged memory layer at `wiki/`. Flag flipped ON 2026-04-29. Bootstrap + curator + compactor shipped.
- **Crypto quarantine** — all crypto code moved to `.archive/crypto/`. Swing-stock-only focus.

### Pending (Wave 3, not yet shipped)

- **Sin #2** — routine cadence: split routines smaller, drop weekday-2x cron → 1x. Being addressed by 14 smaller swing routines + 1 weekly wiki-maintenance routine.
- **Sin #4** — deterministic screener tier; most days no LLM cost. **Biggest remaining structural win.**
- **Sin #8** — fact-bundle dedup (RE-SCOPED — was prompt caching, but project doesn't call Anthropic SDK directly; real cost win is shared common context per ticker)
- **Sin #11** — confidence calibration (defer until 50+ closed trades)
- **Sin #15** — per-run timeout/budget
- **Sin #16** — stop management (trailing / breakeven / time-based exits)
- **Sin #19** — Claude Routines reliability — 8 known Anthropic-side bugs cited in audit doc; partly mitigated by smaller routines + Sonnet pin

## Live dashboard (Wave 4 — SHIPPED 2026-04-30)

The original "Flask + HTMX with human-execute step" plan was scrapped during the Apr 30 session. Final architecture is **fully autonomous**, no Mac dependency, no human review step:

```
Anthropic Routine                    Auto-merge workflow             Dashboard cron (every 5 min)
  /swing TICKER          push        claude/* → main fast-fwd         ingest_decisions.py
  decisions.json + wiki/     ─►      auto-merge.yml                ─► simulator.py (yfinance 1-min bars)
                                                                      dashboard/build.py (Jinja2)
                                                                      push to gh-pages
                                                                      │
       Turso (cloud SQLite) ◄──── reads/writes ──┘                    │
                                                                      ▼
                                                           https://namanvinayak.github.io/
                                                           claude-code-hedge-fund/
```

What shipped:
- `tracker/turso_client.py` — HTTP-based Turso client, 4 tables (`trades`, `daily_summary`, `fills`, `pending_decisions`)
- `tracker/simulator.py` — autonomous fill engine, intra-bar detection from 1-min yfinance bars, trailing stop on `target_price_2`, idempotent via `last_checked_at`, full audit log to `fills` table
- `tracker/ingest_decisions.py` — reads `runs/*/decisions.json`, inserts pending trades into Turso (skips `hold`)
- `dashboard/build.py` + 5 Jinja2 templates — 4 page types (live positions, today's decisions, closed trades, per-ticker)
- `.github/workflows/dashboard.yml` — 5-min cron, no market-hours skip (public repo = unlimited free Actions minutes)
- `.github/workflows/auto-merge-routine-branches.yml` — fast-forwards routine `claude/*` pushes into `main` and deletes the feature branch

**Why no human-execute step?** Earlier in the session a `project_executor_scope.md` decision said the dashboard would have a "review run → click execute" button. That decision was reversed: the user explicitly preferred a fully autonomous loop. The simulator IS the executor now. If a kill-switch is ever needed it'll be a feature flag, not a foundational design.

**Why our own simulator instead of Alpaca/IBKR/Moomoo?**
- Alpaca: blocked in Canada
- IBKR: requires the user's local Gateway daemon (same problem as Moomoo)
- Moomoo: was on the user's Mac; retired with the rest of the Mac dependency

Owning the simulator means owning the bugs, but also owning the rules and audit trail. ~200 lines of Python, 3 trade states (pending → entered → closed), every state change logged.

## Wiki Phase 2 (pending)

## Wiki Phase 2 (pending)

Per `scripts/wiki_memory_plan.md`:
- Page types: `recent.md`, `sectors.md`, `calendar.md`, `lessons.md`, `playbook.md`
- Telemetry: `wiki_used` Trade column, `tracker/backtest.py --split-on wiki_used`
- `decisions.json` schema extension for the "thesis-update warranted" structured field
- PM thesis-contradiction confidence penalty (currently 0 — flag-only) — tune from data after ~10 closed trades
