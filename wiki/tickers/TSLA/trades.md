---
name: TSLA trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 812
summary: No fills recorded in tracker.db; one model-recommended short (Apr 15) at $391.86 target $343.80; three holds across three runs reflecting poor R:R and earnings risk.
---

# TSLA — Trades

## TL;DR

TSLA was analyzed in three swing runs during April 2026. The model recommended a short once (April 15), held twice (April 11 and April 17). No TSLA trade was ever executed — tracker.db shows zero rows for this ticker. The April 15 short recommendation was sized to 1 share ($392 notional) because the April 22 earnings binary made position sizing nearly impossible. This is a useful case study in "model agrees on direction but refuses to deploy capital."

## Open positions

None. tracker.db: 0 rows for TSLA.

## Model decisions log (unexecuted)

### Run: swing_20260411_211655 — Hold

| Field | Value |
|---|---|
| Run date | 2026-04-11 |
| Action | HOLD |
| Reference price | $349.00 |
| Bear target | $330.00 |
| Stop | $362.00 |
| R:R | 1.5:1 (failed 2:1 minimum) |
| Confidence | 55% |
| Head Trader stance | Bearish at 62%, 78% agent agreement |

**Why hold?** The directional signal was bearish — ADX 29.5, EMAs aligned bearish, Head Trader 62% bear confidence with 78% agent agreement. But the risk-reward was only 1.5:1: 19 points of target distance vs. 13 points of stop distance. The PM's rule requires 2:1 minimum. The model explicitly said: "Hold until a bounce to $357 (10 EMA) offers better R:R." The thesis was correct (bearish), the entry timing was not. (Source: runs/swing_20260411_211655/decisions.json)

---

### Run: 20260415_093758 — Short (1 share, unexecuted)

| Field | Value |
|---|---|
| Run date | 2026-04-15 |
| Action | SHORT |
| Recommended quantity | 1 share |
| Entry price | $391.86 |
| Target | $343.80 |
| Stop | $399.60 |
| R:R | 6.21:1 |
| Confidence | 49% |
| Timeframe | 5-10 days |

**Why short?** The stock had bounced into the resistance cluster the April 11 model was waiting for: EMA/Fibonacci resistance zone $387–$399. Daily downtrend remained intact. Four bearish strategies agreed. With 48 points of downside to target and only 7.74 points of upside to stop, the mathematical R:R was exceptional at 6.21:1.

**Why only 1 share and unexecuted?** Two factors killed sizing. First, the April 22 earnings call was just 7 days away — a binary event that could gap the stock 15-20% in either direction, making any stop meaningless. Second, the Head Trader confidence was only 49%, reflecting multi-timeframe uncertainty. The PM described it as "sized minimal due to Apr 22 earnings binary risk." No order was placed in Moomoo, and tracker.db confirms no fill. (Source: runs/20260415_093758/decisions.json)

---

### Run: 20260417_233350 — Hold

| Field | Value |
|---|---|
| Run date | 2026-04-17 |
| Action | HOLD |
| Reference price | $391.95 |
| Bear target | $408.00 (bullish scenario) |
| Stop | $382.00 |
| R:R | 1.64:1 |
| Confidence | 48% |
| Head Trader stance | 48% confidence, stand aside |

**Why hold?** By April 17, the stock had barely moved from April 15 but the technical picture had changed: a daily downtrend was now fighting against an hourly uptrend, creating a multi-timeframe conflict the model explicitly cited. Momentum showed divergence between 5-day (positive) and 21-day (negative). R:R was 1.64:1, below the 2:1 minimum. Confidence fell to 48%. The portfolio notes for this run describe TSLA as "stand aside" among 14 tickers. (Source: runs/20260417_233350/decisions.json)

---

## Lessons learned from TSLA non-trades

**1. Earnings blackout works.** TSLA's April 22 earnings created a near-blackout condition for two of three runs. The earnings blackout rule (3-trading-day window) in risk_manager.py is designed for exactly this situation. The model respected it even before the formal rule was codified.

**2. R:R discipline prevented bad trades.** On April 11, the direction was correct (TSLA was in a downtrend that continued). But entering at $349 with a $362 stop and $330 target would have been a poor trade structurally. Waiting for the bounce worked — the April 15 setup had 6.21:1 R:R vs. 1.5:1 on April 11.

**3. Multi-timeframe conflict = no trade.** April 17 is a clean example: daily bear + hourly bull = stand aside. The model correctly refused to make a swing bet with a 5-day + 21-day momentum divergence.

**4. Low confidence + binary event = do not size.** 49% confidence + April 22 earnings = 1 share. This is the right answer even though the mathematical R:R was 6.21:1.

## Closed positions

None.

## Lifetime stats

| Metric | Value |
|---|---|
| Total trades executed | 0 |
| Total tracker.db rows | 0 |
| Model recommendations | 3 (1 short, 2 holds) |
| Unexecuted shorts | 1 (Apr 15, earnings risk) |
| Realized P&L | $0 |
| Unrealized P&L | $0 |

## Last updated

2026-04-29, sourced from tracker.db query (0 rows) + decisions.json from runs swing_20260411_211655, 20260415_093758, 20260417_233350.
