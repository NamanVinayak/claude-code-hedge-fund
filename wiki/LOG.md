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
## [2026-05-01] swing | MSFT | run 20260501_153820 | HOLD (conf 38%); 2B/2Br/1N split; Q3 FY2026 beat (EPS $4.27, Azure +40%) but $190B capex guidance spooked market; Apr 30 breakdown below $413 pivot on 2.06x volume; stop $412 violated; wait for $416-420 recapture or $404 bear confirmation; R/R 0.82:1 fails 2:1 minimum | wiki touched: tickers/MSFT/technicals.md, tickers/MSFT/catalysts.md, tickers/MSFT/thesis.md, tickers/MSFT/recent.md (created), macro/regime.md, LOG.md, INDEX.md
## [2026-05-01] swing | TSLA | run 20260501_160246 | HOLD (conf 35%); 3B/2N split; Q1 gross margin 18.03% crossed prior flip trigger; hourly squeeze fired on 2.74x vol; price mid-resistance $387-399 zone; R/R 1.18:1 fails 2:1 minimum; watch $381-385 pullback with bullish daily candle for 2.7:1 entry | wiki touched: tickers/TSLA/thesis.md, tickers/TSLA/recent.md (created), LOG.md, INDEX.md
## [2026-05-01] swing | GOOG | run 20260501_164617 | HOLD (conf 45); 1B/1Br/3N split; Q1 2026 earnings blowout (EPS $5.11 vs $2.62, revenue $109.9B, Cloud +63% YoY) gapped price +10% to $381.94 — prior bear-invalidation clause triggered; R/R 0.79:1 fails 2:1 minimum; RSI-7 97.75 extreme; wait for $342-358 pullback for 3:1+ R/R | wiki touched: tickers/GOOG/technicals.md, tickers/GOOG/catalysts.md, tickers/GOOG/thesis.md, tickers/GOOG/recent.md (created), LOG.md, INDEX.md
