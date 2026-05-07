---
name: NVDA technicals
last_updated: 2026-05-07
last_run_id: 20260507_123732
target_words: 350
stale_after_days: 7
word_count: 348
summary: Confirmed breakout — price surged from $196.50 to $207.83 (+4.64%) on May 6; both entry gates fired (hourly MACD histogram +0.9366, confirmed bullish engulfing); ADX 51.68 strong uptrend; daily OBV bearish divergence persists; HOLD decision (allowed_actions blocks buy); next resistance $208.20 → $214.73 → $216.83; hard exit May 17.
---

# NVDA — Technicals

## TL;DR

As of 2026-05-07 (run 20260507_123732, price $207.83), the 4-day consolidation at the EMA-21/Fib 38.2% zone has resolved bullishly. Both wiki-defined entry gates fired simultaneously for the first time across five consecutive runs: (1) hourly MACD histogram turned positive (+0.9366), and (2) confirmed bullish engulfing candle above $194.74. Price broke through $200.24 (17-test hourly resistance) and $203.00 (7-test hourly resistance) closing at $207.83 (+4.64%). Decision: HOLD — allowed_actions blocks a new buy (current position state), conf 60. Daily OBV bearish divergence and sub-threshold volume (1.26x vs 1.5x required) are the primary cautions. Hard exit deadline ~May 17 (3-day pre-earnings blackout before NVDA Q1 FY2027 ~May 20).

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Bullish (ADX 51.68, +DI 24.25 > -DI 17.23, full EMA stack) | Re-accelerating (RSI-14 57.92, z-score 1.61) | MACD histogram -0.7836 (decelerating negative); 21d ROC +16.69% |
| Hourly | Strongly bullish (ADX 37.6, +DI 36.55 >> -DI 11.21) | Expanding positive (MACD histogram +0.9366) | Hourly OBV trending up, no divergence; volume 1.26x (below 1.5x gate) |

**EMA stack (daily, 2026-05-07):** EMA-10: $202.36 / EMA-21: $198.61 / EMA-50: $191.99 — all fanned bullish. Price at $207.83 is above all EMAs.

**Trend indicators:** ADX-14 = 51.68 (+DI 24.25, -DI 17.23). Daily MACD histogram -0.7836 (negative but decelerating). Hourly MACD histogram +0.9366 (crossed above zero — gate 1 fired). Hourly RSI-21 healthy, no extreme.

**Mean-reversion stress:** Bollinger %B = 0.73 (daily). Z-score vs 50-SMA = 1.61 (elevated but not extreme). RSI-14 57.92 (neutral-bullish — not overbought). OBV: daily trending DOWN (divergence from price, distribution warning). Hourly OBV trending UP with no divergence.

Sources: run 20260507_123732 — swing_trend_momentum, swing_mean_reversion, swing_breakout, swing_catalyst_news, swing_macro_context, swing_head_trader signals; decisions.json; risk_management_agent.

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (prior high / 52-week high) | $216.83 | swing_head_trader synthesis, 20260507_123732 |
| Resistance (Fib ext 1.618 / hourly cluster) | $214.73 | swing_breakout, 20260507_123732 |
| Resistance (Fib ext 1.272) | $211.94 | swing_breakout, 20260507_123732 |
| Resistance (broken support re-test) | $208.20 | swing_head_trader, 20260507_123732 |
| Current price | $207.83 | decisions.json, 20260507_123732 |
| Hourly support (7 tests, volume-confirmed) | $203.00 | swing_breakout, 20260507_123732 |
| Hourly support (23 tests, volume-confirmed) | $198.70 | swing_head_trader, 20260507_123732 |
| EMA-21 | $198.61 | swing_trend_momentum, 20260507_123732 |
| Hourly support / prior consolidation floor | $194.74 | swing_breakout, 20260507_123732 |
| Conditional stop (if new entry) | $198.50 | swing_head_trader, 20260507_123732 |
| Conditional target | $216.00 | swing_head_trader, 20260507_123732 |

## Setup type

**Watch / No position (gates fired, buy blocked).** Prior trade (16 shares @ $209.25, trade id 112, Turso) stopped out at $205.30 on 2026-04-30 (-$63.20). Both entry gates fired May 6 simultaneously — the first time across five consecutive runs — but allowed_actions blocks a new buy. If buy were permitted: entry zone $204.50–$207.00 (modest pullback preferred), stop $198.50, target $216.00, R/R ~2.2:1–2.8:1. Key risk: volume sub-threshold (1.26x vs 1.5x) and daily OBV bearish divergence. Hard exit deadline May 17.

## Last updated

2026-05-07 — source: 20260507_123732 (all five swing strategy agents, swing_head_trader, PM decisions.json, risk_management_agent). Prior setup type (continuation pullback deepened, $196.50) superseded by confirmed breakout close at $207.83. Both entry gates fired. Prior setup note moved to recent.md — signal flip: HOLD below zone → HOLD above zone after confirmed breakout.
