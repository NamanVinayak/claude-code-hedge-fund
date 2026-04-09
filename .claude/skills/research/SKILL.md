---
name: research
description: Comprehensive stock research using 30+ AI agents. Bull case, bear case, key metrics, risk factors. No trade recommendation.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: TICKER1[,TICKER2,...]
---

# Research Mode — AI Hedge Fund

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS` as the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.

Set variables: `TICKERS`, `RUN_ID`.

## Step 2 — Fetch data and build facts

```bash
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode research
```

This fetches all raw data, saves metadata.json, and builds ALL facts (invest, swing, and daytrade).

## Step 3 — Dispatch ALL 30 LLM subagents in 9 batches

Dispatch agents **in batches of 4**. Send 4 Agent tool calls in a SINGLE message, wait for all 4 to complete, then send the next batch.

Use the invest template for invest agents, swing template for swing agents, daytrade template for daytrade agents.

Note: `stanley_druckenmiller` and `news_sentiment` appear in both invest and swing lists. Only dispatch each once (in invest batches — their facts file is the same). Do NOT dispatch them again in swing batches.

**Batch 1** (invest — send all 4 in one message, wait for completion):
- `warren_buffett`
- `charlie_munger`
- `ben_graham`
- `bill_ackman`

**Batch 2** (invest):
- `cathie_wood`
- `michael_burry`
- `nassim_taleb`
- `peter_lynch`

**Batch 3** (invest):
- `phil_fisher`
- `stanley_druckenmiller`
- `mohnish_pabrai`
- `rakesh_jhunjhunwala`

**Batch 4** (invest):
- `aswath_damodaran`
- `news_sentiment`

**Batch 5** (swing):
- `swing_trend_follower`
- `swing_pullback_trader`
- `swing_breakout_trader`
- `swing_momentum_ranker`

**Batch 6** (swing):
- `swing_mean_reversion`
- `swing_catalyst_trader`
- `swing_sector_rotation`

**Batch 7** (daytrade):
- `dt_vwap_trader`
- `dt_momentum_scalper`
- `dt_mean_reversion`
- `dt_breakout_hunter`

**Batch 8** (daytrade):
- `dt_gap_analyst`
- `dt_volume_profiler`
- `dt_pattern_reader`
- `dt_stat_arb`

**Batch 9** (daytrade):
- `dt_news_catalyst`

### Invest agent prompt template (for Batches 1-4):

```
You are the {AGENT} investor agent.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json

Analyze each ticker using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."}},
  "TICKER2": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."}}
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json

Use exactly the schema from ai_hedge/schemas.py for this persona.
```

### Swing agent prompt template (for Batches 5-6):

```
You are the {AGENT} swing trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json

Analyze each ticker for swing trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry": float, "target": float, "stop": float, "timeframe": "..."}},
  "TICKER2": ...
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json
```

### Daytrade agent prompt template (for Batches 7-9):

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

After ALL 30 agents complete, proceed to Step 4 (skip Head Trader — go straight to aggregate).

## Step 4 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash 100000
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager, technicals_intraday), computes allowed actions, and writes `signals_combined.json`.

## Step 5 — Dispatch Research Report Writer

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/research_report_writer.md

You are the Research Report Writer. Compile a comprehensive research report for [{TICKERS}] using ALL agent signals (30+ agents from invest, swing, and daytrade modes plus deterministic agents).

Organize into: bull case, bear case, key metrics, risk factors, sentiment distribution.
Do NOT make a trading recommendation — this is research, not advice.

Return JSON:
{{
  "bull_case": [{{"agent": "...", "signal": "bullish", "confidence": int, "reasoning": "..."}}],
  "bear_case": [{{"agent": "...", "signal": "bearish", "confidence": int, "reasoning": "..."}}],
  "key_metrics": {{"metric": "value"}},
  "risk_factors": ["..."],
  "sentiment_distribution": {{"bullish": int, "bearish": int, "neutral": int}}
}}

Write the output to: runs/{RUN_ID}/decisions.json
```

## Step 6 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: bull case, bear case, key metrics, risk factors, sentiment distribution, full agent signal grid.
