---
name: AMZN technicals
last_updated: 2026-05-05
last_run_id: 20260505_173521
target_words: 350
stale_after_days: 7
word_count: 347
summary: HOLD — no valid entry; price $272.05–$273.49; RSI-14 80.49/RSI-21 90.43 deeply overbought; ADX 65.1 extreme mature uptrend; EMA alignment clean bullish; $276 resistance not decisively broken; all 5 agents neutral; wait for 10 EMA pullback to $258–$265 or confirmed breakout above $276 on 1.5x+ volume
---

# AMZN — Technicals

## TL;DR

As of run 20260505_173521 (May 5, 2026), price closed at $272.05 (current $273.49). RSI-14 80.49, RSI-21 90.43 — deeply overbought. ADX 65.1 with +DI 35.65 vs -DI 11.3 — extreme bullish trend, bulls absorbed the $268-276 distribution zone (prior short ID 115 stopped out May 4 at $276). Setup type: **HOLD — no valid entry from current levels.** All 5 swing agents returned neutral. No short without hourly RSI-21 >75 + volume-confirmed rejection at $273-276. No long without pullback to 10 EMA zone $258-265.

*Prior setup (run 20260504_173321): HOLD after stop-out of short from 20260501_173921 at $276 (-$10.14). Technicals stale 1 day.*

---

## Multi-timeframe state

**Daily (primary):** EMA alignment clean bullish — 10 EMA $261.20 > 21 EMA $250.05 > 50 EMA $235.75. ADX 65.1 with +DI 35.65 vs -DI 11.3 — extreme trend strength. RSI-14 80.49, RSI-21 90.43 (deeply overbought). Z-score vs 50-SMA: 2.06. Price 20.36% above 50-SMA. BB upper band ~$280.53; Bollinger %B 0.86 (near upper band). MACD histogram positive at +1.17.

**Hourly:** Hourly RSI-21 at 67.45 — elevated but NOT at extreme fade threshold (>75 needed). Hourly relative volume 0.04x — near zero, very thin trading activity. 10 EMA zone $261-265 is the nearest valid pullback support. [source: signals_combined.json swing_trend_momentum and swing_macro_context, run 20260505_173521]

---

## Key levels

| Level | Value | Source |
|---|---|---|
| Current price | ~$272.05–$273.49 | Run 20260505_173521 |
| Resistance zone | $273–$276 | April 30 swing high; prior stop stop-out level |
| Short re-entry trigger | Hourly RSI-21 >75 + vol rejection at $273–$276 | decisions.json, run 20260505_173521 |
| Breakout long trigger | Daily close above $276 on volume 1.5x+ | swing_breakout, run 20260505_173521 |
| Long pullback entry zone | $258–$265 (10 EMA zone) | swing_trend_momentum, run 20260505_173521 |
| Short dip-buy zone | $257.94 (Fib 23.6%) | swing_mean_reversion, run 20260505_173521 |
| Fib extension (1.272) | $284.65 (breakout target) | swing_macro_context, run 20260505_173521 |
| Breakout measured move | $296 (if $276 clears on volume) | swing_breakout, run 20260505_173521 |
| Stop for any short entry | $277 (above resistance) | decisions.json, run 20260505_173521 |

---

## Setup type

**HOLD — no valid entry.** Three potential entry scenarios defined but none active today: (A) SHORT — requires hourly RSI-21 >75 plus volume-confirmed rejection candle at $273-276; current hourly RSI-21 only 67.45 and hourly relative volume near zero (0.04x). (B) BREAKOUT LONG — requires confirmed daily close above $276 on 1.5x+ volume; no such close confirmed. (C) PULLBACK LONG — requires retracement to 10 EMA zone $258-265 with RSI cooling below 65; price is 4.15% above 10 EMA. ADX 65.1 is extreme trend strength — fading without confirmation is disqualified. [source: decisions.json, signals_combined.json swing_head_trader, run 20260505_173521]

---

## Indicator snapshot (May 5, 2026)

| Indicator | Value | Interpretation |
|---|---|---|
| ADX | 65.1 | Extreme mature uptrend — fade risk |
| +DI / -DI | 35.65 / 11.3 | Bull momentum dominant |
| RSI-14 | 80.49 | Deeply overbought |
| RSI-21 | 90.43 | Extremely overbought |
| Hourly RSI-21 | 67.45 | Elevated but below fade threshold |
| Hourly rel-vol | 0.04x | Near-zero — very thin |
| Z-score (50-SMA) | 2.06 | At +2σ — statistically stretched |
| % above 50-SMA | 20.36% | Extreme extension |
| BB %B (daily) | 0.86 | Near upper band |
| ATR-14 | ~2.66% daily | High volatility — wide stops needed |
