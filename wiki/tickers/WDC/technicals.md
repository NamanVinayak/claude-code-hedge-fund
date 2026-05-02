---
name: WDC technicals
last_updated: 2026-05-01
last_run_id: bootstrap_2026-05-01
target_words: 350
stale_after_days: 7
word_count: 360
summary: current chart state
---

# WDC — Technicals

## TL;DR

$431.52 close on 2026-05-01 sits ~36% above the 50-day SMA ($317.04) and ~126% above the 200-day SMA ($190.91). 14-day ATR is $23.99. 52w high $446.62 (intraday today) / 52w low $43.41. RSI is implied extreme on the 1-week move; runtime should compute fresh.

> _This is bootstrap context dated 2026-05-01. The runtime swing routine must do its own fresh research and indicator analysis; do not anchor to anything stated here._

## Multi-timeframe state

- **Daily:** Closed 2026-05-01 at $431.52 after touching a fresh 52-week high of $446.62 intraday on 15.4M shares (vs. recent 5–7M norm). Earnings beat 2026-04-30 produced a $34 close-to-close gap up. Daily RSI is likely in extreme-overbought territory given the +30% one-week move — runtime to verify.
- **Weekly:** Multi-quarter advance from the $43 low — over 9x off the bottom. Weekly closes YTD have stayed above the rising 10-week MA.
- **Monthly:** YTD +130% (from $187.61 to $431.52). +900% over twelve months.

## Key levels

| level | value |
|---|---|
| support (near) | $400 (round number / prior breakout pivot) |
| support (50dma) | $317 |
| support (200dma) | $191 |
| resistance (ATH) | $446.62 (intraday 2026-05-01) |
| 1 ATR below spot | ~$408 |
| 1 ATR above spot | ~$455 |

## Setup type

Multiple setup types are technically applicable — runtime to determine which is active:

- **Trending / continuation** — price above all major MAs, higher highs intact. Applies if the daily structure holds above $400 and prints continuation bars.
- **Breakout** — applies if price puts in a tight range above $430 and breaks/holds over $446.62 ATH on volume.
- **Mean-reversion (pullback long)** — applies if price retraces 1–1.5 ATR into the $390–$405 zone and bases.
- **Mean-reversion (fade short)** — applies if price extends further from the 50dma without consolidation; classic exhaustion-bar setup off a parabolic gap.
- **Range-bound** — applies if price chops between $430 and $446.62 without resolving.

Runtime swing routine should pick the active setup based on fresh price action, RSI, volume, and tape. Position size for the $24 ATR, not for a fixed dollar move.

## Last updated

2026-05-01 — yfinance pull at session close. ATR(14)=$23.99, 50dma=$317.04, 200dma=$190.91, 52w high=$446.62, 52w low=$43.41.
