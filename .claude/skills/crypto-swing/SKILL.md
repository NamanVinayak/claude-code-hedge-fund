---
name: crypto-swing
description: Find crypto swing trade setups using 9 strategy agents + crypto sentiment. 2-20 day trades with entry/target/stop.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent WebSearch WebFetch
argument-hint: TICKER1[,TICKER2,...] [--cash N]
---

# Crypto Swing Mode — AI Hedge Fund

## Step 1 — Parse arguments and generate run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
```

Parse `$ARGUMENTS` as the comma-separated ticker list. Normalize to uppercase, comma-separated, no spaces.
Crypto tickers use the `-USD` suffix (e.g., BTC-USD, ETH-USD, SOL-USD).

Set variables: `TICKERS`, `RUN_ID`. Extract `--cash` if present (default 100000).

## Step 2 — Fetch data (crypto mode)

```bash
python -m ai_hedge.runner.prepare --tickers $TICKERS --run-id $RUN_ID --mode swing --asset-type crypto
```

This fetches price data via yfinance (works for crypto tickers), skips financial metrics/insider trades, saves metadata with `asset_type: crypto`, and builds swing strategy facts (indicators computed on price data).

## Step 2.5 — Crypto Web Research Agent

Dispatch one Agent tool call **per ticker** (can be parallel if multiple tickers):

```
You are the Crypto Web Research Agent.

1. Read your system prompt from: ai_hedge/personas/prompts/crypto_web_researcher.md
2. For ticker {TICKER}, use WebSearch to research:
   - Macro crypto context (search: "crypto market news today", "Bitcoin dominance", "crypto Fear Greed Index today", "Bitcoin ETF flows today", "crypto regulation news")
   - Ticker-specific (search: "{TICKER} whale movements", "{TICKER} funding rate", "{TICKER} exchange inflows outflows", "{TICKER} development activity GitHub", "{TICKER} upcoming upgrades roadmap", "{TICKER} news this week")
   - Institutional flows (search: "institutional crypto purchases this week", "government Bitcoin reserve news")
3. Write your research to: runs/{RUN_ID}/web_research/{TICKER}.json

Follow the JSON format in your system prompt exactly.
```

NOTE: Do NOT run the facts_builder rebuild after web research (invest-mode facts are skipped for crypto). Swing facts are already built from Step 2.

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
You are the {AGENT} swing trade analyst. You are analyzing CRYPTO assets (not stocks).

1. Read your system prompt from: ai_hedge/personas/prompts/{AGENT}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{AGENT}__{TICKER}.json
   (For stanley_druckenmiller and news_sentiment, the facts file uses the invest-mode name.)
   NOTE: This is crypto — financial metrics will be empty. Focus on price action, technicals, and volume.

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
You are the Head Swing Trader. You are analyzing CRYPTO assets.

1. Read your prompt from: ai_hedge/personas/prompts/swing_head_trader.md
2. Read ALL swing strategy signal files from runs/{RUN_ID}/signals/:
   - swing_trend_follower.json, swing_pullback_trader.json, swing_breakout_trader.json,
     swing_momentum_ranker.json, swing_mean_reversion.json, swing_catalyst_trader.json,
     swing_sector_rotation.json, stanley_druckenmiller.json, news_sentiment.json
3. Also read the crypto sentiment signal: runs/{RUN_ID}/signals/crypto_sentiment.json

Synthesize all strategy signals + crypto sentiment into a unified swing trade assessment per ticker in [{TICKERS}].
Resolve conflicting signals, identify highest-conviction setups, note crypto-specific risk factors.

Write your output to: runs/{RUN_ID}/signals/swing_head_trader.json
```

## Step 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers $TICKERS --cash $CASH --asset-type crypto
```

This loads all signals, runs technicals + risk_manager (skips fundamentals/valuation/sentiment for crypto), computes allowed actions, and writes `signals_combined.json`.

## Step 6 — Dispatch Crypto Swing Portfolio Manager

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- runs/{RUN_ID}/signals/crypto_sentiment.json
- ai_hedge/personas/prompts/crypto_swing_pm.md

You are the Crypto Swing Portfolio Manager. You are managing a portfolio with ${CASH} total capital. Size all positions to fit within this budget. Maximum 25% of capital per position. Crypto supports fractional quantities.

Make swing trade decisions for each ticker in [{TICKERS}].
Consider the Head Swing Trader's synthesis, crypto sentiment, and all strategy signals and deterministic agent outputs.

Return JSON with per-ticker entry/target/stop/risk-reward/timeframe and an overall synthesis.

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

The mode is: swing (crypto)
The tickers are: [{TICKERS}]

Produce a layered educational explanation following the prompt exactly.
Note: this is crypto — adapt explanations to crypto context (no earnings, no PE ratios, focus on on-chain metrics and crypto catalysts).
Return JSON matching the format in the prompt.

Write the output to: runs/{RUN_ID}/explanation.json
```

## Step 8 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

This displays: entry/target/stop/risk-reward/timeframe, Head Trader synthesis, strategy breakdown.

## Step 9 — Commit and push results to GitHub

Write a plain-English summary of the run to `runs/$RUN_ID/summary.md` — top 3 setups, key themes, overall market context (1-2 paragraphs). Then commit the full run and push to a new branch:

```bash
BRANCH="claude/crypto-swing-${RUN_ID}"
git checkout -b $BRANCH
git add -f runs/$RUN_ID/
git commit -m "crypto swing ${RUN_ID}: ${TICKERS}

$(cat runs/$RUN_ID/summary.md | head -5)"
git push origin $BRANCH
```

Print the branch URL: `https://github.com/NamanVinayak/claude-code-hedge-fund/tree/$BRANCH`
