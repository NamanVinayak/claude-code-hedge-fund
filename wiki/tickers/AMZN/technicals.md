---
name: AMZN technicals
last_updated: 2026-05-06
last_run_id: 20260506_173925
target_words: 350
stale_after_days: 7
word_count: 348
summary: HOLD — no valid entry; price $273.55 daily close / $278.56 intraday wick (unconfirmed); RSI-14 82.32/RSI-21 90.24 deeply overbought; ADX 64.96 extreme mature uptrend; EMA alignment clean bullish; $276 intraday wick did NOT close above — unconfirmed; 4/5 agents neutral, 1 bullish conditional; wait for 10 EMA pullback to $263–$266 or confirmed breakout above $276 on 1.5x+ volume
---

# AMZN — Technicals

## TL;DR

As of run 20260506_173925 (May 6, 2026), price closed at $273.55; intraday high $278.56 was an **unconfirmed wick** — price failed to close above the $276 breakout trigger level. RSI-14 82.32, RSI-21 90.24 — deeply overbought. ADX 64.96 with +DI 36.89 vs -DI 10.95 — extreme bullish trend intact. Setup type: **HOLD — no valid entry from current levels.** 4/5 swing agents returned neutral; 1 bullish (conditional only at $264 pullback). No short without hourly RSI-21 >75 + volume-confirmed rejection at $273-276. No long without pullback to 10 EMA zone $263-266 OR confirmed daily close above $276 on 1.5x+ volume (volume today 0.80x — well below 1.5x gate).

*Prior setup (run 20260505_173521): HOLD — same regime. 10 EMA moved from $261.20 → $263.44 (rising). Intraday wick to $278.56 is new information but does not change the setup type.*

---

## Multi-timeframe state

**Daily (primary):** EMA alignment clean bullish — 10 EMA $263.44 > 21 EMA $252.19 > 50 EMA $237.23. ADX 64.96 with +DI 36.89 vs -DI 10.95 — extreme trend strength. RSI-14 82.32, RSI-21 90.24 (deeply overbought). Z-score vs 50-SMA: 1.99 (just below +2.0). Price 20.3% above 50-SMA. BB upper band ~$279.90; Bollinger %B 0.88 (near upper band). MACD histogram positive at +1.10. Volume 0.80x 20-day average — below threshold.

**Hourly:** Hourly RSI-21 at 64.43 — elevated but NOT at extreme fade threshold (>75 needed). Hourly relative volume 0.06x — extremely thin, near zero. 10 EMA zone $263-266 is nearest valid pullback support. [source: signals_combined.json swing_trend_momentum and swing_macro_context, run 20260506_173925]

---

## Key levels

| Level | Value | Source |
|---|---|---|
| Current price | $273.55 (close) / $278.56 (intraday wick) | Run 20260506_173925 |
| Breakout trigger | Daily close above $276 on 1.5x+ volume | swing_breakout, run 20260506_173925 |
| Breakout long entry | ~$276.50 (if confirmed) | swing_breakout, run 20260506_173925 |
| Long pullback entry zone | $263–$266 (10 EMA zone) | swing_trend_momentum, run 20260506_173925 |
| EMA-based pullback entry | ~$264 (trend_momentum) / ~$267.50 (macro_context) | signals_combined.json, run 20260506_173925 |
| Fib extension (1.272) | $284.20 (pullback target) | swing_trend_momentum, run 20260506_173925 |
| Breakout measured move | $296 (range height $21 added to $276) | swing_breakout, run 20260506_173925 |
| Short re-entry trigger | Hourly RSI-21 >75 + vol rejection at $273–$276 | decisions.json, run 20260506_173925 |
| Stop for any pullback long | $259.50 | swing_trend_momentum, run 20260506_173925 |

---

## Setup type

**HOLD — no valid entry.** Three potential entry scenarios defined; none active. (A) BREAKOUT LONG — requires confirmed daily close above $276 on 1.5x+ volume; today closed at $273.55 with 0.80x volume (intraday wick to $278.56 explicitly unconfirmed per swing_breakout). (B) PULLBACK LONG — requires retracement to 10 EMA zone $263-266 with RSI cooling below 65; price is 3.84% above 10 EMA. (C) SHORT — requires hourly RSI-21 >75 plus volume-confirmed rejection candle at $273-276; current hourly RSI-21 only 64.43 with 0.06x relative volume. ADX 64.96 extreme trend strength — prior short (ID 115) stopped at $276; elevated confirmation bar enforced. [source: decisions.json, signals_combined.json swing_head_trader, run 20260506_173925]

---

## Indicator snapshot (May 6, 2026)

| Indicator | Value | Interpretation |
|---|---|---|
| ADX | 64.96 | Extreme mature uptrend — fade risk high |
| +DI / -DI | 36.89 / 10.95 | Bull momentum dominant |
| RSI-14 | 82.32 | Deeply overbought |
| RSI-21 | 90.24 | Extremely overbought |
| Hourly RSI-21 | 64.43 | Elevated but below fade threshold (75) |
| Hourly rel-vol | 0.06x | Near-zero — extremely thin |
| Z-score (50-SMA) | 1.99 | Near +2σ — statistically stretched |
| % above 50-SMA | 20.3% | Extreme extension |
| BB %B (daily) | 0.88 | Near upper band ($279.90) |
| Volume (daily) | 0.80x avg | Below 1.5x breakout threshold |
