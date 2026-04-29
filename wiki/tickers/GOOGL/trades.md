---
name: GOOGL trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 814
summary: One swing trade placed on April 18, 2026; status abandoned; no fills, no realized P&L
---

# GOOGL — Trades

## TL;DR

GOOGL has one trade in the system, placed April 18, 2026 from run 20260417_233350. It was marked **abandoned** (unfilled limit order that expired). Entry at $337.12 was never filled. No realized P&L. This is the complete trading history for this ticker in tracker.db as of 2026-04-29.

---

## Open positions

**None.** The one attempted GOOGL trade reached `abandoned` status before fill. There are no open GOOGL positions.

---

## All trades — full history

### Trade #23 — Long, April 2026

| field | value |
|---|---|
| Trade ID | 23 |
| Ticker | GOOGL |
| Direction | long |
| Quantity | 45 shares |
| Status | **abandoned** |
| Entry price (limit) | $337.12 |
| Exit fill price | None |
| Realized P&L | None (unfilled) |
| Created | 2026-04-18 00:18:19 UTC |
| Closed | 2026-04-29 11:19:51 UTC |
| Source run | 20260417_233350 |

**What happened:** The April 17 swing run (20260417_233350) produced the highest-conviction decision in the 14-ticker cohort — GOOGL at 82% confidence, quantity 45 shares, entry $337.12, target $350.00, stop $325.00, R:R 2.17:1, timeframe 8-14 trading days. The PM reasoning was: "Strongest conviction in cohort (82): multi-TF aligned, hourly ADX 72, ROC accelerating. R:R 2.17:1 meets rule as-is." The limit order was placed via Moomoo paper trading on April 18 but was never filled before expiry. Moomoo paper trading orders expire at end of each trading day (DAY orders only; GTC not supported), so any unfilled order must be re-placed the next session. The order was not re-placed and was eventually marked abandoned.

**Lessons recorded:**
1. DAY-only order type in Moomoo paper trading means any limit below the open requires active re-placement. An entry at $337.12 that is not immediately marketable becomes an overnight stale order.
2. The 82% conviction call was never tested — we do not know if the trade would have worked. Q1 2026 earnings on April 28 were the primary catalyst within the 8-14 day timeframe. The outcome of that earnings report is relevant context for future GOOGL trades.
3. GOOGL was the highest-confidence name in the April 17 cohort; the failure to fill represents a process gap in order monitoring rather than a model miss.

---

## Closed — last 30 days

No closed trades with exit fills in the past 30 days.

---

## Closed — older, rolled by month

No prior GOOGL trades in tracker.db before the April 18, 2026 entry.

---

## Closed — older than 6 months

No trades older than 6 months on record.

---

## Lifetime stats

| metric | value | notes |
|---|---|---|
| Total trades attempted | 1 | includes abandoned |
| Fills (entries executed) | 0 | none filled |
| Abandoned / expired | 1 | trade #23 |
| Realized P&L | $0 | no fills |
| Unrealized P&L | $0 | no open position |
| Win rate (closed trades) | n/a | no closed trades |
| Entry hit rate | 0% | 0 of 1 limit orders filled |
| Average confidence at entry | 82% (attempted) | from run 20260417_233350 |
| Average R:R at entry | 2.17:1 (attempted) | from run 20260417_233350 |
| Modes attempted | swing | only swing mode used |

---

## Model signal history

This table tracks every time GOOGL/GOOG appeared in a run, regardless of whether a trade was placed, to build a signal accuracy record over time.

| run_id | date | mode | signal | confidence | action | outcome |
|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | swing | bullish (head trader avg 59.8) | 59.8% | buy (GOOG) | no order placed (GOOG ticker; tracker uses GOOGL) |
| 20260415_093758 | 2026-04-15 | swing | bullish | 60% (head trader) | buy $332.06, tgt $355, stp $318 | no order placed (different run) |
| 20260417_233350 | 2026-04-17 | swing | bullish | **82%** | buy $337.12, tgt $350, stp $325 | abandoned (unfilled) |

Notes:
- April 11 run used ticker symbol GOOG (non-voting). The tracker uses GOOGL (voting). For fundamental analysis purposes these are treated as equivalent (same underlying business, ~1% price spread historically).
- April 15 run produced a separate entry decision at $332.06; no order was placed from that run (different execution session).
- No run has produced a bearish/short signal on GOOGL/GOOG to date.

---

## Next trigger conditions

The model should re-analyze GOOGL after:
1. **Q1 2026 earnings release** (April 28, 2026 post-market) — EPS estimate $2.60, revenue $106.81B. A beat, especially on cloud segment, would re-confirm the bull thesis. A miss on cloud revenue or guidance cut would be a thesis breaker.
2. **DOJ antitrust cross-appeal developments** — any court ruling on the divestiture request changes the long-term thesis materially.
3. **Price revisits the $317-$330 pullback zone** — the ideal entry per the April 15 swing_pullback_trader signal; current abandoned entry at $337 was above this zone, so a pullback would offer a better risk/reward setup.

## Last updated

2026-04-29 — bootstrapped from tracker.db (trade #23) and run archives 20260415_093758, 20260417_233350, swing_20260411_211655
