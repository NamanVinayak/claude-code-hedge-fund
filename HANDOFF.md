# HANDOFF — Resume from here

_Last updated: 2026-04-30 (autonomous dashboard system shipped)_

This file is for resuming work after a conversation compaction or session change. Read this first; it points at the right files for whatever you're picking up.

## Current state in one paragraph

The swing-stock AI hedge fund is now **fully autonomous** — no Mac dependency. The pipeline (5 swing strategies → Head Trader → Swing PM → Explainer → Wiki Curator) runs as Anthropic Routines on claude.ai. Routines push to `claude/*` feature branches, an auto-merge workflow merges to `main`, and a 5-min GitHub Actions cron runs the **decision ingester → fill simulator → dashboard builder → GitHub Pages deploy**. **Moomoo and OpenD are retired.** All trade state lives in a free Turso cloud SQLite DB. The live dashboard is at **https://namanvinayak.github.io/claude-code-hedge-fund/** and rebuilds itself every 5 minutes regardless of time. First real routine test (`swing-jpm`) ran end-to-end on 2026-04-30 and the PM correctly returned HOLD (R/R below 2:1 minimum). Wiki feature flag remains ON; first wiki-curator update on `JPM/recent.md` succeeded.

## What just happened (Apr 30 session)

1. **Turso cloud DB layer** (`tracker/turso_client.py`) — HTTP-based client (Hrana over HTTP, no native extension). Same public API as the SQLite layer. 4 tables: `trades`, `daily_summary`, `fills`, `pending_decisions`.
2. **Migration script** (`scripts/migrate_to_turso.py`) — moved 28 historical rows from `tracker.db` to Turso once, then wiped both for a clean slate.
3. **Fill simulator** (`tracker/simulator.py`) — replaces Moomoo. Uses 1-min yfinance bars, checks bar.high/bar.low for intra-bar entry/stop/target detection. Trailing stop on `target_price_2`. Idempotent via `last_checked_at`. Audit log to `fills` table.
4. **Decision ingester** (`tracker/ingest_decisions.py`) — closes the loop: reads `runs/*/decisions.json`, inserts pending trades into Turso for `buy`/`short` actions (skips `hold`). Idempotent via `tracker/ingested_runs.txt` + Turso double-check.
5. **Dashboard builder** (`dashboard/build.py` + 5 Jinja2 templates) — produces 4 page types: live positions, today's decisions, closed trades, per-ticker. Reads Turso + `runs/` + `wiki/` + yfinance.
6. **GitHub Actions cron** (`.github/workflows/dashboard.yml`) — fires every 5 min, no market-hours skip (public repo = unlimited free minutes). Runs ingester → simulator → builder → push to gh-pages.
7. **Auto-merge workflow** (`.github/workflows/auto-merge-routine-branches.yml`) — claude routines push to `claude/*` feature branches; this fast-forward-merges them into main and deletes the branch.
8. **GitHub Pages live** at `https://namanvinayak.github.io/claude-code-hedge-fund/`. Pages is set to `legacy` build_type, source = `gh-pages` branch. (Initial misconfig had it on `workflow` build_type — fixed.)
9. **Turso credentials** (`TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`) added to GitHub Actions secrets and to local `.env`.
10. **First real routine** (`swing-jpm`) fired manually on 2026-04-30. Full pipeline ran. Wiki curator updated `wiki/tickers/JPM/recent.md`. PM returned `HOLD` because R/R at $309.25 is 1.55:1 (target $319, stop $303), below the 2:1 minimum. Discipline working as intended.
11. Routine pushed to `claude/admiring-cannon-YmJlL`. Cherry-picked to main manually (one-time, pre auto-merge workflow). Going forward auto-merge handles it.
12. Pyproject swap: removed `libsql-experimental` (segfaults on Python 3.14), added `jinja2`.

## Where the truth lives

| If you need... | Read |
|---|---|
| Project overview, commands, smoke tests | `CLAUDE.md` (slim root, ~6 KB) |
| Pipeline internals, key modules, indicators, wiki | `ai_hedge/CLAUDE.md` |
| Persona helpers + rename map | `ai_hedge/personas/CLAUDE.md` |
| Cloud DB + simulator + ingester + dashboard | `tracker/CLAUDE.md` |
| Architectural audit + roadmap (Wave 4 SHIPPED) | `ARCHITECTURE.md` |
| User context (style, focus, preferences) | `~/.claude/projects/-Users-naman-Downloads-artist/memory/MEMORY.md` and pointed files |
| Most recent project snapshot | `~/.claude/projects/-Users-naman-Downloads-artist/memory/project_apr30_dashboard_ship.md` |
| Manual run instructions | `RUN_PLAYBOOK.md` |
| Production swing skill (used by routines) | `.claude/skills/swing/SKILL.md` |

## Live URLs / Infrastructure

- **Dashboard**: https://namanvinayak.github.io/claude-code-hedge-fund/
- **Repo**: https://github.com/NamanVinayak/claude-code-hedge-fund (push remote name: `hedge-remote`)
- **Turso DB**: `libsql://hedge-fund-namanvinayak.aws-us-east-1.turso.io` (free tier — 5 GB, 500M reads/mo, 10M writes/mo)
- **GitHub Actions cron**: every 5 min, always on
- **Auto-merge**: triggers on push to `claude/**`

## Next steps queued (in order)

### 1. Trigger more real routines (user)

Re-enable / trigger more routines from the list of 15 (14 swing + 1 wiki-maintenance). Recommended next test: a ticker likely to produce a `buy` action so we exercise the full chain (decision → ingester creates pending trade in Turso → simulator checks bars → dashboard shows pending position). NVDA, MSFT, TSLA all good candidates.

### 2. Validate first auto-merge (user)

When the next routine fires, watch:
- `git log hedge-remote/main --oneline` — should see `swing run ...` commit landing on main directly (via auto-merge)
- `claude/<name>` branch should be auto-deleted
- Within 5 min, dashboard cron should pick it up — visible at the dashboard URL

### 3. Fancy dashboard redesign (delegated, awaiting trigger)

A creative-brief delegate prompt for redesigning the dashboard UI was prepared. The current UI is dark-themed but plain. The brief gives a worker full creative freedom (typography, color, charts, motion, layout). Trigger when ready.

### 4. Phase 2 wiki work (not blocking)

- Page types: `recent.md`, `sectors.md`, `calendar.md`, `lessons.md`, `playbook.md`
- Telemetry: `wiki_used: bool` column on Trade table, `tracker/backtest.py --split-on wiki_used`
- `decisions.json` schema extension for "thesis-update warranted" field
- Now possible because Turso has full trade history that the wiki curator can read

## Pending audit items (not yet shipped)

- Sin #2: routine cadence — addressed by smaller routines (15 total)
- Sin #4: deterministic screener — biggest remaining structural win
- Sin #8: fact-bundle dedup
- Sin #11: confidence calibration (defer until 50+ closed trades)
- Sin #15: per-run timeout/budget
- Sin #16: stop management (trailing/breakeven beyond `target_price_2`)
- Sin #19: Routines reliability — known Anthropic-side bugs; partly mitigated by smaller routines + Sonnet pin

## Conventions to keep

- All Agent dispatches: `model: sonnet` (never haiku, never opus)
- Swing-stock only — crypto frozen at `.archive/crypto/`, daytrade/invest/research exist but not the focus
- Use `/delegate` for substantive work — head terminal supervises, fresh worker executes
- Run `.venv/bin/python scripts/check_docs_drift.py` after structural changes
- Wiki feature flag is ON. Routines clone the repo per run, so config changes must be pushed to `hedge-remote/main`
- **After every Playwright worker**: delete `.playwright-mcp/storageState*.json` to prevent session tokens from leaking into next session's context
- **graphify is no longer used** — do not run rebuild scripts, do not read `graphify-out/`

## How to verify nothing has regressed

```bash
.venv/bin/python scripts/check_docs_drift.py
.venv/bin/python -c "from ai_hedge.wiki.inject import is_wiki_enabled; print('wiki:', is_wiki_enabled())"
.venv/bin/python -c "
from dotenv import load_dotenv; load_dotenv()
from tracker.turso_client import get_all_trades, get_pending_trades, get_open_positions
print('Turso — total:', len(get_all_trades()), 'pending:', len(get_pending_trades()), 'open:', len(get_open_positions()))
"
gh secret list --repo NamanVinayak/claude-code-hedge-fund
gh api repos/NamanVinayak/claude-code-hedge-fund/pages | python3 -c "import sys,json; d=json.load(sys.stdin); print('Pages:', d['source']['branch'], d['build_type'])"
git log hedge-remote/main --oneline -5
```

Expected: drift passes, wiki flag True, Turso reachable, both TURSO_* secrets present, Pages on `gh-pages`/`legacy`, recent commits include the dashboard worker series + auto-merge workflow.
