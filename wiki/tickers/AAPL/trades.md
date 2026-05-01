---
name: AAPL trades
last_updated: 2026-05-01
last_run_id: 20260501_144523
target_words: 800
stale_after_days: 60
word_count: 798
summary: Full trade journal for AAPL — one open limit-buy (2 shares at $276, run 20260501_144523); one prior abandoned long; five no-trade holds; lifetime stats updated
---

# AAPL — Trades

## TL;DR

AAPL has one trade on record in tracker.db (trade ID 19, abandoned, no fill, $0 P&L) and one new open position initiated by run 20260501_144523: a limit buy of 2 shares at $276.00. The system will only enter on a pullback from the current $282–285 level; the order is conditional and not yet filled.

## Open positions

### Trade — Conditional limit buy (20260501_144523)

| field | value |
|---|---|
| Status | open (limit order pending fill) |
| Direction | long |
| Quantity | 2 shares |
| Limit entry | $276.00 |
| Entry zone | $274–$278 |
| Target price | $294.84 (Fib ext 1.618) |
| Stop loss | $269.50 |
| Risk/reward | 2.9:1 |
| Confidence | 42% |
| Timeframe | 5–12 trading days |
| Run ID | 20260501_144523 |
| Mode | swing |
| Created | 2026-05-01 |
| Entry fill | Pending — limit at $276 not yet triggered |

**Rationale.** Head trader neutral (42 conf) after Q2 FY2026 earnings beat (EPS $2.01, gross margin 49.3% record). Breakout above $276.11 on 2.08x volume confirmed on April 30. System will not chase at $282 — hourly Z-score 2.52 and Bollinger %B 1.28 flag overextension. Entry trigger: pullback to $274–278 (Fib 38.2% / daily upper Bollinger Band confluence) with ADX rising above 19. Size: 2 shares × $276 = $552, within risk manager cap $768. Key risks: insider net selling (-$235M), ADX still sub-25, prior portfolio loss on similar NVDA setup (-$264.65). (Source: decisions.json, run 20260501_144523.)

## Closed — last 30 days

### Trade 19 — Abandoned long (never filled)

| field | value |
|---|---|
| Trade ID | 19 |
| Status | abandoned |
| Direction | long |
| Quantity | 40 shares |
| Intended entry | $262.50 |
| Target | $282.00 |
| Stop loss | $256.50 |
| Risk/reward | 3.25:1 |
| Confidence | 60% |
| Timeframe | 5–8 trading days |
| Run ID | 20260417_233350 |
| Mode | swing |
| Created | 2026-04-18 00:18 UTC |
| Closed | 2026-04-29 11:19 UTC |
| Entry fill | none |
| Realized P&L | $0 |

**What happened.** The Apr 17 swing run was the first run to give AAPL a buy signal after two consecutive no-trade decisions. Intended entry $262.50 was a limit order that sat unfilled for 11 days and was abandoned April 29. No capital at risk was incurred.

## Closed — older than 30 days

No trades.

## Prior run decisions (no orders placed)

| run_id | date | decision | confidence | reasoning summary |
|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 42% | EMAs tangled, ADX 15.2, overbought stochastic 89.75, no actionable setup |
| 20260415_093758 | 2026-04-15 | hold | 47% | ADX 12.5 (lowest in universe), daily supertrend bearish, 8/10 strategies neutral, Cook sold $12M+ |
| wiki_phase1_on | 2026-04-29 | (no decisions file) | n/a | Data-only run, no PM dispatch |
| wiki_phase1_off | 2026-04-29 | (no decisions file) | n/a | Data-only run, no PM dispatch |
| 20260430_144524 | 2026-04-30 | hold | 30% | Earnings blackout (0 days to Q2 print) blocks all new positions; R/R 0.71:1 fails 2:1 minimum; ADX 15.78 still below 25 |

## Lifetime stats

| metric | value |
|---|---|
| Total trades (with order) | 2 |
| Filled entries | 0 |
| Open (pending fill) | 1 |
| Abandoned / expired | 1 |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 (pending fill at $276) |
| Net P&L | $0.00 |
| Win rate (closed, filled) | n/a |
| Average hold time | n/a |
| Average R:R on entry | 3.08:1 (avg of 3.25:1 and 2.9:1) |
| Runs analyzed (AAPL) | 7 |
| No-trade decisions | 4 (Apr 11, Apr 15, wiki_phase1, Apr 30) |
| Buy decisions | 2 (Apr 17 abandoned; May 1 limit pending) |
| Short decisions | 0 |

## Notes and lessons

**Q2 earnings binary resolved bullishly.** The April 30 run (20260430_144524) was blocked by the 3-day earnings blackout. May 1 run (20260501_144523) is the first post-earnings entry attempt. Gross margin at 49.3% (record) falsified the bear-case margin-collapse scenario the model was hedging against.

**Entry discipline maintained.** The system is not chasing the gap from $271 to $282. Limit at $276 reflects the confluence of Fib 38.2% and daily upper Bollinger Band — the same pullback discipline that (with hindsight) would have avoided the NVDA dip-buy stop-out (-$264.65 on an aggressive entry into stretched hourly RSI).

**Watch for re-queue.** The Apr 17 abandoned trade suggests the daily order expiry may not auto-re-queue. If the $276 limit order expires without a fill, manual resubmission or a new run will be needed. (Source: trades.md, prior runs.)
