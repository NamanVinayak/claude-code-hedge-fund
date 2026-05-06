---
name: DIS recent
last_updated: 2026-05-06
last_run_id: 20260506_220627
target_words: 200
stale_after_days: 30
word_count: 286
summary: Signal history — direction flips and key level breaks for DIS across swing runs
---

# DIS — Recent Signal History

Append-only. One bullet per signal direction flip or key level break. Curator adds entries; compactor archives entries >60 days old.

---

- **2026-05-01** (run `20260501_221355`): **Signal flip: Hold/cautious-buy → Active BUY (62%).** Apr 30 breakout above $103 resistance (1.23x vol) triggered 4/5 bullish votes. Q2 FY2026 earnings confirmed May 6 (consensus EPS $1.49) moved into catalyst window. Buy decision: 2 shares, limit $102.50, target $107.11, stop $101.00, 3.07:1 R/R. Prior "no near-term catalyst" thesis falsified. Prior thesis also noted "do not enter above $103" — today's price is above that but entry is set on pullback, not a chase. [source: `decisions.json`, `swing_head_trader`, run `20260501_221355`]

- **2026-05-04** (run `20260504_221111`): **Signal flip: Active BUY → HOLD (42%).** Risk manager hard block: earnings in 2 days (May 6 pre-market), 3-day blackout enforced, remaining_position_limit = $0. Key level break: April 30 breakout fully retraced — hourly price $101.31 near hard stop $101.00 (prior $103.75 breakout close now overhead). Open long id 117 (2 shares at $103.495 fill) intact but near stop. Macro tailwind claim from May 1 falsified by Iran escalation (WTI near $105, Dow -557 pts). [source: `decisions.json`, `risk_management_agent`, `web_research/DIS.json`, run `20260504_221111`]

- **2026-05-05** (run `20260505_220625`): **Key level break: stop $101.00 hit — trade id 117 closed.** Open long id 117 (2 shares, fill $103.495) stopped out at $101.00, realizing -$4.99 P&L. No open DIS positions remain. Hourly price fell to $100.48 — below the hard stop and below all short-term EMAs. Prior bullish call (run `20260501_221355`, 4/5 agents, 62% confidence) confirmed invalidated: breakout at $104.83 fully retraced and closed at a loss. All 5 swing agents neutral (100% consensus) heading into May 6 earnings. Post-earnings plan: gap and hold above $104.83 = fresh long opportunity; gap below $98.45 = wait for stabilization at $97.89 Fib 61.8%. [source: `trade_ledger.json per_ticker_history["DIS"]`, `decisions.json`, run `20260505_220625`]

- **2026-05-06** (run `20260506_220627`): **Signal flip: Neutral → Bullish lean (earnings catalyst fired).** Q2 FY2026 earnings beat (EPS $1.57 vs. $1.49 est, rev $25.17B vs. $24.84B est) triggered the pre-stated bull restart condition — gap above $104.83 on 1.5x+ volume. Price gapped +7.5% to $108.06 on 1.81x daily volume, clearing 11-test resistance at $107.11 (key level break). 2/5 swing agents bullish (breakout 62 conf, catalyst_news 52 conf). However: earnings blackout (3-day rule, until May 9+) prohibits new position, and R/R at $108 is 0.16:1 — makes immediate entry indefensible. Head Trader consensus bullish (42 conf, recommended_action: buy) but PM enforces blackout hold. No new trade. Watch for pullback to $105–107 consolidation zone post-May 9 for fresh long entry. [source: `signals_combined.json swing_breakout`, `swing_head_trader`, `risk_management_agent`, `web_research/DIS.json`, run `20260506_220627`]
