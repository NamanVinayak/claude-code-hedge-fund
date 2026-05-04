---
name: JNJ technicals
last_updated: 2026-05-04
last_run_id: 20260504_194523
target_words: 350
stale_after_days: 7
word_count: 410
summary: Confirmed downtrend deepening — ADX 31.07, EMA death stack intact, RSI 34.19 approaching oversold; price $224.07 pressing $223.78 pivot support (4 tests); hourly BB squeeze 0.0313; short id 116 in flight, +$14.85 unrealized
---

# JNJ — Technicals

## TL;DR

As of May 4, 2026, JNJ's confirmed daily downtrend has deepened: price dropped from $229.85 (May 1) to $224.07, now pressing the critical $223.78 pivot support tested 4 times without breaking. Daily RSI at 34.19 is approaching oversold — bounce risk is rising. ADX at 31.07 (up from 30.72) confirms the downtrend is strengthening. Hourly Bollinger width 0.0313 (extreme squeeze) with pct_b 0.076 — a directional resolution is imminent. Active short (id 116, 3 shares entered at $229.06 fill) running with ~$14.85 unrealized gain. Stop $231.50 intact; target $216.53 still ~$7.50 away. (Source: swing_head_trader signal, decisions.json, trade_ledger.json, run 20260504_194523.)

**Prior setup evolution.** May 1 had price $229.85 at 10-EMA resistance, hourly BB width 0.029. Price has since broken below the 10-EMA and dropped $5.78 toward $223.78. Downtrend is working exactly as modeled.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Confirmed downtrend — ADX 31.07, -DI 26.9 > +DI 19.9; all EMAs inverted | MACD -3.24 below signal -2.78; ROC-21d -6.94%; OBV down; volume bias 10d down | RSI-14 34.19 approaching oversold; bounce risk increasing near $223.78 |
| Hourly | Downtrend — EMAs bearish aligned | -DI (32.44) >> +DI (14.83); Bollinger width 0.0313 (extreme squeeze); pct_b 0.076 | Spring-loaded at $223.78 support — imminent directional resolution |

EMA stack (daily): EMA 5 $228.0 < EMA 10 $229.2 < EMA 21 $232.2 < EMA 50 $233.5 — bearish tightening intact. Price $224.07 below all EMA levels. (Source: swing_trend_momentum, signals_combined.json, run 20260504_194523.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Critical pivot support (breakdown trigger) | $223.78 (4 tests) | swing_breakout, run 20260504_194523 |
| Measured-move target | $216.53 | swing_breakout, run 20260504_194523 |
| Active short entry fill | $229.06 (id 116, 3 shares) | trade_ledger.json, run 20260504_194523 |
| Stop loss (active) | $231.50 | decisions.json, run 20260504_194523 |
| Dead-cat bounce resistance | $226–229 | swing_mean_reversion, run 20260504_194523 |
| Price at analysis (May 4) | $224.07 | signals_combined.json, run 20260504_194523 |

## Setup type

**Bearish continuation — holding active short at $223.78 support.** The short (id 116, fill $229.06) is running in-direction. A close below $223.78 on volume >1.5x average confirms the measured-move breakdown to $216.53. Risk: hourly Bollinger squeeze at the lower band and RSI approaching oversold signal a possible dead-cat bounce to $226–229 before continuation. No new entries; hold existing position. (Source: decisions.json; swing_head_trader, run 20260504_194523.)
