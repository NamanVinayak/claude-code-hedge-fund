---
name: JNJ technicals
last_updated: 2026-05-05
last_run_id: 20260505_194525
target_words: 350
stale_after_days: 7
word_count: 412
summary: Downtrend deepening — ADX 33.25 (up from 31.07), RSI 27.22 deeply oversold, price ~$225.67 still below all EMAs; $223.78 pivot support (5 tests); BofA Healthcare Conference May 12 is live event risk; active short id 116 in flight; PM issued new short at $226.50 (5 shares) per decisions.json — not yet confirmed in ledger
---

# JNJ — Technicals

## TL;DR

As of May 5, 2026, JNJ's confirmed daily downtrend has further deepened. Price is trading around $225.67 (signals_combined portfolio state shows short_cost_basis $0 — new short order from this run not yet in ledger), with RSI-14 at 27.22 (deeply oversold) and ADX at 33.25 (strengthened from 31.07 on May 4). Daily EMA alignment remains fully bearish: price below all 5, 10, 20, 21, and 50-period EMAs. The $223.78 pivot support has now been tested 5 times. Hourly Bollinger squeeze primed (width 0.0325, pct_b 0.3422). Active short: id 116 (3 shares filled at $229.06, target $216.53, stop per ledger $235.00 / decisions.json says $231.00). Decisions this run: PM issued a new 5-share short at $226.50 entry, stop $231.00, target $216.53, R/R 2.2:1, conf 52 — hold-vs-add debate; ledger not yet confirmed. (Source: swing_head_trader signal, decisions.json, trade_ledger.json, run 20260505_194525.)

**Prior setup evolution.** May 4 had price $224.07 pressing the $223.78 pivot (4 tests). May 5 shows price ~$225.67 — slight dead-cat bounce from the pivot. The bounce has not exceeded $226–229 resistance zone. ADX strengthened (31.07 → 33.25), -DI still >> +DI (34.83 vs 15.44). Downtrend working as modeled.

## Multi-timeframe state

| Timeframe | Trend | Momentum | Note |
|---|---|---|---|
| Daily | Confirmed downtrend — ADX 33.25, -DI 34.83 >> +DI 15.44; all EMAs inverted | MACD -3.45 below signal -2.92; ROC-21d -7.75%; OBV daily down | RSI-14 27.22 deeply oversold; bounce risk rising but no reversal candle |
| Hourly | Downtrend — EMAs bearish aligned; -DI (33.31) >> +DI (12.36) | Bollinger width 0.0325 (extreme squeeze primed); pct_b 0.3422 | Hourly OBV slight upward divergence — watch for dead-cat bounce $226–229 |

EMA stack (daily): EMA 5 $226.74 > EMA 10 $228.29 > EMA 21 $231.44 > EMA 50 $233.15 — all above price (~$225.67). Bearish alignment intact. (Source: swing_trend_momentum, signals_combined.json, run 20260505_194525.)

## Key levels

| Level | Value | Source |
|---|---|---|
| Critical pivot support (5-test breakdown trigger) | $223.78 | swing_breakout, run 20260505_194525 |
| Measured-move target on breakdown | $216.53 | swing_breakout; decisions.json, run 20260505_194525 |
| Fib 1.272 extension target | $217.15 | swing_trend_momentum, run 20260505_194525 |
| Bollinger lower band | $220.47 | swing_macro_context, run 20260505_194525 |
| Active short entry fill (id 116) | $229.06 (3 shares) | trade_ledger.json, run 20260505_194525 |
| Stop loss (ledger) | $235.00 (id 116) | trade_ledger.json |
| New short decision (decisions.json, unconfirmed) | Entry $226.50 / stop $231.00 / target $216.53 | decisions.json, run 20260505_194525 |
| Dead-cat bounce resistance | $226–229 | swing_mean_reversion, run 20260505_194525 |
| BofA Healthcare Conference watch date | May 12, 2026 (~5 trading days) | swing_catalyst_news, run 20260505_194525 |

## Setup type

**Bearish continuation — active short at id 116, new short decision from current run unconfirmed.** ADX 33.25 confirms the downtrend has real strength. The $223.78 pivot has been tested 5 times; a confirmed daily close below on volume >1.5x average opens the measured-move target of $216.53. Risk: RSI 27.22 is deeply oversold and the hourly Bollinger squeeze could resolve either direction. Dead-cat bounce to $226–229 is possible before continuation. BofA Healthcare Conference May 12 is the two-sided event risk. Do not add to short if price is bouncing without a rejection candle at resistance. (Source: decisions.json; swing_head_trader, run 20260505_194525.)
