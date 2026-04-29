---
name: BAC trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 612
summary: Full trade history and run decisions for BAC; no executed trades in tracker.db as of bootstrap
---

## TL;DR

No BAC trades have been executed and recorded in tracker.db. The system has analyzed BAC twice in swing mode — April 11 (hold, overbought) and April 15 (buy signal generated). The April 15 buy decision was placed by the model but execution status in the paper trading system is unconfirmed in this bootstrap. Lifetime P&L: $0 realized, 0 closed trades.

---

## Open Positions

**None recorded in tracker.db as of 2026-04-29.**

---

## Model Decisions (Run Archive)

These are the raw model outputs. They become executed trades only when `tracker execute` is run against the run ID. Execution status is unverified in this bootstrap.

### Run `20260415_110848` — Swing, April 15, 2026

| Field | Value |
|---|---|
| Action | **BUY** |
| Quantity | 18 shares |
| Entry price | $53.00 |
| Target price | $57.00 |
| Stop loss | $51.50 |
| Risk-reward | 2.67:1 |
| Timeframe | 6–10 trading days |
| Confidence | 65% |
| Agent vote | 5 of 9 bullish |

**Decision reasoning (from `decisions.json`):** "Cleanest earnings catalyst: best Q1 in nearly 2 decades, zero trading loss days, profit +17%. 5/9 agents bullish. RSI 78.6, ADX 40, squeeze bullish breakout. Entry on pullback to $53 (prior resistance-turned-support). Iran peace talks tailwind for financials."

**Expected P&L if target hit:** 18 shares × ($57.00 − $53.00) = **+$72.00**
**Maximum loss if stop hit:** 18 shares × ($53.00 − $51.50) = **−$27.00**
**Position notional at entry:** 18 × $53 = **$954** (19.1% of $5,000 paper portfolio)

---

### Run `swing_20260411_211655` — Swing, April 11, 2026

| Field | Value |
|---|---|
| Action | **HOLD** |
| Quantity | 0 |
| Entry reference | $52.54 |
| Target reference | $55.00 |
| Stop reference | $50.00 |
| Risk-reward | 1.0:1 |
| Confidence | 40% |
| Agent vote | 4 bull vs 4 neutral/bear |

**Decision reasoning (from `decisions.json`):** "Head Trader neutral at 45% with near-even agent split (4 bull vs 4 neutral/bear). RSI at 79.0 — most overbought of all financials. Volume only 0.66x. Multiple analysts cut price targets. R:R at 1.0:1 fails the 2:1 minimum. Clear hold."

**Key difference between the two runs:** The April 11 run identified that BAC was already overbought (RSI 79.0) pre-earnings and the 1.0:1 risk-reward ratio didn't qualify for a trade. Four days later, after the earnings beat confirmed the fundamental catalyst, the system upgraded to a buy with a 2.67:1 risk-reward at the same general price area ($52–53), justified by the now-confirmed earnings story providing a new risk framework.

---

## Closed Trades

**None.** tracker.db query returned 0 rows for BAC as of bootstrap date 2026-04-29.

---

## Lifetime Statistics

| Metric | Value |
|---|---|
| Total trades executed | 0 |
| Open positions | 0 |
| Closed trades | 0 |
| Realized P&L | $0.00 |
| Win rate | N/A |
| Average hold time | N/A |
| Entry hit rate | N/A |
| Runs analyzed | 2 (Apr 11, Apr 15) |
| Model buy signals | 1 (Apr 15 run) |
| Model hold signals | 1 (Apr 11 run) |
| Model short signals | 0 |

---

## Notes for Next Run

1. If a BAC position was opened from the April 15 run, the entry target was $53.00. Verify fill status by checking Moomoo paper account or running `python -m tracker status`.
2. The April 15 stop at $51.50 defines the invalidation level for the swing thesis. A close below $51.50 means exit and re-evaluate.
3. The target is $57.00. If the stock reaches $57 within 10 trading days of a fill, that is a win to close out.
4. After any close, update this file with: fill price, exit price, hold days, realized P&L, and whether the stop or target was hit.
5. The model has never shorted BAC. Both runs generated either hold or buy signals, consistent with the broadly bullish analyst consensus and NII tailwind thesis.
