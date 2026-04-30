---
name: JNJ recent
last_updated: 2026-04-30
last_run_id: 20260430_194522
target_words: 300
stale_after_days: 30
word_count: 158
summary: Signal history — direction flips and key level breaks for JNJ across swing runs
---

# JNJ — Recent Signal History

## TL;DR

Append-only log of direction flips and key level breaks. Only material changes are recorded.

---

- **2026-04-11** — swing_20260411_211655: HOLD (conf 35%). Squeeze building (BB width 0.048), ADX 22.9 (below threshold), z-score -0.36, RSI 56.9. Earnings binary (April 14) blocked entry. Proposed but unexecuted: $238.46 entry, target $245, stop $234, R/R 1.5:1 (failed 2:1 minimum). (Source: swing_head_trader.json, run swing_20260411_211655.)

- **2026-04-15** — 20260415_110848: HOLD (conf 42%). Post-earnings squeeze still unresolved. ADX 23 (below 25), SuperTrend bearish, EMAs flat (EMA10 $240.08 vs EMA21 $240.21). 8/9 agents neutral. Bullish trigger: $244 close on 1.5x volume. Bearish trigger: $233 close. (Source: decisions.json, run 20260415_110848.)

- **2026-04-30** — 20260430_194522: SHORT (conf 42%). **Direction flip: hold → short.** Squeeze resolved bearish — the Apr 15 bearish trigger ($233 close) was surpassed; price at $227.35. ADX 29.46 broke above 25 threshold; EMA alignment fully bearish (-DI 33.25 > +DI 15.99); MACD -3.45. Short entry $229.50 (bounce into 10-EMA resistance), target $216.53 (measured move), stop $235. R/R 2.36:1. Risk manager allows ~4 shares ($918 notional). (Source: decisions.json, swing_head_trader signal, run 20260430_194522.)
