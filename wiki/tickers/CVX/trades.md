---
name: CVX trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 904
summary: Full trade journal for CVX — 2 short attempts, both cancelled/abandoned, zero fills
---

## TL;DR

CVX has been targeted twice for a short position, both times from the same swing run thesis (Apr 11). Neither trade filled: the first order was cancelled outright, the second was abandoned (likely due to unfilled orders expiring or a manual decision). No realized P&L, no fills, zero closed trades. The model was right on direction (CVX did fall post-April 11) but paper trading mechanics prevented capturing the move.

---

## Open Positions

None. Both CVX positions have been closed (cancelled/abandoned) as of April 29.

---

## Closed Trades — All CVX History

### Trade #4 — Short (Cancelled)

| Field | Value |
|---|---|
| Trade ID | 4 |
| Ticker | CVX |
| Direction | Short |
| Quantity | 5 shares |
| Status | **Cancelled** |
| Entry price (intended) | $192.00 |
| Exit fill price | None (never filled) |
| P&L | $0 (no fill) |
| Created at | 2026-04-12 04:56 UTC |
| Closed at | Not recorded in DB |

**Context:** This was the first execution attempt for the April 11 swing run CVX signal. The run (`swing_20260411_211655`) recommended shorting 5 shares at $192 — a "short on relief bounce" setup. The current price on April 11 was approximately $188.55, so the entry required waiting for a bounce to $192 before placing the short. The order was placed on April 12 and subsequently cancelled. Most likely cause: the $192 bounce entry was never reached as CVX continued lower without the expected relief rally, rendering the limit order stale.

---

### Trade #10 — Short (Abandoned)

| Field | Value |
|---|---|
| Trade ID | 10 |
| Ticker | CVX |
| Direction | Short |
| Quantity | 5 shares |
| Status | **Abandoned** |
| Entry price (intended) | $192.00 |
| Exit fill price | None (never filled) |
| P&L | $0 (no fill) |
| Created at | 2026-04-14 08:45 UTC |
| Closed at | 2026-04-29 11:19 UTC |

**Context:** A second short attempt at the same $192 entry price, placed two days after the first cancellation. This order remained open for more than two weeks before being marked abandoned on April 29 — the date of this wiki bootstrap. The "abandoned" status in the tracker DB typically means the position was never filled and was manually or systematically written off. The Moomoo paper trading system uses `TimeInForce.DAY` orders that expire at end of day, so this likely represents a repeated daily re-placement that was ultimately written off rather than left as a zombie order.

---

## Why Neither Trade Filled

The swing model set the CVX entry at $192, deliberately above the then-current price (~$188.55 on April 11), because the stochastic oscillator was at 7.37 — deeply oversold. The thesis was: wait for a relief bounce to $192, then enter short. If the bounce never came — if CVX continued to decline from $188.55 without first bouncing to $192 — the limit sell-short order would never trigger. This is the classic "short on bounce" execution risk: the setup is disciplined, but if the stock gaps down or slides without a counter-rally, the trade is missed entirely.

This is a known failure mode in swing trading. The model explicitly noted in the run's risk notes: "All 3 short entries assume a relief bounce before entering. If stocks continue falling without bouncing, the entry prices may not be reached. Adjust entries downward if needed." (Source: `swing_20260411_211655/decisions.json`, risk_notes)

---

## Lifetime Stats

| Metric | Value |
|---|---|
| Total trade attempts | 2 |
| Fills | 0 |
| Open positions | 0 |
| Closed positions | 2 |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 |
| Win rate | N/A (no fills) |
| Entry hit rate | 0% (0 of 2 entries triggered) |
| Average holding period | N/A |
| Direction | Both attempts: Short |
| Source runs | `swing_20260411_211655` (both trades) |

---

## Lessons for Future CVX Runs

1. **Bounce entry discipline vs. execution risk.** The $192 entry was correct in theory — entering short on a bounce offers better risk-reward than chasing a falling knife. But if the stock never bounces, the entry never triggers. Future runs should consider an alternative "break-below" entry at the then-current price with a tighter stop, especially when the stock is already at oversold extremes (stochastic < 10).

2. **Both attempts were the same thesis.** Trade #10 was effectively a retry of Trade #4 at the same price. If the thesis was unchanged and the entry level was unchanged, the retry was unlikely to behave differently unless market conditions shifted. In future, a second attempt should recalibrate the entry price to reflect the new market level.

3. **Moomoo DAY order constraint.** Paper trading on Moomoo only supports `TimeInForce.DAY` orders. For a "short on bounce" setup where the bounce might take several days, limit orders need to be re-placed daily. The "abandoned" status on Trade #10 suggests this re-placement loop was not sustained long enough or was stopped by a system-level decision.

4. **The directional call may have been correct.** CVX closed at ~$155 by late April (XOM target was also $145) based on the portfolio synthesis context. If so, the model identified a real move but the paper trading mechanics prevented capturing it.
