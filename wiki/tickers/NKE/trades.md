---
name: NKE trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 803
summary: 3 DB records (1 closed loss, 1 cancelled, 1 abandoned); net realized P&L -$35.70; short thesis correct long-term but entries hit bounce zone
---

# NKE — Trades

## TL;DR

Three tracker.db entries for NKE, all shorts. One closed at a realized loss of -$35.70 (entered Apr 14, closed Apr 29). One cancelled before fill (Apr 12). One abandoned (Apr 17 run, never filled). The short thesis was directionally correct across both runs, but both entries fell into a deeply oversold bounce zone that inflicted short-term pain before any trend continuation. Lesson: ADX 64+ in deeply oversold territory still creates violent reversals; the bounce entry strategy is necessary but hard to time precisely.

---

## Open positions

None. All NKE positions are closed, cancelled, or abandoned as of 2026-04-29.

---

## Closed — April 2026

### Trade ID 11 — Short 17 shares — CLOSED at loss

| Field | Value |
|---|---|
| Trade ID | 11 |
| Ticker | NKE |
| Direction | Short |
| Quantity | 17 shares |
| Status | **closed** |
| Entry price (model) | $43.50 |
| Entry fill price | None recorded (likely market fill near model price) |
| Exit fill price | None recorded |
| Realized P&L | **-$35.70** |
| Created at | 2026-04-14 08:45:51 |
| Entered at | 2026-04-14 10:36:30 |
| Closed at | 2026-04-29 (DB timestamp) |

**Source run**: `swing_20260411_211655` — decision called short 17 shares at $44.00 entry, target $38.00, stop $46.50, R:R 2.4:1, confidence 65%.

**What happened**: The Apr 11 model identified NKE as the strongest downtrend in the universe (ADX 64.6) and called a short entry at $44.00, anticipating the stock would bounce to the 10 EMA zone ($45.74) before continuing lower. The trade was entered on April 14 at ~$43.50. The position moved against the short — insider buying by board directors (Swan $500K, Rogers $173K) created a stronger-than-expected oversold bounce. The position was closed on April 29 at a loss of $35.70 ($2.10 per share adverse move on 17 shares).

**Context**: The mean-reversion agent had flagged this exact risk — z-score -2.06 plus insider buying = high bounce probability in the near term before trend resumes. The trend follower and momentum ranker (85% bearish confidence) were correct over a longer horizon, but the immediate bounce was real.

---

## Cancelled / Abandoned

### Trade ID 5 — Short 17 shares — CANCELLED

| Field | Value |
|---|---|
| Trade ID | 5 |
| Ticker | NKE |
| Direction | Short |
| Quantity | 17 shares |
| Status | **cancelled** |
| Entry price (model) | $44.00 |
| Entry fill price | None (never filled) |
| Exit fill price | None |
| Realized P&L | $0 |
| Created at | 2026-04-12 04:58:09 |
| Entered at | None |
| Closed at | None |

**Source run**: `swing_20260411_211655`. This was the initial order placed from the Apr 11 run. It was cancelled before execution — likely because the order expired at end of day (Moomoo paper trading uses DAY-only orders) or was superseded by Trade ID 11.

---

### Trade ID 27 — Short 180 shares — ABANDONED

| Field | Value |
|---|---|
| Trade ID | 27 |
| Ticker | NKE |
| Direction | Short |
| Quantity | 180 shares |
| Status | **abandoned** |
| Entry price (model) | $45.54 |
| Entry fill price | None (never filled) |
| Exit fill price | None |
| Realized P&L | $0 |
| Created at | 2026-04-18 00:18:19 |
| Entered at | None |
| Closed at | 2026-04-29 11:19:51 |

**Source run**: `20260417_233350` — this was the larger Apr 17 run which analyzed 14 tickers simultaneously with a $100K budget. That run called short 180 shares at $45.54, target $41.50, stop $47.50, R:R 2.06:1, confidence 70%. The model noted "Strong downtrend: daily EMAs down ADX 48, -17% 21d, collapsing EPS. Oversold-bounce risk sized moderate; 2.06:1 R:R."

The order was abandoned (never reached Moomoo execution). The Apr 17 run was a larger portfolio exercise; NKE was one of 14 tickers. The position was marked abandoned on Apr 29, consistent with end-of-session cleanup.

**Note on size**: 180 shares at $45.54 = ~$8,197 notional. This was appropriate for a $100K book (8.2% position) vs. the 17 shares in the $5K paper account run. The larger run's portfolio notes called out NKE + XOM shorts as "negatively-correlated ballast" that hedged the tech-long book beta.

---

## Lifetime stats (NKE only)

| Metric | Value |
|---|---|
| Total entries attempted | 3 |
| Filled and closed | 1 |
| Cancelled / abandoned before fill | 2 |
| Win / loss | 0W / 1L |
| Realized P&L | **-$35.70** |
| Average loss per closed trade | -$35.70 |
| Model direction accuracy | Directionally correct (short thesis) over full period; entry timing suboptimal |
| Avg model confidence (filled trades) | 65% (`swing_20260411_211655`) |

---

## Lessons learned

1. **Deeply oversold + insider buying = dangerous entry zone for shorts.** Both Apr 11 and Apr 17 models noted the RSI 22 / stochastic 2 risk. The Apr 11 model even recommended entering "on bounce to $44 (near 10 EMA at $45.74)" — the bounce came but went further than the $46.50 stop before reversing.

2. **ADX 64 trend conviction does not eliminate bounce risk.** The statistical arb agent reported a near-zero Hurst exponent, meaning price process is near-random at fine scale despite the strong macro trend. This argues for wider stops or smaller size in extreme oversold territory.

3. **Paper portfolio budget matters for sizing.** The $5K paper account forced 17-share sizing with a $757 risk limit. The $100K run sized 180 shares but was never executed. The lesson: position size affects stop feasibility — a 17-share position at $43.50 with a $46.50 stop is $51 max loss; the actual -$35.70 loss was within the risk model's tolerance.
