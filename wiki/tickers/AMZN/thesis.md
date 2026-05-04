---
name: AMZN thesis
last_updated: 2026-05-04
last_run_id: 20260504_173321
target_words: 500
stale_after_days: 30
word_count: 498
summary: Short stopped out at $276 on May 4 — prior claim "stop at $276 holds" falsified by bull absorption in distribution zone; near-term bias still bearish/neutral but no capital to act; AWS structural bull case intact; re-entry requires fresh confirmation candle
---

# AMZN — Thesis

## TL;DR

**Prior claim falsified:** The 20260501_173921 thesis stated a short was open at ~$269 with stop $276, targeting $244.44 (20-SMA mean reversion). That stop was hit on May 4, 2026: price rallied through $276 intraday, closing the position at -$7.00. **What this falsifies:** the assumption that the April 30 shooting star distribution candle would be immediately followed by a bearish continuation without first absorbing the $268-276 zone. The mean-reversion directional thesis (stock is statistically extreme) remains intact — but the stop-out is evidence bulls have short-term control. No new AMZN position can be entered: portfolio cash = $0, risk manager limit = $0. HOLD is the only allowed action. [source: decisions.json, trade_ledger.json per_ticker_history[AMZN] ID 115, run 20260504_173321]

---

## What falsified the prior thesis claim

The 20260501_173921 thesis placed a short at ~$265.86 (fill) with a hard stop at $276. The stop-out on May 4 demonstrates that bulls successfully absorbed the selling pressure in the $268-276 distribution zone identified by the April 30 shooting star. This is the second consecutive stop-out at RSI 82-88 / ADX 60+ levels in the portfolio (NVDA at $205.30, AMZN at $276) — a pattern flagging that extreme-trend stocks can stay overbought far longer than expected even with confirmed reversal candles. The stop-out does NOT invalidate the mean-reversion direction — RSI 82.9/88.96 and z-score 2.03 still flag statistical extreme — but it sets a higher bar for re-entry confirmation. [source: trade_ledger.json, signals_combined.json, run 20260504_173321]

---

## Bull case (structural — intact, not actionable)

**AWS as the AI picks-and-shovels play.** Q1 2026 confirmed: revenue $181.5B (+17% YoY), EPS $2.78 (beat $1.64 estimate by 69.5%), AWS $37.6B (+28% YoY). OpenAI and Anthropic confirmed using Amazon Trainium chips — validating AWS AI silicon strategy. $11.57B Globalstar acquisition (second-largest in company history) adds satellite connectivity optionality. Amazon Supply Chain Services launched for external businesses, expanding logistics revenue. Analyst consensus: ~45 Buy / 2 Hold / 0 Sell, avg PT $310.25. Q2 2026 guide: $194-199B revenue, operating income $20-24B. [source: web_research/AMZN.json, run 20260504_173321]

---

## Bear case (near-term — intact but no capital)

**Mean reversion thesis survives the stop-out.** RSI-14 at 82.9 and RSI-21 at 88.96 remain deeply overbought. Z-score 2.03. Price 19.3% above 50-SMA. ADX 65.59 (extreme, mature trend — the bull headwind). The April 30 shooting star on 2.05x volume ($273.88 high / $265.06 close) remains the key distribution reference candle. Two of five swing agents are actively bearish (swing_mean_reversion 58 conf, swing_macro_context 76 conf); zero are bullish. Macro backdrop is risk-off: Iran missile strike on US warship near Jask (May 4), WTI crude above $105, Dow futures lower. Fed hawkish succession (Warsh replacing Powell May 15). No new capital available — this thesis is directionally valid but unactionable. [source: signals_combined.json, web_research/AMZN.json, explanation.json, run 20260504_173321]

**ADX 65 is the primary headwind.** This is among the strongest trend readings in the portfolio — historically, trends this powerful absorb multiple distribution attempts before reversing. The stop-out confirms this risk is live, not theoretical.

---

## What would change my mind

**Bear (re-entry conditions):** Hourly RSI extreme (>75) plus volume-confirmed rejection at $273-276 resistance zone. OR daily close below $265 to re-establish bearish momentum. Both conditions needed given the stop-out warning. New capital must become available.

**Bull re-entry:** Price pulls back to 10 EMA zone $258-261, RSI normalizes below 65, constructive daily candle forms. R:R long entry at those levels exceeds 2:1 with stop below EMA cluster. Alternatively, AWS Q2 revenue materially above $188.9B guide confirms structural acceleration.

**Bull case strengthened:** Iran ceasefire holds durably, macro risk-off resolves, giving AMZN's AI infrastructure premium room to re-expand.
