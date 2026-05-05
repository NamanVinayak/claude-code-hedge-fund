---
name: META trades
last_updated: 2026-05-05
last_run_id: 20260505_140723
target_words: 800
stale_after_days: 60
word_count: 622
summary: 1 confirmed open short (id 118, 1 share, fill $611.78, stop $635, target $580, R/R 2.5:1); 2 prior longs closed/abandoned; net lifetime realized P&L approximately -$2.38; holding short from run 20260504_143030.
---

# META — Trades

## TL;DR

One open short position — trade id 118, 1 share filled at $611.78 on 2026-05-04 (entered at 14:48 UTC), stop $635, target $580, R/R 2.5:1. Tracking well: MFE +2.78%, MAE 0.0%. Decision run 20260505_140723: **hold**, no new entry (same-direction stacking blocked, remaining position limit 0). Two prior long trades are fully closed/abandoned. (source: trade_ledger.json per_ticker_history[META] id 118, run 20260505_140723)

## Open positions

### Trade ID 118 — Short, Entered (Run: 20260504_143030)

| Field | Value |
|---|---|
| Trade ID | 118 |
| Direction | Short |
| Quantity | 1 share |
| Status | Entered (open) |
| Entry price (model) | $621.00 (limit on bounce) |
| Entry fill price | $611.78 |
| Entry tolerance | 1.5% |
| Stop loss | $635.00 |
| Target price | $575.00 (original) / $580.00 (PM adjusted, run 20260505_140723) |
| R/R ratio | 3.3:1 (original) / 2.5:1 from fill |
| Confidence | 62% (entry run) / 58% (current hold run) |
| Timeframe | 5–12 trading days |
| Created at | 2026-05-04T14:46:00+00:00 |
| Entered at | 2026-05-04T14:48:00+00:00 |
| MFE / MAE | +2.78% / 0.0% |

**Model thesis at entry (run 20260504_143030):** Post-earnings capex-shock breakdown ($669→$600, 3.26x avg vol Apr 30) confirmed structural re-rating. Head Trader bearish 62 conf. Conditional short at $619–628 resistance (Fib 38.2% + former support) with bearish rejection candle. Daily ADX 49.52 with -DI 34.25 >> +DI 26.06; hourly ADX 50.9 with -DI 47.79 >> +DI 7.66 — extreme bearish trend. Risk-off macro (Iran escalation May 4, Fed hawkish succession risk). R/R 3.3:1 from $621 entry. (source: trade_ledger.json raw_decision, id 118)

**Current status (run 20260505_140723):** Holding. Price ~$604.55, fill was $611.78, MFE +2.78%, MAE 0.0%. PM decision: hold with stop $635, target $580, R/R 2.5:1. ADX now 50.73 (strengthened bearish trend). 4/5 swing agents directionally bearish. (source: decisions.json, run 20260505_140723)

---

## Closed / Abandoned trades

### Trade ID 16 — Long, Filled and Abandoned (Run: 20260415_093758)

| Field | Value |
|---|---|
| Trade ID | 16 |
| Direction | Long |
| Quantity | 1 share |
| Status | Abandoned (closed) |
| Entry fill price | $673.72 |
| Exit fill price | $671.34 |
| P&L | ~-$2.38 |
| Closed at | 2026-04-29T11:19:51 |

**What happened:** Pre-earnings risk-off exit on April 29. Q1 2026 earnings capex shock (Apr 29 AH) fully validated the exit — stock dropped ~$70 the next day. (source: trades.md bootstrap, run 20260415_093758)

---

### Trade ID 22 — Long, Never Filled (Run: 20260417_233350)

| Field | Value |
|---|---|
| Trade ID | 22 |
| Direction | Long |
| Quantity | 15 shares (phantom budget era — sizing bug) |
| Status | Abandoned, never filled |
| Entry fill price | None |
| P&L | None |
| Closed at | 2026-04-29T11:19:51 |

**What happened:** After-hours order placement; limit at $676.87 likely gapped above on open. Sizing was from phantom $100K budget bug (fixed commit b2b472d). (source: trades.md bootstrap, run 20260417_233350)

---

## Lifetime stats (META, all trades per trade_ledger.json)

| Metric | Value |
|---|---|
| Total trades in ledger | 3 (id 16, id 22, id 118) |
| Open positions | 1 (id 118 — short) |
| Filled and closed | 1 (id 16 — long, ~-$2.38) |
| Unfilled/abandoned | 1 (id 22 — long, no P&L) |
| Realized P&L | ~-$2.38 (id 16 only) |
| Unrealized P&L | ~+$7.23 (id 118: 1 share × ($611.78 − $604.55)) |
| Win rate (closed) | 0% (1 closed, 0 wins) |
| Directions traded | Long (id 16, 22), Short (id 118) |
| First short ever | id 118 (run 20260504_143030) |

(source: trade_ledger.json per_ticker_history[META], run 20260505_140723)
