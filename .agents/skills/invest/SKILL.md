---
name: invest
description: Analyze stocks using 14 legendary investor personas (Buffett, Munger, Graham, etc.). Long-term portfolio decisions.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: TICKER1[,TICKER2,...]
---

# Invest Mode — AI Hedge Fund

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
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode invest
```

This fetches all raw data, saves metadata.json, and builds invest persona facts.

## Step 2.5 — Web Research Agent

Dispatch one Agent tool call **per ticker** (can be parallel if multiple tickers), using `model: sonnet`:

```
You are the Web Research Agent.

1. Read your system prompt from: ai_hedge/personas/prompts/web_researcher.md
2. For ticker {TICKER}, use WebSearch to research:
   - Current macro market conditions (search: "stock market news today", "Federal Reserve latest decision", "geopolitical news affecting stock market")
   - Ticker-specific news (search: "{TICKER} news this week", "{TICKER} analyst rating upgrade downgrade")
   - Analyst consensus (search: "{TICKER} price target analyst consensus")
   - Earnings info (search: "{TICKER} next earnings date estimate")
   - Competitor activity (search: "{TICKER} competitors news")
3. Write your research to: runs/{RUN_ID}/web_research/{TICKER}.json

Follow the JSON format in your system prompt exactly.
```

After web research completes for all tickers, rebuild facts to include web context:
```bash
python -m ai_hedge.personas.facts_builder --run-id $RUN_ID --tickers $TICKERS
```

## Step 2.8 — Web Verification Agent

Dispatch **one** Agent tool call (covers all tickers), using `model: sonnet`:

```
You are the Data Verification Agent.

1. Read your system prompt from: ai_hedge/personas/prompts/web_verifier.md
2. For each ticker in [{TICKERS}]:
   - Read facts bundles from runs/{RUN_ID}/facts/ (check 2-3 persona files per ticker)
   - Extract key metrics: net_margin, operating_margin, pe_ratio, revenue, market_cap
   - Use WebSearch to verify each metric (search: "{TICKER} net margin TTM", "{TICKER} PE ratio")
   - If any metric deviates >20% from web data, update ALL facts bundles for that ticker
3. Write verification report to: runs/{RUN_ID}/verification/{TICKER}.json for each ticker
```

## Step 3 — Dispatch 14 LLM subagents in batches of 4

Dispatch agents **in batches of 4** using `model: sonnet`. Send 4 Agent tool calls in a SINGLE message, wait for all 4 to complete, then send the next batch.

(`growth_analyst_agent` is already computed deterministically in Step 2 — do NOT dispatch it.)

**Batch 1** (send all 4 in one message, wait for completion):
- `warren_buffett`
- `charlie_munger`
- `ben_graham`
- `bill_ackman`

**Batch 2**:
- `cathie_wood`
- `michael_burry`
- `nassim_taleb`
- `peter_lynch`

**Batch 3**:
- `phil_fisher`
- `stanley_druckenmiller`
- `mohnish_pabrai`
- `rakesh_jhunjhunwala`

**Batch 4**:
- `aswath_damodaran`
- `news_sentiment`

For each agent, use this prompt template for `{AGENT}`:

```
You are the {AGENT} investor agent.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   The facts include financial data AND a "web_context" section with current market conditions and news. Use both in your analysis.

Analyze each ticker using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."}},
  "TICKER2": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "holding_period": "..."}}
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json

Use exactly the schema from ai_hedge/schemas.py for this persona.
```

After ALL 14 agents complete, proceed to Step 4.

## Step 4 — Aggregate signals

Parse `$ARGUMENTS` for an optional `--cash` flag. If present, use that value. Otherwise default to 100000.

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash $CASH --require-turso
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager), computes allowed actions, and writes `signals_combined.json`.

## Step 5 — Dispatch Portfolio Manager

Dispatch **one** Agent tool call (model: sonnet):

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

## Step 6 — Explainer Agent

Dispatch **one** Agent tool call (model: sonnet) to produce a plain-English educational explanation:

```
You are a Financial Explainer agent.

1. Read your system prompt from: ai_hedge/personas/prompts/explainer.md
2. Read the mode from: runs/{RUN_ID}/metadata.json
3. Read the final decisions from: runs/{RUN_ID}/decisions.json
4. Read all signals from: runs/{RUN_ID}/signals_combined.json

The mode is: invest
The tickers are: [{TICKERS}]

Produce a layered educational explanation following the prompt exactly.
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

## Step 7 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: action/quantity/confidence, analyst breakdown, holding periods, portfolio summary.
