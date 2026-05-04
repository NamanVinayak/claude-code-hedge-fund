---
name: BAC thesis
last_updated: 2026-05-04
last_run_id: 20260504_192106
target_words: 500
stale_after_days: 30
word_count: 502
summary: Bull thesis intact — open 15-share long at $52.75; Iran escalation (May 4) falsifies prior "macro tailwind" claim; pullback to $52.31 deepens but stop at $51.50 not hit; OBV divergence and Iran headwind are the new primary cautions
---

## TL;DR

Bank of America has an active long position: 15 shares at $52.75 (Apr 30, 2026, id 110), currently at $52.31 (unrealized ~-$0.44/share). The underlying uptrend is structurally intact — ADX 51.52, EMA-10 > EMA-21 > EMA-50 — but near-term momentum has turned negative. **Prior thesis falsification (run `20260504_192106`):** The May 1 thesis cited "Iran peace talks easing oil pressure" as a macro tailwind (web_research/BAC.json, run `20260501_190923`). That claim is falsified: Iran-US military escalation returned on May 4 (UAE intercepted Iranian missiles, WTI surged above $106), directly reversing the risk-on narrative. The new macro backdrop is mixed-to-cautious. No bull-to-bear flip; the position remains open with stop at $51.50.

---

## Prior Thesis Claim Falsified

**Falsified claim (run `20260501_190923`):** "Iran peace talks easing oil pressure" — cited as a positive macro tailwind for banks.

**What falsified it (run `20260504_192106`):** Iran-US ceasefire collapsed. UAE intercepted Iranian missiles on May 4, Strait of Hormuz closure fears re-emerged, WTI surged above $106, and Dow futures declined. Macro regime reverted to mixed-to-cautious per `macro/regime.md` (updated run `20260504_125732`). [web_research/BAC.json, run `20260504_192106`]

---

## Bull Case

**Exceptional trend structure.** ADX 51.52 — still in the "exceptional" range (>50). EMA alignment bullish (EMA-10 $52.93 > EMA-21 $52.31 > EMA-50 $51.56). The 38.2% Fibonacci retracement ($52.07) and volume-confirmed hourly support at $52.25 (28 tests) form a dip-buy confluence zone that swing_mean_reversion rates as valid. [signals_combined.json, run `20260504_192106`]

**Fundamentals remain strong.** Q1 2026: EPS $1.11 beat (+9.9%), NII $15.7B (+9% YoY), zero trading loss days. Analyst consensus: 40% Strong Buy / 45% Buy, avg PT ~$61.61 (17% implied upside from $52.31). $18.66B trailing buyback. Basel III capital relief could unlock ~$40B additional buyback capacity. [web_research/BAC.json, run `20260504_192106`]

---

## Bear Case

**Iran escalation is a direct macro headwind.** Risk-off on May 4 specifically pressures financials: loan demand, credit quality, and consumer spending deteriorate under a stagflationary energy-shock scenario. [web_research/BAC.json macro_context]

**OBV divergence persists.** On-Balance Volume trending down on both daily and hourly timeframes — institutional distribution into the rally. Hourly MACD histogram negative (-0.085). 10-day ROC -1.24% (negative). Short-term momentum decelerating even as the daily trend holds. [signals_combined.json, swing_trend_momentum]

**Berkshire Hathaway structural overhang.** Ongoing stake reduction; no disclosed floor. Persistent cap on institutional enthusiasm. Berkshire continues to reduce. [web_research/BAC.json, swing_catalyst_news]

**R/R to target is marginal.** From $52.31, upside to $55.40 is +$3.09; downside to stop $51.50 is -$0.81. R/R is approximately 3.8:1 from current price but 4/5 agents are neutral and the risk manager's remaining_position_limit is $0 (BAC position is at cap). No add-on is authorized regardless of R/R. [signals_combined.json, risk_management_agent]

---

## What Would Change the Thesis

**Bull-to-bear flip:** Hard exit if daily close below stop at $51.50. Secondary: Berkshire stake disclosed below 5%, or Iran escalation drives NII guidance cut at Q2 earnings (July 14, 2026).

**Re-entry / add-on trigger:** Not applicable while position is open at max capital allocation. Monitor OBV for re-convergence. Re-acceleration trigger: daily MACD histogram turns positive AND 5d/10d ROC both turn positive AND macro regime stabilizes.

---

## Synthesis

The 15-share long is the core active position. The underlying trend is real and structurally intact. The short-term case is challenged by decelerating momentum, Iran escalation headwind, and OBV distribution — all of which the four neutral agents flagged correctly. The position is held with stop at $51.50; no new capital is deployed into BAC at this run. [decisions.json, run `20260504_192106`]
