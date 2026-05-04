---
name: GS thesis
last_updated: 2026-05-04
last_run_id: 20260504_192106
target_words: 500
stale_after_days: 30
word_count: 498
summary: Iran escalation directly targets GS revenue drivers (M&A, IPO, FICC) — prior "partial stabilization" claim from May 1 falsified; price dropped $18 to $905.10; $924.23 confirmed as overhead resistance; model issues 5th consecutive HOLD; zero GS trades in ledger
---

## TL;DR

**Prior thesis falsification (run `20260504_192106`):** The May 1 thesis (last_run_id `20260501_190923`) described "post-breakdown partial recovery — unresolved direction" with an hourly RSI bullish divergence suggesting potential stabilization at $923.77. That stabilization claim is falsified: GS dropped from $923.77 to $905.10 by May 4, the $924.23 broken support has now been tested as resistance and rejected, and the Iran escalation on May 4 creates a sector-specific headwind directly targeting GS's core revenue drivers. The model issued a fifth consecutive HOLD (confidence 30%). Zero GS trades exist in the ledger. [run `20260504_192106`]

---

## Prior Thesis Claim Falsified

**Falsified claim (run `20260501_190923`):** "Hourly RSI bullish divergence confirmed — first recovery signals post-breakdown. Partial stabilization after sell-the-news breakdown."

**What falsified it (run `20260504_192106`):** Price dropped $18.67 from $923.77 to $905.10. The hourly RSI divergence did not produce a recovery — price made lower lows. $924.23 (29-test former support, now resistance) held as ceiling during the partial recovery and has rejected price. [signals_combined.json, swing_trend_momentum, run `20260504_192106`]

---

## Bull Case

**Structural daily trend still intact.** ADX 34.03 (strong, above 25 threshold). Daily EMA fully aligned bullish: EMA-10 $920.84 > EMA-21 $907.08 > EMA-50 $888.81. Plus DI (30.62) > Minus DI (12.32) on the daily — uptrend confirmed by daily directionality. GS has not broken below EMA-21 ($907.08). [signals_combined.json, run `20260504_192106`]

**Strong earnings franchise.** Q1 2026: EPS $17.55 beat $16.37 estimate (+24.3% YoY), revenue $17.2B (+14.4% YoY). Equities trading all-time Wall Street record: $5.33B. GS leads North America M&A by value ($267B Q1 2026). HSBC raised PT from $729 to $765 on May 4. Anthropic/Blackstone AI joint venture partnership ($1.5B) adds institutional AI revenue stream. [web_research/GS.json, run `20260504_192106`]

**Hourly RSI bullish divergence still visible.** swing_mean_reversion (bullish, 45 conf) sees confirmed hourly RSI divergence (price lower lows, RSI higher lows) and volume-confirmed support at $899.16 (8 tests). R/R from $905 entry to $933.48 target with $896 stop = 3.5:1 — passes 3:1 threshold. [signals_combined.json, swing_mean_reversion]

---

## Bear Case

**Iran escalation is directly negative for GS's revenue model.** Risk-off suppresses M&A deal flow, IPO activity, and FICC trading revenue — GS's three core profit drivers. The macro_context agent applies a sector-specific veto on this basis; this is not general risk-off but a targeted structural headwind. [signals_combined.json, swing_macro_context; web_research/GS.json]

**Extreme insider distribution.** 3.3:1 sell ratio: ~$109.9M in insider sales, zero purchases over trailing 3 months. Highest sell ratio in the current run universe. No new Form 4 filings in run `20260504_192106`. [signals_combined.json, swing_catalyst_news]

**$924.23 confirmed overhead resistance.** Former hourly support (29 tests) broke April 29 and has since rejected recovery attempts. Hourly ADX 26.7 with minus DI (28.24) > plus DI (18.74) — confirmed hourly downtrend. Daily MACD histogram -1.42, deeply negative; 5d ROC -0.35%, 10d ROC -0.24%. [signals_combined.json, swing_trend_momentum]

**Active bearish analyst background thesis.** swing_catalyst_news carries a live in-progress bearish thesis from run `20260430_190826` (bearish entry $925.48, target $864.45, confidence 68, MFE 2.21%) — a new long would directly conflict with this active thesis on the same ticker. [signals_combined.json, swing_catalyst_news]

---

## What Would Change the Thesis

**Bull entry trigger:** Daily close above $924.23 on volume ≥ 1.5x average AND daily RSI-7 > 50 AND hourly MACD histogram positive. These three conditions must fire simultaneously. [signals_combined.json, wiki policy]

**Bear confirmation / exit trigger:** Sustained close below EMA-21 ($907.08) or volume-accelerated break below $899.16 support (8-test floor). If $899.16 breaks, Branch B thesis entirely invalidates.

---

## Model Verdict History

| Run | Date | Signal | Confidence | Action |
|---|---|---|---|---|
| `swing_20260411_211655` | Apr 11 | HT bullish (7/9) | 63% | Pre-earnings candidate — not entered |
| `20260415_110848` | Apr 15 | HT neutral | 48% | Hold — ADX 19.4 |
| `20260417_233350` | Apr 17 | PM hold | 62% | Hold — ADX 20.66, R/R 1.43:1 |
| `20260430_190826` | Apr 30 | HT neutral | 38% | Hold — FICC miss, insider sell, broken support |
| `20260504_192106` | May 4 | HT neutral | 30% | Hold — Iran escalation, price drop to $905, 5th consecutive hold |
