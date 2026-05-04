---
name: NVDA trades
last_updated: 2026-05-04
last_run_id: 20260504_125732
target_words: 800
stale_after_days: 60
word_count: 737
summary: One formally closed position — 16 shares at $209.25 stopped out 2026-04-30 at $205.30, P&L -$63.20 (corrected from buggy -$264.65; see lessons.md). Four prior abandoned tracker.db entries from Apr 14-29 (no realized P&L). No open positions as of 2026-05-04.
---

# NVDA — Trades

## TL;DR

One formally closed NVDA position in Turso (trade id 112): originally booked as 67 shares @ $209.25 due to a phantom $100K budget bug (commit b2b472d), now corrected to its proper sizing of 16 shares (14.2% vol-adjusted limit on the actual $25K paper account). Stopped out at $205.30 on 2026-04-30, realized P&L **-$63.20** (corrected from the buggy -$264.65 that briefly appeared in earlier wiki versions). Four prior tracker.db entries (IDs 6, 12, 13, 21) were marked abandoned 2026-04-29 with no realized P&L. No open NVDA positions as of 2026-05-01. Latest 2026-05-01 run scored HOLD (R/R 2.67, conf 35) pending hourly reversal candle at $196.75–$199.50.

## Open positions

None. Last position closed 2026-04-30.

## Recently Closed — last 30 days

### Trade 112 — CLOSED 2026-04-30 (run 20260430_060402)

| Field | Value |
|---|---|
| Entry price | $209.25 |
| Exit price | $205.30 |
| Quantity | **16 shares (corrected — see note)** |
| P&L | **-$63.20 (corrected from -$264.65)** |
| Position size | $3,348 (corrected from $14,020) |
| Closed via | stop_hit |
| Days held | 0 (entered and stopped out same day, 2026-04-30) |
| Run | 20260430_060402 |
| Turso trade id | 112 |

**Notes:** Originally booked at 67 shares ($14,020) because aggregate.py was running with a hardcoded `--cash 100000` budget instead of reading `paper_account_size` from `tracker/watchlist.json` (which was $5K at the time, now $25K). Bug fixed in commit `b2b472d`. With proper $25K budget × 14.167% vol-adjusted limit, position should have been **16 shares ($3,348)**. The trade was corrected on 2026-05-01 to reflect the strategy-appropriate size; original 67-share buggy values are preserved in the `fills` audit log. Stop at $205.30 = hourly Fib 61.8% level from the $216.83 high. 4/5 swing agents were bullish on entry (ADX 54.67, pullback to Fib 38.2% support), but price broke below the stop intraday.

## Closed trades — 2026-04-14 to 2026-04-29

### Trade 12 — FILLED, abandoned
- **Qty:** 2 shares | **Fill:** $197.29 | **Exit mark:** $213.17 (not a formal close)
- **Status:** abandoned 2026-04-29 | **Created/Filled:** 2026-04-15
- **Implied P&L:** +$31.76 (unrealized; not recorded in DB pnl column)
- **Source:** 20260415_093758 — buy 6 shares at $198.47 limit; 7/10 strategies bullish; breakout above $196.51.

### Trade 13 — FILLED, abandoned
- **Qty:** 4 shares | **Fill:** $197.15 (favorable vs $198.50 limit) | **Exit mark:** $213.17
- **Status:** abandoned 2026-04-29 | **Created/Filled:** 2026-04-15
- **Implied P&L:** +$64.08 (unrealized; not in DB)
- **Source:** 20260415_093758 — same PM decision as trade 12 (6 shares split across two orders).

**Combined (trades 12+13):** 6 shares, blended cost $197.22, implied unrealized P&L at mark = **+$95.70 (+8.1%)**.

### Trade 6 — NOT FILLED, abandoned
- **Qty:** 3 shares | **Limit:** $188.00 | **Fill:** None
- **Status:** abandoned 2026-04-29 | **Source:** swing_20260411_211655 — PM held (R:R 1.7:1 below 2:1 minimum); $188 limit never hit.

### Trade 21 — NOT FILLED, abandoned
- **Qty:** 50 shares | **Limit:** $199.50 | **Fill:** None
- **Status:** abandoned 2026-04-29 | **Source:** 20260417_233350 — PM bought at $199.50 limit; price moved away.

## Run decision history

| Run ID | Date | Action | Entry | Target | Stop | R:R | Conf |
|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | $186 | $196 | $180 | 1.7:1 | 65 |
| 20260415_093758 | 2026-04-15 | **buy** 6 sh | $198.47 | $209.70 | $189.10 | 2.27:1 | 62 |
| 20260417_233350 | 2026-04-17 | **buy** 50 sh | $199.50 | $210.00 | $195.00 | 2.33:1 | 78 |
| validation_20260427_113014 | 2026-04-27 | buy (conditional) | $207.50 | $231.00 | $207.00 | contingent | 55 |
| sanity_20260429_031705 | 2026-04-29 | **hold** | $197.20 (cost) | $231.00 | $207.00 | 2.9:1 | 55 |
| 20260430_060402 | 2026-04-30 | **buy 67 sh** (only this one ingested → corrected to 16 sh, trade 112) | $209.25 | $222.50 | $205.30 | 3.35:1 | 72 |
| 20260430_124724 | 2026-04-30 | buy 3 sh (decision JSON only — NEVER ingested into Turso, no real position) | $209.50 | $221.89 | $205.30 | 2.95:1 | 74 |
| **20260501_124529** | **2026-05-01** | **hold** | n/a | $212.25 (conditional) | $194.00 (conditional) | 2.67:1 | 35 |
| **20260504_125732** | **2026-05-04** | **hold** | n/a | $210.50 (conditional) | $194.00 (conditional) | ~2.6:1 | 44 |

## Lessons learned

1. **Apr 17 50-share order never filled.** Price had moved past $199.50 before the order was placed; the limit was too tight. Do not chase.
2. **Apr 15 entry was excellent.** Fills of $197.29 and $197.15 were below the $198.47 limit — favorable slippage. Position reached +8.1% unrealized by Apr 29.
3. **Abandonment vs formal close.** Four prior trades (IDs 6, 12, 13, 21) show None in the DB pnl column — the +$95.70 implied gain is not in realized P&L.
4. **Model waited correctly for pullback.** All prior runs flagged overextension. Apr 15 and Apr 30 are the only two runs where a clean entry existed near the constructive zone.
5. **EMA pullback dip-buy: 0 wins, 1 stop, -$63.20 (corrected) in 30 days.** This setup type requires a confirmed hourly reversal candle at the EMA-21 / Fib 38.2% confluence ($196.75–$197.67) before re-entry — not a blind dip-buy.
6. **$208.20 invalidation level must be respected.** The Apr 30 entry at $209.25 was just above $208.20. Price went on to break $208.20 decisively. The wiki's own hard stop was the right signal — trust it.
7. **Sizing bug taught us a meta-lesson.** A buggy $100K phantom budget produced a position 4× too large. The strategy itself wasn't broken — the engineering was. Going forward, the new conviction-based sizing model + hard caps should prevent this recurring.

## Lifetime stats

| Metric | Value |
|---|---|
| Total tracker.db / Turso trades | 5 (4 prior abandoned + 1 formally closed) |
| Filled (prior, abandoned) | 2 (trades 12, 13) |
| Unfilled (prior, abandoned) | 2 (trades 6, 21) |
| Formally closed | 1 (trade 112, stop_hit, corrected -$63.20) |
| Recorded realized P&L | **-$63.20** (corrected from buggy -$264.65) |
| Win rate (formally closed trades) | 0% (0 wins / 1 closed) |
| Implied unrealized P&L (abandoned) | +$95.70 (+8.1%) — not in realized P&L |
| **Current open** | **None** |
