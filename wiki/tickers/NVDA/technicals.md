---
name: NVDA technicals
last_updated: 2026-05-06
last_run_id: 20260506_123913
target_words: 350
stale_after_days: 7
word_count: 352
summary: Continuation pullback deepened — price $196.50 fell below EMA-21 ($197.69) and Fib 38.2% zone; daily ADX 53.63 strong trend intact; hourly MACD histogram -0.7742 (bearish, not bottomed); hourly RSI-21 39.64; 4th consecutive HOLD at this zone.
---

# NVDA — Technicals

## TL;DR

As of 2026-05-06 (run 20260506_123913, price ~$196.50), NVDA has dipped further below the EMA-21 / Fib 38.2% confluence zone ($196.75–$197.80) — now at $196.50, 0.13% below the bottom of the entry zone. AMD Q1 2026 earnings (May 5 AMC) passed without triggering the confirmation signal; price slipped -1% post-AMD print. This is the 4th consecutive HOLD at this zone (runs 20260501, 20260504, 20260505, and now 20260506). The daily trend structure remains intact (ADX 53.63, full EMA uptrend). Hourly MACD histogram is -0.7742 — bearish, though modestly improved from -1.86 on May 5. Decision: HOLD, conf 38 (below 40 threshold). Both entry gates still unmet: (1) confirmed hourly bullish reversal candle at/above $194.74 AND (2) hourly MACD histogram turning positive.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 53.63, full EMA stack) | Decelerating (RSI-14 47.58, z-score 0.75) | MACD histogram -1.197 (bearish); 5d ROC -7.82%; 21d ROC +10.62% |
| Hourly | Bearish (MACD histogram -0.7742, bearish) | Recovering from extreme (RSI-21 39.64) | No bullish reversal candle confirmed; OBV trending down on both timeframes |

**EMA stack (daily, 2026-05-06):** EMA-10: $201.14 / EMA-21: $197.69 / EMA-50: $191.34 — all fanned bullish. Price at $196.50 is below EMA-10 and now also below EMA-21.

**Trend indicators:** ADX-14 = 53.63 (+DI 17.33, -DI 18.73). SuperTrend status unchanged bullish on daily. Hourly MACD histogram -0.7742 (bearish but improved from -1.86 on May 5 — early-stage deceleration of bearish momentum).

**Mean-reversion stress:** Bollinger %B = 0.42 (daily, below mid-band). Z-score vs 50-SMA = 0.75 (healthy, not extreme). Daily RSI-7 = 29.36 (short-term oversold — bounce plausible). Hourly RSI-21 = 39.64. Volume 0.76x relative (below average — declining-volume pullback; no accumulation confirmed).

Sources: run 20260506_123913 — swing_trend_momentum, swing_mean_reversion, swing_breakout, swing_catalyst_news, swing_macro_context, swing_head_trader signals; decisions.json; risk_management_agent.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (prior high) | $216.83 (52-week high) | web_research/NVDA.json, 20260506_123913 |
| Resistance (overhead) | $208.20 (broken support, multiple tests) | swing_head_trader synthesis, 20260506_123913 |
| Resistance (hourly pivot) | $200.24 (21 hourly tests, volume-confirmed) | swing_breakout signal, 20260506_123913 |
| Current price | $196.50 | decisions.json, 20260506_123913 |
| Fib 38.2% / EMA-21 confluence | $196.75–$197.69 | swing_trend_momentum, 20260506_123913 |
| Hourly support (2 tests) | $194.74 (invalidation floor) | swing_breakout signal, 20260506_123913 |
| Conditional entry | $197.00 (post-confirmation) | swing_head_trader, 20260506_123913 |
| Conditional stop | $193.50 | decisions.json, 20260506_123913 |
| Conditional target | $210.00 | swing_macro_context, 20260506_123913 |
| Fib 50% / next support | $190.55 / EMA-50 $191.34 | swing_trend_momentum, 20260506_123913 |

## Setup type

**Watch / No position.** Prior trade (16 shares @ $209.25, trade id 112, Turso) stopped out at $205.30 on 2026-04-30 (-$63.20). AMD Q1 earnings (May 5 AMC) did not deliver the confirmation trigger — price slipped below the Fib 38.2% zone to $196.50. Entry requires: (1) hourly MACD histogram crosses above 0 AND (2) confirmed bullish reversal candle at/above $194.74. If both fire: entry ~$197.00, stop $193.50, target $210.00, R/R 3.7:1. Invalidation: close below $194.74 → next support $179/$174. Hard exit deadline May 17 (3-day pre-earnings blackout before NVDA Q1 FY2027 ~May 20).

## Last updated

2026-05-06 — source: 20260506_123913 (all five swing strategy agents, swing_head_trader, PM decisions.json, risk_management_agent). Price slipped to $196.50 from $198.48 (May 5); now below EMA-21 ($197.69). AMD earnings passed without triggering confirmation signal. Hourly MACD histogram improved marginally (-1.86→-0.7742) but still negative. Prior setup note moved to recent.md only on direction flip — no flip this run.
