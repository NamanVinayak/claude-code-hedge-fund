# AI Hedge Fund — Run Playbook

When the user says **"run the hedge fund on TICKER1,TICKER2"**, execute the steps below in order.

---

## STEP 1 — Generate a run ID

```bash
RUN_ID=$(date +%Y%m%d_%H%M%S)
echo "Run ID: $RUN_ID"
```

---

## STEP 2 — Fetch raw data

```bash
python -m ai_hedge.runner.prepare --tickers TICKER1,TICKER2 --run-id $RUN_ID
```

Creates `runs/$RUN_ID/raw/<TICKER>.json` for each ticker with:
- financial metrics, line items, market cap, insider trades, company news, prices

---

## STEP 3 — Build facts bundles

```bash
python -m ai_hedge.personas.facts_builder --tickers TICKER1,TICKER2 --run-id $RUN_ID
```

Creates `runs/$RUN_ID/facts/<persona>__<ticker>.json` for each persona × ticker combo.

---

## STEP 4 — Dispatch 15 persona subagents IN PARALLEL

Send **all 15 Agent tool calls in a single message** (one per persona).

Personas:
`warren_buffett`, `charlie_munger`, `ben_graham`, `bill_ackman`, `cathie_wood`,
`michael_burry`, `nassim_taleb`, `peter_lynch`, `phil_fisher`, `stanley_druckenmiller`,
`mohnish_pabrai`, `rakesh_jhunjhunwala`, `aswath_damodaran`, `growth_agent`, `news_sentiment`

Prompt template for each persona (replace `{PERSONA}`, `{RUN_ID}`, `{TICKERS}`):

```
You are the {PERSONA} investor agent.

1. Read your system prompt from: ai_hedge/personas/prompts/{PERSONA}.md
2. For each ticker in [{TICKERS}], read the facts bundle from:
   runs/{RUN_ID}/facts/{PERSONA}__{TICKER}.json

Analyze each ticker using ONLY the provided facts data.

Return a JSON object mapping each ticker to your signal:
{
  "TICKER1": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "..."},
  "TICKER2": {"signal": "bullish|bearish|neutral", "confidence": 0-100, "reasoning": "..."}
}

Write your output to: runs/{RUN_ID}/signals/{PERSONA}.json

Use exactly the schema from ai_hedge/schemas.py for this persona.
```

---

## STEP 5 — Aggregate signals

```bash
python -m ai_hedge.runner.aggregate --run-id $RUN_ID --tickers TICKER1,TICKER2 --cash 100000
```

- Loads all persona signals from `runs/$RUN_ID/signals/*.json`
- Runs 4 deterministic agents: fundamentals, technicals, valuation, sentiment
- Runs risk manager
- Computes allowed actions given portfolio limits
- Writes `runs/$RUN_ID/signals_combined.json`

Optional flags:
- `--cash 250000` — starting cash
- `--margin-requirement 0.5` — margin requirement (0.0 = no shorting margin limit)

---

## STEP 6 — Portfolio manager subagent

Dispatch **one** Agent tool call:

```
Read the following files:
- runs/{RUN_ID}/signals_combined.json
- ai_hedge/personas/prompts/portfolio_manager.md

Make final trading decisions for each ticker in {TICKERS} based on:
- analyst_signals: all 15 persona signals + 4 deterministic signals + risk manager
- allowed_actions: what actions are physically possible given current portfolio limits

Return JSON in this exact format:
{
  "decisions": {
    "TICKER1": {"action": "buy|sell|short|cover|hold", "quantity": 123, "confidence": 75, "reasoning": "..."},
    "TICKER2": {"action": "buy|sell|short|cover|hold", "quantity": 0,   "confidence": 90, "reasoning": "..."}
  }
}

Write the output to: runs/{RUN_ID}/decisions.json
```

---

## STEP 7 — Display results

```bash
python -m ai_hedge.runner.finalize --run-id $RUN_ID
```

Prints a colored table showing:
- Each ticker's action, quantity, confidence, and reasoning
- Analyst signal breakdown (bullish/bearish/neutral counts)
- Per-analyst signal and reasoning
- Portfolio summary

---

## Directory layout after a full run

```
runs/
└── 20240101_120000/
    ├── raw/
    │   ├── AAPL.json
    │   └── MSFT.json
    ├── facts/
    │   ├── warren_buffett__AAPL.json
    │   └── ...
    ├── signals/
    │   ├── warren_buffett.json
    │   ├── charlie_munger.json
    │   └── ...  (15 persona files)
    ├── signals_combined.json
    └── decisions.json
```
