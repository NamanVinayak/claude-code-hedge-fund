---
name: AAPL trades
last_updated: 2026-05-04
last_run_id: 20260504_144833
target_words: 800
stale_after_days: 60
word_count: 796
summary: Trade ID 114 now entered — 2 shares filled at $277.27 on 2026-05-04 (run 20260501_144523 decision, entered May 4); primary target $291, extended $296.77, stop $269.50; one prior abandoned long (ID 19); lifetime stats updated
---

# AAPL — Trades

## TL;DR

AAPL has one open entered position (trade ID 114, 2 shares long at $277.27 fill, stop $269.50, primary target $291, extended target $296.77) and one prior abandoned long (trade ID 19, no fill). This run (20260504_144833) issued a HOLD — the existing position is thesis-compatible; no duplicate entry allowed. (Source: trade_ledger.json per_ticker_history[AAPL], run 20260504_144833.)

## Open positions

### Trade ID 114 — Long (entered)

| field | value |
|---|---|
| Trade ID | 114 |
| Status | entered |
| Direction | long |
| Quantity | 2 shares |
| Decision entry | $276.00 (limit) |
| Entry fill price | $277.27 |
| Entry zone | $274–$278 |
| Primary target | $291.00 |
| Extended target | $296.77 (Fib ext 1.618, measured move) |
| Partial profit level | $285.50 |
| Stop loss | $269.50 |
| Risk/reward | 2.0:1 at fill ($277.27 → $291 / $277.27 → $269.50); 2.8:1 at extended target |
| Confidence | 42% (decision run); 55% (this run head trader) |
| Timeframe | 5–12 trading days |
| Decision run | 20260501_144523 |
| This run | 20260504_144833 (HOLD — maintain existing position) |
| Created | 2026-05-01T15:00:50 UTC |
| Entered | 2026-05-04T13:31:00 UTC |
| Closed | — |
| PnL | open (unrealized) |

**Rationale (decision run 20260501_144523).** Head trader neutral (42 conf) after Q2 FY2026 earnings beat (EPS $2.01, gross margin 49.3% record). Breakout above $276.11 on 2.08x volume confirmed April 30. Not chasing at $283; limit at $276 (Fib 38.2% / daily upper Bollinger Band confluence). ADX 16.83 was the main caveat; trigger required ADX rising above 19. Size: 2 shares × $276 = $552, within risk manager cap. Key risks: insider net selling (−$235M), ADX sub-25. (Source: trade_ledger.json id 114 raw_decision, run 20260501_144523.)

**This run update (20260504_144833).** 5/5 swing agents unanimously bullish (first full consensus on AAPL). Head trader confirms hold — existing position at $277.27 fill is thesis-compatible. Target range awareness raised to $291 primary / $296.77 extended (vs. original $294.84 at decision). Partial profit at $285.50. Confidence capped at 55 by Iran geopolitical escalation (May 4 missile strike reports) and marginal R/R 2.0:1. No duplicate entry permitted. (Source: decisions.json, swing_head_trader signal, run 20260504_144833.)

## Closed — last 30 days

No closed AAPL positions in trade_ledger.json recent_closures_30d. (Source: trade_ledger.json, run 20260504_144833.)

## Closed — older than 30 days

### Trade ID 19 — Abandoned long (never filled)

| field | value |
|---|---|
| Trade ID | 19 |
| Status | abandoned |
| Direction | long |
| Quantity | 40 shares (intended) |
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

**What happened.** First buy signal on AAPL after two consecutive holds. Limit order at $262.50 sat unfilled for 11 days — price never pulled back to that level — and was abandoned April 29. No capital at risk was incurred.

## Prior run decisions (no orders placed)

| run_id | date | decision | confidence | reasoning summary |
|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 42% | EMAs tangled, ADX 15.2, overbought stochastic 89.75, no actionable setup |
| 20260415_093758 | 2026-04-15 | hold | 47% | ADX 12.5 lowest in universe, daily supertrend bearish, Cook sold $12M+ |
| wiki_phase1_on | 2026-04-29 | n/a | n/a | Data-only run, no PM dispatch |
| wiki_phase1_off | 2026-04-29 | n/a | n/a | Data-only run, no PM dispatch |
| 20260430_144524 | 2026-04-30 | hold | 30% | Earnings blackout (0 days) blocks all new positions; R/R 0.71:1 fails 2:1 minimum |
| 20260504_144833 | 2026-05-04 | hold | 55% | Existing position (ID 114) is thesis-compatible; 5/5 bullish but no duplicate entry allowed |

## Lifetime stats

| metric | value |
|---|---|
| Total trades (with order) | 2 |
| Filled entries | 1 (ID 114, entered $277.27) |
| Open (entered, in position) | 1 |
| Abandoned / expired | 1 (ID 19) |
| Realized P&L | $0.00 |
| Unrealized P&L | open — entry $277.27, current approx. $277.68 (mark from risk_manager signal) |
| Net P&L | $0.00 realized |
| Win rate (closed, filled) | n/a |
| Average hold time | n/a (1 open position, no closed fills) |
| Average R:R on entry | 3.13:1 (avg of 3.25:1 ID 19 and 2.9:1 ID 114 at decision entry $276) |
| Runs analyzed (AAPL) | 8 |
| No-trade / hold decisions | 5 (Apr 11, Apr 15, wiki_phase1 ×2, Apr 30, May 4) |
| Buy decisions | 2 (Apr 17 abandoned; May 1 limit — filled May 4) |
| Short decisions | 0 |

## Notes and lessons

**Position filled — entry discipline validated.** The Apr 30 run was blocked by earnings blackout. May 1 issued limit at $276; the pullback to the $274–$278 target zone arrived May 4 and the fill came at $277.27 — exactly within the identified zone. The discipline of not chasing at $282 (hourly Z-score 2.52 / %B 1.28 on May 1) was rewarded.

**Target range upgraded, stop unchanged.** Decision run target was $294.84 (Fib 1.618). This run head trader consensus raises primary target to $291 (macro-adjusted, given Iran headwind) and confirms $296.77 as extended case. Partial profit at $285.50 is new guidance. Stop remains $269.50.

**Watch for macro risk-off.** Iran Strait of Hormuz risk is a left-tail scenario that could drag AAPL 3–5% in a broad market selloff regardless of fundamentals. Stop at $269.50 is the protection. Active monitoring required over the 5–12 trading day window. (Source: decisions.json, trade_ledger.json, explanation.json, run 20260504_144833.)
