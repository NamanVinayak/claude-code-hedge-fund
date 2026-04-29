---
name: JNJ technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 358
summary: Squeeze-ON, SuperTrend bearish, flat EMAs — direction unresolved as of Apr 15 close
---

# JNJ — Technicals

## TL;DR

As of the Apr 15, 2026 run, JNJ is in a textbook Bollinger squeeze with the direction unresolved. The daily SuperTrend is bearish, EMAs are flat and converging (EMA10 $240.08 vs EMA21 $240.21), and ADX reads 23 — all below the threshold for a tradeable trend. Eight of nine swing agents voted neutral. Wait for the squeeze to fire before entering. (Source: swing_head_trader.json, run 20260415_110848)

## Multi-timeframe state

**Daily (Apr 15, 2026 close ~$240)**

- SuperTrend: **bearish** — the primary trend indicator is bearish despite the Q1 earnings beat. Price action did not confirm the fundamental positive. (Source: swing_head_trader.json, run 20260415_110848)
- EMAs: **flat / converging** — EMA10 $240.08, EMA21 $240.21. The 1-basis-point spread means no directional lean from moving averages. (Source: swing_head_trader.json, run 20260415_110848)
- ADX: **23** — below the 25 threshold; no confirmed trend in either direction. (Source: swing_head_trader.json, run 20260415_110848)
- RSI (14): **59.7** — mildly elevated but not overbought. Provides no edge. (Source: technical_analyst_agent, signals_combined.json, run 20260415_110848)
- MACD: **slightly negative** — marginal negative momentum. (Source: swing_catalyst_trader, signals_combined.json, run 20260415_110848)
- Squeeze: **ON (building)** — volatility is compressing. A directional breakout is coming; timing and direction are unknown. (Source: swing_head_trader.json, run 20260415_110848)
- Bollinger Band position: **0.55** — mid-band. Not extended in either direction. (Source: technical_analyst_agent, signals_combined.json, run 20260415_110848)
- z-score: **-0.16** — essentially at the statistical mean, confirming no mean-reversion edge. (Source: technical_analyst_agent, signals_combined.json, run 20260415_110848)

**Apr 11 baseline (pre-earnings)**

- ADX 22.9, RSI 56.9, Bollinger width 0.048 (tight squeeze already building). z-score -0.36. Pullback trader saw a textbook 50% Fib entry at $237.30. (Source: swing_head_trader.json, run swing_20260411_211655)

## Key levels

| level | value | basis |
|---|---|---|
| resistance (bullish trigger) | $244 | Apr 15 head trader target for squeeze resolution — close above this with volume triggers long |
| current price (Apr 15 close) | ~$240 | EMA10/21 cluster |
| 50-SMA support | ~$238–240 | Price slightly below 50-SMA (swing_catalyst_trader, run 20260415_110848) |
| Fibonacci 50% pullback | $237.30 | Apr 11 pullback trader entry level (run swing_20260411_211655) |
| support / bearish trigger | $233–234 | Below this level confirms bearish SuperTrend; Apr 15 head trader stop reference |

## Setup type

**Squeeze — direction unresolved.** This is not a trend trade or a mean-reversion trade. It is a wait-for-breakout situation. Two consecutive swing runs (Apr 11, Apr 15) produced an identical "no setup" verdict. Enter only on a confirmed squeeze release with volume, not before.

## Last updated

Bootstrap from runs 20260415_110848 and swing_20260411_211655 on 2026-04-29.
