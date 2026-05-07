---
name: MU thesis
last_updated: 2026-05-07
last_run_id: 20260507_211526
target_words: 500
stale_after_days: 30
word_count: 498
summary: HBM leader with exceptional fundamentals (revenue +48.9% YoY, EPS +997%); price $646.63 intraday (pulled back from $667 prior run); JEDEC HBM4 conference May 12-13 is the concrete near-term catalyst (5-6 trading days); 5.5:1 R/R setup identified but blocked by MU+SNDK cluster cap; wait-to-buy zone is $627-$650 (hourly support entry) with cluster cap removal; 10-EMA zone migrated to $560 (from prior $514-530)
---

# MU — Thesis

## TL;DR

Micron is one of three global HBM suppliers (~21% share) with exceptional near-term fundamentals: revenue +48.9% YoY, EPS +997% YoY, operating margin 26.14%, ROE 15.76%, PEG 0.23. HBM capacity sold out through end of 2026 (~$8B annualized run-rate). Price is ~$646.63 intraday (run 20260507_211526), pulled back 3% from the $667 prior run high. The JEDEC industry conference May 12–13 (5–6 trading days) is a concrete near-term catalyst — Micron presenting on HBM4 and cloud AI memory specifically on May 13. AMD Q1 2026 blowout (+38% YoY revenue) confirmed HBM demand is intact. The 5.5:1 R/R setup (entry $647, stop $625, target $764.55) is mathematically excellent — but the trade is **blocked by the MU+SNDK cluster cap** (combined $874 > 30% of $1,457 capital per risk_management_agent). The 10-EMA has migrated to ~$560 — the prior wait-to-buy zone of $514–$530 is stale. [source: signals_combined.json swing_head_trader MU + decisions.json + web_research/MU.json, run 20260507_211526]

**Prior thesis claim superseded this run:** The prior wait-to-buy zone ($514–$530, 10-EMA as of run 20260505_211609) is stale — the 10-EMA has migrated to ~$560 as the uptrend extended. Additionally, the prior thesis cited the AMD binary gate (May 5 AMC) as a gating factor — that gate has now closed as a blowout. The new gating factor is the MU+SNDK cluster cap; the new watch scenario is the JEDEC May 13 catalyst entry at $627–$650 if the cluster cap is removed.

## Bull case

- **HBM demand supercycle intact.** AMD Q1 2026 blowout (+38% YoY revenue, HBM demand confirmed May 5 AMC) is the most recent direct read-through. JEDEC May 13 presentation on HBM4 is the next concrete near-term catalyst. [source: web_research/MU.json + signals_combined.json swing_catalyst_news MU, run 20260507_211526]
- **Exceptional fundamentals.** ROE 15.76%, net margin 22.84%, operating margin 26.14%, EPS growth +997% YoY, revenue growth +48.9% YoY. PEG ratio 0.23 — fundamentally attractive relative to growth rate. D/E 0.22; current ratio 2.52 — healthy balance sheet. Fitch upgraded to BBB+. [source: signals_combined.json fundamentals_analyst_agent MU + web_research/MU.json, run 20260507_211526]
- **5.5:1 R/R identified.** Entry $647, stop $625 (hourly support 4 tests), target $764.55 (Fib ext 1.272x) = 5.5:1. Comfortably exceeds the 3:1+ preferred minimum. [source: signals_combined.json swing_macro_context MU, run 20260507_211526]
- **Analyst conviction.** DA Davidson $1,000 (initiated May 2026); Melius Research $700; TD Cowen $660; 39 Buy / 5 Hold / 0 Sell. [source: web_research/MU.json analyst_consensus, run 20260507_211526]
- **Macro tailwind.** Dow crossed 50,000 for first time ever (May 7); S&P/Nasdaq at ATHs; AI capex supercycle confirmed. Macro_context agent bullish (62 conf). [source: web_research/MU.json macro_context, run 20260507_211526]

## Bear case

- **Valuation extreme.** DCF intrinsic value ~$20.8B vs market cap ~$729B — 97% overvaluation gap. EV/EBITDA gap -32.2%. Valuation_analyst_agent bearish at 100% confidence. [source: signals_combined.json valuation_analyst_agent MU, run 20260507_211526]
- **Overbought across all timeframes.** Z-score 3.27 (highest of both tickers — most statistically stretched), RSI-7 88.35, RSI-14 87.17, daily pct_b 1.12 (above upper band). [source: signals_combined.json swing_mean_reversion MU, run 20260507_211526]
- **Hourly OBV divergence returned.** Bearish OBV divergence reappeared this run after clearing last run — the most positive technical development from 20260506_211601 has reversed. Hourly rel vol 0.38x (severely sub-threshold). [source: signals_combined.json swing_breakout MU, run 20260507_211526]
- **Cluster cap blocks all entries.** Risk manager `remaining_position_limit = 0.0` — MU+SNDK combined $874 > 30% of $1,457 capital. No new MU position possible until cluster cap is resolved. [source: signals_combined.json risk_management_agent MU, run 20260507_211526]
- **Memory cyclicality.** ~81% gross margins at cycle peak; prior supercycles mean-reverted violently when supply caught demand. Samsung HBM4 NVIDIA qualification is active compression risk. [source: web_research/MU.json competitor_activity, run 20260507_211526]

## What would change my mind

- **Bear flips bullish if:** Cluster cap resolved (WDC or SNDK exited) + pullback to $627–$650 hourly support entry zone holds with JEDEC catalyst intact; or pullback to 10-EMA (~$560) with momentum re-acceleration and R/R ≥ 3:1 to Fib target.
- **Bull flips bearish if:** Samsung qualifies HBM4 at scale with NVIDIA; any major hyperscaler cuts AI capex guidance; JEDEC May 13 presentation disappoints on HBM4 roadmap; hourly OBV divergence accelerates (OBV turning decisively down while price makes new highs); MU closes below $625 hourly support on volume.
