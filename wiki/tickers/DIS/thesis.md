---
name: DIS thesis
last_updated: 2026-05-07
last_run_id: 20260507_220640
target_words: 500
stale_after_days: 30
word_count: 497
summary: Short decision issued — 3 shares at $108.50, target $103, stop $110.60, R/R 2.62:1 (conf 35); prior thesis "wait for pullback to $105-107 for fresh long" falsified by dual Z-score extreme and unanimous entry-price warning from all 4 bullish agents; short thesis: post-earnings gap statistically overextended (daily 2.05, hourly 2.12 Z-score), OBV distribution on 2.72x volume, all bullish agents' preferred entry zone of $103-104 aligns with fade target
---

# DIS — Thesis

## TL;DR

⚠️ Recent trade: stop_hit 2026-05-05, -$4.99. Thesis under review.

**Prior thesis falsified (run `20260506_220627`):** The May 6 thesis stated "wait for pullback to $105–107 consolidation zone for fresh long with acceptable R/R" — the pre-stated bull restart trigger (gap above $104.83 on 1.5x+ vol) fired on May 6. [source: `signals_combined.json swing_breakout`, `web_research/DIS.json`, run `20260506_220627`]

**Falsification trigger for this rewrite:** The "wait for pullback to long" thesis was not acted on because: (1) no pullback to $105-107 occurred — price remained above $108; (2) all 4 bullish agents unanimously agree that $108 is the wrong entry for a long — their preferred entry of $103-104 is exactly where the mean-reversion short is targeting. The dual Z-score extreme (daily 2.05, hourly 2.12 simultaneously) triggered a short decision instead of waiting for a long entry. [source: `signals_combined.json swing_mean_reversion`, `swing_head_trader`, `decisions.json`, run `20260507_220640`]

**New thesis:** Post-earnings gap fade short. Entry $108.50, target $103.00 (Bollinger midline/20-SMA), stop $110.60, R/R 2.62:1, confidence 35%. 3 shares ($325.50), 0.5% account risk. [source: `decisions.json DIS`, run `20260507_220640`]

---

## Bull case

**Q2 FY2026 beat is genuine.** EPS $1.57 vs $1.49 estimate (+5.4% beat); revenue $25.17B vs $24.84B estimate; streaming income +88% to $582M; CEO D'Amaro raised FY2026 EPS growth guidance to ~12% and share buybacks to $8B+. [source: `web_research/DIS.json`, run `20260507_220640`]

**Strong trend structure.** ADX 33.39 with +DI 37.60 > -DI 23.85 — confirmed uptrend on daily. Daily MACD bullish crossover. Hourly EMAs all aligned up. ROC-21d: +12.82%. [source: `signals_combined.json swing_trend_momentum`, run `20260507_220640`]

**Mandalorian catalyst pipeline intact.** Mandalorian and Grogu theatrical release May 22 (~11 trading days). Analyst consensus Buy with avg PT $132 — ~18-22% upside from current price. [source: `web_research/DIS.json`, run `20260507_220640`]

---

## Bear case (active thesis)

**Dual Z-score extreme — rare overextension signal.** Daily Z-score 2.05 and hourly Z-score 2.12 are simultaneously above the 2.0 threshold — a "dual-timeframe extreme" that is the strongest Branch A mean-reversion trigger per strategy rules. [source: `signals_combined.json swing_mean_reversion`, run `20260507_220640`]

**Bollinger pct_b 1.06 — price above upper band.** The daily close is statistically outside normal boundaries. Distance from 50-SMA: +7.14%. Post-earnings gaps of this magnitude commonly retrace 40-60% within 5-10 trading days. [source: `signals_combined.json swing_mean_reversion`, run `20260507_220640`]

**OBV bearish divergence on high volume.** On-balance volume trended DOWN even as price spiked on 2.72x average volume on May 6 — a distribution signal suggesting informed sellers are unloading into the gap. [source: `signals_combined.json swing_mean_reversion`, `swing_breakout`, run `20260507_220640`]

**Unanimous bullish agents warn against $108 entry.** All 4 bullish agents explicitly stated $108 is a poor entry — they all target $103-104 for a long. This convergence on the short-target zone provides an unusual cross-directional confirmation for the fade. [source: `signals_combined.json swing_head_trader`, run `20260507_220640`]

---

## What would change the thesis

**Short exit (stop):** Close or sustained price above $110.60 — stops the short. Indicates the gap continuation thesis is winning.

**Short target (take profit):** Price reaching $103.00 (Bollinger midline). At this level, the long case at $103-104 becomes the primary watch scenario.

**Long reset (post-fade entry):** If price pulls back to $103-104 on declining volume (not distribution), re-evaluate fresh long with stop $100.42, target $110.48, R/R ~3:1. This is the scenario all 4 bullish agents preferred.

**Thesis flip back to bull:** Two consecutive daily closes above $109.14 resistance on 1.5x+ volume — would confirm momentum continuation over mean reversion.
