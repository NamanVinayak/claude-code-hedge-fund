---
name: WDC recent
last_updated: 2026-05-07
last_run_id: 20260507_203631
target_words: 200
stale_after_days: 60
word_count: 330
summary: hourly OBV reversed BACK to downtrend (distribution re-emerged near high, reversing prior run's resolved signal); price $483 still ~1.2% from $489 target; hold id 150 to target or stop; no direction flip — HOLD maintained
---

# WDC — Recent Signal History

Append-only. One dated bullet per signal direction flip or key level break.

---

- **2026-05-05 (run 20260505_203524):** Key level break — ATH $446.62 breached intraday (daily high $453.83; daily close $442.36 still below). Former resistance flipped to support zone ($444–$448). Setup type changed from "pre-ATH coiling" (run 20260504_203608) to "post-ATH breakout pullback." Cluster cap resolved: STX assigned hold this run (conf 22, no new position opened), so the STX+WDC combined exposure ($971 simulated) no longer triggers the 30% cap on a $1,618 portfolio. Prior thesis claim that ATH $446.62 was "directly overhead as resistance" is now partially falsified — price traded through it intraday. Buy decision issued: 2 shares limit $446, target $489 (measured move: range height $42.62 added to $446.62), stop $428, R/R 2.39:1, conf 44. All 5 swing agents unanimously flagged hourly OBV bearish divergence (OBV trending down while price trended up on 0.46x relative volume) — key monitoring risk. Fill not yet confirmed in trade_ledger.json per_ticker_history[WDC]. [source: signals_combined.json, decisions.json, trade_ledger.json, run 20260505_203524]

- **2026-05-06 (run 20260506_203627):** Fill confirmed — trade id 150 entered at $448.99 (limit $446, 1.5% tolerance triggered) on 2026-05-06 at 14:29. Prior "fill not confirmed" claim falsified. OBV bearish divergence from prior run fully resolved — hourly OBV now trending UP with price. Price advanced from ~$465 (hourly, May 5) to ~$483 (hourly, May 6), now ~1.2% from $489 measured-move target. Unrealized gain ~7.6%. Decision: hold to target $489 (conf 28); no new entry — R/R from current price 0.65:1 (catastrophic for new entry). Four of five swing agents neutral (no new entry); breakout agent affirms prior thesis directionally correct. Hold existing 2-share position to $489 target or $428 stop. [source: trade_ledger.json per_ticker_history[WDC] id 150, signals_combined.json, decisions.json, run 20260506_203627]

- **2026-05-07 (run 20260507_203631):** Key level monitoring — hourly OBV reversed back to downtrend (distribution re-emerged near the high), reversing the "OBV resolved" signal from run 20260506_203627. Hourly MACD histogram -1.92 (negative); hourly volume bias 10d = DOWN; hourly ROC 5d -0.77%, 10d -1.13% — all negative on hourly frame. Hourly ADX only 24.95 (below 25 threshold — hourly trend weakening). Daily trend intact (ADX 67.1, RSI-14 89.57). Price held ~$483 — no advance toward $489 this run. No signal direction flip (HOLD maintained, conf 15); no new entry (R/R ~0.11:1 from $483). Existing position id 150 ($448.99 fill, $489 target, $428 stop) holds. Watch: if price stalls at $483–$486 without reaching $489 within 1-2 trading days, hourly distribution could accelerate toward stop. [source: signals_combined.json swing_trend_momentum, swing_head_trader, trade_ledger.json, run 20260507_203631]
