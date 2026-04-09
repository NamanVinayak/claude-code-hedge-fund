# AI Hedge Fund — Claude Code Skill Collection

Analyze stocks using 30+ AI agents — legendary investor personas, swing trade strategies, and intraday day-trade systems. Built as a collection of Claude Code slash commands.

## Install

```bash
pip install ai-hedge-fund
ai-hedge-fund install
```

## Commands

| Command | What it does | Agents | Time |
|---------|-------------|--------|------|
| `/invest AAPL,MSFT` | Long-term portfolio decisions | 14 investor personas (Buffett, Munger, Graham, etc.) | ~5 min |
| `/swing TSLA` | Swing trade setups (2-20 days) | 9 swing strategies + Head Trader | ~3 min |
| `/daytrade SPY` | Intraday trade plan | 9 day-trade strategies + Head Trader | ~3 min |
| `/research NVDA` | Comprehensive research report | All 30+ agents | ~15 min |

## How It Works

Each command follows the same pattern:

```
Your ticker → Fetch financial data → N AI agents analyze independently
→ Deterministic math agents → Synthesis → Final decision/report
```

**Invest**: 14 legendary investors (Warren Buffett, Charlie Munger, Ben Graham, Cathie Wood, Michael Burry, etc.) each independently analyze the stock using their real-world investment philosophy. A portfolio manager synthesizes all opinions into a buy/sell/hold decision with holding duration.

**Swing**: 9 trading strategies (trend following, pullback, breakout, momentum, mean reversion, catalyst, sector rotation) analyze the daily chart. A Head Trader resolves conflicting signals. Output includes entry price, target, stop-loss, and risk-reward ratio.

**Day Trade**: 9 intraday strategies (VWAP, momentum scalping, mean reversion, breakout, gap analysis, volume profiling, pattern reading, stat arb, news catalyst) analyze 5-minute charts. Output is a specific trade plan for the day.

**Research**: All 30+ agents from all modes run. Output is a balanced report: bull case, bear case, key metrics, risk factors, sentiment breakdown. No trading recommendation.

## Data Sources (all free)

- **yfinance** — daily + intraday price data, market cap
- **SEC EDGAR** — 10+ years of quarterly financials, TTM snapshots
- **Finnhub** (free tier) — insider trades, company news

No paid API keys required. Optional `FINNHUB_API_KEY` in `.env` for enhanced data.

## Uninstall

```bash
ai-hedge-fund uninstall
pip uninstall ai-hedge-fund
```

## Requirements

- Python 3.10+
- Claude Code

## License

MIT
