---
name: AAPL technicals
last_updated: 2026-05-05
last_run_id: 20260505_144544
target_words: 350
stale_after_days: 7
word_count: 348
summary: Post-breakout consolidation — price $276.83 daily / $281.68 hourly; ADX 22.55 (rising from 19.92, approaching 25 threshold); hourly OBV divergence RESOLVED (was bearish, now uptrend no divergence); z-score improved 2.25 → 1.77; hold position, no add
---

# AAPL — Technicals

## TL;DR

As of run 20260505_144544, AAPL is in post-breakout consolidation mode with the existing 2-share long position (Trade ID 114, entry fill $277.27, stop $269.50). Daily ADX has improved to 22.55 (from 19.92 on May 4), continuing its upward trajectory toward the 25 confirmation threshold. Hourly OBV bearish divergence that was flagged in the prior run (20260504_144833) has now **resolved** — OBV trend is up with no divergence from price. Daily z-score improved from 2.25 to 1.77 — less extended. Price pulled back to $276.83 daily close (hourly $281.68). Hourly volume 0.38x — quiet consolidation. Hold position. No new entries. (Source: swing_trend_momentum, swing_breakout, swing_macro_context, swing_head_trader signals, run 20260505_144544.)

## Multi-timeframe state

| timeframe | trend | momentum | note |
|---|---|---|---|
| Daily | Developing trend (ADX 22.55, rising: 16.83 → 19.92 → 22.55) | Bullish — 5d ROC +3.45%, 21d ROC +8.17%, RSI 65.75, MACD hist +0.8836 | EMA 10 (272.21) > 21 (267.99) > 50 (264.08) aligned up; Plus DI 37.96 >> Minus DI 17.32; bullish RSI divergence on daily |
| Hourly | Below 25 threshold | Weakening volume — rel-vol 0.38x, hourly BB width 0.0775 (mild re-squeeze) | RSI elevated, OBV uptrend confirmed (prior bearish divergence resolved); Bollinger %B 0.897 (approaching upper band) |

Prior run (May 4, 20260504_144833): ADX 19.92, hourly OBV in downtrend diverging from price. This run: ADX improved to 22.55 (+2.63), hourly OBV divergence fully resolved — a meaningful positive development. BB width daily 0.1046 (still expanding from squeeze). Hourly BB width 0.0775 — mild re-squeeze as price digests the $287 spike, could precede a secondary push.

## Key levels

| level | value | source |
|---|---|---|
| Extended target — measured move (Fib ext 1.618) | $296.77 | swing_breakout signal, 20260505_144544 |
| Primary target — macro-adjusted | $291.00 | decisions.json, 20260505_144544 |
| Partial profit level | $285.50 | swing_head_trader signal, 20260505_144544 |
| Current position entry (filled) | $277.27 | trade_ledger.json id 114 |
| Breakout level / new support | $276.11 | swing_breakout signal, prior runs (11 tests, broken Apr 30) |
| Hourly volume-confirmed support | $274.86 | swing_macro_context signal, 20260505_144544 (15 tests) |
| Stop loss (existing position) | $269.50 | trade_ledger.json id 114 |
| Base pivot low (21 tests) | $255.45 | swing_breakout signal, prior runs |

## Setup type

**Post-earnings breakout continuation — consolidation / re-squeeze phase.** The $276.11 breakout is confirmed (2.08x Apr 30, 1.74x May 1). Hourly OBV divergence from prior run has resolved — bullish confirmation. ADX trajectory (16.83 → 19.92 → 22.55) is constructive; a cross of 25 would fully confirm the trend. Hourly BB re-squeeze (0.0775) suggests a secondary push toward $285–$291 is possible. Position held; no new entries permitted (stacking blocked, R/R at current price ~1.4:1 fails 2:1 minimum). Hold targets: $285.50 partial / $291 primary / $296.77 extended. Stop $269.50 intact. (Source: decisions.json, swing_breakout, swing_trend_momentum, swing_head_trader signals, run 20260505_144544.)
