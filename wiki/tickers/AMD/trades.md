---
name: AMD trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 680
summary: 1 lifetime trade (abandoned, no fill); no realized P&L
---

# AMD — Trades

## TL;DR

One trade placed against AMD — a limit long entered April 18, 2026 from run 20260417_233350. The order was placed at a limit of $278.26 but was never filled and was subsequently marked abandoned on April 29, 2026. No realized P&L exists for AMD. The system generated buy signals in two of three runs analyzed and a hold in one; only the third run resulted in an actual order placement.

## Open positions

None. The single AMD position (trade id 25) was closed as abandoned on 2026-04-29 11:19 UTC.

## Closed — recent (last 30 days)

### Trade 25 — Long 15 shares — Abandoned (no fill)

| Field | Value |
|---|---|
| Trade ID | 25 |
| Direction | Long |
| Status | Abandoned |
| Quantity ordered | 15 shares |
| Limit entry price | $278.26 |
| Entry fill price | None (order never filled) |
| Stop loss | $270.00 |
| Target price | $305.00 |
| Risk-reward | 3.24:1 |
| Timeframe | 7–12 trading days |
| Confidence | 70% |
| Run ID | 20260417_233350 |
| Order placed | 2026-04-18 00:18 UTC |
| Closed | 2026-04-29 11:19 UTC |
| Realized P&L | $0 (no fill) |

**Why this trade was placed:** The April 17 run showed AMD with the highest 21-day ROC (41.7%) in the entire 19-stock watchlist. ADX was 41, all daily EMAs were aligned bullish, and the swing consensus was bullish. The system sized the position small at 15 shares (~$4,175 notional, ~4.2% of $100k) rather than a full-size position because RSI was 91 and the hourly STC indicator had crossed bearish, both signaling short-term pullback risk. The reasoning: high conviction on direction, low conviction on entry timing. A $278.26 limit was set to buy on a brief dip, not at market (source: decisions.json, run 20260417_233350).

**Why it was never filled:** The limit was $278.26. If AMD never pulled back to that level after the order was placed on April 18 — or if it sold off through the stop — the limit order would expire unfilled. Moomoo paper trading orders use day-only time-in-force (no GTC allowed per API constraints documented in CLAUDE.md). Unfilled orders must be manually re-placed each day. The order was not re-placed, and the trade was marked abandoned on April 29.

## Run history — all AMD signals

| Run ID | Date | Signal | Confidence | Action | Entry | Target | Stop | Notes |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | Hold | 50% | None | $245 | $260 | $228 | R:R 0.9:1 — severely overextended; z-score 2.35, RSI 73.7. Risk manager limit $550. Wait for $224–$237 pullback. |
| 20260415_110848 | 2026-04-15 | Buy | 62% | 2 shares | $248 | $268 | $241 | 5/9 agents bullish; ADX 41, squeeze breakout. Risk manager capped at 2 shares. No fill recorded. |
| 20260417_233350 | 2026-04-17 | Buy | 70% | 15 shares | $278.26 | $305 | $270 | 41.7% 21d ROC; RSI 91 + hourly STC cross down = small size despite high conviction. Abandoned. |

Sources: decisions.json from each respective run; tracker.db trade id 25.

## Closed — older than 30 days

None.

## Closed — older than 6 months

None.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades placed | 1 |
| Filled | 0 |
| Abandoned / expired | 1 |
| Win rate | N/A (no fills) |
| Gross realized P&L | $0.00 |
| Unrealized P&L | $0.00 |
| Total return vs entry | N/A |
| Avg confidence at entry | 70% (single data point) |
| Avg R:R at entry | 3.24:1 (single data point) |

## Key lessons from this ticker

1. **Limit entries on parabolic runs get missed.** AMD ran from ~$245 on April 11 to $278+ by April 17 — a 13.5% move in six days. The system correctly avoided chasing at April 11 and April 15 prices, but by April 17 the limit of $278.26 may have been set too tight relative to the momentum. The result was a missed trade rather than a losing trade.

2. **Overbought management was sound.** All three runs flagged the extreme RSI and Z-score readings correctly. The system did not blindly follow the bullish agent majority — it moderated conviction into position sizing. Even if the April 17 limit had filled, the 3.24:1 R:R with a $270 stop provided meaningful downside protection.

3. **No realized loss incurred.** Despite three runs of analysis and one order placement, AMD produced zero realized loss. The "miss" is an opportunity cost, not a capital loss.
