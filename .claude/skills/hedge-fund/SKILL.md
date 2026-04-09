---
name: hedge-fund
description: Run AI hedge fund analysis. Supports invest, swing, day-trade, and research modes.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: [--mode invest|swing|daytrade|research] TICKER1[,TICKER2,...]
---

# AI Hedge Fund Skill

Parse `$ARGUMENTS` for an optional `--mode` flag and ticker list. Default mode is `invest`.

Examples:
- `AAPL,MSFT` → invest mode, tickers AAPL and MSFT
- `--mode swing TSLA` → swing mode, ticker TSLA
- `--mode research NVDA,AMD` → research mode, tickers NVDA and AMD

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS`:
- If `--mode` flag is present, extract the mode (invest|swing|daytrade|research). Otherwise default to `invest`.
- Everything else is the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.

Set variables: `MODE`, `TICKERS`, `RUN_ID`.

## Step 2 — Fetch data and build facts

```bash
.venv/bin/python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode $MODE
```

This fetches all raw data, saves metadata.json, builds invest persona facts, and conditionally builds swing/daytrade facts based on mode.

## Step 3 — Dispatch LLM subagents in parallel

Send ALL agents for the mode as Agent tool calls **in a single message** (maximum parallelism).

### If MODE is `invest`: dispatch 14 agents

Agents: `warren_buffett`, `charlie_munger`, `ben_graham`, `bill_ackman`, `cathie_wood`, `michael_burry`, `nassim_taleb`, `peter_lynch`, `phil_fisher`, `stanley_druckenmiller`, `mohnish_pabrai`, `rakesh_jhunjhunwala`, `aswath_damodaran`, `news_sentiment`

(`growth_analyst_agent` is already computed deterministically in Step 2 — do NOT dispatch it.)

Use this prompt template for each `{AGENT}`:

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

### If MODE is `swing`: dispatch 9 agents

Agents: `swing_trend_follower`, `swing_pullback_trader`, `swing_breakout_trader`, `swing_momentum_ranker`, `swing_mean_reversion`, `swing_catalyst_trader`, `swing_sector_rotation`, `stanley_druckenmiller`, `news_sentiment`

Use this prompt template for each `{AGENT}`:

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

### If MODE is `daytrade`: dispatch 9 agents

Agents: `dt_vwap_trader`, `dt_momentum_scalper`, `dt_mean_reversion`, `dt_breakout_hunter`, `dt_gap_analyst`, `dt_volume_profiler`, `dt_pattern_reader`, `dt_stat_arb`, `dt_news_catalyst`

Use this prompt template for each `{AGENT}`:

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

### If MODE is `research`: dispatch ALL agents (30+)

Dispatch all 14 invest agents + all 9 swing agents + all 9 daytrade agents in a single message.
Use the invest template for invest agents, swing template for swing agents, daytrade template for daytrade agents.

Note: `stanley_druckenmiller` and `news_sentiment` appear in both invest and swing lists. Only dispatch each once (use the invest template — their facts file is the same).

Total unique agents for research: 14 (invest) + 7 (swing-only) + 9 (daytrade) = 30.

## Step 4 — Head Trader synthesis (swing and daytrade only)

Skip this step for `invest` and `research` modes.

### If MODE is `swing`: dispatch Head Swing Trader

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

### If MODE is `daytrade`: dispatch Head Day Trader

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
.venv/bin/python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash 100000
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager — and technicals_intraday for daytrade/research), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch final agent

Based on MODE, dispatch **one** Agent tool call:

### If MODE is `invest`: Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/portfolio_manager.md

You are the Portfolio Manager. Make final trading decisions for each ticker in [{TICKERS}] based on:
- analyst_signals: 14 LLM persona signals + growth_analyst_agent (deterministic) + 5 deterministic agents
- allowed_actions: what actions are physically possible given current portfolio limits

Return JSON in this exact format:
{{
  "decisions": {{
    "TICKER1": {{"action": "buy|sell|short|cover|hold", "quantity": 123, "confidence": 75, "reasoning": "..."}},
    "TICKER2": ...
  }},
  "duration": "recommended portfolio holding period"
}}

Write the output to: runs/{RUN_ID}/decisions.json
```

### If MODE is `swing`: Swing Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/swing_portfolio_manager.md

You are the Swing Portfolio Manager. Make swing trade decisions for each ticker in [{TICKERS}].
Consider the Head Swing Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe and an overall synthesis.

Write the output to: runs/{RUN_ID}/decisions.json
```

### If MODE is `daytrade`: Day Trade Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/dt_portfolio_manager.md

You are the Day Trade Portfolio Manager. Make intraday trade decisions for each ticker in [{TICKERS}].
Consider the Head Day Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs (including intraday technicals).

Return JSON with per-ticker setup/entry-trigger/targets/stop/position-size/time-window and an overall synthesis.

Write the output to: runs/{RUN_ID}/decisions.json
```

### If MODE is `research`: Research Report Writer

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

## Step 7 — Display results

```bash
.venv/bin/python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This reads mode from `metadata.json` and displays mode-appropriate output:
- **invest**: Action/quantity/confidence, analyst breakdown, holding periods, portfolio summary
- **swing**: Entry/target/stop/risk-reward/timeframe, Head Trader synthesis, strategy breakdown
- **daytrade**: Setup/entry-trigger/targets/stop/position-size/time-window, Head Trader synthesis
- **research**: Bull case, bear case, key metrics, risk factors, sentiment distribution, full agent signal grid
