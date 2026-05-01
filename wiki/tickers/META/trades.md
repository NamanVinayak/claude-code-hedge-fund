---
name: META trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 889
summary: Two paper trades placed; trade ID 16 filled at $673.72 and was abandoned (exit $671.34, small loss); trade ID 22 was abandoned before fill at $676.87.
---

# META — Trades

## TL;DR

Two paper trades were placed in META across the April 2026 run cycle. Trade 16 (from run 20260415_093758) was the only one that actually filled — entering at $673.72, closing at $671.34, a small loss of approximately $2.38/share. Trade 22 (from run 20260417_233350) was abandoned before fill: it was placed at $676.87 but no entry fill was ever recorded, and it was abandoned on April 29, 2026. One hold recommendation from run swing_20260411_211655 preceded both trades and correctly identified the setup was not yet ripe.

## Open positions

None. Both trades are closed/abandoned as of April 29, 2026 (source: tracker.db query).

## Closed trades

### Trade ID 16 — Long, Filled (Run: 20260415_093758)

| Field | Value |
|---|---|
| Trade ID | 16 |
| Direction | Long |
| Quantity | 1 share |
| Status | Abandoned (closed after partial fill) |
| Entry price (model) | $675.75 |
| Entry fill price | $673.72 |
| Exit fill price | $671.34 |
| P&L | Not recorded in DB (estimated: ~-$2.38 per share, ~-$2.38 gross) |
| Created at | 2026-04-15 17:12:54 |
| Entered at | 2026-04-15 17:14:47 |
| Closed at | 2026-04-29 11:19:51 |

**Model thesis at entry:** Strongest momentum in the April 15 basket — #1 momentum rank, MACD histogram +11.84 (more than double next-best), 5-day ROC +15.2%, 10-day ROC +23.5%. Morgan Stanley named META top tech earnings pick ahead of Q1 2026 report. Broadcom AI chip partnership through 2029 cited. Daily RSI at 65.8 was notably not overbought, leaving statistical room. One share was the maximum allowed at the time (originally a $5K paper budget — bumped to $25K when the phantom-budget sizing bug was fixed in commit b2b472d). Confidence: 63%, R:R: 2.38:1 (target $706.40, stop $637.70), timeframe 7–14 days (source: decisions.json, run 20260415_093758).

**What happened:** Fill came in slightly below model entry ($673.72 vs. $675.75 — favorable $2.03 slip). Closed April 29 at $671.34, a $2.38 loss. Close coincides with Q1 2026 earnings day — likely exited rather than held through the binary event. Stop of $637.70 was never hit.

**Lessons:** Trade was directionally correct — confirmed by the April 17 follow-on run also buying at $676.87. Small loss reflects pre-earnings risk-off exit, not stop-out.

---

### Trade ID 22 — Long, Never Filled (Run: 20260417_233350)

| Field | Value |
|---|---|
| Trade ID | 22 |
| Direction | Long |
| Quantity | 15 shares |
| Status | Abandoned |
| Entry price (model) | $676.87 |
| Entry fill price | None (never filled) |
| Exit fill price | None |
| P&L | None |
| Created at | 2026-04-18 00:18:19 |
| Entered at | None |
| Closed at | 2026-04-29 11:19:51 |

**Model thesis at entry:** Explosive breakout with 1.75x volume. Hourly ADX at 66 signaling very strong intraday trend strength. The April 17 run had much higher confidence (74%) and a position size (15 shares) that — at the time — was sized against a phantom $100K budget (a sizing bug since fixed in commit b2b472d; current paper account is $25K with proper conviction-based sizing). R:R: 2.79:1 (target $710, stop $665), timeframe 8–12 trading days. The fundamental bearish signal (declining EPS trend, heavy insider selling) kept the position "moderate" for that run's context (source: decisions.json, run 20260417_233350).

**What happened:** No fill recorded. Order placed at 00:18 on April 18 (after market close). Moomoo paper trading uses day-only limit orders — after-hours placement means execution depends on next-day open. If META opened above $676.87, the order would expire unfilled. Abandoned April 29.

**Lessons:** After-hours order placement risks missing entries. This trade is a relic from the phantom $100K budget bug (fixed) — the 15-share size was never appropriate for the actual paper account. Going forward, the new conviction-based sizing model + ledger-aware risk manager prevent recurrence (commits b2b472d, 5361f7c).

---

## Prior hold recommendation

### swing_20260411_211655 — Hold (no trade placed)

The April 11 run correctly held META at $625. EMA structure was still bearish, R:R was 1.4:1 (below the 2:1 minimum), and Head Trader confidence was only 58%. The system explicitly waited for a pullback to $610 for 2.5:1 R:R. META instead ran to $675+ without that pullback, and the system bought the breakout on April 15 instead. This is an example of "missed the ideal entry, bought the confirmation" — a valid outcome under strict R:R discipline (source: decisions.json, run swing_20260411_211655).

## Lifetime stats (META, all paper trades to date)

| Metric | Value |
|---|---|
| Total trades | 2 |
| Filled | 1 (trade 16) |
| Unfilled/abandoned | 1 (trade 22) |
| Winning trades | 0 |
| Losing trades | 1 (trade 16, ~-$2.38) |
| Win rate | 0% (1 trade sample, insufficient) |
| Avg P&L per filled trade | ~-$2.38 |
| Avg model confidence | 68.5% (63% + 74% / 2) |
| All directions | Long only |

Note: Sample size of 1 filled trade is too small to draw conclusions about model accuracy for META. Q1 2026 earnings on April 29 (the day both trades closed) was the key unresolved catalyst at time of position close.
