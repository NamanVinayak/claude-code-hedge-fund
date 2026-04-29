---
name: GOOG trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 812
summary: 2 total GOOG trades in tracker.db — 1 filled and abandoned, 1 unfilled and abandoned. No closed P&L recorded. Net lifetime result: $0 realized.
---

# GOOG — Trades

## TL;DR

Two GOOG trades exist in tracker.db. Trade #14 (April 15, 2026) was the only one with a fill: 3 shares entered at $331.73, target $347.50, stop $318. The position was marked "abandoned" on April 29, 2026 with exit_fill_price $347.50 recorded but pnl=NULL in the database — the exit fill field appears to have been set without a corresponding P&L calculation. Trade #7 (April 14, 2026) was placed at $315 and never filled before being abandoned. Net realized P&L in the DB: $0 (pnl field is NULL on both rows). The model's confidence on both entries was 60%.

---

## Open positions

None. Both GOOG trades are in status "abandoned" as of 2026-04-29.

---

## Closed trades — full log

### Trade #14 — Long 3 shares at $331.73 (April 15, 2026)

**Model decision source:** run 20260415_093758 (swing mode)

| Field | Value |
|---|---|
| Trade ID | 14 |
| Direction | Long |
| Quantity | 3 shares |
| Model entry price | $332.06 |
| Actual entry fill | $331.73 |
| Target | $347.50 |
| Stop loss (model) | $318.00 |
| Exit fill recorded | $347.50 |
| Realized P&L | NULL (database gap) |
| Status | Abandoned |
| Entered at | 2026-04-15 17:14:47 |
| Closed at | 2026-04-29 11:19:51 |
| Hold duration | ~14 calendar days |

**Model rationale (from 20260415_093758 decisions.json):** "7/10 strategies bullish; clean breakout above $330.58 with daily ADX 37 and hourly ADX 80; Google Cloud AI partnership catalyst." Confidence: 60%. Risk/reward: 2.08.

**Technical setup at entry:** GOOG had broken above daily resistance at $330.58 on April 14. The model entered on confirmation at $332.06 (filled at $331.73 — slippage of $0.33, favorable). Momentum indicators were strongly bullish: daily MACD histogram +4.87 (highest in the basket), squeeze firing bullish, supertrend bullish on both daily and hourly timeframes. The primary risk acknowledged at entry was simultaneous overbought readings on both timeframes (daily RSI 77, hourly RSI 82), which increased pullback probability.

**Outcome note:** The exit_fill_price field in the DB shows $347.50, which equals the exact model target. This may reflect the target being auto-filled rather than a confirmed Moomoo execution — pnl is NULL, which is unusual for a completed trade. If the exit was real at $347.50, gross P&L would be: (347.50 - 331.73) x 3 = **+$47.31** on a $995.19 position (+4.75%). This is unconfirmed pending DB reconciliation.

---

### Trade #7 — Long 3 shares at $315.00 (April 14, 2026) — Never filled

**Model decision source:** Implied from earlier swing run context (entry placed April 14, 2026)

| Field | Value |
|---|---|
| Trade ID | 7 |
| Direction | Long |
| Quantity | 3 shares |
| Model entry price | $315.00 |
| Actual entry fill | None (no fill) |
| Target | Not recorded |
| Stop loss | Not recorded |
| Exit fill | None |
| Realized P&L | NULL |
| Status | Abandoned |
| Created at | 2026-04-14 08:45:51 |
| Entered at | Never |
| Closed at | 2026-04-29 11:19:51 |

**Context:** This order was placed at $315 ahead of the April 14–15 breakout. GOOG was trading at ~$313 in the swing_20260411 run (target $330, hold due to 1.3:1 R:R at that level). The $315 entry appears to be a limit order that the model placed but the stock never pulled back to fill — instead, GOOG rallied directly through $315 and broke out above $330.58. The unfilled order was then abandoned and superseded by Trade #14. Net impact: $0 (no capital deployed).

---

## Lifetime stats

| Metric | Value | Notes |
|---|---|---|
| Total GOOG trades in DB | 2 | IDs: 14, 7 |
| Filled trades | 1 | Trade #14 |
| Unfilled / abandoned | 1 | Trade #7 |
| Confirmed realized P&L | $0 | pnl=NULL in DB for both rows |
| Unconfirmed P&L (if #14 exit real) | +$47.31 | Needs DB reconciliation |
| Model confidence average | 60% | Both runs |
| Mode | Swing | Both entries |
| Entry accuracy | 1/1 filled | Trade #14 filled within $0.33 of model price |
| Win rate (confirmed closes) | N/A | No confirmed P&L yet |

---

## Data quality notes

1. **pnl=NULL anomaly:** Trade #14 has exit_fill_price=$347.50 (the exact model target) but pnl is NULL. The monitor or executor likely wrote the exit fill field without running the P&L calculation step. To fix: `UPDATE trade SET pnl = (exit_fill_price - entry_fill_price) * quantity WHERE id = 14` — but verify the exit was a real Moomoo fill first.

2. **Trade #7 entry price context:** The $315 limit was set when GOOG was at ~$313 (swing_20260411_211655 run, April 11 data). The stock gapped through this level on the April 15 breakout without pulling back, leaving the order unfilled. This is a known pattern when the model places limit entries below market in anticipation of a pullback that does not materialize.

3. **Both statuses show "abandoned":** The mass-abandon event on 2026-04-29 11:19:51 closed both trades simultaneously, suggesting a batch cleanup operation rather than individual position management. This is consistent with the tracker monitor running a periodic expiry sweep.

---

## Last updated

Data pulled from tracker.db on 2026-04-29 using: `s.query(Trade).filter(Trade.ticker == 'GOOG').order_by(Trade.created_at.desc())`. Bootstrap date: 2026-04-29.
