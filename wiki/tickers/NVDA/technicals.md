---
name: NVDA technicals
last_updated: 2026-04-30
last_run_id: 20260430_124724
target_words: 350
stale_after_days: 7
word_count: 362
summary: Pullback-buy confirmed — ADX 54.67 strongest trend in run history, price at $209.25/$209.50 near Fib 38.2% with volume-confirmed $208.20 support; RSI elevated but dip buy active.
---

# NVDA — Technicals

## TL;DR

As of 2026-04-30 (price ~$209.25, entry $209.50), NVDA is executing a pullback-buy in one of the strongest trends in the market. ADX 54.67 (highest recorded in this pipeline), full daily EMA alignment confirmed. Price has pulled back 3.5% from the $216.83 52-week high to the hourly Fib 38.2% zone ($209.70) with volume-confirmed support at $208.20 (15 tests). RSI-14 at 74.76 and RSI-21 at 81.52 are elevated but have cooled from the 81.67/83.39 extremes of 2026-04-29. Buy 3 shares at $209.50, stop $205.30 (hourly Fib 61.8%), target $221.89, R/R 2.95:1 (run 20260430_124724).

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 54.67, full EMA stack) | Extended (RSI 74.76, z-score 1.92) | MACD histogram +1.80; ROC 21d +26.69% |
| Hourly | Consolidating (EMAs uptrend) | Neutral (RSI-21 ~51.94) | OBV trend down, volume 0.56x avg; normal post-breakout digestion |

**EMA stack (daily, 2026-04-30):** EMA-10: $204.98 / EMA-21: $197.47 / EMA-50: $190.15 — all fanned bullish. Price at $209.25 is 2.1% above EMA-10, inside the constructive pullback zone.

**Trend indicators:** ADX-14 = 54.67 (+DI 39.03, -DI 4.66). SuperTrend bullish (daily). Prior squeeze fired (squeeze_off: true) — volatility already expanded; no new squeeze forming.

**Momentum:** MACD line above signal, histogram +1.80. ROC: 5d +3.33%, 10d +5.22%, 21d +26.69%. 52-week high $216.83 set on 2026-04-28.

**Mean-reversion stress:** Bollinger %B = 0.7824 (inside bands). Z-score vs 50-SMA = 1.92 (cooled from 2.39). RSI-14 = 74.76, RSI-21 = 81.52. Hourly RSI-21 ≈ 51.94 — neutral, not exhausted.

Sources: run 20260430_124724 — swing_trend_momentum, swing_mean_reversion, swing_catalyst_news, swing_macro_context, swing_head_trader signals; decisions.json; risk_management_agent.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (next) | $214.73 (hourly, 7 tests) | swing_breakout signal, 20260430_124724 |
| Resistance (major) | $216.83 (52-week high) | web_research/NVDA.json, 2026-04-30 |
| Entry | $209.50 | PM decision, 20260430_124724 |
| Support (hourly) | $208.20 (15 tests, volume-confirmed) | swing_head_trader synthesis, 20260430_124724 |
| Stop | $205.30 (hourly Fib 61.8%) | swing_head_trader stop consensus, 20260430_124724 |
| Target | $221.89 (cluster median) | PM decision, 20260430_124724 |
| Target (extended) | $231.13 (daily Fib 1.272 ext) | swing_macro_context signal |
| Invalidation | Close below $208.20 before new high | swing_head_trader synthesis |

## Setup type

**Pullback buy in a strong trend.** 3 shares entered at $209.50 (run 20260430_124724), supplementing the 67-share position from run 20260430_060402. Setup unchanged: post-breakout dip to hourly Fib 38.2% / volume-confirmed $208.20 support. Re-evaluate at $216.83 resistance: clear on expanding volume → activate $231 extension target. Break below $208.20 before new high invalidates thesis.

## Last updated

2026-04-30 — source: 20260430_124724 (swing_trend_momentum, swing_mean_reversion, swing_catalyst_news, swing_macro_context, swing_head_trader signals; PM decisions.json; risk_management_agent). Prior run: 20260430_060402 (unchanged setup, same key levels).
