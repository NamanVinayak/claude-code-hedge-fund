---
name: GS trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 682
summary: GS has zero executed trades in tracker.db; model held GS on all three analyzed runs due to weak ADX and R:R constraints
---

## TL;DR

No GS trades have ever been placed in the paper trading system. The model analyzed GS three times (Apr 11, Apr 15, Apr 17) and issued a Hold decision every time. The consistent blocker was weak daily ADX (sub-25) and an inability to construct a clean 2:1 risk-reward setup. GS remains a "watched but not traded" name with a well-documented thesis for when conditions improve.

---

## Open Positions

None. GS has zero open positions in `tracker.db` as of 2026-04-29.

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

Source: `tracker.db` query on 2026-04-29 — returned 0 rows for ticker = 'GS'.

---

## Model Decision Log

This section records every model run that analyzed GS and the resulting decision, explaining why no trade was ever placed.

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

Based on the three-run hold streak, the model has implicitly defined the entry criteria:

1. **Daily ADX > 25** — this is the hardest gate; has never been cleared across any GS run in this archive
2. **Hourly MACD histogram turns positive** — confirms intraday momentum re-aligns with daily
3. **Volume > 1.5x average on the trigger day** — breakout threshold the model uses consistently
4. **Risk-reward ≥ 2:1 constructable** — requires a tight entry near fib/EMA support with a meaningful target; current analyst target of $933.75 with stock at ~$910 makes this difficult without a deeper pullback
5. **Insider selling trend reverses** — a secondary soft condition; 3.3:1 sell ratio is a persistent headwind in the sentiment agent

If GS pulls back to $874–$880 (EMA-50 zone), ADX begins rising above 25, and hourly stabilizes, the model would likely flip to a buy decision with approximately 60–65% confidence.
