---
name: WMT technicals
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 350
stale_after_days: 7
word_count: 371
summary: ADX below 25, failed breakout at $129, hourly EMAs in downtrend — no swing setup on either April run.
---

# WMT — Technicals

## TL;DR

Both April runs reached the same conclusion: WMT has no tradeable swing setup. The stock failed to break $129 resistance, ADX is too weak to confirm any trend (17-18 on both dates), and the hourly EMA structure is bearish. The model needs a clean high-volume close above $129 before any entry is warranted.

## Multi-timeframe state

| Timeframe | Signal | Notes |
|---|---|---|
| Daily trend | No trend | ADX 17-18, well below 25 threshold — choppy, non-directional [decisions both runs] |
| Daily EMAs | Mixed | Failed breakout at $129.13 resistance; price pulled back toward $124-$127 zone |
| Hourly EMAs | Bearish | Downtrend on hourly chart as of Apr 15 run [decisions 20260415_110848] |
| Hourly momentum | Negative | Head Trader noted negative hourly momentum on Apr 15; no reversal signal |
| Risk-reward | Unacceptable | Apr 11 run: R:R 0.9:1 (entry $126.77, target $131, stop $122) — fails the 2:1 minimum |

## Key levels

| Level | Value | Source |
|---|---|---|
| Resistance (prior breakout attempt) | $129.00–$129.13 | Apr 11 + Apr 15 decisions |
| Entry zone (bull setup trigger) | Close above $129 on 1.5x+ volume | Apr 15 decision reasoning |
| Support / stop zone | ~$122.00 | Apr 11 implied stop level |
| Price on Apr 11 run | $126.77 | decisions swing_20260411 |
| Price on Apr 15 run | ~$124.56 (Yahoo Finance cited) | web_research 2026-04-15 |

## Setup type

**No setup — wait mode.** The stock is in a failed-breakout pattern: it tested $129 resistance and rejected, with insufficient trend strength (ADX < 25) to support a directional trade. This is a textbook "no-man's-land" condition. The Squeeze Momentum indicator likely shows compression without a confirmed directional break.

The system's rule is clear: do not swing-trade when ADX < 25. [decisions 20260415_110848, reasoning: "ADX 18 below 25 threshold"]

## When to revisit

Re-evaluate after:
1. A daily close above $129 on 1.5x average volume — potential breakout long
2. A daily close below $122 on elevated volume — potential breakdown short
3. May 21, 2026 Q1 FY2027 earnings — binary event that could resolve the squeeze

## Last updated

Bootstrap — sourced from runs `20260415_110848` (Apr 15) and `swing_20260411_211655` (Apr 11). Technicals are stale after 7 days; re-run the swing pipeline before using these levels.
