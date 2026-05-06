---
name: TSLA trades
last_updated: 2026-05-06
last_run_id: 20260506_160353
target_words: 800
stale_after_days: 60
word_count: 818
summary: No fills in trade_ledger.json per_ticker_history[TSLA]; seven swing runs analyzed (Apr 11, Apr 15, Apr 17, May 1, May 4, May 5, May 6); model recommended 1 unexecuted short (Apr 15, earnings risk) and 6 holds; consistent R/R failure and resistance-zone caution across all runs near $387-399 zone.
---

# TSLA — Trades

## TL;DR

TSLA has been analyzed across seven swing runs (April–May 2026). The model recommended one short (April 15, unexecuted due to earnings binary) and six holds. No TSLA trade has ever been executed — `trade_ledger.json per_ticker_history[TSLA]` shows zero rows across all runs through 20260506_160353. The consistent theme: price keeps returning to the $387–$399 bear-rally resistance zone with R/R below 2:1, and macro or setup conditions have repeatedly blocked entry. Portfolio book tilt (currently 4 net short + 2 net long open positions in other tickers) adds an additional reason to stay neutral on TSLA at record-high market.

## Open positions

None. `trade_ledger.json per_ticker_history[TSLA]: []` (run 20260506_160353 — authoritative).

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

**Why hold?** Price at $392.51 inside the $387–$399 bear-rally resistance cluster (14–15 tests). Head Trader confidence 35, below 40 capital-deployment threshold. Vote tally: 4 neutral, 1 bearish (catalyst_news, 58 conf on Warsh vote May 15 macro headwind); 0 bullish. The portfolio already carries 3 shorts (AMD, JNJ, META) — adding a 4th concentrates the short book. R/R at current price 1.26:1 (entry $392.51 to $409.28 target, stop $379) fails the 2:1 minimum. Hourly OBV bearish divergence is the strongest cross-confirmed technical read (4 of 5 agents independently flagged). [source: runs/20260505_160654/decisions.json, trade_ledger.json per_ticker_history[TSLA]=[]]

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
| Allowed actions | hold / short only (no new long per portfolio state) |

**Why hold?** Price at $389.37, 7th consecutive run inside the $387–$399 resistance cluster. Head Trader confidence 32, below the 40 capital-deployment threshold. Vote tally: 4 neutral (swing_trend_momentum 30, swing_breakout 20, swing_catalyst_news 52, swing_macro_context 38), 1 bearish (swing_mean_reversion 42), 0 bullish. Short fade (entry $391, target $381.76, stop $404) delivers only 0.71:1 R/R — fails the 2:1 minimum from the short side as well. Market at S&P/Nasdaq ATH as of May 5. Book tilt: 4 net short (AMD stopped today — now JNJ, META open + AMD/GOOG closures), 2 net long (BAC, AAPL) + WDC new long; adding a 5th short into record-high market with concentrated short-book is imprudent. Bearish OBV divergence confirmed by 4/5 agents but divergence alone without level break is not a short trigger. [source: runs/20260506_160353/decisions.json, trade_ledger.json per_ticker_history[TSLA]=[]]

---

## Closed positions

None. No fills ever executed for TSLA.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades executed | 0 |
| trade_ledger.json rows (TSLA) | 0 |
| Model runs analyzed | 7 |
| Unexecuted shorts recommended | 1 (Apr 15, earnings risk) |
| Holds issued | 6 (Apr 11, Apr 17, May 1, May 4, May 5, May 6) |
| Realized P&L | $0 |
| Unrealized P&L | $0 |

## Last updated

2026-05-06. Sourced from `trade_ledger.json per_ticker_history[TSLA]` (0 rows, run 20260506_160353) + decisions.json from runs swing_20260411_211655, 20260415_093758, 20260417_233350, 20260501_160246, 20260504_161542, 20260505_160654, 20260506_160353. Supersedes 2026-05-05 entry — adds 7th consecutive hold decision.
