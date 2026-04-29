---
name: JPM trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 812
summary: 3 long trades initiated (Apr 14–18 2026); all abandoned by Apr 29; 1 partial fill recorded (trade #15, filled at $305.30, exited at $311.45); 2 never filled
---

# JPM — Trades

## TL;DR

Three long positions were attempted across two consecutive swing runs in April 2026. One (trade #15) filled and was exited at a gain ($305.30 entry, $311.45 exit fill). Two others (#8 and #26) were placed but never filled, both abandoned by Apr 29 during a tracker cleanup. No shorts have been taken on JPM. The model has been consistently bullish on JPM (or hold pre-earnings) across all three runs that analyzed it.

## Open positions

None as of 2026-04-29. All three trades were closed with `abandoned` status in the tracker as of Apr 29.

## Closed — last 30 days

### Trade #15 — Long, Partial Success (Apr 15 run)
| Field | Value |
|---|---|
| Trade ID | 15 |
| Direction | Long |
| Quantity | 4 shares |
| Entry price (model) | $304.78 |
| Entry fill price | $305.30 |
| Exit fill price | $311.45 |
| P&L | Not recorded in DB (null) |
| Status | Abandoned (Apr 29) |
| Created at | 2026-04-15 17:12:54 |
| Entered at | 2026-04-15 17:14:47 |
| Closed at | 2026-04-29 11:19:51 |
| Source run | 20260415_093758 |

**Context:** This was the highest-conviction trade in the Apr 15 batch — 7 of 10 strategy models bullish, 0 neutral, confidence 70%. The thesis was "buy the post-earnings dip in an uptrend": JPM reported record Q1 profits (+13% YoY, $5.94 EPS vs $5.45 estimate) but sold off intraday, pushing the hourly RSI to 31 (extreme oversold) while the daily trend remained intact [run: 20260415_093758]. The fill was $305.30, very close to the $304.78 model price. The exit fill of $311.45 suggests the trade moved in the right direction — the target was $319.60, so the exit was a partial gain vs full target, likely from the abandoned status rather than a clean target hit. Implied gain: ($311.45 - $305.30) x 4 = ~$24.60.

### Trade #8 — Long, Never Filled (Apr 14 run)
| Field | Value |
|---|---|
| Trade ID | 8 |
| Direction | Long |
| Quantity | 3 shares |
| Entry price (model) | $310.00 |
| Entry fill price | None (never filled) |
| Exit fill price | None |
| P&L | None |
| Status | Abandoned (Apr 29) |
| Created at | 2026-04-14 08:45:51 |
| Entered at | None |
| Closed at | 2026-04-29 11:19:51 |
| Source run | Likely 20260415_093758 or adjacent run |

**Context:** Order placed at $310.00 but never filled. Given trade #15 filled the same day at $305.30, it is likely trade #8 was a duplicate or contingent order placed at a limit above the market that was never triggered. No capital at risk; no P&L impact.

### Trade #26 — Long, Never Filled (Apr 18 run)
| Field | Value |
|---|---|
| Trade ID | 26 |
| Direction | Long |
| Quantity | 30 shares |
| Entry price (model) | $309.95 |
| Entry fill price | None (never filled) |
| Exit fill price | None |
| P&L | None |
| Status | Abandoned (Apr 29) |
| Created at | 2026-04-18 00:18:19 |
| Entered at | None |
| Closed at | 2026-04-29 11:19:51 |
| Source run | 20260417_233350 |

**Context:** This was from the Apr 17 run [run: 20260417_233350]. The model recommended buying 30 shares at $309.95, target $325.00, stop $304.00, confidence 62%, R:R 2.53:1. Reasoning: trend and sector rotation bullish, but momentum ranker neutral and Druckenmiller bearish on fundamentals — modest conviction compared to the Apr 15 trade. The order was placed at 00:18 (after-hours) and never filled; Moomoo paper orders expire end of day and require re-placement. No P&L impact.

## Closed — older, rolled by month

None. All JPM activity is within April 2026.

## Closed — older than 6 months

None. JPM first appeared in run swing_20260411_211655 (Apr 11, 2026) as a pre-earnings hold.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades recorded | 3 |
| Filled trades | 1 (trade #15) |
| Unfilled / abandoned | 2 (trades #8 and #26) |
| Long entries | 3 |
| Short entries | 0 |
| Win rate (filled trades) | 1/1 (100%, but small sample) |
| Implied P&L on filled trade | ~+$24.60 (4 shares, $305.30→$311.45) |
| Recorded P&L in DB | null (not tracked to close) |
| Model confidence range | 58–70% across runs |
| Best model confidence | 70% (Apr 15 run, 7/10 strategies bullish) [run: 20260415_093758] |
| Avg R:R recommended | 2.41:1 (2.18, 1.50, 2.53 across three runs) |

## Model recommendation history

| Run | Action | Entry | Target | Stop | Confidence | R:R | Notes |
|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | Hold | $308.00 | $320.00 | $300.00 | 58% | 1.5:1 | Pre-earnings binary risk; R:R too low [run: swing_20260411_211655] |
| 20260415_093758 | Buy | $304.78 | $319.60 | $298.30 | 70% | 2.18:1 | Post-earnings dip; highest conviction in batch [run: 20260415_093758] |
| 20260417_233350 | Buy | $309.95 | $325.00 | $304.00 | 62% | 2.53:1 | Trend continuation; split conviction [run: 20260417_233350] |

## Last updated

2026-04-29. Trade data from tracker.db query (trades #8, #15, #26). Model recommendation data from decisions.json in runs swing_20260411_211655, 20260415_093758, and 20260417_233350.
