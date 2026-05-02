---
name: open positions snapshot
description: Structured ledger view of currently-open and pending swing trades. Refreshed nightly. Read by head trader + portfolio manager only.
type: meta
last_updated: 2026-05-02
snapshot_at_pt: 2026-05-02T06:28:06.010377-07:00
target_words: 600
stale_after_days: 2
word_count: 220
---

# Open Positions — Snapshot

Snapshot taken: `2026-05-02T06:28:06.010377-07:00`. Refreshed nightly by `tracker/wiki_open_positions_update.py` + `wiki_open_position_writer`.

## Summary

- Open positions: 5
- Pending orders: 1
- Net long count: 3
- Net short count: 3
- Tickers held: BAC, AMD, AMZN, JNJ, DIS, AAPL

## Open positions

| Ticker | Dir | Qty | Entry | Current | Stop | Target | Days | Unreal $ | Unreal % | Run |
|---|---|---|---|---|---|---|---|---|---|---|
| BAC | long | 15 | 52.75 | 53.24 | 51.50 | 55.40 | 2 | +7.35 | +0.93% | 20260430_190826 |
| AMD | short | 1 | 354.49 | 360.54 | 372.31 | 277.74 | 1 | -6.05 | -1.71% | 20260501_132346 |
| AMZN | short | 1 | 265.86 | 268.26 | 276.00 | 244.44 | 1 | -2.40 | -0.90% | 20260501_173921 |
| JNJ | short | 3 | 229.06 | 227.19 | 235.00 | 216.53 | 1 | +5.61 | +0.82% | 20260501_194523 |
| DIS | long | 2 | 103.50 | 103.08 | 101.00 | 107.11 | 1 | -0.83 | -0.40% | 20260501_221355 |

## Pending orders

| Ticker | Dir | Qty | Limit | Current | Stop | Target | Confidence | Run |
|---|---|---|---|---|---|---|---|---|
| AAPL | long | 2 | 276.00 | 280.14 | 269.50 | 294.84 | 42 | 20260501_144523 |

## Field definitions

- **Dir**: `long` or `short`.
- **Entry**: actual fill price for open positions; limit price for pending orders.
- **Current**: most recent traded price at snapshot time (may be stale on weekends/holidays).
- **Days**: trading days between entry and snapshot (open positions only).
- **Unreal $/%**: unrealized P&L from entry to current price. Sign reflects long/short direction.
- **Run**: the run_id that originated this position.
