---
name: GS trades
last_updated: 2026-05-06
last_run_id: 20260506_190825
target_words: 800
stale_after_days: 60
word_count: 692
summary: GS has zero executed trades in tracker.db; model held GS across seven analyzed runs (Apr 11–May 6); blockers evolved from weak ADX → FICC miss/insider sell/broken support → Iran escalation macro veto → EMA-21 break + R/R failure → hourly reversal without volume, dip-buy entry passed
---

## TL;DR

No GS trades have ever been placed in the paper trading system. The model has analyzed GS seven times (Apr 11, Apr 15, Apr 17, Apr 30, May 4, May 5, May 6) and issued a Hold decision every time. The blockers evolved: initial weak ADX (sub-25), then post-earnings FICC miss and broken support, then Iran escalation targeting GS's M&A/IPO/FICC revenue, then EMA-21 break with R/R failure, and now a bullish hourly reversal where the ideal dip-buy entry at $924 already passed before the analysis ran. GS remains "watched but not traded." `per_ticker_history[GS]` in trade_ledger.json (run `20260506_190825`) = [] — zero fills confirmed. [trade_ledger.json, run `20260506_190825`]

---

## Open Positions

None. GS has zero open positions in `tracker.db` as of 2026-05-06. `per_ticker_history[GS]` = [] per trade_ledger.json (run `20260506_190825`).

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
| Runs analyzed | 7 (Apr 11, Apr 15, Apr 17, Apr 30, May 4, May 5, May 6) |
| Model hold signals | 7 |

Source: trade_ledger.json (run `20260506_190825`) — per_ticker_history[GS] = [], 0 rows confirmed.

---

## Model Decision Log

### Run: `20260506_190825` — May 6, 2026

**Decision:** Hold, 38% confidence. 0 shares. (7th consecutive hold.)

**Why not entered:** Bullish setup is forming but today is not the entry day. The ideal dip-buy opportunity at $924 (the 35-test hourly support) was already in the rearview mirror when analysis ran — GS had surged to $940.77 intraday. Entering at $940 compresses target to $952 (only +$11 upside vs $30 downside to $912 stop = 0.37:1 R/R). Volume remains critically absent: 0.77x daily, 0.32x hourly — both far below the 1.5x confirmation threshold. Daily MACD histogram still -3.19 (no daily confirmation). Agent vote: 2 bullish (trend_momentum 48, macro_context 52) / 3 neutral (mean_reversion 40, breakout 30, catalyst_news 40). The two bullish agents agree pullback to $924 is valid; the three neutral agents agree today's price is already too extended to enter. Consensus: wait for a pullback to $924 with volume. [decisions.json, run `20260506_190825`]

**Key metrics at decision time:**
- Intraday price: $940.77 (from $903.27 daily close May 5)
- Daily close: $918.89
- ADX daily: 33.63 (strong); plus_DI 21.39 > minus_DI 17.12
- Hourly MACD histogram: +2.8851 (strongly bullish, major reversal)
- MACD histogram daily: -3.1933 (still negative)
- Daily volume: 0.77x average
- Hourly volume: 0.32x average
- Insider sell ratio: 3.3:1 ($109.9M sold, zero buys)
- Head Trader confidence: 38%

---

### Run: `20260505_190606` — May 5, 2026

**Decision:** Hold, 35% confidence. 0 shares. (6th consecutive hold.)

**Why not entered:** Price $903.27 broke below daily EMA-21 ($906.74) for first time in run sequence. R/R for short from $903.27 to target $864.45 vs stop $933.48 = 1.28:1 (below 2:1 minimum). RSI-7 33.74 near oversold — bounce risk. Agent vote: 0 bullish / 1 bearish (catalyst_news 62) / 4 neutral. [decisions.json, run `20260505_190606`]

---

### Run: `20260504_192106` — May 4, 2026

**Decision:** Hold, 30% confidence. 0 shares. (5th consecutive hold — lowest confidence in GS history.)

**Why not entered:** Iran escalation directly suppresses GS revenue. Hourly confirmed downtrend. $924.23 overhead resistance. Extreme insider distribution (3.3:1). Agent vote: 1B/4N. [decisions.json, run `20260504_192106`]

---

### Run: `20260430_190826` — Apr 30, 2026

**Decision:** Hold, 38% confidence. 0 shares.

**Why not entered:** FICC miss; $924.23 hourly support broke April 29 (-2.4%); ADX crossed 25 (32.67) but conflicting signals (1B/3N/1Bear) precluded clean setup on either side. [decisions.json, run `20260430_190826`]

---

### Run: `20260417_233350` — Apr 17, 2026

**Decision:** Hold, 62% confidence. 0 shares. Entry reference $909.63, target $925.00, stop $890.00, R/R 1.43:1.

**Why not entered:** R/R 1.43:1 below 2:1 minimum. ADX 20.66 (weak). 5d ROC -0.4%. [decisions.json, run `20260417_233350`]

---

### Run: `20260415_110848` — Apr 15, 2026

**Decision:** Hold, 48% confidence. 0 shares.

**Why not entered:** Post-earnings agent split deteriorated (4-3-3). ADX 19.4 (below 25 threshold). FICC miss and insider selling added bearish votes. [decisions.json, run `20260415_110848`]

---

### Run: `swing_20260411_211655` — Apr 11, 2026

**Decision:** Not placed (pre-earnings hold pending confirmation)

**Head Trader signal:** Bullish, 63% confidence (7/9 agents). Entry suggested $895–$910, target $940. Earnings "buy the rumor, sell the news" risk flagged. Not entered. Validated: stock fell intraday on April 13 FICC-miss print.

---

## What Would Trigger a Trade

Based on seven-run hold streak, entry criteria (updated run `20260506_190825`):

**Long entry — all three must fire simultaneously:**
1. **Pullback to $924.00** (35-test hourly support) with constructive reversal candle
2. **Volume ≥ 1.5x average** on entry bar
3. **Hourly MACD histogram positive** — confirms hourly re-entry

**Short entry:** No longer valid. Prior bearish thesis stop $933.48 breached intraday by the May 6 surge. Short thesis retired.

**Macro pre-condition:** Iran ceasefire must durably hold before initiating any long.
