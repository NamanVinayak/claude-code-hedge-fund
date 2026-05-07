---
name: open positions snapshot
description: Structured ledger view of currently-open and pending swing trades. Refreshed nightly. Read by head trader + portfolio manager only.
type: meta
last_updated: 2026-05-06
snapshot_at_pt: 2026-05-06T22:05:15.165128-07:00
target_words: 600
stale_after_days: 2
word_count: 273
---

# Open Positions — Snapshot

Snapshot taken: `2026-05-06T22:05:15.165128-07:00`. Refreshed nightly by `tracker/wiki_open_positions_update.py` + `wiki_open_position_writer`.

## Summary

- Open positions: 5
- Pending orders: 0
- Net long count: 3
- Net short count: 2
- Tickers held: BAC, AAPL, JNJ, META, WDC

## Open positions

| Ticker | Dir | Qty | Entry | Current | Stop | Target | Days | Unreal $ | Unreal % | Run |
|---|---|---|---|---|---|---|---|---|---|---|
| BAC | long | 15 | 52.75 | 53.60 | 51.50 | 55.40 | 7 | +12.75 | +1.61% | 20260430_190826 |
| AAPL | long | 2 | 277.27 | 287.51 | 269.50 | 294.84 | 3 | +20.48 | +3.69% | 20260501_144523 |
| JNJ | short | 3 | 229.06 | 224.62 | 235.00 | 216.53 | 6 | +13.32 | +1.94% | 20260501_194523 |
| META | short | 1 | 611.78 | 612.88 | 635.00 | 575.00 | 3 | -1.10 | -0.18% | 20260504_143030 |
| WDC | long | 2 | 448.99 | 483.15 | 428.00 | 489.00 | 1 | +68.32 | +7.61% | 20260505_203524 |

## Pending orders

_None._

## Field definitions

- **Dir**: `long` or `short`.
- **Entry**: actual fill price for open positions; limit price for pending orders.
- **Current**: most recent traded price at snapshot time (may be stale on weekends/holidays).
- **Days**: trading days between entry and snapshot (open positions only).
- **Unreal $/%**: unrealized P&L from entry to current price. Sign reflects long/short direction.
- **Run**: the run_id that originated this position.
