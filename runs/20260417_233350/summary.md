# Swing Trading Run — Top 3 Trade Setups

**Run ID:** `20260417_233350`
**Date:** 2026-04-17
**Universe:** AAPL, MSFT, TSLA, NVDA, META, GOOGL, AMZN, AMD, JPM, GS, NKE, XOM, SPY, QQQ
**Mode:** swing (2-20 day holds)

Decisions were synthesized across 9 swing strategy agents (trend, pullback, breakout, momentum, mean-reversion, catalyst, sector, Druckenmiller, news) plus deterministic fundamentals/technicals/valuation/sentiment/risk agents. Trades below are ranked by conviction × risk/reward.

---

## 1. QQQ — BUY (highest reward-to-risk)

- **Entry:** ~$640.47
- **Target:** $668.00 (+4.3%)
- **Stop:** $634.00 (-1.0%)
- **Risk/Reward:** 4.25 : 1
- **Timeframe:** 8-12 trading days
- **Confidence:** 72%

**Why:** QQQ is the cleanest expression of the tech uptrend gripping the universe. The sector-rotation agent flagged technology as the top-flowing sector (confidence 83%), and the trend-follower/breakout/momentum strategies all aligned bullish. The call is to keep size modest: QQQ is 96% correlated with SPY and overlaps heavily with our single-name tech longs (NVDA, MSFT, AMZN, META, GOOGL), so the position doubles as a market beta vehicle rather than an independent bet. Stop is placed just below the recent swing pivot; a break there would signal the whole tech complex is rolling over.

---

## 2. XOM — SHORT (highest-conviction contrarian trade)

- **Entry:** ~$151.97
- **Target:** $144.00 (-5.2%)
- **Stop:** $154.00 (+1.3%)
- **Risk/Reward:** 3.93 : 1
- **Timeframe:** 5-10 trading days
- **Confidence:** 72%

**Why:** Energy is the mirror image of tech in this snapshot — every momentum window (5/10/21-day ROC) is negative, the sector-rotation agent flags outflows, and EPS is down 10.3% year-over-year. Druckenmiller-style macro also sides bearish. Crucially, XOM's return is essentially **uncorrelated** (-0.04) with the rest of the book, so the short earns its keep as a hedge against the tech-heavy long side as well as on its own merits. The tight $2 stop limits downside if oil catches a geopolitical bid; the 3.93 R:R gives the trade plenty of runway.

---

## 3. AMD — BUY (strongest momentum, but size managed)

- **Entry:** ~$278.26
- **Target:** $305.00 (+9.6%)
- **Stop:** $270.00 (-3.0%)
- **Risk/Reward:** 3.24 : 1
- **Timeframe:** 7-12 trading days
- **Confidence:** 70%

**Why:** AMD is the runaway momentum leader — 21-day ROC of 41.7% put it at the top of the universe ranking, and the sector-rotation agent confirmed semiconductor inflows. The catch: daily RSI is 91 and the hourly Schaff Trend Cycle just crossed down, flagging a meaningful pullback risk inside the larger uptrend. The portfolio manager responded by sizing small (~$4.2k notional) and keeping the stop tight below recent support. We accept the statistical risk of a short-term mean-reversion shakeout in exchange for the asymmetric upside if the thrust continues.

---

## Portfolio context

The full book is 10 longs / 2 shorts / 2 holds with ~75% gross exposure. Tech longs are intentionally under-sized because of 0.67-0.96 pairwise correlations with QQQ and SPY — double-counting tech beta is the single biggest risk flag. XOM and NKE shorts (energy and apparel) add negatively-correlated ballast. TSLA and GS are held flat: TSLA shows conflicting daily/hourly signals; GS has weak daily ADX (20.7) and cannot produce a clean 2:1 setup. All enforced trades clear a minimum R:R of 2.0.

See `decisions.json`, `signals/swing_head_trader.json`, and `explanation.json` for full detail.
