---
name: DIS trades
last_updated: 2026-05-04
last_run_id: 20260504_221111
target_words: 800
stale_after_days: 60
word_count: 791
summary: 1 confirmed open long — id 117, 2 shares filled at $103.495 on 2026-05-01 (run 20260501_221355); near stop $101.00 ahead of May 6 earnings binary; three prior model recommendations (2 unexecuted, 1 hold).
---

# DIS — Trades

## TL;DR

`trade_ledger.json per_ticker_history["DIS"]` as of run `20260504_221111` contains **1 confirmed fill**: trade id 117, 2 shares long, filled at $103.495 on 2026-05-01 (entered at 13:39 UTC). Status: "entered" — open. Stop $101.00, target $107.11, R/R 3.07:1. As of May 4 (hourly price $101.31), the position is $0.50 above its stop, with May 6 earnings binary as the next resolution event. All claims below are sourced from `per_ticker_history["DIS"]` (hard rule #11). [source: `trade_ledger.json`, run `20260504_221111`]

---

## Open positions

### Trade ID 117 — Long 2 shares — OPEN

| Field | Value |
|---|---|
| Trade ID | 117 |
| Ticker | DIS |
| Direction | Long |
| Quantity | 2 shares |
| Status | **entered (open)** |
| Entry price (model) | $102.50 |
| Entry fill price | **$103.495** |
| Exit fill price | None |
| Realized P&L | None (open) |
| Stop loss | $101.00 |
| Target price | $107.11 |
| Risk-reward | 3.07:1 |
| Timeframe | 5–10 trading days |
| Confidence | 62% |
| Created at | 2026-05-01T22:41:01+00:00 |
| Entered at | **2026-05-01T13:39:00+00:00** |
| Run ID | `20260501_221355` |
| Last checked | 2026-05-04T19:59:00+00:00 |

**Context**: Filled at $103.495 — slightly above the $102.50 model limit, within the 1.0% tolerance band. Decision was issued by the PM at run `20260501_221355` (4/5 swing agents bullish, ADX 37.34, April 30 breakout above $103 on 1.23x volume, earnings May 6 catalyst). As of May 4, the position is near its stop ($101.31 hourly price vs. $101.00 stop) after the breakout was fully retraced. Earnings binary on May 6 is the resolution catalyst. [source: `trade_ledger.json per_ticker_history["DIS"]`, run `20260504_221111`]

**Prior trades.md note corrected**: The May 1 trades.md stated "per_ticker_history[DIS] is empty as of run 20260501_221355 — zero confirmed fills." The current ledger as of run `20260504_221111` shows id 117 confirmed with fill price $103.495, status "entered." This confirms the fill occurred — the ledger lag from the May 1 write has now resolved.

---

## Closed trades

None. No historical DIS fills have been closed.

---

## Run-level model recommendations (not confirmed fills)

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
| Status | NOT EXECUTED |

**Why not executed**: Stock was trading at ~$102–103 at signal time — above the $100.50 entry level. Head trader directive: "do not enter above $103." Limit order never filled.

---

### Run: `swing_20260411_211655` — April 11, 2026

**Model recommendation:** HOLD — NO TRADE

| Field | Value |
|---|---|
| Action | hold |
| Entry (indicative) | $99.17 |
| Risk-reward | 0.9:1 |
| Confidence | 42% |
| Status | HOLD — NO TRADE |

**Why held**: R/R of 0.9:1 at $99.17 failed the 2:1 minimum. Downtrend intact but bounce testing resistance; earnings not until May.

---

## Model signal trajectory

| Date | Run ID | Price | Model stance | Confidence | Notes |
|---|---|---|---|---|---|
| Apr 11, 2026 | `swing_20260411_211655` | $99.17 | Hold | 42% | R/R 0.9:1 fails; downtrend testing |
| Apr 15, 2026 | `20260415_110848` | ~$102–103 | Cautious buy | 55% | MACD crossover; limit $100.50 missed |
| May 1, 2026 | `20260501_221355` | $103.75 | **Buy** | 62% | Breakout confirmed; May 6 earnings catalyst; 3.07:1 R/R |
| May 4, 2026 | `20260504_221111` | $101.31 | **Hold** | 42% | Earnings blackout enforced; R/R N/A; no new entry |

---

## Lifetime stats (DIS — confirmed fills only)

| Metric | Value |
|---|---|
| Total confirmed fills | 1 |
| Open positions (confirmed) | 1 (id 117, 2 shares long at $103.495) |
| Closed positions | 0 |
| Realized P&L | $0.00 (open trade, no exit) |
| Win rate | N/A (no closed trades) |
| Model buy signals issued | 3 (Apr 15 unexecuted; May 1 filled at $103.495; May 4 hold) |
| Fill rate vs. signaled buys | 1 / 2 actionable signals (Apr 15 missed level; May 1 filled) |

*Source: `per_ticker_history["DIS"]` from `trade_ledger.json`, run `20260504_221111`. Update with exit fill price and P&L after May 6 earnings resolves position.*
