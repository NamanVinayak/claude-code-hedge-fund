---
name: UNH technicals
last_updated: 2026-05-05
last_run_id: 20260505_194525
target_words: 350
stale_after_days: 7
word_count: 390
summary: Runaway uptrend — fourth consecutive no-trade run — ADX 86.04, RSI 94.52, z-score 2.04, price $370.75; buyer volume 0.54x average (fatigue visible); hourly distribution in progress; wait for pullback to $348-355 10-EMA zone
---

# UNH — Technicals

## TL;DR

As of May 5, 2026 (fourth consecutive no-trade run), UNH remains in a runaway uptrend at statistical extremes. ADX 86.04, RSI-14 94.52, z-score 2.04, price $370.75 — essentially flat vs the May 4 close ($370.12). The parabola is stalling, not extending. Hourly internals confirm intraday distribution: hourly -DI (29.64) > +DI (10.08), MACD histogram -2.18, OBV trending down. No actionable entry exists at current price. Wait for a pullback to the $348–355 10-EMA zone. (Source: swing_head_trader signal, signals_combined.json, run 20260505_194525.)

**Prior setup archived.** May 4 had RSI-14 94.45, z-score 2.12; May 5 shows RSI 94.52 (essentially unchanged), z-score 2.04 (fractionally eased). Volume at 0.54x 20-day average fails every entry confirmation threshold. Momentum is stalling, not reversing. No-trade verdict is unchanged for the fourth consecutive run.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 86.04, +DI >> -DI | RSI-14 94.52, z-score 2.04, price 22.59% above 50-SMA | ROC-21d +33.72%; volume 0.54x average — buyer fatigue; no reversal candle |
| Hourly | Uptrend intact but distribution underway | MACD histogram -2.18 (bearish), hourly -DI (29.64) > +DI (10.08), OBV trending down | Intraday sellers in control; hourly RSI 36.02 approaching oversold |

EMA stack (daily): 10 EMA $358.02 > 21 EMA $338.88 > 50 EMA $317. Price at $370.75 is 3.56% above the 10-EMA. (Source: swing_trend_momentum, signals_combined.json, run 20260505_194525.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $348–355 | swing_head_trader; swing_trend_momentum, run 20260505_194525 |
| Long target (from EMA pullback) | $390 | swing_trend_momentum, run 20260505_194525 |
| Mean-reversion fade entry | $363–365 on confirmed bearish reversal candle | swing_mean_reversion, run 20260505_194525 |
| Mean-reversion target | $340 (20-EMA) | swing_mean_reversion, run 20260505_194525 |
| Mean-reversion stop | $374.50 (above prior high) | swing_mean_reversion, run 20260505_194525 |
| Price at analysis (May 5) | $370.75 | signals_combined.json, run 20260505_194525 |

## Setup type

**No setup — no-trade zone (fourth consecutive run).** RSI remains near the 94.52 extreme (up fractionally from May 4's 94.45); volume at 0.54x average signals buyer fatigue; hourly internals (MACD -2.18, -DI > +DI, OBV down, RSI 36.02) signal intraday distribution. The only conditional trade is a mean-reversion fade (swing_mean_reversion, 55% confidence): entry on a daily bearish reversal candle in the $363–365 zone, stop $374.50, target $340 — but ADX at 86.04 (top 1% of all readings) and absence of a confirmed daily reversal candle disqualify execution. All five swing agents declined entry. (Source: swing_head_trader signal, decisions.json, run 20260505_194525.)
