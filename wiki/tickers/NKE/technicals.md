---
name: NKE technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 362
summary: extreme downtrend — ADX 64.6, all EMAs aligned bearish, multi-oscillator oversold floor near $42
---

# NKE — Technicals

## TL;DR

As of April 11, 2026 (`swing_20260411_211655`), NKE was in one of the strongest downtrends in the analyzed universe (ADX 64.6). All EMAs fanning bearish, price at $42.62 — 35% below the 200 SMA. Every momentum oscillator at or near statistical extremes. A bounce from this zone was likely; the trend direction was not in dispute.

---

## Multi-timeframe state

All data from `swing_20260411_211655` unless noted.

| Indicator | Value | Interpretation |
|---|---|---|
| Price (Apr 11) | $42.62 | Near 52-week low of $42.36 |
| 10 EMA | $45.74 | Price well below — bearish |
| 21 EMA | $49.27 | Fanning bearish |
| 50 EMA | $54.51 | Further bearish fan |
| 200 SMA | $65.34 | Price 35% below — extreme |
| ADX | 64.64 | Very strong trend (>60 rare) |
| RSI (14) | 22.6 | Deeply oversold (<30) |
| RSI (28) | 17.95 | Longer-window confirms extreme |
| Stochastic K | 2.19 | At floor — near 0 |
| Williams %R | -97.8 | Extreme |
| Z-score | -2.06 | Past -2 standard deviation |
| MACD histogram | -0.56 | Still negative, no cross |
| CCI | -107.0 | Bearish territory |
| Bollinger position | 0.12 | Hugging lower band |
| ROC (5d) | -3.6% | Accelerating |
| ROC (10d) | -18.1% | Catastrophic |
| ROC (21d) | -23.5% | Catastrophic |
| Historical volatility | 59.1% | High — wide stops required |
| ATR ratio | 4.6% | Daily range ~$1.97 on $42.62 |

---

## Key levels

| Level | Value | Source |
|---|---|---|
| 52-week low | $42.36 | `swing_20260411_211655` web_research |
| Apr 11 price | $42.62 | `swing_20260411_211655` signals |
| 10 EMA (resistance) | $45.74 | Swing head trader bounce entry zone |
| Apr 17 entry price | $45.54 | `20260417_233350` decision |
| Apr 11 short entry | $44.00 | `swing_20260411_211655` decision |
| Short stop (Apr 17) | $47.50 | `20260417_233350` decision |
| Short stop (Apr 11) | $46.50 | `swing_20260411_211655` decision |
| Bear target (Apr 17) | $41.50 | `20260417_233350` decision |
| Bear target (Apr 11) | $38.00 | `swing_20260411_211655` decision |

---

## Setup type

**Continuation short on oversold bounce.** Both runs targeted entry near the 10 EMA ($44–$46 zone) — not at the absolute low. The logic: ADX 64.6 trend continuation shorts have higher probability when entered on a relief bounce rather than into the capitulation low, where short-covering can produce violent reversals (which did happen in April, see trades.md).

The Hurst exponent near zero (stat-arb agent, `swing_20260411_211655`) indicates a near-random-walk price process at this scale — high volatility, not a smooth trend. Combined with skewness of -2.7 and kurtosis 16.3, this signals fat-tailed downside with occasional explosive reversals.

---

*Data freshness: 7-day stale threshold. Re-run prepare.py to refresh.*
