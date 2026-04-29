---
name: SPY technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 368
summary: Apr 15–17 chart showed triple-confluence breakout above OR high / VWAP / prior day high; extended daily RSI warns of mean-reversion risk
---

# SPY — Technicals

## TL;DR

Both the Apr 15 daytrade and the Apr 17 swing run saw SPY in a confirmed daily uptrend with multi-timeframe EMA alignment. The daytrade setup was a textbook triple-confluence breakout: price cleared the opening range high, prior day high, and VWAP simultaneously, with a bullish squeeze breakout firing positive momentum. The swing read added hourly ADX of 65, signaling strong directional momentum. The one consistent caution: daily RSI was stretched near 72–73 and RSI-7 reached 98.86, placing SPY in statistically overbought territory on the higher timeframe.

## Multi-timeframe state

| Timeframe | State (as of Apr 15–17 2026) | Source |
|---|---|---|
| Daily | Uptrend. EMA stack bullish, ADX ~33.68, squeeze fired bullish. RSI 72.46 (extended). | run 20260415_104041 signals |
| Hourly | Strong momentum. ADX 65, EMAs stacked below price, SuperTrend bullish. | run 20260417_233350 decision |
| 5-minute (Apr 15) | Breakout. Price above OR high ($696.35), VWAP ($696.58), prior day high ($694.58). Intraday EMAs 9/20/50 all below price. Squeeze momentum +0.30 and rising. | dt_head_trader.json |

## Key levels

| Level | Value | Notes |
|---|---|---|
| Swing entry (Apr 17) | $701.66 | PM entry on hourly breakout continuation |
| Daytrade entry (Apr 15) | $697.45 | Triple-confluence breakout zone |
| VWAP / SuperTrend support | $696.44–$696.58 | Intraday stop anchor on Apr 15 |
| Prior day high (Apr 15) | $694.58 | Key structure level cleared |
| Swing stop | $695.00 | Below VWAP cluster and swing structure |
| Daytrade stop | $696.26 | Below SuperTrend / VWAP |
| Swing target | $722.00 | 3.05:1 R:R from $701.66 entry |
| Daytrade target | $699.33 | 1.58:1 R:R (1-share position; volume limited upside) |
| Psychological resistance | $700 / 7,000 | S&P 7,000 — algorithmic profit-taking level |

## Setup type

- **Apr 15 (daytrade):** Opening-range breakout + VWAP reclaim + prior-day-high clear. Squeeze momentum confirmation. "Long above VWAP" textbook setup per dt_vwap_trader agent.
- **Apr 17 (swing):** Multi-timeframe trend continuation. Daily uptrend + hourly ADX 65. Entry on breakout from consolidation, target at prior swing high zone ($722). Sizing capped at 15 shares due to 0.96 correlation with QQQ and overlap with single-name tech book.

## Cautions

- Daily RSI-7 at 98.86 and pct_b > 1.0 (above upper Bollinger band) as of Apr 15 indicate extreme short-term overbought; historically this precedes a mean-reversion pullback within 3–5 sessions.
- Below-average intraday volume on Apr 15 (relative volume 0.71x, decreasing) reduced breakout conviction and was the primary reason confidence was capped at 64% for the daytrade.

## Last updated

Bootstrap from runs 20260415_104041 and 20260417_233350. Technicals are stale within 7 days — refresh on next run.
