---
name: WMT thesis
last_updated: 2026-05-01
last_run_id: 20260501_212730
target_words: 500
stale_after_days: 30
word_count: 498
summary: Daily close at $131.93 confirmed above $128.49 and $129 resistance (falsifying the prior "daily not confirmed" claim), but daily ADX deteriorated to 11.4 — price trigger met, ADX gate not met; still hold; wait for pullback to $128-129 for valid entry.
---

## TL;DR

**What falsified the prior thesis:** The April 30 thesis stated "the daily close at $128.01 has not confirmed above $128.49 resistance" as its central bear-case claim. That is now factually stale: the April 30 session closed at $131.93 on the daily bar — fully confirming price above both the $128.49 and $129-$130 resistance levels the prior thesis identified as the bull trigger. The price condition of the watch trigger has been met. However, the second gate — daily ADX inflecting above 20 — has not been met; ADX actually deteriorated from 12.89 to 11.4, its weakest reading in any WMT analysis run. Volume on the Apr 30 surge was 1.19x vs. the required ≥1.5x. The signal direction remains neutral. Decision: HOLD — wait for pullback to $128-$129 zone. (Source: run `20260501_212730/signals_combined.json`, swing_breakout, swing_head_trader)

---

## Bull Case

**Price breakout above multi-test resistance confirmed.** The daily close at $131.93 cleared both the $128.49 consolidation ceiling (23-test resistance) and the $129 bull trigger level identified by three prior runs. Hourly ADX at 35.96 with +DI (33.15) > -DI (15.94) shows strong intraday bullish trend. Daily EMA stack fully aligned uptrend (EMA-10 128.83 > EMA-21 127.58 > EMA-50 125.40). (Source: `20260501_212730/signals_combined.json`, swing_breakout, swing_trend_momentum)

**Pre-earnings catalyst window is active.** Q1 FY2027 earnings due May 14 (9 trading days away). Morgan Stanley $140 PT (Overweight). Consensus 28 Buy / 2 Hold / 0 Sell, avg PT $137.79. FY2026 revenue +4.73%, earnings +12.64%, US e-commerce +27% YoY — first-ever profitable global e-commerce quarter. Quarterly dividend ex-date May 8 ($0.248/share). (Source: `20260501_212730/web_research/WMT.json`, swing_catalyst_news)

**Structural consumer trade-down tailwind.** In a tariff environment with US-China 145% tariffs, consumer spending migrates to Walmart's everyday-low-price model. Beauty expansion (425 stores), $350M domestic milk facility, Great Value private-label redesign all support margin improvement. (Source: `20260501_212730/web_research/WMT.json`)

---

## Bear Case

**ADX deterioration is the central concern.** Daily ADX fell from 12.89 (Apr 30 run) to 11.4 (May 1 run) — the trend strength gate has not only remained open, it has worsened. The prior thesis explicitly set ADX > 20 as a hard requirement for any directional trade. At 11.4, the stock is drifting without a legitimate trend despite bullish EMA structure. (Source: `20260501_212730/signals_combined.json`, swing_trend_momentum, swing_breakout)

**Price statistically extended.** Daily Z-score vs 50-SMA is 2.31 — above the +2.0 statistical overbought threshold. Bollinger %B at 0.947 places price pressing the upper band ($132.46). Hourly bearish RSI divergence confirmed (price new high, hourly RSI diverging down). Hourly OBV trending down. Current R/R at $131.93 entry: bull 0.84:1, short 1.47:1 — both fail the 2:1 minimum. (Source: `20260501_212730/signals_combined.json`, swing_mean_reversion)

**Insider distribution and stretched valuation.** Walton family sold $4.6B cumulatively — founding family treating current price as a distribution opportunity. DCF fair value $177B vs. market cap $1.05T — 83% premium. P/E 48.21x on ~5% revenue growth. (Source: `20260501_212730/signals_combined.json`, valuation_analyst_agent, swing_catalyst_news)

---

## What Would Change the Thesis

**Turn bullish (long entry):** Pullback to $128.50-$129.00 zone (former resistance now support) while maintaining daily EMA uptrend AND daily ADX inflecting above 20. From $128.50, entry $128.50, target $134.41, stop $126.00 = R/R 2.36:1 — meets minimum. Alternatively, daily close above $132.46 on ≥1.5x volume with ADX rising would confirm the breakout directly.

**Turn bearish (short):** Confirmed daily close below $125.91 support on elevated volume, or Q1 FY2027 earnings miss on May 14, or tariff cost surprise compressing gross margin below expectations.
