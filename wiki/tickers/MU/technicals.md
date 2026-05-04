---
name: MU technicals
last_updated: 2026-05-04
last_run_id: 20260504_212836
target_words: 350
stale_after_days: 7
word_count: 340
summary: Extended bullish trend — price $576 intraday / $542 daily close; ADX 57.4 strong uptrend; NO hourly RSI bearish divergence (key distinction from SNDK); risk-blocked by SNDK cluster correlation 0.70; wait-to-buy zone $502-520; AMD earnings May 5 is binary gate
---

# MU — Technicals

## TL;DR

Price ~$576 intraday / $542.21 daily close (run 20260504_212836). 27.4% above the 50-SMA (~$425), 95.8% above the 200-SMA. Daily ADX 57.40 — very strong uptrend, +DI 35.46 >> -DI 10.94. Critically: **no hourly RSI bearish divergence** (unlike SNDK — bearish: false confirmed). Daily RSI(14) 77.96, RSI(21) 82.18. Daily Bollinger pct_b 0.92 (inside upper band). Z-score vs 50-period: 2.36. Hourly pct_b 1.0007 (just at upper band). Setup type: extended bull trend, no actionable entry at current price — wait for AMD binary (May 5 AMC) and dip to $502-520. [source: signals_combined.json swing_head_trader MU, run 20260504_212836]

## Multi-timeframe state

- **Daily:** EMA alignment fully bullish — 10 EMA ~$500 > 21 EMA ~$470 > 50 SMA ~$431. All rising. Daily Bollinger pct_b 0.92 (inside band, not the extreme overextension of SNDK). RSI(14) 77.96, RSI(21) 82.18 — overbought but trend intact. MACD histogram positive at +7.61. ROC 21d +47.4%, 10d +19.2%, 5d +9.2%. [source: signals_combined.json swing_trend_momentum MU, run 20260504_212836]
- **Hourly:** RSI(21) 72.12 (elevated but not extreme). Hourly ADX 47.36 with +DI 40.89 >> -DI 4.34 — strong bullish alignment. Hourly pct_b 1.0007 — just at upper band. Hourly MACD histogram +5.21 positive. **NO hourly RSI bearish divergence** (bearish: false). Hourly 5d ROC -0.78% — minor pause, not a momentum reversal. Z-score 2.25. [source: signals_combined.json swing_mean_reversion MU, run 20260504_212836]
- **Volume:** May 1 volume 40.1M vs 20-day avg 39.3M (1.02x) — no breakout confirmation. Hourly relative volume 0.34 — thin participation. [source: signals_combined.json swing_breakout MU, run 20260504_212836]

## Key levels

| level | value | rationale |
|---|---|---|
| intraday high | $576.45 | May 4 intraday — at hourly Bollinger upper |
| daily close / 52-week high | $542.21–$545.91 | May 1 close / prior intraday high |
| hourly resistance | $592.77 | nearest hourly resistance (2.9% above daily close) |
| wait-to-buy zone | $502–$520 | 10 EMA convergence, hourly support cluster (9 tests at $502.58), Fib 23.6% |
| trend_momentum entry | $503 | limit entry level from swing_trend_momentum agent |
| macro_context entry | $510 | swing_macro_context entry reference |
| mean_reversion target | $490.59 | Fib 23.6% retrace from $576 |
| bear dip zone (post-AMD miss) | $471–$490 | 21 EMA / prior pivot cluster if AMD prints negatively |
| stop reference | $465 | below 21 EMA with buffer |

## Setup type

**Extended bull trend, timing fail — no actionable entry.** Trend and momentum are structurally intact (ADX 57.4, EMA aligned, no bearish hourly divergence). The distinction from SNDK: MU lacks the hourly RSI bearish divergence, keeping the bull thesis technically alive. However, price at $576 is at the hourly Bollinger upper with only 2.9% upside to next resistance ($592.77) vs 12.8% downside to $502.58 support — R/R 1.7:1 fails the 2:1 minimum. AMD earnings May 5 AMC is a direct HBM binary event within the swing window. Risk manager correlation-blocked: SNDK+MU cluster 0.70 corr, cap exceeded. Head Trader neutral (conf 38, below 40 threshold). [source: signals_combined.json swing_head_trader MU, run 20260504_212836]

## Last updated

2026-05-04 — run 20260504_212836 (first live swing run for MU).
