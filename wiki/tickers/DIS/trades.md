---
name: DIS trades
last_updated: 2026-04-29
last_run_id: 20260429_220825
target_words: 800
stale_after_days: 60
word_count: 801
summary: first DIS buy signal issued Apr 29 at $101.50 for 192 shares; prior two runs (hold Apr 11, cautious buy Apr 15) never executed; lifetime record: 0 closed trades, 1 open position pending
---

# DIS — Trades

## TL;DR

As of run `20260429_220825` (April 29, 2026), DIS has its first active buy signal: 192 shares at $101.50, target $107.11, stop $100.20, R/R 4.3:1, confidence 62%. This is a pre-earnings mean-reversion trade at the 38.2% Fib + 15-test support confluence ahead of Q2 FY2026 earnings on May 6. Prior runs (Apr 11 hold, Apr 15 cautious buy never executed) are documented below. Zero closed trades in tracker.db to date.

---

## Open positions

### Model recommendation — BUY 192 shares (run `20260429_220825`)

| Field | Value |
|---|---|
| Run ID | `20260429_220825` |
| Action | buy |
| Quantity | 192 shares |
| Entry price (model) | $101.50 |
| Target price | $107.11 |
| Stop loss | $100.20 |
| Risk-reward | 4.3:1 |
| Timeframe | 5–12 trading days |
| Confidence | 62% |
| Notional value | $19,488 (192 × $101.50) |
| Capital at risk | $249.60 (192 × $1.30 stop distance) |
| Run date | 2026-04-29 |
| Status | PENDING EXECUTION |

**Model reasoning** (source: `runs/20260429_220825/decisions.json`): "3/5 strategy agents bullish; Head Trader confidence 62. 38.2% Fib ($101.41) + 15-test volume-confirmed support ($101.02) confluence. Q2 FY2026 earnings catalyst in 5-10 days, Q1 beat, streaming +72% YoY. R/R 4.3:1 ($5.61 upside / $1.30 downside). RSI-7 at 9.15 extreme oversold at support; daily MACD still positive. Wait for hourly stabilization before entry — abort if $100.50 breaks on volume."

**Agent vote breakdown** (`20260429_220825`):
- Bullish (3): swing_mean_reversion (72% confidence), swing_catalyst_news (62%), swing_macro_context (62%)
- Neutral (2): swing_breakout (30%), swing_trend_momentum (25%)
- Bearish: none

**Execution note**: Wait for hourly reversal candle or stabilization at $100.61–$101.02 support zone before entry. If price breaks below $100.50 on volume before entry, stand aside — next support at $98.45. Position is sized to risk manager's $19,499 limit (19.5% of capital).

---

## Closed trades

None. No historical DIS closes in tracker.db.

---

## Prior run model recommendations (not executed)

### Run `20260415_110848` — April 15, 2026

**Model recommendation:** BUY 9 shares (cautious, not executed)

| Field | Value |
|---|---|
| Action | buy |
| Quantity | 9 shares |
| Entry price | $100.50 (limit) |
| Target price | $108.00 |
| Stop loss | $97.50 |
| Risk-reward | 2.5:1 |
| Timeframe | 7–12 trading days |
| Confidence | 55% |
| Status | NOT EXECUTED — stock above entry at $102–103 when signal generated |

**Why not executed**: Stock was at $102–103 when signal generated; limit order at $100.50 required a pullback that occurred later (April 29). Head trader specified "do not enter above $103." The April 29 run is the entry window that prior run anticipated.

---

### Run `swing_20260411_211655` — April 11, 2026

**Model recommendation:** HOLD (no trade)

| Field | Value |
|---|---|
| Action | hold |
| Entry (indicative) | $99.17 |
| Target (indicative) | $103.00 |
| Stop (indicative) | $95.00 |
| Risk-reward | 0.9:1 (below 2:1 threshold) |
| Confidence | 42% |
| Status | HOLD — NO TRADE |

**Why held**: R/R of 0.9:1 at April 11 price ($99.17) failed the 2:1 minimum. DIS was testing the prior downtrend but lacking enough remaining upside to the $103 target vs. downside to $95 stop.

---

## Signal trajectory

| Date | Run ID | Price | Model stance | Confidence | Key change |
|---|---|---|---|---|---|
| Apr 11, 2026 | `swing_20260411_211655` | $99.17 | Hold | 42% | R/R 0.9:1 fails |
| Apr 15, 2026 | `20260415_110848` | ~$102–103 | Cautious buy | 55% | MACD crossover, ADX 31; entry at $100.50 — stock above entry |
| Apr 29, 2026 | `20260429_220825` | $101.30 | **Buy** | 62% | Pulled back to Fib/support confluence + confirmed earnings May 6 |

---

## Lifetime stats (DIS only)

| Metric | Value |
|---|---|
| Total executions | 0 (pending) |
| Open positions | 1 (model recommendation, pending execution) |
| Closed positions | 0 |
| Realized P&L | $0.00 |
| Win rate | N/A |
| Model buy signals | 2 (Apr 15, Apr 29) |
| Model hold signals | 1 (Apr 11) |
| Executed vs. signaled | 0/2 executed (Apr 15 was limit that required pullback; Apr 29 pending) |

---

## Notes for active trade management

1. **Abort trigger**: Close below $100.50 on volume before earnings. Do not hold through stop hoping for bounce.
2. **Earnings management**: Q2 FY2026 reports May 6. Hold through earnings given the setup is specifically a pre-earnings catalyst trade. If Q2 disappoints on streaming margin, exit at open.
3. **Target**: $107.11 (prior swing high, 15-test resistance). Consider partial exit at $105 if hourly shows exhaustion signals before full target.
4. **Blackout**: Risk manager enforces 3-day pre-earnings blackout for new entries (~May 3). This position should be opened before May 3 or not at all.
