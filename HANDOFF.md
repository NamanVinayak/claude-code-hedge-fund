# HANDOFF — Resume from here

_Last updated: 2026-04-29 (wiki flag flipped ON)_

This file is for resuming work after a conversation compaction or session change. Read this first; it points at the right files for whatever you're picking up.

## Current state in one paragraph

The swing-stock AI hedge fund is architecturally clean and shipped to GitHub at `claude-code-hedge-fund`. The wiki memory layer (Phase 1) is built, bootstrapped with 96 pages across 23 tickers, and **flag is now ON** (`tracker/watchlist.json:settings.wiki_enabled` = true, committed `ed5ebaa`, pushed to hedge-remote/main). The 5 swing strategy agents work end-to-end. Paper positions were wiped for a fresh start; closed-trade history is preserved. Next: set up 15 routines on claude.ai (which clone this repo per run), then validate the first real curator fire.

## What just happened (Apr 29 session)

1. Indicator code consolidated to one file with real OBV, RSI divergence, Fibonacci extensions, pivot S/R, hourly-appropriate parameters
2. 9 swing strategy agents collapsed to 5 distinct viewpoints (Sin #3 shipped)
3. Head trader Pydantic guard added (Sin #20 — silent JSON parse failures)
4. Crypto code quarantined to `.archive/crypto/`
5. Wiki memory layer Phase 1 built + bootstrapped + compactor ready
6. Paper positions abandoned; tracker.db cleaned
7. `summary.json` writer added to finalize.py (dashboard-ready)
8. Repo published cleanly to `claude-code-hedge-fund`, main reconciled, 4 stale branches deleted, LICENSE added

## Where the truth lives

| If you need... | Read |
|---|---|
| Project overview, architecture, pipeline diagram | `CLAUDE.md` |
| User context (style, focus, preferences) | `~/.claude/projects/-Users-naman-Downloads-artist/memory/MEMORY.md` and pointed files |
| Most recent state of everything | `~/.claude/projects/-Users-naman-Downloads-artist/memory/project_apr29_session.md` |
| Sin status (architectural audit) | `scripts/architecture_audit.md` |
| Wiki memory layer design | `scripts/wiki_memory_plan.md` |
| Pipeline run instructions | `RUN_PLAYBOOK.md` |
| Skill orchestration | `.agents/skills/swing/SKILL.md` |

## Next steps queued (in order)

### 1. Set up 15 routines on claude.ai/code (user, 30-60 min)

Wiki flag is already ON in git (commit `ed5ebaa`). Routines clone this repo per run, so the flag travels with it.

On claude.ai/code, set up:
- 14 swing routines (split watchlist tickers across them) firing weekday market mornings
- 1 weekly maintenance routine pointing at `/wiki-maintenance`, Sunday afternoon UTC

### 2. First-real-curator validation (user, monitor)

After the first scheduled routine fires:
- Check `git status wiki/` to see what pages the curator updated
- Read a couple of the updated pages to confirm sensible synthesis
- Confirm `runs/<id>/summary.json` shows `wiki_enabled: true` and `wiki_pages_updated: N`

### 3. Wave 4 — Live dashboard (deferred, ~1-2 weeks of work when ready)

Reads `runs/<id>/summary.json`, `tracker.db`, `wiki/`. Architecture sketch:
- Flask single-file app
- Server-rendered HTMX polling
- Hosted free (GitHub Actions cron commits the data; Vercel/Cloudflare Pages serves the read-only view)
- Public-share mode optional (Cloudflare tunnel)

Wave 4 should NOT start before Phase 2 telemetry lands (`wiki_used` column on Trade table) — without that, the dashboard can't show wiki-on vs wiki-off comparisons.

## Phase 2 work still pending (not blocking)

Per `scripts/wiki_memory_plan.md`:
- Page types: recent.md, sectors.md, calendar.md, lessons.md, playbook.md
- Telemetry: `wiki_used` Trade column, `tracker/backtest.py --split-on wiki_used`
- `decisions.json` schema: structured "thesis-update warranted" field
- PM thesis-contradiction confidence penalty (currently 0 — flag-only)

## Pending audit items (not yet shipped)

- Sin #2: routine cadence — being addressed by user setting up 15 smaller routines
- Sin #4: deterministic screener — biggest remaining structural win
- Sin #8: fact-bundle dedup
- Sin #11: confidence calibration (defer until 50+ closed trades)
- Sin #15: per-run timeout/budget
- Sin #16: stop management (trailing/breakeven)
- Sin #19: Routines reliability — partly mitigated already by smaller routines + Sonnet pin

## Conventions to keep

- All Agent dispatches: `model: sonnet` (never haiku, never opus)
- Swing-stock only — crypto is frozen at `.archive/crypto/`, daytrade/invest/research still exist but are not the focus
- Use `/delegate` for substantive work — head terminal supervises, fresh worker executes
- Always run `.venv/bin/python scripts/check_docs_drift.py` after structural changes
- Wiki feature flag is ON (flipped 2026-04-29). Routines clone the repo per run so changes to `tracker/watchlist.json` must be pushed to `hedge-remote/main`.

## How to verify nothing has regressed

```bash
.venv/bin/python scripts/check_docs_drift.py
.venv/bin/python -c "from ai_hedge.wiki import manifest, inject, loader, lint, templates; print('wiki imports OK')"
.venv/bin/python -c "from ai_hedge.wiki.inject import is_wiki_enabled; print('flag:', is_wiki_enabled())"
.venv/bin/python -c "from tracker.db import get_session, Trade; s=get_session(); print('open:', s.query(Trade).filter(Trade.status=='entered').count())"
git log --oneline main -5
```

Expected: drift passes, imports OK, flag=True, open=0, recent commits include `feat: enable wiki memory layer`, `chore: add LICENSE`, the wiki feat, the Sin #3 collapse, the indicator consolidation, the crypto quarantine.
