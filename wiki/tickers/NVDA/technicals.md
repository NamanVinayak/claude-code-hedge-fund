---
name: NVDA technicals
last_updated: 2026-05-01
last_run_id: 20260501_124529
target_words: 350
stale_after_days: 7
word_count: 341
summary: Breakdown confirmed — price collapsed 8% to $199.57; hourly -DI 38.45 >> +DI 11.92; all positions stopped out; watch for reversal candle at 38.2% Fib / EMA-21 confluence $196.75–$197.67 before re-entry.
---

# NVDA — Technicals

## TL;DR

As of 2026-05-01 (run 20260501_124529, price ~$199.57), NVDA has broken down 8% from the $216.83 swing high. The $208.20 support zone — previously the hard invalidation level — was breached on 1.52x average volume. All NVDA positions are now closed (both stops hit at $205.30 on 2026-04-30; portfolio shows 0 long shares). The daily trend structure remains intact (ADX 55.96, full EMA stack bullish), but the hourly timeframe is actively bearish. No new entry until a confirmed reversal candle appears at the 38.2% Fib / EMA-21 confluence ($196.75–$197.67). Decision: HOLD, conf 35.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 55.96, full EMA stack) | Normalizing (RSI-14 59.74, z-score ~1.06) | MACD histogram +0.73; 21d ROC +14.43%; 5d ROC -0.04% |
| Hourly | Bearish (-DI 38.45 >> +DI 11.92, MACD -1.95) | Deeply oversold (RSI-21 23.58) | OBV diverging bullish — accumulation signal; no reversal candle yet |

**EMA stack (daily, 2026-05-01):** EMA-10: $203.99 / EMA-21: $197.67 / EMA-50: $190.52 / EMA-200: $177.38 — all fanned bullish. Price at $199.57 is below EMA-10, just above EMA-21.

**Trend indicators:** ADX-14 = 55.96 (+DI 29.83, -DI 14.49). SuperTrend bullish on daily. Prior squeeze fired and expanded bearishly on hourly.

**Mean-reversion stress:** Bollinger %B = 0.57 (daily, near midband). Z-score vs 50-SMA = 1.06. Daily RSI-14 = 59.74, RSI-21 = 67.88 — healthy, not stretched. Hourly %B = 0.17 (near lower band). Hourly RSI-21 = 23.58 (deeply oversold). OBV trending up while price falls — bullish divergence.

Sources: run 20260501_124529 — swing_trend_momentum, swing_mean_reversion, swing_breakout, swing_catalyst_news, swing_macro_context, swing_head_trader signals; decisions.json; risk_management_agent.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (prior high) | $216.83 (52-week high) | web_research/NVDA.json, 20260501_124529 |
| Resistance (next) | $214.73 (hourly pivot) | swing_breakout signal, 20260501_124529 |
| Key failed support | $208.20 (now resistance; 15 tests) | swing_head_trader synthesis, 20260501_124529 |
| Current price | $199.57 | decisions.json, 20260501_124529 |
| Support (hourly) | $199.00 (18 tests) | swing_macro_context signal, 20260501_124529 |
| Target entry zone | $197.50–$199.50 | swing_head_trader synthesis, 20260501_124529 |
| Fib 38.2% / EMA-21 confluence | $196.75–$197.67 | swing_trend_momentum, 20260501_124529 |
| Stop (conditional) | $194.00 | swing_head_trader synthesis, 20260501_124529 |
| Target (conditional) | $212.25 | decisions.json, 20260501_124529 |
| Fib 50% / EMA-50 | $190.52 | swing_trend_momentum, 20260501_124529 |

## Setup type

**Watch / No position.** Both open positions (67 shares @ $209.25 and 3 shares @ $209.50) were stopped out at $205.30 on 2026-04-30. Price has broken below $208.20 invalidation level on elevated volume (1.52x avg). Entry requires: (1) confirmed hourly reversal candle (hammer, bullish engulfing, or morning star) at $196.75–$199.50 zone, (2) hourly MACD histogram turning positive. If triggered: entry $197.50–$199.50, stop $194.00, target $212.25, R/R 2.67:1, timeframe 5–12 trading days. Hard exit deadline ~May 17 (3-day pre-earnings blackout before May 20 NVDA earnings).

## Last updated

2026-05-01 — source: 20260501_124529 (all five swing strategy agents, swing_head_trader, PM decisions.json, risk_management_agent). Both positions stopped out; noted in trades.md and recent.md.
