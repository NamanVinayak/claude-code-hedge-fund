---
name: DIS recent
last_updated: 2026-05-04
last_run_id: 20260504_221111
target_words: 200
stale_after_days: 30
word_count: 148
summary: Signal history — direction flips and key level breaks for DIS across swing runs
---

# DIS — Recent Signal History

Append-only. One bullet per signal direction flip or key level break. Curator adds entries; compactor archives entries >60 days old.

---

- **2026-05-01** (run `20260501_221355`): **Signal flip: Hold/cautious-buy → Active BUY (62%).** Apr 30 breakout above $103 resistance (1.23x vol) triggered 4/5 bullish votes. Q2 FY2026 earnings confirmed May 6 (consensus EPS $1.49) moved into catalyst window. Buy decision: 2 shares, limit $102.50, target $107.11, stop $101.00, 3.07:1 R/R. Prior "no near-term catalyst" thesis falsified. Prior thesis also noted "do not enter above $103" — today's price is above that but entry is set on pullback, not a chase. [source: `decisions.json`, `swing_head_trader`, run `20260501_221355`]

- **2026-05-04** (run `20260504_221111`): **Signal flip: Active BUY → HOLD (42%).** Risk manager hard block: earnings in 2 days (May 6 pre-market), 3-day blackout enforced, remaining_position_limit = $0. Key level break: April 30 breakout fully retraced — hourly price $101.31 near hard stop $101.00 (prior $103.75 breakout close now overhead). Open long id 117 (2 shares at $103.495 fill) intact but near stop. Macro tailwind claim from May 1 falsified by Iran escalation (WTI near $105, Dow -557 pts). [source: `decisions.json`, `risk_management_agent`, `web_research/DIS.json`, run `20260504_221111`]
