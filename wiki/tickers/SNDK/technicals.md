---
name: SNDK technicals
last_updated: 2026-05-04
last_run_id: 20260504_212836
target_words: 350
stale_after_days: 7
word_count: 342
summary: Parabolic post-earnings extension — price $1,256 (intraday), 55% above 50-SMA; hourly RSI bearish divergence active; setup type trending/mean-reversion watch — no actionable entry at current price
---

# SNDK — Technicals

## TL;DR

Price ~$1,256 intraday / $1,187 daily close (run 20260504_212836). 55.6% above the 50-SMA ($812 area), 164.6% above the 200-SMA. Daily ADX 62.46 — extreme trend strength, +DI 30.85 >> -DI 6.58. Hourly RSI 81.45 with confirmed bearish divergence. Daily Bollinger pct_b 1.03 (price above upper band). Z-score vs 50-period: 2.56. Setup type: parabolic trending extension — watch-not-act zone. [source: signals_combined.json swing_head_trader, run 20260504_212836]

## Multi-timeframe state

- **Daily:** EMA stack fully bullish — 10 EMA ~$1,032 > 21 EMA ~$940 > 50 SMA ~$812. All rising. Daily Bollinger pct_b 1.03 (outside upper band). RSI(14) 68.91. RSI(28) 70.48. Daily BB width 0.51 (wide — volatility already expanded, squeeze is done). MACD histogram positive at +16.98, momentum accelerating. [source: signals_combined.json swing_trend_momentum SNDK]
- **Hourly:** Hourly RSI(21) 81.45 with confirmed bearish RSI divergence (price higher highs, RSI lower highs). Hourly pct_b 1.02 (also above upper band). Hourly relative volume 0.61 — follow-through thinning. Hourly Z-score 2.67. [source: signals_combined.json swing_mean_reversion SNDK]
- **Volume:** May 1 breakout volume ~23M vs 20-day average ~15.4M (1.49x — borderline). Hourly relative volume 0.61 — well below 1.5x confirmation threshold. [source: signals_combined.json swing_breakout SNDK]

## Key levels

| level | value | rationale |
|---|---|---|
| recent intraday high | $1,275.08 | May 4 intraday high — mean-reversion stop reference |
| daily close / ATH area | $1,187–$1,189 | May 1 ATH close and intraday high |
| wait-to-short zone | above $1,200 | head trader: requires reversal candle confirmation |
| wait-to-buy zone | $1,030–$1,060 | 10 EMA convergence zone — 2:1+ R/R long entry |
| hourly support cluster | $1,060 | macro_context entry reference; prior hourly support |
| Fib 23.6% mean-reversion target | $1,040 | mean_reversion agent target from $1,256 entry |
| deeper support | $980–$1,002 | prior hourly pivot cluster |

## Setup type

**Trending / parabolic extension — no actionable entry.** The trend is real (ADX 62.46, best in run history), but price is statistically extreme (Z-score 2.56, pct_b 1.03, 55.6% above 50-SMA). Hourly RSI bearish divergence is an early exhaustion signal but not a confirmed reversal. Head Trader neutral (conf 30, below 40 threshold): wait for price to come to the trade — long entry at $1,030–$1,060 or short entry above $1,200 with reversal candle. [source: signals_combined.json swing_head_trader, run 20260504_212836]

## Last updated

2026-05-04 — run 20260504_212836 (first live swing run for SNDK).
