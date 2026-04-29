# AI Hedge Fund — Architecture Audit & Solutions

_Generated 2026-04-27. Plain-English diagnostic for a non-technical owner. Each problem is paired with its proposed fix._

> **CRITICAL UPDATE 2026-04-27 (afternoon):** Three of the original "sins" (#8, #11, #15) were framed as if this code calls the Anthropic API directly. **It doesn't.** All work runs inside Claude Code via the user's $140/month subscription. There is no per-token bill. The accounting unit is "monthly usage cap consumed" and "routine reliability." A new central sin **#19 (Claude Routines reliability)** has been added at the bottom. The waves and cost estimates have been re-thought through this lens — see "Architectural decision needed" near the end._

---

## TL;DR — what's broken, in 30 seconds

**Status legend:**
- ✅ **Fixed + validated** — code change shipped AND verified by a smoke test that actually exercised the changed code path
- 🟢 **Fixed in code, not yet observed in production** — code change shipped, unit/smoke tested, but a real LLM-firing routine has not yet exercised it (so we know the code works, we don't yet know the live system behaves correctly)
- 🔵 **In progress** — being worked on now
- ⏳ **Not started**
- 🔁 **Re-scoped** — original framing was wrong; replaced with a different fix; now in a later wave

| #  | Problem | 🔴/🟠/🟡 | Fix effort | Status |
|---:|---------|:------:|:----------:|:-------|
| 1  | Portfolio Manager pretends $100k cash every run | 🔴 | medium | ✅ shipped + smoke-tested (NVDA buy correctly blocked; allowed_actions verified) — real routine fire pending |
| 2  | Routines fire 2×/day for 5–20-day swing trades | 🔴 | tiny | ⏳ |
| 3  | 7 redundant strategy agents | 🟠 | medium | ✅ shipped — collapsed to 5 distinct viewpoints (swing_trend_momentum / swing_mean_reversion / swing_breakout / swing_catalyst_news / swing_macro_context); old 6 archived |
| 4  | No deterministic screening tier (LLM analyzes everything) | 🔴 | medium | ⏳ |
| 5  | No portfolio memory across runs | 🔴 | medium | 🟢 partial — in-run portfolio state shipped with #1; cross-run thesis memory shipped behind feature flag (Wiki Memory Phase 1, `settings.wiki_enabled` default OFF) |
| 6  | Cache never expires (stale prices) | 🔴 | tiny | 🟢 shipped + unit-tested (TTL eviction verified) — production fire pending |
| 7  | WebSearch results deleted after use | 🟠 | tiny | 🟢 shipped (prompt-only edit) — **NOT yet observed: needs a real web_researcher Agent run to confirm raw-save lines fire** |
| 8  | Cost reduction (was prompt caching) | 🔴 | medium | 🔁 re-scoped to Wave 3 — see Sin #8 below |
| 9  | No earnings blackout | 🟠 | small | ✅ shipped + smoke-tested (AAPL 3-days-out blocked, NVDA 23-days clean) |
| 10 | Correlation computed and ignored | 🟠 | small | ✅ shipped + smoke-tested (BAC 74% corr w/ JPM blocked; XOM 0.9% corr clean) |
| 11 | Confidence scores uncalibrated | 🟠 | medium | ⏳ defer until 50+ closed trades exist |
| 12 | No central run index | 🟡 | tiny | 🟢 shipped + unit-tested (open/close roundtrip) — **NOT yet observed: no real run has fired since the index was added, so `runs/index.json` is still empty** |
| 13 | Failures silent in `aggregate.py` | 🔴 | tiny | 🟢 shipped + unit-tested (loader flags missing) — **NOT yet observed: needs a real run with a missing agent to confirm `degraded_inputs` field surfaces correctly** |
| 14 | CLAUDE.md / code drift | 🟠 | small | ✅ shipped + drift CI check passes |
| 15 | No token budget per run | 🟠 | small | ⏳ |
| 16 | Static stops, no management | 🟠 | medium | ⏳ |
| 17 | No SPY benchmark | 🟠 | tiny | ✅ shipped + verified in actual reports (you trail SPY by ~5pts, painful but real) |
| 18 | Documentation lies (meta) | 🔴 | small | ✅ shipped (same fix as #14) |
| 19 | Claude Routines reliability (Anthropic-side bugs) | 🔴 | depends on Option A/B/C | ⏳ pending architectural decision |
| 20 | Silent JSON parse failures hide head trader output | 🔴 | small | 🟢 shipped + fault-injection tested — raises HeadTraderSynthesisFailed; all agents now pin model: sonnet |

**Score: 11 of 19 sins fixed in code (58%) — Sin #3 (swing 9→5) shipped after the 2026-04-27 sweep. Sin #5 remains "partial" because the cross-run wiki memory layer is feature-flagged OFF until validated. (#19 is an Anthropic-side issue, not a code fix.)**

**Note on validation status (2026-04-27 fix pass):** The original 9-fix validation run confirmed 7 of 9 cleanly. 2 issues surfaced: #7 web research not in RUN_PLAYBOOK.md (now fixed), and #20 head trader silent failures (now fixed with raise + Pydantic validation). The 7 confirmed fixes remain valid; re-validate #7 and #20 on the next real run.

**Bottom line:** All four critical-and-tiny sins (#6, #12, #13, #14/#18) are now in code. Sin #20 (head trader silent failures) is now also fixed. The next-biggest wins are operational — splitting routines smaller (#2), collapsing redundant agents (#3), and adding a deterministic screener (#4) — all deferred to a later sprint after the data layer is honest.

---

## The 18 sins, with proposed solutions

### Sin #1 — PM has no portfolio state
**Status: ✅ shipped + smoke-tested 2026-04-27.** Code change exercised via end-to-end smoke run on AAPL+NVDA. `compute_allowed_actions()` correctly blocks `buy` for NVDA when 6 shares are already held; `sell`/`short` still permitted. `signals_combined.json` shows `portfolio.positions` lot-aggregated and `portfolio.cash` reduced by exposure. ⚠️ A real LLM PM has not yet read this injected state — once a swing routine fires post-fix, verify the PM actually respects the "Current portfolio state" section in its prompt.

**Problem (plain English):** The Portfolio Manager (the AI that decides which trades to take) starts every run thinking you have $100,000 sitting in cash, even when most of it is locked in 8 open trades. It's like a chef who walks into the kitchen every morning and starts a fresh shopping list, ignoring the food already in the fridge — they double-buy milk and run out of fridge space.

**Evidence:** `ai_hedge/portfolio/allowed_actions.py:121-131` initializes positions at zero, never reads `tracker.db`.

**Severity:** 🔴 Critical · **Fix effort:** medium

**Fix (plain English):** Before the PM agent runs, read open positions from `tracker.db`, format them as a small table, and inject that into the PM prompt as immutable context. Also pass actual remaining cash (paper capital minus open exposure) to `allowed_actions.py`. The PM still makes its own decisions — we just stop it from making them with bad data.

**Files touched:**
- `ai_hedge/portfolio/allowed_actions.py` — accept `current_positions`, `available_cash`
- `ai_hedge/runner/aggregate.py` — load DB rows before PM dispatch
- `ai_hedge/personas/prompts/swing_portfolio_manager.md` — add "Current portfolio" section

**Depends on:** none. **Risk:** First runs may behave conservatively when they suddenly see existing positions. Test with a known portfolio state.

---

### Sin #2 — Routines fire 2×/day for 5–20-day swing trades

**Problem:** Anthropic Routines fire twice every weekday (Stock Swing Batch 1 at 18:30 UTC, Batch 2 at 23:30 UTC). Swing trades hold 5–20 days. Most runs see no chart change since the last run — you're paying full price for the same answer over and over. CLAUDE.md falsely claims "4×/day" but the real schedule is 2×/day.

**Evidence:** Cron expressions `30 18 * * 1-5` and `30 23 * * 1-5` in the Anthropic Routines triggers (verified by Playwright pull this session).

**Severity:** 🔴 Critical · **Fix effort:** tiny

**Fix:** Edit each Anthropic Routine schedule via the web UI (claude.ai/code → Routines) or PATCH `/v1/code/triggers/<trigger_id>` with a new cron — recommended `0 18 * * 1-5` (once daily, 6 PM UTC, weekdays only).

**Files touched:**
- Anthropic Routines (web UI / API) — no codebase file change
- `CLAUDE.md` — fix the "4×/day" line (overlaps with #14)

**Depends on:** none. **Risk:** None. Pure cost reduction.

---

### Sin #3 — Seven redundant strategy agents
**Status: ✅ shipped 2026-04-29.** Collapsed to 5 genuinely distinct viewpoints: `swing_trend_momentum`, `swing_mean_reversion`, `swing_breakout`, `swing_catalyst_news`, `swing_macro_context`. Old prompts archived at `ai_hedge/personas/prompts/_archive/`. `swing_facts_builder.SWING_AGENTS` updated; `aggregate.py:_expected_agents()` updated; `swing_head_trader.md` rewritten for 5 inputs; both `.agents/skills/swing/` and `.claude/skills/swing/` SKILL.md dispatches updated. The drift CI confirms `swing=5` matches code.

**Problem:** You have 7 swing strategy agents staring at the same chart (trend follower, pullback trader, breakout, momentum ranker, mean reversion, catalyst, sector rotation). Most use overlapping indicators (RSI, EMAs, MACD) and ~70% of the time converge on the same call. It's like asking 7 doctors who trained at the same school — you get one opinion, just yelled 7 times.

**Evidence:** `ai_hedge/personas/swing_facts_builder.py:383-391` lists 7 agents (CLAUDE.md says 9 — doc drift, see #14).

**Severity:** 🟠 Major · **Fix effort:** medium

**Fix:** Collapse to 3 agents that disagree on purpose:
- **Trend follower** — rides momentum ("winners keep winning")
- **Mean reversion trader** — bets on snapbacks ("extremes don't last")
- **Catalyst-driven trader** — acts on news, earnings, sector rotation ("react to events")

These 3 will frequently disagree, which is exactly the diversity you want. Archive the other 4 prompts in `personas/prompts/_archive/` (don't delete — useful as reference).

**Files touched:**
- `ai_hedge/personas/swing_facts_builder.py` — `SWING_AGENTS` reduced to 3
- `ai_hedge/personas/prompts/swing_*.md` — keep 3, archive 4
- `ai_hedge/personas/prompts/swing_head_trader.md` — synthesis prompt updated for 3 inputs

**Depends on:** none. **Risk:** Backtest the new 3-agent system against historical predictions before going live; win-rate should be similar or better, cost will drop ~57%.

---

### Sin #4 — No deterministic screening tier

**Problem:** Every routine analyzes all 14 watchlist tickers with full LLM cost, even on days when nothing has meaningfully changed. It's like a chef cooking 14 dishes every morning whether anyone ordered them or not — most go in the trash. Real funds use cheap rules first to find 0–3 names worth deeper analysis.

**Evidence:** No `screening/` module exists. `ai_hedge/runner/prepare.py` runs facts_builder over the full ticker list unconditionally.

**Severity:** 🔴 Critical · **Fix effort:** medium

**Fix:** Add `ai_hedge/screening/swing_screener.py`. Cheap rules using already-cached prices: RSI < 30 or > 70, breakout above 20-day high, volume > 1.5× 20-day avg, gap > 2%. Output: list of 0–3 candidate tickers. The routine runs the LLM analysis ONLY on candidates. Most days the screener finds 0 — the routine writes "no trades today" and exits costing essentially nothing.

**Files touched:**
- `ai_hedge/screening/swing_screener.py` — new
- `ai_hedge/runner/prepare.py` — call screener, filter ticker list
- Routine prompt — add a "if screener returns 0 candidates, exit" branch

**Depends on:** #6 (cache TTL — screener relies on fresh prices). **Risk:** First weeks of "no trades today" may feel like the system broke. It hasn't — it's behaving like a real fund. Add a daily summary log: "Screener checked 14 names, 0 candidates met criteria."

---

### Sin #5 — No portfolio memory across runs
**Status: 🟢 partial — in-run portfolio state shipped with Sin #1 (2026-04-27). Cross-run thesis memory shipped 2026-04-29 as Wiki Memory Phase 1, behind a feature flag (`tracker/watchlist.json:settings.wiki_enabled`, default OFF). Will flip to ✅ once the wiki has been enabled and validated against a real run cycle.

**Problem:** Same root cause as #1, plus the model has no idea what it decided yesterday. It can re-buy a stock it already bought.

**Evidence:** Same as #1.

**Severity:** 🔴 Critical · **Fix effort:** medium

**Fix:** Solved together with #1 + #12. When #1 ships, the PM sees current positions. When #12 ships (run index), the PM also sees the last 5 runs' decisions. Together: full memory.

**Files touched:** see #1 and #12.

**Depends on:** #1, #12. **Risk:** none beyond what those two cover.

---

### Sin #6 — Cache never expires
**Status: 🟢 shipped + unit-tested 2026-04-27.** TTL eviction verified with fast-clock test (set→sleep past TTL→get returns None). ⚠️ Not yet observed in production — a real run has to actually re-fetch a stale entry to confirm the user-visible behavior. Low risk because the change is purely additive (cache miss falls through to provider, which is the original no-cache behavior).

**Problem:** Your data cache (`ai_hedge/data/cache.py`) is in-memory and stores prices forever once fetched. If the Python process stays alive long enough, it'll happily serve a 3-day-old price as "current." It's a fridge with no use-by dates — old milk sits next to new milk and the chef might pour the wrong one.

**Evidence:** `ai_hedge/data/cache.py` — entire file has no expiry logic.

**Severity:** 🔴 Critical · **Fix effort:** tiny

**Fix:** Store an `expires_at` timestamp alongside each cached value. Default TTLs: prices = 1 hour, fundamentals = 24 hours, news = 5 minutes. On lookup, check the timestamp; if expired, re-fetch and update.

**Files touched:**
- `ai_hedge/data/cache.py` — add TTL field, expiry check

**Depends on:** none. **Risk:** Tiny. First run after the change re-fetches everything once (slightly slower). After that, normal speed.

---

### Sin #7 — WebSearch results deleted after use
**Status: 🟢 shipped 2026-04-27 (prompt-only edit).** ⚠️ NOT yet observed in production. The change is an instruction added to `web_researcher.md` and `crypto_web_researcher.md` telling the LLM agent to write raw search results to disk before processing. Whether the agent actually obeys the instruction can only be verified by a real Web Researcher Agent run. **Action item:** after the next swing routine fires, check whether `runs/<id>/web_research/raw/` contains files. If empty, the prompt edit needs strengthening.

**Problem:** The web research agent calls Google, reads headlines, summarizes, decides — then the raw search results vanish. If you ever want to ask "what did the model see Monday morning when it shorted NKE?" — you can't. There's no record. Backtesting the strategy is impossible because re-running tomorrow gives different web results than today.

**Evidence:** `ai_hedge/personas/prompts/web_researcher.md` instructs the agent to write JSON output but does NOT instruct it to persist raw search inputs.

**Severity:** 🟠 Major · **Fix effort:** tiny

**Fix:** Add an instruction to the prompt: "Before processing, save each WebSearch result verbatim to `runs/<run_id>/web_research/raw/<ticker>_search.json`." Then a future audit can replay exactly what the model saw.

**Files touched:**
- `ai_hedge/personas/prompts/web_researcher.md` — append save-to-disk instruction
- `ai_hedge/personas/prompts/crypto_web_researcher.md` — same

**Depends on:** none. **Risk:** Disk usage grows ~50KB per ticker per run. Trivial.

---

### Sin #8 — Cost reduction (RE-SCOPED — original fix was wrong)

**Original claim:** "Add `cache_control` to persona prompts for ~90% cost cut."

**Investigation finding (2026-04-27):** This project does NOT call the Anthropic SDK directly. All LLM work is dispatched through Claude Code's Agent tool from inside skills (`.claude/skills/swing/SKILL.md`, etc.). The Agent tool's caching is managed by Claude Code's runtime — user code can't add `cache_control` blocks.

**Real cost driver:** Persona system-prompt `.md` files are small (~2-4 KB each). The dominant cost per run is the **facts bundle** passed to each agent. For invest mode, 14 personas each receive a fresh copy of `runs/<id>/facts/<persona>__<ticker>.json` — much of which (price history, basic financials, news) is identical across personas. That duplication is what's expensive.

**Severity:** 🔴 Critical · **Fix effort:** medium (was: small — re-estimated after investigation)

**Re-scoped fix:** Build ONE shared context block per ticker (raw prices, news, technical indicators) and have each persona's facts bundle reference it via a relative path. Rewrite the Agent-dispatch step in skills to read the shared block + only the persona-specific helper outputs. This deduplicates ~70% of input tokens per ticker.

This is a structural change, NOT a 1-line `cache_control` wrap. Moving to **Wave 3** (structural).

**Files touched:**
- `ai_hedge/runner/aggregate.py` and persona dispatch sites — wrap prompts in cache_control blocks
- Possibly `prepare.py` for the web researcher

**Depends on:** none. **Risk:** None — prompt caching is opt-in and fully backwards compatible.

---

### Sin #9 — No earnings blackout
**Status: ✅ shipped + smoke-tested 2026-04-27.** AAPL (earnings 2026-04-30, 3 days out) blocked: `remaining_position_limit=0`, `earnings_blackout` field populated, console log `[earnings blackout] AAPL skipped — earnings in 3 days`. NVDA (23 days out) passes through clean. Crypto tickers correctly skip the check. Cache hit verified (~0.0001s vs 0.5s first call).

**Problem:** The model can buy MSFT 10 minutes before MSFT reports earnings. Earnings reports cause 5–15% overnight moves that have nothing to do with technical analysis. Real funds explicitly skip stocks within 3 trading days of their earnings date because the move is essentially a coin flip.

**Evidence:** No earnings calendar import exists. `ai_hedge/deterministic/risk_manager.py` doesn't filter by earnings dates.

**Severity:** 🟠 Major · **Fix effort:** small

**Fix:** Add `ai_hedge/data/earnings_calendar.py` (yfinance has earnings dates free). In `risk_manager.py`, reject any candidate within 3 trading days of its earnings date. Log the rejection: "AAPL skipped — earnings 2026-04-30."

**Files touched:**
- `ai_hedge/data/earnings_calendar.py` — new
- `ai_hedge/deterministic/risk_manager.py` — earnings filter

**Depends on:** none. **Risk:** Some legitimate trades may be skipped during peak earnings season. Acceptable — alternative is gambling.

---

### Sin #10 — Correlation computed and ignored
**Status: ✅ shipped + smoke-tested 2026-04-27.** BAC analyzed against held JPM: blocked with `correlation_blocked=True`, reason "74% correlated with JPM", raw correlation 0.7386. XOM analyzed: passes through (max |corr| with held positions = 0.009). 5 unit tests on the cluster helper all pass (single-linkage at 0.7, NaN handling, negative-correlation absolute-value treatment).

**Problem:** `risk_manager.py` literally builds a correlation matrix between proposed positions and uses it for **nothing**. So you can be long JPM + BAC + GS + WFC and the system thinks that's "4 diversified trades" when it's actually one bet (banks) with 4× the risk. If banks dump, all 4 stop out the same day.

**Evidence:** `ai_hedge/deterministic/risk_manager.py:94-102` computes `correlation_matrix`; lines 158-178 never enforce limits on it.

**Severity:** 🟠 Major · **Fix effort:** small

**Fix:** Use the matrix you already have. Reject any new position with >0.7 correlation to an existing one (or size it down 50%). Cluster cap: max 30% of capital in any single correlation cluster.

**Files touched:**
- `ai_hedge/deterministic/risk_manager.py` — add enforcement

**Depends on:** #1 (need to know existing positions). **Risk:** May reduce trade count further. That's the point — fewer correlated bets = lower drawdown.

---

### Sin #11 — Confidence uncalibrated, no feedback loop

**Problem:** When the model says "70% confident," it's actually right 38% of the time (per the audit we just ran). The model is overconfident by ~2×. Nothing in the codebase adjusts confidence based on track record. It's like a weatherman who says "70% chance of rain" every day and nobody updates his forecast even though it actually rains 38% of the time.

**Evidence:** No `calibration.py` exists. Risk manager doesn't adjust LLM-reported confidence.

**Severity:** 🟠 Major · **Fix effort:** medium

**Fix:** Add `tracker/calibration.py`. Reads closed trades from `tracker.db`, computes per-agent and per-confidence-bucket actual win rates. Risk manager applies a calibration multiplier: if 70%-confidence agent has historically won 38% of resolved trades, multiply its declared confidence by 0.54 before sizing. Re-runs nightly so it stays current.

**Files touched:**
- `tracker/calibration.py` — new
- `ai_hedge/deterministic/risk_manager.py` — apply multiplier

**Depends on:** #1. **Risk:** Initial calibration may be unstable until ~50+ closed trades exist. Use a Bayesian prior to smooth early estimates.

---

### Sin #12 — No central run index
**Status: 🟢 shipped + unit-tested 2026-04-27.** open/close roundtrip verified with mocked file. ⚠️ NOT yet observed in production — `runs/index.json` will only start populating when the next routine actually fires `prepare.py` and `finalize.py` end-to-end. Currently the file does not exist yet on disk because no real run has happened since the change.

**Problem:** No master file lists all the runs you've done. To find what ran on a date, you walk every `runs/*/metadata.json`. The audit work today required scraping Anthropic's web UI with Playwright because there was no such index. It's a library with no card catalog — every search means walking every shelf.

**Evidence:** No `runs/index.json` or equivalent exists.

**Severity:** 🟡 Minor · **Fix effort:** tiny

**Fix:** `prepare.py` appends one line to `runs/index.json` at the start of every run: `{run_id, date, mode, asset_type, tickers, status: "in_progress"}`. `finalize.py` updates with `status: "completed"` (or `"failed"`) at the end.

**Files touched:**
- `ai_hedge/runner/prepare.py` — append index entry
- `ai_hedge/runner/finalize.py` — close index entry
- `runs/index.json` — new (single source of truth)

**Depends on:** none. **Risk:** None.

---

### Sin #13 — Failures silent in `aggregate.py`
**Status: 🟢 shipped + unit-tested 2026-04-27.** `_expected_agents()` returns the right counts per mode (invest=15, swing=9, daytrade=9, research=33). Loader correctly flags missing files (verified by writing 2 of 3 expected → loader logs warning + returns missing list). ⚠️ NOT yet observed in production — the `degraded_inputs` field in `signals_combined.json` only populates when an actual Agent tool call fails to write its signal JSON. Confirmed in code path; needs a real degraded run to validate the head trader / PM see the field.

**Problem:** `aggregate.py` uses `glob.glob('runs/<id>/signals/*.json')` to load agent outputs. If 3 of 7 agents crash and don't write their JSON, glob just skips them with no warning. The head trader synthesizes the surviving 4 and reports a confident "consensus" — which is actually a degraded view from a partial set. You'd never know.

**Evidence:** `ai_hedge/runner/aggregate.py:38-48` — silent glob, no error handling.

**Severity:** 🔴 Critical · **Fix effort:** tiny

**Fix:** Replace the glob with an explicit `EXPECTED_AGENTS` list per mode. After loading, compare what loaded vs what was expected. Missing agents log a warning AND write a `degraded_inputs: ["swing_trend_follower"]` field into `signals_combined.json`, so the head trader sees the gap honestly.

**Files touched:**
- `ai_hedge/runner/aggregate.py` — explicit expected list, gap detection
- `ai_hedge/personas/prompts/swing_head_trader.md` — instructed to acknowledge degraded inputs

**Depends on:** none. **Risk:** None — tighter error handling is strictly better.

---

### Sin #14 — CLAUDE.md / code drift
**Status: ✅ shipped + verified 2026-04-27.** `scripts/check_docs_drift.py` prints `✓ CLAUDE.md matches code: helpers=79, swing=9, dt=9, invest=14`. The CI guard works — if you change one of those counts and forget to update the doc, the next drift-check call fails with exit code 1.

**Problem:** Doc says "9 swing agents" — reality is 7. Says "4×/day" — reality is 2×/day. Says "78 helpers verbatim from upstream" — but `reference/ai-hedge-fund/` has no `helpers.py`. Anyone (you, future-you, an AI assistant in 6 months) reading these docs to make a change is operating on stale information.

**Evidence:** Multiple lines in `CLAUDE.md` confirmed wrong by today's Explore audit.

**Severity:** 🟠 Major · **Fix effort:** small

**Fix:** One-time sweep — rewrite the false claims in CLAUDE.md to match current code. Add a CI check (or pre-commit hook): a tiny script that reads CLAUDE.md and the actual `SWING_AGENTS` list, fails if counts diverge. Same idea for the cron schedule.

**Files touched:**
- `CLAUDE.md` — rewrite inaccurate sections
- `scripts/check_docs_drift.py` — new pre-commit check

**Depends on:** ideally ships AFTER #2 and #3 (so corrected counts are stable). **Risk:** None.

---

### Sin #15 — No token budget per run

**Problem:** No per-run ceiling, max iterations, or alarm exists. One verbose sub-agent on a bad day can spend 10× a normal run, blowing through your monthly Anthropic credit silently. You find out at end of month when the bill arrives.

**Evidence:** No env var, config, or check exists.

**Severity:** 🟠 Major · **Fix effort:** small

**Fix:** Add `MAX_TOKENS_PER_RUN` env var (default ~500,000). `prepare.py` and `aggregate.py` track cumulative token usage from agent responses. Soft limit at 80% logs a warning. Hard limit at 100% aborts the run with a clear "budget exceeded" message in the failure log.

**Files touched:**
- `ai_hedge/runner/prepare.py` and `aggregate.py` — token counter
- `.env.example` — document new var

**Depends on:** none. **Risk:** A legitimate complex run might hit the limit. Adjust the default after observing.

---

### Sin #16 — Static stops, no management

**Problem:** Once you set stop $X at entry, it stays at $X forever. No moving the stop to breakeven once the trade is up by 1× the original risk. No trailing the stop up as price climbs. No "if it's been flat for 5 of 10 days, just cut it." Real swing traders manage stops daily — yours just sits frozen.

**Evidence:** `tracker/monitor.py` has no trailing/breakeven logic. Stops are read once from `decisions.json` and never updated.

**Severity:** 🟠 Major · **Fix effort:** medium

**Fix:** In `tracker/monitor.py`, add three optional rules toggleable per trade:
1. **Move stop to breakeven** once unrealized gain ≥ 1× original risk
2. **Trailing stop** at 1.5× ATR below the highest price since entry (for longs)
3. **Time-based exit** if trade has been flat (within 1% of entry) for >50% of its declared timeframe

Each is a flag on the trade record so you can A/B test.

**Files touched:**
- `tracker/monitor.py` — add the 3 rules
- `tracker/db.py` — new fields: `trailing_stop_enabled`, `breakeven_moved_at`, `time_exit_enabled`

**Depends on:** none. **Risk:** Trailing stops can take you out on a wick before the real move resumes. Test on historical data first.

---

### Sin #17 — No SPY benchmark
**Status: ✅ shipped + verified in actual reports 2026-04-27.** Live numbers from today's run:
- `tracker/backtest.py`: "Performance vs SPY: +$351.81 / +1.61% (you) — SPY: +$1,259.56 / +5.78% — you trail SPY by $907.75 (-4.16 pts)"
- `scripts/swing_audit_stock.md`: "+$207.77 / +0.81% (you) — SPY: +$1,470.66 / +5.77% — you trail by 4.95 pts"
- `scripts/swing_audit_crypto.md`: "+$24.45 / +0.24% — SPY: +$379.10 / +3.79% — you trail by 3.55 pts (with crypto-not-meaningful caveat)"

**The painful truth:** the strategy is currently underperforming SPY by ~5 points. This is exactly why the benchmark needed to exist.

**Problem:** Your audit says "+$130 P&L." Cool — but in the same period SPY (just buy the index and sleep) might have made +$500 on the same capital. You could be catastrophically underperforming a passive index and not know.

**Evidence:** `scripts/swing_audit.py` and `tracker/backtest.py` both lack a benchmark column.

**Severity:** 🟠 Major · **Fix effort:** tiny

**Fix:** Extend `swing_audit.py` to also fetch SPY hourly bars over the audit window, compute "buy SPY at audit start, hold to today" P&L, and add a top-line "you made +0.4% vs SPY +5.0%" comparison. Same for `tracker/backtest.py`.

**Files touched:**
- `scripts/swing_audit.py` — SPY fetch + comparison
- `tracker/backtest.py` — same

**Depends on:** none. **Risk:** None.

---

### Sin #18 — Documentation lies (meta-sin)
**Status: ✅ shipped 2026-04-27** (same fix as #14). CLAUDE.md and AGENTS.md both updated; drift CI live.

**Problem:** Same root as #14, but listed separately because it's a discipline issue, not a single fix. Every time the code changes meaningfully, the docs need to change too — or future decisions get made on lies.

**Evidence:** Pattern visible across CLAUDE.md and several inline file docstrings.

**Severity:** 🔴 Critical · **Fix effort:** small (but ongoing)

**Fix:** Solved largely by the CI check from #14. Plus: add a "Last verified against code on YYYY-MM-DD" footer to CLAUDE.md and to this audit doc. Quarterly sweep on the calendar.

**Files touched:**
- All docs get a "last verified" footer
- `scripts/check_docs_drift.py` — same as #14

**Depends on:** #14. **Risk:** None.

---

---

## Model tier decision (2026-04-27)

**Decision:** All subagent dispatches now pin `model: sonnet`. Orchestrator model is set at the claude.ai Routines page level (unchanged).

**Rationale:**
- **Sonnet for all agents:** The flat-rate subscription means model choice is quality/reliability, not cost. Sin #20 (head trader malformed JSON) was traced to Haiku under complex synthesis prompts. Switching to Sonnet eliminates the reliability gap.
- **NOT Opus:** Opus is slower (more tokens/sec time), which worsens the stream-idle-timeout failure mode documented in Sin #19. For structured-output tasks (all our agents), Sonnet's reliability is equivalent to Opus with a better latency profile.
- **Orchestrator stays as-is:** The orchestrator model (the session that runs the skill, coordinates batches, calls Bash) is set per-Routine at claude.ai. This decision does not affect it.

**Files changed:** All 6 skill files (`.agents/skills/{swing,daytrade,invest,research}/SKILL.md`, `.claude/skills/crypto-{swing,day}/SKILL.md`) + `RUN_PLAYBOOK.md`.

**Impact on Sin #19:** Sonnet's lower latency per event slightly reduces stream-idle-timeout risk (fewer events/second during synthesis steps). It doesn't fix #19's Anthropic-side bugs, but it reduces one contributing factor.

---

## Recommended fix order

### Wave 1 — cheap & critical · CODE SHIPPED 2026-04-27 (validation pending for some)
- 🟢 #6 (cache TTL) — code shipped + unit-tested. **Production fire pending.**
- 🟢 #7 (save WebSearch raw) — prompt edits shipped. **Real LLM run needed to confirm raw files actually appear.**
- 🟢 #12 (run index) — code shipped + unit-tested. **`runs/index.json` will populate on next routine fire.**
- 🟢 #13 (silent failures) — code shipped + unit-tested. **`degraded_inputs` field will populate when an agent first fails post-fix.**
- ✅ #14 + #18 (doc fix + CI check) — CI script live and exits 0 on current state.

**#8 was re-scoped to Wave 3 after investigation** — Claude Code's Agent tool doesn't expose `cache_control` from user code; real cost lever is fact-bundle deduplication, not prompt caching. See Sin #8 above.

**Outcome:** Full reproducibility (#7), no more silent failures (#13), auditable run history (#12), accurate docs that stay accurate (#14/#18 + drift check), no stale-price serving (#6). Smoke-tested: all entry points still parse args; cache TTL works; drift check returns 0.

### Wave 2 — risk hygiene (≈3–4 days)
- #2 (cron)
- #9 (earnings blackout)
- #10 (correlation cap)
- #15 (token budget)
- #17 (SPY benchmark)

**Outcome after Wave 2:** Stop wasting compute on duplicate runs. Stop blowing up around earnings. Stop piling into correlated bets. Cap monthly Anthropic spend. Know if you're beating SPY.

### Wave 3 — structural (≈1–2 weeks)
- #1 + #5 (portfolio state + memory) — in-run state shipped Wave 2; cross-run thesis memory shipped 2026-04-29 behind `wiki_enabled` flag
- #3 (collapse 7 agents → 5) — ✅ shipped 2026-04-29
- #4 (screening tier) — pending
- #11 (confidence calibration) — pending
- #16 (stop management) — pending

**Outcome after Wave 3:** The system stops pretending and starts behaving like a real fund. This is when you can sensibly evaluate "does this strategy make money?" — because before now, the answer was "we don't know, the data is garbage."

---

---

### Sin #20 — Silent JSON parse failures hide head trader output
**Status: 🟢 shipped + fault-injection tested 2026-04-27.** Exception raises correctly on trailing-comma JSON, degraded_inputs populated, snippet logged. ⚠️ NOT yet observed in production — needs a real swing/daytrade run where head trader emits malformed JSON.

**Problem (plain English):** `aggregate.py` catches `JSONDecodeError` on all signal files and silently continues with a logged warning. The head trader (`swing_head_trader.json` / `dt_head_trader.json`) is the MOST important signal in swing/daytrade mode — it's the synthesis layer that reconciles 9 conflicting strategy opinions into a single clear direction for the PM. When Haiku (the model previously used for head trader dispatch) emitted malformed JSON, the parse error was swallowed: the head trader was quietly added to `missing_agents`, logged as a warning, and the Swing PM ran as if 9 individual strategy signals had been reconciled — when they hadn't. The PM saw `degraded_inputs: ["swing_head_trader"]` in `signals_combined.json` but no exception was raised to the orchestrator.

**Evidence:** Validation run `validation_20260427_113014` — `swing_head_trader.json` failed to parse with `Expecting ':' delimiter: line 23 column 9`. Aggregate printed a warning and continued. Swing PM ran without synthesis layer.

**Root cause:** Head trader was dispatched with `model: "haiku"` (see RUN_PLAYBOOK.md STEP 4 model note). Haiku produces less reliable structured JSON under complex multi-input synthesis prompts. Sin #20 would not have occurred with Sonnet.

**Severity:** 🔴 Critical · **Fix effort:** small

**Fix:**
1. Add `HeadTraderSynthesisFailed` exception class in `aggregate.py`.
2. Add `_validate_head_trader_strict()` function: reads the head trader file if it exists, parses JSON strictly, validates per-ticker entries against `HeadTraderSignal` Pydantic schema, logs full context on failure (file path, error, first 200 chars of content), adds to `degraded_inputs`, and **raises** `HeadTraderSynthesisFailed`.
3. Called in `main()` immediately after `_load_persona_signals()` — before deterministic agents run.
4. Add `swing_head_trader` / `dt_head_trader` to `_expected_agents()` for their respective modes (research skips head trader, so it is excluded).
5. Update all skill files and RUN_PLAYBOOK.md to use `model: sonnet` for head trader dispatch.

**Files touched:**
- `ai_hedge/runner/aggregate.py` — exception class, validator function, expected agents update, call in main
- `ai_hedge/schemas.py` — `HeadTraderSignal` was already present; used for validation
- `RUN_PLAYBOOK.md` — model note updated from haiku → sonnet
- `.agents/skills/{swing,daytrade,invest,research}/SKILL.md` — all Agent dispatches now pin `model: sonnet`
- `.claude/skills/crypto-{swing,day}/SKILL.md` — same

**Depends on:** none. **Risk:** A real malformed head trader output will now abort the aggregate step instead of silently degrading. This is intentional — the orchestrator needs to see the failure to decide whether to re-run the head trader or accept the degraded run.

---

## Sin #19 — Claude Routines is not a guaranteed production runtime

**Problem:** Half of all routine failures (9 of 18 in the Apr 17–27 audit) are `"API Error: Stream idle timeout — partial response received"`. That's **Anthropic's runtime giving up on a long-running job**, not a usage-cap issue and not our code crashing. We have no visibility, no retries, no logs beyond what shows in the web UI.

**Why this was missed in the original 18:** I framed earlier sins as if cost was per-token and reliability was about our own code. Reality: **cost is fixed-subscription**, and the biggest failure source is upstream of our code entirely.

**External evidence (Apr 27 research, citations from anthropics/claude-code GitHub issues):**

| # | Title | Status | Relevance |
|---|---|---|---|
| [#41289](https://github.com/anthropics/claude-code/issues/41289) | Scheduled tasks fail with rate-limit error despite available quota | OPEN | Matches our 3 "hit your limit · resets" failures |
| [#42522](https://github.com/anthropics/claude-code/issues/42522) | Scheduled triggers cannot access MCP connector tools | Closed (not planned) | Architectural limitation — won't be fixed |
| [#42582](https://github.com/anthropics/claude-code/issues/42582) | Remote triggers return HTTP 500 and auto-disable | OPEN | Could explain silent failures in our index |
| [#42662](https://github.com/anthropics/claude-code/issues/42662) | Scheduled triggers miss cron runs; manual /run also returns 500 | OPEN | Could explain "no_detail" failures |
| [#44785](https://github.com/anthropics/claude-code/issues/44785) | CCR scheduled triggers cannot access claude.ai MCP connectors | Closed (duplicate of #35899) | Architectural — also won't be fixed |
| [#46987](https://github.com/anthropics/claude-code/issues/46987) | Stream idle timeout / partial response received | OPEN | **Direct match to our dominant failure mode (9/18)** |
| [#50312](https://github.com/anthropics/claude-code/issues/50312) | Scheduled routine stalls waiting for human input on ToolSearch | OPEN | Routines can hang forever silently |
| [#51110](https://github.com/anthropics/claude-code/issues/51110) | Routines inject UTC date instead of user timezone | OPEN | Off-by-hours bug in scheduled context |

**Verdict (cited from external research):** "**known-flaky** — works, but for production daily workloads you should expect meaningful failure rates and design retries or migrate. The observed 55% failure rate is worse than 'annoying beta bug' territory; it is operationally unreliable for a hedge-fund pipeline."

**Why splitting alone isn't enough:** #41289 (false rate-limit), #42582 (auto-disable), #50312 (silent hang), #51110 (wrong date) all hit routines regardless of size. Splitting fixes the #46987 timeout subset (~9/18) but leaves the rest. Real reliability requires either retry logic at a layer Anthropic doesn't expose, or migration off Routines.

**Severity:** 🔴 Critical · **Fix effort:** depends on chosen path (see options below)

**Three architectural options (mutually exclusive):**

### Option A — Stay on Claude Code, split routines smaller (RECOMMENDED first)
- Drop the 2 IPL routines you don't actually use → frees 2 slots
- Split each big routine (currently 7+ tickers per run) into 3-ticker runs → ~10 small routines
- Smaller runs = fewer events per session = much less likely to hit stream-idle timeout
- **Cost:** $0 incremental (stays inside $140/mo subscription)
- **Risk:** If timeouts are caused by Anthropic-side flakiness regardless of run size, this won't fully fix it
- **Effort:** ~1 day to redesign routine prompts and re-create them in the Claude.ai UI

### Option B — Migrate production to direct Anthropic API
- Run the daily pipeline via a Python script that calls the Anthropic API directly
- Hosted on a free cloud (GitHub Actions cron or Cloudflare Workers)
- Real prompt caching now applies → ~70% cost reduction on input tokens
- **Cost (real money, on top of subscription if kept):**
  - Sonnet 4.6 + caching, 1×/day × 22 days = **$30–45/month**
  - Sonnet 4.6 + caching, 5 split routines = **$140–220/month**
  - Opus 4.7, 1×/day = **$240–350/month** (too expensive)
- **Risk:** Real money flowing now; need cost guardrails (#15 reframed as $$ ceiling, not just tokens)
- **Effort:** ~1 week to port skill prompts to API calls, host the cron, add retry logic

### Option C — Hybrid (best of both, most setup)
- Keep Claude Code subscription for ad-hoc dev/exploration (where it shines)
- Production daily run goes through API (Option B)
- **Cost:** $140 subscription + Option B cost
- **Risk:** Two runtimes to maintain
- **Effort:** ~1 week + ongoing maintenance

**Decision needed BEFORE Wave 2 work:** which option to pursue. Wave 2 fixes (earnings blackout, correlation cap, etc.) make sense in any of the three architectures. But Wave 3 / Sin #8 design (fact-bundle dedup, prompt caching) depends heavily on which path you pick.

**Recommended path:** Try Option A first because it's free and reversible. Watch timeout rates for ~2 weeks. If they drop sharply with smaller routines, stay. If timeouts persist regardless of size, escalate to Option B or C with eyes open.

---

## How three of the original sins were misframed (re-stated with the right motivation)

These fixes are still right. The *reason* I gave was wrong because I assumed per-token billing.

- **#8 (cost reduction):** Original framing implied $$$ savings via prompt caching. Real benefit on Claude Code: **stretching your monthly usage cap** so routines stop hitting "you've used your limit." If you migrate to Option B, prompt caching becomes a real $$ saver.
- **#11 (confidence calibration):** Still valid. The motivation is "trades sized by miscalibrated confidence are mis-sized," not "we're paying real money for wrong sizing."
- **#15 (token budget):** Reframe as a **time budget** (per-run timeout) on Claude Code, since timeouts are the actual failure mode and there's no per-token bill. Becomes a real $$ ceiling on Option B.

---

## Validation gap — what we shipped vs what we've actually observed

**Important distinction.** "Shipped" means code is committed and unit/smoke tests confirm the function works. **It does NOT mean a full production routine has fired since the change** — the LLM-driven Agent calls (the expensive part) have not run end-to-end after Wave 1+2 landed. Several fixes will only show their full value when a real swing routine fires next.

### Validated end-to-end (smoke test exercised the new code path)
- ✅ #1 + #5 — Portfolio state injected into `signals_combined.json`. Verified: NVDA buy correctly blocked by `compute_allowed_actions()` because 6 shares already held.
- ✅ #9 — Earnings blackout. Verified: AAPL blocked (3 days), NVDA clean (23 days), crypto auto-skipped.
- ✅ #10 — Correlation cap. Verified: BAC (74% corr w/ JPM) blocked, XOM (0.9% corr) clean, 5 unit tests pass.
- ✅ #14/#18 — Doc drift. Verified: CI script exits 0 on current state.
- ✅ #17 — SPY benchmark. Verified: live headlines printed in both `tracker/backtest.py` and `swing_audit_stock.md`.

### Unit-tested but NOT yet observed under a real routine fire
These are 🟢 not ✅ above. Code is solid, but the user-visible production behavior depends on a real LLM agent run we haven't executed yet:

- 🟢 #6 — Cache TTL eviction. The TTL math works. Production check: re-run a stock more than 5 minutes after the first fetch and confirm prices are re-pulled fresh.
- 🟢 #7 — WebSearch raw save. The PROMPT was edited; whether the LLM actually obeys "save raw before processing" is empirical. Production check: after the next swing routine, look in `runs/<id>/web_research/raw/` — empty means we need to strengthen the prompt.
- 🟢 #12 — Run index. `prepare.py`/`finalize.py` will populate `runs/index.json` on the next fire. Production check: after the next routine, `runs/index.json` should exist and contain one entry per recent run.
- 🟢 #13 — Silent failures surfaced. `degraded_inputs` will only appear if an Agent crashes mid-run. Production check: next time a routine has 8/9 agents complete, `signals_combined.json` should list the missing one in `degraded_inputs` instead of silently ignoring it.

### When to re-validate

**Trigger one full swing routine** after the next user session opens, then audit:
1. `runs/index.json` exists with the run entry → ✅ Sin #12 confirmed
2. `runs/<id>/web_research/raw/*.json` files exist → ✅ Sin #7 confirmed
3. Cache stats from the run show fresh fetches after TTL expiry → ✅ Sin #6 confirmed
4. If any agent failed: `signals_combined.json["degraded_inputs"]` lists it → ✅ Sin #13 confirmed
5. `signals_combined.json["portfolio"]["positions"]` is populated AND the PM's actual decisions don't include "buy" for already-held tickers → ✅ Sin #1+#5 fully confirmed at the LLM-decision level

If any of those don't pan out, that fix needs a follow-up.

---

## Wave 4 — Live Dashboard (planned, NOT yet built)

The eventual UI for this project is a live web dashboard. Why it's deferred: the data underneath has to be honest first. The dashboard reads `tracker.db`, `crypto_tracker.db`, and `runs/index.json` directly — building it on top of broken portfolio state (#1) or silent agent failures (#13) just means rebuilding when those land. Now that Wave 1 + most of Wave 2 are shipped, the data layer is finally trustworthy enough.

**Target architecture (when we get there):**
- **Stack:** Flask single-file app, server-rendered HTML with HTMX polling for refresh. ~300 lines. Runs in existing `.venv/`.
- **Data sources:** `tracker.db` (stocks), `crypto_tracker.db` (crypto), `runs/index.json` (run history), yfinance for live prices, `scripts/swing_audit_*.md` for backtest summaries.
- **Sections:** Open positions table, pending orders, closed trades, daily P&L vs SPY, win rate by source (routine_v2 / local / manual), recent run log.
- **Hosting:** GitHub Actions cron commits an updated DB to a branch every 15-60 min during market hours. Vercel/Cloudflare Pages serves the read-only view from the same repo. Public-share mode optional via Cloudflare Tunnel — free, stable URL while running.
- **Cost:** $0 (subscription unaffected; GitHub Actions free tier).

**Pre-reqs before building:**
1. ✅ Sin #1+#5 (portfolio state) — done; dashboard needs accurate positions
2. ✅ Sin #12 (run index) — done; dashboard's "recent runs" panel reads this
3. ✅ Sin #13 (silent failures surfaced) — done; dashboard can show degraded runs honestly
4. ✅ Sin #17 (SPY benchmark) — done; "you vs SPY" headline goes straight onto the dashboard
5. ⏳ Sin #4 (screener tier) — recommended; lets the dashboard show "today's screened candidates: 0" when nothing fired
6. ⏳ Sin #16 (stop management) — recommended; otherwise the dashboard can't show "trailing stop activated" / "moved to breakeven"

**Decision needed:** local-only vs public-share-mode. Local-only is simplest; public-share is useful if Naman wants to put the URL on Instagram. Both are cheap.

**Out of scope for the dashboard plan:**
- User accounts / auth (single-user)
- Mobile-first design (desktop only initially)
- Real broker integration (waits on Sin #19 / Moomoo replacement)

---

## What this audit does NOT solve

- Real-broker execution (Moomoo replacement, cloud-cron simulator) — separate plan after Wave 2
- Options trading support — defer until swing is profitable for 8–12 weeks
- Crypto trading — explicitly dropped from scope
- Daytrade mode — explicitly dropped from scope
- Watchlist composition / rotation — separate audit
- Explainer agent hallucination check — separate audit
- Moomoo-layer post-mortem — separate audit

---

## Glossary (for the non-technical reader)

- **PM (Portfolio Manager):** The AI agent that takes all the strategy signals and decides which actual trades to put on, with sizes.
- **Stop loss:** A pre-set price where you exit a losing trade automatically. "Buy at $100, stop at $95" = "if it drops to $95, get me out, I've capped my loss."
- **R:R (Risk-to-Reward ratio):** How much you can win vs how much you can lose. "2:1 R:R" means the target is 2× as far from entry as the stop. Industry rule of thumb: don't take trades below 1.5:1.
- **Correlation:** A number from -1 to +1 that says how often two stocks move together. JPM and BAC correlate ~0.85 (almost always move together) — owning both is mostly the same as owning one.
- **Trailing stop:** A stop loss that moves UP with the stock as it climbs (but never down). Locks in profit if the trade reverses.
- **ATR (Average True Range):** A measure of how much a stock typically moves in a day. Used to set stops "wide enough to not get whipsawed but tight enough to limit loss."

---

_Last verified against code on 2026-04-27. Re-verify before quoting any file:line citation as fact — the codebase moves._
