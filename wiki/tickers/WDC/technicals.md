---
name: WDC technicals
last_updated: 2026-05-06
last_run_id: 20260506_203627
target_words: 350
stale_after_days: 7
word_count: 381
summary: trade in-flight — fill confirmed at $448.99; price $483 (hourly) now ~1.2% from $489 target; RSI-14 86.09 / ADX 67.88; hourly OBV divergence resolved (now uptrend); setup type: running measured-move, hold to target
---

# WDC — Technicals

## TL;DR

Price ~$483 (hourly) / $465.26 (daily close, run 20260506_203627). Trade id 150 is in-flight: fill confirmed at $448.99, target $489, stop $428. Target is now ~1.2% away. **Key change from prior run (20260505_203524):** hourly OBV bearish divergence has fully resolved — OBV is now trending UP with price. Daily RSI-14 86.09 (vs 82.48 prior run), ADX 67.88 (vs 67.55 prior run). Bollinger pct_b 1.032 — price above daily upper band. Z-score vs 50-SMA = 2.37. Setup type: **running measured-move — hold to target, no new entry.** [source: signals_combined.json, trade_ledger.json, run 20260506_203627]

## Multi-timeframe state

- **Daily**: Price $465.26 (close) / $483 (hourly). EMA-10 ~$420, EMA-21 ~$389, EMA-50 ~$339 — fully stacked and rising. MACD histogram +5.07 (positive, expanding). Volume ratio 1.27x daily (below 1.5x breakout threshold). Bollinger pct_b 1.032 (above upper band). Daily RSI-14 86.09; RSI-21 89.49.
- **Hourly**: RSI at/above overbought. ADX 67.88 on daily confirms strong trend; hourly ADX 29.93 (digestion phase). OBV trending UP — prior bearish divergence (flagged 20260505_203524) has resolved. Hourly Bollinger pct_b 0.94 (inside upper band — less stretched than daily). ROC-5d hourly 2.48% (decelerating).
- **Momentum**: ROC 5d +19.0%, 10d +21.22%, 21d +53.0%. All positive and expanding. Daily MACD bullish.

## Key levels

| level | value | note |
|---|---|---|
| Current price | ~$483 (hourly) | above upper BB daily, running to target |
| Target (measured move) | $489 | range height $42.62 added to ATH $446.62; ~1.2% away |
| ATH → support | $446.62 | former 6-test resistance, flipped; current stop reference |
| Stop (per trade_ledger) | $428 | id 150 stop; below hourly pivot cluster |
| Daily close | $465.26 | EMA stack clean |
| EMA-10 | ~$420 | dip-buy zone if position were not open |
| EMA-21 | ~$389 | secondary support |
| Fib 1.272 extension | ~$505–$509 | secondary target if $489 breaks |

## Setup type

**Running measured-move — hold to target.** Prior "post-ATH breakout pullback" setup (20260505_203524) resolved on fill — price rallied without giving back the entry zone. Trade id 150 (fill $448.99, target $489, stop $428) is now ~$34 in profit. R/R from current price to target/stop: ~0.65:1 — catastrophically unfavorable for new entry. No new shares; hold existing position to $489 or stop. Mean-reversion agent and macro context agent both explicitly pass on new entries at current extension. [source: signals_combined.json swing_breakout, swing_macro_context, swing_head_trader, trade_ledger.json id 150, run 20260506_203627]

## Last updated

2026-05-06 — run 20260506_203627. Hourly OBV bearish divergence from run 20260505_203524 resolved — OBV now trending up. Fill confirmed in per_ticker_history[WDC] (id 150, $448.99). Price advanced from ~$465 hourly to ~$483. Sources: signals_combined.json, trade_ledger.json.
