---
name: NVDA trades
last_updated: 2026-05-01
last_run_id: 20260501_124529
target_words: 800
stale_after_days: 60
word_count: 790
summary: All positions closed — Position 1 (67 shares at $209.25) stop_hit 2026-04-30 (-$264.65); Position 2 (3 shares at $209.50) stop_hit 2026-04-30 at $205.30 (~-$12.60 est.); 4 abandoned DB trades (2026-04-29); portfolio shows 0 NVDA long shares as of 2026-05-01.
---

# NVDA — Trades

## TL;DR

Four tracker.db entries (trade IDs 6, 12, 13, 21) all marked "abandoned" on 2026-04-29. Position 1 (67 shares @ $209.25, run 20260430_060402) was stop-hit on 2026-04-30 at $205.30, P&L -$264.65. Position 2 (3 shares @ $209.50, run 20260430_124724) was also stopped out at $205.30 on 2026-04-30 — confirmed by signals_combined.json portfolio showing 0 NVDA long shares and current price $199.57 (well below the $205.30 stop). All NVDA positions are closed as of 2026-05-01. No new entry pending — HOLD, waiting for confirmed hourly reversal candle at $196.75–$199.50 before re-entry.

## Open positions

None. All positions closed as of 2026-04-30.

## Recently Closed — last 30 days

### Position 2 — CLOSED 2026-04-30 (run 20260430_124724)

| Field | Value |
|---|---|
| Entry price | $209.50 |
| Exit price | $205.30 (stop) |
| Estimated P&L | ~-$12.60 (3 shares × $4.20 stop distance) |
| Closed via | stop_hit (price below $205.30 stop; confirmed by signals_combined portfolio = 0 long shares and recent_closed entry showing $199.57 price) |
| Days held | 0–1 (entered 2026-04-30; stopped out 2026-04-30) |
| Run | 20260430_124724 |

**Notes:** Position 2 from run 20260430_124724 (3 shares). Stop at $205.30 matched Position 1 — both were using the hourly Fib 61.8% level from the $216.83 high as the stop anchor. Price collapsed from $209.50 to $199.57 by 2026-05-01, well below the stop. The signals_combined.json portfolio for run 20260501_124529 confirms `"NVDA": {"long": 0}` with no open position. Estimated P&L based on stop price; exact fill may differ by a few cents.

### Position 1 — CLOSED 2026-04-30 (run 20260430_060402)

| Field | Value |
|---|---|
| Entry price | $209.25 |
| Exit price | $205.30 |
| P&L | -$264.65 |
| Closed via | stop_hit |
| Days held | 0 (entered and stopped out same day, 2026-04-30) |
| Run | 20260430_060402 |

**Notes:** 67 shares entered on the first Apr 30 run. Stop at $205.30 (hourly Fib 61.8%) was the agreed invalidation level. 4/5 swing agents were bullish on entry (ADX 54.67, pullback to Fib 38.2% support), but price broke below the stop zone intraday. Exit filled at $205.30. Confirmed in signals_combined.json `recent_closed` array.

## Closed trades — 2026-04-14 to 2026-04-29

### Trade 12 — FILLED, abandoned
- **Qty:** 2 shares | **Fill:** $197.29 | **Exit mark:** $213.17 (not a formal close)
- **Status:** abandoned 2026-04-29 | **Created/Filled:** 2026-04-15
- **Implied P&L:** +$31.76 (unrealized; not recorded in DB pnl column)
- **Source:** 20260415_093758 — buy 6 shares at $198.47 limit; 7/10 strategies bullish; breakout above $196.51; AI capex thesis intact.

### Trade 13 — FILLED, abandoned
- **Qty:** 4 shares | **Fill:** $197.15 (favorable vs $198.50 limit) | **Exit mark:** $213.17
- **Status:** abandoned 2026-04-29 | **Created/Filled:** 2026-04-15
- **Implied P&L:** +$64.08 (unrealized; not in DB)
- **Source:** 20260415_093758 — same PM decision as trade 12 (6 shares split across two orders).

**Combined (trades 12+13):** 6 shares, blended cost $197.22, implied unrealized P&L at mark = **+$95.70 (+8.1%)**.

### Trade 6 — NOT FILLED, abandoned
- **Qty:** 3 shares | **Limit:** $188.00 | **Fill:** None
- **Status:** abandoned 2026-04-29 | **Source:** swing_20260411_211655 — PM held (R:R 1.7:1 below 2:1 minimum); $188 limit never hit as price moved higher.

### Trade 21 — NOT FILLED, abandoned
- **Qty:** 50 shares | **Limit:** $199.50 | **Fill:** None
- **Status:** abandoned 2026-04-29 | **Source:** 20260417_233350 — PM bought at $199.50 limit; price moved away and never pulled back to limit.

## Run decision history

| Run ID | Date | Action | Entry | Target | Stop | R:R | Conf |
|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | $186 | $196 | $180 | 1.7:1 | 65 |
| 20260415_093758 | 2026-04-15 | **buy** 6 sh | $198.47 | $209.70 | $189.10 | 2.27:1 | 62 |
| 20260417_233350 | 2026-04-17 | **buy** 50 sh | $199.50 | $210.00 | $195.00 | 2.33:1 | 78 |
| validation_20260427_113014 | 2026-04-27 | buy (conditional) | $207.50 | $231.00 | $207.00 | contingent | 55 |
| sanity_20260429_031705 | 2026-04-29 | **hold** | $197.20 (cost) | $231.00 | $207.00 | 2.9:1 | 55 |
| 20260430_060402 | 2026-04-30 | **buy 67 sh** | $209.25 | $222.50 | $205.30 | 3.35:1 | 72 |
| 20260430_124724 | 2026-04-30 | **buy 3 sh** | $209.50 | $221.89 | $205.30 | 2.95:1 | 74 |
| **20260501_124529** | **2026-05-01** | **hold** | n/a | $212.25 (conditional) | $194.00 (conditional) | 2.67:1 | 35 |

## Lessons learned

1. **Apr 17 50-share order never filled.** Price had moved past $199.50 before the order was placed; the limit was too tight. Do not chase.
2. **Apr 15 entry was excellent.** Fills of $197.29 and $197.15 were below the $198.47 limit — favorable slippage. Position reached +8.1% unrealized by Apr 29.
3. **Abandonment vs formal close.** All four prior trades (IDs 6, 12, 13, 21) show None in the DB pnl column — the +$95.70 implied gain is not in realized P&L.
4. **Model waited correctly for pullback.** All prior runs flagged overextension. Apr 15 and Apr 30 are the only two runs where a clean entry existed near the constructive zone.
5. **Two same-day stops, same level.** Both Apr 30 entries (Positions 1 and 2) used stop $205.30 — both stopped out same day. Layering into the same setup on the same day with identical stops is not diversification. If Stop 1 fires, Stop 2 fires too.
6. **EMA pullback dip-buy: 0 wins, 2 stops, -$264.65+ in 30 days.** This setup type requires a longer pause before re-entry. The 38.2% Fib at $196.75 with EMA-21 at $197.67 is the next defensible level — but a confirmed reversal candle is required, not a blind dip-buy.
7. **$208.20 invalidation level must be respected.** Both Apr 30 entries were made above $208.20. Price went on to break $208.20 decisively. The wiki's own hard stop was the right signal — trust it.

## Lifetime stats

| Metric | Value |
|---|---|
| Total DB trades | 4 (all prior abandoned) + 2 open→stopped |
| Filled (prior, abandoned) | 2 (trades 12, 13) |
| Unfilled (prior, abandoned) | 2 (trades 6, 21) |
| Formally closed | 2 (Position 1 stop_hit -$264.65; Position 2 stop_hit ~-$12.60) |
| Recorded realized P&L | -$264.65 (Position 1 confirmed) + ~-$12.60 (Position 2 est.) |
| Win rate (formally closed trades) | 0% (0 wins / 2 closed) |
| Implied unrealized P&L (abandoned) | +$95.70 (+8.1%) — not in realized P&L |
| **Current open** | **None — all positions closed** |
