---
name: GOOG trades
last_updated: 2026-05-07
last_run_id: 20260506_164526
target_words: 800
stale_after_days: 60
word_count: 657
summary: 3 total GOOG trades in ledger — id 149 (short 1 share, stopped out May 6, -$6.50 realized); id 14 (long 3 shares, abandoned, P&L null); id 7 (long 3 shares, never filled, abandoned). Net confirmed realized P&L: -$6.50. No open GOOG positions.
---

# GOOG — Trades

## TL;DR

Three GOOG trades on record. The only confirmed realized P&L trade is id 149 — a mean-reversion short (1 share at $383.00, stopped out $389.50 on May 6, 2026) for a loss of −$6.50. Two prior bootstrapped trades (id 14 and id 7) are classified as abandoned with NULL P&L. No open GOOG positions as of run 20260506_164526. (Source: trade_ledger.json per_ticker_history[GOOG], run 20260506_164526)

---

## Open positions

None. No open GOOG positions confirmed in trade_ledger.json as of run 20260506_164526.

---

## Recently Closed

### Trade: SHORT 1 share GOOG — CLOSED 2026-05-06

| Field | Value |
|---|---|
| Entry price | $383.00 |
| Exit price | $389.50 |
| P&L | -$6.50 |
| Closed via | stop_hit |
| Days held | 1 (2026-05-05 → 2026-05-06) |
| Run | `20260505_164543` |

---

## Closed — last 30 days

### Trade id 149 — Short 1 share at $383.00 (May 5, 2026) — STOPPED OUT

**Model decision source:** run 20260505_164543 (swing mode)

| Field | Value |
|---|---|
| Trade ID | 149 |
| Direction | Short |
| Quantity | 1 share |
| Entry fill price | $383.00 |
| Target | $338.95 |
| Stop loss | $389.50 |
| Exit fill price | $389.50 (stop hit) |
| Realized P&L | −$6.50 |
| Risk/Reward (model) | 4.32:1 |
| Confidence | 40% |
| Status | stop_hit |
| Entered at | 2026-05-05T13:30:00+00:00 |
| Closed at | 2026-05-06T13:31:00+00:00 |
| Hold duration | ~1 trading day |
| Run ID | 20260505_164543 |

**Model rationale (from raw_decision):** Mean-reversion Branch A: Z-score 2.56, RSI-7 90.69, Bollinger %B 0.963, hourly $384.16 resistance (13 tests). Head trader conf 35 but R/R 4.32:1 cleared exceptional threshold. 1 share within risk mgr $600 cap. Portfolio was 2 short / 2 long. Valuation bearish (DCF gap −75%).

**Outcome:** Stop hit at $389.50 on May 6. The hourly $384.16 resistance ceiling (16 tests) was broken to the upside. ADX continued to intensify to 74.23 — extreme trend regime absorbed the mean-reversion fade, consistent with NVDA (Apr 30, −$63.20) and AMZN (May 4, −$10.14) lessons. Thesis falsification clause triggered: "price breaks cleanly above $389.50 stop." (Source: trade_ledger.json per_ticker_history[GOOG] id 149, recent_closures_30d, run 20260506_164526)

---

## Closed trades — historical (bootstrapped)

### Trade id 14 — Long 3 shares at $331.73 (April 15, 2026) — Abandoned

| Field | Value |
|---|---|
| Trade ID | 14 |
| Direction | Long |
| Quantity | 3 shares |
| Entry fill price | $331.73 |
| Target | $347.50 |
| Stop loss | $318.00 |
| Exit fill recorded | $347.50 (DB field only) |
| Realized P&L | NULL (database gap — P&L not computed) |
| Status | Abandoned |
| Entered at | 2026-04-15T17:14:47 |
| Closed at | 2026-04-29T11:19:51 |

**Note:** Exit fill field shows $347.50 (exact model target) but P&L is NULL — likely auto-populated target field, not confirmed Moomoo execution. If real, gross P&L would be +$47.31 on a $995.19 position (+4.75%). Unconfirmed. (Source: bootstrap, run bootstrap)

### Trade id 7 — Long 3 shares at $315.00 (April 14, 2026) — Never filled

| Field | Value |
|---|---|
| Trade ID | 7 |
| Direction | Long |
| Entry price | $315.00 (limit, never filled) |
| Realized P&L | NULL |
| Status | Abandoned (2026-04-29T11:19:51) |

**Note:** Limit order placed at $315 ahead of the April 14–15 breakout. GOOG rallied through $315 without pulling back, leaving the order unfilled. Superseded by Trade #14. Net impact: $0. (Source: bootstrap, run bootstrap)

---

## Lifetime stats

| Metric | Value | Notes |
|---|---|---|
| Total GOOG trades in ledger | 3 | IDs: 149, 14, 7 |
| Filled trades | 2 | id 149 (confirmed fill + stop); id 14 (fill recorded, exit unconfirmed) |
| Unfilled / abandoned | 1 | id 7 |
| Confirmed realized P&L | −$6.50 | id 149 stop_hit (trade_ledger.json) |
| Unconfirmed P&L (id 14 if exit real) | +$47.31 | Needs DB reconciliation |
| Net confirmed P&L | −$6.50 | id 149 only |
| Win rate (confirmed closes) | 0% (0W / 1L) | id 149 stop_hit |
| Mode | Swing | All entries |
| Last closed | 2026-05-06 | id 149 |

---

## Last updated

Sources: trade_ledger.json per_ticker_history[GOOG] (run 20260506_164526). id 149 confirmed stopped out at $389.50 (−$6.50) on 2026-05-06. No open GOOG positions. Next potential entry: pullback to $375–$385 or May 14–15 I/O pre-positioning window per decisions.json run 20260506_164526.
