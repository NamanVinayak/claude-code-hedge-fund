---
name: NVDA technicals
last_updated: 2026-04-29
last_run_id: sanity_20260429_031705
target_words: 350
stale_after_days: 7
word_count: 368
summary: Strong trend (ADX 49) with full EMA alignment, but deeply overbought daily; hourly shows early deceleration — wait for EMA-10 pullback.
---

# NVDA — Technicals

## TL;DR

As of 2026-04-29 (price ~$213.17), NVDA is in one of the strongest trends in the market — ADX 49.47, full daily EMA alignment, 21-day ROC +27%. The move is extended: RSI 81.67, z-score 2.39, stochastic 94. Hourly timeframe shows early deceleration (STC 1.56 oversold, supertrend bearish, OBV trend down). Do not enter at market. The constructive pullback zone is $204–$208.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 49.47, full EMA stack) | Overbought (RSI 81.67, stoch 94) | Squeeze fired bullish breakout; MACD +2.29 |
| Hourly | Bearish supertrend (218.17 vs ~213) | Oversold STC (1.56) | OBV trend down, volume 0.51x avg; early exhaustion |

**EMA stack (daily, 2026-04-29):** EMA-10: $204.03 / EMA-21: $196.30 / EMA-50: $189.37 — all perfectly fanned bullish. Price at $213.17 is 4.5% above EMA-10 and 8.6% above EMA-21 — extended for fresh entry.

**Trend indicators:** ADX-14 = 49.47 (+DI 40.07, -DI 4.01). Supertrend bullish at $194.41 (daily). Squeeze momentum: squeeze fired (squeeze_off: true), histogram positive but not increasing.

**Momentum:** MACD line 8.04 vs signal 5.75, histogram +2.29. ROC: 5d +6.65%, 10d +8.48%, 21d +27.25%. 52-week high of $216.83 hit on 2026-04-28 (first record since Oct 2025).

**Mean-reversion stress:** Bollinger %B = 0.88 (near upper band 219.15). Z-score vs 50-SMA = 2.39. RSI-14 = 81.67, RSI-21 = 83.39, Stochastic K/D = 94/93, Williams %R = -10.11. Multiple independent agents flagged "extreme overbought."

Source: sanity_20260429_031705, swing_trend_momentum signal; validation_20260427_113014, swing_mean_reversion signal.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance | $216.83 (52-week high) | web_research, Apr 28 2026 |
| Entry zone (tight) | $207–$208.20 (hourly support) | Head Trader synthesis, sanity_20260429_031705 |
| Entry zone (wide) | $204 (EMA-10) | swing_trend_momentum, sanity_20260429_031705 |
| Stop (tight entry) | $207.00 (below hourly support invalidation) | PM decision, sanity_20260429_031705 |
| Stop (wide entry) | $194.50 (below EMA-21) | swing_trend_momentum signal |
| Target | $231.00 (Fibonacci 1.272 extension) | Head Trader, macro_context, trend_momentum |
| Invalidation (bull thesis) | Close below EMA-21 ($196) on volume | thesis assessment |

## Setup type

**Hold existing position + conditional pullback buy.** As of 2026-04-29, we hold 6 shares at $197.20 cost basis. PM decision (sanity_20260429_031705): hold with stop $207, target $231. New entry not permitted (above $211 no-chase zone; buy blocked by allowed_actions given existing position). Reentry eligible only if price pulls to $204–$208 zone.

## Last updated

2026-04-29 — source: sanity_20260429_031705 (swing_trend_momentum, swing_macro_context, swing_mean_reversion, swing_head_trader signals; risk_management_agent).
