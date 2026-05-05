---
name: GS trades
last_updated: 2026-05-05
last_run_id: 20260505_190606
target_words: 800
stale_after_days: 60
word_count: 694
summary: GS has zero executed trades in tracker.db; model held GS across six analyzed runs (Apr 11–May 5); blockers evolved from weak ADX → FICC miss/insider sell/broken support → Iran escalation macro veto → EMA-21 break + R/R failure
---

## TL;DR

No GS trades have ever been placed in the paper trading system. The model has analyzed GS six times (Apr 11, Apr 15, Apr 17, Apr 30, May 4, May 5) and issued a Hold decision every time. The consistent blockers evolved: initially weak ADX (sub-25), then post-earnings FICC miss and broken support, then the Iran escalation macro headwind specifically targeting GS's M&A/IPO/FICC revenue, and now an EMA-21 break with R/R still failing the 2:1 minimum (1.28:1). GS remains a "watched but not traded" name. `per_ticker_history[GS]` in trade_ledger.json (run `20260505_190606`) = [] — zero fills confirmed. [trade_ledger.json, run `20260505_190606`]

---

## Open Positions

None. GS has zero open positions in `tracker.db` as of 2026-05-05. `per_ticker_history[GS]` = [] per trade_ledger.json (run `20260505_190606`).

---

## Closed Trades

None. No GS trades have been executed, filled, or closed in the paper trading system.

---

## Lifetime Statistics

| Metric | Value |
|--------|-------|
| Total trades | 0 |
| Open positions | 0 |
| Closed trades | 0 |
| Win rate | N/A |
| Average P&L per trade | N/A |
| Realized P&L | $0 |
| Unrealized P&L | $0 |
| Total return | N/A |
| Runs analyzed | 6 (Apr 11, Apr 15, Apr 17, Apr 30, May 4, May 5) |
| Model hold signals | 6 |

Source: trade_ledger.json (run `20260505_190606`) — per_ticker_history[GS] = [], 0 rows confirmed.

---

## Model Decision Log

This section records every model run that analyzed GS and the resulting decision, explaining why no trade was ever placed.

### Run: `20260505_190606` — May 5, 2026

**Decision:** Hold, 35% confidence. 0 shares. (6th consecutive hold.)

**Why not entered:** Price $903.27 broke below daily EMA-21 ($906.74) for the first time in the run sequence — a new deterioration signal. R/R for short from daily close ($903.27) to target ($864.45) vs stop ($933.48) = 1.28:1 — still below 2:1 minimum. RSI-7 at 33.74 near oversold creates near-term bounce risk that would hit the short stop. Iran escalation headwinds on M&A/IPO/FICC persist despite May 5 partial ceasefire. Agent vote: 0 bullish / 1 bearish (catalyst_news 62) / 4 neutral (trend_momentum 20, mean_reversion 35, breakout 25, macro_context 32). Preferred short entry remains $918–$924 resistance zone. [decisions.json, run `20260505_190606`]

**Key metrics at decision time:**
- Price: $903.27 daily close / $918.94 hourly
- ADX daily: 34.21 (strong)
- EMA-21 daily: $906.74 — price now below
- Hourly MACD histogram: -0.2997 (negative, confirmed downtrend)
- MACD histogram daily: -3.1266 (deeply negative)
- Insider sell ratio: 3.3:1 ($109.9M sold, zero buys)
- Head Trader confidence: 35%

---

### Run: `20260504_192106` — May 4, 2026

**Decision:** Hold, 30% confidence. 0 shares. (5th consecutive hold — lowest confidence in GS history.)

**Why not entered:** Five blockers converging: (1) Iran escalation directly suppresses GS revenue drivers; (2) hourly confirmed downtrend (minus DI 28.24 > plus DI 18.74); (3) $924.23 overhead resistance confirmed; (4) extreme insider distribution (3.3:1); (5) active in-progress bearish background thesis (run `20260430_190826`, conf 68, target $864.45). Agent vote: 1B/4N. [decisions.json, run `20260504_192106`]

---

### Run: `swing_20260411_211655` — Apr 11, 2026

**Decision:** Not placed (pre-earnings hold pending confirmation)

**Head Trader signal:** Bullish, 63% confidence (7/9 agents). Entry suggested $895–$910, target $940. Earnings "buy the rumor, sell the news" risk flagged. Not entered. Validated: stock fell intraday on April 13 FICC-miss print.

---

### Run: `20260415_110848` — Apr 15, 2026

**Decision:** Hold, 48% confidence. 0 shares.

**Why not entered:** Post-earnings agent split deteriorated (4-3-3). ADX 19.4 — below 25 threshold. Hourly momentum negative post-earnings. FICC miss and insider selling added bearish votes. [decisions.json, run `20260415_110848`]

---

### Run: `20260417_233350` — Apr 17, 2026

**Decision:** Hold, 62% confidence. 0 shares. Entry reference $909.63, target $925.00, stop $890.00, R/R 1.43:1.

**Why not entered:** R/R 1.43:1 below 2:1 minimum. ADX 20.66 (weak). 5d ROC -0.4% (decelerating). [decisions.json, run `20260417_233350`]

---

### Run: `20260430_190826` — Apr 30, 2026

**Decision:** Hold, 38% confidence. 0 shares.

**Why not entered:** FICC miss dissipated momentum; $924.23 hourly support broke April 29 (-2.4%); ADX crossed 25 threshold (32.67) but conflicting signals (1B/3N/1Bear) precluded clean setup on either side. [decisions.json, run `20260430_190826`]

---

## What Would Trigger a Trade

Based on six-run hold streak, the model has explicitly defined entry criteria (updated run `20260505_190606`):

**Long entry — all three must fire simultaneously:**
1. **Daily close above $924.23** on volume ≥ 1.5x average — reclaims broken support as support
2. **Daily RSI-7 > 50** — confirms daily momentum stabilization
3. **Hourly MACD histogram positive** — hourly trend re-aligns with daily

**Short entry:**
- Bounce to $918–$924 resistance zone with 2:1+ R/R (stop $933.48, target $864.45 = 4:1 from $918 entry)
- OR volume-accelerated break below $899.16 (8-test floor) → momentum short thesis

**Macro pre-condition:** Iran escalation must de-escalate durably before initiating any long.
