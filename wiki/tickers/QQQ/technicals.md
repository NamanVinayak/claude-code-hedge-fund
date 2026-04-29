---
name: QQQ technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 507
summary: daily trend bullish with ADX 36/squeeze breakout; intraday was conflicted on Apr 15 with bearish SuperTrend and negative squeeze momentum
---

# QQQ — Technicals

## TL;DR

Daily timeframe is cleanly bullish: ADX 36, SuperTrend bullish, squeeze fired to the upside. The intraday picture as of April 15, 2026 (daytrade run) was the opposite — 5-minute SuperTrend bearish, squeeze momentum negative at -0.42, all 9 DT agents voted neutral. The divergence between daily and intraday led to a no-trade decision for the day. The swing run on April 17 used the daily trend to justify a long at $640.47 with a 4.25:1 R:R.

## Multi-timeframe state

**Daily (as of 2026-04-15 daytrade run)** [Source: signals_combined.json, technical_analyst_agent & dt_breakout_hunter, 20260415_104041]

| Indicator | Value | Signal |
|---|---|---|
| ADX | 36.08 | Strong trend |
| Daily Squeeze | bullish_breakout | Bullish |
| Daily SuperTrend | Bullish | Bullish |
| RSI-14 (daily) | 71.51 | Overbought — caution |
| Z-score (daily) | 2.01 | Extended, mean-reversion risk |
| EMA stack | Bullishly stacked | Bullish |

**Intraday 5-minute (as of 2026-04-15 mid-morning)** [Source: signals_combined.json, multiple DT agents, 20260415_104041]

| Indicator | Value | Signal |
|---|---|---|
| 5m SuperTrend | Bearish at $633.70 | Bearish — overhead resistance |
| 5m Squeeze Momentum | -0.42, bearish_breakout | Bearish |
| 5m MACD histogram | Slightly negative | Bearish |
| Intraday RSI-14 | 46.34 | Neutral |
| Relative volume | 0.49x | Below-average, low conviction |
| EMA 9 (5m) | $632.96 | Price just below — bearish crossover |
| VWAP | $631.67 | Price above by $1.49 |

## Key levels

| Level | Value | Source |
|---|---|---|
| Swing entry (Apr 17) | $640.47 | decisions.json, 20260417_233350 |
| Swing target | $668.00 | decisions.json, 20260417_233350 |
| Swing stop | $634.00 | decisions.json, 20260417_233350 |
| DT OR high (Apr 15) | $630.27 | signals_combined.json, 20260415_104041 |
| DT VWAP (Apr 15) | $631.67 | signals_combined.json, 20260415_104041 |
| DT 5m SuperTrend resistance | $633.70 | signals_combined.json, 20260415_104041 |
| 52-week high | $637.01 | web_research/QQQ.json, 20260415_104041 |
| 52-week low | $427.93 | web_research/QQQ.json, 20260415_104041 |

## Setup type

**Swing (Apr 17 run):** Trend-pullback-breakout in a mature daily uptrend. QQQ had already cleared resistance, so the entry at $640.47 is a continuation long with the 4.25:1 R:R justified by the 83-rated sector confidence (tech). Size constrained to 12 shares (vs fundamental allocation) due to 0.96 correlation with SPY and overlap with single-name tech longs already in the book. [Source: portfolio_notes, 20260417_233350]

**Daytrade (Apr 15 run):** No valid setup. Unanimous 9/9 neutral. Conflicted intraday structure (daily bull, intraday bear) with anemic volume (0.49x) meant no entry met the 1.5:1 minimum risk-reward. Correct call was to sit out. [Source: decisions.json, 20260415_104041]

## Last updated

2026-04-29. Technicals data is from runs 20260415_104041 and 20260417_233350. Stale after 7 days — refresh before any new QQQ trade.
