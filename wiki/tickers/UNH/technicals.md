---
name: UNH technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 358
summary: Post-catalyst chart state as of Apr 11, 2026 — strong ADX trend but overbought oscillators, EMAs not yet aligned, mean-reversion risk elevated above $300
---

# UNH — Technicals

## TL;DR

As of the Apr 11 run, UNH had just gapped 10% higher on the Medicare Advantage rate hike, printing ADX at 44.1 — a very strong trend reading. But the gap created a split-picture chart: momentum agents were bullish, while mean-reversion and trend-following agents were neutral-to-bearish because the stock was overextended (z-score 2.11, price 7.9% above 50-SMA) and the EMAs were not yet cleanly aligned in a new uptrend. The system's chosen entry — a limit order at $296 rather than chasing the $304 close — was an attempt to buy the retracement to the 23.6% Fibonacci level rather than the extended top.

## Multi-timeframe state

| timeframe | trend | momentum | note |
|---|---|---|---|
| Daily | Dislocated — strong ADX but EMAs tangled | Overbought (RSI 68.9, stochastic 84.8) | 50 EMA between 10 and 21 EMA, no clean bullish stack |
| Intraday (context) | Post-gap consolidation | Declining from $312.43 intraday high | Apr 9–10 candles showed pullback from gap high |

The 10 EMA was at 291.63, the 50 EMA at 289.40, and the 21 EMA at 285.86 — the 50 was sandwiched between the other two rather than below them, which is the structure needed to confirm a bullish trend resumption. ADX at 44.1 reflects the *prior* downtrend's momentum being absorbed, not a confirmed new uptrend. (Source: swing_trend_follower signal, signals_combined.json, run swing_20260411_211655.)

## Key levels

| level | value | source |
|---|---|---|
| Gap-up origin (hard support) | $281.36 | swing_breakout_trader signal |
| 50% Fibonacci retracement | $283.38 | swing_pullback_trader signal |
| 38.2% Fibonacci retracement | $289.12 | swing_pullback_trader signal |
| 23.6% Fibonacci / PM entry | $296.23 | swing_pullback_trader signal; decisions.json |
| Stop loss (PM decision) | $288.00 | decisions.json |
| Price at analysis | $304.33 | signals_combined.json |
| Intraday gap high | $312.43 | swing_breakout_trader signal |
| Target (PM decision) | $320.00 | decisions.json |
| Measured-move breakout target | ~$331 | swing_breakout_trader signal |

## Setup type

**Volume-confirmed gap breakout with post-gap consolidation entry.** The gap printed on 2.4x average volume, meeting the breakout trader's institutional confirmation threshold. The measured move from the prior range ($259–$283, height ~$24) projects to approximately $331. (Source: swing_breakout_trader signal, signals_combined.json.)

However, the setup has conflicting signals. Mean reversion (60% bearish) interprets the same data as a gap-fill setup targeting $282. The MACD histogram at +4.89 and ROC readings (+9.8% five-day, +13.5% ten-day) support continuation, but the stochastic K at 84.8 rolling below D at 87.3 was an early sign of short-term momentum exhaustion. (Source: swing_momentum_ranker, swing_mean_reversion signals, signals_combined.json.)

**Volatility context.** Daily volatility at 3.36%, annualized at 53.3%, at the 68th percentile of its 60-day range. ATR ratio of 3.0% means moves of $9 per day are typical — the $8 stop distance in the decision is within one ATR. (Source: risk_management_agent, signals_combined.json.)
