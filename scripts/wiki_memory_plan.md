# Wiki Memory Layer — Implementation Plan

_Plan only — no code. Drafted 2026-04-29 by a planning subagent against the swing-stock pipeline as it exists today._

This plan describes how to bolt a Karpathy-style "LLM Wiki" onto the swing-stock pipeline so each run has continuous memory across runs without:
- letting pages grow forever,
- bloating every agent's context,
- adding a separate database, and
- changing the 5 strategy agents, head trader, or PM that were just collapsed/stabilized.

The wiki is a markdown synthesis of what we have learned — it sits **between** the raw `runs/<id>/` artifacts (immutable) and the LLM agents (consumers), and is itself maintained by an LLM agent (the curator) plus a deterministic compactor.

The pattern follows Karpathy's three-layer model: **raw sources → wiki → schema**. In our case raw sources are `runs/<id>/`, `web_research/raw/`, and `tracker.db`; the wiki is `wiki/`; the schema is this file plus the per-page templates and the per-agent manifest.

---

## 0. Decisions Baked In From Head-Terminal Review

These were open questions on the first draft. They are now final — implementing worker should treat them as constraints, not options.

- **Curator model:** pinned to `sonnet`, consistent with the project-wide model policy in `CLAUDE.md` (Sin #20 fix). One extra Sonnet call per swing run.
- **Bootstrap timing:** runs **before** the next swing routine fires. The bootstrap script keeps a runtime check that refuses to start if any run is in flight (per `runs/index.json:status == "in_progress"`).
- **Validation approach:** **no A/B alternation**. Replaced with telemetry-only: a `wiki_used: bool` column on the `Trade` table, plus logging of every "thesis-update warranted" PM note. Compare pre-wiki vs post-wiki win rate as a natural before/after split. Escalate to a real A/B only if the pre/post comparison suggests the wiki is hurting.
- **Curator scope:** single-call curator stays. Hard limit added: **max 30 page outputs per curator call**. If a run would exceed that (15+ tickers × 5 per-ticker pages, plus macro), split into two dispatches — first half tickers, then second half + macro pages. The 1–3 ticker case (the common one) remains a single dispatch with no sharding.
- **PM thesis-contradiction penalty:** **start at 0**. PM prompt only flags the contradiction in `reasoning`; no fixed confidence subtraction. Threshold can be tuned from Phase 3 telemetry once we see whether contradictions correlate with losses.
- **Compactor cadence:** **independent Sunday cron**, not bolted onto `/autorun`. `/autorun` only fires on weekday market days; the compactor runs Sunday afternoon when there is no trading activity. A separate `scripts/wiki_compactor.py` cron entry is added; `/autorun` and `tracker/cli.py` are NOT modified for compactor scheduling.

---

## 1. Wiki Folder Structure

The wiki lives at the repo root in a new top-level `wiki/` directory. It is plain markdown, version-controlled in git, no separate DB. (Markdown was chosen so a human can also read and edit it; git is the audit log.)

```
wiki/
├── README.md                  # human-readable schema + how to read/edit (~150 words)
├── INDEX.md                   # auto-generated catalog of every page + last_updated
├── LOG.md                     # append-only chronological run log (rolled up after 60d)
├── tickers/
│   └── <TICKER>/              # one folder per ticker we have ever held or analyzed
│       ├── thesis.md          # the durable bull/bear story (rarely rewritten)
│       ├── technicals.md      # current state of the chart (rewritten most runs)
│       ├── catalysts.md       # upcoming events + recent news synthesis
│       ├── trades.md          # journal — open positions + recent closed + rolled history
│       └── recent.md          # last 30 days of materially-changed signals
├── macro/
│   ├── regime.md              # current macro regime (Fed, rates, geopolitical)
│   ├── sectors.md             # sector rotation / relative strength map
│   └── calendar.md            # earnings + economic events for held tickers
├── meta/
│   ├── lessons.md             # crystallized lessons across all closed trades
│   ├── playbook.md            # patterns that have worked / not worked + sample sizes
│   └── compactor_log.md       # what was compacted/dropped on each compactor run
└── _archive/                  # tickers we no longer track; pages moved here, not deleted
```

**Naming conventions:**
- Ticker folders are uppercase symbol (`AAPL`, not `aapl`).
- All filenames lowercase, snake_case, `.md` extension.
- Front matter (YAML) on every page: `last_updated`, `last_run_id`, `word_count`, `target_words`, `stale_after_days`. The compactor reads these.
- No `.md` page is ever deleted — orphans go to `wiki/_archive/<ticker>/` so git history stays clean.

**Why root-level and not `ai_hedge/wiki/`:** the wiki is a project-level artifact, not a Python module. Code that touches it (the curator-supporting Python helpers) lives at `ai_hedge/wiki/`; the markdown content lives at the repo root next to `runs/`, `tracker/`, and `scripts/`.

---

## 2. Page Templates

Each template lists: **purpose**, **target word count**, **required sections (TL;DR first)**, **what's in vs. out**, **update rule**. Word counts are budgets the compactor enforces.

### 2.1 `wiki/tickers/<TICKER>/thesis.md`
- **Purpose:** the durable bull/bear story for this name. Why we ever care about it.
- **Target:** 400–600 words.
- **Sections:**
  1. **TL;DR** (≤50 words) — one sentence bull, one sentence bear, one sentence verdict.
  2. **Bull case** — 3 bullets, durable claims only (moat, secular trend, structural advantage).
  3. **Bear case** — 3 bullets, durable risks (competitive pressure, balance sheet, regulatory).
  4. **What would change my mind** — 2 bullets describing falsification triggers.
  5. **Last updated** — date + run id.
- **In:** durable, slow-moving claims about the business and its market position.
- **Out:** today's price, technical levels, today's news headlines, this week's analyst rating.
- **Update rule:** rewritten only when (a) the curator detects a material story-level change in `web_research/<TICKER>.json` or `explanation.json`, or (b) the compactor finds the page is >30 days unchanged AND the last 5 runs show signal direction has flipped. Default action on a routine run: do nothing.

### 2.2 `wiki/tickers/<TICKER>/technicals.md`
- **Purpose:** current state of the chart in plain English. The "what kind of chart is this" snapshot.
- **Target:** 250–400 words.
- **Sections:**
  1. **TL;DR** (≤40 words) — chart state in one sentence (e.g. "uptrend, pulling back to 21-EMA, momentum cooling but still positive").
  2. **Multi-timeframe state** — daily vs hourly alignment in 2–3 sentences.
  3. **Key levels** — `support`, `resistance`, `entry zone`, `invalidation` as a small table; numeric values.
  4. **Setup type** — one of `trending / ranging / coiling / breaking-out / extended`.
  5. **Last updated**.
- **In:** indicator readings as **state** (overbought, accelerating), key S/R levels, regime label.
- **Out:** explanations of what an indicator does (those live in `meta/lessons.md` glossary or the explainer's output).
- **Update rule:** rewritten on every run for that ticker. Old state is NOT appended — it is overwritten. If the prior setup-type changed, the curator copies the prior label to `recent.md` as a single dated bullet.

### 2.3 `wiki/tickers/<TICKER>/catalysts.md`
- **Purpose:** what events are pending and what news has actually moved this name recently.
- **Target:** 300–500 words.
- **Sections:**
  1. **TL;DR** (≤50 words) — next catalyst, sentiment of recent news, insider tilt.
  2. **Upcoming events** — dated list (earnings date, FDA windows, conferences, ex-div).
  3. **Recent news synthesis** — 3–5 bullets, last 14 days, **summarized not appended**. Curator must compress, not concat.
  4. **Insider activity** — net buy/sell direction last 30 days; one line.
  5. **Analyst consensus** — current rating + price target if known.
  6. **Last updated**.
- **In:** dated facts, sentiment summaries, named sources.
- **Out:** raw headline copy/paste; long quotes from articles.
- **Update rule:** rewritten on every run. Dated events past their date drop off automatically. Headlines older than 14 days drop off (older material lives in `runs/<id>/web_research/raw/` if anyone needs it).

### 2.4 `wiki/tickers/<TICKER>/trades.md`
- **Purpose:** the trade journal for this ticker. The only page allowed to grow with run count, but its growth is bounded by tier compaction.
- **Target:** 800 words **soft cap**; pages over budget trigger compactor's tiering rules below.
- **Sections (in display order, top to bottom):**
  1. **TL;DR** (≤40 words) — open position summary + lifetime P&L on this name.
  2. **Open positions** — full detail, every entry+stop+target+rationale; uncompressed; max 8 entries.
  3. **Closed — last 30 days** — 3-line entries each (entry/exit/lesson).
  4. **Closed — older, rolled by month** — 1-line summaries (e.g. `2026-03: 4 trades, 3W/1L, +$140`).
  5. **Closed — older than 6 months** — 1-line YTD summary.
  6. **Lifetime stats** — N trades / win rate / median R / SPY-relative.
- **In:** all closed-trade rows (sourced from `tracker.db`); rationale at entry; lesson at exit.
- **Out:** intra-trade chatter, every monitor-tick price update.
- **Update rule:** the only page that legitimately appends. Curator adds a new `Open positions` block on a buy/short. On exit (sell/cover), the entry moves down to "Closed — last 30 days." Compactor rolls older entries down the tier ladder weekly.

### 2.5 `wiki/tickers/<TICKER>/recent.md`
- **Purpose:** rolling 30-day log of materially-changed signals. The "what's changed lately on this name" feed.
- **Target:** 200–300 words.
- **Sections:**
  1. **TL;DR** (≤30 words) — most recent signal change.
  2. **Dated bullets** — only when the swing signal direction flipped, a catalyst hit, or a key level broke. No-change runs do NOT add a bullet.
  3. **Last updated**.
- **In:** state changes, level breaks, signal flips.
- **Out:** "trend continued bullish today again" (that is what `technicals.md` is for).
- **Update rule:** appended on material-change runs only. Compactor prunes bullets >30 days old.

### 2.6 `wiki/macro/regime.md`
- **Purpose:** current top-down macro picture, owned by the macro view.
- **Target:** 300–500 words.
- **Sections:**
  1. **TL;DR** (≤50 words) — regime label (`risk-on`, `risk-off`, `transitional`) + one-sentence justification.
  2. **Fed posture** — current rate, last move, market expectation for next 2 meetings.
  3. **Rate trajectory & inflation** — 2–3 sentences.
  4. **Geopolitical / regulatory** — 2–3 sentences.
  5. **Risk-off triggers to watch** — 3 bullets.
  6. **Last updated**.
- **In:** dated, sourced macro claims.
- **Out:** ticker-specific commentary.
- **Update rule:** rewritten on a run when `web_research/<TICKER>.json:macro_context` differs materially from current page (curator does the diff judgement). Otherwise unchanged.

### 2.7 `wiki/macro/sectors.md`
- **Purpose:** sector relative-strength + rotation map.
- **Target:** 200–300 words.
- **Sections:**
  1. **TL;DR** (≤40 words) — leaders / laggards in one sentence.
  2. **Leaders** — 3 sectors with 1-line "why."
  3. **Laggards** — 3 sectors with 1-line "why."
  4. **Rotation phase** — early-cycle / mid / late / risk-off.
  5. **Last updated**.
- **In:** sector ETF relative-strength reads, rotation observations.
- **Out:** ticker-level commentary; constituent picks.
- **Update rule:** rewritten weekly by the compactor (full pass against held universe). On run-time, curator makes a one-line edit only if `web_research` strongly contradicts current state.

### 2.8 `wiki/macro/calendar.md`
- **Purpose:** the dated event list for tickers we hold or watch.
- **Target:** 100–300 words; mostly a table.
- **Sections:**
  1. **TL;DR** (≤30 words) — most imminent catalyst across the watchlist.
  2. **Earnings dates** — table of ticker → date → days-out.
  3. **Macro events** — Fed meeting, CPI, jobs print dates.
  4. **Last updated**.
- **In:** dated, future events.
- **Out:** prose explanation; that goes in `regime.md` or `catalysts.md`.
- **Update rule:** rewritten every run from `earnings_calendar.py` + `web_research` macro key_events. Past events drop off.

### 2.9 `wiki/meta/lessons.md`
- **Purpose:** durable lessons crystallized from closed trades. Cross-ticker.
- **Target:** 300–500 words.
- **Sections:**
  1. **TL;DR** (≤60 words) — top 5 lessons, one sentence each.
  2. **Entry lessons**, **Sizing lessons**, **Exit lessons**, **Agent disagreement lessons** — 2–4 bullets each.
  3. **Last updated**.
- **In:** patterns observed across **3+ closed trades** (single-trade observations don't qualify).
- **Out:** trade-specific recaps (those live in the per-ticker `trades.md`).
- **Update rule:** updated by the compactor monthly OR when the user explicitly adds a lesson via a `wiki note` command. The curator may **propose** a lesson in `compactor_log.md` but cannot promote it without compactor approval, to prevent recency bias.

### 2.10 `wiki/meta/playbook.md`
- **Purpose:** which setups have actually worked, with sample size and win rate.
- **Target:** 300–500 words.
- **Sections:**
  1. **TL;DR** (≤50 words) — best and worst pattern by R-multiple, gated on n≥5.
  2. **Patterns table** — pattern → trade count → win rate → median R → SPY-relative.
- **In:** quantitative pattern outcomes derived deterministically from `tracker.db`.
- **Out:** narrative speculation.
- **Update rule:** regenerated end-to-end weekly by the compactor, programmatically — no LLM call. Pattern tags come from the entry-time signal mix (which agents fired).

### 2.11 `wiki/INDEX.md`
- **Purpose:** auto-generated catalog of every page, with last-updated date and a one-line description. Karpathy's index page.
- **Target:** as long as it needs to be (it's a list).
- **Sections:** one line per page: `- [tickers/AAPL/thesis.md](tickers/AAPL/thesis.md) — last_updated 2026-04-29 — durable bull/bear`.
- **Update rule:** regenerated by the compactor and at the end of every run by `finalize.py`. Never edited by hand.

### 2.12 `wiki/LOG.md`
- **Purpose:** append-only chronological log of runs and material wiki changes. Karpathy's log page.
- **Target:** soft cap 1500 lines; compactor rolls older entries.
- **Format:** `## [YYYY-MM-DD] swing | TICKERS | run <id> | <decision summary> | wiki touched: <pages>`
- **Update rule:** the curator appends one entry per run. Compactor rolls entries >60 days old into weekly summary lines, and entries >365 days old into monthly summary lines.

---

## 3. Per-Agent Reading Manifest

The 7 LLM agents in the swing pipeline each get a different slice of the wiki. Default reading is **TL;DR only** of any listed page (≤50 words at the top, parsed by reading until the first `## ` heading after the TL;DR header). Full sections are read only where listed.

Manifest is encoded in code at `ai_hedge/wiki/manifest.py` so prompts can stay short — the harness injects the right slice into the facts bundle, the agent doesn't have to know the wiki path.

| Agent | Pages it reads | Mode | Why |
|---|---|---|---|
| `swing_trend_momentum` | `tickers/<T>/technicals.md` | TL;DR | knows what kind of chart this was last run; spots regime change vs. memory |
| | `macro/regime.md` | TL;DR | risk-on vs risk-off colors what counts as "trending" |
| `swing_mean_reversion` | `tickers/<T>/technicals.md` | TL;DR | needs prior chart-state to know if today's read is genuinely new extreme |
| | `tickers/<T>/recent.md` | TL;DR | recent reversal attempts → context for "is this the third try?" |
| `swing_breakout` | `tickers/<T>/technicals.md` | full | needs precise S/R levels from the levels table |
| `swing_catalyst_news` | `tickers/<T>/catalysts.md` | **full** | this is its meat: dated events, news synthesis, insider tilt, analyst rating |
| | `macro/calendar.md` | full | macro event window |
| `swing_macro_context` | `macro/regime.md` | **full** | this is its meat |
| | `macro/sectors.md` | **full** | also its meat |
| | `tickers/<T>/thesis.md` | TL;DR | enough to know the durable story without re-reading bull/bear cases |
| `swing_head_trader` | _none_ | — | by spec it synthesizes the 5 strategy signals only; adding wiki here would double-count |
| `swing_portfolio_manager` | `tickers/<T>/thesis.md` | TL;DR | sanity check that today's call doesn't contradict the thesis |
| | `tickers/<T>/trades.md` | full | sees prior open lots, prior losses on this name, lifetime P&L |
| | `meta/lessons.md` | TL;DR | top-5 lessons act as guardrails |

**Rationale for omitting the head trader:** the strategy agents already do the wiki-aware reading. The head trader's job is to synthesize disagreement between the strategy signals — its inputs are already a mix of "live read" + "memory-aware read." Adding wiki context here would be a triple-read.

**Default rule:** if an agent's manifest is empty, no `wiki_context` key is added to its facts bundle. This means existing prompts work unchanged for agents not on the list.

---

## 4. Wiki Update Flow

The wiki is touched in two phases per run: a **read phase** before the agents fire, and a **write phase** after the PM has decided.

### 4.1 Read phase (where the wiki is injected)

Where it fires: `prepare.py` step, after `build_swing_facts()` completes.

What happens:
1. A new helper `ai_hedge.wiki.inject_context(run_id, tickers, mode="swing")` is called.
2. For each agent listed in the manifest, for each ticker, the helper:
   a. Looks up which pages that agent reads, in what mode (TL;DR vs full).
   b. Reads each page; for TL;DR mode, returns only the content between the `TL;DR` heading and the next `## ` heading.
   c. Bundles those slices into a single `wiki_context` dict, e.g. `{"thesis_tldr": "...", "technicals_full": "..."}`.
   d. Writes the dict into the agent's existing facts bundle at `runs/<id>/facts/<agent>__<TICKER>.json` under a new top-level key `wiki_context`.
3. The wiki itself is **not** modified during read phase. Read phase is purely injection.
4. If a page is missing (e.g. brand-new ticker), `wiki_context` is `{"new_ticker": true}` and agents see the absence honestly — no fake memory.
5. If a page's front-matter says `last_updated` is older than `stale_after_days`, the helper adds `"stale": true` so the agent can weight the prior less.

Cost: deterministic, zero LLM calls. Wall time <1 second per run.

### 4.2 Write phase (curator agent)

A new pipeline step **Step 7.5** lives between the explainer (Step 7) and `finalize.py` (Step 8) in `.claude/skills/swing/SKILL.md`. It dispatches one Agent tool call: `wiki_curator`.

The curator's responsibilities, in order:

1. **Per-ticker page updates.** For each ticker in the run, decide what to rewrite based on the diff between current wiki and today's `decisions.json`/`signals_combined.json`/`web_research/<TICKER>.json`/`explanation.json`:
   - `thesis.md` — rewrite **only if** explainer's bull/bear cases differ materially from existing TL;DR, OR page is >30 days unchanged AND signal direction flipped within the run. Otherwise: leave alone.
   - `technicals.md` — rewrite every run from current indicators + setup label.
   - `catalysts.md` — rewrite every run from `web_research/<TICKER>.json` + `recent_news`. Prune dated events whose date has passed.
   - `recent.md` — append one dated bullet only if signal direction flipped or a key level broke.
   - `trades.md` — append a new "Open positions" block on a buy/short decision. On a sell/cover, move that block to "Closed — last 30 days."

2. **Macro page updates** (once per run, after all per-ticker pages):
   - `regime.md` — rewrite if the latest `web_research:macro_context` is materially different from current TL;DR. Use the explainer's macro narrative as the rewrite source.
   - `sectors.md` — small edit only if the macro view contradicts current state. Full rewrite is owned by the compactor.
   - `calendar.md` — regenerate from `earnings_calendar.py` (deterministic call already in code) + `macro_context.key_events`.

3. **Index + Log updates** (once per run, last):
   - Append one line to `LOG.md`.
   - Touch `INDEX.md` with new `last_updated` dates (this part can be deterministic — but having the curator do it keeps the agent honest about what it actually changed).

4. **Hard rules baked into the prompt:**
   - Synthesis only: when rewriting, the curator must produce a **replacement** version that fits the page's word budget. It may NOT just append.
   - Cite sources: every claim must reference a run id, a `web_research/raw/` filename, or a `tracker.db` trade id. No free-floating assertions.
   - Word budgets are NOT optional. If a rewrite would exceed budget, the curator must compact existing content first. The harness's post-write linter (described in §5) will reject a write that exceeds budget by >20%.
   - **Max 30 page outputs per curator call.** If a single dispatch would touch more than 30 pages (rough math: 5 per-ticker pages × 6 tickers + macro/index/log = 33), the orchestrator splits the work into two curator dispatches: dispatch A covers the first half of tickers (per-ticker pages only); dispatch B covers the remaining tickers AND the macro + INDEX + LOG pass. The 1–3 ticker case (the common one) stays a single dispatch — no pre-emptive sharding.

5. **What if the curator wants to update the same page from multiple tickers?**
   - For per-ticker pages this is impossible by construction (each page is owned by one ticker).
   - For macro pages, the curator processes them ONCE at the run level after the per-ticker pass — never per ticker. The prompt enforces this ordering explicitly.

### 4.3 Curator prompt outline

The curator system prompt (lives at `ai_hedge/personas/prompts/wiki_curator.md`) sketches as:

```
You are the Wiki Curator. You maintain wiki/ as a synthesis — not an append-log.

Inputs you will be given:
- run_id, mode, tickers, decisions.json, signals_combined.json, explanation.json
- web_research/<TICKER>.json for each ticker
- For each page that may be touched: full current content + its front-matter (target_words, stale_after_days, last_updated)

For each ticker, decide which of {thesis, technicals, catalysts, recent, trades} to rewrite or leave alone.
For each page you rewrite:
  - Produce a complete replacement that fits target_words ± 20%.
  - TL;DR section first (under heading exactly "## TL;DR"), then the rest in template order.
  - Update the YAML front-matter (last_updated, last_run_id, word_count).
  - Cite every claim with a run id, web_research source, or trade id.
  - Synthesize — do NOT append today's commentary onto yesterday's. Old content that is no longer load-bearing must be dropped.

For macro pages: process AFTER the per-ticker pass, ONCE.

For LOG.md: append exactly one line.
For INDEX.md: rewrite the last_updated cells for any page you touched.

Hard rules:
- Never delete a ticker folder. (That is the compactor's job, after a 60-day idle window.)
- Never grow a page past target_words by more than 20%.
- Never write a thesis change without naming what falsified the prior thesis.
- If you have nothing to add to a page, do not rewrite it.
- Hard ceiling of 30 page outputs in this dispatch. If the inputs imply more than 30, the orchestrator will have already shrunk your scope — process only the tickers and pages explicitly listed in this dispatch.

Return a JSON manifest at the end listing { page: action } where action is one of {rewrote, appended, untouched, error}.
```

Failure mode: if the curator's output fails the size or front-matter linter (deterministic check after the agent runs), the orchestrator logs the issue to `runs/<id>/wiki_curator_error.txt`, leaves the wiki **unchanged**, and proceeds to `finalize.py`. Trade decisions are never blocked by curator failure.

---

## 5. Compactor / Linter

The compactor is non-optional. Without it the wiki rots within ~30 runs.

### 5.1 What it checks

| Check | Pages | Auto-fix? |
|---|---|---|
| **Word budget** — page exceeds `target_words` by >20% | every page | yes — re-runs curator on that page in compaction mode |
| **Trade tiering** — closed trades >30d still in detail block | `trades.md` | yes — rolls into monthly summary |
| **Trade tiering** — closed trades >180d still as monthly lines | `trades.md` | yes — rolls into YTD summary |
| **Recent pruning** — bullets older than 30d | `recent.md` | yes — drops |
| **Log rolling** — entries >60d / >365d | `LOG.md` | yes — rolls |
| **Orphan ticker** — folder for ticker with no run + no open position in 60d | `tickers/<T>/` | yes — moves to `_archive/` |
| **Stale page** — page not touched in `stale_after_days` (default 30) | every page | flag only — human review |
| **Contradiction** — `thesis.md` bullish but last 5 closed trades on this ticker were all losses | per ticker | flag only |
| **Contradiction** — page cites a run id that isn't in `runs/index.json` | every page | flag only |
| **Broken cross-ref** — relative link in any page resolves to a missing file | every page | flag only |
| **Front-matter integrity** — YAML missing required keys | every page | flag only |

### 5.2 When it runs

- **Independent Sunday cron**, run by a dedicated cron entry that invokes `scripts/wiki_compactor.py` directly. **Not** routed through `/autorun`. `/autorun` only fires on weekday market days; the compactor needs to run when there is no trading activity, so it owns its own schedule. Recommended cron: `0 16 * * 0` (Sunday 4 PM local) — a separate entry next to the existing `/autorun` cron, not a modification of it.
- **On demand**, via a manual `python -m scripts.wiki_compactor [--dry-run]` invocation.
- **NOT** on every run — that would couple compactor latency to trade timing. The curator handles per-run upkeep; the compactor handles rot.

### 5.3 Output

- `wiki/meta/compactor_log.md` — one section per compactor run, listing what was rolled, what was archived, what was flagged.
- `scripts/wiki_lint_report.md` — written every compactor run; if non-empty, the compactor's own stdout (cron output) surfaces it to the user as an action item ("X items in wiki need human review"). Not routed through `/autorun`.
- `--dry-run` mode writes the report but makes no edits.

### 5.4 Surfacing problems

When `wiki_lint_report.md` has any items in flag-only categories (stale, contradiction, broken xref, front-matter), the compactor's stdout summary (printed at the end of its Sunday run) ends with a one-line "Wiki review needed: N items at scripts/wiki_lint_report.md." Because the compactor is its own cron, that message lands in the cron's output (mailed/logged per the user's cron setup), not in `/autorun`. The user reads the report and either edits the wiki manually or runs the curator with a hint.

---

## 6. Integration Points

Exact code-level touch list. Each item lists the file and the change.

| File | Status | Change |
|---|---|---|
| `wiki/` (new directory) | create | top-level wiki tree per §1 |
| `ai_hedge/wiki/__init__.py` | new | package |
| `ai_hedge/wiki/manifest.py` | new | per-agent page manifest dict + `pages_for(agent)` lookup |
| `ai_hedge/wiki/inject.py` | new | `inject_context(run_id, tickers, mode)` writes `wiki_context` into facts bundles |
| `ai_hedge/wiki/loader.py` | new | `read_tldr(path)`, `read_full(path)`, front-matter parser |
| `ai_hedge/wiki/templates.py` | new | string templates for each page type (used by bootstrap + curator's first-write fallback) |
| `ai_hedge/wiki/lint.py` | new | size + front-matter + cross-ref checks (importable; used by curator post-write and compactor) |
| `ai_hedge/runner/prepare.py` | modify | after `build_swing_facts()` for swing mode, call `wiki.inject.inject_context(run_id, tickers, mode="swing")` |
| `ai_hedge/runner/finalize.py` | modify | after `close_run()`, call `wiki.inject.touch_index(run_id)` to keep INDEX.md last_updated dates fresh |
| `ai_hedge/personas/swing_facts_builder.py` | **no change** | `wiki_context` is added to facts files post-build, not embedded here, so the builder's contract is unchanged |
| `ai_hedge/personas/prompts/swing_trend_momentum.md` | modify | one paragraph: "Your facts bundle may include a `wiki_context` block with prior chart state and macro regime read. Use it as memory; on contradiction, current data wins — flag the contradiction in your reasoning." |
| `ai_hedge/personas/prompts/swing_mean_reversion.md` | modify | same paragraph, calling out `recent.md` |
| `ai_hedge/personas/prompts/swing_breakout.md` | modify | same paragraph, calling out S/R levels |
| `ai_hedge/personas/prompts/swing_catalyst_news.md` | modify | same paragraph, but stronger — wiki catalysts page IS the priority view |
| `ai_hedge/personas/prompts/swing_macro_context.md` | modify | same paragraph, regime + sectors are the priority view |
| `ai_hedge/personas/prompts/swing_head_trader.md` | **no change** | this agent has no wiki context per manifest |
| `ai_hedge/personas/prompts/swing_portfolio_manager.md` | modify | new sub-section under "Current portfolio state": "If your decision contradicts the wiki thesis (`tickers/<T>/thesis.md` TL;DR), flag the contradiction in `reasoning` with a 'thesis-update warranted' note. Do **not** apply a fixed confidence penalty — the threshold may be tuned later from telemetry." |
| `ai_hedge/personas/prompts/wiki_curator.md` | new | the curator system prompt per §4.3 |
| `ai_hedge/personas/prompts/wiki_bootstrap.md` | new | the one-time bootstrap prompt per §7 |
| `.claude/skills/swing/SKILL.md` | modify | new **Step 7.5 — Wiki Curator** between explainer and `finalize.py`; also a one-line reminder in Step 1 to ensure `wiki/` exists |
| `scripts/wiki_compactor.py` | new | weekly compactor CLI |
| `scripts/wiki_lint.py` | new | thin wrapper over `ai_hedge.wiki.lint` for ad-hoc human-run linting |
| `scripts/wiki_bootstrap.py` | new | one-time bootstrap orchestrator (calls the bootstrap agent per ticker) |
| `tracker/watchlist.json` | modify | add `wiki_enabled: true|false` feature flag (read by `prepare.py` to decide whether to call `wiki.inject.inject_context`) |
| `tracker/cli.py` | **no change** | `/autorun` does NOT route the compactor; the compactor is its own Sunday cron entry per §5.2 |
| _user's crontab_ | new entry | one-line cron `0 16 * * 0 cd /Users/naman/Downloads/artist && .venv/bin/python -m scripts.wiki_compactor` — not a project-tracked file, but worker should document the line in `scripts/wiki_compactor.py`'s docstring |
| `CLAUDE.md` | modify | new "Wiki Memory" section + Step 7.5 in pipeline diagram (head terminal does this — see §12) |
| `AGENTS.md` | modify | mirror CLAUDE.md changes (head terminal does this) |
| `scripts/check_docs_drift.py` | modify | also count agent prompts mentioning `wiki_context` and fail if mismatched (head terminal does this) |

The PM prompt change is the only place where wiki affects an actual decision — the strategy agents are told "current data wins on contradiction," so the wiki is purely additive context for them.

---

## 7. Seeding / Migration

The wiki must be populated for tickers we already trade before the first wiki-aware run, or every agent will see `{"new_ticker": true}` and the memory layer adds zero value for the first 30+ days.

**Bootstrap timing is fixed:** bootstrap runs **before** the next swing routine fires. The script's first action is a runtime check that aborts if `runs/index.json` shows any entry with `status == "in_progress"`. Operationally: stop scheduled routines (or wait for their natural completion) → run bootstrap → unblock routines.

### 7.1 Bootstrap process

A one-time `scripts/wiki_bootstrap.py` does this in three passes:

1. **Identify the universe.** Read tickers from:
   - `tracker.db` rows with `status in ('pending', 'entered', 'target_hit', 'stop_hit', 'expired')` and `created_at` within the last 90 days.
   - `tracker/watchlist.json` configured tickers.
   - Union, deduplicated, uppercase.
   Expected size: 10–20 tickers.

2. **Bootstrap macro pages first.** Read the most recent successful run from `runs/index.json` (`status == 'completed'`), pull `web_research/*.json`, dispatch one `wiki_bootstrap` agent that writes:
   - `wiki/macro/regime.md`
   - `wiki/macro/sectors.md`
   - `wiki/macro/calendar.md` (this part is deterministic — no agent needed)

3. **Bootstrap per-ticker pages.** For each ticker, dispatch one `wiki_bootstrap` agent (parallel batch of ~5 at a time):
   - Reads the **last 5 swing runs** for that ticker from `runs/index.json` (filtered by ticker).
   - For each run, pulls `decisions.json`, the relevant strategy signals, and `web_research/<TICKER>.json`.
   - Reads ALL `tracker.db` rows for that ticker (open + closed, full history).
   - Writes `thesis.md` (synthesizing the 5-run narrative), `technicals.md` (from the most recent run), `catalysts.md` (from the most recent web_research), `trades.md` (deterministic from `tracker.db`), and `recent.md` (one dated bullet per material change in the last 30 days).

4. **Bootstrap meta pages.** After all ticker pages exist, dispatch one `wiki_bootstrap` agent that writes:
   - `meta/lessons.md` (synthesized from all closed trades).
   - `meta/playbook.md` (deterministic from `tracker.db` — no agent needed).

5. **Run the compactor in dry-run mode** to validate the bootstrap output: word budgets respected, no contradictions, no orphans, all front-matter present.

Cost: ~15 ticker × ~3 minutes per Agent dispatch × 5-at-a-time batches = ~15 minutes wall. One-shot, never repeated.

### 7.2 Migrating without bootstrap

If we ship the curator before bootstrap completes (e.g. urgent need), the curator handles a missing page by writing a fresh skeleton from the templates module, with a placeholder TL;DR and `last_updated == today`. Subsequent runs flesh out the skeleton naturally. The cost is that the **first 3–5 runs after launch see weak `wiki_context`** — they get only what today's run added. This is acceptable as a fallback but bootstrap is preferred.

---

## 8. Storage + Growth Budgets

### 8.1 Page sizes

| Page type | Target | Bytes (rough) |
|---|---|---|
| `thesis.md` | 500 words | ~3 KB |
| `technicals.md` | 350 words | ~2 KB |
| `catalysts.md` | 400 words | ~2.5 KB |
| `trades.md` | varies by history | 2–8 KB |
| `recent.md` | 250 words | ~1.5 KB |
| `regime.md` | 400 words | ~2.5 KB |
| `sectors.md` | 250 words | ~1.5 KB |
| `calendar.md` | 200 words | ~1 KB |
| `lessons.md` | 400 words | ~2.5 KB |
| `playbook.md` | 400 words | ~2.5 KB |
| `INDEX.md` | grows with N pages | ~2 KB at month 1, ~5 KB by month 24 |
| `LOG.md` | rolling capped | ~50 KB max |

### 8.2 Total wiki size projections

Assuming a stable universe of ~15 tickers tracked at any time, with ~10 per quarter cycling out via the orphan rule:

| Horizon | Tickers active | Tickers archived | Total wiki size |
|---|---|---|---|
| Month 1 | 15 | 0 | ~200 KB |
| Month 6 | 15 | ~25 | ~600 KB (counting archive) |
| Month 24 | 15 | ~80 | ~1.5 MB |

Trivial in git terms. The compactor's tiered rolling on `trades.md` and `LOG.md` means the bulk of growth comes from the archive — which is git-stored but not read.

### 8.3 Per-agent context overhead (the cost we actually care about)

Agents currently read facts bundles of ~6 KB. Adding `wiki_context`:

| Agent | Wiki bytes added | Tokens added (est.) |
|---|---|---|
| `swing_trend_momentum` | ~600 (2 TL;DRs) | ~150 |
| `swing_mean_reversion` | ~600 | ~150 |
| `swing_breakout` | ~2 KB (full technicals) | ~500 |
| `swing_catalyst_news` | ~3.5 KB (full catalysts + calendar) | ~900 |
| `swing_macro_context` | ~4.5 KB (full regime + sectors + thesis TL;DR) | ~1100 |
| `swing_head_trader` | 0 | 0 |
| `swing_portfolio_manager` | ~5 KB (trades full + thesis TL;DR + lessons TL;DR) | ~1250 |

**Per-run overhead:** ~4000 tokens added across all agents combined. Against a baseline ~80,000-token swing run, that's ~5%. Within the monthly subscription cap.

---

## 9. Edge Cases

1. **First-ever run for a new ticker, no wiki yet.** `wiki_context = {"new_ticker": true}`. Strategy agents see the `new_ticker` flag and skip the "compare to memory" reasoning. The curator at the end of the run creates skeleton pages from templates.

2. **Wiki page exists but is stale (>`stale_after_days`).** The injector adds `"stale": true` to the relevant slice. The agent prompt instruction is: "if `wiki_context.stale` is true, weight the prior view as background only — do not let it override fresh data." The compactor flags stale pages for human review.

3. **Curator fails mid-run.** Step 7.5 is wrapped in try/except (well, the SKILL.md equivalent — the agent dispatch is followed by a check on its return file). On failure: log to `runs/<id>/wiki_curator_error.txt`, leave the wiki unchanged, proceed to `finalize.py`. The trade decision is already final by Step 6 — wiki failure must never block trade execution.

4. **Two tickers in the same run trying to update `macro/regime.md`.** Impossible by construction: the curator processes per-ticker pages in a per-ticker pass, then macro pages in a single run-level pass. The prompt enforces this ordering explicitly. There is one curator agent per run, not one per ticker.

5. **Wiki vs. current data conflict ("wiki says bullish thesis but today's run is bearish").** Agents are instructed: current data wins on contradiction; flag the contradiction in `reasoning`. The PM is instructed: if your decision contradicts the wiki thesis, add a "thesis-update warranted" note in `reasoning` — **no fixed confidence penalty** (per §0; threshold may be tuned later from telemetry once we see whether contradictions correlate with losses). The curator will then likely rewrite the thesis page on this same run.

6. **Bootstrap fires while a routine is mid-run.** Bootstrap should only run when no swing routine is in flight. `scripts/wiki_bootstrap.py` checks `runs/index.json` for in-progress runs and refuses to run if any exist.

7. **Orphan ticker reactivation.** If a ticker was archived but appears in a new run, the bootstrap of that ticker re-emerges from `_archive/`. Curator restores the folder + appends a `## reactivated <date>` line to its `recent.md`.

8. **Ticker symbol change (e.g. FB → META).** Out of scope for v1; resolved manually with a `git mv` and a hand-edit. Fewer than 1 per year for our universe.

9. **Two runs in the same day for the same ticker (rare, but possible during testing).** The curator runs after each. Per-ticker pages may be rewritten twice the same day; that's fine because the rule is synthesis, not append. `LOG.md` gets two entries.

10. **Compactor finds a thesis that contradicts trade history.** Flag-only. The compactor cannot rewrite the thesis itself — that requires the curator. The flag prompts the user to either run the curator with a thesis-rewrite hint or hand-edit the page.

11. **Run with >6 tickers (curator output exceeds 30 pages).** Orchestrator splits the curator into two dispatches per §4.2 hard rules: A covers tickers 1..N/2 (per-ticker pages only); B covers tickers N/2+1..N AND the macro + INDEX + LOG pass. Both dispatches share the same `run_id` so `LOG.md` still gets exactly one new entry (written by dispatch B). If dispatch A fails but B succeeds, the failed tickers' pages are left unchanged and logged to `runs/<id>/wiki_curator_error.txt`; B still completes the macro pass.

---

## 10. Validation Plan

### 10.1 Smoke tests (pre-merge)

1. **Bootstrap on synthetic data.** Construct a fake `runs/` tree with 3 tickers × 3 runs each, and a fake `tracker.db`. Run `scripts/wiki_bootstrap.py`. Verify all expected pages exist with valid front-matter and within budget.
2. **Inject + read round-trip.** With a real wiki, run `wiki.inject.inject_context()` for a synthetic run id; assert each agent's facts file has a `wiki_context` block matching its manifest.
3. **Curator dry-run.** Feed the curator a real run's outputs. Assert: only pages flagged by manifest get rewritten; word budgets respected; front-matter updated.
4. **Linter rejects oversized writes.** Manually inflate a page beyond 120% of target; run lint; confirm it flags.
5. **Compactor tier rolling.** Construct a `trades.md` with synthetic 90-day-old trades; run compactor; confirm they got rolled to monthly summaries.
6. **Curator failure doesn't block finalize.** Force the curator to return malformed JSON; confirm `finalize.py` still runs and `runs/index.json` is closed properly.

### 10.2 Telemetry-only decision-quality test (no A/B alternation)

The first draft proposed an A/B alternation between wiki-on and wiki-off runs. That has been dropped — paper trades are real enough that we don't want a deliberately-degraded control arm. Instead, use a natural before/after split using telemetry already in our pipeline:

- Add a `wiki_used: bool` column to the `Trade` table (true on every row created after the wiki ships; false on rows that pre-date it).
- Have the PM agent's "thesis-update warranted" note be captured as a structured field in the run's `decisions.json` (not just inside free-text reasoning), so a separate counter can roll it up.
- Compare **pre-wiki** trades (existing rows) vs **post-wiki** trades (new rows) on:
  - win rate
  - median R-multiple
  - average PM confidence
  - frequency of "thesis-update warranted" flags per closed trade
- Use the existing `tracker/backtest.py` runner extended with a `--split-on wiki_used` flag.

Decision threshold: if post-wiki win rate or median R is materially worse than pre-wiki after 50+ closed trades on each side, suspect the wiki is hurting and only **then** escalate to a real A/B (turn `wiki_enabled` on/off in `watchlist.json` for alternating weeks). Default expectation: post-wiki should be at least flat or slightly better; the goal here is mostly to detect rot, not prove uplift.

### 10.3 Long-term readability check

At month 6, hand a fresh reader (a person who hasn't seen the wiki) the `INDEX.md` and ask them to summarize the bull case for any 3 tickers in 5 minutes. If they can do it, the wiki is succeeding at synthesis. If pages are too long or contradictory, compaction needs tuning.

### 10.4 Rot detection

The compactor's `wiki_lint_report.md` count is itself a metric: if it grows unboundedly run-over-run, the curator is not producing clean writes. Watchdog threshold: >10 flagged items at any compactor run is a problem.

---

## 11. Estimated Effort

### Phase 1 — MVP (~2–3 days of focused implementer work)

Goal: a working wiki for the swing-stock pipeline, even if not all page types or all agents.

- 5 page templates: thesis, technicals, catalysts, trades, regime.
- `ai_hedge/wiki/` package with `manifest.py`, `inject.py`, `loader.py`, `lint.py`, `templates.py`.
- `wiki_curator.md` prompt.
- `wiki_bootstrap.md` prompt + `scripts/wiki_bootstrap.py` runner.
- SKILL.md Step 7.5 added.
- `prepare.py` injector hook.
- 5 strategy agent prompts get the "wiki_context" paragraph.
- `INDEX.md`, `LOG.md` minimal.
- Files to create: ~13. Files to modify: ~7.

### Phase 2 — Full schema (~3–4 days)

- Add `recent.md`, `sectors.md`, `calendar.md`, `lessons.md`, `playbook.md`.
- PM prompt update for thesis-contradiction rule.
- `scripts/wiki_compactor.py` with all tiering rules.
- `scripts/wiki_lint.py`.
- `wiki_used` column on `Trade` table for telemetry (per §10.2).
- `decisions.json` schema extension to capture the PM's "thesis-update warranted" flag as a structured field (not just free text).
- `tracker/backtest.py` extended with `--split-on wiki_used` for the natural before/after comparison.
- Independent Sunday cron entry for the compactor (documented in `scripts/wiki_compactor.py` docstring; user's crontab modification is operational, not in-repo).
- Files to create: ~4. Files to modify: ~4.

### Phase 3 — Validation + tuning (~2 weeks elapsed, ~1 day actual work)

- Collect 2 weeks of post-wiki runs. Use the telemetry-only natural before/after comparison from §10.2 — no A/B alternation.
- Tune word budgets based on what actually compacts cleanly.
- Add or drop pages based on what agents actually used.
- Decide whether the PM thesis-contradiction flag warrants a confidence penalty (currently 0 per §0); revisit only if the data shows contradictions correlate with losses.
- Files to modify: 2–3.

### Total

- **Files created:** ~18
- **Files modified:** ~14
- **Implementer time:** ~5–7 working days for phases 1+2.
- **Calendar time:** ~3 weeks elapsed including phase 3 soak.

Phase 1 is the **must-ship** before any decision-quality claim can be made. Phase 2 is the polish that makes the system survive past month 3. Phase 3 decides whether the experiment goes from "interesting" to "default-on."

---

## 12. The Gap in Our Current Docs

The user explicitly flagged that `CLAUDE.md`, `AGENTS.md`, and `scripts/architecture_audit.md` are partially out of date. Here is what is stale today **before** the wiki ships, and what the head terminal will need to update **after** Phase 1 lands. The implementing worker should NOT touch these — flagging only.

### What is stale today (independent of the wiki work)

- **`CLAUDE.md`**, in the table on line ~46 and the audit recap section, lists Sin #5 ("No portfolio memory across runs") as "shipped with #1 (same fix)." That fix only addresses the in-run portfolio state — there is still no cross-run thesis memory until the wiki lands. The current language overstates progress.
- **`CLAUDE.md`** still mentions "9 swing strategy agents" in some prose paragraphs even though the table at the top correctly says 5. (The Sin #3 collapse happened the same day. `swing_facts_builder.py:10` docstring also still says "9 strategy signals.")
- **`AGENTS.md`** is a near-duplicate of CLAUDE.md but with `Codex` replacing `Claude Code` — same staleness propagated.
- **`scripts/architecture_audit.md`** lists Sin #3 as `⏳` in the headline table even though the collapse landed today (per the brief). The Sin #5 + #1 framing implies "fully solved" when the cross-run memory piece is still missing.
- The "Wave 4 — Live Dashboard" pre-reqs section in `architecture_audit.md` lists "memory across runs" as already done (via #1). After the wiki ships, that pre-req should explicitly point at the wiki.

### What the head terminal will need to update AFTER Phase 1 lands

- **`CLAUDE.md`:** add a "Wiki Memory Layer" subsection under the architecture section. Add Step 7.5 (Wiki Curator) to the pipeline diagram. Add `wiki/` to the project tree drawing. Update the Sin #5 line to point at the wiki as the actual cross-run memory implementation.
- **`AGENTS.md`:** mirror the CLAUDE.md changes.
- **`scripts/architecture_audit.md`:** mark Sin #5 as fully addressed only after Phase 1 + Phase 2 ship and the side-by-side validation produces a positive read. Until then, mark it as "partially addressed — see wiki memory layer (Phase 1 shipped / Phase 2 in flight)."
- **`scripts/check_docs_drift.py`:** add a check that for every entry in `ai_hedge/wiki/manifest.py`, the corresponding agent prompt mentions `wiki_context`. Fails the build if drift.
- **`RUN_PLAYBOOK.md`** (not in the read list, but should be updated): add Step 7.5 alongside the existing Step 7.

### What's intentionally left out of this plan

- Crypto modes (quarantined, per user constraint).
- Daytrade and invest modes (focus is swing-stock only).
- A UI for browsing the wiki (Wave 4 dashboard, separate concern).
- A vector store or embedding index over the wiki — Karpathy's spec is explicit that the wiki itself **is** the index, with `INDEX.md` as the table of contents. We follow that.
- Full CRDT-style conflict resolution. We rely on the per-run / per-page ownership constraint instead.

---

_Plan ends. The implementing worker should start with Phase 1 and ship MVP behind a feature flag (`wiki_enabled` boolean in `tracker/watchlist.json`) so the first wave can be tested against a few runs before being defaulted on._
