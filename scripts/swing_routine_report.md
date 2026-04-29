# Stock Swing Routine — Accuracy Report

**Period:** April 17–24, 2026 (12 routine sessions)  
**Generated:** 2026-04-24 20:40:22  
**Data source:** `routine_raw_results.json` (Claude routines UI)  
**Position sizing:** $500 per trade

```
========================================================
STOCK SWING ROUTINE — ACCURACY REPORT
April 17-24, 2026 (12 routine sessions)
========================================================

OVERALL: 3 wins / 8 losses / 19 open / 26 not triggered
TOTAL RECOMMENDATIONS: 56 (from 6 run dates)
WIN RATE: 27.3% (of 11 resolved trades)
ENTRY HIT RATE: 53.6% (entries that actually triggered)
REALIZED P&L: +$31.84 (assuming $500/trade)
UNREALIZED P&L: +$52.14 (19 open positions)
TOTAL P&L: +$83.97

────────────────────────────────────────────────────────
PER-TICKER BREAKDOWN
────────────────────────────────────────────────────────
Ticker  Trades  Wins  Loss  Open NoHit   WinR        P&L
--------------------------------------------------------
AAPL         3     0     0     1     2    N/A          —
AMD          6     1     0     0     5   100%    +$48.05
AMZN         6     1     1     0     4    50%    +$12.63
GOOGL        6     0     1     2     3     0%     $-9.09
GS           4     0     0     4     0    N/A          —
JPM          6     0     1     4     1     0%     $-7.94
META         2     0     1     1     0     0%     $-8.77
MSFT         3     0     1     2     0     0%     $-9.83
NKE          5     0     1     1     3     0%     $-5.43
NVDA         5     1     0     1     3   100%    +$26.32
QQQ          6     0     2     1     3     0%    $-14.10
SPY          2     0     0     1     1    N/A          —
XOM          2     0     0     1     1    N/A          —

────────────────────────────────────────────────────────
PER-DATE BREAKDOWN
────────────────────────────────────────────────────────
Date         Trades  Wins  Loss  Open NoHit   WinR
--------------------------------------------------
2026-04-17       12     3     2     3     4    60%
2026-04-20       10     0     3     3     4     0%
2026-04-21        7     0     3     3     1     0%
2026-04-22       10     0     0     6     4    N/A
2026-04-23        9     0     0     4     5    N/A
2026-04-24        8     0     0     0     8    N/A

────────────────────────────────────────────────────────
DETAILED TRADE LOG
────────────────────────────────────────────────────────
Date         Ticker Dir       Entry     Stop   Target Status              P&L Conf
----------------------------------------------------------------------------------
2026-04-17   AAPL   long   $ 262.50 $ 256.50 $ 282.00 not_triggered         —  60%
2026-04-17   AMD    long   $ 278.26 $ 270.00 $ 305.00 win 2026-04-23   +$48.05  70%
2026-04-17   AMZN   long   $ 249.70 $ 244.00 $ 262.00 win 2026-04-24   +$24.63  72%
2026-04-17   GOOGL  long   $ 337.12 $ 325.00 $ 350.00 open @344.40    +$10.80  82%
2026-04-17   JPM    long   $ 309.95 $ 304.00 $ 325.00 open @308.28     $-2.69  62%
2026-04-17   META   long   $ 676.87 $ 665.00 $ 710.00 loss 2026-04-23    $-8.77  74%
2026-04-17   MSFT   long   $ 420.26 $ 412.00 $ 442.00 loss 2026-04-23    $-9.83  72%
2026-04-17   NKE    short  $  45.54 $  47.50 $  41.50 open @44.69      +$9.33  70%
2026-04-17   NVDA   long   $ 199.50 $ 195.00 $ 210.00 win 2026-04-24   +$26.32  78%
2026-04-17   QQQ    long   $ 640.47 $ 634.00 $ 668.00 not_triggered         —  72%
2026-04-17   SPY    long   $ 701.66 $ 695.00 $ 722.00 not_triggered         —  72%
2026-04-17   XOM    short  $ 151.97 $ 154.00 $ 144.00 not_triggered         —  72%
2026-04-20   AMD    long   $ 265.00 $ 255.00 $ 290.00 not_triggered         —  65%
2026-04-20   AMZN   long   $ 246.00 $ 237.00 $ 265.00 not_triggered         —  65%
2026-04-20   GOOGL  long   $ 318.00 $ 307.00 $ 350.00 not_triggered         —  60%
2026-04-20   GS     long   $ 926.00 $ 912.00 $ 960.00 open @926.91     +$0.49  65%
2026-04-20   JPM    long   $ 315.00 $ 310.00 $ 328.00 loss 2026-04-23    $-7.94  68%
2026-04-20   MSFT   long   $ 414.00 $ 407.00 $ 445.00 open @424.62    +$12.83  62%
2026-04-20   NKE    short  $  46.00 $  46.50 $  42.62 loss 2026-04-21    $-5.43  72%
2026-04-20   NVDA   long   $ 191.50 $ 185.50 $ 205.00 not_triggered         —  68%
2026-04-20   QQQ    short  $ 644.50 $ 655.00 $ 603.00 loss 2026-04-22    $-8.15  58%
2026-04-20   XOM    long   $ 147.68 $ 144.50 $ 154.61 open @148.91     +$4.16  52%
2026-04-21   AMD    long   $ 280.00 $ 272.00 $ 305.00 not_triggered         —  82%
2026-04-21   AMZN   short  $ 250.00 $ 256.00 $ 222.82 loss 2026-04-23   $-12.00  70%
2026-04-21   GOOGL  short  $ 330.00 $ 336.00 $ 307.91 loss 2026-04-22    $-9.09  73%
2026-04-21   GS     long   $ 920.00 $ 905.00 $ 960.00 open @926.91     +$3.76  65%
2026-04-21   JPM    long   $ 310.00 $ 305.00 $ 325.00 open @308.28     $-2.77  68%
2026-04-21   META   short  $ 670.00 $ 685.00 $ 629.59 open @675.03     $-3.75  72%
2026-04-21   QQQ    short  $ 644.33 $ 652.00 $ 620.00 loss 2026-04-22    $-5.95  58%
2026-04-22   AAPL   long   $ 270.00 $ 262.00 $ 286.00 open @271.06     +$1.96  65%
2026-04-22   AMD    long   $ 297.00 $ 289.00 $ 315.00 not_triggered         —  75%
2026-04-22   AMZN   long   $ 252.00 $ 245.00 $ 266.00 not_triggered         —  72%
2026-04-22   GOOGL  long   $ 333.00 $ 325.00 $ 349.00 not_triggered         —  58%
2026-04-22   GS     long   $ 930.00 $ 905.00 $ 980.00 open @926.91     $-1.66  75%
2026-04-22   JPM    long   $ 311.50 $ 305.00 $ 325.00 open @308.28     $-5.17  72%
2026-04-22   NKE    short  $  46.35 $  48.20 $  42.62 not_triggered         —  70%
2026-04-22   NVDA   long   $ 200.00 $ 195.50 $ 215.00 open @208.27    +$20.68  68%
2026-04-22   QQQ    long   $ 648.00 $ 617.00 $ 710.00 open @663.88    +$12.25  78%
2026-04-22   SPY    long   $ 705.00 $ 687.50 $ 740.00 open @713.94     +$6.34  72%
2026-04-23   AMD    long   $ 285.00 $ 270.00 $ 320.00 not_triggered         —  55%
2026-04-23   AMZN   long   $ 250.00 $ 240.00 $ 270.00 not_triggered         —  63%
2026-04-23   GOOGL  long   $ 340.00 $ 330.00 $ 360.00 open @344.40     +$6.47  65%
2026-04-23   GS     long   $ 935.00 $ 918.00 $ 968.00 open @926.91     $-4.33  60%
2026-04-23   JPM    long   $ 312.00 $ 307.00 $ 322.00 open @308.28     $-5.96  65%
2026-04-23   MSFT   short  $ 415.81 $ 425.00 $ 393.49 open @424.62    $-10.59  68%
2026-04-23   NKE    short  $  47.00 $  49.50 $  42.00 not_triggered         —  68%
2026-04-23   NVDA   long   $ 196.50 $ 188.50 $ 213.00 not_triggered         —  62%
2026-04-23   QQQ    long   $ 652.00 $ 642.00 $ 672.00 not_triggered         —  58%
2026-04-24   AAPL   short  $ 270.05 $ 274.00 $ 260.23 not_triggered         —  65%
2026-04-24   AMD    short  $ 347.00 $ 360.00 $ 312.00 not_triggered         —  68%
2026-04-24   AMZN   short  $ 260.00 $ 265.00 $ 245.00 not_triggered         —  65%
2026-04-24   GOOGL  long   $ 338.00 $ 334.50 $ 350.00 not_triggered         —  72%
2026-04-24   JPM    long   $ 308.28 $ 304.50 $ 320.37 not_triggered         —  65%
2026-04-24   NKE    short  $  44.69 $  46.60 $  40.00 not_triggered         —  55%
2026-04-24   NVDA   long   $ 202.00 $ 199.10 $ 210.00 not_triggered         —  75%
2026-04-24   QQQ    short  $ 663.88 $ 675.00 $ 604.99 not_triggered         —  62%

────────────────────────────────────────────────────────
CONFIDENCE CALIBRATION
────────────────────────────────────────────────────────
  Confidence  Trades  Wins  Win Rate
------------------------------------
      50-59%       2     0        0%
      60-69%       1     0        0%
      70-79%       8     3       38%

────────────────────────────────────────────────────────
DIRECTION BREAKDOWN
────────────────────────────────────────────────────────
LONG: 40 trades, 3/6 resolved wins (50%), P&L: +$72.46
SHORT: 16 trades, 0/5 resolved wins (0%), P&L: $-40.62

========================================================
Report generated: 2026-04-24 20:40:22
Data source: routine_raw_results.json (Claude routines UI)
Position sizing: $500 per trade
========================================================
```

## Summary

- **Win rate:** 27.3% (3 wins / 8 losses)
- **Open trades:** 19
- **Not triggered:** 26
- **Realized P&L:** +$31.84

## Data Sources

Extracted from 12 Claude routine sessions via Playwright MCP scraping.
