---
name: UNH technicals
last_updated: 2026-04-30
last_run_id: 20260430_194522
target_words: 350
stale_after_days: 7
word_count: 342
summary: Parabolic trend at statistical extremes — ADX 81.64, RSI 94.3, z-score 2.54; no-trade zone until pullback to $348-355 EMA cluster
---

# UNH — Technicals

## TL;DR

As of the April 30, 2026 run, UNH is in a runaway uptrend with ADX 81.64 — one of the strongest trend readings in the healthcare sector — but is severely overextended: RSI-14 at 94.3, RSI-7 at 99.52, z-score 2.54, and price 25% above the 50-SMA. No actionable entry exists at current price. Wait for pullback to the $348–355 10-EMA zone. Prior setup (Apr 11 post-catalyst consolidation near $304) has been completely superseded by the +41.6% surge. (Source: swing_head_trader signal, signals_combined.json, run 20260430_194522.)

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Extreme uptrend — ADX 81.64, +DI 49.41 vs -DI 2.75 | Severely overbought — RSI 94.3, pct-b 0.905 | Textbook parabolic extension; mean-reversion risk elevated |
| Hourly | Uptrend intact (24h EMA 365.6 > 48h EMA 358.3 > 120h EMA 336.6) | MACD histogram -0.63 (turning negative) | Early intraday momentum exhaustion signal |

EMA stack (daily): 10 EMA $348.1 > 21 EMA $328.6 > 50 EMA $310.7 — textbook bullish alignment. However, price at $370.74 is 6.5% above the 10-EMA and 12.8% above the 21-EMA. (Source: swing_trend_momentum signal, signals_combined.json, run 20260430_194522.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Wait-to-buy zone (10-EMA) | $348–355 | swing_head_trader; swing_trend_momentum, run 20260430_194522 |
| Upside target (if trend resumes) | $402 (Fib 1.272 extension) | swing_trend_momentum, run 20260430_194522 |
| Mean-reversion fade entry | $368–370 on confirmed reversal candle | swing_mean_reversion, run 20260430_194522 |
| Mean-reversion target | $348 | swing_mean_reversion, run 20260430_194522 |
| Stop loss (pullback entry) | $325 (below 21-EMA) | decisions.json, run 20260430_194522 |
| Bollinger upper | $381.87 | swing_macro_context, run 20260430_194522 |
| Price at analysis (Apr 30) | $370.74 | signals_combined.json, run 20260430_194522 |

## Setup type

**No setup — no-trade zone.** This is a parabolic extension, not a consolidation or breakout pattern. The breakout that generated the prior measured-move target (~$331) fired weeks ago at ~$281–283 and has been surpassed. The current structure is: too extended to chase long (R/R 0.5:1), too strong a trend to short with confidence (ADX 81.64). Three agents independently declined entry: breakout (no consolidation range), catalyst_news (all catalysts priced), macro_context (sub-1:1 R/R veto). (Source: swing_head_trader signal, decisions.json, run 20260430_194522.)

**Prior setup archived.** The Apr 11 volume-confirmed gap breakout near $304 with target ~$331 is now historical. That measured-move target was achieved and exceeded by 12%. (Source: technicals.md bootstrap 2026-04-29.)
