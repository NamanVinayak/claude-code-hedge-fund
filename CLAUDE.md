# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repository. **Keep this file slim** — subsystem detail lives in per-folder `CLAUDE.md` files and historical context in `ARCHITECTURE.md`.

## What this project is

A zero-cost re-implementation of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund). Instead of paid LLM APIs and a paid data API, it uses:
- **Claude Code subagents** as the LLM (each persona = one Agent tool call)
- **yfinance** + **SEC EDGAR companyfacts** + **Finnhub free tier** for all financial data

Reference upstream lives at `reference/ai-hedge-fund/` (read-only). Do NOT assume any function in this repo is verbatim from upstream — see `ARCHITECTURE.md` for the rule.

## Where detail lives

| Need | Read |
|---|---|
| Pipeline internals (data flow, key modules, indicators, wiki, web research) | `ai_hedge/CLAUDE.md` |
| Persona helpers + prompt rename map | `ai_hedge/personas/CLAUDE.md` |
| Cloud DB (Turso) + simulator + ingester + dashboard | `tracker/CLAUDE.md` |
| Architectural audit + dashboard ship notes | `ARCHITECTURE.md` |
| Resume-from-here after compaction | `HANDOFF.md` (gitignored — local personal notes only; not used by routines) |
| Run instructions step-by-step | `RUN_PLAYBOOK.md` |
| Trading journal (every trade, position, lesson) | `tracker/TRADING_LOG.md` |

**Live dashboard (autonomous)**: https://namanvinayak.github.io/claude-code-hedge-fund/ — rebuilds every 5 min via GitHub Actions cron, reads Turso cloud DB. No Mac dependency.

## Running the hedge fund

When the user says "run the hedge fund on AAPL, MSFT", follow `RUN_PLAYBOOK.md`. Slash command shortcut: `/swing TSLA`, `/invest AAPL,MSFT`, `/daytrade SPY`, `/research NVDA`.

Quick reference:
```bash
python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id $(date +%Y%m%d_%H%M%S) --mode invest
# Step 2: dispatch persona subagents in parallel (varies by mode)
python -m ai_hedge.runner.aggregate --run-id <id> --tickers AAPL,MSFT
# Step 4: dispatch final agent (PM / head trader / research writer)
# Step 4.5: dispatch explainer agent
# Step 4.6 (optional): dispatch wiki curator (gated on settings.wiki_enabled — currently TRUE)
python -m ai_hedge.runner.finalize --run-id <id>
```

Venv: `.venv/`. Use `.venv/bin/python` or `source .venv/bin/activate`.

## Modes

| Mode | Purpose | Agents | Final Agent | Output |
|---|---|---|---|---|
| `invest` | Long-term portfolio | 14 investor personas | Portfolio Manager | Buy/sell/hold + holding period |
| `swing` | 2–20 day setups | 5 swing strategies | Swing PM | Entry/target/stop/RR |
| `daytrade` | Intraday plans | 9 day-trade strategies | DT PM | Setup + time window |
| `research` | Comprehensive | All 30+ agents | Research Writer | Bull/bear, no recommendation |

Universal pattern: **multiple diverse opinions → synthesis → decision**. Each mode dispatches its agents in parallel, head trader synthesizes (swing/daytrade), then PM decides.

> **Model policy:** All Agent dispatches pin `model: sonnet`. Orchestrator model is set per-routine at claude.ai. Do NOT use `model: haiku` anywhere in this project (Sin #20 fix).

## Pipeline

```
Claude Code (orchestrator)
├── prepare.py                       → fetches data + builds facts bundles
├── Agent × N (mode-dependent)       → reads facts + prompt, writes signal JSON
├── [Agent × 1 Head Trader]          → swing/daytrade only
├── aggregate.py                     → deterministic agents + risk manager
├── Agent × 1 (final agent)          → PM / Head Trader PM / Research Writer
├── Agent × 1 (explainer)            → educational narrative
├── [Agent × 1 wiki curator]         → optional, gated on settings.wiki_enabled
└── finalize.py                      → prints + writes summary.json
```

Detail in `ai_hedge/CLAUDE.md`.

## Slash commands

| Command | Purpose |
|---|---|
| `/invest AAPL,MSFT` | Long-term portfolio decisions |
| `/swing TSLA,NVDA` | Swing trade setups (2–20 days) |
| `/daytrade SPY` | Intraday trade plan |
| `/research NVDA` | Comprehensive research report |
| `/autorun` | Daily routine (monitor → model → execute → dashboard) |
| `/wiki-maintenance` | Sunday wiki compactor (one of 15 Anthropic Routines) |

## Crypto status

Crypto code is **QUARANTINED** at `.archive/crypto/` (Apr 2026). Swing-stock only focus. To restore see `.archive/crypto/README.md`.

## Environment

- Python 3.14, venv at `.venv/`
- Package installed editable: `import ai_hedge` works from any directory
- `.env` holds `FINNHUB_API_KEY` (optional)
- SQLite cache at `ai_hedge/data/cache.py` — speeds up repeated API calls

## Smoke tests

```bash
.venv/bin/python -c "from ai_hedge.data.api import get_prices; print(get_prices('AAPL', '2024-01-01', '2024-03-01'))"
.venv/bin/python -m ai_hedge.runner.prepare --tickers AAPL --run-id test --mode swing
.venv/bin/python -c "from ai_hedge.wiki.inject import is_wiki_enabled; print('wiki:', is_wiki_enabled())"
.venv/bin/python scripts/check_docs_drift.py
```

## Daily Accuracy Check (session start)

When the user opens a new session, run the swing backtest and report a plain-English portfolio summary:

```bash
.venv/bin/python tracker/backtest.py
```

One short paragraph: open trades, net P&L, entry hit rate, win rate. Wealthsimple-style: "You're up $X / down $X across N open trades. Win rate Y%, entry hit rate Z%."

## Git remote (single — clean as of 2026-05-02)

This folder has exactly **one** GitHub remote: **`hedge-remote`** → `NamanVinayak/claude-code-hedge-fund`. That's production — Anthropic Routines clone it on every fire; auto-merge workflow + dashboard cron live there. All pushes go to `hedge-remote main`.

The legacy fork (`NamanVinayak/ai-hedge-fund`) was disconnected from this folder on 2026-05-02 to eliminate two-remote confusion. A standalone clone of the legacy repo lives at `~/Downloads/oldartist/` for backup; it has its own `origin` and is unrelated to this project. Don't touch it from here.

**Verification any time:**
```bash
git remote -v   # should show ONLY hedge-remote
git ls-remote hedge-remote refs/heads/main   # SHA matches `git rev-parse main` after a push
```

If `git remote -v` ever shows a remote other than `hedge-remote` in this folder, something pulled it back in by mistake — investigate before pushing.

## Conventions

- **`.agents/` is for OpenCode** — Claude Code does NOT auto-load it. Treat it as out-of-scope; do not read or modify files there unless the user explicitly requests it.
- **graphify is no longer used** — do not run rebuild scripts, do not read `graphify-out/`. The dir is gitignored and will be deleted in a later cleanup.
- All Agent dispatches: `model: sonnet`
- Run `.venv/bin/python scripts/check_docs_drift.py` after structural changes
- Wiki feature flag is currently ON. Routines clone the repo per run, so config changes must be pushed to `hedge-remote/main` (see "Git remotes" above).
- **After every Playwright worker**: delete `.playwright-mcp/storageState*.json` to prevent session tokens from leaking into next session's context.
- **Routine push flow**: routines push to `claude/*` feature branches on `hedge-remote`; the `auto-merge-routine-branches.yml` workflow fast-forwards them to `main` automatically.

---

_Last updated: 2026-05-02. Disconnected legacy `origin` remote (NamanVinayak/ai-hedge-fund); folder now single-remote (hedge-remote = production). Legacy backup clone at `~/Downloads/oldartist/`._
