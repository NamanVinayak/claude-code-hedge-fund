---
name: AMZN trades
last_updated: 2026-05-04
last_run_id: 20260504_173321
target_words: 800
stale_after_days: 60
word_count: 790
summary: All AMZN positions now closed — short from run 20260501_173921 stopped out at $276 on May 4 (-$7/share); HOLD decision from 20260504_173321 (no capital to deploy); 1 prior abandoned long; net lifetime realized P&L -$7.00
---

# AMZN — Trades

## TL;DR

All AMZN positions are closed as of May 4, 2026. The short from run 20260501_173921 (1 share, entered ~$265.86, stop $276) was stopped out on May 4 at $276.00, P&L -$7.00. Run 20260504_173321 issued a HOLD decision — no new position (portfolio cash $0, risk manager limit $0, allowed actions constrain to hold only). The bearish thesis direction remains intact per swing agents (2 bearish, 3 neutral/anti-bullish) but no capital to act. Net lifetime realized P&L: -$7.00 (1 closed short, 1 abandoned long at $0).

---

## Open positions

**No open AMZN positions.** [source: trade_ledger.json open_positions, run 20260504_173321]

---

## Closed trades — last 30 days

### Short — Run 20260501_173921 (Closed May 4, 2026) — STOP HIT

| Field | Value |
|---|---|
| Trade ID (primary ledger) | 115 |
| Direction | Short |
| Quantity | 1 share |
| Entry price (decision) | $269.00 |
| Entry fill price | $265.86 (ID 115) |
| Stop loss | $276.00 |
| Target | $244.44 (20-SMA / mean reversion) |
| Risk:Reward | 3.51:1 |
| Timeframe | 7–14 trading days |
| Confidence | 55 |
| Status | stop_hit |
| Entered | 2026-05-01 |
| Closed | 2026-05-04T14:48:00+00:00 |
| Exit fill price | $276.00 |
| Realized P&L | -$7.00 per share |
| Source run | 20260501_173921 |

**What happened:** The mean-reversion short thesis (April 30 shooting star on 2.05x volume, RSI 82/88, z-score 2.01) was entered with a $276 stop above the reversal swing high. On May 4, price rallied through $276 intraday, triggering the stop. The bullish absorption of the $268-276 distribution zone is a key lesson: ADX 64-65 (extreme trend strength) counteracted the overbought fade setup. The short was correctly sized (1 share) and the stop discipline held — loss was contained at -$7.00. [source: trade_ledger.json per_ticker_history[AMZN] ID 115, run 20260504_173321]

*Note: The ledger contains duplicate stop-hit records (IDs 115, 124, 130, 134) for the same underlying decision from run 20260501_173921. Per hard rule #11, ID 115 is treated as the canonical entry (earliest created_at 2026-05-01T17:55:57); duplicates are a system ingestion artifact and are not counted as separate trades.*

---

### Trade #24 — Long (Abandoned, no P&L)

| Field | Value |
|---|---|
| Direction | Long |
| Quantity | 35 shares |
| Status | Abandoned |
| Entry price (intended) | $249.70 |
| Exit fill price | None |
| Realized P&L | $0 |
| Source run | 20260417_233350 |

**What happened:** April 17 swing run produced a BUY at $249.70, target $262.00, stop $244.00. Limit order created but never filled. Marked abandoned April 29. The PM's $262 target was subsequently achieved by price — thesis was correct but order did not execute. [source: trades.md bootstrap]

---

## Model history across all runs

| Run ID | Date | Action | Entry | Target | Stop | R:R | Confidence | Result |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | Hold | $238.38 | $248.00 | $224.00 | 0.7:1 | 45% | No fill — R:R failed 2:1 |
| 20260415_110848 | 2026-04-15 | Buy | $246.00 | $263.00 | $238.50 | 2.27:1 | 72% | Not in ledger |
| 20260417_233350 | 2026-04-17 | Buy | $249.70 | $262.00 | $244.00 | 2.16:1 | 72% | Abandoned (Trade #24) |
| 20260501_173921 | 2026-05-01 | **Short** | $269.00 | $244.44 | $276.00 | 3.51:1 | 55% | Stop hit -$7.00 (ID 115) |
| 20260504_173321 | 2026-05-04 | **Hold** | N/A | N/A | N/A | N/A | 55% | No fill — no capital |

---

## Lifetime statistics

| Metric | Value |
|---|---|
| Total closed P&L trades | 1 (short, stop_hit) |
| Wins | 0 |
| Losses | 1 (stop hit, -$7.00) |
| Abandoned / no fill | 1 (long, #24) |
| Open positions | 0 |
| Win rate | 0% (0/1 closed P&L trade) |
| Total realized P&L | -$7.00 |
| Total unrealized P&L | $0 (no open positions) |
| Average confidence at entry | 55% (closed short) |
| Times model voted Buy | 2 of 5 runs |
| Times model voted Hold | 2 of 5 runs |
| Times model voted Short | 1 of 5 runs |

---

## Notes for position management

**Stop-out lesson:** ADX 65 strong trend absorbed the mean-reversion short at the $276 stop. The NVDA lesson (April 30, same RSI regime, stop hit) repeated in AMZN — fading extreme-trend stocks at overbought RSI carries elevated stop-out risk even with a textbook distribution candle. Two consecutive stop-outs at RSI 82-88 / ADX 60+ environments pattern-flag that the $265-276 zone may be distribution in progress, not breakout failure.

**Re-entry conditions:** Bearish — hourly RSI extreme (>75) + volume-confirmed rejection at $273-276. Bullish — pullback to 10 EMA zone at $258-261 with RSI normalized below 65 and constructive daily candle.

**Long re-entry after bearish resolve:** swing_trend_momentum and swing_macro_context identify $258-261 (10 EMA) as the ideal long re-entry zone. EMA-20 mean-reversion target zone: $247-$248. Monitor live SMA rather than fixed number.
