---
name: MU technicals
last_updated: 2026-05-05
last_run_id: 20260505_211609
target_words: 350
stale_after_days: 7
word_count: 347
summary: Overbought extension deepened — price $640 intraday (up from $576 prior run, $542 daily prior); ADX 59.67 daily / 64.77 hourly extreme; hourly OBV bearish divergence confirmed (new vs prior run); R/R broken at current price; wait-to-buy $514-530 (10 EMA); AMD binary now resolved
---

# MU — Technicals

## TL;DR

Price ~$640 intraday (run 20260505_211609). 34.5% above the 50-SMA (~$476), 85.8% above the 200-SMA. Daily ADX 59.67 — very strong uptrend, +DI 36.56 >> -DI 10.68. **Hourly OBV is bearishly diverging from price** (OBV trend down, diverging_from_price: true — new vs prior run which confirmed no divergence). Hourly relative volume 0.25x average — distribution warning. Daily RSI(7) 84.35, pct_b 1.026. Z-score vs 50-period: 2.74 daily, 2.72 hourly. Setup type: overbought extension — no actionable entry. Prior wait-to-buy zone $502–520 is now too deep relative to 10 EMA migration to $514–$530. [source: signals_combined.json swing_head_trader + swing_mean_reversion MU, run 20260505_211609]

## Multi-timeframe state

- **Daily:** EMA fully bullish — 10 EMA ~$514 > 21 EMA ~$479 > 50 SMA ~$437. All rising. Daily pct_b 1.026 (above upper band). RSI(7) 84.35, RSI(14) 77.43. MACD histogram +9.43 (positive, expanding). ROC-5d +9.89%, ROC-10d +28.55%, ROC-21d +57.4% — all positive. [source: signals_combined.json swing_trend_momentum MU, run 20260505_211609]
- **Hourly:** RSI(21) 80.4 (deeply overbought). Hourly ADX 64.77 — extreme, +DI 47.28 >> -DI 3.33. Hourly pct_b 1.014 (above upper band). **Hourly OBV divergence: bearish** (OBV trend down, diverging_from_price: true). Hourly relative volume 0.25x — critically thin. Hourly volume_bias_10d: down — institutional distribution warning. [source: signals_combined.json swing_mean_reversion + swing_macro_context MU, run 20260505_211609]
- **Volume:** May 4 volume 46.04M vs 20-day avg 39.52M (1.17x) — below 1.5x breakout threshold. Hourly relative volume 0.25x — sub-threshold. [source: signals_combined.json swing_breakout MU, run 20260505_211609]

## Key levels

| level | value | rationale |
|---|---|---|
| current price | $640 | intraday price run 20260505_211609 |
| hourly resistance | $651.74 | 2 tests, volume-confirmed — likely friction |
| Fib ext 1.272 (target) | $692 | upside target (8.1% from current) |
| mean-reversion stop ref | $675 | mean_reversion agent adjusted stop |
| wait-to-buy zone | $514–$530 | 10 EMA convergence; R/R 2:1+ long toward $692 |
| macro_context entry | $530 | swing_macro_context preferred entry |
| trend_momentum entry | $518 | swing_trend_momentum limit entry |
| prior hourly support | $502.58 | 9 tests — strong floor if $514-530 breaks |
| mean-reversion target | $471–$482 | 50-SMA area / full mean reversion |

## Setup type

**Overbought extension — no actionable entry.** R/R from current price ($640): Fib 1.272 target ($692) = 8.1% upside vs $502.58 support = 21.5% downside = **0.38:1**. Even using tightest stop ($592.77 hourly pivot): R/R = 1.09:1 — fails 2:1 minimum. AMD earnings (May 5 AMC) binary gate has now resolved; next entry gate is a pullback to the 10 EMA ($514–$530). Hourly OBV bearish divergence (new this run) is the most important technical development — institutional distribution into the price surge to $640. Correlation-blocked: SNDK+MU cluster 70.2%, risk manager cap exceeded. Head Trader neutral (conf 30). [source: decisions.json + signals_combined.json swing_macro_context MU, run 20260505_211609]

## Last updated

2026-05-05 — run 20260505_211609. Prior technicals (run 20260504_212836) showed price $576/$542 with NO hourly OBV divergence. Key change this run: OBV divergence confirmed bearish at $640 intraday (institutional distribution into the hourly price surge), and AMD binary has resolved.
