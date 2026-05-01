---
name: swing
description: Find swing trade setups using 5 strategy agents (trend+momentum, mean reversion, breakout, catalyst+news, macro context). 2-20 day trades with entry/target/stop.
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
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode swing
```

This fetches all raw data, saves metadata.json, and builds swing strategy facts.

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

## Step 3 — Dispatch all 5 LLM subagents in ONE parallel batch

Dispatch all 5 agents in a **single message** using `model: sonnet`, wait for all 5 to complete, then proceed to Step 4.

The 5 agents are:
- `swing_trend_momentum` — with-the-trend continuation
- `swing_mean_reversion` — counter-extension (fade extremes OR buy dips at Fib)
- `swing_breakout` — regime-change / volatility expansion
- `swing_catalyst_news` — external triggers (events, news, insiders)
- `swing_macro_context` — top-down macro + relative strength + asymmetric R/R

For each agent, use this prompt template for `{AGENT}`:

```
You are the {AGENT} swing trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   The facts include financial data AND a "web_context" section with current market conditions and news. Use both in your analysis.

Analyze each ticker for swing trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{{
  "TICKER1": {{"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry": float, "target": float, "stop": float, "timeframe": "..."}},
  "TICKER2": ...
}}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json
```

After all 5 agents complete, proceed to Step 4.

## Step 4 — Head Swing Trader synthesis

Dispatch **one** Agent tool call (model: sonnet):

```
You are the Head Swing Trader.

1. Read your prompt from: ai_hedge/personas/prompts/swing_head_trader.md
2. Read ALL swing strategy signal files from runs/{RUN_ID}/signals/:
   - swing_trend_momentum.json, swing_mean_reversion.json, swing_breakout.json,
     swing_catalyst_news.json, swing_macro_context.json
3. Read wiki memory BEFORE synthesizing (per the "Wiki Memory" section of your prompt):
   - wiki/meta/lessons.md (whole file, ~15 most recent bullets)
   - For EACH ticker in [{TICKERS}]:
     - read the TL;DR section (top of file) of wiki/tickers/<TICKER>/trades.md
     - read the YAML front-matter (top block between `---` lines) of
       wiki/tickers/<TICKER>/thesis.md — pay attention to `confidence_score`
   - If a wiki file does not exist or is empty, proceed with vote-counting only.

Synthesize all strategy signals into a unified swing trade assessment per ticker in [{TICKERS}].
Resolve conflicting signals, identify highest-conviction setups, note risk factors.
When the wiki memory contradicts a 3-of-5 bullish/bearish vote — recent failures of the same
setup type, or a stop-out on this exact ticker — dial down confidence accordingly and call it out
in `key_conflicts` and `reasoning`.

Write your output to: runs/{RUN_ID}/signals/swing_head_trader.json
```

## Step 5 — Aggregate signals

Parse `$ARGUMENTS` for an optional `--cash` flag. If present, use that value. Otherwise default to 100000.

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash $CASH --require-turso
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Swing Portfolio Manager

Dispatch **one** Agent tool call (model: sonnet):

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/swing_portfolio_manager.md

You are the Swing Portfolio Manager. You are managing a portfolio with ${CASH} total capital. Size all positions to fit within this budget. Maximum 25% of capital per position.

Make swing trade decisions for each ticker in [{TICKERS}].
Consider the Head Swing Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe and an overall synthesis.

Write the output to: runs/{RUN_ID}/decisions.json
```

## Step 7 — Explainer Agent

Dispatch **one** Agent tool call (model: sonnet) to produce a plain-English educational explanation:

```
You are a Financial Explainer agent.

1. Read your system prompt from: ai_hedge/personas/prompts/explainer.md
2. Read the mode from: runs/{RUN_ID}/metadata.json
3. Read the final decisions from: runs/{RUN_ID}/decisions.json
4. Read all signals from: runs/{RUN_ID}/signals_combined.json

The mode is: swing
The tickers are: [{TICKERS}]

Produce a layered educational explanation following the prompt exactly.
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

## Step 7.5 — Wiki Curator (feature-flagged)

This step runs only if `tracker/watchlist.json:settings.wiki_enabled == true`. Check first:

```bash
python -c "from ai_hedge.wiki.inject import is_wiki_enabled; print('ON' if is_wiki_enabled() else 'OFF')"
```

If the output is `OFF`, **skip this step entirely** and go to Step 8.

If `ON`, dispatch **one** Agent tool call (model: sonnet) to maintain the wiki:

```
You are the Wiki Curator.

1. Read your system prompt from: ai_hedge/personas/prompts/wiki_curator.md
2. Read the run artifacts:
   - runs/{RUN_ID}/decisions.json
   - runs/{RUN_ID}/signals_combined.json
   - runs/{RUN_ID}/explanation.json
   - runs/{RUN_ID}/web_research/<TICKER>.json for each ticker in [{TICKERS}]
3. Read the current wiki pages for each ticker in [{TICKERS}]:
   - wiki/tickers/<TICKER>/thesis.md
   - wiki/tickers/<TICKER>/technicals.md
   - wiki/tickers/<TICKER>/catalysts.md
   - wiki/tickers/<TICKER>/trades.md
   plus wiki/macro/regime.md and wiki/INDEX.md, wiki/LOG.md.

run_id: {RUN_ID}
mode: swing
tickers in scope: [{TICKERS}]
is_macro_dispatch: true
pages_in_scope: thesis, technicals, catalysts, trades, regime, INDEX, LOG

Update the wiki per the rules in your system prompt. Synthesize, do NOT
append. Stay within each page's target_words ± 20%. Return a JSON manifest
listing every page touched and its action.

Write any errors to runs/{RUN_ID}/wiki_curator_error.txt instead of failing —
trade decisions are final, the wiki must never block finalize.
```

After the curator returns, lint:

```bash
python -c "from ai_hedge.wiki import lint; import json; print(json.dumps(lint.lint_directory(), indent=2))"
```

If the linter reports issues, log them to `runs/{RUN_ID}/wiki_curator_error.txt` but **do not abort**.

> **6+ tickers:** if the run has more than 6 tickers, split the curator into two dispatches per the plan §4.2 — first half tickers (per-ticker pages only, `is_macro_dispatch: false`), then second half + macro/index/log (`is_macro_dispatch: true`). The 1–3 ticker case stays one dispatch.

## Step 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: entry/target/stop/risk-reward/timeframe, Head Trader synthesis, strategy breakdown. It also touches `wiki/INDEX.md` to keep its `last_updated` dates fresh (no-op if `wiki_enabled=false`).
