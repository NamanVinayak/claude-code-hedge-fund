---
name: QQQ trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 872
summary: 1 closed trade (swing long, abandoned before fill); 1 daytrade no-trade decision; lifetime record 0W/0L/1 abandoned
---

# QQQ — Trades

## TL;DR

One trade attempted (swing long, April 18, 2026), never filled — abandoned before entry. One daytrade run (April 15) resulted in a deliberate no-trade sit-out with unanimous 9/9 neutral consensus. Lifetime P&L: $0. No wins, no losses. The model has been correct to stay disciplined on QQQ: the April 15 no-trade avoided a churn day with no clear intraday setup, and the April 18 swing long at $640.47 was abandoned before the position was established.

---

## Open positions

None. The one QQQ position was abandoned before fill on 2026-04-29 (closed_at in DB). No open exposure.

---

## Closed — last 30 days

### Trade #30 — Swing Long | ABANDONED (never filled)

| Field | Value | Source |
|---|---|---|
| Trade ID | 30 | tracker.db |
| Direction | Long | tracker.db |
| Status | Abandoned | tracker.db |
| Quantity | 12 shares | tracker.db |
| Entry price (model) | $640.47 | tracker.db / decisions.json, 20260417_233350 |
| Entry fill price | None (never filled) | tracker.db |
| Exit fill price | None | tracker.db |
| Realized P&L | $0 | tracker.db |
| Created at | 2026-04-18 00:18:19 UTC | tracker.db |
| Entered at | None | tracker.db |
| Closed at | 2026-04-29 11:19:51 UTC | tracker.db |

**Model reasoning (April 17 swing run):** "Tech-heavy uptrend, 83 sector confidence. Cut size — 0.96 corr with SPY and overlaps with single-name tech longs. 4.25:1 R:R." [Source: decisions.json, 20260417_233350]

**Target:** $668.00 | **Stop:** $634.00 | **R:R:** 4.25:1 | **Confidence:** 72% | **Timeframe:** 8–12 trading days

**Portfolio context at time of signal (April 17):** QQQ was one of 14 tickers analyzed in a 14-ticker swing run. The swing PM allocated only 12 shares (vs. a full allocation) specifically to avoid double-counting tech exposure — QQQ's 0.96 correlation with SPY and 0.74 correlation with NVDA meant a full-size QQQ position on top of AAPL, MSFT, NVDA, META, GOOGL, AMZN, AMD longs would have effectively levered the same sector bet. [Source: portfolio_notes, decisions.json, 20260417_233350]

**Why abandoned:** The order was placed (based on created_at 2026-04-18) but the entry at $640.47 was never filled before the position was abandoned on 2026-04-29. This is consistent with the Moomoo paper trading system's DAY order type — unfilled orders expire at end of day. The position was likely re-evaluated daily; if QQQ traded above $640.47 without filling, or if the model's conviction changed, the order would have been let lapse. No stop was ever triggered (entry_fill_price = None), so no capital was at risk.

---

## No-Trade Decision — Daytrade (April 15, 2026)

This was not a trade but a deliberate decision documented here for completeness.

| Field | Value | Source |
|---|---|---|
| Run ID | 20260415_104041 | metadata.json |
| Mode | Daytrade | metadata.json |
| Action | Hold (no trade) | decisions.json, 20260415_104041 |
| Confidence | 0% | decisions.json |
| DT agent consensus | 9/9 neutral | signals_combined.json |
| Intraday price at decision | $633.16 | decisions.json |
| R:R available | 0.0 (no valid setup) | decisions.json |

**Reasoning:** "9/9 unanimous neutral. Intraday SuperTrend bearish, squeeze momentum negative, MACD histogram negative. No setup meets the 1.5:1 risk-reward threshold. Sitting out is the correct call." [Source: decisions.json, 20260415_104041]

**Outcome:** This was the right call. The intraday structure on April 15 showed QQQ churning with sub-0.5x relative volume, a 5-minute SuperTrend providing overhead resistance at $633.70, and all momentum indicators muted. A forced trade would have had a near-zero edge.

---

## Closed — older, rolled by month

None. QQQ has no trade history prior to April 2026 in the tracker database.

---

## Closed — older than 6 months

None.

---

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades attempted | 1 (swing long, abandoned) |
| Total no-trade decisions | 1 (daytrade, Apr 15) |
| Wins | 0 |
| Losses | 0 |
| Abandoned/never filled | 1 |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 (no open position) |
| Win rate | N/A (no closed trades) |
| Average R:R on signals | 4.25:1 (swing) / 0:1 (daytrade) |
| Average model confidence | 72% (swing) / 0% (daytrade) |

**Notes:**
- QQQ's high correlation (0.96 vs SPY) means it will often be sized down or skipped when single-name tech is already in the book. This is correct portfolio behavior, not a bug.
- The abandoned status on Trade #30 is not a loss — the model was never at risk. It represents an order that was placed and lapsed unfilled. This is different from a stopped-out trade.
- Future QQQ trades are most likely to appear in daytrade mode (SPY/QQQ/IWM are the canonical daytrade universe) rather than swing mode, unless QQQ disconnects from SPY correlation meaningfully.

---

## Last updated

2026-04-29. Trade data sourced from tracker.db (query on Trade table, ticker='QQQ'). Model signals sourced from runs 20260415_104041 (daytrade) and 20260417_233350 (swing).
