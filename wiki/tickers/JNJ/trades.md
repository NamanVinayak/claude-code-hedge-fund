---
name: JNJ trades
last_updated: 2026-05-01
last_run_id: 20260501_194523
target_words: 800
stale_after_days: 60
word_count: 784
summary: No confirmed JNJ fills in trade_ledger.json per_ticker_history as of run 20260501_194523; two short decisions placed (Apr 30 and May 1); ledger shows 0 JNJ entries — pending ingestion or fill confirmation
---

# JNJ — Trades

## TL;DR

As of run 20260501_194523, the trade ledger (`trade_ledger.json:per_ticker_history["JNJ"]`) contains **zero records** for JNJ. Two short decisions have been issued across two consecutive runs — April 30 (decisions.json, run 20260430_194522: ~4 shares at $229.50) and May 1 (decisions.json, run 20260501_194523: 3 shares at $229.85) — but neither appears as a confirmed fill in per_ticker_history. Until a JNJ record appears in the ledger, no JNJ trade is confirmed. All stats below are sourced exclusively from trade_ledger.json per hard rule #11.

**Note on prior page.** The prior trades.md (run 20260430_194522) described an "open short of ~4 shares at $229.50" sourced from decisions.json. Per the current trade_ledger snapshot, that record does not appear in per_ticker_history[JNJ]. It may be pending ingestion or was not queued to the broker. This page reflects only what the ledger confirms.

## Open positions

**None confirmed in trade_ledger.json.** `per_ticker_history["JNJ"]` = `[]` as of run 20260501_194523. (Source: trade_ledger.json, run 20260501_194523.)

## Pending orders (unconfirmed — decisions.json only)

The following decisions were issued by the PM but are NOT confirmed by trade_ledger.json. Listed for reference only — do not count toward P&L or confirmed positions.

### Decision A — Short (Apr 30, 2026)

| field | value |
|---|---|
| Run ID | 20260430_194522 |
| Direction | short |
| Quantity | ~4 shares (approximate) |
| Entry price | $229.50 |
| Target | $216.53 |
| Stop | $235.00 |
| R/R | 2.36:1 |
| Confidence | 42% |
| Ledger status | Not in per_ticker_history — unconfirmed |

### Decision B — Short (May 1, 2026)

| field | value |
|---|---|
| Run ID | 20260501_194523 |
| Direction | short |
| Quantity | 3 shares |
| Entry price | $229.85 |
| Entry tolerance | 1.0% |
| Target | $216.53 |
| Stop | $235.00 |
| R/R | 2.59:1 |
| Confidence | 58% |
| Account risk | 0.51% |
| Timeframe | 5–12 trading days |
| Ledger status | Not in per_ticker_history — pending confirmation |
| Reasoning | 4/5 swing agents bearish; confirmed downtrend (EMA stack inverted, ADX 30.72, -DI > +DI, OBV down); bounce to 10-EMA resistance ($229–231) is textbook short entry; risk-on macro removes defensive bid; stop $235 above EMA21/consolidation |

(Source: decisions.json, run 20260501_194523.)

## Closed — last 30 days

None confirmed in trade_ledger.json.

## Run history — holds and decisions (no confirmed ledger entries)

| Run ID | Date | Decision | Confidence | Direction |
|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 35% | None — earnings binary blocked entry; BB squeeze building |
| 20260415_110848 | 2026-04-15 | hold | 42% | None — squeeze unresolved; ADX below 25 threshold |
| 20260430_194522 | 2026-04-30 | short | 42% | ~4 shares at $229.50 (not in ledger) |
| 20260501_194523 | 2026-05-01 | short | 58% | 3 shares at $229.85 (not in ledger) |

(Source: decisions.json for each respective run; trade_ledger.json for ledger status.)

## Closed — older than 30 days

None.

## Lifetime stats (from trade_ledger.json)

| Metric | Value |
|---|---|
| Total confirmed trades (ledger) | 0 |
| Open confirmed positions | 0 |
| Closed confirmed trades | 0 |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 (no confirmed positions) |
| Runs analyzed | 4 |
| Runs resulting in hold | 2 (Apr 11, Apr 15) |
| Runs resulting in short decision | 2 (Apr 30, May 1) |
| Confirmed fills | 0 |

## Notes and lessons

**Two consecutive short decisions, zero ledger entries.** The bearish thesis has now generated two short decisions across two back-to-back runs at nearly the same price ($229.50 on Apr 30; $229.85 on May 1). The run 20260430_194522 short at $229.50 should have been filled if it was entered at market or on the Apr 30 close — the absence from per_ticker_history[JNJ] suggests it may not have been ingested into the ledger system at the time of this snapshot. Check ingester/Turso for any JNJ records created after 2026-04-30.

**The setup is textbook but relies on technical continuation.** Both short decisions share the same core thesis: confirmed downtrend, EMA death stack, OBV institutional distribution, and macro rotation away from defensive healthcare. The catalyst/news agent (neutral, 78% confidence) correctly noted there is no scheduled binary within 10 days — the short relies purely on technical deterioration. If the bounce extends to $231–232 without a catalyst, confidence remains intact and the setup improves (better R/R from a higher entry).

**Stop discipline.** Both decisions used $235 as the stop — above EMA21 ($232.66) and the consolidation range. A close above $235 would confirm the bearish thesis is wrong and trigger the stop regardless of any ledger status.
