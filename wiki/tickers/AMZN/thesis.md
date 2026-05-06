---
name: AMZN thesis
last_updated: 2026-05-06
last_run_id: 20260505_173521
target_words: 500
stale_after_days: 30
word_count: 513
summary: Prior "no capital to act" constraint falsified — portfolio now has $1,617.76 cash and short is allowed; HOLD is now a setup-quality decision, not a capital constraint; 5/5 swing agents unanimous neutral; bullish structural trend intact (ADX 65.1, EMA aligned); entry blocked by lack of a clean R/R setup; wait for 10 EMA pullback $258–$265 or confirmed breakout above $276 on 1.5x+ volume
---

# AMZN — Thesis

## TL;DR

⚠️ Recent trade: stop_hit 2026-05-04, -$10.14. Thesis under review.

**Prior claim falsified:** The 20260504_173321 thesis stated "HOLD is the only allowed action — portfolio cash = $0, risk manager limit = $0." As of run 20260505_173521, that capital constraint no longer holds: portfolio cash is $1,617.76, risk manager max position is $485.33, and `allowed_actions[AMZN]` shows short: 1. **HOLD today is a setup-quality decision, not a capital-constraint decision.** All 5 swing agents returned neutral with 100% agreement — no valid entry exists from current price ($272-273). Two distinct entry scenarios are fully defined and waiting; neither is available today. [source: decisions.json, signals_combined.json, trade_ledger.json, run 20260505_173521]

---

## What falsified the prior thesis claim

The May 4 thesis (run 20260504_173321) stated no trade was possible because cash was zero and risk manager limit was $0. That capital state has changed: other positions closed (DIS stop hit May 5, -$4.99; see trade_ledger.json recent_closures_30d) and portfolio cash is now $1,617.76. The AMZN position remains closed (ID 115 stop_hit at $276 on May 4, P&L -$10.14 — see trade_ledger.json per_ticker_history[AMZN]). No new AMZN capital constraint exists today. The prior AMZN short thesis (mean-reversion from April 30 shooting star) remains falsified by the stop-out: bulls proved control above $268-276. HOLD today reflects the consensus of all five agents that no actionable entry exists at current price, not a lack of capital. [source: trade_ledger.json, decisions.json, run 20260505_173521]

---

## Bull case (structural — intact, waiting for entry)

**AWS as the AI picks-and-shovels play.** Q1 2026 confirmed: EPS $2.78 (beat $1.64 by 69.5%), revenue $181.5B (+17% YoY), AWS $37.6B (+28% YoY), backlog ~$365B (+50% QoQ). OpenAI deepened AWS commitment, pivoting aggressively from Microsoft Azure. Amazon Supply Chain Services launched — described as "AWS of Logistics," threatening UPS/FedEx (-8-9% on announcement). Analyst consensus: ~45 Buy / 2 Hold / 0 Sell, avg PT $311.65. Trend is structurally real: ADX 65.1, EMA aligned (10 > 21 > 50), higher highs/higher lows intact. [source: web_research/AMZN.json, explanation.json, run 20260505_173521]

**Bull entry scenario:** Pullback to 10 EMA zone $258-265 with RSI normalizing below 65 and constructive daily candle — entry ~$262, target $284.65 (Fib 1.272), stop $256, R/R ~3.5:1. OR confirmed daily close above $276 on 1.5x+ volume — entry ~$276.50, measured move target $296, stop $268, R/R ~2.3:1. Neither condition met today.

---

## Bear case (near-term — valid but no trigger)

**Statistical extreme.** RSI-14 80.49, RSI-21 90.43 (deeply overbought). Z-score 2.06. Price 20.36% above 50-SMA. Valuation: DCF gap -47.4% (market cap $2.94T vs. intrinsic value $1.55T). Hourly volume bias negative (0.04x relative volume). Macro tail: Iran-Strait of Hormuz unresolved, WTI $104.10, Fed hawkish succession (Warsh, May 15). ADX 65.1 extreme means reversal attempts face a powerful adversary.

**Prior short falsified:** Mean-reversion short (run 20260501_173921) stopped out May 4 at $276 (-$10.14) — bulls absorbed the distribution zone. Two consecutive stop-outs in RSI 80+/ADX 60+ environment (NVDA Apr 30 -$63.20, AMZN May 4 -$10.14) are a pattern flag: do NOT re-enter shorts in this regime without hourly RSI-21 >75 PLUS volume-confirmed rejection candle at $273-276. Current hourly RSI-21 is only 67.45 with near-zero volume (0.04x). Short trigger not met. [source: signals_combined.json, trade_ledger.json ID 115, run 20260505_173521]

---

## What would change my mind

**Bull re-entry:** Price pulls back to 10 EMA zone $258-265, RSI cools below 65, constructive daily candle. OR confirmed daily close above $276 on 1.5x+ volume (breakout long).

**Bear re-entry (short):** Hourly RSI-21 >75 PLUS volume-confirmed rejection candle at $273-276 resistance. Entry ~$272-273, target $257 (Fib 23.6%), stop $277, R/R ~2.5:1. Both conditions must be met simultaneously — stop-out pattern demands higher confirmation bar.

**Macro catalyst:** Durable Iran ceasefire removes energy cost tail and restores clean risk-on bid for AMZN AI premium. Hawkish Warsh confirmation on May 15 would be a bearish catalyst for high-multiple growth.
