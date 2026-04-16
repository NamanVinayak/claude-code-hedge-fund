# Claude Code Hedge Fund

This is a fork of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) rebuilt as **Claude Code slash commands** — with new trading modes, zero paid APIs, and optional paper trading.

Instead of calling OpenAI or Groq, every AI agent runs as a Claude Code subagent. This means the entire system is **free to run** if you already use Claude Code.

This project is for **educational purposes only** and is not intended for real trading or investment.

> Built on top of virattt's original work. Core investor persona logic is adapted from the upstream repo. Swing trading, day trading, crypto modes, the slash command interface, web research pipeline, and paper trading integration are original additions.

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

---

## The story behind this fork

[virattt's ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) blew up on GitHub — 55,000+ stars — because the idea clicked instantly: what if Warren Buffett, Charlie Munger, Michael Burry, and a dozen other legendary investors were AI agents that actually analyzed your stocks together? It's a brilliant proof of concept.

But when we started using it, we noticed a few things:

**It only did one thing.** Long-term investing. "Should I hold this stock for a year?" is a valid question, but most people watching charts also want to know: *should I trade this over the next week? Is there a day trade setup here today? What about crypto?*

**It required paid APIs.** Every analysis call went to OpenAI or Groq. That adds up fast, especially when you're running 14 agents across 10 tickers.

**There was no way to act on the output.** The system produced signals — but they just printed to the terminal and disappeared.

So we rebuilt it. Here's what changed:

### 1. Three new trading modes, each with its own team of agents

The original had one mode. We added three:

- **`/swing`** — nine specialized swing trading strategies analyze each ticker together. A Mean Reversion agent, a Breakout Trader, a Trend Follower, a Momentum Ranker, and five more each write an independent signal. A Head Swing Trader synthesizes all nine into a unified view. A Portfolio Manager makes the final call with a specific entry price, target, stop loss, and risk/reward ratio.

- **`/daytrade`** — same multi-agent structure, but built for intraday. Nine day-trade strategies (VWAP, Opening Range, Gap Analyst, Volume Profiler, etc.) debate the setup. Output is a concrete trade plan for the current session: entry trigger, targets, stop, time window.

- **`/crypto-swing` and `/crypto-day`** — the same pipeline adapted for crypto. Swapped out the fundamental agents (no SEC filings for Bitcoin) and added crypto-native signals: Fear & Greed Index, whale wallet movements, exchange funding rates, ETF flow data. Runs 24/7 with a simulated local exchange — no real account needed.

### 2. Rebuilt on Claude Code — zero cost, slash command interface

Instead of calling OpenAI's API, every agent runs as a **Claude Code subagent**. If you have Claude Code, you already have everything you need. No API keys, no usage bills, no rate limits to manage.

The interface is three slash commands: `/swing`, `/daytrade`, `/autorun`. Type one in Claude Code and the entire pipeline — data fetch, 9+ agent debates, synthesis, final decision, plain-English explanation — runs automatically.

### 3. Live web research built in

Before the agents analyze anything, a Web Research agent pulls the current macro picture and live news for each ticker using real web searches. Every agent decision is grounded in what's actually happening today — not just historical price data.

### 4. Paper trading to validate the signals

We added an optional Moomoo paper trading integration. After each run, `/autorun` places the model's recommended trades in a simulated account. Over time, this builds an accuracy log: how often does the model's entry get filled? How often does the target hit before the stop? This turns the system from a signal generator into something you can actually evaluate.

---

## What's new vs. the original

| | [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) | This repo |
|---|---|---|
| Interface | Python CLI | **Claude Code slash commands** |
| LLM cost | Paid APIs required | **Free** — Claude Code subagents |
| Trading modes | Long-term invest | Invest + **Swing + Day Trade + Crypto** |
| Paper trading | None | Optional Moomoo integration |
| Web research | None | Live news + macro context per ticker |
| Budget control | None | `--cash` flag, position limits |

---

## Agents

**Invest mode** — 14 legendary investor personas:

1. Aswath Damodaran — The Dean of Valuation
2. Ben Graham — Godfather of value investing, margin of safety
3. Bill Ackman — Activist investor, bold concentrated positions
4. Cathie Wood — Queen of growth investing, disruptive innovation
5. Charlie Munger — Wonderful businesses at fair prices
6. Michael Burry — The Big Short contrarian
7. Mohnish Pabrai — Dhandho investor, doubles at low risk
8. Nassim Taleb — Black Swan risk analyst, tail risk and antifragility
9. Peter Lynch — Practical investor seeking ten-baggers
10. Phil Fisher — Deep scuttlebutt growth research
11. Rakesh Jhunjhunwala — The Big Bull of India
12. Stanley Druckenmiller — Macro legend, asymmetric opportunities
13. Warren Buffett — Oracle of Omaha, wonderful companies at fair prices
14. Growth Agent — Quantitative growth metrics

**Swing mode** — 9 specialized strategies:
Trend Follower · Pullback Trader · Breakout Trader · Momentum Ranker · Mean Reversion · Catalyst Trader · Sector Rotation · Stanley Druckenmiller · News Sentiment

**Day trade mode** — 9 intraday strategies:
VWAP Trader · Momentum Scalper · Mean Reversion · Breakout Hunter · Gap Analyst · Volume Profiler · Pattern Reader · Stat Arb · News Catalyst

**Supporting agents** (all modes):
Fundamentals · Technicals · Valuation · Sentiment · Risk Manager · Portfolio Manager · Web Researcher · Web Verifier · Explainer

---

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results

By using this software, you agree to use it solely for learning purposes.

---

## Table of Contents
- [How to Install](#how-to-install)
- [How to Run](#how-to-run)
  - [Slash Commands](#slash-commands)
  - [Manual CLI](#manual-cli)
- [Optional: Paper Trading](#optional-paper-trading-moomoo)
- [How to Contribute](#how-to-contribute)
- [License](#license)

---

## How to Install

### 1. Prerequisites
- [Claude Code](https://claude.ai/code) CLI installed and authenticated
- Python 3.11+

### 2. Clone the repository

```bash
git clone https://github.com/NamanVinayak/claude-code-hedge-fund.git
cd claude-code-hedge-fund
```

### 3. Create a virtual environment and install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### 4. Optional API keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```bash
# Free tier at finnhub.io — improves news quality
FINNHUB_API_KEY=your-finnhub-key

# Free tier at coingecko.com — enables crypto sentiment agent
COINGECKO_API_KEY=your-coingecko-key
```

Both keys are optional. The system works without them using yfinance + SEC EDGAR.

---

## How to Run

### Slash Commands

Open Claude Code in this directory and use any of these commands:

#### `/swing AAPL,TSLA,NVDA`
Multi-day trade setups (2–20 day holds). Nine specialized swing strategies debate each ticker, a Head Trader synthesizes, a Portfolio Manager decides. Output: entry price, target, stop, risk/reward, position size.

#### `/daytrade SPY,QQQ,IWM`
Intraday trade plans for the current session. Nine day-trade strategies analyze each ticker. Output: setup type, entry trigger, targets, stop, time window.

#### `/autorun`
The full daily routine in one command: syncs open positions → runs the model → places paper orders → prints the accuracy dashboard. Schedule and tickers are configured in `tracker/watchlist.json`.

#### `/invest AAPL,MSFT`
Long-term portfolio decisions powered by 14 legendary investor personas. Output: buy/sell/hold with holding period and conviction.

#### `/research AAPL`
Comprehensive deep-dive using all 30+ agents. Output: bull/bear case, full signal grid, key risks and catalysts. No trade recommendation.

#### Crypto modes
```
/crypto-swing BTC-USD,ETH-USD,SOL-USD
/crypto-day BTC-USD,ETH-USD,SOL-USD
/crypto-autorun
```
Same pipeline with crypto-native agents: Fear & Greed Index, whale movements, funding rates, ETF flows, regulatory news. Simulated locally — no exchange account needed.

---

### Manual CLI

You can also run the pipeline directly from the terminal:

```bash
# Step 1: Fetch data and build facts bundles
python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id $(date +%Y%m%d_%H%M%S) --mode swing

# Step 2: Run agents (Claude Code handles this when using slash commands)

# Step 3: Aggregate signals + risk manager
python -m ai_hedge.runner.aggregate --run-id <id> --tickers AAPL,MSFT

# Step 4: Display results
python -m ai_hedge.runner.finalize --run-id <id>
```

---

## How It Works

```
/swing AAPL,MSFT,NVDA
  └─ prepare.py          fetch prices, financials, news (yfinance + SEC EDGAR + Finnhub)
  └─ web research        live macro context + ticker news per ticker (WebSearch)
  └─ 9 swing agents      each reads a facts bundle, writes a signal (run in parallel)
  └─ head trader         synthesizes 9 signals into a unified market view
  └─ aggregate.py        deterministic technicals, fundamentals, valuation, risk manager
  └─ portfolio manager   final entry / target / stop decisions with position sizing
  └─ explainer           plain-English educational breakdown of every signal
  └─ finalize.py         prints the results
```

All LLM calls use Claude Code's built-in Agent tool — **no OpenAI key, no Anthropic API key, no paid data provider.**

---

## Optional: Paper Trading (Moomoo)

Connect your own Moomoo account to have the system place paper trades automatically after each analysis run.

### Setup

1. Download [Moomoo OpenD](https://www.moomoo.com/download) — the local API gateway
2. Copy the config template:
   ```bash
   cp opend/OpenD.xml.example opend/OpenD.xml
   ```
3. Fill in your phone number and MD5 password hash in `opend/OpenD.xml`
4. Set your account ID as an environment variable:
   ```bash
   export MOOMOO_ACCOUNT_ID=your_account_id
   ```
5. Launch OpenD:
   ```bash
   open opend/OpenD.app
   ```

### Commands

```bash
python -m tracker execute --run-id RUN_ID    # place orders from a model run
python -m tracker monitor                     # sync fills, manage stops/targets
python -m tracker report                      # accuracy dashboard
python -m tracker status                      # open positions and P&L
python -m tracker cash                        # available capital
```

---

## Project Structure

```
ai_hedge/
  data/             yfinance, SEC EDGAR, Finnhub providers + indicators
  personas/         investor agents, swing/daytrade strategies, prompt files
  deterministic/    fundamentals, technicals, valuation, sentiment, risk manager
  runner/           prepare, aggregate, finalize scripts
tracker/            Moomoo paper trading integration (optional)
crypto_tracker/     crypto simulated trading (optional)
.claude/skills/     slash command definitions (/swing, /daytrade, /autorun, etc.)
```

---

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please keep pull requests small and focused.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
