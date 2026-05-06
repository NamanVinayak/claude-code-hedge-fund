---
name: MU technicals
last_updated: 2026-05-06
last_run_id: 20260506_211601
target_words: 350
stale_after_days: 7
word_count: 348
summary: Overbought extension further deepened — price $667 intraday (up from $640 prior run); Z-score 3.36 (up from 2.74); ADX 61.98 daily / 81.52 hourly extreme; hourly OBV divergence CLEARED (now uptrend — bullish development vs prior run); wait-to-buy zone migrated to $537 (10 EMA); cluster-blocked by SNDK
---

# MU — Technicals

## TL;DR

Price ~$667 intraday (run 20260506_211601). 47.9% above the 50-SMA (~$451), hourly price extended. Daily ADX 61.98 — very strong uptrend, +DI 45.41 >> -DI 9.55. **Hourly OBV now trending UP — prior run's bearish divergence has cleared** (key improvement vs run 20260505_211609). Hourly ADX 81.52 extreme. Daily RSI(7) 88.44, RSI(14) 85.9. Z-score vs 50-period: **3.36** (escalated from 2.74 — highest stretch in current analysis). Daily pct_b 1.17 (above upper band). Hourly relative volume 0.40x average — still sub-threshold. Setup type: overbought extension — no actionable entry. [source: signals_combined.json swing_head_trader + swing_mean_reversion MU, run 20260506_211601]

## Multi-timeframe state

- **Daily:** EMA fully bullish — 10 EMA ~$537 > 21 EMA ~$494 > 50 SMA ~$445. All rising. Daily pct_b 1.17 (above upper band). RSI(7) 88.44, RSI(14) 85.9, RSI(28) 76.98. MACD histogram 13.89 (positive, expanding). ROC-5d +26.95%, ROC-10d +42.46%, ROC-21d +69.47% — all positive and expanding. [source: signals_combined.json swing_trend_momentum MU, run 20260506_211601]
- **Hourly:** RSI(21) 76.7 (overbought). Hourly ADX 81.52 — extreme, +DI 45.41 >> -DI 9.55. Hourly pct_b above upper band. **Hourly OBV: uptrend** (divergence from prior run cleared — institutional distribution warning from 20260505_211609 no longer active). Hourly relative volume 0.40x average — sub-threshold. Hourly 5d ROC ~0.0% (short-term momentum essentially flat). [source: signals_combined.json swing_mean_reversion + swing_macro_context MU, run 20260506_211601]
- **Volume:** May 5 daily volume 64.27M vs 20-day avg 40.72M (1.58x) — meets the 1.5x threshold on the daily frame. Hourly relative volume 0.40x — sub-threshold. [source: signals_combined.json swing_breakout MU, run 20260506_211601]

## Key levels

| level | value | rationale |
|---|---|---|
| current price | ~$667 | intraday price run 20260506_211601 |
| hourly resistance | $667.67 | 3 tests, volume-confirmed — price at this level |
| Fib ext 1.272 (target) | $710.50 | swing_breakout Fib extension target |
| mean-reversion stop ref | $675–$680 | swing_mean_reversion agent stop (prior in-progress short near stop) |
| wait-to-buy zone | $627–$650 | PM preferred entry zone (R/R 2:1+ toward Fib target) |
| 10 EMA | ~$537 | trend_momentum strategy entry zone |
| prior hourly support | $627.58 | hourly support level, swing_breakout stop reference |
| 50-SMA area | ~$445–$451 | deep support / mean-reversion target |

## Setup type

**Overbought extension — no actionable entry.** R/R from current price ($667): Fib 1.272 target ($710.50) = +6.5% upside vs $627.58 support = -5.8% downside = 1.1:1 — fails 2:1 minimum. The key development this run vs prior: **hourly OBV bearish divergence has cleared** (OBV now trending up), reducing the institutional distribution signal. However, Z-score escalated to 3.36 (highest in this analysis), and hourly ADX 81.52 matches the NVDA Apr-30 and AMZN May-4 stop-out pattern exactly. JEDEC May 13 catalyst intact. Correlation-blocked: SNDK+MU cluster 70.7%, risk manager cap exceeded ($874 > 30% of $1,457). Head Trader neutral (conf 30). [source: decisions.json + signals_combined.json risk_management_agent MU, run 20260506_211601]

## Last updated

2026-05-06 — run 20260506_211601. Prior technicals (run 20260505_211609) showed price $640, Z-score 2.74, ADX 59.67, **hourly OBV bearishly diverging**. Key changes this run: price extended to $667, Z-score escalated to 3.36, ADX 61.98 daily / 81.52 hourly (more extreme), and **hourly OBV divergence cleared** (now uptrend — most significant development).
