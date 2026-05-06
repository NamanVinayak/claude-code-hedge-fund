---
name: GOOG recent
last_updated: 2026-05-06
last_run_id: 20260506_164526
target_words: 300
stale_after_days: 60
word_count: 354
summary: Signal history — direction flips and key level breaks for GOOG across swing runs
---

# GOOG — Recent Signal History

Append-only. One dated bullet per significant direction flip or key level break.

---

- **2026-05-01** (run 20260501_164617) — **Key level break + setup transition.** Prior technicals page tracked breakout entry zone $327–332 with targets $342–355 and stop $318–321. On April 30, GOOG gapped +10% to $381.94 on 2.6x volume (44.5M vs 17.1M avg), driven by Q1 2026 earnings blowout (EPS $5.11 vs $2.62, revenue $109.9B, Google Cloud +63% YoY). All prior targets exceeded in a single session. Prior setup type "confirmed breakout entry — chase $330.58" is retired. New setup type: "post-earnings extension — no-chase zone." Price is 10.1% above EMA10 ($346.87), RSI-7 at 97.75 (extreme), Z-score 3.29 vs 50-SMA. Decision: HOLD (conf 45) — R/R 0.79:1 fails 2:1 minimum. Three agents converge on $342–$358 as the re-entry zone for 3:1+ R/R. Signal direction: shifted from "entry-active long" to "wait-for-pullback neutral." No position open. Next trigger: price returning to $353–$358 with a confirmed daily candle.

- **2026-05-05** (run 20260505_164543) — **Signal direction flip: neutral → short decision issued.** Price $383.51 (+$0.29 from prior run $383.22 on May 4) — four sessions of going essentially nowhere after the Apr 30 gap-up. PM issued a short: 1 share at $383, target $338.95 (20-SMA), stop $389.50, R/R 4.32:1, conf 40%. Mean-reversion Branch A trigger: RSI-7 90.69, Z-score 2.56 vs 50-SMA, Bollinger %B 0.963, hourly resistance $384.16 (13 tests). Prior "watch-not-act neutral" stance from May 1–May 4 ended — 4 days of price stall at hourly resistance with easing RSI extremes (from 97.47 to 90.69) without a breakout confirms the ceiling thesis. Hourly RSI-21 normalized (54.93 from 79.28), OBV divergence resolved. ADX increased to 71.68 — trend strength intensified but no new upside. No fill confirmed in trade_ledger.json per_ticker_history[GOOG]=[] as of this run. (Source: decisions.json, trade_ledger.json, swing_mean_reversion, swing_head_trader, run 20260505_164543)

- **2026-05-06** (run 20260506_164526) — **Short stopped out — signal direction flip: short → neutral/hold.** Prior short (id 149, entry $383, stop $389.50) stopped out at $389.50, realized P&L −$6.50. Price continued to $395.11 hourly — the mean-reversion ceiling thesis ($384.16 hourly resistance, 16 tests) was broken to the upside. ADX intensified to 74.23 (+DI 42.98 vs −DI 3.72); RSI-7 remained extreme at 90.7. The prior bear-invalidation clause ("price breaks cleanly above $389.50 stop") was triggered. PM issued Hold (conf 28) — no new entry in either direction at current overextended levels. Three agents stand aside (no volume for breakout, catalyst window not yet open, R/R fails 2:1 minimum at $395). Revisit: $375–$385 pullback zone or May 14–15 I/O pre-positioning window. (Source: trade_ledger.json per_ticker_history[GOOG] id 149, decisions.json, swing_head_trader, run 20260506_164526)
