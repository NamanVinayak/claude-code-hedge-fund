---
name: TSLA trades
last_updated: 2026-05-07
last_run_id: 20260507_160055
target_words: 800
stale_after_days: 60
word_count: 822
summary: No fills in trade_ledger.json per_ticker_history[TSLA]; eight swing runs analyzed (Apr 11, Apr 15, Apr 17, May 1, May 4, May 5, May 6, May 7); model recommended 1 unexecuted short (Apr 15, earnings risk) and 7 holds; consistent R/R failure and resistance-zone caution across all runs near $387-409 zone.
---

# TSLA — Trades

## TL;DR

TSLA has been analyzed across eight swing runs (April–May 2026). The model recommended one short (April 15, unexecuted due to earnings binary) and seven holds. No TSLA trade has ever been executed — `trade_ledger.json per_ticker_history[TSLA]` shows zero rows across all runs through 20260507_160055. The consistent theme: price keeps returning to the $387–$409.28 bear-rally resistance zone with R/R below 2:1, and macro or setup conditions have repeatedly blocked entry. On May 7, price pushed intraday to $406.85 (near the $409.28 ceiling) but failed to confirm a daily close above the zone — still watch-not-act.

## Open positions

None. `trade_ledger.json per_ticker_history[TSLA]: []` (run 20260507_160055 — authoritative).

## Model decisions log (all unexecuted)

### Run: swing_20260411_211655 — Hold

| Field | Value |
|---|---|
| Run date | 2026-04-11 |
| Action | HOLD |
| Reference price | $349.00 |
| Bear target | $330.00 |
| Stop | $362.00 |
| R/R | 1.5:1 (failed 2:1 minimum) |
| Confidence | 55% |

**Why hold?** Directional signal bearish (ADX 29.5, bearish EMAs, Head Trader 62% bear with 78% agent agreement). But R/R only 1.5:1 — 19 points downside vs. 13-point stop distance. Model said: "hold until bounce to $357 (10 EMA) offers better R/R." [source: runs/swing_20260411_211655/decisions.json]

---

### Run: 20260415_093758 — Short (1 share, unexecuted)

| Field | Value |
|---|---|
| Run date | 2026-04-15 |
| Action | SHORT |
| Recommended qty | 1 share |
| Entry price | $391.86 |
| Target | $343.80 |
| Stop | $399.60 |
| R/R | 6.21:1 |
| Confidence | 49% |
| Timeframe | 5–10 days |

**Why short?** Stock bounced into $387–$399 resistance cluster. Daily downtrend intact. Four bearish strategies agreed. R/R 6.21:1 was exceptional.

**Why unexecuted?** April 22 earnings binary 7 days away — any stop becomes meaningless against a 15-20% potential gap. Confidence only 49%. PM sized to 1 share and placed no order; trade_ledger confirms no fill. [source: runs/20260415_093758/decisions.json]

---

### Run: 20260417_233350 — Hold

| Field | Value |
|---|---|
| Run date | 2026-04-17 |
| Action | HOLD |
| Reference price | $391.95 |
| R/R | 1.64:1 (failed 2:1 minimum) |
| Confidence | 48% |

**Why hold?** Daily bear + hourly bull = multi-timeframe conflict. Momentum split (5d positive, 21d negative). R/R 1.64:1 below minimum. [source: runs/20260417_233350/decisions.json]

---

### Run: 20260501_160246 — Hold

| Field | Value |
|---|---|
| Run date | 2026-05-01 |
| Action | HOLD |
| Reference price | $390.82 (May 1 close $381.63) |
| Conditional entry | $381–$385 pullback zone |
| Target | $409.28 |
| Stop | $365 |
| Conditional R/R | 2.7:1 |
| Confidence | 35% |

**Why hold?** Q1 earnings resolved (EPS $0.41 beat, gross margin 18.03%). Price surged +3.8% on 2.74x volume into $387–$399 resistance. R/R fails 2:1 at all current-price entries. Head Trader conf 35, below 40 threshold. Watch zone: $381–$385 pullback with bullish daily candle. [source: runs/20260501_160246/decisions.json]

---

### Run: 20260504_161542 — Hold

| Field | Value |
|---|---|
| Run date | 2026-05-04 |
| Action | HOLD |
| Reference price | $390.82 |
| Conditional entry | $381–$385 pullback zone |
| Target | $409.28 |
| Stop | $364 |
| Conditional R/R | ~3:1 from entry zone midpoint |
| Confidence | 38% |

**Why hold?** Price at $390.82 still inside $387–$399 resistance cluster. 4 of 5 swing agents neutral; 1 bullish (mean_reversion, conditional limit-order only). R/R at current price ~1.96:1 fails 2:1 minimum. Head Trader conf 38, below 40 threshold. Iran escalation (May 4 missile reports near Jask) added macro veto on high-beta growth names. [source: runs/20260504_161542/decisions.json, trade_ledger.json]

---

### Run: 20260505_160654 — Hold (6th consecutive)

| Field | Value |
|---|---|
| Run date | 2026-05-05 |
| Action | HOLD |
| Reference price | $392.51 |
| Conditional entry (long) | $381–$385 pullback with bullish daily reversal candle |
| Conditional entry (breakout) | Daily close above $409.28 on 1.5x+ volume |
| Target (if entered) | $409.28 (long from dip) or $437 (breakout measured move) |
| Stop | $379.00 (below recent low $378.80) |
| Conditional R/R | ~3:1 from $381–$385 dip zone; 1.26:1 from current price (fails 2:1) |
| Confidence | 35% |

**Why hold?** Price at $392.51 inside the $387–$399 bear-rally resistance cluster (14–15 tests). Head Trader confidence 35, below 40 capital-deployment threshold. Vote tally: 4 neutral, 1 bearish (catalyst_news, 58 conf on Warsh vote May 15 macro headwind); 0 bullish. Portfolio already carries 3 shorts (AMD, JNJ, META). [source: runs/20260505_160654/decisions.json, trade_ledger.json per_ticker_history[TSLA]=[]]

---

### Run: 20260506_160353 — Hold (7th consecutive)

| Field | Value |
|---|---|
| Run date | 2026-05-06 |
| Action | HOLD |
| Reference price | $389.37 |
| Conditional entry (long) | $381–$385 pullback with bullish daily reversal candle |
| Conditional entry (breakout) | Daily close above $409.28 on 1.5x+ volume |
| Target (if entered) | $409.28 (long from dip), stop $379, R/R ~3:1 |
| Confidence | 32% |
| Allowed actions | hold / short only |

**Why hold?** Price at $389.37, 7th consecutive run inside the $387–$399 resistance cluster. Head Trader confidence 32. EMA structure deteriorated (50 EMA above 10 EMA and 21 EMA). Short fade R/R 0.71:1 fails 2:1 minimum. Hourly OBV bearish divergence confirmed by 4/5 agents. [source: runs/20260506_160353/decisions.json, trade_ledger.json per_ticker_history[TSLA]=[]]

---

### Run: 20260507_160055 — Hold (8th consecutive)

| Field | Value |
|---|---|
| Run date | 2026-05-07 |
| Action | HOLD |
| Reference price | $406.85 intraday / $398.73 daily close |
| Conditional entry (long) | $385–$390 pullback with bullish daily reversal candle + hourly OBV reversal |
| Conditional entry (breakout) | Daily close above $409.28 on 1.5x+ volume |
| Target if breakout | $432 measured move; stop $404; R/R ~3.9:1 |
| Target if dip | $409.28; stop $379; R/R ~3:1 |
| Confidence | 38% |
| Allowed actions | hold / short |

**Why hold?** Price at $406.85 intraday — near the $409.28 ceiling but NO daily close above it. Volume 0.85x — fails the 1.5x breakout confirmation gate. RSI-7 76.34 overbought. EMA fan tangled (50 EMA $386.88 above 10 EMA $386.54). R/R from current price (upside $409.28 = 0.6%, downside to $381.40 support = 6.3%) is 0.1:1 — catastrophically below 2:1 minimum. Head Trader confidence 38, below 40 threshold. Vote tally: 5/5 neutral (cleanest possible non-trade signal). Analyst consensus PT $405.47 at essentially the same price as current — no consensus upside. Hourly OBV bearish divergence cross-confirmed by 4/5 agents across May 6 AND May 7 (two consecutive runs) — strongest cross-confirmed technical read in the dataset. Warsh Fed Chair vote May 15 (~6 days) is asymmetric risk for high-beta growth names. [source: runs/20260507_160055/decisions.json, trade_ledger.json per_ticker_history[TSLA]=[]]

---

## Closed positions

None. No fills ever executed for TSLA.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades executed | 0 |
| trade_ledger.json rows (TSLA) | 0 |
| Model runs analyzed | 8 |
| Unexecuted shorts recommended | 1 (Apr 15, earnings risk) |
| Holds issued | 7 (Apr 11, Apr 17, May 1, May 4, May 5, May 6, May 7) |
| Realized P&L | $0 |
| Unrealized P&L | $0 |

## Last updated

2026-05-07. Sourced from `trade_ledger.json per_ticker_history[TSLA]` (0 rows, run 20260507_160055) + decisions.json from runs swing_20260411_211655, 20260415_093758, 20260417_233350, 20260501_160246, 20260504_161542, 20260505_160654, 20260506_160353, 20260507_160055. Supersedes 2026-05-06 entry — adds 8th consecutive hold decision; price pushed intraday to $406.85 but failed to confirm breakout; 5/5 unanimous neutral; hourly OBV divergence cross-confirmed two consecutive runs.
