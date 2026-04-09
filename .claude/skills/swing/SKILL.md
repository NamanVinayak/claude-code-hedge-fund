---
name: swing
description: Find swing trade setups using 9 strategy agents (trend, breakout, mean reversion, etc.). 2-20 day trades with entry/target/stop.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: TICKER1[,TICKER2,...]
---

# Swing Mode — AI Hedge Fund

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS` as the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.

Set variables: `TICKERS`, `RUN_ID`.

## Step 2 — Fetch data and build facts

```bash
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode swing
```

This fetches all raw data, saves metadata.json, and builds swing strategy facts.

## Step 3 — Dispatch 9 LLM subagents in 3 batches

Dispatch agents **in batches of 4**. Send 4 Agent tool calls in a SINGLE message, wait for all 4 to complete, then send the next batch.

**Batch 1** (send all 4 in one message, wait for completion):
- `swing_trend_follower`
- `swing_pullback_trader`
- `swing_breakout_trader`
- `swing_momentum_ranker`

**Batch 2**:
- `swing_mean_reversion`
- `swing_catalyst_trader`
- `swing_sector_rotation`
- `stanley_druckenmiller`

**Batch 3**:
- `news_sentiment`

For each agent, use this prompt template for `{AGENT}`:

```
You are the {AGENT} swing trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   (For stanley_druckenmiller and news_sentiment, the facts file uses the invest-mode name.)

Analyze each ticker for swing trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry": float, "target": float, "stop": float, "timeframe": "..."}},
  "TICKER2": ...
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json
```

After ALL 9 agents complete, proceed to Step 4.

## Step 4 — Head Swing Trader synthesis

Dispatch **one** Agent tool call:

```
You are the Head Swing Trader.

1. Read your prompt from: ai_hedge/personas/prompts/swing_head_trader.md
2. Read ALL swing strategy signal files from runs/{RUN_ID}/signals/:
   - swing_trend_follower.json, swing_pullback_trader.json, swing_breakout_trader.json,
     swing_momentum_ranker.json, swing_mean_reversion.json, swing_catalyst_trader.json,
     swing_sector_rotation.json, stanley_druckenmiller.json, news_sentiment.json

Synthesize all strategy signals into a unified swing trade assessment per ticker in [{TICKERS}].
Resolve conflicting signals, identify highest-conviction setups, note risk factors.

Write your output to: runs/{RUN_ID}/signals/swing_head_trader.json
```

## Step 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash 100000
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Swing Portfolio Manager

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/swing_portfolio_manager.md

You are the Swing Portfolio Manager. Make swing trade decisions for each ticker in [{TICKERS}].
Consider the Head Swing Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe and an overall synthesis.

Write the output to: runs/{RUN_ID}/decisions.json
```

## Step 7 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: entry/target/stop/risk-reward/timeframe, Head Trader synthesis, strategy breakdown.
