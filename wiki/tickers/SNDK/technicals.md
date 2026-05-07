---
name: SNDK technicals
last_updated: 2026-05-07
last_run_id: 20260507_211526
target_words: 350
stale_after_days: 7
word_count: 347
summary: Parabolic extension persists but Z-score eased slightly — price $1,339.96 intraday (pulled back from $1,410 prior run); Z-score 2.79 (down from 3.09); ADX 70.42 (up from 68.03); hourly OBV still trending DOWN, rel vol improved to 0.53x (from 0.19x); shooting star intraday candle; 5/5 unanimous neutral — watch-not-act zone; wait-to-buy $1,183-$1,200 (10 EMA)
---

# SNDK — Technicals

## TL;DR

Price ~$1,339.96 intraday (run 20260507_211526) — pulled back ~5% from $1,410 prior run high. 75% above the 50-SMA (~$791), 197% above the 200-SMA. Daily ADX **70.42** (up from 68.03 — extreme, confirming entrenched trend), +DI 46.61 >> -DI 3.13. RSI-7 85.73, RSI-14 82.51. Z-score vs 50-period: **2.79** (eased from 3.09 — still extreme). Daily Bollinger pct_b 1.07 (above upper band). **Hourly OBV still trending DOWN** — rel vol improved to 0.53x (from 0.19x prior) but still sub-threshold distribution signal. **Intraday bearish shooting star**: high $1,439.70, close $1,339.96 — long upper wick rejection at the all-time high zone. Setup type: parabolic trending extension — 5/5 unanimous watch-not-act. [source: signals_combined.json swing_head_trader + swing_mean_reversion SNDK, run 20260507_211526]

## Multi-timeframe state

- **Daily:** EMA stack fully bullish — 10 EMA ~$1,183 > 21 EMA ~$1,045 > 50 SMA ~$791. All rising. Daily pct_b 1.07. RSI(7) 85.73, RSI(14) 82.51, BB width 0.6523 (fully expanded). MACD histogram +38.92. ROC-5d +32.49%, ROC-10d +44.01%, ROC-21d +98.37%. [source: signals_combined.json swing_trend_momentum SNDK, run 20260507_211526]
- **Hourly:** RSI(21) 56.81 (eased from extreme). **Hourly OBV trend: DOWN** (distribution signal active). Hourly MACD histogram -9.25 (negative, contracting). Hourly ROC-5d -1.34%, ROC-10d -3.09% — momentum stalling/reverting on shorter timeframe. Hourly relative volume 0.53x (sub-threshold, improved from 0.19x). [source: signals_combined.json swing_mean_reversion + swing_macro_context SNDK, run 20260507_211526]
- **Volume:** Daily volume ratio 1.30x 20-day average (below 1.5x breakout threshold). Hourly relative volume 0.53x — sub-threshold. [source: signals_combined.json swing_breakout SNDK, run 20260507_211526]

## Key levels

| level | value | rationale |
|---|---|---|
| intraday price | ~$1,340 | run 20260507_211526 |
| intraday high | $1,439.70 | bearish shooting star rejection |
| Fib ext 1.272 (upside target) | $1,679 | swing_breakout/trend_momentum target |
| sell-side avg PT | ~$1,383.75 | web_research/SNDK.json analyst_consensus May 7 |
| wait-to-buy zone | $1,183–$1,200 | 10 EMA convergence; R/R 2:1+ long entry |
| hourly pivot support | $1,334.67 | macro_context entry reference (near-term) |
| 21 EMA | ~$1,045 | trend_momentum strategy entry zone |

## Setup type

**Parabolic trending extension — no actionable entry.** ADX 70.42 is extreme and rising; trend direction is unambiguously bullish. However, price is 19% above the 10-EMA ($1,183) — no valid pullback entry exists. Intraday shooting star (high $1,439.70, close $1,339.96) with hourly OBV distribution and hourly ROC negative is the clearest near-term warning of exhaustion at the shorter timeframe. R/R from current price: Fib 1.272 ($1,679) = +25.3% upside vs 10-EMA stop ($1,183) = -11.7% downside = 2.2:1 — barely clears 2:1 but requires aggressive target. Using nearest resistance ($1,439.70) as target: 0.63:1 — fails badly. 5/5 agents unanimous neutral. [source: decisions.json + signals_combined.json, run 20260507_211526]

## Last updated

2026-05-07 — run 20260507_211526. Prior technicals (run 20260506_211601) showed price $1,410, Z-score 3.09, ADX 68.03, hourly OBV DOWN at 0.19x rel vol. Key changes: Z-score eased slightly to 2.79, ADX increased to 70.42, price pulled back to $1,339.96 with bearish shooting star intraday, hourly rel vol improved to 0.53x (still distribution).
