# Wiki Trades Audit Report

Scanned 23 ticker `trades.md` files. Found 4 with discrepancies.

Phantom runs = referenced in wiki but no Turso trade with that run_id.
Cross-contamination = run_id exists in Turso for a different ticker.
Stale findings = old/buggy numbers we flagged for cleanup.

## Tickers with issues

### IWM
- File: `wiki/tickers/IWM/trades.md`
- **Phantom runs** (1): 20260415_104041

### JNJ
- File: `wiki/tickers/JNJ/trades.md`
- **Phantom runs** (1): 20260430_194522

### META
- File: `wiki/tickers/META/trades.md`
- **Phantom runs** (1): 20260415_093758

### SPY
- File: `wiki/tickers/SPY/trades.md`
- **Phantom runs** (1): 20260415_104041

## Tickers clean

AAPL, AMD, AMZN, BAC, CVX, DIS, GOOG, GOOGL, GS, JPM, MSFT, NKE, NVDA, PFE, QQQ, TSLA, UNH, WMT, XOM
