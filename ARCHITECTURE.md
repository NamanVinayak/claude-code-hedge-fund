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

## Live dashboard (planned, not built)

A live web dashboard reading `tracker.db` + `runs/index.json` + `wiki/` is the eventual UI. The 18-sin remediation work is foundational — the dashboard reads structured data, so the data must be honest first. **Don't build the dashboard until Wave 3 lands.**

Target shape:
- Flask single-file app
- Server-rendered HTMX polling
- Hosted free (GitHub Actions cron commits the data; Vercel/Cloudflare Pages serves the read-only view)
- Public-share mode optional (Cloudflare tunnel)
- Open positions, pending orders, closed trades, P&L vs SPY, win rate per source

Phase 2 telemetry (`wiki_used: bool` column on Trade table, `tracker/backtest.py --split-on wiki_used`) must land before the dashboard so it can show wiki-on vs wiki-off comparisons.

## Wiki Phase 2 (pending)

Per `scripts/wiki_memory_plan.md`:
- Page types: `recent.md`, `sectors.md`, `calendar.md`, `lessons.md`, `playbook.md`
- Telemetry: `wiki_used` Trade column, `tracker/backtest.py --split-on wiki_used`
- `decisions.json` schema extension for the "thesis-update warranted" structured field
- PM thesis-contradiction confidence penalty (currently 0 — flag-only) — tune from data after ~10 closed trades
