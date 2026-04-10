# AI Hedge Fund — Run Playbook

When the user says **"run the hedge fund on TICKER1,TICKER2"**, execute the steps below in order.
The `--mode` flag determines which agents to dispatch.

**Modes:** `invest` (default) | `swing` | `daytrade` | `research`

---

## STEP 1 — Generate a run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
echo "Run ID: $RUN_ID"
```

---

## STEP 2 — Fetch raw data + build facts bundles

```bash
python -m ai_hedge.runner.prepare --tickers TICKER1,TICKER2 --run-id $RUN_ID --mode MODE
```

This command:
1. Fetches all raw financial data → `runs/$RUN_ID/raw/<TICKER>.json`
2. Saves metadata → `runs/$RUN_ID/metadata.json`
3. Builds invest persona facts → `runs/$RUN_ID/facts/<persona>__<ticker>.json`
4. Writes `runs/$RUN_ID/signals/growth_analyst_agent.json` (fully deterministic)
5. If `--mode swing` or `--mode research`: also builds swing strategy facts
6. If `--mode daytrade` or `--mode research`: also builds day-trade strategy facts + fetches intraday data

---

## STEP 3 — Dispatch LLM subagents in batches of 4

Dispatch agents **in batches of 4**. Send 4 Agent tool calls in a SINGLE message, wait for all 4 to complete, then send the next batch. Which agents to dispatch depends on mode:

### Invest mode (14 agents, 4 batches)

`growth_analyst_agent` is skipped — already computed deterministically in Step 2.

**Batch 1** (send all 4 in one message, wait for completion):
`warren_buffett`, `charlie_munger`, `ben_graham`, `bill_ackman`

**Batch 2**:
`cathie_wood`, `michael_burry`, `nassim_taleb`, `peter_lynch`

**Batch 3**:
`phil_fisher`, `stanley_druckenmiller`, `mohnish_pabrai`, `rakesh_jhunjhunwala`

**Batch 4**:
`aswath_damodaran`, `news_sentiment`

Prompt template for each persona:

```
You are the {PERSONA} investor agent.

1. Read your system prompt from: ai_hedge/personas/prompts/{PERSONA}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{PERSONA}__{TICKER}.json

Analyze each ticker using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{
  "TICKER1": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."},
  "TICKER2": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."}
}

Write your output to: runs/{RUN_ID}/signals/{PERSONA}.json

Use exactly the schema from ai_hedge/schemas.py for this persona.
```

### Swing mode (9 agents, 3 batches)

**Batch 1** (send all 4 in one message, wait for completion):
`swing_trend_follower`, `swing_pullback_trader`, `swing_breakout_trader`, `swing_momentum_ranker`

**Batch 2**:
`swing_mean_reversion`, `swing_catalyst_trader`, `swing_sector_rotation`, `stanley_druckenmiller`

**Batch 3**:
`news_sentiment`

Prompt template for each strategy:

```
You are the {STRATEGY} swing trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{STRATEGY}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{STRATEGY}__{TICKER}.json

Analyze each ticker for swing trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{
  "TICKER1": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry": float, "target": float, "stop": float, "timeframe": "..."},
  "TICKER2": ...
}

Write your output to: runs/{RUN_ID}/signals/{STRATEGY}.json
```

### Day-trade mode (9 agents, 3 batches)

**Batch 1** (send all 4 in one message, wait for completion):
`dt_vwap_trader`, `dt_momentum_scalper`, `dt_mean_reversion`, `dt_breakout_hunter`

**Batch 2**:
`dt_gap_analyst`, `dt_volume_profiler`, `dt_pattern_reader`, `dt_stat_arb`

**Batch 3**:
`dt_news_catalyst`

Prompt template for each strategy:

```
You are the {STRATEGY} day trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{STRATEGY}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{STRATEGY}__{TICKER}.json

Analyze each ticker for intraday trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{
  "TICKER1": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry_trigger": "...", "targets": [float], "stop": float, "position_size": "...", "time_window": "..."},
  "TICKER2": ...
}

Write your output to: runs/{RUN_ID}/signals/{STRATEGY}.json
```

### Research mode (30 agents, 9 batches)

Dispatch ALL agents from invest + swing + daytrade modes in batches of 4. All 14 invest personas + 7 swing-only strategies + 9 day-trade strategies (30 total). `stanley_druckenmiller` and `news_sentiment` appear in both invest and swing — dispatch each once only (in invest batches).

**Batches 1-4**: Same as invest mode batches above.
**Batch 5**: `swing_trend_follower`, `swing_pullback_trader`, `swing_breakout_trader`, `swing_momentum_ranker`
**Batch 6**: `swing_mean_reversion`, `swing_catalyst_trader`, `swing_sector_rotation`
**Batch 7**: `dt_vwap_trader`, `dt_momentum_scalper`, `dt_mean_reversion`, `dt_breakout_hunter`
**Batch 8**: `dt_gap_analyst`, `dt_volume_profiler`, `dt_pattern_reader`, `dt_stat_arb`
**Batch 9**: `dt_news_catalyst`

---

## STEP 4 — Head Trader synthesis (swing and daytrade modes only)

Skip this step for `invest` and `research` modes.

For **swing** mode, dispatch one Head Trader agent:

```
You are the Head Swing Trader. Read all swing strategy signals from runs/{RUN_ID}/signals/.
Read the prompt from ai_hedge/personas/prompts/swing_head_trader.md.

Synthesize all strategy signals into a unified swing trade plan per ticker.

Write output to: runs/{RUN_ID}/signals/swing_head_trader.json
```

For **daytrade** mode, dispatch one Head Day Trader agent:

```
You are the Head Day Trader. Read all day-trade strategy signals from runs/{RUN_ID}/signals/.
Read the prompt from ai_hedge/personas/prompts/dt_head_trader.md.

Synthesize all strategy signals into a unified day trade plan per ticker.

Write output to: runs/{RUN_ID}/signals/dt_head_trader.json
```

---

## STEP 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers TICKER1,TICKER2 --cash 100000
```

- Loads all persona/strategy signals from `runs/$RUN_ID/signals/*.json`
- Runs deterministic agents: fundamentals, technicals, valuation, sentiment, risk_manager (all modes)
- If daytrade or research mode: also runs `technicals_intraday`
- Computes allowed actions given portfolio limits
- Writes `runs/$RUN_ID/signals_combined.json`

Optional flags:
- `--cash 250000` — starting cash
- `--margin-requirement 0.5` — margin requirement
- `--mode MODE` — override the mode from metadata.json

---

## STEP 6 — Final agent

Dispatch **one** Agent tool call based on mode:

### Invest → Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/portfolio_manager.md

Make final trading decisions for each ticker in {TICKERS} based on:
- analyst_signals: 14 LLM persona signals + growth_analyst_agent + 5 deterministic agents
- allowed_actions: what actions are physically possible given current portfolio limits

Return JSON in this exact format:
{
  "decisions": {
    "TICKER1": {"action": "buy|sell|short|cover|hold", "quantity": 123, "confidence": 75, "reasoning": "..."},
    "TICKER2": ...
  },
  "duration": "recommended portfolio holding period"
}

Write the output to: runs/{RUN_ID}/decisions.json
```

### Swing → Swing Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/swing_portfolio_manager.md

Make swing trade decisions for each ticker in {TICKERS}.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe.

Write the output to: runs/{RUN_ID}/decisions.json
```

### Day-trade → Day Trade Portfolio Manager

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/dt_portfolio_manager.md

Make day trade decisions for each ticker in {TICKERS}.

Return JSON with per-ticker setup/entry-trigger/targets/stop/position-size/time-window.

Write the output to: runs/{RUN_ID}/decisions.json
```

### Research → Research Report Writer

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/research_report_writer.md

Compile a comprehensive research report across ALL agent signals.

Return JSON with bull_case, bear_case, key_metrics, risk_factors, sentiment_distribution.

Write the output to: runs/{RUN_ID}/decisions.json
```

---

## STEP 7 — Explainer Agent (all modes)

Dispatch **one** Agent tool call to produce a plain-English educational explanation:

```
You are a Financial Explainer agent.

1. Read your system prompt from: ai_hedge/personas/prompts/explainer.md
2. Read the mode from: runs/{RUN_ID}/metadata.json
3. Read the final decisions from: runs/{RUN_ID}/decisions.json
4. Read all signals from: runs/{RUN_ID}/signals_combined.json

The mode is: {MODE}
The tickers are: {TICKERS}

Produce a layered educational explanation following the prompt exactly.
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

This step runs for ALL modes. The explainer adapts its output based on the mode.

---

## STEP 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

Output varies by mode:
- **invest**: Action/quantity/confidence per ticker, analyst breakdown, portfolio summary, holding periods
- **swing**: Entry/target/stop/risk-reward/timeframe per ticker, Head Trader synthesis, strategy breakdown
- **daytrade**: Setup/entry-trigger/targets/stop/position-size/time-window per ticker, Head Trader synthesis
- **research**: Bull case, bear case, key metrics, risk factors, sentiment distribution, full agent signal grid

---

## Example commands

```bash
# Invest mode (default) — long-term portfolio decisions
python -m ai_hedge.runner.prepare --tickers AAPL,MSFT --run-id $RUN_ID --mode invest

# Swing mode — multi-day trade setups
python -m ai_hedge.runner.prepare --tickers AAPL,TSLA --run-id $RUN_ID --mode swing

# Day-trade mode — intraday trade plans
python -m ai_hedge.runner.prepare --tickers SPY,QQQ --run-id $RUN_ID --mode daytrade

# Research mode — comprehensive analysis using all 30+ agents
python -m ai_hedge.runner.prepare --tickers NVDA --run-id $RUN_ID --mode research
```

---

## Directory layout after a full run (research mode)

```
runs/
└── 20240101_120000/
    ├── metadata.json                  ← mode, tickers, dates
    ├── raw/
    │   ├── AAPL.json
    │   └── MSFT.json
    ├── facts/
    │   ├── warren_buffett__AAPL.json   ← invest persona facts
    │   ├── swing_trend_follower__AAPL.json ← swing strategy facts
    │   ├── dt_vwap_trader__AAPL.json    ← day-trade strategy facts
    │   └── ...
    ├── signals/
    │   ├── growth_analyst_agent.json   ← deterministic (from prepare)
    │   ├── warren_buffett.json         ← invest persona signals
    │   ├── swing_trend_follower.json    ← swing strategy signals
    │   ├── dt_vwap_trader.json         ← day-trade strategy signals
    │   └── ...
    ├── signals_combined.json           ← all signals + deterministic agents
    └── decisions.json                  ← final output
```
