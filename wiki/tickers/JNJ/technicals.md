---
name: JNJ technicals
last_updated: 2026-05-06
last_run_id: 20260506_194605
target_words: 350
stale_after_days: 7
word_count: 388
summary: Downtrend intact — ADX 35.28 (up from 33.25), RSI-14 31.16 (recovered from 27.22), price $224.28 below all EMAs; $223.78 pivot support (5 tests, no breakdown confirmed); active short id 116 in flight (+~$14 unrealized); BofA Healthcare Conference May 12 is live binary event; hold existing position, no new entry
---

# JNJ — Technicals

## TL;DR

As of May 6, 2026, JNJ's confirmed daily downtrend continues. Price is at $224.28 (signals_combined portfolio state; short_cost_basis $229.06 confirmed in ledger). RSI-14 at 31.16 — slightly recovered from May 5's deeply oversold 27.22 but still near oversold territory. ADX has strengthened to 35.28 (up from 33.25), with -DI at 35.61 significantly exceeding +DI at 15.78 — confirming the downtrend is strong and directional, not choppy. The $223.78 pivot support has held through 5 tests without a confirmed daily close below on volume >1.5x. Hourly Bollinger squeeze width 0.0369 (tight, primed). Active short: id 116 (3 shares filled at $229.06, target $216.53, stop $235.00 per ledger). Decision this run: HOLD existing short — no new entry (BofA Conference May 12 binary risk + position limit exhausted). (Source: swing_head_trader signal, decisions.json, trade_ledger.json, run 20260506_194605.)

**Prior setup evolution.** May 5 had price ~$225.67, RSI-14 27.22, ADX 33.25. May 6 shows price $224.28 (slight further decline), RSI recovered to 31.16 (dead-cat bounce risk present but no reversal candle confirmed), ADX strengthened to 35.28. The hourly MACD histogram remains at -0.197 (bearish). Price bounced off the $223.78 area — did not break through on this session.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Confirmed downtrend — ADX 35.28, -DI 35.61 >> +DI 15.78; all EMAs above price | MACD -3.462 below signal -3.025; ROC-21d -6.40%; OBV daily down | RSI-14 31.16 — near oversold but ADX 35+ keeps trend absorbed; no reversal candle |
| Hourly | Downtrend confirmed — EMAs bearish aligned; -DI (29.01) >> +DI (11.65), ADX 32.24 | Bollinger width 0.0369 (squeeze primed); hourly MACD histogram -0.197 (bearish) | Hourly RSI 37.64 (recovering but not reversal signal); OBV trending down |

EMA stack (daily): price $224.28 is below EMA5, EMA10, EMA20, EMA21, EMA50. All EMAs overhead in confirmed bearish alignment. (Source: swing_trend_momentum, signals_combined.json, run 20260506_194605.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Critical pivot support (5-test breakdown trigger) | $223.78 | swing_breakout, run 20260506_194605 |
| Breakdown volume requirement | >1.5x average | swing_breakout; swing_catalyst_news, run 20260506_194605 |
| Measured-move target on confirmed breakdown | $216.53 | swing_breakout; decisions.json, run 20260506_194605 |
| Fib 1.272 extension target | $217.15 | swing_trend_momentum, run 20260506_194605 |
| Active short entry fill (id 116) | $229.06 (3 shares) | trade_ledger.json, run 20260506_194605 |
| Stop loss (ledger) | $235.00 (id 116) | trade_ledger.json |
| Dead-cat bounce resistance | $226.53 (37 hourly tests) | swing_breakout, run 20260506_194605 |
| BofA Healthcare Conference watch date | May 12, 2026 (~5 trading days) | swing_catalyst_news, run 20260506_194605 |

## Setup type

**Bearish continuation — active short id 116 running in-direction.** ADX 35.28 confirms the downtrend has real strength. The $223.78 pivot has now held through 5 tests without a daily close below on volume >1.5x — when this level finally breaks, the measured-move to $216.53 is the primary target. Risk: RSI-14 31.16 approaches oversold and hourly Bollinger squeeze is primed and could fire either direction. Dead-cat bounce to $226.53 resistance is possible and expected before continuation. BofA Healthcare Conference May 12 is the primary binary event risk — positive IMAAVY commentary could trigger a short squeeze from these oversold levels. Position limit for JNJ exhausted (risk manager: remaining $0.00). Decision: hold existing short, do not add ahead of May 12. (Source: decisions.json; swing_head_trader; risk_management_agent, run 20260506_194605.)
