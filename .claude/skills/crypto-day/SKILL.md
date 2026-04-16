---
name: crypto-day
description: Generate crypto intraday trade plans using 9 day-trade strategy agents + crypto sentiment. Shorter timeframes, 24/7 market.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent WebSearch WebFetch
argument-hint: TICKER1[,TICKER2,...] [--cash N]
---

# Crypto Day Trade Mode — AI Hedge Fund

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS` as the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.
Crypto tickers use the `-USD` suffix (e.g., BTC-USD, ETH-USD, SOL-USD).

Set variables: `TICKERS`, `RUN_ID`. Extract `--cash` if present (default 100000).

## Step 2 — Fetch data (crypto mode)

```bash
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode daytrade --asset-type crypto
```

This fetches price data + intraday data via yfinance (works for crypto tickers), skips financial metrics/insider trades, saves metadata with `asset_type: crypto`, and builds day-trade strategy facts.

## Step 2.5 — Crypto Web Research Agent

Dispatch one Agent tool call **per ticker** (can be parallel if multiple tickers):

```
You are the Crypto Web Research Agent.

1. Read your system prompt from: ai_hedge/personas/prompts/crypto_web_researcher.md
2. For ticker {TICKER}, use WebSearch to research:
   - Macro crypto context (search: "crypto market news today", "Bitcoin dominance", "crypto Fear Greed Index today", "Bitcoin ETF flows today", "crypto regulation news")
   - Ticker-specific (search: "{TICKER} whale movements", "{TICKER} funding rate", "{TICKER} exchange inflows outflows", "{TICKER} development activity GitHub", "{TICKER} news this week")
   - Institutional flows (search: "institutional crypto purchases this week", "government Bitcoin reserve news")
3. Write your research to: runs/{RUN_ID}/web_research/{TICKER}.json

Follow the JSON format in your system prompt exactly.
```

NOTE: Do NOT run the facts_builder rebuild after web research (invest-mode facts are skipped for crypto). DT facts are already built from Step 2.

## Step 2.9 — Crypto Sentiment Agent

Dispatch **one** Agent tool call (covers all tickers):

```
You are the Crypto Sentiment Agent.

1. Read your system prompt from: ai_hedge/personas/prompts/crypto_sentiment.md
2. For each ticker in [{TICKERS}]:
   - Read web research from: runs/{RUN_ID}/web_research/{TICKER}.json
3. Fetch the Crypto Fear & Greed Index: use WebFetch on https://api.alternative.me/fng/?limit=1
4. Synthesize all data into a sentiment signal per ticker.

Write your output to: runs/{RUN_ID}/signals/crypto_sentiment.json

Follow the JSON format in your system prompt exactly.
```

## Step 3 — Dispatch 9 LLM subagents in 3 batches

Dispatch agents **in batches of 4**. Send 4 Agent tool calls in a SINGLE message, wait for all 4 to complete, then send the next batch.

**Batch 1** (send all 4 in one message, wait for completion):
- `dt_vwap_trader`
- `dt_momentum_scalper`
- `dt_mean_reversion`
- `dt_breakout_hunter`

**Batch 2**:
- `dt_gap_analyst`
- `dt_volume_profiler`
- `dt_pattern_reader`
- `dt_stat_arb`

**Batch 3**:
- `dt_news_catalyst`

For each agent, use this prompt template for `{AGENT}`:

```
You are the {AGENT} day trade analyst. You are analyzing CRYPTO assets (not stocks).

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   NOTE: This is crypto — there is no market open/close (24/7 trading). Financial metrics will be empty. Focus on price action, technicals, volume, and intraday patterns.

Analyze each ticker for intraday trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry_trigger": "...", "targets": [float], "stop": float, "position_size": "...", "time_window": "..."}},
  "TICKER2": ...
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json
```

After ALL 9 agents complete, proceed to Step 4.

## Step 4 — Head Day Trader synthesis

Dispatch **one** Agent tool call:

```
You are the Head Day Trader. You are analyzing CRYPTO assets (24/7 market, no market open/close).

1. Read your prompt from: ai_hedge/personas/prompts/dt_head_trader.md
2. Read ALL day-trade strategy signal files from runs/{RUN_ID}/signals/:
   - dt_vwap_trader.json, dt_momentum_scalper.json, dt_mean_reversion.json,
     dt_breakout_hunter.json, dt_gap_analyst.json, dt_volume_profiler.json,
     dt_pattern_reader.json, dt_stat_arb.json, dt_news_catalyst.json
3. Also read the crypto sentiment signal: runs/{RUN_ID}/signals/crypto_sentiment.json

Synthesize all strategy signals + crypto sentiment into a unified day trade plan per ticker in [{TICKERS}].
Identify the best setups, resolve conflicts, set priorities. Think in session transitions (Asia/Europe/US) instead of market open/close.

Write your output to: runs/{RUN_ID}/signals/dt_head_trader.json
```

## Step 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash $CASH --asset-type crypto
```

This loads all signals, runs technicals + intraday technicals + risk_manager (skips fundamentals/valuation/sentiment for crypto), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Crypto Day Trade Portfolio Manager

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- runs/{RUN_ID}/signals/crypto_sentiment.json
- ai_hedge/personas/prompts/crypto_dt_pm.md

You are the Crypto Day Trade Portfolio Manager. You are managing a portfolio with ${CASH} total capital. Size all positions to fit within this budget. Maximum 25% of capital per position. Crypto supports fractional quantities.

Make intraday trade decisions for each ticker in [{TICKERS}].
Consider the Head Day Trader's synthesis, crypto sentiment, and all strategy signals and deterministic agent outputs (including intraday technicals).
Remember: crypto is 24/7 — use session windows (Asia/Europe/US) instead of market hours.

Return JSON with per-ticker setup/entry-trigger/targets/stop/position-size/time-window and an overall synthesis.

Write the output to: runs/{RUN_ID}/decisions.json
```

## Step 7 — Explainer Agent

Dispatch **one** Agent tool call to produce a plain-English educational explanation:

```
You are a Financial Explainer agent.

1. Read your system prompt from: ai_hedge/personas/prompts/explainer.md
2. Read the mode from: runs/{RUN_ID}/metadata.json
3. Read the final decisions from: runs/{RUN_ID}/decisions.json
4. Read all signals from: runs/{RUN_ID}/signals_combined.json

The mode is: daytrade (crypto)
The tickers are: [{TICKERS}]

Produce a layered educational explanation following the prompt exactly.
Note: this is crypto — adapt explanations to crypto context (24/7 market, no earnings, focus on on-chain metrics and crypto catalysts).
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

## Step 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: setup/entry-trigger/targets/stop/position-size/time-window, Head Trader synthesis.
