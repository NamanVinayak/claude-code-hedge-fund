# ai_hedge/personas/ — Persona Helpers + Prompts

## Duplicate function rename map

Five function names existed in multiple upstream persona files. In `helpers.py` they are prefixed with a 2-letter persona code:

| Original | Renamed to (persona) |
|---|---|
| `analyze_management_quality` | `wb_analyze_management_quality` (Warren Buffett) |
| `analyze_management_quality` | `cm_analyze_management_quality` (Charlie Munger) |
| `calculate_intrinsic_value` | `wb_calculate_intrinsic_value` (Warren Buffett) |
| `calculate_intrinsic_value` | `rj_calculate_intrinsic_value` (Rakesh Jhunjhunwala) |
| `analyze_valuation` | `ba_analyze_valuation` (Bill Ackman) |
| `analyze_valuation` | `ga_analyze_valuation` (Growth Agent) |
| `analyze_sentiment` | `pl_analyze_sentiment` (Peter Lynch) |
| `analyze_sentiment` | `pf_analyze_sentiment` (Phil Fisher) |
| `analyze_sentiment` | `sd_analyze_sentiment` (Stanley Druckenmiller) |
| `analyze_insider_activity` | `pl_analyze_insider_activity` (Peter Lynch) |
| `analyze_insider_activity` | `pf_analyze_insider_activity` (Phil Fisher) |
| `analyze_insider_activity` | `sd_analyze_insider_activity` (Stanley Druckenmiller) |

## Persona codes

`wb`=warren_buffett, `cm`=charlie_munger, `bg`=ben_graham, `ba`=bill_ackman, `cw`=cathie_wood, `mb`=michael_burry, `nt`=nassim_taleb, `pl`=peter_lynch, `pf`=phil_fisher, `sd`=stanley_druckenmiller, `mp`=mohnish_pabrai, `rj`=rakesh_jhunjhunwala, `ad`=aswath_damodaran, `ga`=growth_agent, `ns`=news_sentiment
