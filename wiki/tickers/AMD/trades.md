---
name: AMD trades
last_updated: 2026-05-01
last_run_id: 20260501_132346
target_words: 800
stale_after_days: 60
word_count: 782
summary: 1 lifetime filled-and-abandoned trade (no P&L); 1 new open short entered 2026-05-01 at $354.49, stop $372.31, target $277.74 (4.31:1 R/R, 1 share)
---

# AMD — Trades

## TL;DR

Two trades placed against AMD. Trade 25 (long 15 shares, limit $278.26) was never filled and was marked abandoned 2026-04-29. On 2026-05-01, run 20260501_132346 issued the first-ever short signal on AMD at $354.49 — entered as 1 share, stop $372.31, target $277.74 (4.31:1 R/R), 42% confidence, half-sized due to earnings binary risk on May 5.

## Open positions

### Trade — Short 1 share — OPEN

| Field | Value |
|---|---|
| Direction | Short |
| Status | Open |
| Quantity | 1 share |
| Entry price | $354.49 |
| Stop loss | $372.31 |
| Target price | $277.74 |
| Risk-reward | 4.31:1 |
| Max risk | $17.82 per share |
| Potential gain | $76.75 per share |
| Timeframe | 8–15 trading days |
| Confidence | 42% |
| Run ID | 20260501_132346 |
| Order placed | 2026-05-01 |
| Notes | Half-size (1 share vs standard 2) due to May 5 earnings binary. Stop above recent swing high + 1 ATR at $372.31. Full re-assessment required after May 5 earnings print. Head Trader recommended hold-flat; PM overrode to short at reduced size given 4.31:1 R/R clearing the 4:1 borderline threshold. |

**Why this trade was placed:** All five swing agents refused to enter long at $354.49. Two agents — swing_mean_reversion and swing_catalyst_news — explicitly called for a short fade. Z-score vs 50-SMA is 2.6 (statistical exhaustion), RSI-14 is 83 (severely overbought), and the stock is 52.6% above its 50-day average after a +74% 21-day surge. Analyst consensus avg target is ~$289–$297, approximately $60 below current price. CEO Lisa Su sold ~$16M in March 2026 (2:1 insider sell ratio). The 4.31:1 R/R clears the 4:1 threshold the PM uses for borderline-confidence trades. Sized at 1 share (risk ~$18) per Head Trader guidance on binary risk (source: decisions.json, run 20260501_132346).

**Key risk:** Q1 2026 earnings May 5 after close. A strong beat with euphoric AI guidance could cause AMD to gap above the $372.31 stop, creating a loss larger than planned. Position is sized specifically to limit this exposure.

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

**Why this trade was placed:** The April 17 run showed AMD with the highest 21-day ROC (41.7%) in the entire 19-stock watchlist. ADX was 41, all daily EMAs were aligned bullish, and the swing consensus was bullish. The system sized the position at 15 shares (~$4,175 notional) rather than full-size because RSI was 91 and the hourly STC indicator had crossed bearish. A $278.26 limit was set to buy on a brief dip, not at market (source: decisions.json, run 20260417_233350).

**Why it was never filled:** Moomoo paper trading uses day-only time-in-force. The limit was not re-placed after expiry. AMD never pulled back to $278.26 within the order window, and the trade was marked abandoned on April 29.

## Run history — all AMD signals

| Run ID | Date | Signal | Confidence | Action | Entry | Target | Stop | Notes |
|---|---|---|---|---|---|---|---|---|
| swing_20260411_211655 | 2026-04-11 | Hold | 50% | None | $245 | $260 | $228 | R:R 0.9:1 — overextended; z-score 2.35, RSI 73.7. Wait for $224–$237 pullback. |
| 20260415_110848 | 2026-04-15 | Buy | 62% | 2 shares | $248 | $268 | $241 | 5/9 agents bullish; ADX 41, squeeze breakout. Risk manager capped at 2 shares. No fill recorded. |
| 20260417_233350 | 2026-04-17 | Buy | 70% | 15 shares | $278.26 | $305 | $270 | 41.7% 21d ROC; RSI 91 + hourly STC cross down = small size despite high conviction. Abandoned. |
| 20260501_132346 | 2026-05-01 | Short | 42% | 1 share | $354.49 | $277.74 | $372.31 | First short on AMD. 0/5 agents bullish; 2 bearish. Z-score 2.6, RSI 83, +74% 21d. Half-size for earnings binary (May 5). |

Sources: decisions.json from each respective run; tracker.db trade id 25.

## Closed — older than 30 days

None.

## Closed — older than 6 months

None.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades placed | 2 |
| Filled / open | 1 open short (no fills on prior long) |
| Abandoned / expired | 1 |
| Win rate | N/A (no closed fills) |
| Gross realized P&L | $0.00 |
| Unrealized P&L | TBD (short entered at $354.49) |
| Avg confidence at entry | 56% (42% short + 70% abandoned long) |
| Avg R:R at entry | 3.78:1 (4.31:1 short + 3.24:1 abandoned long) |

## Key lessons from this ticker

1. **Limit entries on parabolic runs get missed.** AMD ran from ~$245 on April 11 to $278+ by April 17 — a 13.5% move in six days. The $278.26 limit was set too tight relative to momentum. The result was a missed trade rather than a losing trade.

2. **Overbought management was sound across all runs.** The system consistently flagged extreme RSI and Z-score readings. It did not blindly follow bullish agent majorities — it moderated conviction into position sizing, then flipped to short when the extension became statistically extreme.

3. **The first short signal on AMD is a direction flip:** After three consecutive hold/buy signals, the system issued a short in run 20260501_132346 driven by Z-score 2.6, RSI 83, analyst consensus below current price, and insider selling. The earnings binary (May 5) creates headline risk in both directions — position sized at minimum to limit exposure.
