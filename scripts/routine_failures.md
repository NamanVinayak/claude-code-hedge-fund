# Claude Routines — Failure-mode Analysis

_Generated 2026-04-27 12:39 UTC · 33 sessions audited (Apr 17–27, trading routines only)._

## TL;DR

- **Sessions captured:** 33
- **Completed with decisions written:** 11
- **Completed but no decisions written (silent failure):** 4
- **Explicitly failed:** 18

## Failure breakdown

| Category | Count | What this means |
|----------|------:|-----------------|
| usage_limit | 5 | Hit your Anthropic monthly usage cap. Routine couldn't run at all or stopped mid-run. |
| timeout | 9 | Session ran longer than allowed before completing. |
| no_detail | 4 | Status was 'failed' but Anthropic returned no reason. |

### Per-routine failure rate

| Routine | Total runs | Failed | Failure % |
|---------|----------:|-------:|----------:|
| Crypto Evening | 10 | 6 | 60% |
| Crypto Morning | 9 | 7 | 78% |
| Stock Swing Batch 1 | 6 | 2 | 33% |
| Stock Swing Batch 2 | 8 | 3 | 38% |

### Every failed session (raw)

| Date | Routine | Session | Category | Status detail |
|------|---------|---------|----------|---------------|
| 2026-04-17 | Stock Swing Batch 2 | …8fAKYsm8oQtV | no_detail | (none) |
| 2026-04-18 | Crypto Evening | …yriwxpcC9yE5 | usage_limit | You've hit your limit · resets 8am (UTC) |
| 2026-04-19 | Crypto Morning | …w8bt7jPxpLX7 | usage_limit | You've hit your limit · resets 4pm (UTC) |
| 2026-04-20 | Crypto Morning | …dVGr3Av95PLF | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-20 | Stock Swing Batch 2 | …XJj1m5VjFU97 | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-21 | Crypto Morning | …myyDQTka6boQ | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-22 | Stock Swing Batch 1 | …p4NK1AYdWRh1 | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-23 | Crypto Evening | …FEyDPSbpjw5o | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-23 | Crypto Morning | …4F9MFkoviLJo | usage_limit | You've hit your limit · resets 4:10pm (UTC) |
| 2026-04-24 | Crypto Evening | …qdUkpfvz2KTT | usage_limit | You've hit your org's monthly usage limit |
| 2026-04-24 | Crypto Morning | …hAp9oGX4MEPc | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-24 | Stock Swing Batch 1 | …JmAPQSj6sM5D | usage_limit | You've hit your org's monthly usage limit |
| 2026-04-24 | Stock Swing Batch 2 | …BxuGwE3igzFW | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-25 | Crypto Evening | …pMia49QX1SJ3 | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-25 | Crypto Morning | …NYcGsJ51znVz | timeout | API Error: Stream idle timeout - partial response received |
| 2026-04-26 | Crypto Evening | …xGQK3wYt9gqX | no_detail | (none) |
| 2026-04-26 | Crypto Morning | …Xq7ko97oXdge | no_detail | (none) |
| 2026-04-27 | Crypto Evening | …srnyoWfvcggM | no_detail | (none) |

## Sessions whose failure reason doesn't match known patterns

These are the ones to investigate manually:

- **2026-04-17** · Stock Swing Batch 2 · `session_014kVb41sE218fAKYsm8oQtV` · branch `claude/beautiful-ritchie-07f6D` · detail: `(none)`
- **2026-04-26** · Crypto Evening · `session_0111aSUCwP8FxGQK3wYt9gqX` · branch `None` · detail: `(none)`
- **2026-04-26** · Crypto Morning · `session_01EmreD6b4eHXq7ko97oXdge` · branch `None` · detail: `(none)`
- **2026-04-27** · Crypto Evening · `session_0196UmQDnjSYsrnyoWfvcggM` · branch `None` · detail: `(none)`

## Silent failures: completed but no decisions written

These ran to completion without errors, yet the agent never wrote `runs/<id>/decisions.json`. Likely the routine decided 'no trades today' or aborted mid-run after exceeding context.

| Date | Routine | Session | Events processed |
|------|---------|---------|----------------:|
| 2026-04-18 | Stock Swing Batch 1 | …6kSvZ1RUwEiU | 1 |
| 2026-04-18 | Crypto Morning | …XnWgti2E7GvF | 976 |
| 2026-04-20 | Crypto Evening | …jZWQsii9ENU1 | 623 |
| 2026-04-22 | Stock Swing Batch 2 | …MZuNhV9FL4Fn | 715 |

## Answer to the original question

Of 18 explicitly-failed routine sessions:

- **5 were usage-limit hits** (monthly cap, or daily/hourly resets)
- **9 were timeouts** ('Stream idle timeout — partial response received')
- **4 were other / no-detail failures**

So: **timeouts are the bigger problem, not usage limits.** Most failed routines are running so long that the API stops streaming a response back. Worth shrinking each routine's scope (fewer tickers per batch, fewer agents, or splitting into more triggers) before assuming you need a bigger plan.
