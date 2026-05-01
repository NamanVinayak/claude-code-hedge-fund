---
name: wiki-daily-update
description: Nightly wiki update — writes lessons and updates thesis/trades pages for trades that closed today. Dispatches a Claude agent only when Turso has closures. Run by nightly cron at 10pm ET.
# Schedule: 0 2 * * *  (2am UTC = 10pm ET)
allowed-tools: Bash(*) Read Write Agent
---

# Wiki Daily Update — Nightly Lesson Writer

Runs nightly at 10pm ET to close the feedback loop: when the simulator closes a trade
(stop_hit, target_hit, expired), this routine writes the lesson, updates thesis confidence,
and marks the trade as closed in trades.md.

No-op if no trades closed today — exits cleanly without dispatching an agent.

## Step 1 — Fetch closed trades and build context bundle

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python tracker/wiki_daily_update.py
```

Read the output:
- If it prints `"No trades closed today. Wiki update skipped."` → **stop here**. Nothing more to do.
- If it prints `"N trade(s) closed today: ..."` → note the tickers and continue.

## Step 2 — Dispatch the lesson writer agent

The bundle was written to `runs/wiki_daily_<YYYY-MM-DD>.json`. Dispatch the agent:

```python
# Dispatch via Agent tool
# model: sonnet
# prompt: read wiki_daily_lesson_writer.md system prompt, bundle at runs/wiki_daily_<TODAY>.json
```

Agent instructions:
- System prompt: read `ai_hedge/personas/prompts/wiki_daily_lesson_writer.md`
- Input: `runs/wiki_daily_<TODAY>.json` (where TODAY = current date in YYYY-MM-DD)
- The agent will: append lesson bullets to `wiki/meta/lessons.md`, prepend outcome notes to `wiki/tickers/<TICKER>/thesis.md`, move closed trades in `wiki/tickers/<TICKER>/trades.md`

Use the `Agent` tool with this prompt:

> Read `ai_hedge/personas/prompts/wiki_daily_lesson_writer.md` for your system prompt.
> Bundle path: `runs/wiki_daily_<TODAY>.json`
> Read the bundle. Write the three types of updates for each closed trade. Return the manifest JSON.

## Step 3 — Verify no structural breakage

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python scripts/check_docs_drift.py
```

If the drift check fails, print the output but do NOT abort — wiki updates are non-blocking.

## Step 4 — Commit and push wiki changes

Push only if something changed:

```bash
cd /Users/naman/Downloads/artist
BRANCH=$(git branch --show-current)
TODAY=$(date -u +%Y-%m-%d)
COUNT=$(git diff --name-only wiki/ | wc -l | tr -d ' ')
if ! git diff --quiet wiki/; then
  git add wiki/
  git commit -m "chore: nightly wiki update ${TODAY} — ${COUNT} file(s) changed"
  git pull --rebase origin "$BRANCH" || { git rebase --abort; echo "Rebase conflict — manual resolution needed"; exit 1; }
  git push origin "$BRANCH"
  echo "Pushed nightly wiki changes to $BRANCH."
else
  echo "No wiki changes — nothing to push."
fi
```

## Notes

- The lesson writer is intentionally lighter than wiki_curator — it only touches lessons.md, thesis.md (prepend only), and trades.md (move closed trade). It does NOT rewrite technicals, catalysts, or recent.md.
- If the agent errors on a specific ticker (e.g. thesis.md not found), it skips that page and continues — wiki updates never block anything.
- Bundle files in `runs/wiki_daily_*.json` are gitignored (run artifacts).
