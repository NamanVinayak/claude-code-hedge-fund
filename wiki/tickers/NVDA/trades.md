---
name: NVDA trades
last_updated: 2026-05-01
last_run_id: 20260430_124724
target_words: 800
stale_after_days: 60
word_count: 920
summary: 4 abandoned DB trades (2026-04-29); 1 open position remaining — 3 shares at $209.50 (run 20260430_124724); Position 1 (67 shares at $209.25) stop_hit 2026-04-30, P&L -$264.65.
---

# NVDA — Trades

## TL;DR

Four tracker.db entries (trade IDs 6, 12, 13, 21) all marked "abandoned" on 2026-04-29. Position 1 (67 shares @ $209.25, run 20260430_060402) was stop-hit on 2026-04-30 at $205.30, P&L -$264.65. One position remains open as of 2026-04-30: 3 shares at $209.50 (run 20260430_124724). Stop: $205.30 (hourly Fib 61.8%), primary target: $221.89 (cluster median), extended target: $231.13 (daily Fib 1.272), R/R: 2.95:1, timeframe: 5–12 trading days. Hard exit deadline ~May 17 (3-day pre-earnings blackout before ~May 20 NVDA earnings).

## Open positions

### Position 2 — 2026-04-30 (run 20260430_124724)
- **Direction:** Long | **Quantity:** 3 shares | **Entry:** $209.50
- **Stop:** $205.30 (hourly Fib 61.8% from $216.83 high) | **Target:** $221.89 | **R/R:** 2.95:1
- **Extended target:** $231.13 (daily Fib 1.272 ext — activates on close above $216.83 with expanding volume)
- **Confidence:** 74 | **Invalidation:** Close below $208.20 before new high
- **Hard exit deadline:** ~May 17, 2026 (3-day pre-earnings blackout)
- **Position value:** $628.50 (3 × $209.50); risk cap $708.36 (14.2% of $5K capital, volatility-adjusted at 38.3% annualized vol)
- **Rationale:** 4/5 swing agents bullish (swing_breakout neutral — not bearish); ADX 54.67 strongest trend in run history; pullback to hourly Fib 38.2% / $208.20 volume-confirmed support (15 tests). (source: decisions.json, signals_combined.json, 20260430_124724)

## Recently Closed

### Trade: Long 67 shares NVDA — CLOSED 2026-04-30

| Field | Value |
|---|---|
| Entry price | $209.25 |
| Exit price | $205.30 |
| P&L | -$264.65 |
| Closed via | stop_hit |
| Days held | 0 (entered and stopped out same day, 2026-04-30) |
| Run | `N/A` |

**Notes:** Position 1 from run 20260430_060402 (67 shares). Stop at $205.30 was the hourly Fib 61.8% level from the $216.83 high. 4/5 swing agents were bullish on entry (ADX 54.67, pullback to Fib 38.2% support), but price broke below the stop zone intraday. Exit filled at $205.30. Thesis remains under review.

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
| **20260430_124724** | **2026-04-30** | **buy 3 sh** | **$209.50** | **$221.89** | **$205.30** | **2.95:1** | **74** |

## Lessons learned

1. **Apr 17 50-share order never filled.** Price had moved past $199.50 before the order was placed; the limit was too tight. Do not chase.
2. **Apr 15 entry was excellent.** Fills of $197.29 and $197.15 were below the $198.47 limit — favorable slippage. Position reached +8.1% unrealized by Apr 29.
3. **Abandonment vs formal close.** All four prior trades show None in the DB pnl column — the +$95.70 implied gain is not in realized P&L.
4. **Model waited correctly for pullback.** All prior runs flagged overextension. Apr 15 and Apr 30 are the only two runs where a clean entry existed near the constructive zone.
5. **Second run on same day adds 3 shares.** Both Apr 30 runs (060402 and 124724) are long at the same support zone — the thesis is consistent across both dispatches; position sizing is disciplined within risk manager caps.
6. **Stop respected on Position 1.** The 67-share position entered 2026-04-30 was stopped out the same day at $205.30 (-$264.65). The stop level (hourly Fib 61.8%) held as a hard floor — execution was correct even though the outcome was a loss. Position 2 (3 shares) remains open.

## Lifetime stats

| Metric | Value |
|---|---|
| Total DB trades | 4 (all prior abandoned) |
| Filled (prior) | 2 (trades 12, 13) |
| Unfilled (prior) | 2 (trades 6, 21) |
| Formally closed | 1 (Position 1, stop_hit 2026-04-30) |
| Recorded realized P&L | -$264.65 |
| Win rate (formally closed trades) | 0% (0 wins / 1 closed) |
| Implied unrealized P&L (abandoned) | +$95.70 (+8.1%) |
| **Current open — Position 2** | **3 shares @ $209.50 (run 20260430_124724)** |
| Open risk (Position 2) | $12.60 (3 × $4.20 stop distance) |
| Open target gain (Position 2) | $37.17 (3 × $12.39 to $221.89 target) |
