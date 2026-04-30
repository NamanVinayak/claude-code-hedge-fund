# Wiki Run Log

Append-only. One line per run, format:

```
## [YYYY-MM-DD] <mode> | <TICKERS> | run <run_id> | <decision summary> | wiki touched: <pages>
```

Compactor rolls entries >60 days old into weekly summaries, and entries
>365 days old into monthly summaries.

---

## [2026-04-29] bootstrap | 23 tickers + MACRO | run bootstrap | fresh-start cleanup + wiki seeded | wiki touched: 93 pages (4×23 ticker pages + macro/regime.md)
## [2026-04-29] swing | NVDA | run sanity_20260429_031705 | HOLD existing 6 shares at $197.20 cost, target $231, stop $207, conf 55; no new entry (above $211 no-chase zone); hard exit by May 17 earnings blackout | wiki touched: LOG.md
## [2026-04-30] swing | JPM | run 20260430_051455 | HOLD at $309.25 (42 conf); 2B/1Br/2N split; R/R 1.55:1 fails 2:1 minimum; watch zone $307.00–$307.50 (R/R ~2.7:1); signal flip Buy→Hold vs Apr 17 run | wiki touched: tickers/JPM/recent.md (created), macro/regime.md, LOG.md, INDEX.md
## [2026-04-30] swing | NVDA | run 20260430_060402 | BUY 67 shares at $209.25, target $222.50, stop $205.30, R/R 3.35:1, conf 72; 4/5 swing agents bullish; ADX 54.67 strongest in run history; pullback to hourly Fib 38.2% / $208.20 volume-confirmed support | wiki touched: tickers/NVDA/trades.md, LOG.md, INDEX.md
## [2026-04-30] swing | NVDA | run 20260430_124724 | BUY 3 shares at $209.50, target $221.89, stop $205.30, R/R 2.95:1, conf 74; 4/5 swing agents bullish; same pullback-buy setup; Meta -9% post-earnings capex shock adds near-term sector headwind; macro regime updated (Fed 3.5-3.75%, mixed market) | wiki touched: tickers/NVDA/technicals.md, tickers/NVDA/catalysts.md, tickers/NVDA/trades.md, macro/regime.md, LOG.md, INDEX.md
## [2026-04-30] swing | META | run 20260430_141238 | HOLD conf 55; bearish medium-term bias — Q1 2026 earnings capex shock ($125-145B raised guidance) invalidated prior long thesis ($675-677 entry); 10% single-session collapse to ~$601 on 9.99x volume; wait for dead-cat bounce to $618-630 before short; target $583, stop $645 | wiki touched: tickers/META/thesis.md, tickers/META/recent.md (created), INDEX.md, LOG.md
## [2026-04-30] swing | AAPL | run 20260430_144524 | HOLD conf 30; earnings blackout (0 days to Q2 FY2026 print) blocks all new positions; head trader confidence 30 < 40 threshold; R/R 0.71:1 fails 2:1 minimum; 3/5 swing agents neutral; ADX 15.78 (weak); valuation 44.8% above DCF fair value; insider net selling -$235M; post-earnings watch: bull above $276.11 / bear Fib $264.21 / invalidation $255.45 | wiki touched: tickers/AAPL/trades.md, LOG.md, INDEX.md
## [2026-04-30] swing | JPM | run 20260430_182725 | HOLD conf 38; R/R 1.83:1 fails 2:1 hard rule; 2 bullish (mean_reversion 62%, macro_context 52%) vs 3 neutral; dual trigger setup — dip-buy $307–$309.50 OR breakout above $315.50 on 1.5x vol; ADX 43.42 uptrend intact; Iran/Hormuz and Dimon credit warning are live stop-thesis triggers | wiki touched: tickers/JPM/technicals.md, tickers/JPM/catalysts.md, macro/regime.md, LOG.md, INDEX.md
