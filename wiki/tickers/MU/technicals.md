---
name: MU technicals
last_updated: 2026-05-01
last_run_id: bootstrap_2026-05-01
target_words: 350
stale_after_days: 7
word_count: 410
summary: current chart state
---

# MU — Technicals

## TL;DR

MU closed 2026-05-01 at $542.21, +4.8% on the day to a fresh 52-week high. Price is +27% above the 50DMA ($425.58) and +96% above the 200DMA ($276.86). ATR(14) is $28.94, ~5.3% of price. Today's bar: open $511.78 / high $545.91 / close $542.21 on volume 40.1M (above the recent 20d average).

> _This is bootstrap context dated 2026-05-01. The runtime swing routine must do its own fresh research and indicator analysis; do not anchor to anything stated here._

## Multi-timeframe state

- **Daily**: 50/200 SMA stack with positive slope on both. Last 8 sessions HH–HL, fresh intraday high $545.91 today. Price ran from $448.42 (Apr 20 close) to $542.21 (May 1 close), +20.9% in nine sessions.
- **Weekly**: Multi-month leg from 52-week low $78.35 to $542. No nearby weekly resistance overhead.
- **Intraday (today)**: Wide-range bar closing in upper third of the day's range. Volume 40.1M, above the recent 20d average.

## Key levels

| level | value | note |
|---|---|---|
| overhead resistance / 52-week high | $545.91 | today's intraday high |
| pivot / breakout shelf | $524.56 | Apr 27 close |
| short-term support | $504.29 | Apr 28 low cluster ~$503 |
| 20-day MA | $461.77 | rising |
| 50DMA | $425.58 | trend reference |
| 200DMA | $276.86 | regime reference |
| 20-day swing low | $364.10 | nearest meaningful prior low |
| ATR(14) | $28.94 | daily range reference |
| short-term range bracket | $480 | prior pivot low |
| trend pivot | $425 (50DMA) | regime change reference |

## Setup type

Multiple setups are possible — runtime to determine which is active:

- **Trending / pullback continuation**: Active if price holds above the 20-day MA and pulls back to $504–$510 (prior resistance turned support, ~1 ATR back) without breaking $480.
- **Breakout**: Active if price builds a tight 3–5 day consolidation above $520 and breaks the inside-bar range high on expanding volume.
- **Mean-reversion (long)**: Active if price overshoots back toward the 20-day MA on declining volume and reverses with a clean higher-low.
- **Range-bound**: Active if price builds a horizontal bracket between the breakout shelf ($524.56) and the 52-week high ($545.91) over multiple sessions.
- **Counter-trend short**: Generally low-edge while the 50/200 stack is positive; would require a confirmed daily close below the 50DMA to be relevant.

## Last updated

2026-05-01 (bootstrap_2026-05-01). yfinance EOD data.
