---
name: AMZN thesis
last_updated: 2026-05-01
last_run_id: 20260501_173921
target_words: 500
stale_after_days: 30
word_count: 497
summary: Prior bull entry thesis falsified by "sell the news" shooting star on Apr 30 — Q1 beat absorbed, distribution volume confirmed; near-term bias now BEARISH (mean reversion to $244); longer-term AWS structural bull case remains intact
---

# AMZN — Thesis

## TL;DR

**Prior claim falsified:** The bootstrap thesis stated the ideal long re-entry zone was $220–$244 and that the system would wait for a pullback from overbought extremes before buying. That claim was not falsified — it was correct discipline. What changed in run 20260501_173921 is that the April 30 "sell the news" shooting star on 2.05x volume has now made the current price ($265–$269) a **short entry**, not a waiting zone. The long-term AWS structural bull case is intact, but the near-term swing bias has flipped to bearish for the first time across all AMZN run history. [source: decisions.json, signals_combined.json, run 20260501_173921]

---

## What falsified the prior near-term thesis

The bootstrap thesis (run bootstrap, April 29 2026) was explicitly bullish with a stated ideal long re-entry in the $220–$244 zone after a pullback. Instead of pulling back, AMZN continued to rally +10% to $265–$273 on Q1 earnings momentum — the PM's $262 target from run 20260417_233350 was exceeded. The April 30 session then produced a failed breakout: price gapped to $273.88 but closed at $265.06. **The falsifying evidence is the shooting star reversal candle on 2.05x volume** — distribution, not continuation. Zero swing agents voted bullish in run 20260501_173921 (vs. 6-of-9 bullish in all prior runs). The mean-reversion and breakout agents now both read the same candle as a short trigger. [source: signals_combined.json, run 20260501_173921]

---

## Bull case (structural — intact, not actionable here)

**AWS as the AI picks-and-shovels play.** Q1 2026 confirmed: AWS $37.6B revenue (+28% YoY, fastest in 15 quarters), Anthropic $100B+ 10-year AWS commitment, OpenAI shifting from Azure to AWS, Meta AWS Graviton5 deal. AWS AI ARR at $15B as disclosed in Andy Jassy's April shareholder letter. Cloud backlog at $244B. Analyst avg PT post-Q1 raises: $308.55 (43–47 Buy ratings). The structural AI infrastructure bull case is stronger post-Q1 than before. [source: web_research/AMZN.json, run 20260501_173921]

**Platform optionality.** The $11.6B Globalstar acquisition (closed April 2026) and Amazon Pharmacy GLP-1 partnerships are intact low-cost options on adjacent markets.

---

## Bear case (near-term — actionable)

**Mean reversion is now the primary swing thesis.** Five metrics align on an extreme: RSI-14 82.21, RSI-21 88.83, z-score 2.01, price 18.58% above 50-SMA, ADX 64.34 (mature trend). The April 30 shooting star on 2.05x volume is the reversal candle that activates Branch A (fade the extreme). Target: 20-SMA at $244.44. Stop: above confirmed reversal high $273.88 + buffer at $276. R:R 3.51:1 from $269 entry. [source: signals_combined.json swing_mean_reversion, run 20260501_173921]

**ADX 64 is the primary risk to the short.** A 64 ADX reading signals a very strong, mature trend — fades in strong trends frequently get run over. Swing_trend_momentum explicitly flagged this: EMA stack is perfectly bullish, ROC is all-positive and accelerating, and the underlying uptrend is structurally intact. The bearish view is a **near-term mean reversion**, not a trend reversal. Confidence is 55 (from 62 head trader, dialed down further by risk manager on NVDA lesson). [source: signals_combined.json swing_head_trader, risk_management_agent, run 20260501_173921]

**NVDA lesson parallel.** The only closed trade in portfolio history (NVDA, April 30, -$63.20 stop hit) was at RSI 81–87 in a similarly stretched ADX environment. AMZN is in the same RSI regime. This pattern match was cited explicitly by three of five swing agents as a warning against chasing at current prices. [source: signals_combined.json, portfolio.recent_closed, run 20260501_173921]

---

## What would change my mind

**Bear to Bull (re-entry):** Price pulls back to $252–$258 (swing_trend_momentum entry zone) or $252 (swing_macro_context entry), z-score normalizes toward 1.0–1.5, RSI drops below 65, and a constructive daily candle forms. At those levels the R:R long exceeds 2:1 with a stop below the EMA cluster. Alternatively, acceptance above $270.62 hourly resistance on volume re-opens a long.

**Bull case strengthened:** AWS Q2 revenue materially above $188.9B guide; further major cloud migration deals announced; Iran ceasefire holds and macro risk-off eases, giving AMZN's AI infrastructure premium room to re-expand.
