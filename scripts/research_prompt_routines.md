# Research Brief — Claude Routines Reliability for Production Workloads

I run a daily AI hedge-fund pipeline on Anthropic's **Claude Routines** feature (also called **scheduled triggers** — the cron-style scheduling inside Claude Code at `claude.ai/code`). I need to decide whether to stay on Routines or migrate to direct Anthropic API. Please research the questions below using web search. **Cite every claim with a URL.**

---

## Concrete observations from my own data (Apr 17–27, 2026)

I have 6 routines configured (4 trading, 2 unrelated cricket-prediction routines I'll drop). Across this 10-day window, **33 sessions ran and 18 failed (55% failure rate)**. Per-routine breakdown:

| Routine               | Total | Failed | Rate |
|-----------------------|------:|-------:|-----:|
| Crypto Morning        |     9 |      7 |  78% |
| Crypto Evening        |    10 |      6 |  60% |
| Stock Swing Batch 2   |     8 |      3 |  38% |
| Stock Swing Batch 1   |     6 |      2 |  33% |

Three distinct error strings observed (please grep these verbatim online):

1. `"API Error: Stream idle timeout — partial response received"` — **9 of 18** failures, the dominant mode
2. `"You've hit your limit · resets [time] (UTC)"` — **3 of 18**, hourly/daily reset (NOT the monthly cap)
3. `"You've hit your org's monthly usage limit"` — **2 of 18**, the actual monthly cap

Routines hit a Claude API endpoint at `claude.ai/v1/sessions/<id>/events` with beta header `anthropic-beta: ccr-byoc-2025-07-29`. The triggers endpoint is `/v1/code/triggers`. Cron expressions in use (UTC): `30 18 * * 1-5`, `30 23 * * 1-5`, `0 15 * * *`, `30 3 * * *`. Median session = **680 events**, p90 = **1,000+ events**. **Crypto routines have higher event counts (~870 avg) and fail more**, while stock routines have lower counts (~575 avg) and fail less — this correlation suggests session length is the trigger, but I want to verify.

The model in use is **Claude Opus 4.7** (the heavy model). Each routine spawns 7-9 sub-agents via the Agent tool, dispatched in parallel.

---

## Questions

**Q1. GitHub issues.** Search `github.com/anthropics/claude-code` issues (and adjacent repos: `anthropics/anthropic-sdk-python`, any repo discussing scheduled triggers) for these EXACT phrases:
- `"Stream idle timeout"`
- `"partial response received"`
- `"scheduled trigger"`
- `"ccr-byoc"`
- `"Routines"` (in title, last 6 months)

For each match, list: URL, date opened, status (open/closed), and any maintainer comment indicating root cause or fix. If zero matches, say so explicitly.

**Q2. Reddit + HN.** Search `r/ClaudeAI`, `r/Anthropic`, `r/ClaudeCode`, and Hacker News for posts (last 6 months) mentioning Claude **Routines** OR **scheduled triggers** AND timeouts/failures/reliability. Top 5 by upvotes/comments, with URLs and a one-sentence summary of each.

**Q3. Anthropic official sources.** Search `docs.anthropic.com`, the Anthropic changelog, `status.anthropic.com` (current and historical incidents), and Anthropic's blog for ANY mention of: routine reliability, stream idle timeouts, known limitations of Routines/scheduled triggers, beta caveats on the Routines product. Quote any relevant text verbatim.

**Q4. Reliability comparison.** Is there community consensus that **Routines** is more flaky than **interactive Claude Code** (chat sessions)? More flaky than calling the **Anthropic API directly**? Quote specific users with links — I want sentiment, not your opinion.

**Q5. Workarounds (ranked by evidence).** What fixes do users report working? For each, cite the source:
- Splitting one big routine into multiple smaller routines (fewer sub-agents per run)
- Reducing context size per sub-agent (smaller prompts/facts bundles)
- Switching from Opus → Sonnet inside sub-agents
- Avoiding parallel Agent tool dispatch
- Other tricks (retry logic, lower max_tokens, simpler skills)

**Q6. Production case studies.** Find at least 2 users who tried Claude Routines for a real daily production workflow (trading bots, monitoring, scraping, scheduled reports, content generation pipelines). Link to their account. Did they stay on Routines, or did they migrate to direct API / a different platform? If they migrated, what was the trigger?

---

## Anti-noise guardrail (CRITICAL)

**Ignore generic Claude Code timeout reports that aren't specifically about Routines / scheduled triggers.** Most online chatter about "Claude Code timeouts" is interactive sessions, API timeouts in the Python SDK, or tool-call errors. **None of that is relevant.** I want results that specifically discuss the Routines product (the cron-scheduled feature inside Claude Code at `claude.ai/code`). If a result doesn't mention routines, scheduled triggers, or one of my quoted error strings, **drop it from your answer.**

---

## Output format

- One bullet list per question (Q1–Q6) with **URL citations** for every claim.
- Total **under 800 words**.
- End with a one-paragraph **VERDICT** that classifies Claude Routines reliability for production daily workloads as exactly one of:
  - `stable` (safe for production)
  - `improving` (known issues but actively being fixed)
  - `known-flaky` (works but expect 30%+ failure; plan for retries)
  - `not recommended` (community consensus is to migrate off)
- Add one final sentence: **"What I'd do if it were my project: ___."**

If a question has zero usable results, write "No relevant results found" — don't pad with generic Claude Code material.
