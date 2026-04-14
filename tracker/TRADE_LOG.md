# Paper Trading Log

## Bankroll

| Date | Starting Capital | Realized P&L | Open Exposure | Available Cash |
|------|-----------------|--------------|---------------|----------------|
| 2026-04-11 | $5,000.00 | $0.00 | $2,934.00 | $2,066.00 |

## Active Positions (placed 2026-04-11, Friday night)

| # | Ticker | Direction | Qty | Entry Price | Stop Loss | Target | Risk:Reward | Thesis | Status |
|---|--------|-----------|-----|-------------|-----------|--------|-------------|--------|--------|
| 1 | UNH | LONG | 1 | $296.00 | $288.00 | $320.00 | 3.0:1 | Medicare Advantage 2.48% rate hike + strongest insider buying | PENDING |
| 2 | XOM | SHORT | 6 | $155.00 | $160.00 | $145.00 | 2.0:1 | Energy sector rotation out on Iran ceasefire | PENDING |
| 3 | CVX | SHORT | 5 | $192.00 | $199.00 | $178.00 | 2.0:1 | Same energy headwind + self-reported $2.7-3.7B hit | PENDING |
| 4 | NKE | SHORT | 17 | $44.00 | $46.50 | $38.00 | 2.4:1 | ADX 64.6 (strongest downtrend), 75% crash, competitive erosion | PENDING |

**Total exposure**: $2,934 (58.7% of capital)
**Max loss if all stops hit**: ~$115 (2.3% of capital)
**Max profit if all targets hit**: ~$404 (8.1% of capital)

## Closed Positions

*None yet — first trades placed 2026-04-11.*

## Daily P&L History

| Date | Trades Placed | Trades Closed | Wins | Losses | Day P&L | Cumulative P&L |
|------|--------------|---------------|------|--------|---------|----------------|
| 2026-04-11 | 4 | 0 | 0 | 0 | $0.00 | $0.00 |

## Run History

| Run ID | Date | Mode | Tickers Analyzed | Trades Placed | Notes |
|--------|------|------|-----------------|---------------|-------|
| swing_20260411_211655 | 2026-04-11 | swing | TSLA,AAPL,NVDA,AMD,META,MSFT,GOOG,AMZN,JPM,BAC,GS,UNH,JNJ,PFE,XOM,CVX,WMT,NKE,DIS (19) | 4 (UNH long, XOM/CVX/NKE short) | First live run. 15 holds, 4 trades. Web research + verification ran. Data bugs caught in AMZN, JPM, UNH, PFE, JNJ, CVX, DIS. |

## Watchlist

**Swing (daily)**: TSLA, AAPL, NVDA, AMD, META, MSFT, GOOG, AMZN, JPM, BAC, GS, UNH, JNJ, PFE, XOM, CVX, WMT, NKE, DIS (19 stocks)
**Daytrade (daily)**: SPY, QQQ, IWM (3 ETFs)

## Settings

- Starting capital: $5,000
- Max per position: $1,250 (25%)
- Max concurrent trades: 8
- Paper trading platform: Moomoo (account 76568910)

## Bugs Found & Fixed During First Run

1. `OrderType.LIMIT` → `OrderType.NORMAL` (Moomoo naming convention)
2. `TimeInForce.GTC` → `TimeInForce.DAY` (paper trading limitation)
3. `TrdSide.SELL_SHORT` → `TrdSide.SELL` (paper trading uses SELL for both long exit and short entry)
4. `TrdSide.BUY_BACK` → `TrdSide.BUY` (same — paper trading simplification)
5. Duplicate UNH order placed due to re-running executor — cancelled duplicate (order 690743)

## Market Context (Week of 2026-04-07)

- US-Iran ceasefire announced April 8 → Dow +1,300 pts (biggest day since April 2025)
- S&P 500 up 3.6% for the week, Nasdaq up 4.7%
- Oil dropped 16% on ceasefire news to ~$94, rebounded to $99
- Fed holding at 3.50-3.75%, next FOMC April 29
- Consumer sentiment record low 47.6 (University of Michigan)
- Energy sector +40% YTD, now at risk of rotation on ceasefire
