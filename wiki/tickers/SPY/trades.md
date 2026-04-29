---
name: SPY trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 843
summary: 2 trades on record — 1 closed daytrade (loss, -$1.05), 1 abandoned swing; net P&L -$1.05; 0% win rate; entry hit rate 50%
---

# SPY — Trades

## TL;DR

Two SPY trades in the tracker database. One closed daytrade on Apr 15 2026: entered at $697.31, stopped out at $696.26 for a -$1.05 loss (1 share). One swing trade opened Apr 17 2026 at a model entry of $701.66 that was never filled — status is "abandoned," meaning the order lapsed before execution. Net realized P&L: -$1.05. No open positions as of Apr 29 2026.

## Open positions

None. The Apr 17 swing entry (ID 29) has status "abandoned" — the limit order at $701.66 was never filled and expired. No active SPY exposure.

## Closed trades

### Trade ID 17 — Daytrade Long, Apr 15 2026 (CLOSED)

| Field | Value |
|---|---|
| Trade ID | 17 |
| Direction | Long |
| Quantity | 1 share |
| Model entry | $697.45 |
| Actual fill (entry) | $697.31 |
| Actual fill (exit / stop-out) | $696.26 |
| Stop loss | $696.26 |
| Model target | $699.33 |
| Realized P&L | -$1.05 |
| Status | Closed |
| Opened | 2026-04-15 18:04:12 (UTC) |
| Closed | 2026-04-15 09:30:00 (local) |
| Mode | Daytrade |
| Run ID | 20260415_104041 |

**What the model said:** 8/9 daytrade strategies were bullish. Triple-confluence setup: SPY had cleared the opening range high ($696.35), prior day high ($694.58), and was holding above VWAP ($696.58). Bullish squeeze fired with momentum +0.30. Risk-reward was 1.58:1, which met the minimum threshold. Confidence was 64% — not high conviction, mainly limited by below-average intraday volume (0.71x relative volume, decreasing). Sizing was deliberately capped to 1 share for the same reason.

**What actually happened:** The fill was $697.31, slightly below the model's $697.45 entry — slightly better fill than expected. However, price reversed and hit the stop at $696.26, resulting in a loss of exactly $1.05 (1 share × $1.05 slippage from fill to stop). The risk-reward being 1.58:1 rather than 2:1 gave very little room for error; any adverse move of ~$1 from entry would stop out. The below-average volume warning the model flagged was prescient — thin tape did not sustain the breakout.

**Lesson:** The 1.58:1 R:R was borderline, only just above the stated minimum. Future SPY daytrades should require relative volume > 1.0x to enter; the model's own volume caveat was the right signal to reduce or skip the trade.

---

### Trade ID 29 — Swing Long, Apr 17 2026 (ABANDONED)

| Field | Value |
|---|---|
| Trade ID | 29 |
| Direction | Long |
| Quantity | 15 shares |
| Model entry | $701.66 |
| Actual fill (entry) | None (not filled) |
| Stop loss | $695.00 |
| Model target | $722.00 |
| Realized P&L | $0 (no fill) |
| Status | Abandoned |
| Opened (order placed) | 2026-04-18 00:18:19 (UTC) |
| Closed (order lapsed) | 2026-04-29 11:19:51 (UTC) |
| Mode | Swing |
| Run ID | 20260417_233350 |

**What the model said:** Swing PM rated SPY buy at 72% confidence, entry $701.66, target $722.00, stop $695.00. Risk-reward was 3.05:1. Reasoning: broad uptrend, hourly ADX 65 showing strong directional momentum. Sizing reduced to 15 shares (from a higher notional) due to 0.96 correlation with QQQ and overlap with the 7 single-name tech longs already in the book (AAPL, MSFT, NVDA, META, GOOGL, AMZN, AMD). The PM explicitly flagged that owning SPY on top of a tech-heavy single-name book amounts to double-counting tech beta.

**What actually happened:** The limit order at $701.66 was placed via Moomoo paper trading at 00:18 UTC on Apr 18. The order never filled — price presumably did not touch the limit level within the session window. Per Moomoo paper trading rules, limit orders expire at end of day (TimeInForce.DAY only), and the order was not re-placed on subsequent days. The trade record remained open in the DB until the abandoned status was set on Apr 29.

**Lesson:** For swing entries, if the model enters a limit order and price gaps away the next morning, the playbook should either (a) re-evaluate and re-enter at market, or (b) explicitly cancel and document why. Letting a swing entry sit as an un-filled limit for 11 days without review is a process gap. The monitor step should flag stale unfilled orders after 2 sessions.

---

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades | 2 |
| Closed trades | 1 |
| Abandoned (unfilled) | 1 |
| Win rate (closed) | 0% (0 wins / 1 closed) |
| Entry hit rate | 50% (1 filled / 2 attempted) |
| Net realized P&L | -$1.05 |
| Average holding time (closed) | Same session (daytrade) |
| Modes traded | Daytrade, Swing |
| Average confidence at entry | 64% (daytrade) / 72% (swing, not filled) |

**Sample size warning:** 1 closed trade is statistically meaningless. The -$1.05 loss and 0% win rate should not influence future SPY trade decisions. The relevant observation is qualitative: the one filled trade was a marginal R:R (1.58:1) on thin volume, and it stopped out. Both data points are consistent with the model's own expressed caution at entry.

## Closed — older than 30 days

None. Both trades occurred in April 2026.

## Closed — older than 6 months

None.
