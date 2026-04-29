---
name: IWM trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 812
summary: Full trade journal for IWM — 1 closed short trade from April 15, 2026 paper trading session.
---

# IWM — Trades

## TL;DR

One closed trade on record as of bootstrap date (April 29, 2026): a short initiated on April 15, 2026 from the daytrade run 20260415_104041. The trade closed the same day at a small loss of -$1.52. The model's 8/9 bearish consensus was directionally correct (IWM was the weakest of SPY/QQQ/IWM) but the fill quality and exit price worked against the position. Running P&L for IWM: -$1.52.

---

## Open Positions

None.

---

## Closed Trades

### Trade #18 — Short, April 15, 2026

| Field | Value |
|---|---|
| Trade ID | 18 |
| Ticker | IWM |
| Direction | Short |
| Quantity | 4 shares |
| Status | Closed |
| Entry (model) | $268.15 |
| Entry fill | $268.47 |
| Exit fill | $268.85 |
| P&L | **-$1.52** |
| Opened | 2026-04-15 17:52:59 UTC |
| Entered | 2026-04-15 17:54:49 UTC |
| Closed | 2026-04-15 09:30:00 (local) |
| Source run | 20260415_104041 |

**Entry slippage:** The model recommended entry at $268.15; fill came in at $268.47 — a $0.32 slippage per share against the short (entry filled higher than the model's level, meaning the trade started underwater by $1.28 before the market moved). For a short, a higher fill price is adverse.

**Exit analysis:** The model set a stop at $268.85. The exit fill was $268.85 — the stop was hit exactly, confirming the trade was managed by the monitor process and exited cleanly at the stop level. The trade did not reach the model's target of $267.01.

**Why the stop was hit:** IWM's intraday bearish setup was real (8/9 strategies agreed), but the extremely thin volume (relative volume 0.38x–0.55x average) created a low-conviction environment. The one dissenting strategy (dt_news_catalyst) had warned that if the macro risk-on tide lifted all boats, IWM's gap fill would invalidate the short thesis. The stop at $268.85 was above the VWAP ($268.63) and OR high cluster — a defensible level, but on a thin tape a brief squeeze through $268.85 was always a meaningful risk.

**Model confidence at entry:** 55/100 (PM-level), avg 54.7 across all 9 strategies. This was a moderate-confidence trade, not a high-conviction setup. The model's risk-reward was 1.63:1 on paper but adverse fill slippage compressed the effective R:R before the trade was even on.

---

## Trade Scorecard

| Metric | Value |
|---|---|
| Total trades | 1 |
| Direction breakdown | 1 short, 0 long |
| Win rate | 0% (0/1) |
| Average P&L per trade | -$1.52 |
| Realized P&L | -$1.52 |
| Unrealized P&L | $0.00 |
| Net P&L | **-$1.52** |
| Average entry slippage (short) | +$0.32 / share (adverse) |
| Avg model confidence at entry | 55/100 |
| Avg risk-reward (model) | 1.63:1 |
| Stop-outs | 1 (100% of trades) |
| Target hits | 0 |

---

## Lessons and Observations

**1. Thin-tape risk is real for IWM.** On April 15, relative volume was 0.38x–0.55x average — extremely thin. In a thin tape, even a small imbalance can push price through a stop without the predicted directional follow-through. Future IWM daytrade entries should require at minimum 0.6x relative volume before initiating.

**2. Entry slippage on shorts is asymmetric.** For a short, filling higher than the model's entry level means the trade starts with an immediate unrealized loss. The $0.32 slippage on this trade was meaningful relative to the $0.70 stop width ($268.15 to $268.85). Effective stop width after slippage was $0.38 — barely half the model's intended risk. Consider using limit orders timed to the 5m close below OR low rather than market orders.

**3. The directional call was correct in context.** IWM was demonstrably the weakest ETF on April 15: SPY and QQQ held above their respective VWAPs while IWM sat below its VWAP, below all intraday EMAs, and with a bearish SuperTrend reading. The relative weakness signal was valid. The trade failed on execution quality (slippage + thin tape stop-out) rather than thesis error.

**4. Model confidence calibration.** 55/100 confidence with 8/9 bearish strategies is actually a reasonably high signal. The loss outcome here is not sufficient to question the signal — one trade is noise. Track the next 10 IWM daytrade signals before drawing conclusions on confidence calibration.

**5. IWM is daytrade-watchlist only.** Per tracker/watchlist.json, IWM appears in the daytrade watchlist alongside SPY and QQQ. No swing or invest trades are currently planned for IWM. All trades on record are daytrade-mode entries.

---

## Context: Why IWM Is Traded

IWM serves as the small-cap benchmark leg of the three-ETF daytrade basket (SPY / QQQ / IWM). The model runs relative-strength analysis across all three simultaneously and takes the strongest and weakest as long/short pairs when setup conditions allow. On April 15, SPY was the long (8/9 bullish, bought at $697.45) and IWM was the short (8/9 bearish, shorted at $268.47 fill). QQQ was held out as a no-trade (9/9 neutral). This three-way relative comparison is the primary edge the model exploits on IWM.

*All trade data from tracker.db query on 2026-04-29. Run data from 20260415_104041.*
