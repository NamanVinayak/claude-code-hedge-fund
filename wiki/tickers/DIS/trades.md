---
name: DIS trades
last_updated: 2026-05-07
last_run_id: 20260507_220640
target_words: 800
stale_after_days: 60
word_count: 761
summary: 1 confirmed closed trade (id 117, long 2 shares, -$4.99); short decision issued run 20260507_220640 (3 shares at $108.50, target $103, stop $110.60, 2.62:1 R/R) — NOT YET confirmed in trade_ledger.json per_ticker_history["DIS"]; per hard rule #11 no open position claimed until ledger confirms fill
---

# DIS — Trades

## TL;DR

`trade_ledger.json per_ticker_history["DIS"]` as of run `20260507_220640` contains **1 confirmed fill**: trade id 117, 2 shares long, filled at $103.495 on 2026-05-01, **stopped out at $101.00 on 2026-05-05**, realizing **-$4.99 P&L**. Status: "stop_hit" — closed. A short decision was issued this run (3 shares at $108.50, run `20260507_220640`), but `per_ticker_history["DIS"]` does not yet contain a corresponding entry — the fill is unconfirmed. Per hard rule #11, no open short position is claimed here. All confirmed-fill claims sourced exclusively from `per_ticker_history["DIS"]`. [source: `trade_ledger.json`, run `20260507_220640`]

---

## Open positions (confirmed in ledger)

None. `per_ticker_history["DIS"]` contains only id 117 (closed). The short decision from run `20260507_220640` is pending ingestion.

---

## Pending decision — not yet in ledger

### Run `20260507_220640` — SHORT 3 shares — DECISION ISSUED, FILL UNCONFIRMED

| Field | Value |
|---|---|
| Action | short |
| Quantity | 3 shares |
| Entry price | $108.50 |
| Entry tolerance | 1.0% |
| Target price | $103.00 |
| Stop loss | $110.60 |
| Risk-reward | 2.62:1 |
| Timeframe | 3-6 trading days |
| Confidence | 35% |
| Account risk pct | 0.5% |
| Status | **DECISION ISSUED — fill not confirmed in per_ticker_history["DIS"]** |

**Rationale**: Dual Z-score extreme (daily 2.05, hourly 2.12), Bollinger pct_b 1.06, OBV distribution on 2.72x volume, and unanimous entry-price warning from all 4 bullish agents (who prefer $103-104 for a long). R/R 2.62:1 clears 2:1 minimum. Sized conservatively at 3 shares ($325.50 = 22.3% of capital, 0.5% account risk). [source: `decisions.json DIS`, run `20260507_220640`]

---

## Closed — May 2026

### Trade ID 117 — Long 2 shares — CLOSED 2026-05-05

| Field | Value |
|---|---|
| Trade ID | 117 |
| Ticker | DIS |
| Direction | Long |
| Quantity | 2 shares |
| Status | **stop_hit (closed)** |
| Entry price (model) | $102.50 |
| Entry fill price | **$103.495** |
| Exit fill price | **$101.00** |
| Realized P&L | **-$4.99** |
| Stop loss | $101.00 |
| Target price | $107.11 (never reached) |
| Risk-reward (model) | 3.07:1 |
| Timeframe | 5–10 trading days |
| Confidence | 62% |
| Created at | 2026-05-01T22:41:01+00:00 |
| Entered at | 2026-05-01T13:39:00+00:00 |
| Closed at | 2026-05-05T14:09:00+00:00 |
| Run ID (decision) | `20260501_221355` |
| Run ID (closure confirmed) | `20260505_220625` |

**What happened**: Pre-earnings breakout thesis — April 30 close above $103 on 1.23x volume, ADX 37.34, MACD bullish cross. Decision: 2 shares long at $102.50 limit (filled at $103.495 with 1% tolerance), target $107.11, stop $101.00, 3.07:1 R/R, confidence 62%. The breakout fully retraced over 4 trading days as macro headwinds (Iran escalation May 4, WTI ~$105, Dow -557 pts) reversed the risk-on environment. By May 5 hourly price reached $100.48, triggering the $101.00 stop at -$4.99 ($2.495/share × 2 shares).

**Lesson**: Volume confirmation was weak (1.23x vs 1.5x threshold). Entering near a 3-day earnings blackout on a sub-threshold breakout extracts premium risk for the binary event. The macro tailwind (Iran peace) was reversed in 3 days. Structurally different from the current post-earnings short setup (different macro regime, different entry direction).

---

## Run-level model recommendations (unexecuted)

| Date | Run ID | Price | Action | Notes |
|---|---|---|---|---|
| Apr 11 | `swing_20260411_211655` | $99.17 | Hold | R/R 0.9:1 fails; downtrend |
| Apr 15 | `20260415_110848` | ~$102–103 | Buy (unexecuted) | Limit $100.50 missed fill |
| May 1 | `20260501_221355` | $103.75 | **Buy** | Filled $103.495; stopped out May 5 |
| May 4 | `20260504_221111` | $101.31 | Hold | Earnings blackout; near stop |
| May 5 | `20260505_220625` | $101.31 | Hold | Stop hit during session |
| May 6 | `20260506_220627` | $108.06 | Hold | Bull restart fired but blackout + R/R 0.16:1 |
| **May 7** | **`20260507_220640`** | **$108.50** | **Short (pending)** | **Dual Z-score extreme; fill unconfirmed** |

---

## Lifetime stats (DIS — confirmed fills only)

| Metric | Value |
|---|---|
| Total confirmed fills | 1 |
| Open positions (confirmed) | 0 |
| Closed positions | 1 (id 117, stop_hit) |
| Realized P&L | **-$4.99** |
| Win rate | 0W / 1L (0%) |
| Avg holding period (closed) | 4 calendar days (May 1 → May 5) |

*Source: `per_ticker_history["DIS"]` from `trade_ledger.json`, run `20260507_220640`. Per hard rule #11: only claims from per_ticker_history["DIS"] are authoritative for fills, P&L, and quantities.*
