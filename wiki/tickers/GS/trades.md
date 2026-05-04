---
name: GS trades
last_updated: 2026-05-04
last_run_id: 20260504_192106
target_words: 800
stale_after_days: 60
word_count: 700
summary: GS has zero executed trades in tracker.db; model held GS across five analyzed runs (Apr 11–May 4); blockers evolved from weak ADX → FICC miss/insider sell/broken support → Iran escalation macro veto
---

## TL;DR

No GS trades have ever been placed in the paper trading system. The model has analyzed GS five times (Apr 11, Apr 15, Apr 17, Apr 30, May 4) and issued a Hold decision every time. The consistent blockers evolved: initially weak ADX (sub-25), then post-earnings FICC miss and broken support, and now the Iran escalation macro headwind specifically targeting GS's M&A/IPO/FICC revenue. GS remains a "watched but not traded" name. `per_ticker_history[GS]` in trade_ledger.json (run `20260504_192106`) = [] — zero fills confirmed. [trade_ledger.json, run `20260504_192106`]

---

## Open Positions

None. GS has zero open positions in `tracker.db` as of 2026-05-04. `per_ticker_history[GS]` = [] per trade_ledger.json (run `20260504_192106`).

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
| Runs analyzed | 5 (Apr 11, Apr 15, Apr 17, Apr 30, May 4) |
| Model hold signals | 5 |

Source: trade_ledger.json (run `20260504_192106`) — per_ticker_history[GS] = [], 0 rows confirmed.

---

## Model Decision Log

This section records every model run that analyzed GS and the resulting decision, explaining why no trade was ever placed.

### Run: `20260504_192106` — May 4, 2026

**Decision:** Hold, 30% confidence. 0 shares. (5th consecutive hold — lowest confidence in GS history.)

**Why not entered:** Five independent blockers converging: (1) Iran escalation on May 4 (UAE intercepted Iranian missiles, WTI >$106) directly suppresses GS's M&A deal flow, IPO activity, and FICC trading revenue — swing_macro_context applied sector-specific veto; (2) Hourly timeframe in confirmed downtrend (minus DI 28.24 > plus DI 18.74, MACD histogram -2.11); (3) $924.23 overhead resistance confirmed — rejected partial recovery from $899 low; (4) Extreme insider distribution (3.3:1, $109.9M in sales, zero buys) remains live headwind; (5) swing_catalyst_news carries active in-progress bearish thesis (run `20260430_190826`, conf 68, target $864.45) — a new long would directly conflict. Agent vote: 1B (mean_reversion, 45) / 4N (trend_momentum 30, breakout 25, catalyst_news 30, macro_context 35). Lone bullish agent limited confidence to 45 and noted broken $924.23 overhead resistance. [decisions.json, run `20260504_192106`]

**Key metrics at decision time:**
- Price: $905.10
- ADX daily: 34.03 (strong, trend confirmed)
- Hourly MACD histogram: -2.11 (deeply negative)
- Hourly RSI divergence: confirmed (positive signal, insufficient alone)
- Insider sell ratio: 3.3:1 ($109.9M sold, zero buys)
- Head Trader confidence: 30%

---

### Run: `swing_20260411_211655` — Apr 11, 2026

**Decision:** Not placed (pre-earnings hold pending confirmation)

**Head Trader signal:** Bullish, 63% confidence. 7 of 9 agents bullish. The run analyzed GS ahead of Q1 earnings on April 13 and identified it as a top catalyst setup in the financial cohort. Entry was suggested at $895–$910 with a $940 target (prior swing high). Bullish votes came from: swing_catalyst_trader (75%), swing_sector_rotation (70%), swing_momentum_ranker (72%), news_sentiment (70%), stanley_druckenmiller (58%), swing_breakout_trader (55%). Neutral votes from: swing_trend_follower (ADX 22.75 below threshold), swing_pullback_trader.

**Why not entered:** The Apr 11 run produced a bullish head trader signal but the entry window was described as conditional on earnings — specifically "buy the rumor, sell the news" risk was flagged explicitly. No executor run placed the trade, and the earnings print (Apr 13) delivered a mixed result: EPS beat but FICC missed. The stock gapped down intraday from ~$907 to ~$865 before recovering, validating the caution.

**Key quote from head trader:** "The only real risk is a 'buy the rumor, sell the news' reaction if earnings merely meet expectations." (run `swing_20260411_211655`, swing_head_trader reasoning for GS)

---

### Run: `20260415_110848` — Apr 15, 2026

**Decision:** Hold, 48% confidence. 0 shares.

**Why not entered:** Post-earnings, the agent split deteriorated from 7/9 bullish to a contested 4-3-3 (4 bullish, 3 neutral, 3 bearish). The head trader cited three explicit blockers: (1) ADX 19.4 — below the 25 threshold for trend confirmation; (2) hourly momentum turned negative post-earnings (ROC slightly negative, MACD histogram negative); (3) heavier bearish participation from growth agent and Druckenmiller due to FICC miss and insider selling. PM reasoning from run `20260417_233350` confirmed: "R:R cannot reach 2:1 cleanly."

**Key metrics at decision time:**
- Price: ~$903–$909
- ADX: 19.4
- RSI-14: 69.1
- Head trader entry/target/stop: $895 / $940 / $874 (implicit R:R ~2.1:1)
- Confidence: 48% — below the model's actionable threshold

---

### Run: `20260417_233350` — Apr 17, 2026

**Decision:** Hold, 62% confidence. 0 shares. Entry price referenced at $909.63, target $925.00, stop $890.00, R:R 1.43:1.

**Why not entered:** The PM's own R:R was 1.43:1 — well below the 2:1 minimum mandate. ADX was cited as "weak (20.66)" and 5-day ROC was -0.4% (decelerating, not accelerating). PM reasoning: "HT neutral; daily ADX weak (20.66), 5d ROC -0.4%, momentum decelerating. R:R cannot reach 2:1 cleanly. Stand aside." (run `20260417_233350`, decisions.json, GS entry)

---

## What Would Trigger a Trade

Based on five-run hold streak, the model has explicitly defined entry criteria (updated run `20260504_192106`):

**Long entry — all three must fire simultaneously:**
1. **Daily close above $924.23** on volume ≥ 1.5x average — reclaims broken support as support
2. **Daily RSI-7 > 50** — confirms daily momentum stabilization
3. **Hourly MACD histogram positive** — hourly trend re-aligns with daily

**Short entry:**
- Sustained volume-accelerated break below $899.16 (8-test floor) → directional short thesis

**Macro pre-condition:** Iran escalation must de-escalate (Strait of Hormuz closure risk off the table) before initiating any long; macro_context will apply veto as long as Iran risk suppresses GS revenue drivers.
