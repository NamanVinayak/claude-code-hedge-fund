---
name: XOM trades
last_updated: 2026-04-30
last_run_id: 20260430_203923
target_words: 800
stale_after_days: 60
word_count: 849
summary: Three short entries recommended by model (Apr 11, Apr 15/17) — all cancelled/abandoned, no fills. Run 4 (Apr 30) is first non-short decision: HOLD (42 conf) due to earnings blackout and macro regime shift (Iran blockade resumes)
---

# XOM — Trades

## TL;DR

The model recommended shorting XOM in all three runs (Apr 11, Apr 15, Apr 17), always with the same thesis: ceasefire-driven oil unwind, confirmed downtrend, oversold-bounce entry. Two orders were placed in the paper trading system — one cancelled (Apr 12) and one abandoned (Apr 18). Neither filled. No realized P&L on XOM to date.

## Open positions

None. Both paper orders were cancelled/abandoned before fill.

## Closed — last 30 days

None filled.

## Model recommendations — chronological

### Run 1: swing_20260411_211655 (Apr 11, 2026)

**Decision:** SHORT 6 shares at $155.00, target $145.00, stop $160.00

- R:R: 2.0:1 ($10 target distance, $5 stop distance)
- Confidence: 58%
- Timeframe: 5–10 trading days
- Thesis: Sector rotation out of energy (75% confidence). Iran ceasefire reducing geopolitical oil premium. Momentum deceleration strong: ROC 5d -5.1%, 10d -7.8%. CCI at -126. Model noted stochastic at 6 (deeply oversold) and recommended waiting for a bounce to $155 before entering.
- Portfolio context: Energy shorts (XOM + CVX) = 37.8% of $5,000 paper portfolio. Risk manager allowed max $1,022 position. 6 × $155 = $930 (18.6% of capital). Max loss if stop hit: -$30.
- Risk flag from portfolio PM: "If ceasefire collapses, oil spikes and both positions lose simultaneously. Combined energy short exposure 37.8% — monitor closely." [Source: decisions.json swing_20260411_211655]

**Paper order outcome:** Cancelled. DB record: Trade ID 3, 6 shares short, entry price $155.00, status = `cancelled`, created 2026-04-12 04:56:08. No fill price, no P&L.

---

### Run 2: 20260415_110848 (Apr 15, 2026)

**Decision:** SHORT 6 shares at $151.00, target $143.00, stop $154.00

- R:R: 2.67:1 ($8 target distance, $3 stop distance)
- Confidence: 62%
- Timeframe: 5–10 trading days
- Thesis: "Bearish divergence: oil macro bullish on Iran/Hormuz but XOM in confirmed downtrend (daily SuperTrend bearish, 5 consecutive down days, RSI 29.4, MACD -2.32). 6/9 agents bearish. Iran peace talks headwind for oil. Enter on bounce to $151 resistance, stop $154."
- Improvement vs Run 1: Entry price lowered from $155 to $151 (the anticipated bounce materialized). Stop tightened from $160 to $154. R:R improved from 2.0:1 to 2.67:1. [Source: decisions.json 20260415_110848]

**Paper order outcome:** No order record in DB for this specific run/entry. The Apr 17 run placed a new order.

---

### Run 3: 20260417_233350 (Apr 17, 2026)

**Decision:** SHORT 70 shares at $151.97, target $144.00, stop $154.00

- R:R: 3.93:1 ($7.97 target distance, $2.03 stop distance)
- Confidence: 72%
- Timeframe: 5–10 trading days
- Thesis: "Bearish consensus: all ROC negative, sector outflow, EPS -10.3%, uncorrelated (-0.04) diversifier. 3.93:1 R:R on tight stop."
- Notable: Quantity jumped from 6 to 70 shares — this is the larger $100k paper account (vs. the $5k account used in the Apr 11 run). The notional size is 70 × $151.97 = ~$10,638. The model also noted XOM's -0.04 correlation to the rest of the book (mostly tech longs), making it an effective hedge.
- Confidence improved to 72% (from 58% / 62% in earlier runs) — the model's bearish conviction strengthened over the three weeks. [Source: decisions.json 20260417_233350]

**Paper order outcome:** Abandoned. DB record: Trade ID 28, 70 shares short, entry price $151.97, status = `abandoned`, created 2026-04-18 00:18:19. No fill price, no P&L.

---

### Run 4: 20260430_203923 (Apr 30, 2026)

**Decision: HOLD — 42% confidence (first non-short decision in XOM run history)**

```
action:        hold
quantity:      0
entry_price:   null (would be $153.00 on pullback post-earnings)
target_price:  null
stop_loss:     null
risk_reward:   N/A — earnings blackout enforced
timeframe:     reassess after May 1 earnings
```

Source: `runs/20260430_203923/decisions.json`

**Why the direction flipped:** Prior three runs were all bearish (ceasefire unwinding oil premium). US-Iran peace talks stalled as of late April; Goldman raised Brent to $90/bbl; the Iran blockade resumed. The macro_context agent (the only directional vote) is now **bullish** at 58% — a 180° flip from prior runs. The mean_reversion agent is bearish on overbought RSI-7 (79.95) and Fib resistance. Three agents are neutral citing the earnings binary. Net result: 1 bullish / 1 bearish / 3 neutral = no tradeable consensus, earnings blackout blocks entry regardless.

**Risk manager ruling:** Earnings in 1 day — 3-day blackout enforced. Position limit = $0. [Source: 20260430_203923 signals_combined.json risk_management_agent]

**Post-earnings watch (bullish path):** If Q1 earnings are absorbed, macro_context's setup is: entry $153.00 (pullback), target $159.61, stop $150.68, R/R 2.9:1. Do not chase at $154.67. [Source: 20260430_203923 decisions.json portfolio_summary]

---

## Lifetime stats

| Metric | Value |
|---|---|
| Total model recommendations | 4 (3 short, 1 hold) |
| Total paper orders placed | 2 |
| Fills | 0 |
| Realized P&L | $0 |
| Unrealized P&L | $0 |
| Win rate | N/A (no fills) |
| Average model confidence | 58.5% across directional runs (58% / 62% / 72% shorts; 42% hold) |
| Direction consistency | Bearish Apr 11–17; first flip to neutral/macro-bullish Apr 30 |

## Lessons / notes

1. **Order execution gap:** The Apr 12 order (cancelled) and Apr 18 order (abandoned) both failed to fill, likely because they were placed as limit orders at $155 and $151.97 respectively and the stock may not have bounced to those exact levels before the orders expired or were manually cancelled. The model's "enter on the bounce" framing requires active monitoring — limit orders at resistance levels can miss if the bounce falls short.

2. **Model conviction strengthened over time:** Confidence rose from 58% → 62% → 72% across three runs, and R:R improved from 2.0:1 to 3.93:1. Had the orders filled, the later entries offered the best setups.

3. **Correlation benefit:** The Apr 17 run explicitly flagged XOM's -0.04 correlation to the tech-heavy long book, making it a genuine portfolio hedge — not just a standalone trade. This is a recurring pattern worth tracking: energy shorts as tech-book insurance.

4. **Ceasefire risk is the key tail risk:** Every run's risk notes flagged the same scenario — "if the ceasefire collapses, oil re-spikes and the short loses fast." This binary event risk suggests tighter stops and smaller size are warranted even when the trend is clearly bearish.
