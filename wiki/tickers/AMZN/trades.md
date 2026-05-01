---
name: AMZN trades
last_updated: 2026-05-01
last_run_id: 20260501_173921
target_words: 800
stale_after_days: 60
word_count: 793
summary: 1 open short position (1 share at $269, run 20260501_173921); 1 prior abandoned long (no fill); model voted short for first time after Q1 earnings "sell the news" reversal
---

# AMZN — Trades

## TL;DR

Amazon has one new open position: a short entered at ~$269 per share (1 share) from run 20260501_173921, stop $276, target $244.44, R:R 3.51:1, confidence 55. This is the first short signal ever generated for AMZN in run history (all prior runs were bullish or hold). Prior closed history: one abandoned long (Trade #24, no fill, no P&L). Net lifetime realized P&L remains $0.

---

## Open positions

### Short — Run 20260501_173921 (May 1, 2026)

| Field | Value |
|---|---|
| Direction | Short |
| Quantity | 1 share |
| Entry price | ~$269.00 |
| Entry tolerance | ±2.0% ($263.38–$274.38) |
| Stop loss | $276.00 (above reversal swing high $273.88 + buffer) |
| Target | $244.44 (20-SMA / mean reversion anchor) |
| Risk:Reward | 3.51:1 |
| Timeframe | 7–14 trading days |
| Confidence | 55 |
| Status | Open (pending fill confirmation) |
| Source run | 20260501_173921 |

**Thesis:** "Sell the news" shooting star on April 30 — gap to $273.88, close $265.06 on 2.05x volume. RSI 82/88, z-score 2.01, 18.58% above 50-SMA. Zero bullish swing votes. Mean-reversion Branch A fires — target 20-SMA $244.44. Stop above confirmed reversal high. Confidence dialed to 55 (from head trader 62) on ADX 64 strong-trend risk and NVDA lesson (same RSI regime, stop hit -$63.20). Risk manager limit $508; 1 share @ $269 = $269 within limit. [source: decisions.json, run 20260501_173921]

---

## Closed trades — last 30 days

### Trade #24 — Long (Abandoned, no P&L)

| Field | Value |
|---|---|
| Trade ID | 24 |
| Direction | Long |
| Quantity | 35 shares |
| Status | Abandoned |
| Entry price (intended) | $249.70 |
| Exit fill price | None |
| Realized P&L | $0 |
| Opened | 2026-04-18 00:18:19 UTC |
| Closed | 2026-04-29 11:19:51 UTC |
| Source run | 20260417_233350 |

**What happened:** April 17 swing run produced a BUY at $249.70, target $262.00, stop $244.00, 2.16:1 R:R, 72% confidence. Limit order was created in tracker.db but never confirmed as filled. Marked abandoned during April 29 monitoring sweep. The PM's $262 target was subsequently achieved by price action in the following weeks — the trade thesis was correct but the limit order did not execute. [source: trades.md bootstrap, run bootstrap]

---

## Model history across all runs

| Run ID | Date | Action | Entry | Target | Stop | R:R | Confidence | Order placed? |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | Hold | $238.38 | $248.00 | $224.00 | 0.7:1 | 45% | No — R:R failed 2:1 |
| 20260415_110848 | 2026-04-15 | Buy | $246.00 | $263.00 | $238.50 | 2.27:1 | 72% | Unknown — not in tracker.db |
| 20260417_233350 | 2026-04-17 | Buy | $249.70 | $262.00 | $244.00 | 2.16:1 | 72% | Yes — Trade #24, abandoned |
| 20260501_173921 | 2026-05-01 | **Short** | $269.00 | $244.44 | $276.00 | 3.51:1 | 55% | Yes — open position |

**First short in AMZN history.** All prior runs voted bullish (2× buy, 1× hold due to R:R failure). The Q1 2026 earnings "sell the news" reversal on April 30 is what flipped the model. Note: the April 17 buy target of $262 was achieved in the interim — the prior long thesis played out as intended even though Trade #24 was never filled.

---

## Lifetime statistics

| Metric | Value |
|---|---|
| Total trades | 2 (1 abandoned, 1 open) |
| Wins | 0 |
| Losses | 0 |
| Abandoned / no fill | 1 |
| Open positions | 1 (short, run 20260501_173921) |
| Win rate | N/A (no closed P&L trades) |
| Total realized P&L | $0.00 |
| Total unrealized P&L | TBD (short at ~$269, mark-to-market on fill) |
| Average confidence at entry | 63.5% (weighted: 72% abandoned long, 55% open short) |
| Times model voted Buy | 2 of 4 runs |
| Times model voted Hold | 1 of 4 runs (R:R failure) |
| Times model voted Short | 1 of 4 runs (this run — first time) |

---

## Notes for position management

**Stop discipline:** The NVDA lesson (April 30, -$63.20, same RSI 81–87 regime) is directly applicable. If price recaptures $273.88 on volume, the reversal hypothesis is invalidated — exit at $276 stop no questions asked.

**Target path:** 20-SMA is currently at $244.44. As days pass and the SMA moves up, the target will drift higher — monitor the live SMA rather than the fixed $244 number.

**Long re-entry after short covers:** swing_trend_momentum and swing_macro_context both identified $252–$258 as the ideal long re-entry zone. If the short plays out to the $244–$252 range, that becomes the buy signal — particularly if RSI normalizes below 65 and a constructive daily candle forms.
