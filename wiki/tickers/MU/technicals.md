---
name: MU technicals
last_updated: 2026-05-07
last_run_id: 20260507_211526
target_words: 350
stale_after_days: 7
word_count: 349
summary: Overbought extension eased marginally — price $646.63 intraday (pulled back from $667 prior run); Z-score 3.27 (down from 3.36 but still extreme — highest in current universe); ADX 63.4 daily / 73.78 hourly; hourly OBV bearish divergence RETURNED (had cleared last run — regression); hourly rel vol 0.38x (distribution); wait-to-buy zone now $627-$650 (hourly support stop) or $560 (10 EMA); cluster-blocked by SNDK; JEDEC May 12-13 catalyst intact
---

# MU — Technicals

## TL;DR

Price ~$646.63 intraday (run 20260507_211526) — pulled back ~3% from $667 prior run high. 52.22% above 50-SMA (~$437). Daily ADX **63.4** — very strong uptrend, +DI 46.62 >> -DI 9.12. RSI-7 88.35, RSI-14 87.17 (extreme overbought). Z-score vs 50-period: **3.27** (eased slightly from 3.36 — still extreme, highest of both tickers this run). Daily Bollinger pct_b 1.12 (above upper band). **Hourly OBV bearish divergence RETURNED** — diverging_from_price: true (was cleared/uptrend in prior run 20260506_211601 — this is a regression of the key bullish development). Hourly relative volume 0.38x average (severely sub-threshold, worsened from 0.40x). Setup type: overbought extension — no actionable entry. Cluster-blocked: MU+SNDK $874 > 30% of $1,457 capital. [source: signals_combined.json swing_head_trader + swing_mean_reversion + swing_macro_context MU, run 20260507_211526]

## Multi-timeframe state

- **Daily:** EMA fully bullish — 10 EMA ~$560 > 21 EMA ~$510 > 50 SMA ~$437. All rising. Daily pct_b 1.12. RSI(7) 88.35, RSI(14) 87.17, RSI(21) 87.83. BB width 0.5428 (fully expanded, squeeze done). MACD histogram +17.36. ROC-5d +28.57%, ROC-10d +36.74%, ROC-21d +76.54%. [source: signals_combined.json swing_trend_momentum MU, run 20260507_211526]
- **Hourly:** RSI(21) 64.87 (not overbought — eased). Hourly ADX 73.78 — extreme, +DI 28.46 >> -DI 12.64. Hourly MACD histogram +0.71 (nearly flat, stalling). Hourly ROC-5d -2.21%, ROC-10d -0.77% — momentum negative/stalling on shorter timeframe. **Hourly OBV: diverging_from_price = true** — bearish divergence reappeared (reversed from the uptrend confirmed in 20260506_211601; this is the key regression this run). Hourly relative volume 0.38x (severely sub-threshold). [source: signals_combined.json swing_mean_reversion + swing_breakout MU, run 20260507_211526]
- **Volume:** Daily volume ratio 1.36x 20-day average (fails 1.5x breakout threshold). Hourly relative volume 0.38x — sub-threshold. [source: signals_combined.json swing_breakout MU, run 20260507_211526]

## Key levels

| level | value | rationale |
|---|---|---|
| intraday price | ~$646.63 | run 20260507_211526 |
| hourly resistance | $651.74 | 12 tests, volume-confirmed (above current price) |
| Fib ext 1.272 (target) | $764.55 | swing_trend_momentum / macro_context target |
| hourly pivot support | $627.58 | volume-confirmed, 4 tests — stop reference for catalyst play |
| catalyst entry zone | $646–$648 | swing_catalyst_news preferred entry near support (JEDEC play) |
| wait-to-buy zone (trend) | ~$560 | 10 EMA — trend_momentum strategy entry zone |
| 50-SMA | ~$437 | deep support / mean-reversion target |

## Setup type

**Overbought extension — no actionable entry.** Z-score 3.27 is the most statistically stretched ticker analyzed this run. R/R from current price ($646.63): Fib 1.272 target ($764.55) = +18.2% upside vs hourly support stop ($625) = -3.3% downside = 5.5:1 — mathematically excellent, but blocked by the MU+SNDK cluster cap (combined $874 > 30% of $1,457). The key technical regression this run: **hourly OBV bearish divergence has returned** (was uptrend last run — the primary bullish improvement from 20260506_211601 is now reversed). JEDEC May 12–13 catalyst intact. Risk manager: `remaining_position_limit = 0.0` (cluster_capped). Head Trader bullish (42 conf) but PM hold (0 conf). [source: decisions.json + signals_combined.json risk_management_agent MU, run 20260507_211526]

## Last updated

2026-05-07 — run 20260507_211526. Prior technicals (run 20260506_211601) showed price $667, Z-score 3.36, ADX 61.98 daily / 81.52 hourly, **hourly OBV divergence cleared** (uptrend). Key changes: price pulled back to $646.63, Z-score eased to 3.27, **hourly OBV bearish divergence reappeared** (primary regression), hourly rel vol worsened to 0.38x, JEDEC catalyst window now 5–6 trading days.
