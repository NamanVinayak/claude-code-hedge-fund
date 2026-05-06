---
name: META thesis
last_updated: 2026-05-06
last_run_id: 20260506_140335
target_words: 500
stale_after_days: 30
word_count: 497
summary: Cover decision issued for trade id 118 (fill $611.78, current $604.96, ~$6.82 gain locked); R/R degraded to 0.17:1 from current levels; extreme oversold RSI-7 6.52 + bullish RSI divergence made holding risky; capex-shock bearish thesis remains structurally intact; re-entry plan on failed bounce to $612-614; cover action run 20260506_140335.
---

# META — Thesis

## TL;DR

The PM has issued a **cover** decision for trade id 118 (run 20260506_140335, 55% confidence). The short (fill $611.78, entered 2026-05-04) is being closed at ~$604.96, locking in approximately **$6.82/share gain**. The bearish structural thesis (capex shock, litigation, ADX 52.76 downtrend) remains intact — but the risk-reward for holding has degraded to 0.17:1 ($4.96 remaining to $580 target vs. $30 adverse risk to $635 stop). RSI-7 at 6.52 with confirmed bullish RSI divergence on both daily and hourly timeframes represents extreme mean-reversion risk. Re-entry plan: wait for a failed bounce to $612–614 resistance zone, enter short on bearish rejection candle. (source: decisions.json, signals_combined.json, trade_ledger.json id 118, run 20260506_140335)

**What changed from prior thesis (run 20260505_140723 — hold):** The prior thesis held the short with R/R 2.5:1 and RSI-7 at 23.22 (oversold but not extreme). This run: RSI-7 collapsed further to 6.52 (extreme), bullish RSI divergence confirmed on both timeframes, hourly OBV diverging bullishly, and the remaining R/R degraded to 0.17:1. The prior claim of "MFE +2.78% / R/R 2.5:1 — tracking well" is superseded. The trade did not falsify the bearish thesis; it harvested a gain from a deteriorating risk-reward setup.

## What falsified the prior bull thesis (carried forward)

The prior thesis (bootstrap 2026-04-29, run 20260430_141238) stated: "Bear to bull trigger: Q1 2026 earnings beat with raised guidance AND any capex discipline signal." The Q1 2026 earnings on April 29 delivered the beat but the inverse of discipline — capex was raised from $115–135B to $125–145B, nearly doubling FY2025's $72B. Institutional sellers confirmed this reading via 3.2x relative daily volume on April 30. (source: signals_combined.json, swing_head_trader, run 20260430_141238)

## Bull case (structurally intact, secondary)

**Fundamentals class-leading.** Revenue +22.2% YoY, operating margin 41.4%, ROE 27.83%, D/E 0.27, current ratio 2.60. EV/EBITDA model shows ~44.5% upside vs. current market cap. PEG ratio 0.93. (source: signals_combined.json, fundamentals_analyst_agent, run 20260506_140335)

**Analyst consensus broadly bullish.** 61 Buy / 0 Sell out of analysts; avg price target $839.87; median $856; range $676–$1,144. Snap Q1 2026 swung to $45M profit — positive digital-ad read-through. (source: web_research/META.json, run 20260506_140335)

**RSI-7 at 6.52 — extreme mean-reversion setup.** Bullish RSI divergence confirmed on both daily and hourly timeframes. Fibonacci 50% retracement at $605.89 is the natural bounce node. Hourly OBV diverging upward from falling price signals early accumulation. (source: signals_combined.json, swing_mean_reversion, run 20260506_140335)

## Bear case (primary, thesis intact)

**Capex shock remains thesis-defining.** Full-year 2026 capex $125–145B — nearly double FY2025's $72B. No cloud revenue stream. FCF compression expected 2–3 years. Meta layoffs ~8,000 employees (10% workforce) concurrent with $135B AI spending. (source: web_research/META.json, run 20260506_140335)

**Trend structure extremely bearish.** Daily ADX 52.76 (-DI 39.5 >> +DI 11.36), price below ALL EMAs. ROC 5d −9.89%, ROC 10d −9.55%. OBV down daily. MACD histogram -8.207 deeply negative. (source: signals_combined.json, run 20260506_140335)

**Litigation overhang worsened.** New Mexico $3.7B youth-harm trial (started May 2026); Reuters Pulitzer Prize reporting on harmful AI chatbots and fraudulent ads. CA 70% liability verdict and 10,000+ suits unchanged. (source: web_research/META.json, run 20260506_140335)

**Macro headwind (partial).** Fed Chair Warsh transition May 15 (hawkish, rate-tightening tail risk). US-Iran ceasefire talks advancing — if deal closes, removes macro tailwind for fresh bearish entries. (source: web_research/META.json macro_context, run 20260506_140335)

## What would change my mind

**Re-entry short trigger:** Failed bounce to $612–614 hourly resistance with bearish rejection candle and volume. Stop above $621. Target $580–585 (Fib 61.8% $585.68).

**Bearish invalidation (medium-term):** Two consecutive quarters of capex stabilization at or below $125B with ad revenue re-accelerating above 25%. Litigation framework settlement. Price recapture above $635 on 1.5x+ volume.

## Source runs

- swing_20260411_211655 through 20260504_143030 (conditional short issued)
- 20260504_143030 (SHORT 1 share at $621, fill $611.78, stop $635, target $575)
- 20260505_140723 (HOLD existing short id 118, R/R 2.5:1)
- 20260506_140335 (COVER id 118 at ~$605, lock in ~$6.82 gain, re-enter on bounce)
