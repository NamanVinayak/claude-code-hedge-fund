---
name: NVDA technicals
last_updated: 2026-05-04
last_run_id: 20260504_125732
target_words: 350
stale_after_days: 7
word_count: 344
summary: Continuation pullback — price $198.45 testing EMA-21 / Fib 38.2% confluence; hourly -DI 36.05 >> +DI 12.97; no new NVDA positions; same watch-not-act setup; confirmed entry conditions remain unmet.
---

# NVDA — Technicals

## TL;DR

As of 2026-05-04 (run 20260504_125732, price ~$198.45), NVDA continues its pullback from the $216.83 swing high — now down 8.5% in 4 sessions. Price is testing the 38.2% Fib / EMA-21 confluence zone ($196.75–$197.74), unchanged from the prior run's identified re-entry zone. The daily trend structure remains intact (ADX 56.9, full EMA uptrend), but the hourly timeframe is actively bearish. No NVDA position exists. Decision: HOLD, conf 44 (below 50 threshold for action). Entry requires a confirmed hourly reversal candle AND hourly MACD histogram turning positive — neither condition is met.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 56.9, full EMA stack) | Contracting (RSI-14 58.08, z-score 0.94) | MACD histogram slightly negative (-0.11); 5d ROC -4.72%; 21d ROC +12.92% |
| Hourly | Bearish (-DI 36.05 >> +DI 12.97, MACD -1.82) | Deeply oversold (RSI-21 18.82) | No bullish reversal candle confirmed; OBV distributing |

**EMA stack (daily, 2026-05-04):** EMA-10: $202.99 / EMA-21: $197.74 / EMA-50: $190.83 — all fanned bullish. Price at $198.45 is below EMA-10, at EMA-21.

**Trend indicators:** ADX-14 = 56.9 (+DI 29.18, -DI 15.93). SuperTrend bullish on daily. Prior hourly squeeze fired bearishly (MACD histogram -1.82, expansion underway).

**Mean-reversion stress:** Bollinger %B = 0.528 (daily, near midband). Z-score vs 50-SMA = 0.94. Daily RSI-14 = 58.08 — healthy, not stretched. Hourly %B = 0.17 (near lower band). Hourly RSI-21 = 18.82 (deeply oversold — bounce potential but no confirmation signal yet).

Sources: run 20260504_125732 — swing_trend_momentum, swing_mean_reversion, swing_breakout, swing_catalyst_news, swing_macro_context, swing_head_trader signals; decisions.json; risk_management_agent.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (prior high) | $216.83 (52-week high) | web_research/NVDA.json, 20260504_125732 |
| Resistance (broken support) | $208.20 (15+ tests; now overhead) | swing_head_trader synthesis, 20260504_125732 |
| Resistance (hourly pivot) | $203.00 (12 tests, volume-confirmed) | swing_breakout signal, 20260504_125732 |
| Current price | $198.45 | decisions.json, 20260504_125732 |
| Target entry zone | $196.75–$199.50 | swing_head_trader synthesis, 20260504_125732 |
| Fib 38.2% / EMA-21 confluence | $196.75–$197.74 | swing_trend_momentum, 20260504_125732 |
| Stop (conditional) | $194.00 | swing_head_trader synthesis, 20260504_125732 |
| Target (conditional) | $210.50 | swing_head_trader synthesis, 20260504_125732 |
| Fib 50% / EMA-50 | $190.83 | swing_trend_momentum, 20260504_125732 |

## Setup type

**Watch / No position.** Prior trade (16 shares @ $209.25, trade id 112) stopped out at $205.30 on 2026-04-30 (-$63.20). Price has broken below the $208.20 invalidation level and is now at the Fib 38.2% / EMA-21 confluence. Entry requires: (1) confirmed hourly reversal candle (hammer, bullish engulfing) at $196.75–$199.50 zone, (2) hourly MACD histogram turning positive. If triggered: entry $196.75–$199.50, stop $194.00, target $210.50, R/R ~2.6:1, timeframe 5–10 trading days. Hard exit deadline May 17 (3-day pre-earnings blackout before ~May 27 NVDA earnings).

## Last updated

2026-05-04 — source: 20260504_125732 (all five swing strategy agents, swing_head_trader, PM decisions.json, risk_management_agent). No position changes; price slightly lower vs. prior run ($198.45 vs $199.57); all indicator readings updated.
