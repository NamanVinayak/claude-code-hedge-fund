---
name: NVDA recent
last_updated: 2026-05-01
last_run_id: 20260501_124529
target_words: 300
stale_after_days: 30
word_count: 265
summary: Signal history — direction flips and key level breaks for NVDA across swing runs
---

# NVDA — Recent Signal History

## TL;DR

Append-log of material direction changes and key level breaks. Only entries where signal direction flipped or a key level broke are recorded here.

---

- **[2026-04-30] run 20260430_060402 | signal flip: HOLD → BUY (new entry)** — Prior setup (hold 6 shares at $197.20 cost basis, no new entry above $211 no-chase zone) superseded by fresh 67-share BUY at $209.25. Prior setup closed when all 4 paper trades were abandoned 2026-04-29. Signal flip triggered by: (1) prior position cleared, enabling new entry; (2) price pulled back from $216.83 high to Fib 38.2% at $209.70 — the entry zone the model has been waiting for since Apr 27 run. 4/5 swing agents bullish (swing_breakout neutral, not bearish). ADX upgraded from 49.47 → 54.67. Stop $205.30, target $222.50, R/R 3.35:1. (run 20260430_060402, PM decisions.json)

- **[2026-04-29] run sanity_20260429_031705 | prior technicals setup** — Setup type: HOLD existing position (6 shares at $197.20), no new entry. Price $213.17 (above $211 no-chase zone). ADX 49.47, RSI-14 81.67, z-score 2.39 — deeply extended. Hourly SuperTrend bearish. Constructive pullback zone identified at $204–$208. This setup has now been superseded by the 2026-04-30 pullback entry.

- **[2026-05-01] run 20260501_124529 | signal flip: BUY → HOLD (all positions stopped out) + key level break: $208.20** — Both open NVDA long positions were stopped out at $205.30 on 2026-04-30: Position 1 (67 shares at $209.25, run 20260430_060402, -$264.65 realized) and Position 2 (3 shares at $209.50, run 20260430_124724, stop also hit). Price continued lower to $199.57 — a breach of the $208.20 hard invalidation level on 1.52x average volume. Signal flipped BUY → HOLD (conf 35). Head trader declines new long entry: same EMA-pullback Fib dip-buy setup is 0% win rate last 30 days; hourly -DI 38.45 >> +DI 11.92; MACD histogram -1.95; no confirmation candle. Conditional re-entry zone defined at $197.50–$199.50 with stop $194.00, target $212.25, R/R 2.67:1 — awaits hourly reversal candle AND MACD histogram turning positive. Prior "EMA pullback Fib dip-buy" setup type is now logged as failed. (run 20260501_124529, swing_head_trader, decisions.json, signals_combined.json portfolio)
