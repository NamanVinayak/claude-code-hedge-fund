---
name: WDC trades
last_updated: 2026-05-05
last_run_id: 20260505_203524
target_words: 200
stale_after_days: 60
word_count: 216
summary: zero confirmed fills — per_ticker_history[WDC]=[] in trade_ledger.json; run 20260505_203524 issued buy decision (2 shares limit $446) but no ledger fill yet; prior cluster-block resolved; watching for fill confirmation
---

# WDC — Trades

## TL;DR

No confirmed fills in trade_ledger.json. Run 20260505_203524 issued a **buy decision: 2 shares, limit $446, target $489, stop $428, R/R 2.39:1, conf 44**. The limit order has NOT been confirmed in per_ticker_history[WDC] — the order will appear in the ledger only when the fill is ingested. Per hard rule #11, this trade is not claimed here until ledger confirmation. [source: trade_ledger.json per_ticker_history[WDC]=[], decisions.json, run 20260505_203524]

## Open positions

_none (no confirmed fills in trade_ledger.json per_ticker_history[WDC])_

## Pending decision (not yet ledger-confirmed)

- **Run 20260505_203524**: Buy 2 shares, limit $446, target $489, stop $428, R/R 2.39:1, conf 44. Entry conditional: price must pull back to $444–$448 zone. Do not chase above $452. [source: decisions.json, run 20260505_203524]

## Closed — last 30 days

_none_

## Closed — older, rolled by month

_none_

## Lifetime stats

| metric | value |
|---|---|
| Total fills | 0 |
| Wins | 0 |
| Losses | 0 |
| Win rate | N/A |
| Net realized P&L | $0 |
| Runs analyzed | 2 (20260504_203608, 20260505_203524) |

## Last updated

2026-05-05 — run 20260505_203524. Buy decision issued; no ledger fill confirmed yet. Prior correlation-block (run 20260504_203608) resolved — STX is hold this run, cluster cap not triggered. Sources: trade_ledger.json per_ticker_history[WDC]=[], decisions.json.
