---
name: MU thesis
last_updated: 2026-05-05
last_run_id: 20260505_211609
target_words: 500
stale_after_days: 30
word_count: 503
summary: HBM leader with exceptional fundamentals (revenue +48.9% YoY, EPS +997%); price $640 (up from $542 bootstrap); prior bullish signal ($503 entry, $609 target) fully achieved and exceeded; AMD binary now resolved (May 5 AMC passed); wait-to-buy $514-530 (10 EMA zone) for 2:1 R/R long toward $692
---

# MU — Thesis

## TL;DR

Micron is one of three global HBM suppliers (~21% share) with exceptional near-term fundamentals: Q2 FY26 revenue $23.86B (+196% YoY), non-GAAP EPS $12.20, Q3 FY26 guide $33.5B at ~81% gross margin; HBM4 in volume production for NVIDIA Vera Rubin. Stock at ~$640 (run 20260505_211609) is 34.5% above the 50-SMA — the prior bullish signal (entry $503, target $609, from prior run) has been fully achieved and exceeded. AMD Q1 2026 earnings printed May 5 AMC (the binary gate flagged in prior runs) — results now resolved. Wait for pullback to the 10 EMA zone ($514–$530) before considering a fresh long entry with proper 2:1 R/R toward the $692 Fib extension target. Fundamentals are strong; timing and entry discipline are the gating factors. [source: signals_combined.json swing_head_trader MU + decisions.json, run 20260505_211609]

**Prior thesis claim superseded:** The bootstrap thesis (2026-05-01) cited stock at $542.21. Price has since run to $640 and the AMD binary gate has now closed (May 5 AMC). The prior "wait for AMD binary" gating instruction has expired; the new gating factor is R/R discipline at $514–$530 entry.

## Bull case

- **HBM demand supercycle.** Micron estimates 50–67% of medium-term HBM demand unmet; DRAM prices up 60% in 2025 with another 30–40% projected for 2026. HBM demand growing 70% YoY across a supply-constrained oligopoly. [source: web_research/MU.json competitor_activity, run 20260505_211609]
- **Exceptional Q2 FY26 print.** Revenue $23.86B (+196% YoY), non-GAAP GM ~81%, Q3 FY26 guide $33.5B. HBM4 36GB 12-high in volume production for NVIDIA Vera Rubin. [source: web_research/MU.json earnings_info, run 20260505_211609]
- **Strong fundamentals.** ROE 15.76%, net margin 22.84%, operating margin 26.14%, EPS growth +997% YoY, revenue growth +48.9% YoY. PEG ratio 0.2 — fundamentally attractive relative to growth. [source: signals_combined.json fundamentals_analyst_agent MU, run 20260505_211609]
- **Analyst support.** DA Davidson initiated Buy at $1,000 (highest on Street); Melius Research Buy $700; TD Cowen raised to $660. Strong Buy consensus (30 analysts). [source: web_research/MU.json analyst_consensus, run 20260505_211609]
- **New enterprise product.** Micron began shipping the 6600 ION SSD — world's highest-capacity storage device, bolstering enterprise portfolio. [source: web_research/MU.json ticker_news, run 20260505_211609]

## Bear case

- **Valuation extreme.** DCF intrinsic value ~$20.8B vs market cap ~$722B — 97% overvaluation gap (valuation_analyst_agent bearish, confidence 100). EV/EBITDA gap -32.1%. [source: signals_combined.json valuation_analyst_agent MU, run 20260505_211609]
- **Overbought across all timeframes.** Z-score 2.74, RSI-7 84.4, daily and hourly pct_b both >1.0. Hourly OBV bearish divergence (OBV trend down while price makes new highs). Hourly relative volume 0.25x average. [source: signals_combined.json swing_macro_context + swing_mean_reversion MU, run 20260505_211609]
- **Samsung competition.** Samsung HBM4 qualification for NVIDIA improving; SK Hynix remains the dominant HBM supplier (revenue from AI memory tripled). Micron's ASP and share face compression if Samsung fully qualifies. [source: web_research/MU.json competitor_activity, run 20260505_211609]
- **Correlation-blocked.** SNDK+MU cluster correlation 70.2%; cluster cap exceeded at current prices — risk manager blocked MU from the portfolio even without the R/R failure. [source: signals_combined.json risk_management_agent MU, run 20260505_211609]
- **Memory cyclicality.** ~81% gross margins extrapolated at peak; prior supercycles have mean-reverted violently when supply caught demand. [source: thesis judgment]

## What would change my mind

- **Bear flips bullish if:** Pullback to $514–$530 (10 EMA zone) on lower volume with bullish candle and R/R ≥ 2:1 to $692 Fib target; AMD Q1 earnings positive HBM guidance (to be confirmed post-AMC); Samsung HBM4 NVIDIA qualification slips; Q3 FY26 print beats $33.5B guide with GM holding ≥81%.
- **Bull flips bearish if:** Samsung qualifies HBM4 at scale with NVIDIA; any major hyperscaler cuts AI capex guidance; Q3 FY26 misses $33.5B guide or GM compresses below 78%; MU closes below 50 SMA ($437) on volume; DRAM contract pricing rolls over for two consecutive months.
