---
name: crypto-autorun
description: Automated crypto trading. Runs model on crypto watchlist, places paper trades, monitors positions, shows dashboard. 24/7 — no market hours check.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent WebSearch WebFetch
argument-hint: [--force]
---

# Crypto Autorun — Automated Crypto Trading Routine

## Step 1 — Sync positions and check schedule

First, monitor existing crypto positions (if crypto_tracker module exists):
```bash
python -m crypto_tracker monitor 2>/dev/null || echo "No crypto_tracker module yet — skipping monitor"
```

Read the crypto watchlist to check what's due:
```bash
python -c "
import json, os
from datetime import datetime

watchlist_path = 'crypto_tracker/watchlist.json'
if not os.path.exists(watchlist_path):
    # Default crypto watchlist
    default = {
        'schedules': [
            {
                'name': 'crypto_swing',
                'mode': 'swing',
                'tickers': 'BTC-USD,ETH-USD,SOL-USD,BNB-USD,XRP-USD,ADA-USD,AVAX-USD,DOT-USD,MATIC-USD,LINK-USD',
                'days': 'mon,wed,fri',
                'note': 'Major caps swing analysis 3x/week'
            },
            {
                'name': 'crypto_day',
                'mode': 'daytrade',
                'tickers': 'BTC-USD,ETH-USD,SOL-USD',
                'days': 'mon,tue,wed,thu,fri,sat,sun',
                'note': 'Top 3 intraday — runs daily (crypto is 24/7)'
            },
            {
                'name': 'altcoin_swing',
                'mode': 'swing',
                'tickers': 'DOGE-USD,ATOM-USD,UNI-USD,NEAR-USD,FTM-USD,ARB-USD,OP-USD,APT-USD,SUI-USD,INJ-USD',
                'days': 'tue,thu',
                'note': 'Altcoin swing analysis 2x/week'
            }
        ],
        'settings': {
            'paper_account_size': 10000,
            'max_position_size_usd': 2500,
            'max_concurrent_trades': 10,
            'note': 'Crypto paper trading budget'
        }
    }
    os.makedirs('crypto_tracker', exist_ok=True)
    with open(watchlist_path, 'w') as f:
        json.dump(default, f, indent=2)
    print('Created default crypto watchlist')
    print(json.dumps(default['schedules'], indent=2))
else:
    days_map = {'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6}
    today = datetime.now().strftime('%a').lower()[:3]
    with open(watchlist_path) as f:
        wl = json.load(f)
    due = []
    for s in wl['schedules']:
        if today in s['days'].split(',') or '--force' in '$ARGUMENTS':
            due.append(s)
    print(json.dumps(due, indent=2))
"
```

NOTE: Crypto is 24/7 — there is NO market hours check. Runs can happen anytime.

If no schedules due today and --force not passed, print "Nothing scheduled today" and show status, then stop.

## Step 2 — Get available cash

```bash
python -c "
import json, os
watchlist_path = 'crypto_tracker/watchlist.json'
if os.path.exists(watchlist_path):
    with open(watchlist_path) as f:
        config = json.load(f)
    cash = config['settings']['paper_account_size']
    print(cash)
else:
    print(10000)
"
```

Set `CASH` to the output value.

## Step 3 — Run model for each due schedule

For each due schedule from Step 1, generate a RUN_ID and run the appropriate crypto slash command.

For swing schedules: run `/crypto-swing {TICKERS}` with `--cash $CASH` appended
For daytrade schedules: run `/crypto-day {TICKERS}` with `--cash $CASH` appended

Wait for each run to complete before proceeding.

## Step 4 — Execute trades (if crypto_tracker exists)

For each completed run:
```bash
python -m crypto_tracker execute --run-id $RUN_ID 2>/dev/null || echo "No crypto_tracker execute module — showing decisions only"
cat runs/$RUN_ID/decisions.json
```

## Step 5 — Show dashboard

```bash
python -m crypto_tracker report --last 7 2>/dev/null || echo "No crypto_tracker report module yet"
python -m crypto_tracker status 2>/dev/null || echo "No crypto_tracker status module yet"
```

If crypto_tracker modules don't exist yet, just display the decisions.json from each run.
