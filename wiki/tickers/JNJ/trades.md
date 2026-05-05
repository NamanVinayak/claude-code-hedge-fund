---
name: JNJ trades
last_updated: 2026-05-05
last_run_id: 20260505_194525
target_words: 800
stale_after_days: 60
word_count: 950
summary: 1 confirmed open short in trade_ledger.json — id 116, 3 shares filled at $229.06 on 2026-05-01, target $216.53, stop $235 (ledger); new short decision from run 20260505_194525 (5 shares at $226.50, stop $231, conf 52) NOT YET in per_ticker_history — not claimed as confirmed trade per hard rule #11
---

# JNJ — Trades

## TL;DR

As of run 20260505_194525, the trade ledger (`trade_ledger.json:per_ticker_history["JNJ"]`) confirms **1 open short position** for JNJ: id 116, 3 shares filled at $229.06 on 2026-05-01 (entered 2026-05-01 13:30 UTC). Target $216.53, stop $235.00 (ledger value). The current run (20260505_194525) decisions.json issued a NEW short decision — 5 shares at $226.50 entry, stop $231.00, target $216.53, R/R 2.2:1, conf 52. **That new short decision does NOT appear in per_ticker_history[JNJ] and is therefore NOT claimed as a confirmed trade per hard rule #11.** All stats below are sourced exclusively from trade_ledger.json per hard rule #11. (Source: trade_ledger.json, per_ticker_history[JNJ], run 20260505_194525.)

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

**Current state (May 5).** Price ~$225.67 area; fill at $229.06. Unrealized gain: ~$3.39/share × 3 = ~$10.17 (slight reduction from prior day bounce from $223.78 pivot). Trade is running in-direction toward target $216.53. Stop $235.00 per ledger; decisions.json from this run recommends $231.00. The position has never touched the stop since entry. Prior grading: direction_correct=true, MFE 1.23–1.51%, MAE 0.0% across agents. (Source: trade_ledger.json id 116; decisions.json, run 20260505_194525.)

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
| 20260505_194525 | 2026-05-05 | short (new) | 52% | 5 shares at $226.50, stop $231, target $216.53 | Not in per_ticker_history — decision only, unconfirmed |

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
| Runs analyzed | 6 |
| Runs resulting in hold | 3 (Apr 11, Apr 15, May 4) |
| Runs resulting in short decision | 3 (Apr 30, May 1, May 5) |
| Confirmed fills | 1 (id 116, fill $229.06 on 2026-05-01) |
| Win rate (closed, confirmed) | n/a — no confirmed closes yet |
| Direction accuracy (open) | Correct — price ~$225.67 vs fill $229.06, moving toward $216.53 target |

## Notes and lessons

**Prior zero-ledger entry now resolved.** The May 1 trades.md correctly flagged that per_ticker_history[JNJ] = [] despite two short decisions being issued. The May 4 ledger snapshot confirmed the May 1 short (id 116) has been ingested and is entered. The Apr 30 short decision (~4 shares at $229.50) remains unconfirmed in per_ticker_history. Per hard rule #11, only id 116 is treated as a confirmed trade.

**May 5 new short decision — unconfirmed in ledger.** Run 20260505_194525 decisions.json issued a new short: 5 shares at entry $226.50, stop $231.00, target $216.53, R/R 2.2:1, conf 52. This decision does NOT appear in trade_ledger.json per_ticker_history[JNJ] as of the snapshot taken for this run. Per hard rule #11, this trade is NOT claimed as confirmed. Once the ledger snapshot is updated (next run), if this entry appears, it will be added to the Open positions block with the confirmed fill price.

**Position sizing note.** 3 shares × $229.06 fill = $687.18 notional. Risk per share = $229.06 − $235.00 stop = $5.94/share × 3 = $17.82 max risk. Account risk pct at entry: 0.51% of portfolio. Within risk manager constraints (max 2.5% account risk, max 30% of capital).

**Stop levels.** The original decision (run 20260501_194523) used stop $235.00 — this remains the ledger value for id 116. The May 4 run (20260504_194523) PM reasoning cited $231.50; the May 5 run (20260505_194525) decisions.json cites $231.00 for the new short. The tightening reflects that price has moved in-profit and the $229–231 zone is confirmed overhead resistance. The ledger stop ($235.00 per id 116) remains the official ingest value until a stop-change is recorded in Turso.

**Key risk ahead.** Price at $224.07 is pressing the 4-test $223.78 pivot support. A bounce from this level to $226–229 is possible before continuation to $216.53 target. Stop at $231.50 gives the trade room to survive such a bounce while protecting the majority of unrealized gain.
