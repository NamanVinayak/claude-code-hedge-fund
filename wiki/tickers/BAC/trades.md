---
name: BAC trades
last_updated: 2026-05-06
last_run_id: 20260506_190825
target_words: 800
stale_after_days: 60
word_count: 696
summary: SELL decision issued for 15-share long (id 110, $52.75 cost basis) at market ~$53.72 on May 6 2026; exit fill NOT YET confirmed in trade_ledger.json per_ticker_history[BAC] — id 110 status still "entered"; decision documented per hard rule #11
---

## TL;DR

PM issued SELL on 15 shares of BAC (id 110) at market (~$53.72) on May 6, 2026, run `20260506_190825`. **Per trade_ledger.json `per_ticker_history[BAC]`, id 110 status is still "entered" (exit_fill_price null, closed_at null) as of this run's ledger snapshot.** The exit fill has not yet been confirmed in the tracker system. This page documents the decision; the confirmed closed entry will appear after fill confirmation in the next ledger update.

---

## Open Positions (as of ledger snapshot, run `20260506_190825`)

### Trade id 110: LONG 15 shares BAC — run `20260430_190826`

| Field | Value |
|---|---|
| Ledger ID | 110 |
| Action | BUY (entered Apr 30 2026) |
| Quantity | 15 shares |
| Entry fill price | $52.75 |
| Target price | $55.40 |
| Stop loss | $51.50 |
| Risk-reward | 2.12:1 |
| Timeframe | 5–10 trading days |
| Confidence | 55% |
| Capital deployed | $791.25 |
| Date entered | 2026-04-30 |
| Status (ledger) | entered — exit fill NOT yet confirmed |
| Run | `20260430_190826` |

**Exit decision issued (run `20260506_190825`):** PM issued SELL at market (~$53.72). Proactive exit — position up ~$14.55 unrealized (~+1.8%) but forward R/R 0.75:1 fails 2:1 minimum. Bearish DI crossover, OBV distribution on both timeframes, and unanimous 5/5 neutral swing agents drove the decision. Trade_ledger.json per_ticker_history[BAC] for this run still shows status "entered" — exit fill not confirmed. [decisions.json, trade_ledger.json, run `20260506_190825`]

**Exit fill (when confirmed):**
- If exited near $53.72 (decision price): 15 × ($53.72 − $52.75) = **+$14.55**
- If stop had hit at $51.50 (did not occur): 15 × ($52.75 − $51.50) = **−$18.75**

---

## Model Decision Log

### Run `20260506_190825` — Swing, May 6, 2026

| Field | Value |
|---|---|
| Action | **SELL** (exit existing long) |
| Quantity | 15 shares (full position) |
| Exit price (decision) | ~$53.72 market |
| Prior entry | $52.75 |
| Confidence | 30% |
| Agent vote | 5/5 neutral |

Decision: "Unanimous 5/5 neutral; OBV distribution divergence daily+hourly; bearish DI crossover; valuation agent 100-conf bearish (-35.8% overvalued); R/R ~0.75:1 fails 2:1 rule. Exit existing 15-share long at market." [decisions.json, run `20260506_190825`]

---

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
| Agent vote | 3/5 bullish (trend_momentum, mean_reversion, breakout); 2 neutral |

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
| Entry reference | $52.54 |
| R/R | 1.0:1 |
| Confidence | 40% |

Decision: RSI 79.0 — overbought. Volume 0.66x. R/R 1.0:1 fails 2:1 minimum. [run `swing_20260411_211655`]

---

## Closed Trades

None confirmed in trade_ledger.json per_ticker_history[BAC] as of run `20260506_190825`. The SELL decision (id 110 exit) has been issued but the exit_fill_price remains null in the ledger snapshot. Update when fill confirmed.

---

## Lifetime Statistics

| Metric | Value |
|---|---|
| Total confirmed open positions | 1 (pending close confirmation) |
| Closed trades (confirmed) | 0 |
| Realized P&L | $0.00 (exit fill pending) |
| Unrealized P&L at decision (~$53.72 exit) | +$14.55 |
| Win rate | N/A (no confirmed closed trades) |
| Runs analyzed | 4 (Apr 11, Apr 15, Apr 30, May 6) |
| Model buy signals | 2 (Apr 15, Apr 30) |
| Model hold signals | 1 (Apr 11) |
| Model sell signals | 1 (May 6) |

Source: trade_ledger.json per_ticker_history[BAC], run `20260506_190825`. Update when exit fill confirmed in ledger.
