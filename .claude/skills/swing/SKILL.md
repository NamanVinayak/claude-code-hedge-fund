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

Dispatch one Agent tool call **per ticker** (all in parallel in a single message):

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files, use WebSearch, and write JSON files.

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

Dispatch **one** Agent tool call (covers all tickers):

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files, use WebSearch, and write JSON files.

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

Send ALL 5 Agent tool calls in a **single message** and wait for all to complete before proceeding.

The 5 agents are:
- `swing_trend_momentum` — with-the-trend continuation
- `swing_mean_reversion` — counter-extension (fade extremes OR buy dips at Fib)
- `swing_breakout` — regime-change / volatility expansion
- `swing_catalyst_news` — external triggers (events, news, insiders)
- `swing_macro_context` — top-down macro + relative strength + asymmetric R/R

For each agent, use this prompt template for `{AGENT}`:

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files and write a JSON file.

You are the {AGENT} swing trade analyst.

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   The facts include financial data AND a "web_context" section with current market conditions and news. Use both in your analysis.

Analyze each ticker for swing trade setups using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{
  "TICKER1": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "...", "entry": float, "target": float, "stop": float, "timeframe": "..."},
  "TICKER2": ...
}

Write your output to: runs/{RUN_ID}/signals/{AGENT}.json
```

After all 5 agents complete, proceed to Step 4.

## Step 4 — Head Swing Trader synthesis

Dispatch **one** Agent tool call:

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files and write a JSON file.

You are the Head Swing Trader.

1. Read your prompt from: ai_hedge/personas/prompts/swing_head_trader.md
2. Read ALL swing strategy signal files from runs/{RUN_ID}/signals/:
   - swing_trend_momentum.json, swing_mean_reversion.json, swing_breakout.json,
     swing_catalyst_news.json, swing_macro_context.json

Synthesize all strategy signals into a unified swing trade assessment per ticker in [{TICKERS}].
Resolve conflicting signals, identify highest-conviction setups, note risk factors.

Write your output to: runs/{RUN_ID}/signals/swing_head_trader.json
```

## Step 5 — Aggregate signals

Parse `$ARGUMENTS` for an optional `--cash` flag. If present, pass it. Otherwise omit it — `aggregate.py` reads `paper_account_size` from `tracker/watchlist.json` as the default ($25,000 currently).

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS  # add --cash N to override
```

This loads all signals, runs deterministic agents (fundamentals, technicals, valuation, sentiment, risk_manager), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Swing Portfolio Manager

Dispatch **one** Agent tool call:

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files and write a JSON file.

Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/swing_portfolio_manager.md

You are the Swing Portfolio Manager. You are managing a portfolio with ${CASH} total capital. Size all positions to fit within this budget. Maximum 25% of capital per position.

Make swing trade decisions for each ticker in [{TICKERS}].
Consider the Head Swing Trader's synthesis in signals_combined along with all strategy signals and deterministic agent outputs.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe and an overall synthesis.

CRITICAL: Your output JSON MUST be wrapped in a "decisions" key like this:
{"decisions": {"TICKER1": {...}, "TICKER2": {...}}}
Do NOT write a flat JSON object at the top level — the executor reads decisions_data["decisions"] and a flat object will result in zero trades being placed.

Write the output to: runs/{RUN_ID}/decisions.json
```

## Step 7 — Explainer Agent

Dispatch **one** Agent tool call to produce a plain-English educational explanation:

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Just read files and write a JSON file.

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

## Step 7.5 — Wiki Curator Agent (skip if wiki disabled)

Only run this step if the wiki feature flag is on:

```bash
.venv/bin/python -c "from ai_hedge.wiki.inject import is_wiki_enabled; import sys; sys.exit(0 if is_wiki_enabled() else 1)"
```

If exit 0 (enabled), first dump the canonical Turso ledger so the curator has authoritative trade ground truth (prevents Position-N hallucinations from inferring trades that never made it to the ledger):

```bash
.venv/bin/python -m tracker.wiki_ledger_export --run-id $RUN_ID --tickers $TICKERS
```

This writes `runs/$RUN_ID/trade_ledger.json` containing open_positions, pending_orders, recent_closures_30d, and per_ticker_history. If the helper fails (e.g. Turso unreachable), continue anyway — the curator will fall back to its previous behavior. Wiki updates never block trade execution.

Then dispatch **one** Agent tool call to update wiki pages with what this run learned:

```
IMPORTANT: Do NOT invoke any skills. Do NOT use memory tools. Read files and write files only.

You are the Wiki Curator agent.

1. Read your system prompt from: ai_hedge/personas/prompts/wiki_curator.md
2. Read the run artifacts:
   - runs/{RUN_ID}/decisions.json
   - runs/{RUN_ID}/signals_combined.json
   - runs/{RUN_ID}/explanation.json
   - runs/{RUN_ID}/trade_ledger.json   ← canonical Turso ledger (authoritative for all trade-related claims, see hard rule #11)
   - runs/{RUN_ID}/web_research/<TICKER>.json (one per ticker if present)
3. For each ticker in [{TICKERS}], read existing wiki/<TICKER>/{thesis,technicals,catalysts,recent,trades}.md (if they exist) plus their YAML front-matter
4. Decide per-page whether to rewrite, append, or leave untouched per the prompt rules

The dispatch scope:
- run_id: {RUN_ID}
- mode: swing
- tickers: [{TICKERS}]
- is_macro_dispatch: true
- pages_in_scope: thesis, technicals, catalysts, recent, trades, regime, LOG, INDEX

Write any rewritten pages directly to disk under wiki/. Update YAML front-matter (last_updated, last_run_id, word_count) on every rewrite. Do not delete any files.

Return the manifest JSON described in the system prompt at the end of your response.
```

## Step 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: entry/target/stop/risk-reward/timeframe, Head Trader synthesis, strategy breakdown.

## Step 9 — Commit and push results to GitHub

Write a plain-English summary of the run to `runs/$RUN_ID/summary.md` — top 3 setups, key themes, overall market context (1-2 paragraphs). Then commit run data + any wiki updates directly to the current branch (routines run on `main`, local runs commit on whatever branch the user is on):

```bash
BRANCH=$(git branch --show-current)

# Commit 1: run artifacts (always)
git add -f runs/$RUN_ID/
git commit -m "swing run ${RUN_ID}: ${TICKERS}

$(cat runs/$RUN_ID/summary.md | head -5)"

# Commit 2: wiki updates (only if curator changed anything)
if ! git diff --quiet wiki/ || ! git diff --cached --quiet wiki/; then
  git add wiki/
  git commit -m "wiki: curator updates from swing run ${RUN_ID}"
fi

# Rebase against remote in case a concurrent routine pushed first, then push
git pull --rebase origin "$BRANCH" || { git rebase --abort; echo "Rebase conflict — manual resolution needed"; exit 1; }
git push origin "$BRANCH"
```

Print the commit URL: `https://github.com/NamanVinayak/claude-code-hedge-fund/commits/$BRANCH`
