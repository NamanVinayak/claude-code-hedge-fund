---
name: BAC thesis
last_updated: 2026-05-06
last_run_id: 20260506_190825
target_words: 500
stale_after_days: 30
word_count: 498
summary: SELL issued — PM exiting 15-share long at market (~$53.72); prior "Iran escalation falsifies macro tailwind" thesis updated — Iran ceasefire MOU now ~48h from completion (macro improved), but bearish technicals (OBV distribution, DI crossover, 0.75:1 R/R, valuation -35.8%) override the macro recovery; unanimous 5/5 neutral; exit is proactive, not stop-hit
---

## TL;DR

**PM issued SELL on the 15-share long (id 110, $52.75 cost basis) at market (~$53.72) on May 6, 2026 (run `20260506_190825`).** **Prior thesis falsification:** The May 4 thesis (run `20260504_192106`) described Iran escalation as the primary macro headwind. That specific claim is now reversed: US-Iran ceasefire MOU is reportedly ~48 hours from completion as of May 6, S&P 500 confirmed ATH close at 7,338.89 (+1.10%). The macro headwind has eased. However, the sell decision is not driven by macro — it is driven by deteriorating technical internals and failed R/R that were present even before the macro improvement. The macro recovery does not fix the bearish DI crossover, OBV distribution on both timeframes, or a risk-reward ratio of 0.75:1 that fails the 2:1 minimum. [decisions.json, signals_combined.json, run `20260506_190825`]

---

## Prior Thesis Claim Falsified

**Falsified claim (run `20260504_192106`):** "Iran-US ceasefire collapsed — new macro backdrop is mixed-to-cautious for banks."

**What falsified it (run `20260506_190825`):** US-Iran ceasefire MOU negotiations are reportedly ~48 hours from completion. S&P 500 and Nasdaq confirmed ATH closes May 6. Oil easing toward $102/bbl from ~$110 peak. The Iran escalation narrative reversed. [web_research/BAC.json, run `20260506_190825`]

**Note:** The macro falsification does NOT change the sell decision. The exit is driven by technical deterioration and R/R failure, not the macro thesis. The bearish case stands on independent technical grounds.

---

## Bull Case

**Fundamentals remain genuinely solid.** Q1 2026: EPS $1.11 beat (+9.9%), NII +9% YoY, zero trading loss days. Q2 EPS estimate $1.09, revenue $29.99B. Analyst consensus 18 Strong Buy / 4 Buy of 24 brokerages, avg PT $60.34, median $62.00 — implying ~12–15% upside from $53.72. $18.66B trailing buyback pace; Basel III endgame softening could unlock ~$40B additional buyback capacity. PEG ratio 0.93 (cheap relative to growth). [web_research/BAC.json, run `20260506_190825`]

**EMA alignment structurally intact.** Daily EMA staircase bullish (EMA-10 $52.86 > EMA-21 $52.37 > EMA-50 $51.65). ADX 44.67 — strong trend. Macro regime now strongly risk-on (S&P ATH). [signals_combined.json, swing_trend_momentum]

---

## Bear Case

**OBV distribution divergence on both timeframes.** On-Balance Volume trending down on daily and hourly despite price bouncing from $52.19 to $53.72 — institutional distribution into the bounce. This signal was present in May 4 and May 5 runs and has not resolved. [signals_combined.json, swing_macro_context, swing_trend_momentum, run `20260506_190825`]

**Bearish DI crossover.** Minus DI (26.59) exceeds Plus DI (20.31) — selling pressure now dominant despite bullish EMA alignment. Daily MACD histogram -0.1405 (negative). 10d ROC -0.67% (decelerating). [signals_combined.json, swing_trend_momentum]

**R/R 0.75:1 fails the 2:1 minimum.** From $53.72 intraday, target $55.40 = +$1.68 upside; prior stop $51.50 = -$2.22 downside. R/R approximately 0.75:1 — well below the 2:1 minimum. [decisions.json, run `20260506_190825`]

**Valuation agent: -35.8% overvalued.** Residual income analysis calculates intrinsic value ~$244.8B vs market cap $381.3B — a 35.8% premium. 100% confidence bearish signal. [signals_combined.json, valuation_analyst_agent]

**Unanimous 5/5 neutral signal.** All five swing agents (trend_momentum, mean_reversion, breakout, catalyst_news, macro_context) issued neutral signals for a new entry. No agent found a reason to hold or add. [signals_combined.json, swing_head_trader, run `20260506_190825`]

---

## What Would Change the Thesis

Position is being exited. Re-entry criteria for a new long: OBV divergence resolves (OBV resumes uptrend), daily MACD histogram turns positive, 5d AND 10d ROC both positive, R/R ≥ 2:1, AND either macro remains risk-on or Berkshire overhang clears. No re-entry while all momentum signals negative.

---

## Synthesis

The 15-share long initiated Apr 30 (id 110) is being exited proactively. The position achieved unrealized gain of ~$14.55 (+$0.97/share) but the forward risk-reward of 0.75:1 and confirmed OBV distribution on both timeframes justify the exit. The macro improvement (ceasefire, ATH) is real but is a sector-wide tailwind, not BAC-specific. BAC-specific technicals (DI crossover, OBV divergence, MACD histogram negative) override the macro recovery. [decisions.json, run `20260506_190825`]
