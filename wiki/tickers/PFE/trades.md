---
name: PFE trades
last_updated: 2026-05-01
last_run_id: 20260501_203521
target_words: 800
stale_after_days: 60
word_count: 876
summary: Zero trades placed across four model runs; runs 1-2 held at 35% conf (no direction), run 3 holds at 38% conf, run 4 holds at 45% conf — all blocked by May 5 earnings binary despite confirmed bearish downtrend; post-print short setup remains primary watch
---

# PFE — Trades

## TL;DR

PFE has been analyzed four times by the swing model (Apr 11, Apr 15, Apr 30, and May 1, 2026) and received a **hold** verdict every time. No orders were ever placed in Moomoo paper trading. `per_ticker_history[PFE]` in trade_ledger.json confirms zero rows as of run 20260501_203521. The ticker sits on the watchlist pending the May 5 earnings print — the bearish setup is confirmed and valid; only the earnings binary is blocking execution.

## Open positions

None. `trade_ledger.json per_ticker_history[PFE] = []` — confirmed zero rows as of run 20260501_203521. [Source: 20260501_203521 trade_ledger.json]

## Closed — last 30 days

None.

## Closed — older, rolled by month

None.

## Closed — older than 6 months

None.

## Run-by-run model decisions

### Run: swing_20260411_211655 (Apr 11, 2026)

**Decision: HOLD — 35% confidence**

```
action:        hold
quantity:      0
entry_price:   $26.92 (reference, not triggered)
target_price:  $28.00
stop_loss:     $26.00
risk_reward:   1.2:1
timeframe:     N/A
```

Source: `runs/swing_20260411_211655/decisions.json`

**Head Trader reasoning (verbatim):** "Head Trader neutral at 35% with no consensus direction. RSI at 49.5 dead neutral. BofA at $26 target vs Morgan Stanley at $28 — analysts split. Patent cliff ($21.4B) is a fundamental headwind. No compelling setup."

**Agent split:** 2 bullish, 5 neutral, 2 bearish — no actionable consensus in either direction. (Source: swing_20260411_211655 explanation.json per_ticker.PFE)

**Why no trade:** Risk/reward of 1.2:1 failed the system's 2:1 minimum. Additionally, the head trader judged the agent split as genuinely inconclusive — not a lean, but a real three-way split with no direction.

---

### Run: 20260415_110848 (Apr 15, 2026)

**Decision: HOLD — 35% confidence**

```
action:        hold
quantity:      0
entry_price:   null
target_price:  null
stop_loss:     null
risk_reward:   N/A
timeframe:     N/A — no swing setup
```

Source: `runs/20260415_110848/decisions.json`

**Portfolio Manager reasoning (verbatim):** "8/9 agents neutral. RSI 51, ADX 26, volume 0.62x avg — no momentum in either direction. Binary earnings risk ahead. Medium-term contrarian value but no swing trigger today."

**Why no trade:** Eight of nine agents were neutral — even the pullback trader and momentum ranker had converged to neutral. Volume at 0.62x confirmed no institutional interest. With Q1 earnings on May 5, taking a swing trade at 35% confidence against a binary earnings event was explicitly flagged as a blocker.

**Context:** On this same run the model deployed capital into AMZN, MSFT, BAC, AMD, DIS, and XOM — six trades with confidence levels 55–72%. PFE ranked near the bottom of conviction.

---

### Run: 20260430_203923 (Apr 30, 2026)

**Decision: HOLD — 38% confidence (below 40 threshold; earnings binary blocks entry)**

```
action:        hold
quantity:      0
entry_price:   null
target_price:  null
stop_loss:     null
risk_reward:   N/A
timeframe:     hold — reassess after May 5 earnings
```

Source: `runs/20260430_203923/decisions.json`

**Head Trader reasoning (verbatim):** "Head Trader confidence 38 (<40 threshold). Earnings binary May 5 (4 days). Mean-reversion vs trend bearish conflict unresolved; no setup clears 2:1 R/R with the pre-catalyst risk. Wait for post-earnings directional clarity before initiating any swing position."

**Agent split:** bearish: swing_breakout (42), swing_trend_momentum (55); bullish: swing_mean_reversion (62); neutral: swing_catalyst_news (38), swing_macro_context (30). [Source: 20260430_203923 signals_combined.json]

**Context:** A confirmed bearish downtrend emerged: ADX 25.48, -DI 28.87, $26.68 support broken on 1.71x volume. The reason for no trade was solely the May 5 earnings binary.

---

### Run: 20260501_203521 (May 1, 2026)

**Decision: HOLD — 45% confidence (below 55 execution floor; earnings binary unchanged)**

```
action:        hold
quantity:      0
entry_price:   $26.68 (reference short entry zone, not triggered)
target_price:  $25.68
stop_loss:     $26.95
risk_reward:   3.7:1
timeframe:     8-12 trading days (post May 5 earnings)
confidence:    45
```

Source: `runs/20260501_203521/decisions.json`

**Head Trader reasoning summary:** "Bearish direction clear (4/5 agents), but May 5 earnings binary (4 days) = uncompensated gap risk. Head Trader holds confidence at 45 below execution floor. Wiki confirms zero PFE trades placed across 3 prior runs — earnings veto is consistent. Re-evaluate post-May 5 print: optimal short entry on bounce to $26.65-$26.85 broken-support-now-resistance. R/R 3.7:1 when setup triggers post-earnings." [Source: 20260501_203521 decisions.json]

**Agent split:** bearish: swing_breakout (52), swing_trend_momentum (55), swing_catalyst_news (62), swing_macro_context (42); neutral: swing_mean_reversion (20). 4/5 agents directionally bearish — the most consensus seen across all PFE runs. [Source: 20260501_203521 signals_combined.json]

**What changed vs run 3:** Confidence rose from 38% to 45%. The RSI-7 recovered from extreme oversold (17.19) to 35.81, confirming the anticipated bounce. Price reached $26.70 — pressing directly into the $26.68 broken-support-now-resistance zone (the exact textbook entry the prior run was waiting for). The setup is structurally complete; execution is blocked only by May 5 earnings binary.

**Price target context:** Entry $26.68, target $25.68 (1:1 measured move from breakdown), stop $26.95. R/R 3.7:1 — the best ratio seen in PFE run history. [Source: 20260501_203521 decisions.json]

---

## What would trigger an entry

| trigger | direction | threshold cited |
|---|---|---|
| Post-earnings confirmation | Short | May 5 print passes; downtrend resumes on bounce to $26.65–$26.85 |
| Volume conviction | Short | Volume ratio above 1.5x on the entry candle |
| RSI confirmation | Short | RSI-7 holding below 45 after the bounce; no recovery above 50 |
| Earnings surprise (long) | Long | Beat + raised guidance + GLP-1 pipeline positive; close above $28 on volume |
| Price level break | Long | Clean close above $28 (analyst ceiling); opens toward $29–$30 |
| Earnings confirm bear | Short | Guidance cut + miss; break below $26 opens $24–$25 measured move |

## Lifetime stats

| metric | value |
|---|---|
| Total runs analyzed | 4 (swing_20260411, 20260415, 20260430_203923, 20260501_203521) |
| Total trades placed | 0 |
| Total orders in Moomoo | 0 |
| Win rate | N/A |
| Average hold time | N/A |
| Net P&L | $0.00 |
| Entry hit rate | N/A |
| Model confidence range seen | 35%–45% |
| Highest conviction achieved | 45% (run 4) — still below 55% execution floor; earnings binary is sole blocker |

## Notes for next analyst

1. **May 5 earnings is the next inflection point.** After the print, re-run the swing model. If PFE misses or provides weak guidance, the short entry zone ($26.65–$26.85) is the setup. R/R 3.7:1 is the best seen in this ticker's run history.
2. **The 4/5 bearish agent split is the strongest consensus PFE has ever produced.** Prior runs had 3-way splits or thin majorities. The current setup is directionally clear — only timing is in question.
3. **Correlation note.** Risk manager flags PFE correlation of 0.32 with JNJ (which now has an open short). Adding a PFE short would increase pharma concentration — size defensively or wait for JNJ exit first.
4. **Tracker DB is clean.** `per_ticker_history[PFE] = []` confirmed — no legacy positions, no partial fills, no cancelled orders to reconcile. [Source: 20260501_203521 trade_ledger.json]
