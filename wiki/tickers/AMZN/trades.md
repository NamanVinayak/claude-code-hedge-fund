---
name: AMZN trades
last_updated: 2026-05-05
last_run_id: 20260505_173521
target_words: 800
stale_after_days: 60
word_count: 785
summary: All AMZN positions closed — short ID 115 stopped out at $276 on May 4 (-$10.14); runs 20260504_173321 and 20260505_173521 both HOLD (no valid entry setup); 1 prior abandoned long; net lifetime realized P&L -$10.14; capital now available but entry conditions not met
---

# AMZN — Trades

## TL;DR

All AMZN positions are closed as of May 4, 2026. The short from run 20260501_173921 (1 share, entered at $265.86 fill, stop $276) was stopped out on May 4 at $276.00, P&L -$10.14 (ID 115, trade_ledger.json per_ticker_history[AMZN]). Run 20260504_173321 issued HOLD — no capital available at that time. Run 20260505_173521 also issued HOLD — capital is now available ($1,617.76 cash, short allowed) but no valid entry setup exists (all 5 swing agents neutral, unanimous). Net lifetime realized P&L: -$10.14 (1 closed short, 1 abandoned long at $0).

---

## Open positions

**No open AMZN positions.** [source: trade_ledger.json open_positions, per_ticker_history[AMZN], run 20260505_173521]

---

## Closed trades — last 30 days

### Short — Run 20260501_173921 (Closed May 4, 2026) — STOP HIT

| Field | Value |
|---|---|
| Trade ID (primary ledger) | 115 |
| Direction | Short |
| Quantity | 1 share |
| Entry price (decision) | $269.00 |
| Entry fill price | $265.86 (entry_fill_price, ID 115) |
| Stop loss | $276.00 |
| Target | $244.44 (20-SMA / mean reversion) |
| Risk:Reward | 3.51:1 |
| Timeframe | 7–14 trading days |
| Confidence | 55 |
| Status | stop_hit |
| Entered | 2026-05-01T13:30:00 |
| Closed | 2026-05-04T14:48:00+00:00 |
| Exit fill price | $276.00 |
| Realized P&L | -$10.14 |
| Source run | 20260501_173921 |

**What happened:** The mean-reversion short thesis (April 30 shooting star on 2.05x volume, RSI 82/88, z-score 2.01) was entered with a $276 stop above the reversal swing high. On May 4, price rallied through $276 intraday, triggering the stop. The bullish absorption of the $268-276 distribution zone is the key lesson: ADX 64-65 (extreme trend strength) counteracted the overbought fade setup. Short correctly sized at 1 share; loss contained to -$10.14. [source: trade_ledger.json per_ticker_history[AMZN] ID 115, run 20260504_173321]

*Note: The P&L of -$10.14 is calculated as (entry fill $265.86 - exit $276.00) × 1 share = -$10.14. The decision entry price was $269.00; the actual fill was $265.86 per the ledger. The trade_ledger.json per_ticker_history[AMZN] contains one record (ID 115). Any additional stop_hit records for the same underlying AMZN decision from run 20260501_173921 are ingestion artifacts; ID 115 is the canonical entry (earliest created_at 2026-05-01T17:55:57).*

---

### Trade — Long (Abandoned, no P&L)

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
| 20260417_233350 | 2026-04-17 | Buy | $249.70 | $262.00 | $244.00 | 2.16:1 | 72% | Abandoned (no fill) |
| 20260501_173921 | 2026-05-01 | **Short** | $269.00 | $244.44 | $276.00 | 3.51:1 | 55% | Stop hit -$10.14 (ID 115) |
| 20260504_173321 | 2026-05-04 | **Hold** | N/A | N/A | N/A | N/A | 55% | No fill — no capital at time |
| 20260505_173521 | 2026-05-05 | **Hold** | N/A | N/A | N/A | N/A | 52% | No fill — no valid entry setup |

---

## Lifetime statistics

| Metric | Value |
|---|---|
| Total closed P&L trades | 1 (short, stop_hit) |
| Wins | 0 |
| Losses | 1 (stop hit, -$10.14) |
| Abandoned / no fill | 1 (long, no P&L) |
| Open positions | 0 |
| Win rate | 0% (0/1 closed P&L trade) |
| Total realized P&L | -$10.14 |
| Total unrealized P&L | $0 (no open positions) |
| Average confidence at entry | 55% (closed short only) |
| Times model voted Buy | 2 of 6 runs |
| Times model voted Hold | 3 of 6 runs |
| Times model voted Short | 1 of 6 runs |

---

## Notes for position management

**Stop-out lesson (ADX / RSI regime):** ADX 65 strong trend absorbed the mean-reversion short at the $276 stop. The NVDA lesson (April 30, same RSI regime, stop hit -$63.20) repeated in AMZN — fading extreme-trend stocks at overbought RSI carries elevated stop-out risk even with a textbook distribution candle. Two consecutive stop-outs at RSI 80-90 / ADX 60-65 environments set a higher confirmation bar for any new position.

**Re-entry conditions (short):** Hourly RSI-21 >75 PLUS volume-confirmed rejection candle at $273-276. Both conditions must fire simultaneously — current reading (hourly RSI-21 67.45, relative volume 0.04x) fails both gates.

**Re-entry conditions (long pullback):** Price retreats to 10 EMA zone $258-265, RSI normalizes below 65, constructive daily candle on rising ADX. Entry ~$262, target $284.65, stop $256, R/R ~3.5:1.

**Breakout long:** Confirmed daily close above $276 on 1.5x+ volume. Entry ~$276.50, measured move target $296, stop $268, R/R ~2.3:1.
