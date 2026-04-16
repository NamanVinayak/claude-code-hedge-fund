---
name: autorun
description: Daily automated paper trading. Runs model on watchlist, places paper trades, monitors positions, shows dashboard.
disable-model-invocation: true
allowed-tools: Bash(*) Read Write Agent
argument-hint: [--force]
---

# Autorun — Daily Paper Trading Routine

## Step 1 — Sync positions and clean up stale orders

First, monitor existing positions. This syncs fills AND cleans up orders that Moomoo
cancelled overnight (DAY-only orders expire at close each day):
```bash
python -m tracker monitor
```

This will:
- Detect filled entries and update status to 'entered'
- Detect cancelled/expired entry orders and mark trades as 'cancelled' in our DB
- Warn about stop/target orders on open positions that need re-placing
- Show what's still active vs what got cleaned up

Read the watchlist to check what's due today:
```bash
python -c "
import json
from datetime import datetime
days_map = {'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6}
today = datetime.now().strftime('%a').lower()[:3]
with open('tracker/watchlist.json') as f:
    wl = json.load(f)
due = []
for s in wl['schedules']:
    if today in s['days'].split(',') or '--force' in '$ARGUMENTS':
        due.append(s)
print(json.dumps(due, indent=2))
"
```

If no schedules due today and --force not passed, print "Nothing scheduled today" and show status, then stop.

## Step 2 — Get available cash

```bash
CASH=$(python -c "from tracker.db import get_available_cash; print(int(get_available_cash()))")
echo "Available cash: $CASH"
```

If CASH is 0 or negative, print "No cash available for new trades" and skip to Step 5.

## Step 3 — Run model for each due schedule

For each due schedule from Step 1, generate a RUN_ID and run the appropriate slash command.

For swing schedules: run `/swing {TICKERS}` with `--cash $CASH` appended
For daytrade schedules: run `/daytrade {TICKERS}` with `--cash $CASH` appended

Wait for each run to complete before proceeding.

## Step 4 — Execute trades

For each completed run, execute the trades:
```bash
python -m tracker execute --run-id $RUN_ID
```

## Step 5 — Show dashboard

```bash
python -m tracker report --last 7
python -m tracker status
```
