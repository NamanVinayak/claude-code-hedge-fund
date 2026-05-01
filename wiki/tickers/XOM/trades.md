---
name: XOM trades
last_updated: 2026-05-01
last_run_id: 20260501_203521
target_words: 800
stale_after_days: 60
word_count: 876
summary: Three short entries recommended by model (Apr 11, Apr 15/17) — all cancelled/abandoned, no fills. Run 4 (Apr 30) first non-short: HOLD (42 conf) due to earnings blackout and macro regime shift. Run 5 (May 1) HOLD (35 conf) — earnings printed today (EPS beat), risk manager blackout enforced, panel 1B/2Br/2N deeply divided
---

# XOM — Trades

## TL;DR

The model recommended shorting XOM in all three runs (Apr 11, Apr 15, Apr 17), always with the same thesis: ceasefire-driven oil unwind, confirmed downtrend, oversold-bounce entry. Two orders were placed in the paper trading system — one cancelled (Apr 12) and one abandoned (Apr 18). Neither filled. No realized P&L on XOM to date. Run 4 (Apr 30) and Run 5 (May 1) are both holds — the Iran macro regime shifted and earnings blackouts blocked entry. `per_ticker_history[XOM]` in trade_ledger.json confirms zero fills. [Source: 20260501_203521 trade_ledger.json]

## Open positions

None. `trade_ledger.json per_ticker_history[XOM] = []` — confirmed zero rows as of run 20260501_203521.

## Closed — last 30 days

None filled.

## Closed — older, rolled by month

None.

## Closed — older than 6 months

None.

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
- Confidence improved to 72% (from 58% / 62% in earlier runs). [Source: decisions.json 20260417_233350]

**Paper order outcome:** Abandoned. DB record: Trade ID 28, 70 shares short, entry price $151.97, status = `abandoned`, created 2026-04-18 00:18:19. No fill price, no P&L.

---

### Run 4: 20260430_203923 (Apr 30, 2026)

**Decision: HOLD — 42% confidence (first non-short decision in XOM run history)**

```
action:        hold
quantity:      0
entry_price:   null (watch $153.00 pullback post-earnings)
target_price:  null
stop_loss:     null
risk_reward:   N/A — earnings blackout enforced
timeframe:     reassess after May 1 earnings
```

**Why the direction flipped:** US-Iran peace talks stalled as of late April; Goldman raised Brent to $90/bbl; the Iran blockade resumed. The macro_context agent flipped to bullish (58%). However: mean_reversion bearish (RSI-7 79.95, Fib 61.8% resistance), three agents neutral, earnings blackout (1 day). Net: 1 bullish / 1 bearish / 3 neutral = no tradeable consensus. [Source: 20260430_203923 decisions.json, signals_combined.json]

---

### Run 5: 20260501_203521 (May 1, 2026)

**Decision: HOLD — 35% confidence**

```
action:        hold
quantity:      0
entry_price:   null
target_price:  null (watch level $159.61 if breakout)
stop_loss:     null ($150.50 would be the stop in a hypothetical entry)
risk_reward:   1.7:1 (below 2:1 minimum — additional blocker)
timeframe:     neutral — monitor post-earnings clarity post-blackout
```

Source: `runs/20260501_203521/decisions.json`

**Context:** Q1 2026 earnings printed today before market open: non-GAAP EPS $1.16 beat consensus $1.02 by 15.1%. Despite the beat, the risk manager's 3-day blackout is enforced (0 days to earnings = blackout active). Beyond the blackout: panel is 1 bullish (catalyst_news 55) / 2 bearish (mean_reversion 42, trend_momentum 40) / 2 neutral (breakout 35, macro_context 35). Iran peace talks advancing on May 1 with WTI -2% — macro_context agent flags this as the dominant headwind, as the oil-supply-shock thesis that drove the Apr bounce is being actively unwound. R/R at best is 1.7:1 (entry $154.67, target $159.61, stop $150.50) — below the 2:1 minimum. [Source: 20260501_203521 decisions.json reasoning, signals_combined.json risk_management_agent]

**Outcome of prior watch scenario:** Run 4 said "watch $153 pullback post-earnings." Post-earnings price is at $154.67 — the pullback to $153 has not materialized. Price stalled at resistance rather than breaking through or dipping to the entry zone. The post-earnings setup remains unresolved.

---

## Lifetime stats

| Metric | Value |
|---|---|
| Total model recommendations | 5 (3 short, 2 hold) |
| Total paper orders placed | 2 |
| Fills | 0 |
| Realized P&L | $0 |
| Unrealized P&L | $0 |
| Win rate | N/A (no fills) |
| Average model confidence | 57.4% across directional runs (58% / 62% / 72% shorts; 42% / 35% holds) |
| Direction consistency | Bearish Apr 11–17; neutral/macro-bullish Apr 30; neutral/conflicted May 1 |

## Lessons / notes

1. **Order execution gap:** The Apr 12 order (cancelled) and Apr 18 order (abandoned) both failed to fill, likely because they were placed as limit orders at $155 and $151.97 respectively and the stock may not have bounced to those exact levels before the orders expired or were manually cancelled.

2. **Iran macro is the dominant variable.** Every regime shift in XOM's run history traces back to Iran: Apr 11–17 bearish (ceasefire driving oil down), Apr 30 neutral-bullish (blockade resumed, Goldman $90/bbl), May 1 conflicted (peace talks active, WTI -2%). XOM is essentially an Iran-geopolitical bet proxied through oil prices.

3. **DCF consistently shows overvaluation.** Valuation agent signals bearish at 100% confidence across runs (market cap $635B vs DCF $460B, -27.5% gap). This is a structural constraint on the bull thesis ceiling.

4. **Post-blackout watch setup:** Once the 3-day blackout lifts (~May 4), the first directional signal will be key: close above $155.89 on 1.5x+ volume targets ~$164.12 (breakout bull case); hold at $151.34 with consolidation enables a base-build entry; close below $151.34 reopens the mean-reversion short toward $147.66–$148.
