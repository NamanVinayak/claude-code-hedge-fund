# Swing Analysis — Batch 2 — 2026-04-22

**Run ID:** `20260422_233705`  
**Mode:** swing  
**Tickers:** TSLA, JPM, GS, NKE, XOM, SPY, QQQ  
**Capital:** $100,000

---

## Overall Market Tone: **BULLISH with hedge**

The broad market is in a strong confirmed uptrend (SPY ADX 42.8, QQQ ADX 43.95). Financial sector is rotating in. Consumer Discretionary (NKE) and Energy (XOM) are under pressure. Momentum is the dominant theme — trend-following agents decisively outweigh mean-reversion warnings.

---

## Decisions

| Ticker | Action | Qty | Entry | Target | Stop | R/R | Confidence | Timeframe |
|--------|--------|-----|-------|--------|------|-----|------------|-----------|
| JPM | **BUY** | 50 | $311.50 | $325.00 | $305.00 | 2.08 | 72% | 5-8 days |
| GS | **BUY** | 15 | $930.00 | $980.00 | $905.00 | 2.00 | 75% | 5-10 days |
| NKE | **SHORT** | 200 | $46.35 | $42.62 | $48.20 | 2.01 | 70% | 4-8 days |
| SPY | **BUY** | 20 | $705.00 | $740.00 | $687.50 | 2.00 | 72% | 7-12 days |
| QQQ | **BUY** | 22 | $648.00 | $710.00 | $617.00 | 2.00 | 78% | 8-14 days |
| TSLA | HOLD | — | — | — | — | — | 30% | — |
| XOM | HOLD | — | — | — | — | — | 25% | — |

**Total exposure:** $51,576 / $100,000 (52%)  
**Long:** JPM + GS + SPY + QQQ · **Short:** NKE

---

## Key Signal Themes

### Bullish (JPM, GS, SPY, QQQ)
- All 4 have ADX > 25 with perfect EMA stack (10 > 21 > 50)
- QQQ: ADX 43.95 — strongest trend reading; RSI 94 but mean-reversion overridden by trend strength
- SPY: ADX 42.8; ROC21 +8.56%; Druckenmiller macro conviction
- GS: ROC21 +13.89% (highest acceleration); broke 941 resistance; Financial sector rotation
- JPM: Hourly RSI 33 at Fibonacci 61.8% support — clean pullback-buy entry

### Bearish (NKE)
- Price 14.5% below 50-SMA; EMA stack fully inverted (45.7 < 47.4 < 52.3 < 64.5)
- EPS -8.8% YoY; momentum ROC21 −11.42%
- 6/9 agents bearish (65–82%); Druckenmiller 82% conviction short
- Mean reversion agent was the lone bullish dissenter (oversold bounce) — overridden

### Avoided (TSLA, XOM)
- **TSLA:** Bearish conviction (205× P/E, EPS −9.4%) but no clean entry — daily RSI 55.8 neutral, EMAs tangled
- **XOM:** Daily RSI 21.8 (deeply oversold) conflicts with negative momentum — no 2:1 setup on either side

---

## Agent Consensus Summary

| Ticker | Bullish | Bearish | Neutral | Decision |
|--------|---------|---------|---------|----------|
| TSLA | 0 | 2 | 7 | HOLD |
| JPM | 6 | 2 | 1 | BUY |
| GS | 6 | 2 | 1 | BUY |
| NKE | 1 | 6 | 2 | SHORT |
| XOM | 1 | 4 | 4 | HOLD |
| SPY | 5 | 2 | 2 | BUY |
| QQQ | 5 | 2 | 2 | BUY |

*(9 swing strategy agents + Druckenmiller + news_sentiment; catalyst_trader all neutral due to no catalyst data)*

---

## Notable Conflicts

- **Mean Reversion vs Trend Followers on SPY/QQQ:** Mean reversion was 88–92% confident on short setups (RSI 90+ / Z-score 2.1+). Overridden by ADX > 42 readings — in strong trending markets, the system correctly weights trend continuation over statistical mean reversion.
- **Fundamental agents bearish on JPM/GS:** Fundamentals and growth agents flag valuation/growth concerns. Swing PM correctly scoped analysis to 5–10 day technical windows, not long-term thesis.
