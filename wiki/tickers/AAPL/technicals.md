---
name: AAPL technicals
last_updated: 2026-04-30
last_run_id: 20260430_144524
target_words: 350
stale_after_days: 7
word_count: 342
summary: Squeeze released, price entered $270-282 target zone — ADX 15.78 (weak), no trend confirmation; earnings blackout blocks new entry; post-earnings structure needed
---

# AAPL — Technicals

## TL;DR

As of the April 30 run (20260430_144524), AAPL has entered the $270–282 break-above target zone identified in prior runs but lacks the trend or volume confirmation to act on it. The Bollinger squeeze that was coiling in mid-April has begun releasing (BB width 0.0994 vs. 0.069 on Apr 15), but ADX at 15.78 daily / 14.33 hourly remains well below the 25 threshold. Q2 earnings today creates a 3-day blackout regardless of technical setup. Wait for post-earnings structure.

## Multi-timeframe state

| timeframe | trend | momentum | note |
|---|---|---|---|
| Daily | No trend (ADX 15.78) | Mixed — 5d ROC -1.1%, 21d ROC +9.54% | Squeeze releasing; EMAs fully aligned up |
| Hourly | No trend (ADX 14.33) | Fading — MACD histogram -0.166 | RSI 63.34 healthy but losing steam |

Prior run (Apr 17, 20260417_233350) had ADX 12.5–15.2 with EMAs clustered in a $2 range. Current run shows marginal improvement — ADX 15.78 daily — but still failing the 25 threshold. EMA alignment is clean: EMA10 $268.71 > EMA21 $265.25 > EMA50 $262.54, price above all. The hourly MACD histogram diverging negative (-0.166) from the positive daily (+0.607) is an early warning of short-term exhaustion.

## Key levels

| level | value | source |
|---|---|---|
| Resistance — daily pivot high (11 tests) | $276.11 | signals_combined.json, 20260430_144524 |
| Hourly pivot resistance (27 tests, volume-confirmed) | $273.22 | swing_breakout signal, 20260430_144524 |
| Current price (Apr 29 close) | ~$271 | signals_combined.json, 20260430_144524 |
| Fib 38.2% retracement / 20-SMA cluster | $264.21 / $264.36 | swing_mean_reversion signal, 20260430_144524 |
| Support — daily pivot low (21 tests) | $255.45 | swing_breakout signal, 20260430_144524 |
| Hard invalidation | $255.45 close | decisions.json, 20260430_144524 |

## Setup type

**Squeeze breakout — unconfirmed.** BB width expanded from 0.069 (Apr 15) to 0.0994 (Apr 30) — the squeeze has begun releasing but direction is not confirmed. Volume is disqualifying: daily relative volume 0.73x, hourly 0.32x (both far below the 1.5x required for breakout confirmation). No close above $276.11 has occurred. Measured move if $276.11 breaks with volume: $276.11 + $20.66 range = $296.77 target. Breakout agent explicitly labeled this "setup to watch, not yet to enter."

**Post-earnings watch levels.** Bull case: clean close above $276.11 on 1.5x+ volume + ADX expansion above 25. Bear case: earnings miss triggers pullback to 38.2% Fib cluster $264.21/$264.36 — mean-reversion long. Invalidation: close below $255.45 (21-test support) signals trend break.
