# HANDOFF — Resume from here

_Last updated: 2026-05-01 (memory feedback loop closed — every agent now reads lessons)_

This file is for resuming work after a conversation compaction or session change. Read this first; it points at the right files for whatever you're picking up.

## Current state in one paragraph

The swing-stock AI hedge fund is fully autonomous AND has a hardened closed feedback loop. The pipeline (5 swing strategies → Head Trader → Swing PM → Explainer → Wiki Curator) runs as Anthropic Routines. Every closed trade flows back into the wiki: a nightly `wiki-maintenance` routine (10pm PT daily; was Sundays only) reads Turso, writes a lesson to `wiki/meta/lessons.md` (with auto-aggregated `## Patterns` table on top by Sunday compactor), prepends an outcome note to the ticker's `thesis.md` (preserved through curator rewrites), and moves the trade to "Recently Closed" in `trades.md`. **All 7 swing agents now read lessons.md before voting** — strategies + PM via the manifest-driven injector (using `full` mode after a critical silent-empty bug was fixed), Head Trader by reading wiki files directly per dispatch instructions. Pending limit-order exposure is correctly subtracted from PM cash. `aggregate.py` reads portfolio state from Turso, and crashes loud if `--require-turso` is set + creds missing OR Turso fails at runtime. Day-of-week / date logic is consistently America/Los_Angeles (the routine's wallclock). SQLite cutoff queries now use `datetime()` to compare across timezones correctly. First auto-written lesson — NVDA stop_hit -$264.65 — landed on May 1. Live dashboard at **https://namanvinayak.github.io/claude-code-hedge-fund/**, GitHub Actions drives the 5-min ingester→simulator→dashboard cycle. Wiki feature flag ON.

## What just happened (May 01 session — memory loop closed)

1. **Pending exposure math fix** (`ai_hedge/runner/aggregate.py`) — `pending_exposure = sum(qty × entry_price)` for `pending` trades is now subtracted from `cash_after_exposure` alongside `total_exposure`. PM no longer sees committed cash as free. PM prompt's `pending_orders` bullet rewritten to say cash already accounts for them.
2. **Empty-positions warning** — `aggregate.py` prints a loud warning if Turso returns 0 open positions, so silent data issues are visible.
3. **Wiki lesson writer** — new `tracker/wiki_daily_update.py` queries Turso for closures in last 3 days, builds a context bundle JSON. New agent prompt `ai_hedge/personas/prompts/wiki_daily_lesson_writer.md` writes one lesson bullet + thesis prepend + trades.md move per closed trade. Bundle has agent-side dedup against `lessons_current` for idempotency.
4. **Unified wiki-maintenance skill** (`.agents/skills/wiki_maintenance/SKILL.md`) — runs nightly. Saturday early-exit (ET-aware). Sunday additionally runs the deterministic compactor. Same Anthropic Routine entry, just a smarter skill internally.
5. **ET timezone fix** — all day-of-week and date checks now use `TZ=America/New_York`, not UTC. Fixes a real bug where 10pm Pacific = 5am UTC = "Saturday" in UTC, which would have silently skipped Friday closures.
6. **`wiki/meta/lessons.md`** created with YAML front-matter + format spec. First real lesson appended on May 1: NVDA stop_hit, -$264.65, EMA pullback Fib dip-buy.
7. **Fix A — Strategy agents see lessons.md** — `ai_hedge/wiki/manifest.py` now adds `("meta", "lessons", "tldr")` to all 5 swing strategies. Each strategy prompt got a paragraph framing lessons as a confidence dial (not a veto).
8. **Fix B — Head Trader sees wiki memory** — `swing_head_trader.md` got a "Wiki Memory" section. `.agents/skills/swing/SKILL.md` Step 4 now instructs the Head Trader to read `wiki/meta/lessons.md` and `wiki/tickers/<T>/trades.md` (TL;DR) before synthesizing. Head Trader is intentionally NOT in the manifest because it has no facts bundle.
9. **Routine env hardened** — user added `TURSO_DATABASE_URL` + `TURSO_AUTH_TOKEN` to the shared `hedge-fund-prod` cloud environment used by all routines. Without this, today's aggregate.py change to read from Turso would have silently fallen back to empty local SQLite.
10. **First nightly wiki update auto-ran** on May 1 ("Run now") and successfully wrote the NVDA lesson + updated `wiki/tickers/NVDA/{thesis,trades}.md`. Auto-merged to main via `claude/admiring-wright-bwyve` → `main` workflow.
11. **PT timezone fix** (`3d59f04`) — switched all day-of-week / date checks in wiki-maintenance from `America/New_York` to `America/Los_Angeles` after realizing 10pm PT = 1am Saturday ET, which would have silently skipped Friday-night runs.
12. **`--require-turso` flag** (`f20727e`, hardened by `d77ace8`) — `aggregate.py` now crashes loud (FATAL) when Turso creds are missing OR when a runtime Turso error happens. All 4 production skills (swing, daytrade, invest, research) pass `--require-turso`.
13. **`check_docs_drift.py` sys.path fix** (`f4c4161`) — script prepends project root to `sys.path` so `import ai_hedge.*` works inside the routine container (where the project isn't installed editable).
14. **Confidence_score system attempted then reverted** (`8d37abd` → `074daa0`) — added a numeric thesis confidence score, then reverted after recognizing LLMs can read lessons.md + trades.md as text and reason directly without needing a separate dial. Kept the deterministic patterns table (compactor-aggregated win rates per setup type).
15. **Critical silent bug — `lessons_tldr` returned empty string** (`ae802b9`) — `lessons.md` has no `## TL;DR` heading, so `read_tldr()` produced an empty slice. Fix A (lessons → strategies, shipped earlier in the session) had been silently delivering empty context. Switched manifest to `full` mode for all 6 agents that read lessons. Verified `build_wiki_context('swing_trend_momentum', 'NVDA')` now returns 791 chars.
16. **4 HIGH bug fixes from a `superpowers:systematic-debugging` audit** — each in its own commit:
    - `d77ace8` H1: re-raise Turso errors when `--require-turso` is set (was being swallowed by a try/except)
    - `2d480b1` H2: tighten lesson dedup to match `[DATE] | [TICKER] | [SETUP TYPE] | [OUTCOME]` (4 fields), so same-day multi-lot closes don't drop the second lot's lesson
    - `a2a8005` H3: switch `closed_at` cutoff query to `datetime(closed_at) >= datetime(?)` so timezone-offset strings compare correctly
    - `751be27` H4: add hard rule to `wiki_curator.md` to preserve `⚠️ Recent trade:` / `✓ Recent trade:` lines through curator rewrites

## Previously shipped (Apr 30 — still current)

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
| Most recent project snapshot | `~/.claude/projects/-Users-naman-Downloads-artist/memory/project_may01_memory_loop_closed.md` |
| Manual run instructions | `RUN_PLAYBOOK.md` |
| Production swing skill (used by routines) | `.claude/skills/swing/SKILL.md` |

## Live URLs / Infrastructure

- **Dashboard**: https://namanvinayak.github.io/claude-code-hedge-fund/
- **Repo**: https://github.com/NamanVinayak/claude-code-hedge-fund (push remote name: `hedge-remote`)
- **Turso DB**: `libsql://hedge-fund-namanvinayak.aws-us-east-1.turso.io` (free tier — 5 GB, 500M reads/mo, 10M writes/mo)
- **GitHub Actions cron**: every 5 min, always on
- **Auto-merge**: triggers on push to `claude/**`

## Next steps queued (in order)

### 1. Verify next morning's swing run uses the new memory (user + automatic)

The NVDA lesson is in `wiki/meta/lessons.md`. When the next swing routine fires:
- Confirm Head Trader's `key_conflicts` field references the recent NVDA failure where relevant
- Confirm the strategies' confidence values are not ignoring the lesson context
- `git log hedge-remote/main --oneline` should show "wiki: nightly update" commits landing every night around 1am UTC (10pm PT)

### 2. Investigate docs drift check failing inside the routine container

The 2026-05-01 routine log said "Docs drift check failed on module import (non-blocking per skill spec)". Locally `.venv/bin/python scripts/check_docs_drift.py` passes clean. Probably a Python-path / installation difference inside the routine container. Investigate fresh — either fix the import or document why the check has to be skipped in routines.

### 3. (Deferred) Numeric thesis confidence_score

Original audit directive #1 was a numeric `confidence_score` field in thesis.md that the simulator could decay automatically. Current implementation prepends a string warning ("⚠️ Recent trade: stop_hit ..."). Good enough for now; numeric score is a future enhancement once we have ~20 closed trades and want to do calibration / decay logic.

### 4. (Deferred) Lessons aggregation

`wiki/meta/lessons.md` is a flat append-log of bullets. After ~20 trades it should grow a "patterns" section synthesized weekly by the Sunday compactor — e.g., "EMA pullback dip-buys have lost 3 of last 4". Punted to a future session.

### 5. Trigger more real routines (user)

The watchlist still has 14 swing routines. Recommended next test: a ticker likely to produce a `buy` decision to exercise the full chain (decision → ingester → simulator fill → dashboard).

### 6. Fancy dashboard redesign (delegated, awaiting trigger)

A creative-brief delegate prompt for redesigning the dashboard UI was prepared in a prior session. Trigger when ready.

## Pending audit items (not yet shipped)

- Sin #2: routine cadence — addressed by smaller routines (15 total)
- Sin #4: deterministic screener — biggest remaining structural win
- Sin #8: fact-bundle dedup
- Sin #11: confidence calibration (defer until 50+ closed trades) — partial mitigation: lessons.md is now feeding the dial
- Sin #15: per-run timeout/budget
- Sin #16: stop management (trailing/breakeven beyond `target_price_2`)
- Sin #19: Routines reliability — known Anthropic-side bugs; partly mitigated by smaller routines + Sonnet pin

**Memory architecture follow-ups (May 1 audit, MEDIUM-priority — not yet shipped):**
- M1: free-text setup-type vocabulary fragments the patterns table (lock to ~10 strings)
- M2: `tracker/ingest_decisions.py` silently ignores `sell` / `cover` actions (PM-driven exits never happen)
- M3: same lex-string TZ comparison risk in `aggregate.py recent_closed=7` window (lower-impact than H3 fix)
- M4: `read_tldr()` returns empty silently when a page lacks `## TL;DR` heading (caught by `ae802b9` for lessons; could recur on any new manifest entry)
- M5: malformed YAML front-matter silently treated as no-frontmatter (`_split_front_matter` failure mode)
- M6: PT-date filename vs UTC cutoff edge case in `tracker/wiki_daily_update.py` at midnight crossings
- L1–L5: simulator partial-profit booking, `entry_fill_price` falsy fallback, ingest dedup edge case, default-cash mismatch, stale schedule comment

**Resolved (May 1):**
- ✅ Numeric confidence_score (rolled back — LLM reads text directly)
- ✅ Lessons pattern aggregation (deterministic compactor step, `## Patterns` block at top of lessons.md)
- ✅ `check_docs_drift.py` module import (sys.path prepend fix in `f4c4161`)

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
from tracker.turso_client import get_all_trades, get_pending_trades, get_open_positions, get_recent_trade_history
print('Turso — total:', len(get_all_trades()), 'pending:', len(get_pending_trades()), 'open:', len(get_open_positions()))
print('  recent closures (3d):', len(get_recent_trade_history(days=3)))
"
.venv/bin/python tracker/wiki_daily_update.py   # writes runs/wiki_daily_<DATE>.json or prints 'No trades closed today'
.venv/bin/python -c "
from ai_hedge.wiki.manifest import AGENT_MANIFEST
for a, e in AGENT_MANIFEST.items():
    print(a, 'lessons=', any(x == ('meta','lessons','tldr') for x in e))
"
gh secret list --repo NamanVinayak/claude-code-hedge-fund
git log hedge-remote/main --oneline -10
```

Expected: drift passes, wiki flag True, Turso reachable, all 6 swing agents in manifest show `lessons=True`, recent commits include the May 1 memory-loop series (`9b364af`, `91e0b6f`, `b921309`, `aa6c73e`, `8e83444`, `2c505c3`, `1d7dfbc`, `51cdfab`, `d44dd6d`).
