---
name: open positions snapshot
description: Structured ledger view of currently-open and pending swing trades. Refreshed nightly. Read by head trader + portfolio manager only.
type: meta
last_updated: 2026-05-05
snapshot_at_pt: 2026-05-05T22:08:51.032741-07:00
target_words: 600
stale_after_days: 2
word_count: 270
---

# Open Positions — Snapshot

Snapshot taken: `2026-05-05T22:08:51.032741-07:00`. Refreshed nightly by `tracker/wiki_open_positions_update.py` + `wiki_open_position_writer`.

## Summary

- Open positions: 6
- Pending orders: 1
- Net long count: 3
- Net short count: 4
- Tickers held: BAC, AMD, AAPL, JNJ, META, GOOG, WDC

## Open positions

| Ticker | Dir | Qty | Entry | Current | Stop | Target | Days | Unreal $ | Unreal % | Run |
|---|---|---|---|---|---|---|---|---|---|---|
| BAC | long | 15 | 52.75 | 53.12 | 51.50 | 55.40 | 6 | +5.55 | +0.70% | 20260430_190826 |
| AMD | short | 1 | 354.49 | 355.26 | 372.31 | 277.74 | 5 | -0.77 | -0.22% | 20260501_132346 |
| AAPL | long | 2 | 277.27 | 284.18 | 269.50 | 294.84 | 2 | +13.82 | +2.49% | 20260501_144523 |
| JNJ | short | 3 | 229.06 | 225.55 | 235.00 | 216.53 | 5 | +10.53 | +1.53% | 20260501_194523 |
| META | short | 1 | 611.78 | 604.96 | 635.00 | 575.00 | 2 | +6.82 | +1.11% | 20260504_143030 |
| GOOG | short | 1 | 383.00 | 384.27 | 389.50 | 338.95 | 1 | -1.27 | -0.33% | 20260505_164543 |

## Pending orders

| Ticker | Dir | Qty | Limit | Current | Stop | Target | Confidence | Run |
|---|---|---|---|---|---|---|---|---|
| WDC | long | 2 | 446.00 | 465.26 | 428.00 | 489.00 | 44 | 20260505_203524 |

## Field definitions

- **Dir**: `long` or `short`.
- **Entry**: actual fill price for open positions; limit price for pending orders.
- **Current**: most recent traded price at snapshot time (may be stale on weekends/holidays).
- **Days**: trading days between entry and snapshot (open positions only).
- **Unreal $/%**: unrealized P&L from entry to current price. Sign reflects long/short direction.
- **Run**: the run_id that originated this position.
