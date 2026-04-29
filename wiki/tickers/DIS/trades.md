---
name: DIS trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 802
summary: No trades ever executed on DIS in tracker.db; the model recommended hold (Apr 11) then cautious buy (Apr 15) — the buy was never placed, likely due to entry discipline (do not chase above $103).
---

# DIS — Trades

## TL;DR

Zero trades have ever been placed on DIS in the paper trading account (tracker.db query returned 0 rows). The model produced two assessments in April 2026: a hold on April 11 and a cautious buy signal on April 15. Neither resulted in an executed order. The April 15 buy recommendation came with an explicit entry constraint — do not enter above $103 — and the stock was trading right at resistance when the signal was generated, which likely explains why no order was placed. As of the last run, DIS represents a tracked-but-not-traded ticker.

## Open positions

None. `tracker.db` contains zero DIS records.

## Closed trades

None. No historical DIS trades in the database.

## Run-level model recommendations (not executed trades)

### Run: `20260415_110848` — April 15, 2026

**Model recommendation:** BUY 9 shares

| Field | Value |
|---|---|
| Action | buy |
| Quantity | 9 shares |
| Entry price | $100.50 |
| Target price | $108.00 |
| Stop loss | $97.50 |
| Risk-reward | 2.5:1 |
| Timeframe | 7–12 trading days |
| Confidence | 55% |
| Run date | April 15, 2026 |
| Status | NOT EXECUTED |

**Model reasoning (from `decisions.json`, run `20260415_110848`):** "Cautious bullish: MACD histogram turned strongly positive, ADX 31, hourly EMAs aligned uptrend. Druckenmiller bullish on valuation (P/E 14.76). Entry on dip to $100.50 (fib 61.8/SuperTrend support). Do NOT enter above $103. Stop $97.50."

**Agent vote breakdown (run `20260415_110848`):**
- Bullish (5): swing_trend_follower (60%), swing_momentum_ranker (65%), swing_catalyst_trader (63%), swing_breakout_trader (38%), stanley_druckenmiller (62%)
- Neutral (2): swing_sector_rotation (40%), growth_analyst_agent (13%)
- Bearish (3): swing_pullback_trader (32%), swing_mean_reversion (52%), news_sentiment (62%)

**Why not executed:** The stock was trading at approximately $102–103 when the signal was generated, right at the resistance level the model flagged. The head trader's directive was explicit: "do not enter above $103." Since the stock was already at resistance, the limit order at $100.50 would have required a pullback that apparently did not occur within the trading window.

---

### Run: `swing_20260411_211655` — April 11, 2026

**Model recommendation:** HOLD (no trade)

| Field | Value |
|---|---|
| Action | hold |
| Quantity | 0 |
| Entry price (indicative) | $99.17 |
| Target (indicative) | $103.00 |
| Stop (indicative) | $95.00 |
| Risk-reward | 0.9:1 |
| Timeframe | N/A |
| Confidence | 42% |
| Run date | April 11, 2026 |
| Status | HOLD — NO TRADE |

**Model reasoning (from `decisions.json`, run `swing_20260411_211655`):** "Head Trader neutral at 42% with 44% agent agreement — lowest consensus. Mixed signals: downtrend intact but bounce testing it. Druckenmiller sees value at 14x P/E but that is a longer-term thesis. No imminent catalyst (earnings not until May). Wait for directional resolution above 102 or below 95."

**Why held:** Risk-reward of 0.9:1 at the April 11 price point ($99.17) failed the system's 2:1 minimum threshold. The stock had bounced from $92.42 to $99 but the remaining upside to the $103 target was only $3.83 vs. $4.17 to the $95 stop — a losing ratio.

---

## What the model has been watching (signal trajectory)

| Date | Run ID | Price | Model stance | Confidence | Explanation |
|---|---|---|---|---|---|
| Apr 11, 2026 | `swing_20260411_211655` | $99.17 | Hold | 42% | Downtrend testing but R:R 0.9:1 fails |
| Apr 15, 2026 | `20260415_110848` | ~$102–103 | Cautious buy | 55% | MACD crossover, ADX 31; entry set at $100.50 — stock above entry |

**Trend:** Confidence improved from 42% to 55% over four days as the MACD crossover confirmed and ADX strengthened. The stock moved past the entry point rather than pulling back to it.

## Lifetime stats

| Metric | Value |
|---|---|
| Total DIS trades | 0 |
| Open positions | 0 |
| Closed positions | 0 |
| Realized P&L | $0.00 |
| Win rate | N/A |
| Average hold time | N/A |
| Model buy signals generated | 1 (Apr 15, 2026) |
| Model hold signals generated | 1 (Apr 11, 2026) |
| Executed vs. signaled ratio | 0 / 1 buys executed |

## Notes for future trades

1. The model's preferred entry range is $99.50–101.00 (fib 61.8/hourly SuperTrend support). If DIS pulls back from its April 15 close of $102.59, this is the zone to watch.
2. Stop discipline: $97.50 (below hourly SuperTrend). A close below $95 would signal the April base has failed and flip the model bearish.
3. Target: $107–109 (prior swing high cluster). At $100.50 entry with $97.50 stop and $108 target, R:R is 2.5:1 — the minimum threshold for system approval.
4. Q2 FY2026 earnings (est. May 6–13, 2026) is the binary event. The system typically avoids holding open swing positions through earnings unless the setup is high-conviction with an earnings catalyst specifically.
5. Max position size at current price: 9 shares × $100.50 = $904.50 (approximately 18% of the $5,000 paper portfolio). This is within the 25% maximum per-position cap.
