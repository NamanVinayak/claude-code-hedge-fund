---
name: META thesis
last_updated: 2026-05-05
last_run_id: 20260505_140723
target_words: 500
stale_after_days: 30
word_count: 498
summary: Active short position confirmed — trade id 118 filled at $611.78; prior "conditional short pending bounce" stance now an open trade; MFE +2.78% / MAE 0%; capex shock thesis intact; hold decision with stop $635, target $580, R/R 2.5:1.
---

# META — Thesis

## TL;DR

The prior conditional short decision (run 20260504_143030: "short 1 share at $621 limit, pending dead-cat bounce") has **converted to an active open position**. Trade id 118 is now entered: fill price $611.78, stop $635, target $580, R/R 2.5:1, 58% confidence. MFE +2.78%, MAE 0.0% — tracking well. The capex-shock bearish thesis remains the controlling narrative. PM decision: **hold**, no new entry allowed (same-direction stacking blocked, remaining position limit = 0). (source: trade_ledger.json id 118, decisions.json, explanation.json, run 20260505_140723)

**What advanced from the prior thesis:** The prior thesis (run 20260504_143030) had a placed conditional order with the entry trigger NOT yet met. This run confirms the entry materialized — price bounced into the $619–621 resistance zone and the short was filled at $611.78 (within 1.5% tolerance). The "pending bounce" posture is now a live trade.

## What falsified the prior bull thesis (carried forward)

The prior thesis (bootstrap 2026-04-29, run 20260430_141238) stated: "Bear to bull trigger: Q1 2026 earnings beat with raised guidance AND any capex discipline signal." The Q1 2026 earnings on April 29 delivered the beat but the inverse of discipline — capex was raised from $115–135B to $125–145B, nearly doubling FY2025's $72B. Institutional sellers confirmed this reading via 3.2x relative daily volume on April 30. (source: signals_combined.json, swing_head_trader, run 20260430_141238)

## Bull case (structurally intact, secondary)

**Fundamentals class-leading.** Revenue +22.2% YoY, operating margin 41.4%, ROE 27.83%, D/E 0.27, current ratio 2.60. EV/EBITDA model shows ~44.5% upside vs. current market cap. PEG ratio 0.93 (below 1.0). (source: signals_combined.json, fundamentals_analyst_agent, run 20260505_140723)

**Analyst consensus still broadly bullish.** 61 Buy / 6 Hold / 0 Sell out of 67 analysts; avg price target $839. No new downgrades week of May 5 beyond prior JPMorgan move to Neutral. Meta on track to surpass Google in global digital ad revenue ($243B vs $239B projected 2026). (source: web_research/META.json, run 20260505_140723)

**RSI recovering from extreme oversold.** RSI-7 at 23.22, up from 18.56 (May 4) — the worst oversold extreme has passed. Short-term downside continuation is less certain at these levels. (source: signals_combined.json, swing_mean_reversion, run 20260505_140723)

## Bear case (primary, confirmed)

**Capex shock remains thesis-defining.** Full-year 2026 capex raised to $125–145B (also raised again at May 4 web research: $125–145B range; analysts flagging margin compression). No cloud revenue stream (vs. Alphabet $20B Cloud quarter, +63% YoY). FCF compression expected 2–3 years. (source: web_research/META.json, run 20260505_140723)

**Trend structure extremely bearish.** Daily ADX 50.73 (-DI 38.27 >> +DI 16.01), hourly ADX 63.39 (-DI 45.47 >> +DI 10.07). Price below ALL EMAs on both timeframes. ROC 5d −10.05%, ROC 10d −9.02%. OBV down on both timeframes. (source: signals_combined.json, run 20260505_140723)

**Macro headwinds intact.** Iran-UAE/Strait of Hormuz conflict ongoing (oil >$102/bbl); Fed 3.5–3.75% with hawkish Warsh succession (May 15); S&P recovered May 5 (+0.7–1%) but Iran risk unresolved. (source: web_research/META.json macro_context, run 20260505_140723)

**Litigation overhang worsened.** New Mexico seeks $3.7B and platform overhaul (trial starting May 2026); Reuters Pulitzer Prize reporting on harmful AI chatbots to children and fraudulent ads. CA liability verdict and 10,000+ suits unchanged. (source: web_research/META.json ticker_news, run 20260505_140723)

## What would change my mind

**Bearish invalidation of short (stop hit):** Price recapture above $635 — stop triggered, trade closed at loss.

**Bearish to bullish (medium-term):** Two consecutive quarters of capex stabilization at or below $125B with ad revenue re-accelerating above 25%. Litigation framework settlement. Price recapture above $635 on 1.5x+ volume.

## Source runs

- swing_20260411_211655 (hold at $625, R:R 1.4:1 failed 2:1 minimum)
- 20260415_093758 (buy 1 share at $675.75, confidence 63%)
- 20260417_233350 (buy 15 shares at $676.87, confidence 74%)
- 20260430_141238 (HOLD, bearish bias; prior long thesis invalidated by capex shock)
- 20260501_142327 (HOLD, bearish conditional; dead-cat bounce watch, no entry at $611–612)
- 20260504_143030 (CONDITIONAL SHORT, 1 share at $621, target $575, stop $635, R/R 3.3:1, conf 62)
- 20260505_140723 (HOLD existing short id 118, fill $611.78, target $580, stop $635, R/R 2.5:1, conf 58)
