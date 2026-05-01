---
name: UNH thesis
last_updated: 2026-04-30
last_run_id: 20260430_194522
target_words: 500
stale_after_days: 30
confidence_score: 70
word_count: 498
summary: Prior contrarian recovery thesis falsified by earnings beat and parabolic +41.6% surge — UNH is now an extended momentum leader awaiting a pullback entry, not a beaten-down value play
---

# UNH — Thesis

## TL;DR

**Prior thesis falsified.** The bootstrap thesis described UNH as a "beaten-down healthcare giant down 54% from all-time highs" with a contrarian recovery setup. That framing is now obsolete: Q1 2026 earnings (April 21) crushed estimates ($7.23 adj. EPS vs $6.57 est.) and the stock surged +41.6% in 21 trading days to $370.74. UNH is no longer a recovery play — it is an extended momentum leader at statistical extremes (RSI 94.3, z-score 2.54, ADX 81.64). The correct posture is wait for a pullback to the $348–355 EMA zone before re-entering long. (Source: decisions.json, explanation.json, web_research/UNH.json, run 20260430_194522.)

**What falsified the prior thesis:** The April 21 Q1 2026 earnings beat — adj. EPS $7.23 vs $6.57 consensus, revenue $111.72B vs $109.57B, medical cost ratio improved to 84%, full-year guidance raised to >$18.25 — confirmed the recovery thesis was correct in direction but rendered the "discounted valuation" framing stale. Price is now extended, not discounted. (Source: web_research/UNH.json, run 20260430_194522.)

## Bull case

- **One of the strongest trends in the S&P.** ADX 81.64 is among the highest readings possible; +DI at 49.41 crushes -DI at 2.75. EMA alignment is textbook bullish: 10 EMA ($348) > 21 EMA ($329) > 50 EMA ($311). This is a confirmed institutional trend. (Source: swing_trend_momentum signal, signals_combined.json, run 20260430_194522.)
- **Earnings beat + guidance raise.** Q1 adj. EPS $7.23 (beat by $0.66, +10%); revenue $111.72B (+$2.15B above consensus); 2026 full-year guidance raised to >$18.25. Wall Street responded with multiple PT upgrades: JPMorgan $420, Oppenheimer $405, Argus Buy at $400. (Source: web_research/UNH.json, run 20260430_194522.)
- **Medicare Advantage structural tailwind.** CMS finalized a 2.48% payment rate increase for 2027, directly lifting UNH's largest segment. UNH was the most profitable payer in 2025 ($12.05B net income) and benefits most from the MA rate hike versus Humana and Cigna. (Source: web_research/UNH.json; competitor_activity section, run 20260430_194522.)
- **Pullback entry zone defined.** Trend momentum agent targets a re-entry at 10-EMA (~$348–355) with a $402 Fibonacci 1.272 extension target and $325 stop — 2.3:1 R/R once price corrects. (Source: swing_trend_momentum signal, signals_combined.json, run 20260430_194522.)

## Bear case

- **Statistically extreme overbought.** RSI-14 at 94.3, RSI-7 at 99.52, z-score 2.54, BB pct-b 0.905. Historically, readings at these extremes precede pullbacks. Mean-reversion agent (72% confidence) targets a fade toward $348. (Source: swing_mean_reversion signal, signals_combined.json, run 20260430_194522.)
- **Sub-1:1 risk-reward at current price.** From $370.74: upside to Bollinger upper ($382) = +3%; downside to 10-EMA mean-reversion target ($348) = -6.1%. R/R is 0.5:1 — fails the 2:1 minimum decisively. Three agents independently declined entry. (Source: swing_macro_context signal; decisions.json, run 20260430_194522.)
- **EPS and FCF growth still declining structurally.** Fundamentals agent: earnings growth -35.64%, FCF growth -19.4%. The Q1 adj. EPS beat masks continued GAAP pressures. Current ratio 0.83 — below 1.0. (Source: fundamentals_analyst_agent signal, signals_combined.json, run 20260430_194522.)
- **RICO legal overhang.** New Haven filed RICO allegations against UNH for insulin pricing scheme alongside Cigna and CVS Health. New legal risk layer on top of existing regulatory scrutiny. (Source: web_research/UNH.json, run 20260430_194522.)

## What would change my mind

**Long entry triggers:** A pullback to the 10-EMA zone ($348–355) with the hourly MACD histogram turning positive and volume confirming buyers absorbing the dip. Alternatively, a reversal candle at $348–355 with daily RSI pulling back below 70. Target $402, stop $325 (below 21-EMA). (Source: swing_head_trader signal, decisions.json, run 20260430_194522.)

**Bearish flip:** A daily close below $325 (21-EMA) on elevated volume would confirm the trend has broken. A RICO lawsuit escalation or adverse MA rate reversal would change the fundamental picture.
