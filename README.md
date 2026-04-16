# claude-code-hedge-fund

> A fork of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) (55k+ stars) rebuilt as Claude Code slash commands — with new trading modes, zero paid APIs, and optional paper trading.

**For educational purposes only. Not financial advice.**

---

## What's different from the original

| | virattt/ai-hedge-fund | This repo |
|---|---|---|
| Interface | Python CLI | **Claude Code slash commands** |
| LLM cost | Paid APIs (OpenAI/Groq/etc.) | **Free** — uses Claude Code subagents |
| Trading modes | Long-term invest only | Invest + **Swing + Day Trade + Crypto** |
| Paper trading | None | Optional Moomoo integration |
| Web research | None | Live news + macro context per ticker |
| Budget control | None | `--cash` flag, position limits |

---

## The three headline commands

### `/swing AAPL,TSLA,NVDA`
Multi-day trade setups (2–20 day holds). Nine specialized agents — breakout, mean reversion, trend follower, momentum, sector rotation, and more — debate each ticker. A Head Trader synthesizes. A Portfolio Manager makes the final call with entry, target, stop, and risk/reward.

### `/daytrade SPY,QQQ,IWM`
Intraday trade plans for the current session. Nine day-trade strategies — VWAP, opening range, momentum scalper, gap analyst, volume profiler — each analyze the same tickers. Produces setup type, entry trigger, targets, stop, and time window.

### `/autorun`
The daily routine in one command: syncs open positions → runs the analysis pipeline → places paper orders → prints the accuracy dashboard. Schedule is driven by `tracker/watchlist.json`.

### Bonus: crypto modes
```
/crypto-swing BTC-USD,ETH-USD,SOL-USD
/crypto-day BTC-USD,ETH-USD,SOL-USD
/crypto-autorun
```
Same pipeline, crypto-native agents (Fear & Greed, whale movements, funding rates), simulated locally — no exchange needed.

---

## How it works

```
/swing AAPL,MSFT,NVDA
  └─ prepare.py        — fetches prices, financials, news via yfinance + SEC EDGAR
  └─ web research      — live macro context + ticker news via WebSearch
  └─ 9 swing agents    — each reads a facts bundle, writes a signal (parallel)
  └─ head trader       — synthesizes the 9 signals into a unified view
  └─ aggregate.py      — deterministic technicals, fundamentals, risk manager
  └─ portfolio manager — final entry/target/stop decisions
  └─ explainer         — plain-English educational breakdown
  └─ finalize.py       — prints results
```

All LLM calls use Claude Code's built-in `Agent` tool — **no OpenAI key, no Anthropic API key, no paid data provider.**

---

## Setup

### 1. Prerequisites
- [Claude Code](https://claude.ai/code) (the CLI)
- Python 3.11+

### 2. Install
```bash
git clone https://github.com/YOUR_USERNAME/claude-code-hedge-fund
cd claude-code-hedge-fund
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Optional: API keys
```bash
cp .env.example .env
# FINNHUB_API_KEY — free tier at finnhub.io (improves news quality)
# COINGECKO_API_KEY — free tier at coingecko.com (for crypto sentiment)
```
Both are optional. The system works without them using yfinance + SEC EDGAR.

### 4. Run a slash command
Open Claude Code in this directory and type:
```
/swing AAPL,TSLA,NVDA
```

---

## Optional: Paper Trading (Moomoo)

Connect your own Moomoo account to have the system place paper trades automatically.

### Setup
1. Download [Moomoo OpenD](https://www.moomoo.com/download) — the local gateway
2. Copy `opend/OpenD.xml.example` → `opend/OpenD.xml` and fill in your credentials
3. Find your account ID in Moomoo app → Settings → About
4. Set it as an environment variable: `MOOMOO_ACCOUNT_ID=your_id`
5. Launch OpenD: `open opend/OpenD.app`

### Commands
```bash
python -m tracker execute --run-id RUN_ID   # place orders from a model run
python -m tracker monitor                    # sync fills, manage stops/targets
python -m tracker report                     # accuracy dashboard
python -m tracker status                     # open positions
```

> Moomoo paper trading is supported in Canada and other regions. US users may need to verify availability.

---

## Project structure

```
ai_hedge/              — core analysis pipeline
  data/                — yfinance, SEC EDGAR, Finnhub providers
  personas/            — 14 investor agents + 9 swing + 9 daytrade strategies
  deterministic/       — fundamentals, technicals, valuation, sentiment, risk
  runner/              — prepare, aggregate, finalize scripts
tracker/               — Moomoo paper trading integration (optional)
crypto_tracker/        — crypto simulated trading (optional)
.claude/skills/        — slash command definitions
```

---

## Analysis modes

| Mode | Command | Agents | Output |
|---|---|---|---|
| Invest | `/invest AAPL` | 14 legendary investor personas | Buy/sell/hold, holding period |
| Swing | `/swing AAPL` | 9 swing strategies | Entry, target, stop, R/R |
| Day Trade | `/daytrade SPY` | 9 intraday strategies | Setup, trigger, targets, time window |
| Research | `/research AAPL` | All 30+ agents | Bull/bear case, full signal grid |
| Crypto Swing | `/crypto-swing BTC-USD` | 9 strategies + crypto agents | Entry, target, stop |
| Crypto Day | `/crypto-day BTC-USD` | 9 strategies + crypto agents | Intraday setup |

---

## Credits

Built on top of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund). Core investor persona logic, helper functions, and portfolio management are adapted verbatim from the original. The swing trading mode, day trading mode, crypto mode, Claude Code slash command interface, paper trading integration, and web research pipeline are original additions.

---

## Disclaimer

This project is for **educational purposes only**. It is not intended for real trading or investment. The authors assume no liability for financial losses. Past paper trading performance does not guarantee future results.
