---
name: AMZN trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 802
summary: 1 trade in history — abandoned long from run 20260417_233350; model recommended buys in 3 runs, only 1 was executed; no closed P&L
---

# AMZN — Trades

## TL;DR

Amazon has one trade in tracker.db (trade ID 24), a long position placed from run 20260417_233350 that was subsequently abandoned — no fill was ever confirmed and the position was closed out administratively on April 29 2026. Net P&L on AMZN: $0 realized. The model was bullish on AMZN in all three runs analyzed; only one trade reached the execution stage, and that one was abandoned rather than filled. This page documents what happened, what the model intended, and what conditions the model wants for a proper re-entry.

---

## Open positions

None. As of April 29 2026, AMZN has no open position in tracker.db.

---

## Closed trades

### Trade #24 — Long (Abandoned, no P&L)

| Field | Value |
|---|---|
| Trade ID | 24 |
| Direction | Long |
| Quantity | 35 shares |
| Status | Abandoned |
| Entry price (intended) | $249.70 |
| Exit fill price | None |
| Realized P&L | None ($0) |
| Opened | 2026-04-18 00:18:19 UTC |
| Closed | 2026-04-29 11:19:51 UTC |
| Source run | 20260417_233350 |

**What happened:** The April 17 swing run (20260417_233350) produced a BUY signal for AMZN at $249.70 with a target of $262.00 and stop of $244.00, 2.16:1 risk-reward, 72% confidence. The executor created the trade record in tracker.db but the limit order was never confirmed as filled (exit_fill_price is null). The trade was eventually marked abandoned during the April 29 monitoring sweep — a standard outcome for limit orders that expire without triggering.

**Why the entry likely did not fill:** The model's April 17 entry at $249.70 was effectively at the market price of the time (AMZN had been trading near that level). Limit orders placed at the current market price depend on exact price action in the following sessions. If AMZN moved upward immediately and never pulled back to $249.70, the order would expire unfilled. Alternatively, if the order was placed as a limit at exactly $249.70 and the stock gapped up through that level, it would also miss. Without a confirmed fill record, the most likely explanation is that either the order lapsed at end of day or price action moved away from the entry level.

**Model reasoning at time of trade (run 20260417_233350):** "77 momentum rank, daily ADX 44, cloud rotation. Tighter 244 stop gives 2.16:1. Extreme Z-score 2.84 risk sizes down." The PM explicitly sized down from a full position because z-score 2.84 indicated AMZN was extended — the same caution flag that appeared in all three runs. The 35-share quantity at $249.70 implies ~$8,740 notional.

---

## Model history across all runs

This section captures every run where AMZN was analyzed, the model's verdict, and whether an order was placed.

| Run ID | Date | Action | Entry | Target | Stop | R:R | Confidence | Order placed? |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | Hold | $238.38 | $248.00 | $224.00 | 0.7:1 | 45% | No — R:R failed 2:1 |
| 20260415_110848 | 2026-04-15 | Buy | $246.00 | $263.00 | $238.50 | 2.27:1 | 72% | Unknown — not in tracker.db |
| 20260417_233350 | 2026-04-17 | Buy | $249.70 | $262.00 | $244.00 | 2.16:1 | 72% | Yes — Trade #24, abandoned |

**April 11 run — Hold (R:R failure):** AMZN surged 13.6% in five days to $238.38. The Head Trader was bullish at 60% but the R:R at current prices worked out to only 0.7:1 — badly below the 2:1 minimum. Z-score was 2.20, CCI hit 305, RSI was 75.3. The system correctly passed on this entry. Ideal pullback range identified: $220–$226.

**April 15 run — Buy recommended (no tracker.db record):** Four days later, with AMZN at $249 (up another ~4.5%), the Globalstar acquisition and 1.57x breakout volume flipped 6 of 9 agents bullish. The Head Trader called it the top-priority long in the basket. Entry was set at $246 (a small pullback from the $249 close). Despite the full buy recommendation at 72% confidence, there is no corresponding trade record in tracker.db, suggesting the executor step was not run or the order was not transmitted for this run.

**April 17 run — Buy → Trade #24 (abandoned):** Two days after the April 15 run, confidence held at 72%, momentum rank was 77, and ADX had risen to 44. The PM placed the trade. Z-score remained elevated at 2.84, which trimmed the size. The entry at $249.70 was essentially a limit at the market — and ultimately the order was abandoned.

---

## Lifetime statistics

| Metric | Value |
|---|---|
| Total trades | 1 |
| Wins | 0 |
| Losses | 0 |
| Abandoned / no fill | 1 |
| Win rate | N/A (no closed P&L trades) |
| Total realized P&L | $0.00 |
| Total unrealized P&L | $0.00 |
| Average holding period | N/A |
| Average confidence at entry | 72% |
| Times model voted Buy | 2 of 3 runs |
| Times model voted Hold | 1 of 3 runs (R:R failure) |
| Times model voted Short | 0 |

---

## Notes for next entry

The model has been consistent across all three runs: AMZN is a high-quality swing candidate when it pulls back from overbought extremes. The ideal entry window the system has identified across multiple runs is the **$220–$244 zone**, where z-score normalizes, RSI drops below 65, and ADX remains above 25. At those levels the R:R becomes 2.5:1 or better with a stop below hourly SuperTrend.

Watch for: pullback on earnings miss or profit-taking post-Q1 report (April 30 2026), FOMC-driven tech sector pressure, or any macro risk-off that compresses the QQQ (AMZN-QQQ correlation 0.67 per run 20260417_233350 portfolio notes). Any of those events creating a controlled pullback into the $230–$244 range would be the re-entry the system has been waiting for since April 11.
