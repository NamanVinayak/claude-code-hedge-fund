---
name: wiki-maintenance
description: Nightly wiki keeper — writes lessons + updates thesis/trades pages for trades that closed today, then refreshes the open-positions ledger snapshot. On Sundays, also runs the deterministic compactor (rolls stale entries, prunes old bullets, archives idle folders). Invoke as /wiki-maintenance.
# Schedule: 0 2 * * *  (2am UTC = 10pm ET, every night)
allowed-tools: Bash(*) Read Write Agent
---

# Wiki Maintenance — Nightly Lesson Writer + Open-Position Snapshot + Sunday Compactor

Runs every night at 10pm ET. Three jobs:

1. **Every night** — write lessons for any trades that closed today, update
   thesis confidence, mark trade as closed in `trades.md`. No-op if nothing
   closed.
2. **Every night** — refresh `wiki/meta/open_positions.md` with the current
   structured ledger snapshot (open + pending positions). No-op if portfolio
   is empty.
3. **Sundays only** — additionally run the deterministic compactor: roll
   stale trade entries, prune old `recent.md` bullets, archive idle ticker
   folders, lint front-matter.

The jobs never conflict — the lesson writer touches lessons/thesis/trades
pages, the open-position writer touches only `wiki/meta/open_positions.md`,
and the compactor touches everything else.

## Step 0 — Saturday early-exit

Markets were closed all of Friday night through Saturday, so nothing
could have closed since the previous run. Skip immediately on Saturdays
to avoid a pointless Turso query and routine compute.

The day-of-week check uses **Pacific Time** because that's the routine's
wallclock — the schedule on the Anthropic Routines page is "10pm PT every
day", so "today" should mean today in PT. (UTC and ET both already say
"Saturday" by 10pm PT Friday, which would silently skip the run.)

```bash
DOW=$(TZ=America/Los_Angeles date +%u)  # 1=Mon ... 6=Sat ... 7=Sun (Pacific Time)
if [ "$DOW" = "6" ]; then
  echo "Saturday in Pacific Time — markets were closed. Nothing to do. Exiting."
  exit 0
fi
```

## Step 1 — Fetch closed trades and build context bundle

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python tracker/wiki_daily_update.py
```

Read the output:
- If it prints `"No trades closed today. Wiki update skipped."` → **skip to Step 3** (no agent dispatch needed).
- If it prints `"N trade(s) closed today: ..."` → continue to Step 2.

## Step 2 — Dispatch the lesson writer agent (only if trades closed)

The bundle was written to `runs/wiki_daily_<YYYY-MM-DD>.json`. Dispatch the agent:

> Read `ai_hedge/personas/prompts/wiki_daily_lesson_writer.md` for your system prompt.
> Bundle path: `runs/wiki_daily_<TODAY>.json` (where TODAY = current Pacific Time date in YYYY-MM-DD)
> Read the bundle. Write the three types of updates for each closed trade:
> 1. Append a lesson bullet to `wiki/meta/lessons.md`
> 2. Prepend an outcome note to `wiki/tickers/<TICKER>/thesis.md`
> 3. Move the closed trade in `wiki/tickers/<TICKER>/trades.md` from "Open Positions" to "Recently Closed"
> Return the manifest JSON.

Agent dispatch: `model: sonnet`. The lesson writer is intentionally lighter than
wiki_curator — it only touches lessons.md, thesis.md (prepend only), and trades.md
(move closed trade). It does NOT rewrite technicals, catalysts, or recent.md.

If the agent errors on a specific ticker (e.g. thesis.md not found), it skips
that page and continues — wiki updates never block anything.

## Step 2.5 — Refresh open-position snapshot (every night)

Independent of whether trades closed today. Runs after the lesson writer so the lesson writer has finished moving any closed positions out of the open-positions list before we snapshot.

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python tracker/wiki_open_positions_update.py
```

Read the output:
- If it prints `"Portfolio is empty (no open or pending positions). Wiki update skipped."` → skip the agent dispatch, continue to Step 3.
- If it prints `"N open, M pending"` → continue with the agent dispatch below.

Bundle is at `runs/wiki_open_positions_<YYYY-MM-DD>.json`. Dispatch the agent:

> Read `ai_hedge/personas/prompts/wiki_open_position_writer.md` for your system prompt.
> Bundle path: `runs/wiki_open_positions_<TODAY>.json` (where TODAY = current Pacific Time date in YYYY-MM-DD)
> Read the bundle. Rewrite `wiki/meta/open_positions.md` per the rules. Touch nothing else.
> Return the manifest JSON.

Agent dispatch: `model: sonnet`. The writer's scope is one file (`wiki/meta/open_positions.md`); it must NOT touch any per-ticker page. The prompt enforces a forbidden-vocabulary list to keep the page editorial-free — the page is read by head trader + PM only and any narrative framing creates anchoring bias.

If the agent errors, the previous snapshot stays in place — wiki updates never block anything.

## Step 3 — On Sundays only, run the deterministic compactor

```bash
DOW=$(TZ=America/Los_Angeles date +%u)  # 1=Mon ... 7=Sun (Pacific Time)
if [ "$DOW" = "7" ]; then
  cd /Users/naman/Downloads/artist && .venv/bin/python -m scripts.wiki_compactor
else
  echo "Not Sunday in ET (DOW=$DOW). Skipping weekly compactor."
fi
```

The compactor performs (in order):
1. Word-budget check — flags pages exceeding `target_words × 1.2`
2. Trade tier rolling — moves closed trades > 30 days from "Closed — last 30 days" to monthly summaries
3. `recent.md` pruning — drops dated bullets older than 30 days
4. `LOG.md` rolling — compacts entries > 60 days to weekly summaries; > 365 days to monthly summaries
5. Orphan detection + archiving — folders idle > 60 days and not in `tracker/watchlist.json` move to `wiki/_archive/`
6. Stale-page flags — pages not updated within `stale_after_days`
7. Broken cross-ref flags — markdown links to missing files
8. Front-matter integrity flags — pages missing required YAML keys

Then read and conditionally print the lint report:

```bash
if [ "$DOW" = "7" ] && [ -f scripts/wiki_lint_report.md ]; then
  if ! grep -q "_No issues found._" scripts/wiki_lint_report.md; then
    cat scripts/wiki_lint_report.md
  fi
fi
```

The message "Wiki review needed: N items at scripts/wiki_lint_report.md" is the
signal for a human to review and either hand-edit or run the curator with a hint.

## Step 4 — Verify no structural breakage

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python scripts/check_docs_drift.py
```

If the drift check fails, print the output but do NOT abort — wiki updates are non-blocking.

## Step 5 — Commit and push wiki changes

Push only if something changed. Use a message that reflects which jobs ran:

```bash
cd /Users/naman/Downloads/artist
BRANCH=$(git branch --show-current)
TODAY=$(TZ=America/Los_Angeles date +%Y-%m-%d)  # Pacific Time, the trading-day calendar
DOW=$(TZ=America/Los_Angeles date +%u)

if ! git diff --quiet wiki/ scripts/wiki_lint_report.md 2>/dev/null; then
  git add wiki/ scripts/wiki_lint_report.md 2>/dev/null || git add wiki/
  if [ "$DOW" = "7" ]; then
    git commit -m "wiki: nightly update + Sunday compactor sweep ${TODAY}"
  else
    git commit -m "wiki: nightly update ${TODAY}"
  fi
  git pull --rebase origin "$BRANCH" || { git rebase --abort; echo "Rebase conflict — manual resolution needed"; exit 1; }
  git push origin "$BRANCH"
  echo "Pushed wiki changes to $BRANCH."
else
  echo "No wiki changes — nothing to push."
fi
```

## Notes

- Dry-run mode for compactor: `.venv/bin/python -m scripts.wiki_compactor --dry-run`
- The compactor appends to `wiki/meta/compactor_log.md` every Sunday run.
- Bundle files in `runs/wiki_daily_*.json` are gitignored (run artifacts).
- If a ticker is archived but reactivated in a future run, the curator
  restores it from `wiki/_archive/<TICKER>/` automatically.
- To suppress specific compactor flag types, edit the compactor's `run()` function.
