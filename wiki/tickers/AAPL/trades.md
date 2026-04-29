---
name: AAPL trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 746
summary: Full trade journal for AAPL — one abandoned long, three no-trade holds, lifetime stats
---

# AAPL — Trades

## TL;DR

AAPL has one trade on record in tracker.db: a long that was placed on April 18 from the Apr 17 swing run and abandoned on April 29 before any fill occurred. Three prior swing runs (Apr 11, Apr 15, and the two wiki_phase1 test runs) resulted in no-trade / hold decisions. Net P&L is $0. No realized or unrealized gain or loss.

## Open positions

None. The one recorded AAPL position (trade ID 19) has status `abandoned` — the order was never filled and was closed out by the monitor on April 29.

## Closed — last 30 days

### Trade 19 — Abandoned long (never filled)

| field | value |
|---|---|
| Trade ID | 19 |
| Status | abandoned |
| Direction | long |
| Quantity | 40 shares |
| Intended entry | $262.50 |
| Target | $282.00 |
| Stop loss | $256.50 |
| Risk/reward | 3.25:1 |
| Confidence | 60% |
| Timeframe | 5–8 trading days |
| Run ID | 20260417_233350 |
| Mode | swing |
| Created | 2026-04-18 00:18 UTC |
| Closed | 2026-04-29 11:19 UTC |
| Entry fill | none |
| Exit fill | none |
| Realized P&L | $0 |

**What happened.** The Apr 17 swing run was the first run to give AAPL a buy signal after two consecutive no-trade decisions (Apr 11 gave hold at 42% confidence; Apr 15 gave hold at 47% confidence). The PM's rationale was "trend + pullback + breakout + sector bullish; fundamental overhang; wider target for 3.25:1 R:R; moderate size on split conviction." The intended entry of $262.50 was a limit order. The order sat unfilled for 11 days and was marked abandoned on April 29.

The abandonment likely reflects one of two things: (a) the order was placed at a limit price the market never revisited in the window, or (b) the monitor's daily re-order logic did not re-queue it after the Day order expired. Either way, the paper portfolio incurred no capital at risk from this position.

## Closed — older than 30 days

No trades.

## Prior run decisions (no orders placed)

These runs analyzed AAPL but the PM gave a no-trade / hold — no order was submitted to Moomoo.

| run_id | date | decision | confidence | reasoning summary |
|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | hold | 42% | EMAs tangled, ADX 15.2, overbought stochastic 89.75, no actionable setup |
| 20260415_093758 | 2026-04-15 | hold | 47% | ADX 12.5 (lowest in universe), daily supertrend bearish, 8/10 strategies neutral, CEO Tim Cook sold $12M+ |
| wiki_phase1_on | 2026-04-29 | (no decisions file) | n/a | Data-only run, no PM dispatch |
| wiki_phase1_off | 2026-04-29 | (no decisions file) | n/a | Data-only run, no PM dispatch |

## Lifetime stats

| metric | value |
|---|---|
| Total trades (with order) | 1 |
| Filled entries | 0 |
| Abandoned / expired | 1 |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 |
| Net P&L | $0.00 |
| Win rate (closed, filled) | n/a |
| Average hold time | n/a |
| Average R:R on entry | 3.25:1 (one data point) |
| Runs analyzed (AAPL) | 5 |
| No-trade decisions | 3 (Apr 11, Apr 15, wiki_phase1) |
| Buy decisions | 1 (Apr 17) |
| Short decisions | 0 |

## Notes and lessons

**The model has been conservative on AAPL — correctly so.** Three no-trade calls in a row reflect the genuine technical ambiguity: trendless price action, overbought oscillators without a trend to support the overbought, and persistent insider selling. The one buy signal (Apr 17) came when enough strategies agreed on "trend + pullback + sector bullish" for the PM to act. That the order was never filled may mean the market moved away from the limit before the order could execute — or the daily order expiry was not re-queued. Worth investigating if the next run produces another limit-order buy.

**Watch for Q2 earnings resolution.** If AAPL reports a clean April 30 earnings beat with margin guidance above 47%, the technical picture could change rapidly. The chart is coiled and the first clean trend signal could be a fast move. The levels to watch are a daily close above $263 (bull) or below $253 (bear).
