---
name: BAC trades
last_updated: 2026-04-30
last_run_id: 20260430_190826
target_words: 800
stale_after_days: 60
word_count: 648
summary: Full trade journal for BAC — 1 open position (15 shares at $52.75, Apr 30 2026); prior model decisions documented
---

## TL;DR

BAC has one open position: 15 shares entered at $52.75 on April 30, 2026 (run `20260430_190826`). This is the first confirmed executed trade in the paper trading system. Target $55.40 (+$2.65/share), stop $51.50 (-$1.25/share), R/R 2.12:1. Capital deployed: $791.25. Timeframe: 5–10 trading days.

---

## Open Positions

### Trade: BUY 15 shares BAC — run `20260430_190826`

| Field | Value |
|---|---|
| Action | **BUY** |
| Quantity | 15 shares |
| Entry price | $52.75 |
| Target price | $55.40 |
| Stop loss | $51.50 |
| Risk-reward | 2.12:1 |
| Timeframe | 5–10 trading days |
| Confidence | 55% |
| Capital deployed | $791.25 |
| Date entered | 2026-04-30 |
| Run | `20260430_190826` |

**Setup:** EMA pullback dip-buy. Price retraced from $55.40 swing high to the 10/21 EMA confluence at $52.73–$52.88 with RSI-7 hitting 30.4 (short-term oversold). ADX 54.8 — exceptional trend strength. Head Trader bullish (55 conf); 3/5 swing agents agree (trend_momentum 58, mean_reversion 60, breakout 38). Risk manager limit $806; 15 shares fits within limit.

**Key risks:** OBV divergence (institutions distributing into the rally), Berkshire Hathaway ongoing stake reduction, negative 5d/10d ROC still confirming pullback.

**Expected outcomes:**
- If target hit: 15 × ($55.40 − $52.75) = **+$39.75**
- If stop hit: 15 × ($52.75 − $51.50) = **−$18.75**

**Exit instructions:** Hard exit if daily close below $51.50. Target exit at $55.40. Review on any Berkshire 13-F filing or material OBV re-convergence.

---

## Model Decision Log

### Run `20260430_190826` — Swing, April 30, 2026

| Field | Value |
|---|---|
| Action | **BUY** |
| Quantity | 15 shares |
| Entry | $52.75 |
| Target | $55.40 |
| Stop | $51.50 |
| R/R | 2.12:1 |
| Confidence | 55% |
| Agent vote | 3/5 bullish (trend_momentum, mean_reversion, breakout); 2 neutral (catalyst_news, macro_context) |

Decision: "Head Trader bullish (55 conf), 3/5 swing agents agree. Pullback to 10/21 EMA confluence at $52.73-52.88 in ADX-54.8 uptrend. R/R 2.12:1 meets threshold. Risk mgr limit $806; 15 shares @ $52.75 = $791 within limit." [decisions.json, run `20260430_190826`]

---

### Run `20260415_110848` — Swing, April 15, 2026

| Field | Value |
|---|---|
| Action | **BUY** |
| Quantity | 18 shares |
| Entry | $53.00 |
| Target | $57.00 |
| Stop | $51.50 |
| R/R | 2.67:1 |
| Confidence | 65% |

Decision: "Cleanest earnings catalyst: best Q1 in nearly 2 decades, zero trading loss days, profit +17%. 5/9 agents bullish. RSI 78.6, ADX 40. Entry on pullback to $53 (prior resistance-turned-support)." Execution status unconfirmed in paper system (bootstrap note).

---

### Run `swing_20260411_211655` — Swing, April 11, 2026

| Field | Value |
|---|---|
| Action | **HOLD** |
| Quantity | 0 |
| Entry reference | $52.54 |
| R/R | 1.0:1 |
| Confidence | 40% |

Decision: RSI 79.0 — overbought. Volume 0.66x. R:R 1.0:1 fails 2:1 minimum. Agent split 4 bull / 4 neutral-bear. Clear hold. [run `swing_20260411_211655`, decisions.json]

---

## Closed Trades

None. No BAC trades have been closed in the paper trading system.

---

## Lifetime Statistics

| Metric | Value |
|---|---|
| Total confirmed open positions | 1 |
| Closed trades | 0 |
| Realized P&L | $0.00 |
| Win rate | N/A |
| Average hold time | N/A |
| Runs analyzed | 3 (Apr 11, Apr 15, Apr 30) |
| Model buy signals | 2 (Apr 15, Apr 30) |
| Model hold signals | 1 (Apr 11) |
| Model short signals | 0 |

Source: `tracker.db` + decisions.json run `20260430_190826`. Update when position is closed.
