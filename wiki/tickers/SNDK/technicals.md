---
name: SNDK technicals
last_updated: 2026-05-06
last_run_id: 20260506_211601
target_words: 350
stale_after_days: 7
word_count: 349
summary: Parabolic extension further deepened — price $1,410 intraday, Z-score 3.09 (up from 2.69), ADX 68.03 (up from 64.82), 78% above 50-SMA; hourly OBV trending DOWN, rel vol 0.19x (distribution); setup type parabolic trending extension — watch-not-act zone; wait-to-buy $1,072-1,100 (10 EMA)
---

# SNDK — Technicals

## TL;DR

Price ~$1,410 intraday (run 20260506_211601). 78% above the 50-SMA (~$791), 201.8% above the 200-SMA. Daily ADX 68.03 (up from 64.82 prior run) — extreme trend strength, +DI 47.44 >> -DI 3.31. RSI-7 87.71, RSI-14 83.05. Z-score vs 50-period: **3.09** (escalated from 2.69). Daily Bollinger pct_b 1.18 (above upper band). **Hourly OBV trending DOWN** with relative volume 0.19x average — distribution warning. Hourly ROC-5d -1.09% (momentum stalling at the hourly level). Setup type: parabolic trending extension — watch-not-act zone. [source: signals_combined.json swing_head_trader + swing_mean_reversion SNDK, run 20260506_211601]

## Multi-timeframe state

- **Daily:** EMA stack fully bullish — 10 EMA ~$1,133 > 21 EMA ~$1,009 > 50 SMA ~$791. All rising. Daily pct_b 1.18 (outside upper band). RSI(7) 87.71, RSI(14) 83.05, RSI(21) 81.13. BB width 0.6025 (wide — volatility fully expanded, squeeze is done). MACD histogram 34.31, momentum accelerating. ROC-5d +40.3%, ROC-10d +55.65%, ROC-21d +94.07% — all positive and expanding. [source: signals_combined.json swing_trend_momentum SNDK, run 20260506_211601]
- **Hourly:** RSI(21) declining from prior run. Hourly pct_b above upper band. **Hourly OBV trend: DOWN** (distribution signal — price advancing while OBV trends lower). Hourly relative volume 0.19x — critically thin, no institutional accumulation. Hourly ROC-5d -1.09% (short-term exhaustion). [source: signals_combined.json swing_mean_reversion + swing_macro_context SNDK, run 20260506_211601]
- **Volume:** Daily volume ratio 1.29x 20-day average — below the 1.5x breakout threshold. Hourly relative volume 0.19x — severely sub-threshold. [source: signals_combined.json swing_breakout SNDK, run 20260506_211601]

## Key levels

| level | value | rationale |
|---|---|---|
| intraday price | ~$1,410 | run 20260506_211601 |
| mean-reversion stop reference | $1,490 | swing_mean_reversion agent stop (prior in-progress short) |
| Fib ext 1.272 (upside target) | $1,652.88 | swing_breakout/trend_momentum target |
| sell-side avg PT | ~$1,409 | web_research/SNDK.json analyst_consensus (post-Q3 revisions) |
| wait-to-buy zone | $1,072–$1,100 | 10 EMA convergence; R/R 2:1+ long entry |
| hourly pivot support | ~$1,060 | macro_context entry reference |
| 21 EMA / mean-reversion target | ~$995–$1,009 | mean_reversion agent primary target zone |

## Setup type

**Parabolic trending extension — no actionable entry.** Trend is genuinely extreme (ADX 68.03, ROC-21d +94.07%). Price stalled near $1,406–$1,410 (essentially flat vs prior run). Z-score escalated from 2.69 to 3.09. Hourly OBV is now trending down and hourly volume is 0.19x average — consistent with distribution at the top. R/R from current price: Fib 1.272 target ($1,652.88) = +17.2% upside vs $1,133 10-EMA stop = -19.7% downside = 0.87:1 — fails 2:1 minimum. Mean-reversion agent (swing_mean_reversion) has an in-progress short from prior run at $1,406 entry, stop $1,490, target $995 (re-affirmed this run). No new entry warranted. Head Trader neutral (conf 22). [source: decisions.json + signals_combined.json swing_macro_context SNDK, run 20260506_211601]

## Last updated

2026-05-06 — run 20260506_211601. Prior technicals (run 20260505_211609) showed price $1,406, Z-score 2.69, ADX 64.82. Key changes this run: Z-score escalated to 3.09, ADX increased to 68.03, hourly OBV now trending DOWN (distribution signal confirmed), hourly rel vol 0.19x critically thin.
