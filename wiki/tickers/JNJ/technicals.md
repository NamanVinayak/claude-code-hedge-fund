---
name: JNJ technicals
last_updated: 2026-05-07
last_run_id: 20260507_194523
target_words: 350
stale_after_days: 7
word_count: 388
summary: Downtrend intact — ADX 35.93 (up from 35.28), RSI-14 34.31 (recovered from 31.16), price $224.62 below all EMAs; $223.78 pivot support (6 tests, no breakdown confirmed); active short id 116 in flight (~+$13.32 unrealized); BofA Healthcare Conference May 12 is live binary event (~5 trading days); hold existing position, no new entry; 5/5 agents unanimously bearish
---

# JNJ — Technicals

## TL;DR

As of May 7, 2026, JNJ's confirmed daily downtrend continues. Price at $224.62 (decisions.json, run 20260507_194523; short fill $229.06 per trade_ledger.json id 116). RSI-14 at 34.31 — recovered from May 6's 31.16 (approaching oversold but no reversal candle confirmed). ADX strengthened to 35.93 (up from 35.28), with -DI 32.88 decisively exceeding +DI 16.66 — confirming the downtrend is strong and directional. The $223.78 pivot support has now held through 6 tests without a confirmed daily close below on volume >1.5x (volume at 1.02x, sub-threshold). Active short: id 116 (3 shares filled at $229.06, target $216.53, stop $235.00 per ledger). Decision this run: HOLD existing short — no new entry (BofA Conference May 12 binary risk + position limit exhausted). (Source: swing_head_trader signal, decisions.json, trade_ledger.json, run 20260507_194523.)

**Prior setup evolution.** May 6 had price $224.28, RSI-14 31.16, ADX 35.28. May 7 shows price $224.62 (slight uptick — minor dead-cat bounce intraday), RSI recovered to 34.31 (approaching but not at 30 oversold threshold), ADX strengthened to 35.93. Hourly price at $222.14 at time of analysis — breaking below $223.78 intraday — but daily close remained above support. No reversal candle confirmed on either timeframe.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Confirmed downtrend — ADX 35.93, -DI 32.88 >> +DI 16.66; all EMAs above price | MACD line -3.51 below signal -3.12; histogram -0.387 (expanding bearish); ROC-21d -5.78%; OBV daily down | RSI-14 34.31 approaching oversold; no reversal candle; volume 1.02x (sub-threshold) |
| Hourly | Downtrend confirmed — EMAs bearish aligned; -DI 26.31 >> +DI 15.17, ADX 39.24 | Bollinger width 0.0469 (slightly wider than prior 0.0369); hourly MACD histogram -0.3126 (bearish) | Hourly RSI 21 at 41.06 (not oversold); hourly price $222.14 below $223.78 intraday |

EMA stack (daily): price $224.62 is below EMA5 ($225.77), EMA10 ($227.21), EMA21 ($230.33), EMA50 ($232.53). All EMAs overhead in confirmed bearish alignment. (Source: swing_trend_momentum, signals_combined.json, run 20260507_194523.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Critical pivot support (6-test breakdown trigger) | $223.78 | swing_breakout, run 20260507_194523 |
| Breakdown volume requirement | >1.5x average (currently 1.02x — unconfirmed) | swing_breakout; swing_catalyst_news, run 20260507_194523 |
| Measured-move target on confirmed breakdown | $216.53 | swing_breakout; decisions.json, run 20260507_194523 |
| Fib 1.272 extension target | $216.35 | swing_mean_reversion, run 20260507_194523 |
| Active short entry fill (id 116) | $229.06 (3 shares) | trade_ledger.json |
| Stop loss (ledger) | $235.00 (id 116) | trade_ledger.json |
| PM stop-loss (this run) | $228.50 | decisions.json, run 20260507_194523 |
| Dead-cat bounce resistance | $226.53 (30 hourly tests) | swing_breakout, run 20260507_194523 |
| BofA Healthcare Conference watch date | May 12, 2026 (~5 trading days) | swing_catalyst_news, run 20260507_194523 |

## Setup type

**Bearish continuation — active short id 116 running in-direction.** ADX 35.93 confirms the downtrend has real strength. The $223.78 pivot has now held through 6 tests without a daily close below on volume >1.5x — when this level finally breaks, the measured-move to $216.53 is the primary target. Risk: RSI-14 34.31 approaches oversold and hourly price $222.14 is already below support intraday, but daily close did not confirm the breakdown. Dead-cat bounce to $226.53 resistance is possible. BofA Healthcare Conference May 12 is the primary binary event risk — positive IMAAVY or Darzalex commentary could trigger a short squeeze from near-oversold levels. Position limit for JNJ exhausted (risk manager: remaining $0.00). 5/5 swing agents unanimously bearish this run. Decision: hold existing short, do not add. (Source: decisions.json; swing_head_trader; risk_management_agent, run 20260507_194523.)
