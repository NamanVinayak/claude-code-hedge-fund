---
name: DIS trades
last_updated: 2026-05-06
last_run_id: 20260505_220625
target_words: 800
stale_after_days: 60
word_count: 865
summary: 1 confirmed closed trade — id 117, 2 shares long, filled $103.495 on 2026-05-01, stopped out $101.00 on 2026-05-05, realized P&L -$4.99; three prior model recommendations (2 unexecuted, 1 hold); no open positions.
---

# DIS — Trades

## TL;DR

`trade_ledger.json per_ticker_history["DIS"]` as of run `20260505_220625` contains **1 confirmed fill**: trade id 117, 2 shares long, filled at $103.495 on 2026-05-01, **stopped out at $101.00 on 2026-05-05**, realizing **-$4.99 P&L**. Status: "stop_hit" — closed. No open DIS positions remain. All claims below are sourced from `per_ticker_history["DIS"]` (hard rule #11). [source: `trade_ledger.json`, run `20260505_220625`]

---

## Open positions

None. All DIS positions are closed as of 2026-05-05.

---

## Recently Closed

### Trade: LONG 2 shares DIS — CLOSED 2026-05-05

| Field | Value |
|---|---|
| Entry price | $103.495 (fill) |
| Exit price | $101.00 |
| P&L | -$4.99 |
| Closed via | stop_hit |
| Days held | 4 (2026-05-01 → 2026-05-05) |
| Run | `20260501_221355` (decision) / `20260505_220625` (closure confirmed) |

---

## Closed — May 2026

### Trade ID 117 — Long 2 shares — CLOSED at loss

| Field | Value |
|---|---|
| Trade ID | 117 |
| Ticker | DIS |
| Direction | Long |
| Quantity | 2 shares |
| Status | **stop_hit (closed)** |
| Entry price (model) | $102.50 |
| Entry fill price | **$103.495** |
| Exit fill price | **$101.00** |
| Realized P&L | **-$4.99** |
| Stop loss | $101.00 |
| Target price | $107.11 (never reached) |
| Risk-reward (model) | 3.07:1 |
| Timeframe | 5–10 trading days |
| Confidence | 62% |
| Created at | 2026-05-01T22:41:01+00:00 |
| Entered at | **2026-05-01T13:39:00+00:00** |
| Closed at | **2026-05-05T14:09:00+00:00** |
| Run ID (decision) | `20260501_221355` |
| Run ID (closure confirmed) | `20260505_220625` |

**What happened**: The May 1 model identified a pre-earnings breakout thesis — April 30 close above $103 on 1.23x volume, ADX 37.34, MACD bullish cross. Decision: 2 shares long at $102.50 limit (filled at $103.495 with 1% tolerance), target $107.11, stop $101.00, 3.07:1 R/R, confidence 62%, run `20260501_221355`. The breakout from $104.83 (post-fill high) fully retraced over the following 4 trading days as macro headwinds (Iran escalation May 4, WTI ~$105, Dow -557 pts) reversed the risk-on environment. By May 5 the hourly price reached $100.48, triggering the $101.00 stop and closing the position at -$4.99 ($2.495 per share × 2 shares).

**Context**: The May 1 decision carried 4/5 swing agent bullish votes and is the first DIS fill in portfolio history. The $103.75 breakout close on April 30 that anchored the thesis had a volume of 1.23x — below the ideal 1.5x threshold. The position's maximum favorable excursion (MFE) was limited; it entered at $103.495 with a post-fill high of approximately $104.83 (the April 30 breakout high) before beginning to retrace. All 5 swing agents were neutral at the time of the stop-out, citing earnings binary and a stock falling into the print.

**Lesson**: The breakout was real but the volume confirmation was weak (1.23x vs. 1.5x threshold). Entering near a 3-day earnings blackout on a sub-threshold volume breakout extracts premium risk for the binary event. The April 30 macro tailwind (Iran peace talks, WTI -2%) that supported the thesis was reversed by May 4 Iranian escalation — a rapid geopolitical reversal that is now recorded as a falsified macro assumption.

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
| May 1, 2026 | `20260501_221355` | $103.75 | **Buy** | 62% | Breakout confirmed; May 6 earnings catalyst; 3.07:1 R/R; filled at $103.495 |
| May 4, 2026 | `20260504_221111` | $101.31 | **Hold** | 42% | Earnings blackout enforced; near stop; no new entry |
| May 5, 2026 | `20260505_220625` | $101.31 | **Hold** | 20% | Stop hit during session; all 5 agents neutral (earnings binary) |

---

## Lifetime stats (DIS — confirmed fills only)

| Metric | Value |
|---|---|
| Total confirmed fills | 1 |
| Open positions (confirmed) | 0 |
| Closed positions | 1 (id 117, stop_hit) |
| Realized P&L | **-$4.99** |
| Win rate | 0W / 1L (0%) |
| Model buy signals issued | 3 (Apr 15 unexecuted; May 1 filled at $103.495; May 4/5 hold) |
| Fill rate vs. signaled buys | 1 / 2 actionable signals (Apr 15 missed level; May 1 filled) |
| Avg holding period (closed) | 4 calendar days (May 1 → May 5) |

*Source: `per_ticker_history["DIS"]` from `trade_ledger.json`, run `20260505_220625`. Last updated by wiki_daily_lesson_writer 2026-05-06. Next update after May 6 earnings resolves post-earnings entry decision.*
