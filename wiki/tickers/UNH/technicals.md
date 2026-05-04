---
name: UNH technicals
last_updated: 2026-05-04
last_run_id: 20260504_194523
target_words: 350
stale_after_days: 7
word_count: 387
summary: Runaway uptrend still in no-trade zone — ADX 85.61, RSI 94.45, z-score 2.12, price $370.12; third consecutive run at statistical extremes; wait for pullback to $348-355 10-EMA zone
---

# UNH — Technicals

## TL;DR

As of May 4, 2026, UNH remains in a runaway uptrend for the third consecutive run. ADX 85.61, RSI-14 94.45, z-score 2.12, price 22.61% above the 50-SMA. Price at $370.12 is flat vs the May 1 close ($370.48) — the parabola is stalling, not extending. No actionable entry exists at current price. Wait for a pullback to the $348–355 10-EMA zone. (Source: swing_head_trader signal, signals_combined.json, run 20260504_194523.)

**Prior setup archived.** May 1 had RSI-14 97.45 and z-score 2.34; both have eased (RSI now 94.45, z-score 2.12), consistent with stalling momentum at the highs. No-trade verdict is unchanged.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 85.61, +DI >> -DI | RSI-14 94.45, RSI-7 88.85, z-score 2.12, price 22.61% above 50-SMA | ROC-21d +34.6%; volume 0.54x average — buyer fatigue visible |
| Hourly | Uptrend intact but momentum rolling | MACD histogram -1.36, hourly -DI (26.15) > +DI (19.16), OBV trending down | Intraday distribution in progress |

EMA stack (daily): 10 EMA $355.2 > 21 EMA $335.7 > 50 EMA $315.3. Price at $370.12 is 3.83% above the 10-EMA. (Source: swing_trend_momentum, signals_combined.json, run 20260504_194523.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $348–355 | swing_head_trader; swing_trend_momentum, run 20260504_194523 |
| Long target (from EMA pullback) | $390 | swing_trend_momentum, run 20260504_194523 |
| Mean-reversion fade entry | $370 on confirmed bearish reversal candle | swing_mean_reversion, run 20260504_194523 |
| Mean-reversion target | $352 (10-EMA) | swing_mean_reversion, run 20260504_194523 |
| Mean-reversion stop | $374.50 (above recent high $372.90) | swing_mean_reversion, run 20260504_194523 |
| Price at analysis (May 4) | $370.12 | signals_combined.json, run 20260504_194523 |

## Setup type

**No setup — no-trade zone (third consecutive run).** RSI has eased from 97.45 peak; volume at 0.54x average signals buyer fatigue; hourly internals (MACD -1.36, -DI > +DI, OBV down) signal intraday distribution. The only conditional trade is a mean-reversion fade (swing_mean_reversion, 52% confidence): entry on a daily bearish reversal candle below $370, stop $374.50, target $352 — but ADX at 85.61 (top 1% of readings) and absence of a confirmed reversal candle on the daily chart disqualify execution. All five swing agents declined entry. (Source: swing_head_trader signal, decisions.json, run 20260504_194523.)
