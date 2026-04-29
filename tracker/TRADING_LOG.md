# Trading Log — Paper Trading Journal

> **Purpose**: Persistent context file for AI agents. Any new chat should read this file first to understand the full trading history, open positions, known bugs, and lessons learned.
>
> **Last updated**: 2026-04-15 12:15 PM PDT
>
> **Platform**: Moomoo paper trading (account 76568910, TrdEnv.SIMULATE)
> **Budget**: $5,000 (self-imposed; Moomoo account has $2M but we enforce our own limit)
> **Max per position**: 25% of capital ($1,250)
> **Max concurrent trades**: 8 per mode

---

## Table of Contents

1. [Current Open Positions (Moomoo)](#current-open-positions-moomoo)
2. [Known Bugs & Sync Issues](#known-bugs--sync-issues)
3. [Run History](#run-history)
4. [Detailed Trade Log](#detailed-trade-log)
5. [Closed / Realized Trades](#closed--realized-trades)
6. [Pending / Unfilled Orders](#pending--unfilled-orders)
7. [Cancelled Orders](#cancelled-orders)
8. [Key Lessons & Notes](#key-lessons--notes)
9. [Moomoo Order History](#moomoo-order-history)

---

## Current Open Positions (Moomoo)

These are the ACTUAL positions held on Moomoo as of 2026-04-15 ~11:50 AM PDT. This is the source of truth — not the tracker DB.

| Ticker | Side | Qty | Cost Basis | Current | Market Val | P&L | Mode | Run |
|--------|------|-----|-----------|---------|-----------|-----|------|-----|
| NVDA | LONG | 6 | $197.196 | $197.51 | $1,177.26 | -$5.92 | swing | 20260415_093758 |
| GOOG | LONG | 3 | $331.730 | $334.46 | $998.85 | +$3.66 | swing | 20260415_093758 |
| JPM | LONG | 4 | $305.300 | $305.80 | $1,223.92 | +$2.72 | swing | 20260415_093758 |
| META | LONG | 1 | $673.720 | $675.04 | $672.19 | -$1.53 | swing | 20260415_093758 |
| SPY | LONG | 1 | $697.310 | $699.56 | $697.99 | +$0.68 | daytrade | 20260415_104041 |
| IWM | SHORT | 4 | $268.470 | $269.04 | -$1,074.52 | -$0.64 | daytrade | 20260415_104041 |

**NKE ghost position CLOSED** at 12:15 PM PDT Apr 15 (covered 17 shares at $45.845, realized loss -$39.10)
**Total open P&L: slightly positive** (NKE drag removed)

---

## Known Bugs & Sync Issues

### ✅ RESOLVED: NKE Ghost Position (was CRITICAL)
- **What happened**: Tracker DB showed NKE (trade id=11) as `status=closed`, but Moomoo still held -17 NKE shares.
- **Root cause**: Monitor SELL 17 + BUY 17 cancelled each other out instead of flattening the position.
- **Resolution**: Manually placed BUY 17 NKE @ $46.50 limit on Apr 15 12:15 PM PDT. Filled at $45.845. Position is now flat (qty=0).
- **Realized loss**: -$39.10 on Moomoo (entry $43.544, exit $45.845, 17 shares).
- **Lesson**: Monitor's close logic needs to check Moomoo position state after execution, not just assume the close worked.

### ⚠️ BUG: Pending Orders Never Placed on Moomoo
- Trades id=6,7,8,9,10 from run `20260413_185011` show as `status=pending` in the tracker but were never submitted to Moomoo as orders. The executor either wasn't run for them or they failed silently. These are theoretical positions only.

### ⚠️ BUG: Moomoo DAY Orders Expire
- Moomoo paper trading only supports `TimeInForce.DAY`. Limit orders expire at end of each trading day. Any unfilled orders from the Apr 11/12 runs were auto-cancelled by Moomoo.

### ⚠️ Note: Mac Sleep Kills Monitor
- The monitor loop runs as a background shell process. If the Mac sleeps or closes, the monitor dies and stops protecting positions with stops/targets. This is what happened with NKE going unprotected.

---

## Run History

### Runs That Produced Executed Trades

| Run ID | Date | Mode | Tickers | Trades Placed |
|--------|------|------|---------|---------------|
| `swing_20260411_211655` | Apr 11 | swing | 19 stocks (TSLA,AAPL,NVDA,AMD,META,MSFT,GOOG,AMZN,JPM,BAC,GS,UNH,JNJ,PFE,XOM,CVX,WMT,NKE,DIS) | UNH buy, XOM short, CVX short, NKE short → all cancelled (placed on weekend) |
| `20260413_185011` | Apr 13 | swing | same 19 stocks | NKE short (filled Apr 14), NVDA/GOOG/JPM/UNH buy + CVX short (pending, never submitted to Moomoo) |
| `20260415_093758` | Apr 15 | swing | NVDA,GOOG,TSLA,JPM,AAPL,META | NVDA buy 6, GOOG buy 3, JPM buy 4, META buy 1 (all filled). TSLA short filtered out (earnings risk). AAPL hold. |
| `20260415_104041` | Apr 15 | daytrade | SPY,QQQ,IWM | SPY buy 1, IWM short 4 (filled). QQQ hold (9/9 neutral). |

### Runs Without Trade Execution (analysis only or incomplete)

| Run ID | Date | Mode | Notes |
|--------|------|------|-------|
| `20260414_031739` | Apr 14 | daytrade (crypto) | BTC/ETH/SOL day trade decisions — not executed on Moomoo |
| `20260414_042308` | Apr 14 | daytrade (crypto) | Another crypto run — not executed |
| `20260414_071817` | Apr 14 | swing | 19 stocks — prepare step only, no decisions.json |
| `20260415_110527` | Apr 15 | swing | 10 stocks (AMD,MSFT,AMZN,BAC,GS,JNJ,PFE,XOM,WMT,DIS) — was being built when /swing skill was being fixed |
| `20260415_110848` | Apr 15 | swing | Same 10 stocks — **analysis complete, decisions ready, NOT yet executed** (usage limit hit before explainer/execution). See "Unexecuted Decisions" section below. |
| Earlier dev runs (20260408-20260410) | Apr 8-10 | various | Pipeline development and testing — no real trades |

---

## Detailed Trade Log

### Trade #1-5: Run `swing_20260411_211655` (Apr 11, 2026)
**Context**: First real swing run. 19-stock universe. Run on Friday evening.

| ID | Ticker | Direction | Qty | Entry | Target | Stop | Conf | Status | Reasoning |
|----|--------|-----------|-----|-------|--------|------|------|--------|-----------|
| 1 | UNH | long | 1 | $296.00 | $320.00 | $288.00 | 58% | **CANCELLED** | Medicare Advantage 2.48% rate hike catalyst. 122 insider buys vs 29 sells. R:R 3.0:1. |
| 3 | XOM | short | 6 | $155.00 | $145.00 | $160.00 | 58% | **CANCELLED** | Sector rotation OUT of energy. Iran ceasefire reducing oil premium. CCI -126. R:R 2.0:1. |
| 4 | CVX | short | 5 | $192.00 | $178.00 | $199.00 | 62% | **CANCELLED** | Worst CCI in universe at -170. Chevron Middle East hit. Insider selling: Pate $8.6M. R:R 2.0:1. |
| 5 | NKE | short | 17 | $44.00 | $38.00 | $46.50 | 70% | **CANCELLED** | (no detailed reasoning in DB) |

**Why cancelled**: Orders were placed on Saturday (Apr 12 00:55-00:58 UTC). Moomoo DAY orders expire — they couldn't fill over the weekend and were auto-cancelled.

---

### Trade #6-11: Run `20260413_185011` (Apr 13, 2026)
**Context**: Second full swing run. Same 19-stock universe. Run on Sunday evening, decisions ready for Monday market open.

| ID | Ticker | Direction | Qty | Entry | Target | Stop | Conf | Timeframe | Status | What Happened |
|----|--------|-----------|-----|-------|--------|------|------|-----------|--------|---------------|
| 6 | NVDA | long | 3 | $188.00 | $210.00 | $180.00 | 75% | 7-14 days | **PENDING** | Limit order at $188 — never submitted to Moomoo. Market opened at ~$197, well above entry. |
| 7 | GOOG | long | 3 | $315.00 | $345.00 | $305.00 | 70% | 7-14 days | **PENDING** | Limit at $315 — never submitted. Market at ~$332. |
| 8 | JPM | long | 3 | $310.00 | $330.00 | $300.00 | 65% | 5-10 days | **PENDING** | Limit at $310 — never submitted. Market at ~$305. Closest to filling. |
| 9 | UNH | long | 1 | $305.00 | $325.00 | $295.00 | 68% | 7-12 days | **PENDING** | Limit at $305 — never submitted. Market at ~$313. |
| 10 | CVX | short | 5 | $192.00 | $182.00 | $197.00 | 55% | 5-10 days | **PENDING** | Limit at $192 — never submitted. Market at ~$185. Would be profitable if entered. |
| 11 | **NKE** | **short** | **17** | **$43.50** | **$40.00** | **$45.00** | **72%** | 5-10 days | **CLOSED (tracker) / OPEN (Moomoo)** | See NKE saga below. |

**NKE Saga (Trade #11)**:
1. Apr 14 10:36 AM: Executor placed MARKET SELL 17 NKE → filled at $43.555 (opened short)
2. Tracker recorded `entered_at=2026-04-14 10:36:30`, entry fill price not recorded (bug)
3. NKE moved against us — price rose from $43.55 to $45+
4. No stop loss was placed on Moomoo (monitor loop wasn't running — Mac was asleep)
5. Apr 15: Monitor attempted to manage: SELL 17 @ $45.51 (filled), then BUY 17 @ $45.52 (filled)
6. Tracker marked trade as `closed` with `pnl=-35.70`
7. **BUT Moomoo still holds -17 NKE at cost $43.544** ← GHOST POSITION
8. As of now, NKE at $45.83 → unrealized loss of **-$38.90** on Moomoo

---

### Trade #12-16: Run `20260415_093758` (Apr 15, 2026)
**Context**: Morning swing run. 6-stock focused universe (NVDA,GOOG,TSLA,JPM,AAPL,META). Executed at ~10:05 AM PDT.

| ID | Ticker | Direction | Qty | Entry Limit | Fill Price | Target | Stop | Conf | Timeframe | R:R | Reasoning |
|----|--------|-----------|-----|------------|-----------|--------|------|------|-----------|-----|-----------|
| 12 | NVDA | long | 2 | $198.47 | $197.29 | $209.70 | $189.10 | 62% | 5-10 days | 2.27 | 7/10 strategies bullish; breakout above $196.51 resistance; AI capex supercycle. First partial fill. |
| 13 | NVDA | long | 4 | $198.50 | $197.15 | $209.70 | $189.10 | — | — | — | Remainder of 6-share NVDA position. |
| 14 | GOOG | long | 3 | $332.10 | $331.73 | $355.00 | $318.00 | — | 7-12 days | 2.08 | 7/10 bullish; breakout above $330.58; Google Cloud AI partnership catalyst. |
| 15 | JPM | long | 4 | $305.30 | $305.30 | $319.60 | $298.30 | 70% | 5-10 days | 2.18 | Highest conviction (7/10 bulls, 0 neutral); Q1 earnings +13% beat; hourly RSI 31 buy-the-dip. |
| 16 | META | long | 1 | $676.00 | $673.72 | $706.40 | $637.70 | 63% | 7-14 days | 2.38 | Strongest momentum (#1 MACD, squeeze, ROC); MS top tech earnings pick; Broadcom AI chip deal. Max 1 share per risk limits. |

**Not traded from this run**:
- **TSLA short** (1 share, $391.86 entry, 49% conf) — Filtered out by executor due to Apr 22 earnings binary risk.
- **AAPL hold** — No trade. ADX 12.5 (no trend), CEO sold $12M+ in April.

**All orders on Moomoo**: Placed as NORMAL (limit) orders, all filled immediately at or below limit.

---

### Trade #17-18: Run `20260415_104041` (Apr 15, 2026)
**Context**: Intraday day trade run. ETF universe (SPY, QQQ, IWM). Executed at ~10:53 AM PDT.

| ID | Ticker | Direction | Qty | Entry Limit | Fill Price | Target | Stop | Conf | Time Window | R:R | Reasoning |
|----|--------|-----------|-----|------------|-----------|--------|------|------|-------------|-----|-----------|
| 17 | SPY | long | 1 | $697.45 | $697.31 | $699.33 | $696.26 | 64% | morning | 1.58 | 8/9 bullish consensus. Triple-confluence breakout: above OR high, prior day high, and VWAP. Bullish squeeze fired. Below-avg volume limits size. |
| 18 | IWM | short | 4 | $268.15 | $268.47 | $267.01 | $268.85 | 55% | afternoon | 1.63 | 8/9 bearish consensus. Relative weakness vs SPY/QQQ. Below VWAP, below intraday EMAs, SuperTrend bearish. |

**Not traded**: QQQ — 9/9 unanimous neutral. No setup met 1.5:1 R:R threshold.

**Note**: An auto-close script was deployed for day trades at 3:44 PM ET. IWM stop at $268.85 was nearly hit (IWM traded to $269.04).

---

### Unexecuted Decisions: Run `20260415_110848` (Apr 15, 2026)
**Context**: Second swing run of the day covering the remaining 10 watchlist tickers not in the morning run. Full pipeline completed (prepare → web research → 9 agents → head trader → aggregate → PM decisions), but the Claude Code session hit its usage limit before the explainer agent finished and before orders were placed. **These decisions have NOT been executed on Moomoo.**

| Ticker | Action | Qty | Entry | Target | Stop | R:R | Conf | Timeframe | Reasoning |
|--------|--------|-----|-------|--------|------|-----|------|-----------|-----------|
| **AMZN** | **buy** | 3 | $246.00 | $263.00 | $238.50 | 2.27:1 | 72% | 6-10 days | Top-priority long: $11.6B Globalstar acquisition + 1.57x breakout volume (only name passing 1.5x test). 6/9 agents bullish. EMAs aligned, ADX 37, squeeze bullish breakout. |
| **BAC** | **buy** | 18 | $53.00 | $57.00 | $51.50 | 2.67:1 | 65% | 6-10 days | Cleanest earnings catalyst: best Q1 in nearly 2 decades, zero trading loss days, profit +17%. 5/9 agents bullish. RSI 78.6, ADX 40, squeeze bullish breakout. |
| **AMD** | **buy** | 2 | $248.00 | $268.00 | $241.00 | 2.86:1 | 62% | 5-10 days | AI/semiconductor momentum: Wayve $60M investment catalyst, ADX 41, daily EMAs fully aligned, squeeze bullish breakout. 5/9 agents bullish. |
| **MSFT** | **buy** | 1 | $400.00 | $422.00 | $390.00 | 2.20:1 | 60% | 7-12 days | Pre-earnings run-up into Apr 29. Daily SuperTrend flipped bullish (trend_changed=true). 6/9 agents bullish. Max qty 1 per risk limit. |
| **XOM** | **short** | 6 | $151.00 | $143.00 | $154.00 | 2.67:1 | 62% | 5-10 days | Bearish divergence: oil macro bullish on Iran/Hormuz but XOM in confirmed downtrend. 6/9 agents bearish. Iran peace talks headwind for oil. |
| **DIS** | **buy** | 9 | $100.50 | $108.00 | $97.50 | 2.50:1 | 55% | 7-12 days | Cautious bullish: MACD histogram turned strongly positive, ADX 31. Druckenmiller bullish on valuation (P/E 14.76). |
| GS | hold | 0 | — | — | — | — | 48% | — | Split 4-3-3, ADX 19.4 too weak. Wait for ADX > 25. |
| JNJ | hold | 0 | — | — | — | — | 42% | — | 8/9 neutral. Daily squeeze building, direction unresolved. |
| PFE | hold | 0 | — | — | — | — | 35% | — | 8/9 neutral. No momentum in either direction. Binary earnings risk. |
| WMT | hold | 0 | — | — | — | — | 42% | — | ADX 18, failed breakout. $4.6B Walton insider selling headwind. |

**To execute these**: `python -m tracker execute --run-id 20260415_110848`
**Note**: All entry prices are limit orders. Check if market prices are still near these levels before executing — some may have moved.

## Closed / Realized Trades

| Trade | Ticker | Direction | Qty | Entry | Exit | P&L | Notes |
|-------|--------|-----------|-----|-------|------|-----|-------|
| #11 | NKE | short | 17 | $43.555 (market fill Apr 14) | $45.845 (manual cover Apr 15 12:15 PM) | **-$39.10** | Ghost position finally closed manually. Stop was $45.00 — price hit $45.85 before we covered. |

**Total realized P&L: -$39.10**

---

## Pending / Unfilled Orders

These orders exist in the tracker DB as `status=pending` but were **never submitted to Moomoo**. They represent model recommendations that weren't acted on.

| ID | Ticker | Dir | Entry | Current | Theoretical P&L | Would have worked? |
|----|--------|-----|-------|---------|-----------------|-------------------|
| 6 | NVDA | long 3 | $188 | $197.51 | +$28.53 | ✅ Yes — entry well below market |
| 7 | GOOG | long 3 | $315 | $334.46 | +$58.38 | ✅ Yes — strong breakout |
| 8 | JPM | long 3 | $310 | $305.80 | -$12.60 | ❌ No — JPM dipped below entry |
| 9 | UNH | long 1 | $305 | $313.86 | +$8.86 | ✅ Yes |
| 10 | CVX | short 5 | $192 | $185.37 | +$33.15 | ✅ Yes — oil weakness continues |

**Theoretical total if all had been entered: +$116.32** (missed opportunity)

---

## Cancelled Orders

| ID | Ticker | Dir | Qty | Entry | Run | Why Cancelled |
|----|--------|-----|-----|-------|-----|---------------|
| 1 | UNH | long | 1 | $296 | swing_20260411_211655 | Placed on Saturday, DAY order expired |
| 3 | XOM | short | 6 | $155 | swing_20260411_211655 | Placed on Saturday, DAY order expired |
| 4 | CVX | short | 5 | $192 | swing_20260411_211655 | Placed on Saturday, DAY order expired |
| 5 | NKE | short | 17 | $44 | swing_20260411_211655 | Placed on Saturday, DAY order expired |

---

## Key Lessons & Notes

### What's Working
1. **Model accuracy is decent** — theoretical P&L on unfilled orders (+$116) shows the signals have value
2. **Today's swing entries** are all in the right direction (bull market, long bias confirmed)
3. **Multi-agent consensus** (7/10+ bullish) correlates with profitable setups

### What's Broken
1. **Order placement timing** — Weekend/after-hours submissions get cancelled by DAY order rules
2. **Monitor loop dies with Mac sleep** — Positions go unprotected
3. **NKE sync bug** — Tracker and Moomoo can get out of sync when monitor tries to manage positions
4. **Pending orders never submitted** — Trade #6-10 were never actually placed on Moomoo, cause unknown (executor may not have been run)

### Trading Infrastructure Bugs Fixed (Apr 15)
1. **Executor concurrent trade limit** — Was global, now scoped per mode (swing vs daytrade tracked separately)
2. **Swing skill batching** — Was 3 batches of 4 agents, now all 9 in parallel
3. **PM decisions format** — Added requirement for `{"decisions": {...}}` wrapper so executor can parse
4. **Subagent skill invocation guard** — Added "Do NOT invoke any skills" to all subagent prompts

### Budget Tracking
- **Budget**: $5,000 paper
- **Available cash**: $0.00 (fully deployed)
- **Open exposure**: ~$4,073 in filled swing positions + ~$1,772 in day trade positions + NKE ghost
- **Moomoo buying power**: $1,992,918 (not relevant — we track our own budget)

---

## Moomoo Order History (Complete)

Raw order history from Moomoo API, oldest first:

```
2026-04-11 23:14:48 | AAPL  BUY    MARKET  1 @ $0.00   | filled=0  | CANCELLED (after hours test)
2026-04-12 00:55:39 | UNH   BUY    LIMIT   1 @ $296.00 | filled=0  | CANCELLED (weekend)
2026-04-12 00:56:07 | UNH   BUY    LIMIT   1 @ $296.00 | filled=0  | CANCELLED (weekend, duplicate)
2026-04-12 00:56:08 | XOM   SELL   LIMIT   6 @ $155.00 | filled=0  | CANCELLED (weekend)
2026-04-12 00:56:08 | CVX   SELL   LIMIT   5 @ $192.00 | filled=0  | CANCELLED (weekend)
2026-04-12 00:56:22 | NKE   SELL   LIMIT  17 @ $44.00  | filled=0  | CANCELLED (weekend)
2026-04-14 10:36:29 | NKE   SELL   MARKET 17 @ $0.00   | filled=17 @ $43.555 | FILLED (opened short)
2026-04-15 13:05:49 | NVDA  BUY    LIMIT   2 @ $198.47 | filled=2  @ $197.29  | FILLED
2026-04-15 13:10:28 | NKE   SELL   LIMIT  17 @ $45.50  | filled=17 @ $45.51   | FILLED (monitor: sold)
2026-04-15 13:11:55 | NKE   BUY    LIMIT  17 @ $45.60  | filled=17 @ $45.52   | FILLED (monitor: bought back — but position still open!)
2026-04-15 13:12:38 | NVDA  BUY    LIMIT   4 @ $198.50 | filled=4  @ $197.15  | FILLED
2026-04-15 13:12:38 | GOOG  BUY    LIMIT   3 @ $332.10 | filled=3  @ $331.73  | FILLED
2026-04-15 13:12:38 | JPM   BUY    LIMIT   4 @ $305.30 | filled=4  @ $305.30  | FILLED
2026-04-15 13:12:39 | META  BUY    LIMIT   1 @ $676.00 | filled=1  @ $673.72  | FILLED
2026-04-15 13:52:59 | SPY   BUY    LIMIT   1 @ $697.45 | filled=1  @ $697.31  | FILLED
2026-04-15 13:52:59 | IWM   SELL   LIMIT   4 @ $268.15 | filled=4  @ $268.47  | FILLED (opened short)
```

---

## How to Update This File

After every trading session or model run that produces trades, append to the **Detailed Trade Log** section and update **Current Open Positions**. Any AI agent should:

1. Read this file at the start of any trading-related conversation
2. Cross-reference with `python -m tracker status` and Moomoo API for live data
3. Update this file after placing/closing any trades
4. Note any discrepancies between tracker DB and Moomoo in the bugs section
