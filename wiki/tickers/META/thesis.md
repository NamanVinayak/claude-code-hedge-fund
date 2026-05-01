---
name: META thesis
last_updated: 2026-04-30
last_run_id: 20260430_141238
target_words: 500
stale_after_days: 30
confidence_score: 70
word_count: 498
summary: Prior bull thesis (breakout long at $675-677) is fully invalidated by Q1 2026 earnings capex shock; bias flipped to bearish medium-term pending reassessment of $125-145B capex narrative.
---

# META — Thesis

## TL;DR

The prior bull thesis — buy breakout at $675–677 targeting $706–710 on AI monetization + ad dominance — is falsified. The prior "bear to bull" trigger was "Q1 2026 earnings beat with capex discipline signal." Q1 2026 did deliver a massive EPS beat ($10.44 vs $6.65 est, +57%) and revenue beat ($56.31B, +33% YoY), but capital discipline was the opposite: full-year capex guidance was raised from $115–135B to **$125–145B**. This is the bear case materializing, not the bull trigger. Price collapsed ~10% from $669 to ~$601–603 on 9.99x hourly volume (source: web_research/META.json, explanation.json, run 20260430_141238). Medium-term bias is now bearish; HOLD awaiting dead-cat bounce to $618–630 before considering a short entry to $583.

## What falsified the prior bull thesis

The prior thesis (bootstrap, 2026-04-29) explicitly stated: "Bear to bull trigger: Q1 2026 earnings beat with raised guidance AND any capex discipline signal." The Q1 2026 earnings on April 29 delivered the beat but the inverse of discipline — capex was raised again, not guided lower. The $125–145B plan now nearly doubles FY2025's $72B. Institutional sellers confirmed this reading via 9.99x relative hourly volume (source: signals_combined.json, swing_head_trader signal, run 20260430_141238).

## Bull case (still live, but secondary)

**Fundamentals remain strong.** Revenue growth 22.2% YoY; operating margin 41.4%; ROE 27.83%; debt-to-equity 0.27; current ratio 2.60. These are class-leading metrics (source: signals_combined.json, fundamentals_analyst_agent, run 20260430_141238).

**Mean-reversion snap-back is near-term probable.** Hourly RSI-21 at 14.7 and BB %B at -0.993 are extreme oversold readings historically consistent with a 3–7 day bounce. The mean_reversion agent rates this bullish at 68% confidence for a snap-back to $651 (source: signals_combined.json, swing_mean_reversion, run 20260430_141238).

**Analyst consensus still heavily bullish.** 28 buy / 5 hold / 0 sell; avg price target ~$840. EV/EBITDA analysis implies intrinsic value above $2.2T vs. $1.5T market cap (source: web_research/META.json, run 20260430_141238).

## Bear case (now primary)

**Capex shock is a thesis-changing event.** The $125–145B capex plan raised April 29, 2026 confirms the bear case: free cash flow compression is real, not hypothetical. FCF growth trend was already -14.7% entering this run. The catalyst_news agent (72% confidence) explicitly classifies this as institutional re-rating, not panic (source: signals_combined.json, run 20260430_141238).

**Key support broken on extreme volume.** The $627.61 support level (11 prior tests) was breached on 9.99x hourly volume. Measured-move target is $583. DCF model values META at ~$724B vs. $1.5T market cap — 52.6% overvalued (source: signals_combined.json, valuation_analyst_agent, run 20260430_141238).

**Litigation overhang unchanged.** California 70% liability verdict; 10,000+ lawsuits; New Mexico $375M award; Massachusetts AG proceeding. Open-ended liability remains a structural discount factor (source: web_research/META.json, run 20260430_141238).

**Layoffs signal capex pressure is real.** ~8,000 employees (10% workforce) cut alongside 6,000 frozen roles — cost offsets against rising capex are being activated (source: web_research/META.json, run 20260430_141238).

## What would change my mind

**Bearish to bullish:** Two consecutive quarters of capex stabilization at or below $125B with ad revenue growth re-accelerating above 25%. A litigation framework settlement removing open-ended liability. Hourly price stabilization above $630 with volume confirmation.

**Bullish to more bearish:** Capex further raised above $145B. Ad revenue growth below 20% in Q2 2026. Iran disruption materially impacting DAP growth (already cited as a factor in Q1 2026 DAP miss: 3.56B, +4% YoY but down >5% QoQ).

## Source runs

- swing_20260411_211655 (hold at $625, R:R 1.4:1 failed 2:1 minimum)
- 20260415_093758 (buy 1 share at $675.75, confidence 63%)
- 20260417_233350 (buy 15 shares at $676.87, confidence 74%)
- 20260430_141238 (HOLD, bearish bias; prior long thesis invalidated by capex shock)
