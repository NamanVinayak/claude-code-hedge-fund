---
name: JNJ trades
last_updated: 2026-05-07
last_run_id: 20260507_194523
target_words: 800
stale_after_days: 60
word_count: 918
summary: 1 confirmed open short in trade_ledger.json — id 116, 3 shares filled at $229.06 on 2026-05-01, target $216.53, stop $235 (ledger); May 7 decision: hold existing short, no new entry (BofA Conference May 12 + position limit exhausted); unrealized gain ~+$13.32 at $224.62; 5/5 agents unanimously bearish; all stats from trade_ledger.json per hard rule #11
---

# JNJ — Trades

## TL;DR

As of run 20260507_194523, the trade ledger (`trade_ledger.json:per_ticker_history["JNJ"]`) confirms **1 open short position** for JNJ: id 116, 3 shares filled at $229.06 on 2026-05-01 (entered 2026-05-01 13:30 UTC). Target $216.53, stop $235.00 (ledger value). Current price ~$224.62 — unrealized gain approximately +$4.44/share × 3 = +$13.32. The May 5 new short decision (run 20260505_194525: 5 shares at $226.50 entry, stop $231.00, target $216.53) does NOT appear in per_ticker_history[JNJ] as of this snapshot — **not claimed as a confirmed trade per hard rule #11.** All stats below are sourced exclusively from trade_ledger.json per hard rule #11. (Source: trade_ledger.json, per_ticker_history[JNJ], run 20260507_194523.)

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
| Stop loss | $235.00 (ledger) |
| R/R (at fill) | 2.59:1 |
| Confidence | 58% |
| Account risk | 0.51% |
| Timeframe | 5–12 trading days |
| Created | 2026-05-01T20:15:58+00:00 |
| Entered | 2026-05-01T13:30:00+00:00 |
| Closed | — (open) |
| Exit fill price | — |
| Realized P&L | — |
| Last checked | 2026-05-07T19:55:00+00:00 |

**Current state (May 7).** Price $224.62; fill at $229.06. Unrealized gain: ~$4.44/share × 3 = ~$13.32. Trade is running in-direction toward target $216.53. Stop $235.00 per ledger; PM decisions.json this run recommends $228.50 as the active management stop. Position has never touched the stop since entry. Prior grading: direction_correct=true. Per run 20260507_194523 decisions.json: "5/5 agents bearish, existing 3-share short (entry $229.06, id 116) working — unrealized gain ~$13. Position limit exhausted ($0 remaining). Hold: let short work toward $216.53 target. Stop at $228.50 protects against BofA conference short squeeze." (Source: trade_ledger.json id 116; decisions.json, run 20260507_194523.)

**Original PM reasoning (run 20260501_194523):** 4/5 swing agents bearish. Confirmed daily downtrend (EMA stack inverted, ADX 30.72, -DI > +DI, OBV down). Bounce to 10-EMA resistance ($229–231) is textbook short entry. R/R 2.59:1. No open JNJ position at time of decision. Risk-on macro removes defensive bid. 3 shares × $229.85 = $689.55 within 25% cap. Stop $235 above EMA21/consolidation.

## Closed — last 30 days

None. (Source: trade_ledger.json, recent_closures_30d, run 20260507_194523.)

## Run history — holds and decisions

| Run ID | Date | Decision | Confidence | Direction | Ledger status |
|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 35% | None — earnings binary blocked entry; BB squeeze building | No ledger entry |
| 20260415_110848 | 2026-04-15 | hold | 42% | None — squeeze unresolved; ADX below 25 threshold | No ledger entry |
| 20260430_194522 | 2026-04-30 | short | 42% | ~4 shares at $229.50 | Not in per_ticker_history — unconfirmed |
| 20260501_194523 | 2026-05-01 | short | 58% | 3 shares at $229.85 | **Confirmed — id 116, fill $229.06** |
| 20260504_194523 | 2026-05-04 | hold | 55% | Hold existing short — no new entry | id 116 open, status entered |
| 20260505_194525 | 2026-05-05 | short (new) | 52% | 5 shares at $226.50, stop $231, target $216.53 | Not in per_ticker_history — decision only, unconfirmed |
| 20260506_194605 | 2026-05-06 | hold | 58% | Hold existing 3-share short; no new entry; BofA Conference May 12 blocks add | id 116 open, status entered; May 5 decision still unconfirmed |
| 20260507_194523 | 2026-05-07 | hold | 58% | Hold existing 3-share short; no new entry; 5/5 agents unanimously bearish; BofA Conference May 12 (~5 days) binary risk; position limit exhausted | id 116 open, status entered; unrealized ~+$13.32 |

(Source: decisions.json for each respective run; trade_ledger.json for ledger status, run 20260507_194523.)

## Closed — older than 30 days

None.

## Lifetime stats (from trade_ledger.json)

| Metric | Value |
|---|---|
| Total confirmed trades (ledger) | 1 |
| Open confirmed positions | 1 (id 116) |
| Closed confirmed trades | 0 |
| Realized P&L | $0.00 |
| Unrealized P&L | ~+$13.32 (3 shares × $4.44/share at $224.62 vs $229.06 fill) |
| Runs analyzed | 8 |
| Runs resulting in hold | 5 (Apr 11, Apr 15, May 4, May 6, May 7) |
| Runs resulting in short decision | 3 (Apr 30, May 1, May 5) |
| Confirmed fills | 1 (id 116, fill $229.06 on 2026-05-01) |
| Win rate (closed, confirmed) | n/a — no confirmed closes yet |
| Direction accuracy (open) | Correct — price $224.62 vs fill $229.06, moving toward $216.53 target |

## Notes and lessons

**May 5 new short decision — still unconfirmed in ledger as of run 20260507_194523.** Run 20260505_194525 decisions.json issued a new short: 5 shares at entry $226.50, stop $231.00, target $216.53, R/R 2.2:1, conf 52. This decision does NOT appear in trade_ledger.json per_ticker_history[JNJ] as of the snapshot for run 20260507_194523. Per hard rule #11, this trade is NOT claimed as confirmed.

**May 7 decision: hold, no add.** Run 20260507_194523 decisions.json holds the existing 3-share short. Reasoning: BofA Healthcare Conference May 12 (~5 trading days) is a binary event — positive IMAAVY or Darzalex commentary could trigger a short squeeze from near-oversold RSI-14 34.31. The risk manager confirms the portfolio position limit for JNJ is exhausted (remaining=$0.00), meaning no new JNJ shares can be added.

**Position is working correctly.** Entry fill $229.06 on May 1; current price $224.62 on May 7 (4 trading days in per calendar). Unrealized gain ~+$13.32 total. The $223.78 pivot support has been tested 6 times without a confirmed daily close below on volume >1.5x. Hourly price $222.14 broke below intraday but daily close held at $224.62. A confirmed daily close below $223.78 on >1.5x volume would open the measured-move target of $216.53 — approximately $8.09 additional downside from current price.

**Stop levels.** The original decision (run 20260501_194523) used stop $235.00 — this remains the ledger value for id 116. The May 7 PM (decisions.json, run 20260507_194523) recommended $228.50 as the active management stop, placed above the $226.53 hourly resistance (30 tests) and the BofA Conference resistance zone. The ledger stop ($235.00) remains the official ingest value for id 116 until a stop-change is recorded.

**Key risk ahead.** BofA Healthcare Conference May 12 is the dominant binary. IBD trial failure (May 5, STAT News) is the most recent pipeline miss supporting the short thesis. 5/5 agents unanimously bearish in run 20260507_194523 — the strongest directional consensus in JNJ's run history.
