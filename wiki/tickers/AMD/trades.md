---
name: AMD trades
last_updated: 2026-05-06
last_run_id: 20260506_150729
target_words: 800
stale_after_days: 60
word_count: 786
summary: 2 lifetime trades — Trade 25 (long 15 shares, abandoned, no fill); id 113 (short 1 share, stopped out 2026-05-06 at $372.31, realized P&L −$17.82); no open positions; net lifetime realized P&L −$17.82
---

# AMD — Trades

## TL;DR

Two trades placed against AMD. Trade 25 (long 15 shares, limit $278.26) was never filled and was marked abandoned 2026-04-29. Short id 113 (1 share, entered $354.49, stop $372.31, target $277.74) was opened 2026-05-01 and stopped out 2026-05-06 at $372.31 for a realized loss of −$17.82 — AMD gapped +15% on Q1 2026 earnings beat (May 5 AMC). No open AMD positions as of run 20260506_150729.

## Open positions

None. All AMD positions closed as of 2026-05-06.

## Closed — recent (last 30 days)

### Trade id 113 — Short 1 share — CLOSED (stop_hit)

| Field | Value |
|---|---|
| Trade ID | 113 |
| Direction | Short |
| Status | stop_hit |
| Quantity | 1 share |
| Entry price | $354.49 |
| Entry fill price | $354.49 |
| Stop loss | $372.31 |
| Exit fill price | $372.31 |
| Target price | $277.74 |
| Risk-reward | 4.31:1 (at entry) |
| Realized P&L | −$17.82 |
| Timeframe | 8–15 trading days |
| Confidence | 42% |
| Run ID (entry) | 20260501_132346 |
| Run ID (close) | 20260506_150729 |
| Entered | 2026-05-01T13:33:00+00:00 |
| Closed | 2026-05-06T13:30:46+00:00 |

**Why this trade was placed:** All five swing agents refused to enter long at $354.49. Two agents — swing_mean_reversion and swing_catalyst_news — explicitly called for a short fade. Z-score vs 50-SMA was 2.6 (statistical exhaustion), RSI-14 was 83 (severely overbought), and the stock was 52.6% above its 50-day average after a +74% 21-day surge. Analyst consensus avg target was ~$289–$297, approximately $60 below current price. CEO Lisa Su sold ~$16M in March 2026 (2:1 insider sell ratio). The 4.31:1 R/R cleared the 4:1 threshold the PM uses for borderline-confidence trades. Sized at 1 share (risk ~$18) per Head Trader guidance on binary risk (source: decisions.json, run 20260501_132346).

**Why it was stopped out:** AMD Q1 2026 earnings (May 5, after close) produced a blowout beat — revenue $10.25B (+38% YoY), EPS $1.37 non-GAAP (+43%), Q2 guide $11.2B topping consensus by $700M. The stock gapped approximately +15% overnight from a ~$355 daily close to $408.66 intraday, blowing through the $372.31 stop. The stop was hit at open on 2026-05-06. This is the "gap-through-stop" scenario flagged as the key risk at entry time (source: trade_ledger.json per_ticker_history[AMD], run 20260506_150729).

**Lesson:** The bearish thesis (failed breakout at $352.99, statistical exhaustion) was structurally correct for the pre-earnings setup but underestimated the magnitude of the AI infrastructure earnings beat. The earnings binary created a non-linear outcome — the stop was not merely touched but blown through by ~$36. Half-sizing the position (1 share vs standard 2) correctly limited damage to −$17.82 rather than −$35.64.

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
| 20260501_132346 | 2026-05-01 | Short | 42% | 1 share | $354.49 | $277.74 | $372.31 | First short on AMD. 0/5 agents bullish; 2 bearish. Z-score 2.6, RSI 83, +74% 21d. Half-size for earnings binary (May 5). STOPPED OUT 2026-05-06 at $372.31. |
| 20260506_150729 | 2026-05-06 | Hold | 38% | None | — | — | — | Post-earnings gap-up. R/R 0.70:1 fails 2:1 minimum. No new entries. Watch pullback $388–$395. |

Sources: decisions.json from each respective run; trade_ledger.json per_ticker_history[AMD] (run 20260506_150729).

## Closed — older than 30 days

None.

## Closed — older than 6 months

None.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades placed | 2 |
| Filled / closed | 1 closed short (id 113, stop_hit) |
| Abandoned / expired | 1 (Trade 25, long, no fill) |
| Open positions | 0 |
| Win rate | 0% (0 wins / 1 closed fill) |
| Gross realized P&L | −$17.82 |
| Avg confidence at entry | 56% (42% short + 70% abandoned long) |
| Avg R:R at entry | 3.78:1 (4.31:1 short + 3.24:1 abandoned long) |

## Key lessons from this ticker

1. **Limit entries on parabolic runs get missed.** AMD ran from ~$245 on April 11 to $278+ by April 17 — a 13.5% move in six days. The $278.26 limit was set too tight relative to momentum. The result was a missed trade rather than a losing trade.

2. **Overbought management was sound across all runs.** The system consistently flagged extreme RSI and Z-score readings. It did not blindly follow bullish agent majorities — it moderated conviction into position sizing, then flipped to short when the extension became statistically extreme.

3. **Half-sizing into earnings binary limited damage.** The short id 113 was sized at 1 share specifically because of the May 5 earnings binary. When the stop was blown through by ~$36 on the earnings gap-up, the damage was −$17.82 instead of −$35.64. The sizing decision was correct even though the directional call was wrong.

4. **Post-earnings entries require pullback discipline.** After the +15% gap to $408.66, all five swing agents agreed: do not enter at current price. R/R is only 0.70:1. The conditional long watch zone is $388–$395 (38.2% Fib) with hourly RSI-21 cooling below 65.
