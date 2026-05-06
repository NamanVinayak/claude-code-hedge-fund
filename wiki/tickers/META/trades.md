---
name: META trades
last_updated: 2026-05-06
last_run_id: 20260506_140335
target_words: 800
stale_after_days: 60
word_count: 648
summary: Cover decision issued for short id 118 (fill $611.78, cover at ~$604.96, ~$6.82 gain; ledger status still "entered" — exit fill not yet confirmed in trade_ledger.json); 2 prior longs closed/abandoned; net lifetime realized P&L approximately -$2.38 (id 16 only); cover fill pending confirmation.
---

# META — Trades

## TL;DR

Cover decision issued for trade id 118 (run 20260506_140335, 55% confidence) — PM instructed closing the 1-share short at ~$604.96, locking in approximately **$6.82/share gain** from fill $611.78. However, the ledger (`trade_ledger.json`) still shows id 118 with status "entered" and no `exit_fill_price` — the exit fill is not yet confirmed. Per hard rule #11, this trade is NOT yet recorded as closed. Two prior long trades remain fully closed/abandoned. (source: trade_ledger.json per_ticker_history[META] id 118, decisions.json, run 20260506_140335)

## Open positions (per trade_ledger.json — exit fill not yet confirmed)

### Trade ID 118 — Short, Entered / Cover Decision Pending (Run: 20260504_143030)

| Field | Value |
|---|---|
| Trade ID | 118 |
| Direction | Short |
| Quantity | 1 share |
| Status | Entered (open in ledger) — cover decision issued run 20260506_140335 |
| Entry price (model) | $621.00 (limit on bounce) |
| Entry fill price | $611.78 |
| Entry tolerance | 1.5% |
| Stop loss | $635.00 |
| Target price | $575.00 (original) / $580.00 (PM adjusted, run 20260505_140723) |
| Cover decision price | ~$604.96 (run 20260506_140335) |
| Expected gain (if filled) | ~$6.82/share |
| R/R ratio | 3.3:1 (original) / 0.17:1 remaining from current levels |
| Confidence | 62% (entry run) / 55% (cover run) |
| Timeframe | 5–12 trading days |
| Created at | 2026-05-04T14:46:00+00:00 |
| Entered at | 2026-05-04T14:48:00+00:00 |
| MFE / MAE | ~+1.11% / 0.0% (as of cover decision) |

**Model thesis at entry (run 20260504_143030):** Post-earnings capex-shock breakdown ($669→$600, 3.26x avg vol Apr 30) confirmed structural re-rating. Head Trader bearish 62 conf. Conditional short at $619–628 resistance (Fib 38.2% + former support) with bearish rejection candle. Daily ADX 49.52 with -DI 34.25 >> +DI 26.06; hourly ADX 50.9 with -DI 47.79 >> +DI 7.66 — extreme bearish trend. Risk-off macro (Iran escalation May 4, Fed hawkish succession risk). R/R 3.3:1 from $621 entry. (source: trade_ledger.json raw_decision, id 118)

**Cover decision (run 20260506_140335, 55% conf):** RSI-7 collapsed to 6.52 (extreme oversold), bullish RSI divergence confirmed on both daily and hourly timeframes, hourly OBV diverging bullishly from price — elevated mean-reversion bounce risk. R/R from $604.96 to target $580 only $4.96 vs. $30 adverse risk to $635 stop = 0.17:1, deeply unfavorable. Head trader voted hold but allowed_actions only permits cover (hold=0, cover=1). PM decision: cover and re-enter on failed bounce to $612–614 resistance zone. Re-entry: short at $612–614, stop above $621, target $580–585 (Fib 61.8% at $585.68). (source: decisions.json, signals_combined.json, run 20260506_140335)

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
| Open positions (ledger) | 1 (id 118 — short; cover decision issued, exit fill unconfirmed) |
| Filled and closed | 1 (id 16 — long, ~-$2.38) |
| Unfilled/abandoned | 1 (id 22 — long, no P&L) |
| Realized P&L | ~-$2.38 (id 16 only) |
| Unrealized P&L (if cover fills) | ~+$6.82 (id 118: 1 share × ($611.78 − $604.96)) |
| Win rate (closed) | 0% (1 closed, 0 wins) |
| Directions traded | Long (id 16, 22), Short (id 118) |
| First short ever | id 118 (run 20260504_143030) |

Note: id 118 exit fill not yet in ledger as of run 20260506_140335. Stats will update when cover fill is confirmed in trade_ledger.json per_ticker_history[META].

(source: trade_ledger.json per_ticker_history[META], run 20260506_140335)
