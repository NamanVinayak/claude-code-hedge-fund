# Crypto Code Archive (Quarantined)

**Status**: Frozen — this code is no longer maintained.

**Date**: 2026-04-27

## Why

User elected to run stock swing only. Crypto code was receiving fixes (model pinning, schema changes, web research dispatch) that didn't apply to it. Quarantined cleanly so:

- Stock swing pipeline runs unchanged
- Crypto code is preserved verbatim, restorable in one move

## What

```
.archive/crypto/
├── crypto_tracker/          # Full crypto tracker module
│   ├── cli.py
│   ├── db.py                 # SQLAlchemy models (Trade, SimOrder)
│   ├── executor.py
│   ├── monitor.py
│   ├── price_watcher.py     # 24/7 yfinance fills orders
│   ├── reporter.py
│   ├── sim_client.py
│   ├── watchlist.json
│   └── crypto_tracker.db
├── .claude/skills/          # Crypto slash command skills
│   ├── crypto-autorun/
│   ├── crypto-day/
│   └── crypto-swing/
└── .agents/skills/           # Same for @ agent reference
    ├── crypto-autorun/
    ├── crypto-day/
    └── crypto-swing/
```

## Restore

To restore crypto trading:

```bash
# 1. Move files back
mv .archive/crypto/crypto_tracker/ ./
mv .archive/crypto/.claude/skills/crypto-* .claude/skills/
mv .archive/crypto/.agents/skills/crypto-* .agents/skills/

# 2. Revert NotImplementedError changes
# In ai_hedge/runner/prepare.py: remove the crypto check
# In ai_hedge/runner/aggregate.py: remove the crypto check
# Restore the --asset-type choices to include "crypto"

# 3. Reference: grep -rn "crypto" .archive/crypto/ --include="*.py" | head -20
```

## References

- Last working state: commit before this quarantine
- Docs: see CLAUDE.md (pre-quarantine) or git log