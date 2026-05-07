---
name: AMZN technicals
last_updated: 2026-05-07
last_run_id: 20260507_173424
target_words: 350
stale_after_days: 7
word_count: 356
summary: HOLD — no valid entry; price ~$274.99 daily close; RSI-14 82.43/RSI-21 90.3 deeply overbought; ADX 65.51 extreme uptrend (+DI 36.96 vs -DI 8.26); Z-score 1.93; 10 EMA $265.54 (rising); 5/5 agents unanimous neutral; wait for pullback to $263–$266 or confirmed daily close above $276 on 1.5x+ volume
---

# AMZN — Technicals

## TL;DR

As of run 20260507_173424 (May 7, 2026), price ~$274.99 daily close. RSI-14 82.43, RSI-21 90.3 — deeply overbought. ADX 65.51 with +DI 36.96 vs -DI 8.26 — extreme bullish trend intact. Z-score 1.93 (just below +2σ). Setup type: **HOLD — no valid entry from current levels.** All 5 swing agents returned unanimous neutral. No short without hourly RSI-21 >75 + volume-confirmed rejection at $273-276 (ADX-regime lesson from ID 115 stop-out). No long without pullback to 10 EMA zone $263-266 OR confirmed daily close above $276 on 1.5x+ volume.

*Prior setup (run 20260506_173925, May 6): HOLD — same regime. Price was $273.55 daily close / $278.56 intraday wick (unconfirmed). 10 EMA moved $263.44 → $265.54 (rising). Regime type unchanged.*

---

## Multi-timeframe state

**Daily (primary):** EMA alignment clean bullish — EMA5 $270.93 > EMA10 $265.54 > EMA21 $254.26 > EMA50 $238.71. ADX 65.51 with +DI 36.96 vs -DI 8.26 — extreme trend strength. RSI-14 82.43, RSI-21 90.3 (deeply overbought). Z-score vs 50-SMA: 1.93. Price 20.22% above 50-SMA. Bollinger %B 0.90 (near upper band). MACD histogram positive at +0.99 (line 13.19 > signal 12.21 — momentum accelerating on daily). Volume 0.86x 20-day average — below 1.5x threshold.

**Hourly:** Hourly price ~$271.50, below 24-period EMA $272.64. Hourly MACD histogram -0.609 (negative — short-term bearish pressure). Hourly RSI-21 50.89 (mid-range, NOT at extreme fade threshold). Hourly ADX: -DI 23.85 > +DI 18.36 (mild intraday bearish lean). Hourly OBV trending DOWN. Hourly relative volume near 0.06x — extremely thin. [source: signals_combined.json swing_trend_momentum and swing_breakout, run 20260507_173424]

---

## Key levels

| Level | Value | Source |
|---|---|---|
| Current price | ~$274.99 daily close | Run 20260507_173424 |
| Breakout trigger | Daily close above $276 on 1.5x+ volume | swing_breakout, run 20260507_173424 |
| Breakout long entry | ~$276.50 (if confirmed) | swing_breakout, run 20260507_173424 |
| Long pullback entry zone | $263–$266 (10 EMA zone) | swing_trend_momentum, run 20260507_173424 |
| Breakout measured move target | $296 (range height $21 added to $276) | swing_breakout, run 20260507_173424 |
| Pullback long target | $284.20 (Fib 1.272) | swing_trend_momentum, run 20260507_173424 |
| Pullback long stop | $259.50 | swing_macro_context, run 20260507_173424 |
| Breakout long stop | $268.00 | swing_head_trader, run 20260507_173424 |
| Short re-entry trigger | Hourly RSI-21 >75 + vol rejection at $273–$276 | decisions.json, run 20260507_173424 |

---

## Setup type

**HOLD — no valid entry.** Three potential entry scenarios defined; none active. (A) BREAKOUT LONG — requires confirmed daily close above $276 on 1.5x+ volume; today ~$274.99 with 0.86x volume. May 6 intraday wick to $278.56 was explicitly unconfirmed (0.80x vol, no daily close above $276). (B) PULLBACK LONG — requires retracement to 10 EMA zone $263-266 with RSI cooling below 65; price is 3.56% above 10 EMA ($265.54). (C) SHORT — requires hourly RSI-21 >75 plus volume-confirmed rejection candle at $273-276; current hourly RSI-21 only 50.89 — well below threshold. ADX 65.51 extreme trend: four consecutive stop-outs on mean-reversion fades in ADX 60+ environment (NVDA Apr 30, AMZN May 4, GOOG May 6, AMD May 6) set an elevated confirmation bar. [source: decisions.json, signals_combined.json swing_head_trader, run 20260507_173424]

---

## Indicator snapshot (May 7, 2026)

| Indicator | Value | Interpretation |
|---|---|---|
| ADX | 65.51 | Extreme mature uptrend — fade risk very high |
| +DI / -DI | 36.96 / 8.26 | Bull momentum dominant |
| RSI-14 | 82.43 | Deeply overbought |
| RSI-21 | 90.3 | Extremely overbought |
| Hourly RSI-21 | 50.89 | Mid-range — well below fade threshold (75) |
| Hourly MACD histogram | -0.609 | Short-term bearish pressure |
| Hourly rel-vol | ~0.06x | Near-zero — extremely thin |
| Z-score (50-SMA) | 1.93 | Near +2σ — statistically stretched |
| % above 50-SMA | 20.22% | Extreme extension |
| BB %B (daily) | 0.90 | Near upper band |
| Volume (daily) | 0.86x avg | Below 1.5x breakout threshold |
| EMA10 | $265.54 | Rising — nearest valid pullback support |
