---
name: SNDK technicals
last_updated: 2026-05-05
last_run_id: 20260505_211609
target_words: 350
stale_after_days: 7
word_count: 345
summary: Parabolic extension deepened — price $1,406 intraday (up from $1,256 prior run), 62% above 50-SMA; hourly RSI divergence no longer confirmed; Z-score 2.69; setup type parabolic trending extension — watch-not-act zone; wait-to-buy $1,072-1,100 (10 EMA)
---

# SNDK — Technicals

## TL;DR

Price ~$1,406 intraday (run 20260505_211609). 62% above the 50-SMA (~$812), 175% above the 200-SMA. Daily ADX 64.82 — extreme trend strength, +DI 37.48 >> -DI 6.42. Hourly RSI-21 84.55 — deeply overbought but **no confirmed RSI bearish divergence** this run (prior divergence signal not reaffirmed). Daily Bollinger pct_b 1.072 (well above upper band). Hourly pct_b 1.014. Z-score vs 50-period: 2.69 daily, 2.88 hourly. Setup type: parabolic trending extension — watch-not-act zone. [source: signals_combined.json swing_head_trader + swing_mean_reversion SNDK, run 20260505_211609]

## Multi-timeframe state

- **Daily:** EMA stack fully bullish — 10 EMA ~$1,072 > 21 EMA ~$969 > 50 SMA ~$812. All rising. Daily Bollinger pct_b 1.072 (outside upper band). RSI(7) 85.22, RSI(14) 72.87. Daily BB width 0.537 (wide — volatility fully expanded, squeeze is done). MACD histogram +22.99, momentum accelerating. ROC-5d +17.35%, ROC-10d +37.55%, ROC-21d +79.0% — all positive and expanding. [source: signals_combined.json swing_trend_momentum SNDK, run 20260505_211609]
- **Hourly:** RSI(21) 84.55 with hourly Z-score 2.88. Hourly pct_b 1.014 (above upper band). Hourly ADX 44.72. Hourly relative volume 0.31 — critically thin, no institutional accumulation. MACD histogram +27.44 (positive, expanding). [source: signals_combined.json swing_mean_reversion SNDK, run 20260505_211609]
- **Volume:** May 4 daily volume 17.85M vs 20-day avg 15.66M (1.14x) — below the 1.5x confirmation threshold. Hourly relative volume 0.31 — sub-threshold. [source: signals_combined.json swing_breakout SNDK, run 20260505_211609]

## Key levels

| level | value | rationale |
|---|---|---|
| intraday high / new ATH | ~$1,418 | hourly swing high reference for mean-reversion stop |
| mean-reversion stop reference | $1,480 | mean_reversion agent adjusted stop (above ATH + buffer) |
| current price | $1,406 | intraday price run 20260505_211609 |
| Fib ext 1.272 (upside target) | $1,470 | only 4.5% upside — fails 2:1 R/R |
| wait-to-buy zone | $1,072–$1,100 | 10 EMA convergence; R/R 2:1+ long entry |
| hourly pivot support | $1,060 | macro_context entry reference |
| deeper support | $960–$980 | 21 EMA zone / mean-reversion primary target |

## Setup type

**Parabolic trending extension — no actionable entry.** Trend is genuinely extreme (ADX 64.82, +DI 37.48 >> -DI 6.42, ROC-21d +79%). Price up from $1,256 (prior run) to $1,406 — the parabolic move has continued. R/R from current price: Fib 1.272 target ($1,470) = 4.5% upside vs $1,060 stop = 24.5% downside = **0.18:1** — fails 2:1 minimum by a factor of 11. Head Trader neutral (conf 22). Stock already trading above sell-side consensus PT ($1,250 avg); Seeking Alpha downgraded as "overheated." Wait for pullback to 10 EMA ($1,072–1,100). [source: signals_combined.json swing_head_trader + swing_macro_context SNDK, run 20260505_211609]

## Last updated

2026-05-05 — run 20260505_211609. Prior technicals (run 20260504_212836) showed price at $1,256 with hourly RSI bearish divergence active; both conditions have evolved — price extended further, divergence not reconfirmed.
