# Wiki Memory Layer

This is the AI hedge fund's cross-run memory — a markdown synthesis of what
the swing-stock pipeline has learned. Maintained by the `wiki_curator` agent
after every run; pruned by `scripts/wiki_compactor.py` (Phase 2) on Sundays.

## How to read it

- `INDEX.md` — auto-generated catalog of every page with last-updated dates.
- `LOG.md` — append-only chronological run log.
- `tickers/<TICKER>/` — per-ticker pages: thesis, technicals, catalysts,
  trades, recent.
- `macro/` — regime, sectors, calendar.
- `meta/` — lessons, playbook, compactor_log.

Each page leads with a `## TL;DR` section. Strategy agents read the TL;DR
by default; the catalyst, macro, and PM agents read full pages — see
`ai_hedge/wiki/manifest.py` for which agent reads what.

## How to edit it

- The wiki is **synthesis, not append**. Old content that isn't load-bearing
  must be dropped, not piled on top of new content.
- Front-matter (YAML at top of each page) is required: `name`,
  `last_updated`, `last_run_id`, `target_words`, `stale_after_days`,
  `word_count`.
- Word budgets are enforced by `ai_hedge/wiki/lint.py`. A write that
  exceeds `target_words` by >20% is rejected.

## Feature flag

The wiki is gated behind `settings.wiki_enabled` in
`tracker/watchlist.json`. Default: `false`. Set to `true` to enable
read-time injection and the curator step on the next run.

See `scripts/wiki_memory_plan.md` for the full design.
