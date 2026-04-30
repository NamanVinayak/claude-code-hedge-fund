---
name: PFE trades
last_updated: 2026-04-30
last_run_id: 20260430_203923
target_words: 800
stale_after_days: 60
word_count: 872
summary: Zero trades placed across three model runs; runs 1-2 held at 35% conf (no direction), run 3 holds at 38% conf due to May 5 earnings binary despite confirmed bearish downtrend — post-print short setup is primary watch
---

# PFE — Trades

## TL;DR

PFE has been analyzed twice by the swing model (Apr 11 and Apr 15, 2026) and received a **hold** verdict both times at 35% confidence. No orders were ever placed in Moomoo paper trading. The ticker sits on the watchlist as a monitor-only name until a directional trigger fires.

## Open positions

None. Tracker database confirms zero rows for PFE (`total: 0` from db query run 2026-04-29).

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

**Bull case noted:** Pullback trader saw a clean Fibonacci entry at $26.83 in a technically intact uptrend structure. CEO Albert Bourla buying shares with his own money. Morgan Stanley $28 target.

**Bear case noted:** Momentum ranker 65% bearish — 5-day ROC of -4.9% accelerating downward. Sector rotation agent flagged mild money outflows from pharma. BofA cut target to $26. $21.4B patent cliff is a structural headwind compounding through 2026–2027.

**Why no trade:** Risk/reward of 1.2:1 failed the system's 2:1 minimum. Even with the Fibonacci entry at $26.83 the potential gain to $28 (target) versus risk to $26 (stop) does not meet threshold. Additionally, the head trader judged the agent split as genuinely inconclusive — not a "5 of 9 vs 4 of 9" lean, but a real three-way split with no direction.

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

**Why no trade:** By Apr 15 the model had hardened its view. Eight of nine agents were neutral — even the pullback trader and momentum ranker had converged to neutral rather than holding split opinions. Volume at 0.62x confirmed no institutional interest. With Q1 earnings on May 5 (three weeks out), taking a swing trade at 35% confidence against a binary earnings event was explicitly flagged as a blocker by the model.

**Context:** On this same run the model deployed capital into AMZN (buy), MSFT (buy), BAC (buy), AMD (buy), DIS (buy), and XOM (short) — six trades with confidence levels 55–72%. PFE ranked near the bottom of conviction alongside JNJ and WMT.

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

**Context:** A confirmed bearish downtrend now exists (ADX 25.48, -DI 28.87, $26.68 support broken on 1.71x volume) — a material change from the prior two runs which found no direction. The reason for no trade is solely the May 5 earnings binary, not a lack of signal. Post-earnings, if the downtrend resumes, a short entry on a bounce to $26.68–$26.85 is the primary setup. [Source: 20260430_203923 decisions.json reasoning]

---

## What would trigger an entry

Based on the model's reasoning across both runs, the following conditions would need to be present for PFE to move from hold to an actionable swing trade:

| trigger | direction | threshold cited |
|---|---|---|
| RSI confirmation | Long | RSI moving above 55 with rising ADX |
| Volume conviction | Either | Volume ratio above 1.0x, ideally 1.5x+ on a move |
| ADX strength | Either | ADX sustaining above 25 with directional EMA alignment |
| Earnings clarity | Either | Post-May 5 earnings; avoid binary event risk |
| Price level break | Long | Clean close above $28 (Morgan Stanley target / analyst ceiling) |
| Price level break | Short | Break below $26 (BofA floor); opens toward $24–25 |
| Agent consensus | Either | Require at least 5–6 of 9 agents aligned; current 2/5/2 split is not tradeable |

## Lifetime stats

| metric | value |
|---|---|
| Total runs analyzed | 3 (swing_20260411, 20260415, 20260430_203923) |
| Total trades placed | 0 |
| Total orders in Moomoo | 0 |
| Win rate | N/A |
| Average hold time | N/A |
| Net P&L | $0.00 |
| Entry hit rate | N/A |
| Model confidence range seen | 35%–38% |
| Highest conviction achieved | 38% (run 3) — still below the 40 threshold and well below 55% floor for typical trades |

## Notes for next analyst

1. **May 5 earnings is the next inflection point.** The model explicitly cited "binary earnings risk ahead" on Apr 15. After the print, re-run the swing model — if PFE beats and holds above $28 with volume, the hold-to-long setup may materialize.
2. **The 1.2:1 risk/reward is not close to actionable.** For PFE to get to 2:1 minimum, the stock needs a tighter stop zone (indicating a clearer technical level) or a wider target (indicating a stronger breakout thesis). Neither exists today.
3. **Patent cliff is a slow-burn headwind, not a swing catalyst.** The $21.4B revenue at risk through 2027 is a long-term fundamental concern. It creates a ceiling on bullish price targets and keeps institutional investors cautious, which explains the persistently below-average volume.
4. **Tracker DB is clean.** Zero PFE rows confirmed — no legacy positions, no partial fills, no cancelled orders to reconcile.
