---
name: UNH technicals
last_updated: 2026-05-06
last_run_id: 20260506_194605
target_words: 350
stale_after_days: 7
word_count: 378
summary: Runaway uptrend — fifth consecutive no-trade run — ADX 86.49, RSI 85.45, z-score 1.74, price $363.87 (down from $370.75); momentum decelerating; hourly distribution persisting; wait for pullback to $348-355 10-EMA zone
---

# UNH — Technicals

## TL;DR

As of May 6, 2026 (fifth consecutive no-trade run), UNH remains in a runaway uptrend but its momentum indicators are easing off prior extremes. Price at $363.87 (-$6.88 from the May 5 close of $370.75). RSI-14 has pulled back from 94.52 to 85.45; z-score eased from 2.04 to 1.74 (now below the +2 extreme threshold). ADX held essentially flat at 86.49 (was 86.04). Hourly internals continue to signal distribution: hourly -DI (25.84) > +DI (13.76), MACD histogram -1.348, OBV trending down. No actionable entry exists. Wait for a pullback to the $348–359 10-EMA zone. (Source: swing_head_trader signal, decisions.json, signals_combined.json, run 20260506_194605.)

**Prior setup evolution.** May 5 had RSI 94.52, z-score 2.04. May 6 shows RSI 85.45 (eased ~9 points), z-score 1.74 (below the 2.0 extreme threshold for the first time since late April). Daily MACD histogram thin at +1.655 — not expanding. The parabola is softening, not reversing; still no reversal candle. Volume ratio 0.78x is below the 1.5x minimum for any entry confirmation.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 86.49, +DI 41.36 far exceeds -DI 6.95 | RSI-14 85.45, z-score 1.74, price 19.65% above 50-SMA | ROC-5d -0.79 (negative); ROC-21d +29.33%; volume 0.78x — sub-threshold; no reversal candle |
| Hourly | Uptrend intact but distribution underway | MACD histogram -1.348 (bearish), hourly -DI (25.84) > +DI (13.76), OBV trending down | Hourly confirms intraday sellers in control; volume bias down |

EMA stack (daily): 10 EMA $359.08 > 21 EMA $341.15 > 50 EMA $319.25. Price at $363.87 is 1.3% above the 10-EMA. (Source: swing_trend_momentum, signals_combined.json, run 20260506_194605.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $348–359 | swing_head_trader; swing_trend_momentum, run 20260506_194605 |
| Long target (from EMA pullback) | $390 | swing_trend_momentum, run 20260506_194605 |
| Mean-reversion fade entry | $368–370 on confirmed bearish reversal candle | swing_mean_reversion, run 20260506_194605 |
| Mean-reversion target | $343 (20-EMA zone) | swing_mean_reversion, run 20260506_194605 |
| Mean-reversion stop | $374.50 (above prior high) | swing_mean_reversion, run 20260506_194605 |
| Price at analysis (May 6) | $363.87 | signals_combined.json, run 20260506_194605 |

## Setup type

**No setup — no-trade zone (fifth consecutive run).** RSI pulled back from the 94.52 prior extreme to 85.45 but remains deeply overbought; z-score 1.74 (eased below +2 but still in the 96th percentile); volume 0.78x fails every entry threshold; 5-day ROC turned negative (-0.79). Hourly distribution is intact (MACD histogram -1.348, -DI > +DI, OBV down). The only conditional trade remains the mean-reversion fade (swing_mean_reversion, 52% confidence): entry on a daily bearish reversal candle in the $368–370 zone, stop $374.50, target $343 — but ADX at 86.49 (extreme trend regime) and the AMZN/NVDA fade lessons (both lost in high-ADX regimes) disqualify execution. 4/5 agents declined entry; only mean-reversion voted bearish and its own reasoning caps confidence at 52 citing ADX regime risk. (Source: swing_head_trader signal, decisions.json, run 20260506_194605.)
