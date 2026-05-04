---
name: TSLA trades
last_updated: 2026-05-04
last_run_id: 20260504_161542
target_words: 800
stale_after_days: 60
word_count: 762
summary: No fills in trade_ledger.json per_ticker_history[TSLA]; five swing runs analyzed (Apr 11, Apr 15, Apr 17, May 1, May 4); model recommended 1 unexecuted short (Apr 15, earnings risk) and 4 holds; consistent R/R failure and resistance-zone caution across all runs near $387-399 zone.
---

# TSLA — Trades

## TL;DR

TSLA has been analyzed across five swing runs (April–May 2026). The model recommended one short (April 15, unexecuted due to earnings binary) and four holds. No TSLA trade has ever been executed — `trade_ledger.json per_ticker_history[TSLA]` shows zero rows across all runs through 20260504_161542. The consistent theme: price keeps returning to the $387–$399 bear-rally resistance zone with R/R below 2:1, and macro conditions have repeatedly blocked entry.

## Open positions

None. `trade_ledger.json per_ticker_history[TSLA]: []` (run 20260504_161542 — authoritative).

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

**Why unexecuted?** April 22 earnings binary 7 days away — any stop becomes meaningless against a 15-20% potential gap. Confidence only 49%. PM sized to 1 share and placed no order; tracker.db confirms no fill. [source: runs/20260415_093758/decisions.json]

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

**Why hold?** Price at $390.82 still inside $387–$399 resistance cluster. 4 of 5 swing agents neutral; 1 bullish (mean_reversion, conditional limit-order only). R/R at current price ~1.96:1 fails 2:1 minimum. Head Trader conf 38, below 40 threshold. Iran escalation (May 4 missile reports near Jask) added macro veto on high-beta growth names. Three prior TSLA runs near this same zone all resulted in holds — the consistency is a signal in itself. [source: runs/20260504_161542/decisions.json, trade_ledger.json]

---

## Closed positions

None. No fills ever executed for TSLA.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades executed | 0 |
| trade_ledger.json rows (TSLA) | 0 |
| Model runs analyzed | 5 |
| Unexecuted shorts recommended | 1 (Apr 15, earnings risk) |
| Holds issued | 4 (Apr 11, Apr 17, May 1, May 4) |
| Realized P&L | $0 |
| Unrealized P&L | $0 |

## Last updated

2026-05-04. Sourced from `trade_ledger.json per_ticker_history[TSLA]` (0 rows, run 20260504_161542) + decisions.json from runs swing_20260411_211655, 20260415_093758, 20260417_233350, 20260501_160246, 20260504_161542. Supersedes bootstrap entry (2026-04-29) which covered only 3 runs.
