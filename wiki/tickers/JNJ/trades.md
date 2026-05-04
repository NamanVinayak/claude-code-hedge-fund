---
name: JNJ trades
last_updated: 2026-05-04
last_run_id: 20260504_194523
target_words: 800
stale_after_days: 60
word_count: 899
summary: 1 confirmed open short in trade_ledger.json — id 116, 3 shares filled at $229.06 on 2026-05-01, target $216.53, stop $231.50; ~$14.85 unrealized gain as of May 4; prior zero-ledger state from run 20260501_194523 is now superseded
---

# JNJ — Trades

## TL;DR

As of run 20260504_194523, the trade ledger (`trade_ledger.json:per_ticker_history["JNJ"]`) confirms **1 open short position** for JNJ: id 116, 3 shares filled at $229.06 on 2026-05-01 (entered 2026-05-01 13:30 UTC). Target $216.53, stop $231.50 (updated from original $235 per decisions.json current run). With current price at $224.07, unrealized gain is approximately $14.85 ($4.95/share × 3 shares). This supersedes the prior trades.md (run 20260501_194523) which showed zero ledger entries — the position was pending ingestion at that time. All stats below are sourced exclusively from trade_ledger.json per hard rule #11. (Source: trade_ledger.json, per_ticker_history[JNJ], run 20260504_194523.)

## Open positions

### Trade ID 116 — Active short

| Field | Value |
|---|---|
| Trade ID | 116 |
| Run ID | 20260501_194523 |
| Status | entered |
| Direction | short |
| Quantity | 3 shares |
| Entry price (decision) | $229.85 |
| Entry fill price | $229.06 |
| Target price | $216.53 |
| Stop loss | $235.00 |
| R/R (at fill) | 2.59:1 |
| Confidence | 58% |
| Account risk | 0.51% |
| Timeframe | 5–12 trading days |
| Created | 2026-05-01T20:15:58+00:00 |
| Entered | 2026-05-01T13:30:00+00:00 |
| Closed | — (open) |
| Exit fill price | — |
| Realized P&L | — |
| Last checked | 2026-05-04T19:55:00+00:00 |

**Current state (May 4).** Price at $224.07; fill at $229.06. Unrealized gain: ~$4.99/share × 3 = ~$14.97. Trade is running in-direction toward target $216.53. Stop $231.50 (current PM hold decision) is intact and above all current price levels. The position has never touched the stop since entry. Prior grading: direction_correct=true, MFE 1.23%, MAE 0.0% after 3 trading days. (Source: trade_ledger.json id 116; decisions.json, run 20260504_194523.)

**Original PM reasoning (run 20260501_194523):** 4/5 swing agents bearish. Confirmed daily downtrend (EMA stack inverted, ADX 30.72, -DI > +DI, OBV down). Bounce to 10-EMA resistance ($229–231) is textbook short entry. R/R 2.59:1. No open JNJ position at time of decision. Risk-on macro removes defensive bid. 3 shares × $229.85 = $689.55 within 25% cap. Stop $235 above EMA21/consolidation.

## Closed — last 30 days

None. (Source: trade_ledger.json, recent_closures_30d, run 20260504_194523.)

## Run history — holds and decisions

| Run ID | Date | Decision | Confidence | Direction | Ledger status |
|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 35% | None — earnings binary blocked entry; BB squeeze building | No ledger entry |
| 20260415_110848 | 2026-04-15 | hold | 42% | None — squeeze unresolved; ADX below 25 threshold | No ledger entry |
| 20260430_194522 | 2026-04-30 | short | 42% | ~4 shares at $229.50 | Not in per_ticker_history — unconfirmed |
| 20260501_194523 | 2026-05-01 | short | 58% | 3 shares at $229.85 | **Confirmed — id 116, fill $229.06** |
| 20260504_194523 | 2026-05-04 | hold | 55% | Hold existing short — no new entry | id 116 open, status entered |

(Source: decisions.json for each respective run; trade_ledger.json for ledger status, run 20260504_194523.)

## Closed — older than 30 days

None.

## Lifetime stats (from trade_ledger.json)

| Metric | Value |
|---|---|
| Total confirmed trades (ledger) | 1 |
| Open confirmed positions | 1 (id 116) |
| Closed confirmed trades | 0 |
| Realized P&L | $0.00 |
| Unrealized P&L | ~+$14.97 (3 shares × $4.99/share at $224.07 vs $229.06 fill) |
| Runs analyzed | 5 |
| Runs resulting in hold | 3 (Apr 11, Apr 15, May 4) |
| Runs resulting in short decision | 2 (Apr 30, May 1) |
| Confirmed fills | 1 (id 116, fill $229.06 on 2026-05-01) |
| Win rate (closed, confirmed) | n/a — no confirmed closes yet |
| Direction accuracy (open) | Correct — price $224.07 vs fill $229.06, moving toward target |

## Notes and lessons

**Prior zero-ledger entry now resolved.** The May 1 trades.md correctly flagged that per_ticker_history[JNJ] = [] despite two short decisions being issued. The May 4 ledger snapshot confirms the May 1 short (id 116) has been ingested and is entered. The Apr 30 short decision (~4 shares at $229.50) remains unconfirmed in per_ticker_history — it may have been superseded by the May 1 decision, or it was a re-queue that was not executed. Per hard rule #11, only id 116 is treated as a confirmed trade.

**Position sizing note.** 3 shares × $229.06 fill = $687.18 notional. Risk per share = $229.06 − $235.00 stop = $5.94/share × 3 = $17.82 max risk. Account risk pct at entry: 0.51% of portfolio. Within risk manager constraints (max 2.5% account risk, max 30% of capital).

**Stop updated to $231.50.** The original decision used stop $235.00; the current run (20260504_194523) PM reasoning cites stop $231.50 as the active level (above the $229–231 resistance zone tested as the bounce peak). This is a tighter stop than the original $235 — reflects that price has already moved $5 in-profit and the zone above $231.50 is confirmed overhead resistance. The $235 original stop remains the thesis-invalidation level per prior documentation.

**Key risk ahead.** Price at $224.07 is pressing the 4-test $223.78 pivot support. A bounce from this level to $226–229 is possible before continuation to $216.53 target. Stop at $231.50 gives the trade room to survive such a bounce while protecting the majority of unrealized gain.
