---
name: UNH technicals
last_updated: 2026-05-01
last_run_id: 20260501_194523
target_words: 350
stale_after_days: 7
word_count: 348
summary: Runaway uptrend at new statistical extremes — ADX 84.15, RSI 97.45, z-score 2.34; no-trade zone intact; wait for pullback to $350-358 10-EMA zone
---

# UNH — Technicals

## TL;DR

As of the May 1, 2026 run, UNH remains in a runaway uptrend with ADX 84.15 — extreme trend territory — but has become even more overextended than the prior run: RSI-14 at 97.45 (up from 94.3), RSI-7 at 98.07, price 23.85% above the 50-SMA, z-score 2.34. No actionable entry exists at current price ($370.48). The no-trade zone is confirmed for the second consecutive run. Wait for a pullback to the $350–358 10-EMA zone. The 10-EMA has risen to $352 but price remains ~$18 above it. (Source: swing_head_trader signal, signals_combined.json, run 20260501_194523.)

**Prior setup archived.** The Apr 30 parabolic extension setup (RSI 94.3, z-score 2.54) was the prior state. RSI has climbed further to 97.45; z-score has eased marginally to 2.34. The no-trade verdict is unchanged.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 84.15, +DI 46.67 vs -DI 4.12 | Historically overbought — RSI-14 97.45, RSI-7 98.07, z-score 2.34, pct-b 0.869 | Runaway trend; ROC-21d +36.92%; no reversal candle yet |
| Hourly | Uptrend intact but losing momentum | MACD histogram -1.01 (negative), ROC mixed, hourly +DI/-DI nearly equal (19.65/19.03) | Early intraday momentum fade; hourly RSI 56.41 (not overbought — divergence from daily) |

EMA stack (daily): 10 EMA $352.17 > 21 EMA $332.39 > 50 EMA $299 — textbook bullish alignment. Price at $370.48 is 5.2% above the 10-EMA and 11.5% above the 21-EMA. (Source: swing_trend_momentum signal, signals_combined.json, run 20260501_194523.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $350–358 | swing_head_trader; swing_trend_momentum, run 20260501_194523 |
| Upside target (if trend resumes from EMA pullback) | $403.55 (Fib 1.272 extension) | swing_trend_momentum, run 20260501_194523 |
| Mean-reversion fade entry | $368 on confirmed bearish reversal candle below prior session low | swing_mean_reversion, run 20260501_194523 |
| Mean-reversion target | $352 (10-EMA) | swing_mean_reversion, run 20260501_194523 |
| Mean-reversion stop | $373.50 (above recent high $371.99) | swing_mean_reversion, run 20260501_194523 |
| Bollinger upper | $385.50 | swing_macro_context, run 20260501_194523 |
| Price at analysis (May 1) | $370.48 | signals_combined.json, run 20260501_194523 |

## Setup type

**No setup — no-trade zone (second consecutive run).** UNH is in a parabolic extension, not a consolidation or breakout pattern. The only conditional setup is a mean-reversion fade (swing_mean_reversion, 42% confidence): entry on a confirmed bearish reversal candle below $368, stop $373.50, target $352 — R/R ~2.9:1, but confidence is below the 40% floor for a swing trade when ADX=84 and no reversal candle exists. All five swing agents declined entry. The flat-top Apr 30 session on 0.74x volume is the first hint of exhaustion but is not yet a confirmed reversal. (Source: swing_head_trader signal, decisions.json, run 20260501_194523.)
