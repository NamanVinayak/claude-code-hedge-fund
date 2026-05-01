---
name: wiki-maintenance
description: Nightly wiki keeper — writes lessons + updates thesis/trades pages for trades that closed today. On Sundays, also runs the deterministic compactor (rolls stale entries, prunes old bullets, archives idle folders). Invoke as /wiki-maintenance.
# Schedule: 0 2 * * *  (2am UTC = 10pm ET, every night)
allowed-tools: Bash(*) Read Write Agent
---

# Wiki Maintenance — Nightly Lesson Writer + Sunday Compactor

Runs every night at 10pm ET. Two jobs:

1. **Every night** — write lessons for any trades that closed today, update
   thesis confidence, mark trade as closed in `trades.md`. No-op if nothing
   closed.
2. **Sundays only** — additionally run the deterministic compactor: roll
   stale trade entries, prune old `recent.md` bullets, archive idle ticker
   folders, lint front-matter.

The two jobs never conflict — the lesson writer touches lessons/thesis/trades
pages; the compactor touches everything else.

## Step 0 — Saturday early-exit

Markets were closed all of Friday night through Saturday, so nothing
could have closed since the previous run. Skip immediately on Saturdays
to avoid a pointless Turso query and routine compute.

The day-of-week check uses **Eastern Time** (not UTC) because that's the
trading-day timezone. The routine fires at 10pm Pacific = 1am Eastern
the next day, but our trading day still ends at 4pm Eastern, so "today
in ET" is the relevant date.

```bash
DOW=$(TZ=America/New_York date +%u)  # 1=Mon ... 6=Sat ... 7=Sun (Eastern Time)
if [ "$DOW" = "6" ]; then
  echo "Saturday in Eastern Time — markets were closed. Nothing to do. Exiting."
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
> Bundle path: `runs/wiki_daily_<TODAY>.json` (where TODAY = current Eastern Time date in YYYY-MM-DD)
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

## Step 3 — On Sundays only, run the deterministic compactor

```bash
DOW=$(TZ=America/New_York date +%u)  # 1=Mon ... 7=Sun (Eastern Time)
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
TODAY=$(TZ=America/New_York date +%Y-%m-%d)  # Eastern Time, the trading-day calendar
DOW=$(TZ=America/New_York date +%u)

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
