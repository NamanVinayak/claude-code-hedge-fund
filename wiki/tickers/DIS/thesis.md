---
name: DIS thesis
last_updated: 2026-05-06
last_run_id: 20260506_220627
target_words: 500
stale_after_days: 30
word_count: 498
summary: Post-earnings gap-up confirmed ($100.48→$108.06, +7.5%, 1.81x volume); pre-stated bull trigger fired; earnings blackout (3-day) prevents new entry until May 9+; R/R at $108 catastrophically poor (0.16:1); wait for pullback to $105–107 consolidation zone for fresh long with acceptable R/R
---

# DIS — Thesis

## TL;DR

⚠️ Recent trade: stop_hit 2026-05-05, -$4.99. Thesis under review.

**Prior thesis falsified (additional):** The May 5 thesis stated "Earnings tomorrow May 6 — reassess post-print." The reassessment is now complete: Q2 FY2026 earnings beat (EPS $1.57 vs. $1.49 est, revenue $25.17B vs. $24.84B est) triggered the pre-stated bull restart condition — "gap and hold above $104.83 on 1.5x+ volume = fresh long opportunity." Both conditions were met: price gapped to $108.06 (+7.5%) and daily volume came in at 1.81x average (above the 1.5x minimum that failed in the prior May 5 trade). [source: `web_research/DIS.json`, `signals_combined.json swing_breakout`, run `20260506_220627`]

**However:** The earnings blackout rule (3-day window) prohibits any new position until at least May 9+. Additionally, R/R at the $108 gap price is 0.16:1 ($1.14 upside to $109.14 resistance vs. $7.36 downside to $100.61 support) — making a chase entry mathematically indefensible regardless of blackout. [source: `signals_combined.json swing_macro_context`, `risk_management_agent`, run `20260506_220627`]

---

## Bull case

**Q2 FY2026 beat confirms streaming inflection.** EPS $1.57 beat $1.49 estimate; revenue $25.17B beat $24.84B estimate. New CEO Josh D'Amaro raised FY2026 adjusted EPS growth guidance to ~12% and guided for double-digit EPS growth in FY2027. Streaming profitability trend intact — DTC operating income confirmed above prior guidance. [source: `web_research/DIS.json`, run `20260506_220627`]

**Pre-stated breakout trigger fired.** The post-earnings gap above $104.83 on 1.81x volume satisfies both conditions of the pre-specified bull restart condition. The 11-test resistance at $107.11 has been decisively cleared. Daily volume at 1.81x addresses the key failure of the May 1 trade (only 1.23x volume). [source: `signals_combined.json swing_breakout`, run `20260506_220627`]

**Catalyst pipeline intact.** The Mandalorian and Grogu theatrical release May 22 (first major Star Wars film in years), Big Thunder Mountain Railroad reopened, Josh D'Amaro CEO transition June. Analyst consensus Buy with avg PT ~$131 (range $77–$160 across 42 analysts) implies ~21% upside from current price. Raymond James Outperform ($115 PT), Guggenheim Buy ($140 PT). [source: `web_research/DIS.json`, run `20260506_220627`]

**Compelling valuation.** P/E 15.91 vs. market average ~20x. EV/EBITDA analysis suggests undervaluation (owner earnings model shows 1,613% gap above market cap). [source: `signals_combined.json valuation_analyst_agent`, run `20260506_220627`]

---

## Bear case

**Hourly OBV bearish divergence on gap day.** OBV trended DOWN as price spiked on 0.55x relative hourly volume — a distribution signal. If informed money is selling into the gap rather than accumulating, the move may fade. This is the single most important risk flag. [source: `signals_combined.json swing_mean_reversion`, run `20260506_220627`]

**R/R at gap price is catastrophically poor.** At $108, upside to nearest resistance $109.14 = +$1.14, downside to $100.61 = -$7.36. R/R of 0.16:1 is one of the worst figures in recent run history. Even a bullish setup cannot be acted upon at these levels. [source: `signals_combined.json swing_macro_context`, run `20260506_220627`]

**Declining margins.** Operating margin declining (-0.52% per period trend), net margin declining (-1.06% per period). Current ratio 0.71 — short-term liquidity tight. DCF analysis shows 37.2% gap between fair value ($120B) and market cap ($191B). [source: `signals_combined.json growth_analyst_agent`, `valuation_analyst_agent`, run `20260506_220627`]

**Warner Bros. Discovery + Netflix consolidation.** Combined entity would control ~22% U.S. streaming share — structural competitive pressure if cleared. [source: `web_research/DIS.json`, run `20260506_220627`]

---

## What would change the thesis

**Post-blackout pullback long (May 9+):** If DIS pulls back to $105–107 consolidation zone with volume easing (not distribution), a fresh long with stop below $104.50 and target $115.77 achieves acceptable R/R. This is the primary watch scenario.

**Failed breakout — bear trigger:** If DIS closes back below the $107.11 breakout level on elevated volume before May 9, the gap is a failed breakout — reassess for short on bounce to $107–108.

**Gap fill risk:** Post-earnings gaps that lack OBV confirmation (like this one) have elevated gap-fill probability. If price returns to $100–104 zone, the thesis resets to pre-earnings neutral.
