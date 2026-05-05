---
name: WDC thesis
last_updated: 2026-05-05
last_run_id: 20260505_203524
target_words: 500
stale_after_days: 30
word_count: 600
summary: cluster cap resolved — buy decision issued (2 shares limit $446, target $489, stop $428, R/R 2.39:1, conf 44); ATH $446.62 broke and now flipped to support; prior correlation-block falsified; hourly OBV divergence is key watch risk
---

# WDC — Thesis

## TL;DR

Run 20260505_203524 (2026-05-05). Decision: **buy — 2 shares, limit $446, target $489, stop $428, R/R 2.39:1, conf 44**.

Prior thesis claim falsified: "Correlation-blocked; cluster cap in force" (20260504_203608). That block is now resolved — STX received a hold decision this run (no new STX position), which means the STX+WDC cluster cap ($971 combined) is no longer triggered. PM issued a buy order. [source: decisions.json, signals_combined.json risk_management_agent, run 20260505_203524]

Prior thesis claim partially falsified: "ATH $446.62 directly overhead as resistance." Price broke above ATH intraday (high $453.83), though daily close ($442.36) was below the level. Former resistance has now flipped to support; the breakout is conditionally confirmed. [source: signals_combined.json swing_breakout, run 20260505_203524]

## Bull case

- **Pure-play HDD after SanDisk divestiture.** WDC divested SanDisk for $3.1B in Feb 2026, creating a focused high-capacity nearline HDD business entirely aligned to AI hyperscaler demand. [source: web_research/WDC.json competitor_activity]
- **Q3 FY26 blowout — fresh catalyst (5 days old).** Revenue $3.3B (+45% YoY), EPS $2.72 blowout. First-ever gross margin above 50% (50.5%). Cloud = 89% of revenue. Q4 FY26 guide: $3.65B ±$100M (+40% YoY), gross margin 51–52%. [source: web_research/WDC.json earnings_info, signals_combined.json swing_catalyst_news, run 20260505_203524]
- **CY2026 sold out to AI hyperscalers.** 100% of HDD output committed. Three AI demand drivers: training data, agentic inference, physical AI/robotics. 20% dividend increase. WDC cited >25% CAGR in exabyte growth. [source: web_research/WDC.json ticker_news]
- **ATH $446.62 flipped to support.** Former 6-test resistance broken intraday (high $453.83). Former ATH is now the pullback entry zone ($444–$448). Measured move target $489 (range height ~$42.62 added to $446.62). ADX 67.55 confirmed uptrend; EMA stack fully aligned. [source: signals_combined.json swing_trend_momentum, swing_breakout, run 20260505_203524]
- **Analyst upgrade wave.** Mizuho $470, TD Cowen $500, BofA $572, JP Morgan ~$530; 25-analyst consensus 20 Strong Buy / 1 Moderate Buy / 4 Hold / 0 Sell. Multiple analyst PTs ($470–$572) above current price. [source: web_research/WDC.json analyst_consensus]

## Bear case

- **Hourly OBV bearish divergence — unanimous warning.** All five swing agents flagged hourly OBV trending DOWN while price trended UP. Hourly relative volume 0.46x. Classic institutional distribution signal. This is the primary risk monitoring the trade. [source: signals_combined.json all swing agents, run 20260505_203524]
- **Buy decision not yet confirmed in ledger.** Per trade_ledger.json per_ticker_history[WDC]=[], no fill recorded as of run snapshot. The buy order is a limit at $446; fill is conditional on price pulling back to that level. [source: trade_ledger.json, run 20260505_203524]
- **Valuation stretched.** P/B 30.20, P/E 27.83, P/S 13.99. DCF model produced $0 base/bull case. Priced for AI-demand perfection. [source: signals_combined.json valuation_analyst_agent, fundamentals_analyst_agent, run 20260505_203524]
- **0% win rate on same-setup type.** NVDA EMA pullback Fib dip-buy stopped out Apr 30 (−$63.20). Pattern caution explicit in lessons.md. Confidence held at 44 — not sized up. [source: signals_combined.json swing_head_trader reasoning, run 20260505_203524]
- **Macro risk-off left-tail.** Iran-UAE/Strait of Hormuz escalation ongoing; oil above $102/bbl. Any energy shock would drag high-multiple tech names. [source: web_research/WDC.json macro_context]

## What would change my mind

- **Trade confirmed (bull):** Fill at $446 per ledger → monitor stop $428 and target $489. Exit if hourly OBV divergence worsens materially.
- **Bull-to-neutral:** Q4 FY26 gross margin guidance drops below 50%; hourly OBV divergence resolves to the downside before fill; price fails to hold $440 on any pullback.
- **Bear flip triggers:** CY2027 bookings commentary withdrawn; HDD ASP reversal; hyperscaler shifts nearline to NAND; WDC closes below EMA-50 (~$330) on heavy volume.

## Last updated

2026-05-05 — run 20260505_203524. Prior cluster-block claim falsified (STX is hold this run); prior "ATH $446.62 as resistance" claim partially falsified (price broke through intraday). Sources: decisions.json, explanation.json, signals_combined.json, web_research/WDC.json, trade_ledger.json.
