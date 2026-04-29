---
name: UNH trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 803
summary: Full trade journal for UNH — two cancelled/abandoned orders, zero fills, net P&L $0; system liked the setup but neither entry ever triggered
---

# UNH — Trades

## TL;DR

UNH has two records in tracker.db: one cancelled limit order (trade ID 1, placed April 12 at $296 entry) and one abandoned order (trade ID 9, placed April 14 at $305 entry). Neither order was ever filled. Net realized P&L is $0. The system generated a buy signal with 58% confidence and a 3:1 risk-reward on April 11, placed the order, then re-queued it at a higher entry on April 14 before both eventually expired or were cancelled. The underlying thesis — Medicare Advantage rate hike + strong insider buying — was sound, but the market never pulled back to the entry levels the system was waiting for.

## Open positions

None. Both recorded UNH positions are closed with zero fills.

## Closed — last 30 days

### Trade 1 — Cancelled long (never filled)

| field | value |
|---|---|
| Trade ID | 1 |
| Status | cancelled |
| Direction | long |
| Quantity | 1 share |
| Intended entry | $296.00 |
| Target price | $320.00 |
| Stop loss | $288.00 |
| Risk/reward | 3.0:1 |
| Confidence | 58% |
| Timeframe | 5–10 trading days |
| Run ID | swing_20260411_211655 |
| Mode | swing |
| Created | 2026-04-12 04:55 UTC |
| Closed | 2026-04-14 08:45 UTC |
| Entry fill | none |
| Exit fill | none |
| Realized P&L | $0 |

**What happened.** The Apr 11 run was the originating analysis. The PM placed a limit-buy at $296, which was the 23.6% Fibonacci retracement level below the $304.33 closing price at time of analysis. The reasoning was explicitly "entry on dip to $296 (not chasing at $304)." The order was placed in the early hours of April 12 and cancelled approximately 52 hours later on April 14. The stock did not pull back to $296 in that window — it likely stayed elevated or moved higher in the days following the Medicare Advantage catalyst.

The PM's rationale for the $296 entry (from decisions.json): "Entry on dip to $296 (not chasing at $304). R:R of 3.0:1 ($24 target distance vs $8 stop distance) meets the 2:1 minimum. Risk manager allows $550 max position which fits 1 share at $296. Position size: $296 = 5.9% of portfolio." The notional exposure was tiny: 1 share at $296, the smallest position in the entire portfolio (5.9% of the $5,000 paper account).

### Trade 9 — Abandoned long (never filled)

| field | value |
|---|---|
| Trade ID | 9 |
| Status | abandoned |
| Direction | long |
| Quantity | 1 share |
| Intended entry | $305.00 |
| Target price | (not recorded) |
| Stop loss | (not recorded) |
| Risk/reward | (not recorded) |
| Confidence | (not recorded) |
| Timeframe | (not recorded) |
| Run ID | (re-queue from swing_20260411_211655 or new run) |
| Mode | swing |
| Created | 2026-04-14 08:45 UTC |
| Closed | 2026-04-14 08:45 UTC |
| Entry fill | none |
| Exit fill | none |
| Realized P&L | $0 |

**What happened.** Trade 9 was created and abandoned at virtually the same timestamp (2026-04-14 08:45 UTC), indicating the system attempted to re-place the UNH order at a revised entry of $305 — likely reflecting that the stock had moved higher and the original $296 level was no longer reachable — but immediately flagged the order as unable to proceed and marked it abandoned. This could reflect a constraint from the monitor (e.g., a daily open-market check failing to queue the order), an allowed-actions block, or a mismatch between the revised entry price and the available cash limit. No fill occurred.

## Closed — older than 30 days

No trades.

## Prior run decisions (no orders placed)

The Apr 11 swing run (swing_20260411_211655) is the only run that analyzed UNH in the dataset available at bootstrap time. The buy signal from that run originated both trade records above.

| run_id | date | decision | confidence | action |
|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | buy | 58% | 1 share at $296 limit, target $320, stop $288 |

## Lifetime stats

| metric | value |
|---|---|
| Total trades (with order placed) | 2 |
| Filled entries | 0 |
| Cancelled orders | 1 (trade ID 1) |
| Abandoned orders | 1 (trade ID 9) |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 |
| Net P&L | $0.00 |
| Win rate (closed, filled) | n/a — no fills |
| Average hold time | n/a — no fills |
| Average R:R on entry | 3.0:1 (one data point, trade ID 1) |
| Runs analyzed | 1 (swing_20260411_211655) |
| No-trade decisions | 0 |
| Buy decisions | 1 |
| Short decisions | 0 |
| Max capital at risk | $296 (5.9% of $5,000 paper account) |

## Notes and lessons

**The system was disciplined about entry price — possibly too disciplined.** The PM explicitly refused to chase UNH at $304 when the signal was generated, opting for a limit at $296 (a $8 pullback from the close). If the stock continued higher after the Medicare catalyst without giving back that $8, the order would never fill — which is exactly what appears to have happened. This is the correct behavior (the 3:1 R:R was calculated from the $296 entry; buying at $304 shrinks the target distance without improving the stop, worsening R:R), but it means the system missed the trade.

**The re-queue at $305 is puzzling.** Trade 9's entry price of $305 is above the original close of $304.33, not below it. This suggests the monitor may have attempted to revise the order upward to chase the stock after it moved — and then immediately self-cancelled because the revised R:R math no longer worked. Worth investigating the monitor's re-queue logic if this pattern recurs.

**UNH was the only long in a mostly-short portfolio.** The Apr 11 portfolio had 3 shorts (XOM, CVX, NKE) and just 1 long (UNH) at 5.9% of capital. The small size reflects genuine risk management — UNH's daily volatility was at the 68th percentile, earnings were 8 days away, and the maximum allowed position was $550. At $296/share, only 1 share fit the constraint.

**Next run priority.** If a future run re-analyzes UNH post-April 21 earnings, the key question is whether the thesis held: did earnings confirm recovery or validate the bear case? The gap origin at $281 is the line in the sand — a post-earnings close above it would suggest the thesis survived; a close below it means the Medicare catalyst was absorbed and reversed.
