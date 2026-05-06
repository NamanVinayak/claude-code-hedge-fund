---
name: JNJ trades
last_updated: 2026-05-06
last_run_id: 20260506_194605
target_words: 800
stale_after_days: 60
word_count: 901
summary: 1 confirmed open short in trade_ledger.json — id 116, 3 shares filled at $229.06 on 2026-05-01, target $216.53, stop $235 (ledger); May 5 new short decision (5 shares at $226.50) confirmed NOT in per_ticker_history as of run 20260506_194605 — not a confirmed trade per hard rule #11; May 6 decision: hold existing short, no new entry; unrealized gain ~+$14.34 at $224.28
---

# JNJ — Trades

## TL;DR

As of run 20260506_194605, the trade ledger (`trade_ledger.json:per_ticker_history["JNJ"]`) confirms **1 open short position** for JNJ: id 116, 3 shares filled at $229.06 on 2026-05-01 (entered 2026-05-01 13:30 UTC). Target $216.53, stop $235.00 (ledger value). Current price ~$224.28 — unrealized gain approximately +$4.78/share × 3 = +$14.34. The May 5 new short decision (run 20260505_194525: 5 shares at $226.50 entry, stop $231.00, target $216.53) does NOT appear in per_ticker_history[JNJ] as of this snapshot — **not claimed as a confirmed trade per hard rule #11.** All stats below are sourced exclusively from trade_ledger.json per hard rule #11. (Source: trade_ledger.json, per_ticker_history[JNJ], run 20260506_194605.)

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
| Last checked | 2026-05-06T19:55:00+00:00 |

**Current state (May 6).** Price $224.28; fill at $229.06. Unrealized gain: ~$4.78/share × 3 = ~$14.34. Trade is running in-direction toward target $216.53. Stop $235.00 per ledger. Position has never touched the stop since entry. Prior grading: direction_correct=true. Per run 20260506_194605 decisions.json: "Hold existing 3-share short (entry $229.06, +$14 unrealized). Bearish thesis intact (4/5 agents, ADX 35 downtrend, macro rotation). BofA Conference May 12 binary — no add before event. Let existing short work toward $217 target. Risk mgr position limit exhausted." (Source: trade_ledger.json id 116; decisions.json, run 20260506_194605.)

**Original PM reasoning (run 20260501_194523):** 4/5 swing agents bearish. Confirmed daily downtrend (EMA stack inverted, ADX 30.72, -DI > +DI, OBV down). Bounce to 10-EMA resistance ($229–231) is textbook short entry. R/R 2.59:1. No open JNJ position at time of decision. Risk-on macro removes defensive bid. 3 shares × $229.85 = $689.55 within 25% cap. Stop $235 above EMA21/consolidation.

## Closed — last 30 days

None. (Source: trade_ledger.json, recent_closures_30d, run 20260506_194605.)

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

(Source: decisions.json for each respective run; trade_ledger.json for ledger status, run 20260506_194605.)

## Closed — older than 30 days

None.

## Lifetime stats (from trade_ledger.json)

| Metric | Value |
|---|---|
| Total confirmed trades (ledger) | 1 |
| Open confirmed positions | 1 (id 116) |
| Closed confirmed trades | 0 |
| Realized P&L | $0.00 |
| Unrealized P&L | ~+$14.34 (3 shares × $4.78/share at $224.28 vs $229.06 fill) |
| Runs analyzed | 7 |
| Runs resulting in hold | 4 (Apr 11, Apr 15, May 4, May 6) |
| Runs resulting in short decision | 3 (Apr 30, May 1, May 5) |
| Confirmed fills | 1 (id 116, fill $229.06 on 2026-05-01) |
| Win rate (closed, confirmed) | n/a — no confirmed closes yet |
| Direction accuracy (open) | Correct — price $224.28 vs fill $229.06, moving toward $216.53 target |

## Notes and lessons

**May 5 new short decision — still unconfirmed in ledger as of run 20260506_194605.** Run 20260505_194525 decisions.json issued a new short: 5 shares at entry $226.50, stop $231.00, target $216.53, R/R 2.2:1, conf 52. This decision does NOT appear in trade_ledger.json per_ticker_history[JNJ] as of the snapshot for run 20260506_194605. Per hard rule #11, this trade is NOT claimed as confirmed. If this entry appears in a future ledger snapshot, it will be added to the Open positions block with the confirmed fill price.

**May 6 decision: hold, no add.** Run 20260506_194605 decisions.json explicitly holds the existing 3-share short. Reasoning: BofA Healthcare Conference May 12 (~5 trading days) is a binary event — positive IMAAVY or Darzalex commentary could trigger a short squeeze from the deeply oversold RSI-14 31.16 level. The risk manager has flagged that the portfolio position limit for JNJ is exhausted (remaining=$0), meaning no new JNJ shares can be added regardless of signal direction.

**Position is working correctly.** Entry fill $229.06 on May 1; current price $224.28 on May 6 (5 trading days in). Unrealized gain ~+$14.34 total. The $223.78 pivot support has been tested 5 times without a confirmed daily close below on volume >1.5x. A successful break of that level would open the measured-move target of $216.53 — approximately $7.75 additional downside from current price.

**Stop levels.** The original decision (run 20260501_194523) used stop $235.00 — this remains the ledger value for id 116. Subsequent run PMs recommended $231.00 (run 20260506_194605) and $231.50 (run 20260505_194525), reflecting that overhead resistance at $229–$231 is now confirmed and the trade has moved in-profit. The ledger stop ($235.00 per id 116) remains the official ingest value until a stop-change is recorded in Turso.

**Key risk ahead.** BofA Healthcare Conference May 12 is the dominant binary. IBD trial failure (May 5, STAT News) is a new pipeline miss that supports the short thesis. A dead-cat bounce to the $226.53 resistance zone (37 hourly tests) is the near-term risk before the next leg lower toward $216–$217 target.
