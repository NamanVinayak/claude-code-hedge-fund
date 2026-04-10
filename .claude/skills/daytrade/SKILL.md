---
name: daytrade
description: Generate intraday trade plans using 9 day-trade strategy agents (VWAP, momentum, breakout, etc.). Close positions by end of day.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: TICKER1[,TICKER2,...]
---

# Day Trade Mode — AI Hedge Fund

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS` as the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.

Set variables: `TICKERS`, `RUN_ID`.

## Step 2 — Check environment and fetch data

First check if the package is installed:
```bash
python -c "import ai_hedge" 2>/dev/null || echo "ERROR: ai-hedge-fund not installed. Run: pip install ai-hedge-fund"
```

Check for optional Finnhub key and inform user:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('FINNHUB_API_KEY',''); print('Finnhub API key: configured' if key else 'Note: No FINNHUB_API_KEY found. Insider trades and news data will be unavailable. Get a free key at finnhub.io and add FINNHUB_API_KEY=your_key to .env')"
```

Fetch data:
```bash
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode daytrade
```

This fetches all raw data, saves metadata.json, and builds day-trade strategy facts + intraday data.

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
You are the {AGENT} day trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json

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
You are the Head Day Trader.

1. Read your prompt from: ai_hedge/personas/prompts/dt_head_trader.md
2. Read ALL day-trade strategy signal files from runs/{RUN_ID}/signals/:
   - dt_vwap_trader.json, dt_momentum_scalper.json, dt_mean_reversion.json,
     dt_breakout_hunter.json, dt_gap_analyst.json, dt_volume_profiler.json,
     dt_pattern_reader.json, dt_stat_arb.json, dt_news_catalyst.json

Synthesize all strategy signals into a unified day trade plan per ticker in [{TICKERS}].
Identify the best setups, resolve conflicts, set priorities for the trading session.

Write your output to: runs/{RUN_ID}/signals/dt_head_trader.json
```

## Step 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash 100000
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager, technicals_intraday), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Day Trade Portfolio Manager

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/dt_portfolio_manager.md

You are the Day Trade Portfolio Manager. Make intraday trade decisions for each ticker in [{TICKERS}].
Consider the Head Day Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs (including intraday technicals).

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

The mode is: daytrade
The tickers are: [{TICKERS}]

Produce a layered educational explanation following the prompt exactly.
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

## Step 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: setup/entry-trigger/targets/stop/position-size/time-window, Head Trader synthesis.
