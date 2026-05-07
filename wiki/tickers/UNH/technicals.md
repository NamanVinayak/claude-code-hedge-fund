---
name: UNH technicals
last_updated: 2026-05-07
last_run_id: 20260507_194523
target_words: 350
stale_after_days: 7
word_count: 388
summary: Runaway uptrend — sixth consecutive no-trade run — ADX 86.26, RSI 85.67, z-score 1.74, price $367.28 (up from $363.87 May 6); momentum fractionally recovering intraday; hourly distribution easing slightly; wait for pullback to $360-365 10-EMA zone
---

# UNH — Technicals

## TL;DR

As of May 7, 2026 (sixth consecutive no-trade run), UNH remains in a runaway uptrend with marginally improved short-term metrics versus May 6. Price at $367.28 (+$3.41 from the May 6 close of $363.87). RSI-14 fractionally higher at 85.67 (was 85.45); z-score unchanged at 1.74 (still below the +2.0 extreme threshold). ADX eased very slightly to 86.26 (was 86.49) — still an extreme regime. Hourly internals show reduced bearish pressure: hourly MACD histogram -0.9259 (was -1.348), hourly -DI 21.45 vs +DI 17.17 (was -DI 25.84 vs +DI 13.76). Volume ratio 0.82x — still below the 1.5x minimum for any entry confirmation. No actionable entry exists. Wait for a pullback to the $360–365 10-EMA zone. (Source: swing_head_trader signal, decisions.json, signals_combined.json, run 20260507_194523.)

**Prior setup evolution.** May 6 had RSI 85.45, price $363.87. May 7 shows RSI 85.67 (negligible uptick), price $367.28 (slight bounce from May 6 dip). Daily MACD histogram +0.8466 — thin and not expanding. Hourly distribution is easing (MACD histogram improved from -1.348 to -0.9259; -DI lead over +DI narrowed) but no reversal candle confirmed. EMA10 now at $360.57 — the wait zone has been updated to $360–365.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 86.26, +DI 39.39 far exceeds -DI 9.19 | RSI-14 85.67, z-score 1.74, price 20.02% above 50-SMA | ROC-5d -0.93 (still negative); ROC-21d +19.35%; volume 0.82x — sub-threshold; no reversal candle |
| Hourly | Uptrend intact, hourly distribution easing | MACD histogram -0.9259 (bearish but less than prior -1.348); hourly -DI 21.45 vs +DI 17.17; hourly RSI 45.87 | Intraday sellers losing some control; still no bullish reversal candle |

EMA stack (daily): 10 EMA $360.57 > 21 EMA $343.53 > 50 EMA $321.13. Price at $367.28 is 1.86% above the 10-EMA — still extended but closer to the entry zone. (Source: swing_trend_momentum, signals_combined.json, run 20260507_194523.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $360–365 | swing_head_trader; swing_trend_momentum, run 20260507_194523 |
| Long target (from EMA pullback) | $395 | swing_trend_momentum, run 20260507_194523 |
| Mean-reversion fade threshold | +2.0 z-score (currently 1.74 — not reached) | swing_mean_reversion, run 20260507_194523 |
| Mean-reversion stop (if fade actioned) | $374.50 above prior high | swing_mean_reversion, run 20260507_194523 |
| Price at analysis (May 7) | $367.28 | signals_combined.json, run 20260507_194523 |

## Setup type

**No setup — no-trade zone (sixth consecutive run).** RSI-14 at 85.67 remains deeply overbought; z-score 1.74 is still in the 96th percentile even though it has held below +2.0 for two consecutive runs; volume 0.82x fails every entry threshold; 5-day ROC negative (-0.93%). Hourly distribution is easing but no reversal signal. The ADX at 86.26 remains one of the highest readings in the portfolio's history, disqualifying any fade short per the lessons database (AMZN -$10.14, GOOG -$6.50, NVDA -$63.20 — all fade failures in ADX 60+ regimes). 5/5 agents unanimously declined entry this run — the first unanimous 5-of-5 neutral since at least May 4. Only conditional long scenario: a pullback to the $360–365 EMA_10 zone with a confirmed bullish reversal candle and volume above the daily average. (Source: swing_head_trader signal, decisions.json, run 20260507_194523.)
