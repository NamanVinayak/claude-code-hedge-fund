---
name: NVDA trades
last_updated: 2026-04-29
last_run_id: sanity_20260429_031705
target_words: 800
stale_after_days: 60
word_count: 812
summary: 4 paper trades total — 2 filled (trades 12+13, 6 shares at ~$197.22 avg cost), 2 unfilled (trades 6+21); all abandoned 2026-04-29; position was never formally closed — abandoned during session cleanup.
---

# NVDA — Trades

## TL;DR

NVDA was actively paper-traded starting 2026-04-14. Four tracker.db entries exist (trade IDs 6, 12, 13, 21). Two were filled (trades 12 and 13, totaling 6 shares at blended cost ~$197.22), two were not filled (trades 6 and 21). All four were marked "abandoned" on 2026-04-29 during a position cleanup — the session that also ran the sanity run. At the time of abandonment, the mark-to-market price was $213.17 (the price used in the sanity run). No pnl field was populated in the DB for any of these trades, meaning P&L was not formally recorded on close.

## Open positions

None — all trades marked abandoned as of 2026-04-29.

## Closed trades — 2026-04-14 to 2026-04-29

### Trade 12 — FILLED, abandoned
- **Direction:** Long
- **Quantity:** 2 shares
- **Limit entry price:** $198.47
- **Entry fill price:** $197.29
- **Exit fill price:** $213.17 (mark at abandonment — not a formal close)
- **Status:** abandoned (2026-04-29 11:19:51)
- **Created:** 2026-04-15 17:05:49
- **Entered:** 2026-04-15 17:07:26
- **Closed:** 2026-04-29 11:19:51
- **Gross P&L (implied):** ($213.17 − $197.29) × 2 = **+$31.76** (unrealized at abandonment; not recorded in DB pnl column)
- **Source run:** 20260415_093758 — PM decision: buy 6 shares at $198.47, target $209.70, stop $189.10, R:R 2.27, confidence 62. Reasoning: 7/10 strategies bullish; breakout above $196.51 resistance confirmed; AI capex supercycle intact.

### Trade 13 — FILLED, abandoned
- **Direction:** Long
- **Quantity:** 4 shares
- **Limit entry price:** $198.50
- **Entry fill price:** $197.15 (slightly better than limit — favorable fill)
- **Exit fill price:** $213.17 (mark at abandonment)
- **Status:** abandoned (2026-04-29 11:19:51)
- **Created:** 2026-04-15 17:12:54
- **Entered:** 2026-04-15 17:14:47
- **Closed:** 2026-04-29 11:19:51
- **Gross P&L (implied):** ($213.17 − $197.15) × 4 = **+$64.08** (unrealized at abandonment; not recorded in DB pnl column)
- **Source run:** 20260415_093758 — same PM decision as trade 12 (6 shares total placed in two separate orders).

**Combined position (trades 12 + 13):** 6 shares, blended fill cost $197.22 (weighted avg of $197.29×2 + $197.15×4 = $1,183.18 / 6), implied unrealized P&L at $213.17 = **+$95.70 (+8.1%)**.

### Trade 6 — NOT FILLED, abandoned
- **Direction:** Long
- **Quantity:** 3 shares
- **Limit entry price:** $188.00
- **Entry fill price:** None (order expired unfilled)
- **Status:** abandoned (2026-04-29 11:19:51)
- **Created:** 2026-04-14 08:45:51
- **Source run:** swing_20260411_211655 — PM decision: hold (R:R 1.7:1 below 2:1 minimum); head trader bullish at 72%, but needed pullback to $182 for 3.5:1 R:R. The $188 limit was likely placed as a conditional/pullback order that was never hit as price moved up instead.

### Trade 21 — NOT FILLED, abandoned
- **Direction:** Long
- **Quantity:** 50 shares
- **Limit entry price:** $199.50
- **Entry fill price:** None (order expired unfilled)
- **Status:** abandoned (2026-04-29 11:19:51)
- **Created:** 2026-04-18 00:18:19
- **Source run:** 20260417_233350 — PM decision: buy 50 shares at $199.50, target $210.00, stop $195.00, R:R 2.33, confidence 78. Reasoning: 78% agent agreement; multi-TF aligned; Druckenmiller bullish; sector leading. Order was placed but never filled — price presumably moved away from the $199.50 limit.

## Run decision history

| Run ID | Date | Action | Entry | Target | Stop | R:R | Confidence | Mode |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold (R:R below floor) | $186 | $196 | $180 | 1.7:1 | 65 | swing |
| 20260415_093758 | 2026-04-15 | **buy** 6 shares | $198.47 | $209.70 | $189.10 | 2.27:1 | 62 | swing |
| 20260417_233350 | 2026-04-17 | **buy** 50 shares | $199.50 | $210.00 | $195.00 | 2.33:1 | 78 | swing |
| validation_20260427_113014 | 2026-04-27 | buy (conditional pullback) | $207.50 | $231.00 | $207.00 | contingent | 55 | swing |
| sanity_20260429_031705 | 2026-04-29 | **hold** existing position | $197.20 (cost) | $231.00 | $207.00 | 2.9:1 from market | 55 | swing |

## Lessons learned from this ticker

1. **The Apr 17 50-share order (trade 21) never filled.** The PM called for a buy at $199.50; price had already moved past that level and did not pull back. This is exactly the "do not chase" discipline the head trader enforces — the model was right not to fill at market, but the limit order was set too tight relative to where price was trading.

2. **The Apr 15 entry (trades 12+13) was excellent.** Fill prices of $197.29 and $197.15 were at the lower bound of the model's $198.47 limit — favorable slippage worked in our favor. The position went from flat to +8.1% unrealized by Apr 29 when price was $213.17.

3. **Abandonment vs formal close.** All four trades were marked "abandoned" rather than "closed with P&L." The DB pnl column shows None for all four. This means the +$95.70 implied gain on trades 12+13 is not reflected in the realized P&L tracker. If these trades are resurrected in a future session, they should be reconstructed with the Apr 15 fill prices as cost basis.

4. **The model consistently said "wait for a pullback."** All 5 runs flagged the stock as overextended at the time of each run. The Apr 15 run was the only one where a clean entry existed near the EMA-10. The Apr 17 run still tried to buy at $199.50 (above EMA-10 at the time) and missed. The Apr 27 and Apr 29 runs correctly said "hold what we have, no new entry above $211."

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades | 4 |
| Filled | 2 (trades 12, 13) |
| Unfilled | 2 (trades 6, 21) |
| Abandoned | 4 |
| Formally closed | 0 |
| Recorded realized P&L | $0 (not captured) |
| Implied unrealized P&L at abandonment | +$95.70 (+8.1% on cost) |
| Avg fill price (filled trades) | $197.22 |
| Avg exit price (mark) | $213.17 |
| Holding period (filled) | 2026-04-15 to 2026-04-29 = 14 calendar days |
