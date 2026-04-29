---
name: CVX technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 402
summary: Chart state as of Apr 11 swing run — bearish momentum, relief bounce entry setup
---

## TL;DR

As of April 11, CVX showed the worst momentum profile in a 19-stock universe: CCI at -170, ROC 10-day at -9.3%, and a 5-of-9 agent bearish signal. The setup was a short-on-bounce, not a break-below — the stock was expected to rally from its oversold levels (~$188.55) to around $192 before resuming the downtrend toward the $178 target. Source: run `swing_20260411_211655`.

---

## Key Levels

| Level | Value | Notes |
|---|---|---|
| Short entry (on bounce) | $192.00 | Swing model recommended entry; above then-current price ~$188.55 |
| Stop loss | $199.00 | Invalidation level; $7 above entry |
| Target | $178.00 | First major support; $14 below entry |
| Fibonacci 61.8% retracement | $185.43 | Bull case technical floor, identified by pullback trader agent |
| Resistance zone | ~$199 | Coincides with stop loss; 10 EMA area |

---

## Momentum Indicators (as of Apr 11)

| Indicator | Value | Interpretation |
|---|---|---|
| CCI | -170 | Worst in the 19-stock universe; strong bearish momentum |
| ROC 10-day | -9.3% | Sharpest 10-day decline in the energy sector |
| Stochastic | 7.37 | Deeply oversold; a bounce toward $192 was expected first |
| ADX | Not reported directly (bearish trend confirmed) | Momentum ranker 78% bearish |

---

## Multi-Timeframe State

The daily timeframe showed a confirmed downtrend with price below key moving averages. The momentum ranker agent — which examines rate of change across 5, 10, and 21-day windows — gave CVX a 78% bearish rating, the second-highest bearish conviction for any strategy on this ticker. The sector rotation agent confirmed at 73% confidence that institutional capital was flowing out of energy broadly, meaning the headwind is systemic, not stock-specific.

No hourly indicator breakdown was included in the run's facts bundle for this ticker (swing mode provides both daily and hourly, but the explanation narrative did not surface hourly divergences for CVX specifically).

---

## Setup Type

**Short on relief bounce.** Classic oversold bounce entry in a confirmed downtrend. The system did not recommend shorting at the then-current price because the stochastic at 7.37 signaled a bounce was statistically probable. The strategy was to wait for a rally to $192, then enter short with a tight $7 stop and a $14 target. Risk-reward: 2.0:1. (Source: `swing_20260411_211655/decisions.json`)

This page is stale after 7 days — technicals change fast.
