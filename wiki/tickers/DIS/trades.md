---
name: DIS trades
last_updated: 2026-05-01
last_run_id: 20260501_221355
target_words: 800
stale_after_days: 60
word_count: 734
summary: No fills confirmed in trade_ledger.json per_ticker_history[DIS]; run 20260501_221355 issued buy decision (2 shares, $102.50 entry, 62% confidence) — pending ledger ingestion; three prior model recommendations, all unexecuted.
---

# DIS — Trades

## TL;DR

`trade_ledger.json` field `per_ticker_history["DIS"]` is empty (`[]`) as of run `20260501_221355` — zero confirmed fills for DIS in the paper trading account. Run `20260501_221355` issued a buy decision (2 shares at $102.50 limit, target $107.11, stop $101.00, 62% confidence, 3.07:1 R/R), but this decision does NOT appear in `per_ticker_history["DIS"]` and therefore has not been confirmed as a fill. It is documented below as a model recommendation pending ledger confirmation. [Hard rule #11: trade_ledger.json is the sole source of truth.]

---

## Open positions

None confirmed. `per_ticker_history["DIS"]` contains zero records as of run `20260501_221355`.

---

## Closed trades

None. No historical DIS fills in the trade ledger.

---

## Run-level model recommendations (not confirmed fills)

### Run: `20260501_221355` — May 1, 2026

**Model recommendation:** BUY 2 shares — DECISION ISSUED, NOT YET CONFIRMED IN LEDGER

| Field | Value |
|---|---|
| Action | buy |
| Quantity | 2 shares |
| Entry price (limit) | $102.50 |
| Target price | $107.11 |
| Stop loss | $101.00 |
| Risk-reward | 3.07:1 |
| Timeframe | 5–10 trading days |
| Confidence | 62% |
| Run date | May 1, 2026 |
| Status | DECISION ONLY — NOT IN PER_TICKER_HISTORY |

**Model reasoning** (from `decisions.json`, run `20260501_221355`): "Head Trader bullish (62), 4/5 swing agents agree. Pre-earnings momentum (May 6–13 catalyst). Apr 30 breakout above $103 on 1.23x vol, MACD bullish cross, ADX 37.34. Limit at $102.50 pullback for 3.07:1 R/R. Stop $101.00 (17-test support). Allowed max qty=2; 2 shares x $102.50 = $205 within 25% cap."

**Agent vote breakdown** (run `20260501_221355`):
- Bullish (4): swing_mean_reversion (52%), swing_breakout (58%), swing_catalyst_news (68%), swing_macro_context (58%)
- Neutral (1): swing_trend_momentum (45%) — EMA tangle / 10d ROC negative, not opposing

**Why not in ledger yet**: Decision was issued by the PM at run time; ingestion into the paper trading account occurs as a separate step. If the $102.50 limit fill is confirmed, this record will be updated.

---

### Run: `20260415_110848` — April 15, 2026

**Model recommendation:** BUY 9 shares — NOT EXECUTED

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

**Why not executed**: Stock was trading at ~$102–103 at signal time — above the $100.50 entry level. The head trader directive was explicit: "do not enter above $103." Limit order never filled. [source: prior bootstrap analysis]

---

### Run: `swing_20260411_211655` — April 11, 2026

**Model recommendation:** HOLD — NO TRADE

| Field | Value |
|---|---|
| Action | hold |
| Entry (indicative) | $99.17 |
| Target (indicative) | $103.00 |
| Stop (indicative) | $95.00 |
| Risk-reward | 0.9:1 |
| Confidence | 42% |
| Run date | April 11, 2026 |
| Status | HOLD — NO TRADE |

**Why held**: R/R of 0.9:1 at $99.17 failed the 2:1 minimum. Downtrend intact but bounce testing resistance; earnings not until May. [source: prior bootstrap analysis]

---

## Model signal trajectory

| Date | Run ID | Price | Model stance | Confidence | Notes |
|---|---|---|---|---|---|
| Apr 11, 2026 | `swing_20260411_211655` | $99.17 | Hold | 42% | R/R 0.9:1 fails; downtrend testing |
| Apr 15, 2026 | `20260415_110848` | ~$102–103 | Cautious buy | 55% | MACD crossover; limit $100.50 missed |
| May 1, 2026 | `20260501_221355` | $103.75 | **Buy** | 62% | Breakout confirmed; May 6 earnings catalyst; 3.07:1 R/R |

Confidence trajectory: 42% → 55% → 62%. Stance trajectory: Hold → Cautious buy → Active buy. Signal flip occurred this run.

---

## Lifetime stats (DIS — confirmed fills only)

| Metric | Value |
|---|---|
| Total confirmed fills | 0 |
| Open positions (confirmed) | 0 |
| Closed positions | 0 |
| Realized P&L | $0.00 |
| Win rate | N/A |
| Model buy signals issued | 2 (Apr 15 unexecuted; May 1 pending confirmation) |
| Model hold signals issued | 1 (Apr 11) |
| Fill rate vs. signaled buys | 0 / 2 confirmed fills |

*Source: `per_ticker_history["DIS"]` from `trade_ledger.json`, run `20260501_221355`. If the May 1 buy fills, update with confirmed entry price from ledger.*
