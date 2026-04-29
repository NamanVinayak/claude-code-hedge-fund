---
name: wiki-maintenance
description: Weekly wiki compactor — deterministic housekeeping for wiki/. Rolls stale trade entries, prunes old recent.md bullets, archives idle ticker folders, and produces a lint report of items needing human review. No LLM calls; pure Python. Invoke as /wiki-maintenance.
disable-model-invocation: true
allowed-tools: Bash(*) Read
---

# Wiki Maintenance — Deterministic Compactor

Run by Sunday cron (`0 16 * * 0`) to keep `wiki/` from growing unbounded.
No LLM dispatches — all operations are deterministic Python.

## Step 1 — Run the compactor

```bash
cd /Users/naman/Downloads/artist && .venv/bin/python -m scripts.wiki_compactor
```

This performs (in order):
1. Word-budget check — flags pages exceeding `target_words × 1.2`
2. Trade tier rolling — moves closed trades > 30 days from "Closed — last 30 days" to monthly summaries
3. `recent.md` pruning — drops dated bullets older than 30 days
4. `LOG.md` rolling — compacts entries > 60 days to weekly summaries; > 365 days to monthly summaries
5. Orphan detection + archiving — folders idle > 60 days and not in `tracker/watchlist.json` move to `wiki/_archive/`
6. Stale-page flags — pages not updated within `stale_after_days`
7. Broken cross-ref flags — markdown links to missing files
8. Front-matter integrity flags — pages missing required YAML keys

## Step 2 — Read the lint report

```bash
cat scripts/wiki_lint_report.md
```

## Step 3 — Print if non-empty

```python
import pathlib
report = pathlib.Path("scripts/wiki_lint_report.md").read_text()
if "_No issues found._" not in report:
    print(report)
```

If the report has items, print it to stdout so the cron log captures it.
The message "Wiki review needed: N items at scripts/wiki_lint_report.md" is the
signal for a human to review and either hand-edit or run the curator with a hint.

## Step 4 — Commit and push wiki changes

The compactor mutates files in `wiki/` (rolling tiers, archiving orphans, updating front-matter). Without this step, every change dies with the routine container. Push only if something changed:

```bash
BRANCH=$(git branch --show-current)
if ! git diff --quiet wiki/ scripts/wiki_lint_report.md; then
  git add wiki/ scripts/wiki_lint_report.md
  git commit -m "wiki: weekly compactor sweep $(date -u +%Y-%m-%d)"
  git pull --rebase origin "$BRANCH" || { git rebase --abort; echo "Rebase conflict — manual resolution needed"; exit 1; }
  git push origin "$BRANCH"
  echo "Pushed weekly compactor changes to $BRANCH."
else
  echo "No wiki changes — nothing to push."
fi
```

## Notes

- Dry-run mode: `.venv/bin/python -m scripts.wiki_compactor --dry-run`
- The compactor appends to `wiki/meta/compactor_log.md` every run.
- To suppress specific flag types, edit the compactor's `run()` function.
- If a ticker is archived but reactivated in a future run, the curator
  restores it from `wiki/_archive/<TICKER>/` automatically.
