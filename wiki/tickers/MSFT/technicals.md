---
name: MSFT technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 358
summary: evolved from confirmed downtrend (Apr 11) to SuperTrend bullish flip + price recovery to $420 (Apr 17); near-term overbought warns caution on size
---

# MSFT — Technicals

## TL;DR

MSFT went from a confirmed downtrend in early April (ADX 28.87, price $371-375, 21.5% below 200-day SMA) to a clear bullish recovery by April 17 (entry $420.26, confidence 72%, momentum agents at 78% each). The SuperTrend flip on April 15 was the key signal change. The stock remained overbought by late April — the Apr 17 run PM noted this explicitly and trimmed size to 25 shares.

## Multi-timeframe state

**As of Apr 11 (run swing_20260411_211655):**
- Daily: confirmed downtrend. ADX 28.87 confirms trend has strength. EMA structure bearish (10 < 21 < 50). Price $371-375, 21.5% below 200-day SMA. P/E 23.7x — historically cheap but technicals overriding valuation.
- Agent consensus: 44% agreement — lowest of all 19 tickers. Bears and bulls roughly balanced. Head Trader bearish at 52%; no trade taken (R:R only 0.9:1).

**As of Apr 15 (run 20260415_110848):**
- Daily SuperTrend **flipped bullish** (`trend_changed=true`) — the primary signal change. Price recovered to ~$400. 6/9 swing agents turned bullish.
- Entry zone identified: $400 (EMA50/fib 38.2% retracement). Stop: $390 (below base support). Target: $422. R:R 2.2:1. Confidence 60%.
- Note: mean reversion agent still bearish (55%); valuation agent 100% bearish on AI capex risk.

**As of Apr 17 (run 20260417_233350):**
- Momentum fully confirmed. Trend agent 78% confidence, momentum ranker 78% confidence — both strong.
- Price: $420.26. Entry taken at market. Target $442, stop $412. R:R 2.63:1.
- PM noted overbought warning and sized down to 25 shares. Hourly indicators not separately logged for this run.

## Key levels

| level | value | source |
|---|---|---|
| strong support | $390 (EMA50/fib 38.2) | run 20260415_110848 |
| stop level used | $412 | run 20260417_233350 |
| entry taken | $420.26 | run 20260417_233350 |
| near-term target | $442 | run 20260417_233350 |
| analyst median PT | $600 | web_research, run 20260415_110848 |
| deep support | $370-375 (Apr 11 low zone) | run swing_20260411_211655 |

## Setup type

**Apr 11:** Downtrend — no trade. R:R failed (0.9:1). Wait for earnings resolution.

**Apr 15:** SuperTrend reversal + pre-earnings run-up play. Classic buy-the-flip-into-earnings setup. Limit entry at pullback to $400.

**Apr 17:** Trend continuation + momentum confirmation. 78% dual-agent agreement. PM executed buy at market.

## Last updated

2026-04-29 — sourced from runs swing_20260411_211655, 20260415_110848, 20260417_233350
