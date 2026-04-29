---
name: WMT trades
last_updated: 2026-04-29
last_run_id: bootstrap
target_words: 800
stale_after_days: 60
word_count: 823
summary: No trades executed in WMT — both swing runs issued hold decisions due to weak trend (ADX < 25) and failed $129 breakout.
---

# WMT — Trades

## TL;DR

Zero trades have been placed in WMT. The paper trading system has analyzed the ticker twice — on April 11 and April 15, 2026 — and both runs produced a **hold** decision. The common blockers were: ADX below the 25 threshold (trend too weak), a failed breakout at $129 resistance, and risk-reward ratios below the 2:1 minimum. The Walton insider selling also weighed on both runs. No entry has been triggered.

## Open positions

None.

## Closed — last 30 days

None.

## Closed — older, rolled by month

None.

## Closed — older than 6 months

None.

---

## Run-by-run decision log

### Run: `swing_20260411_211655` — April 11, 2026

**Decision:** Hold (no trade)
**Model confidence:** 40%
**Head Trader stance:** Neutral at 40%

**Proposed levels (not executed):**
| Field | Value |
|---|---|
| Direction considered | Long (implied by target > entry) |
| Entry | $126.77 |
| Target | $131.00 |
| Stop | $122.00 |
| Risk-reward | 0.9:1 |
| Timeframe | N/A |

**Why no trade:**
The R:R of 0.9:1 (target distance $4.23, stop distance $4.77) failed the hard 2:1 minimum required by the portfolio manager. Additionally:
- ADX at 17.0 — far below the 25 threshold for trend confirmation
- Failed breakout at $129.13 resistance — price rejected and was trending back down
- Druckenmiller persona flagged the valuation as "absurd 52x P/E for 1.9% revenue growth"
- Walton Family selling $400M+ noted as a bearish signal
- Macro context: stock described as "defensive stock in risk-on market" — the Apr 11 environment (Iran ceasefire rally, S&P 500 up 3.6% for the week) favored risk-on names, not defensives

**Source:** `runs/swing_20260411_211655/decisions.json` — WMT entry

---

### Run: `20260415_110848` — April 15, 2026

**Decision:** Hold (no trade)
**Model confidence:** 42%
**Agent split:** 2 bullish / 4 neutral / 4 bearish (written as "2-4-4 split")

**Why no trade:**
The agent split resolved to no consensus, and the technical picture had deteriorated further since April 11:
- ADX 18 — still below 25 threshold
- Hourly EMAs confirmed in downtrend (not just weak, actively bearish on the short timeframe)
- Failed breakout from $129 high remained the dominant chart feature
- $4.6B in Walton family insider selling cited as a "structural headwind" (upgraded language vs Apr 11)
- The model's entry trigger was explicit: "wait for clean close above $129 on 1.5x+ volume"
- No risk-reward figures were even computed; the setup was rejected before that stage

**What changed from Apr 11 to Apr 15:**
- Price drifted lower (~$126.77 → ~$124.56 per Yahoo Finance data in web_research)
- Insider selling framing escalated from "$400M+" to "$4.6B" — possibly cumulative figure vs. a recent window
- Agent split worsened (2-4-4 vs. prior run's neutral lean), showing more models turning bearish
- Hourly EMA structure explicitly confirmed as downtrend (Apr 11 did not call this explicitly)

**Source:** `runs/20260415_110848/decisions.json` — WMT entry

---

## Entry trigger for future trades

The model has set a clear, repeatable trigger for WMT. Track these conditions before the next run:

**Bull trigger (long setup):**
1. Daily close above $129.00 on volume >= 1.5x 20-day average
2. ADX crosses above 25 on daily chart
3. Hourly EMA structure flips: 10 EMA > 20 EMA > 50 EMA

If all three conditions are met, a swing long with entry near $129-$130, target ~$136-$137 (analyst consensus), and stop below $124-$125 would give approximately 2:1 R:R.

**Bear trigger (short setup):**
1. Daily close below $122.00 support on elevated volume
2. Catalyst: Q1 FY2027 earnings miss (May 21, 2026) or tariff cost surprise
3. ADX rising above 20 on a downward slope

**No-touch conditions:**
- ADX < 25 with no clear direction
- Price in $122-$129 chop zone without catalyst

---

## Lifetime stats

| Metric | Value |
|---|---|
| Total runs analyzed | 2 |
| Trades placed | 0 |
| Win rate | N/A |
| Average hold time | N/A |
| Realized P&L | $0.00 |
| Unrealized P&L | $0.00 |
| Entry hit rate | N/A |
| Runs with "hold" decision | 2 / 2 (100%) |
| Highest confidence seen | 42% (Apr 15 run) |
| Model consensus high-water | 2 bullish / 4 neutral / 4 bearish (Apr 15) |

**Takeaway:** WMT has been analyzed twice and passed over both times. This is not an accident — the stock is in a genuine technical no-man's-land with a valuation that makes the risk-reward unattractive until either the breakout confirms or the price corrects enough to offer margin of safety. The paper trading system is correctly staying disciplined.

## Last updated

Bootstrap — sourced from `tracker.db` (0 rows for WMT) and decisions from runs `20260415_110848` and `swing_20260411_211655`. Next meaningful update: after May 21, 2026 Q1 FY2027 earnings, or if a breakout/breakdown triggers an entry.
