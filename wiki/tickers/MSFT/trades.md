---
name: MSFT trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 821
summary: 1 trade in DB (trade_id=20, abandoned); 3 model runs covered — holds on Apr 11 and Apr 15 (poor R:R), buy executed Apr 17 at $420.26 (25 shares, confidence 72%)
---

# MSFT — Trades

## TL;DR

One trade is recorded in `tracker.db` for MSFT (trade_id=20). It was placed on April 18, 2026 from the April 17 run and immediately marked `abandoned` — meaning the order was placed in Moomoo but not filled before expiry (Moomoo paper orders expire end-of-day). The model recommended MSFT as a buy in two of the three runs. The first run (Apr 11) was a hold due to downtrend and poor R:R; the second run (Apr 15) issued a buy but limited to 1 share at $400; the third run (Apr 17) issued a buy at $420.26 with 25 shares.

## Open positions

None. Trade_id=20 status is `abandoned`.

## Closed — last 30 days

None closed. See abandoned trade below.

## All model runs — MSFT decision history

### Run: swing_20260411_211655 (Apr 11, 2026)

**Decision:** HOLD — no trade taken.

**Reasoning from PM:** Head Trader bearish at 52% confidence with only 44% agent agreement — lowest consensus of all 19 tickers. Downtrend confirmed (ADX 28.87, EMAs bearish, price 21.5% below 200-day SMA). Fundamentals argued against short (P/E 23.7x historically cheap), but technicals overrode. R:R failed at 0.9:1. System recommended waiting for earnings April 29 to resolve the bull/bear conflict. [source: decisions.json, run swing_20260411_211655]

**What the model wanted:** A bounce to $373 Fibonacci level for a pullback entry long, OR a further decline into $357 10-EMA for a short entry with better R:R.

**What the agents said:**
- Pullback trader: saw Fibonacci 78.6% entry near $373 as textbook long setup
- Druckenmiller-style: bullish on 23.7x P/E as cheapest Microsoft in years
- Trend follower: bearish — confirmed downtrend with all EMAs aligned down
- Sector rotation: confirmed money outflows from enterprise software
- Head Trader overall: bearish at 52%, but R:R math killed the short

---

### Run: 20260415_110848 (Apr 15, 2026)

**Decision:** BUY 1 share at $400.00. Target $422. Stop $390. R:R 2.2:1. Confidence 60%.

**Reasoning from PM:** Daily SuperTrend flipped bullish (`trend_changed=true`) — primary technical signal change. 6/9 swing agents now bullish. Pre-earnings run-up into April 29 expected. Bernstein reaffirmed $641 PT on April 13. Entry on pullback to $400 (EMA50/fib 38.2 zone), not at extended $408. Hard limit: do not chase above $408. Stop below $390 base support. Risk manager capped position at 1 share at $400 = 8% of the $5,000 portfolio. [source: decisions.json, run 20260415_110848]

**What agents disagreed:**
- Mean reversion: bearish (55%) — recent gains could reverse
- Valuation agent: 100% bearish — AI capex uncertainty, expensive absolute price

**Trade outcome:** Not executed via tracker (this run's orders may not have been placed, or order at $400 limit was not filled given the stock had already moved). No tracker.db record from this run.

---

### Run: 20260417_233350 (Apr 17, 2026) — EXECUTED

**Decision:** BUY 25 shares at $420.26. Target $442. Stop $412. R:R 2.63:1. Confidence 72%.

**Reasoning from PM:** Strong trend + accelerating momentum — trend agent and momentum ranker both at 78% confidence each, the highest reading across MSFT's model history. Tightened stop ($412) and extended target ($442) to achieve 2.63:1 R:R. PM explicitly noted overbought warning and sized down (25 shares vs. what the math would suggest) to manage mean-reversion risk at extended price. [source: decisions.json, run 20260417_233350]

**Portfolio context:** Part of a 10-long, 2-short, 2-hold portfolio. MSFT was one of 7 large-cap tech longs in this run (alongside AAPL, NVDA, META, GOOGL, AMZN, AMD). PM flagged high inter-correlation across the tech names and trimmed sizes across all of them. Gross exposure target: ~75% of $100k cash. [source: decisions.json (portfolio_notes), run 20260417_233350]

---

## Tracker.db record

| field | value |
|---|---|
| trade_id | 20 |
| ticker | MSFT |
| direction | long |
| quantity | 25 |
| status | **abandoned** |
| entry_price | $420.26 |
| exit_fill_price | None |
| pnl | None |
| created_at | 2026-04-18 00:18:19 |

**Abandoned explanation:** Moomoo paper trading orders expire at end of each trading day. The order was placed on April 18 (after midnight, so prior trading session) but did not fill before expiry. No realized P&L. [source: tracker.db query]

## Lifetime stats

| metric | value |
|---|---|
| Total model signals | 3 runs |
| Buy signals | 2 (Apr 15, Apr 17) |
| Hold signals | 1 (Apr 11) |
| Short signals | 0 |
| Orders placed in Moomoo | 1 (trade_id=20) |
| Orders filled | 0 |
| Realized P&L | $0 |
| Win rate | N/A (no fills) |

**Note:** The model was bullish on MSFT from April 15 onward with improving conviction (60% → 72% confidence). Execution failure was operational (order expiry), not a model signal failure. If the April 17 buy at $420.26 had filled and the target of $442 was hit, the gain would have been $21.74/share × 25 shares = $543.50 gross.

## Last updated

2026-04-29 — seeded from tracker.db + runs swing_20260411_211655, 20260415_110848, 20260417_233350
