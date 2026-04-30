---
name: NVDA technicals
last_updated: 2026-04-30
last_run_id: 20260430_124034
target_words: 350
stale_after_days: 7
word_count: 359
summary: Pullback-buy confirmed — ADX 54.67, full EMA alignment, 3 shares at $209.25, target $223.25, stop $205.30, R/R 3.5:1.
---

# NVDA — Technicals

## TL;DR

As of 2026-04-30 (price ~$209.25), NVDA is executing a pullback-buy in one of the strongest market trends. ADX 54.67, full daily EMA alignment. Price pulled back 3.5% from the $216.83 52-week high to hourly Fib 38.2% (~$209.70) with volume-confirmed support at $208.20 (15 tests). PM decision run 20260430_124034: BUY 3 shares at $209.25, stop $205.30 (Fib 61.8%), target $223.25, R/R 3.5:1, confidence 74. Hard exit ~May 17 (pre-earnings blackout).

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 54.67, full EMA stack) | Extended (RSI 74.76, z-score 1.92) | MACD +1.80; ROC 21d +26.69% |
| Hourly | Consolidating (EMAs uptrend) | Neutral (RSI 51.94) | OBV down, volume 0.56x avg — normal digestion |

**EMA stack (daily):** EMA-10: $204.98 / EMA-21: $197.47 / EMA-50: $190.15 — all fanned bullish. Price 2.1% above EMA-10.

**Momentum:** MACD histogram +1.80. ROC: 5d +3.33%, 10d +5.22%, 21d +26.69%. Squeeze fired prior run (squeeze_off: true) — no new squeeze forming.

**Mean-reversion stress:** Bollinger %B = 0.7824 (inside bands). Z-score vs 50-SMA = 1.92. RSI-14 = 74.76, RSI-21 = 81.52. Hourly RSI-21 = 51.94 — neutral.

Source: run 20260430_124034, swing_trend_momentum, swing_mean_reversion, swing_head_trader.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (next) | $214.73 (hourly, 7 tests) | swing_breakout, 20260430_060402 |
| Resistance (major) | $216.83 (52-week high, 2026-04-28) | web_research/NVDA.json |
| Entry | $209.25 | decisions.json, 20260430_124034 |
| Support (hourly) | $208.20 (15 tests, volume-confirmed) | swing_head_trader, 20260430_060402 |
| Stop | $205.30 (Fib 61.8%) | swing_head_trader, 20260430_124034 |
| Target (primary) | $223.25 (trend+MR median) | decisions.json, 20260430_124034 |
| Target (extended) | $231.13 (Fib 1.272) | swing_macro_context signal |
| Invalidation | Close below $208.20 before new high | swing_head_trader |

## Setup type

**Pullback buy in strong trend.** 3 shares at $209.25 (run 20260430_124034). 4/5 agents bullish — swing_breakout neutral (prior squeeze already fired), not bearish. R/R 3.5:1. Position $627.75 within $708.36 risk cap (14.2% of $5K, 38.3% vol). Re-evaluate at $216.83: expand to $231 target on volume confirmation.

## Last updated

2026-04-30 — run 20260430_124034 (decisions.json, signals_combined.json, risk_management_agent).
