---
name: NVDA thesis
last_updated: 2026-05-07
last_run_id: 20260507_123732
target_words: 500
stale_after_days: 30
word_count: 498
summary: Breakout confirmed May 6 — both entry gates fired simultaneously; price $207.83 (+4.64%), 5-of-5 bullish consensus; HOLD (allowed_actions blocks buy); prior zone (4-run HOLD at EMA-21/Fib 38.2%) resolved bullishly; new watch zone above $200.24; hard exit May 17 before Q1 FY2027 earnings May 20.
---

# NVDA — Thesis

## TL;DR

⚠️ Recent trade: stop_hit 2026-04-30, -$63.20 corrected (originally -$264.65 due to sizing bug, see commit b2b472d). Thesis under review.

NVDA dominates the AI chip market (~81% share) in a multi-year capex supercycle. The structural thesis is intact and has materially strengthened this run. The 4-run HOLD at the EMA-21/Fib 38.2% confluence ($196.75–$197.69) has now resolved **bullishly**: both wiki-defined entry gates fired simultaneously for the first time across five consecutive runs — (1) hourly MACD histogram crossed above zero (+0.9366), and (2) confirmed bullish engulfing candle above $194.74. Price surged from $196.50 to $207.83 (+4.64%) on May 6, clearing $200.24 (17-test resistance) and $203.00 (7-test resistance) with conviction. AMD Q1 2026 blowout ($10.25B +38% YoY) confirmed the AI capex supercycle. All 5 swing agents are bullish (confidence 60). Decision: HOLD — allowed_actions blocks a new buy. Hard exit deadline ~May 17 (3-day pre-earnings blackout before NVDA Q1 FY2027 ~May 20 AMC).

**Prior thesis claim falsified:** The 2026-05-06 thesis stated "both entry gates remain unmet" and "AMD earnings passed without triggering confirmation signal." That claim is now falsified. Both gates fired on May 6 (hourly MACD histogram +0.9366 positive; bullish engulfing candle above $194.74 confirmed). Price is now $207.83 — above the prior watch zone and approaching the $208.20 broken-support-now-resistance level. The failing condition (lack of confirmation) has been resolved.

## Bull case

- **AI capex supercycle confirmed.** AMD Q1 2026 (+38% YoY revenue, +43% EPS) is the strongest direct read-through for NVDA GPU demand. Azure +40%, AWS $37.6B capex confirm hyperscaler spend. Consensus NVDA Q1 FY2027 revenue $78.8B (+78.6% YoY) with 118% EPS growth. (web_research/NVDA.json, swing_macro_context, 20260507_123732)
- **Breakout confirmed.** Both wiki-entry gates fired simultaneously — hourly MACD histogram +0.9366 (positive), confirmed bullish engulfing candle above $194.74. ADX 51.68 with +DI > -DI; hourly ADX 37.6 with +DI 36.55 >> -DI 11.21. RSI-14 57.92 (neutral-bullish, not overbought). 5-of-5 swing agents bullish — rare consensus. (swing_head_trader, 20260507_123732)
- **Fundamentals exceptional.** PEG 0.66, D/E 0.11, current ratio 4.44, 59% operating margin, 61% revenue growth. Blackwell Ultra leads AMD/Intel by "two generations." New Corning optical-fiber partnership (10x US optical capacity). (growth_analyst_agent, web_research/NVDA.json, 20260507_123732)
- **Macro tailwind strengthening.** S&P 500 and Nasdaq both at all-time highs. US-Iran peace deal advancing — oil fell to $91.73/bbl. Risk-on regime removes defensive rotation headwind for growth names. (swing_macro_context, web_research/NVDA.json, 20260507_123732)
- **Earnings catalyst ~9 days.** NVDA Q1 FY2027 earnings May 20 AMC historically drives 8–15% move. Analyst avg PT $271 (~30% upside from $207.83). Entry window 7–9 trading days with hard exit ~May 17. (swing_catalyst_news, 20260507_123732)

## Bear case

- **Volume below threshold.** Relative volume 1.26x vs 1.5x minimum required by swing_breakout strategy. The DIS pre-earnings breakout on May 5 had similar sub-threshold volume (1.23x) and failed. Daily OBV trending down and diverging bearishly from price — distribution signal. (swing_breakout, 20260507_123732)
- **Price chasing after breakout.** Ideal entry was $204.50–$207.00; current price $207.83 is already at the breakout level. No pullback opportunity materialized. Allowed_actions blocking buy means this run is HOLD — no position exists to ride the move. (swing_head_trader, 20260507_123732)
- **Resistance overhead.** $208.20 broken support re-tests as resistance (multiple prior tests); $214.73 hourly cluster; $216.83 52-week high. Price sits just below the $208.20 hurdle. (technicals.md, 20260507_123732)
- **Kevin Warsh tail risk.** Fed chair transition May 15 sits inside the trade window. Hawkish tightening-bias signal could re-rate growth stocks lower. (swing_macro_context, 20260507_123732)
- **EMA pullback Fib dip-buy: 0% win rate last 30 days.** Prior Apr 30 entry (-$63.20) lacked confirmation candle; today's setup is different (both gates fired), but the lesson moderates confidence. (trades.md, swing_head_trader, 20260507_123732)
- **In-house silicon risk (long-term).** Anthropic multi-billion TPU deal with Google; analyst projects Google could capture 20% AI chip market if sold externally. Not a near-term risk but a structural moat erosion signal. (web_research/NVDA.json, 20260507_123732)

## What would change my mind

**Bearish flip triggers:** close below $198.70 (hourly support, 23 tests) on a daily basis — thesis invalidated; second hyperscaler cuts AI capex; NVDA earnings miss on demand.

**Bullish conviction boost:** volume exceeds 1.5x on follow-through day; price clears $208.20 and holds; daily MACD histogram turns positive; allowed_actions opens buy on a future run.

## Last updated

2026-05-07 — run 20260507_123732. Prior thesis (2026-05-06, run 20260506_123913) falsified: "both entry gates unmet" claim superseded — both gates fired May 6. Price $207.83 (+4.64%), 5-of-5 bullish consensus. HOLD (allowed_actions). Synthesized from swing agents, swing_head_trader, fundamentals/growth/valuation analysts; decisions.json; web_research/NVDA.json.
