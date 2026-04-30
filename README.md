# AI Hedge Fund — Claude Code Skill Collection

Analyze stocks using ~28 AI agents — legendary investor personas, swing trade strategies, and intraday day-trade systems. Built as a collection of Claude Code slash commands. Runs entirely on a Claude Code subscription — no paid LLM APIs.

## Install

```bash
pip install ai-hedge-fund
ai-hedge-fund install
```

## Commands

| Command | What it does | Agents | Time |
|---------|-------------|--------|------|
| `/invest AAPL,MSFT` | Long-term portfolio decisions | 14 investor personas (Buffett, Munger, Graham, etc.) | ~5 min |
| `/swing TSLA` | Swing trade setups (2-20 days) | 5 swing strategies + Head Trader | ~3 min |
| `/daytrade SPY` | Intraday trade plan | 9 day-trade strategies + Head Trader | ~3 min |
| `/research NVDA` | Comprehensive research report | ~28 agents (all modes combined) | ~15 min |

## How It Works

Each command follows the same pattern:

```
Your ticker → Fetch financial data → N AI agents analyze independently
→ Deterministic math agents → Synthesis → Final decision/report
```

**Invest**: 14 legendary investors (Warren Buffett, Charlie Munger, Ben Graham, Cathie Wood, Michael Burry, etc.) each independently analyze the stock using their real-world investment philosophy. A portfolio manager synthesizes all opinions into a buy/sell/hold decision with holding duration.

**Swing**: 5 trading strategies (trend/momentum, mean reversion, breakout, catalyst/news, macro context) analyze daily + hourly charts. Each owns a genuinely distinct viewpoint so the Head Trader resolves real disagreement, not echoes. Output includes entry price, target, stop-loss, and risk-reward ratio.

**Day Trade**: 9 intraday strategies (VWAP, momentum scalping, mean reversion, breakout, gap analysis, volume profiling, pattern reading, stat arb, news catalyst) analyze 5-minute charts. Output is a specific trade plan for the day.

**Research**: All agents from all modes run. Output is a balanced report: bull case, bear case, key metrics, risk factors, sentiment breakdown. No trading recommendation.

## Wiki Memory Layer (optional)

Each run can read and update a per-ticker wiki — a synthesis of past analysis, trade outcomes, and current thesis. The agents read TL;DR slices of the relevant wiki pages, write decisions, and a curator agent updates the wiki at the end of the run. A weekly compactor keeps pages within size budgets.

Disabled by default. Enable by setting `settings.wiki_enabled: true` in `tracker/watchlist.json` after running `scripts/wiki_bootstrap.py` for your watchlist.

## Data Sources (all free)

- **yfinance** — daily + intraday price data, market cap
- **SEC EDGAR** — 10+ years of quarterly financials, TTM snapshots
- **Finnhub** (free tier) — insider trades, company news

No paid API keys required. Works out of the box with prices, financials, and technicals.

### Optional: Finnhub API key (free, recommended)

For insider trading data and company news sentiment, add a free Finnhub API key:

1. Go to [finnhub.io](https://finnhub.io) and create a free account (no credit card needed)
2. Copy your API key from the dashboard
3. Create a `.env` file in your project directory:
```
FINNHUB_API_KEY=your_key_here
```

Without this key, the system still works — you just won't get insider trade patterns or news sentiment analysis.

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
