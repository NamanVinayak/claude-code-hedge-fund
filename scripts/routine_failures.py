#!/usr/bin/env python3
"""
Classify every routine session whose status_category != "completed" by reading
status_detail and bucketing into:
  - usage_limit
  - timeout
  - tool_error
  - data_error
  - unknown   (printed verbatim so user can see what's hiding)

Also flag "completed but no decisions" sessions as a separate category, since
those are silent failures from the user's perspective.

Output: scripts/routine_failures.md
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
INPUT = SCRIPTS / "routine_raw_results_v2.json"
OUT = SCRIPTS / "routine_failures.md"

PATTERNS = [
    # "you've hit your limit · resets …" is also a usage cap (daily/hourly reset),
    # not just monthly. Catch it before tool_error grabs the word "tool".
    ("usage_limit", re.compile(r"(monthly usage limit|usage limit|hit your (org's |)limit|rate limit|out of credits)", re.I)),
    ("timeout",     re.compile(r"(timed? out|time.?out|stream idle timeout|exceeded.*time|deadline)", re.I)),
    ("tool_error",  re.compile(r"(tool execution failed|MCP error|subagent failed)", re.I)),
    ("data_error",  re.compile(r"(yfinance|EDGAR|fetch failed|finnhub)", re.I)),
]


def classify(detail: str) -> str:
    if not detail:
        return "no_detail"
    for label, pat in PATTERNS:
        if pat.search(detail):
            return label
    return "unknown"


def main() -> None:
    data = json.loads(INPUT.read_text())
    runs = data["runs"]

    failed = [r for r in runs if r.get("status") == "failed"]
    completed_no_dec = [r for r in runs if r.get("status") == "completed" and not r.get("decisions")]
    completed_with_dec = [r for r in runs if r.get("status") == "completed" and r.get("decisions")]

    # Categorize failures
    fail_buckets: dict[str, list[dict]] = defaultdict(list)
    for r in failed:
        fail_buckets[classify(r.get("status_detail", ""))].append(r)

    md = []
    md.append("# Claude Routines — Failure-mode Analysis\n")
    md.append(f"_Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} · "
              f"{len(runs)} sessions audited (Apr 17–27, trading routines only)._\n")

    md.append("## TL;DR\n")
    md.append(f"- **Sessions captured:** {len(runs)}")
    md.append(f"- **Completed with decisions written:** {len(completed_with_dec)}")
    md.append(f"- **Completed but no decisions written (silent failure):** {len(completed_no_dec)}")
    md.append(f"- **Explicitly failed:** {len(failed)}")
    md.append("")

    if failed:
        md.append("## Failure breakdown\n")
        md.append("| Category | Count | What this means |")
        md.append("|----------|------:|-----------------|")
        descriptions = {
            "usage_limit": "Hit your Anthropic monthly usage cap. Routine couldn't run at all or stopped mid-run.",
            "timeout":     "Session ran longer than allowed before completing.",
            "tool_error":  "A tool call (Bash/Write/Skill) errored out and the agent didn't recover.",
            "data_error":  "yfinance / EDGAR / Finnhub API failed to return data.",
            "unknown":     "Failure reason doesn't match a known pattern — see verbatim list below.",
            "no_detail":   "Status was 'failed' but Anthropic returned no reason.",
        }
        for cat in ("usage_limit", "timeout", "tool_error", "data_error", "unknown", "no_detail"):
            n = len(fail_buckets.get(cat, []))
            if n:
                md.append(f"| {cat} | {n} | {descriptions[cat]} |")
        md.append("")

        md.append("### Per-routine failure rate\n")
        md.append("| Routine | Total runs | Failed | Failure % |")
        md.append("|---------|----------:|-------:|----------:|")
        per_routine = Counter()
        per_routine_failed = Counter()
        for r in runs:
            per_routine[r["batch"]] += 1
            if r["status"] == "failed":
                per_routine_failed[r["batch"]] += 1
        for routine, total in sorted(per_routine.items()):
            f = per_routine_failed[routine]
            pct = f / total * 100 if total else 0
            md.append(f"| {routine} | {total} | {f} | {pct:.0f}% |")
        md.append("")

        md.append("### Every failed session (raw)\n")
        md.append("| Date | Routine | Session | Category | Status detail |")
        md.append("|------|---------|---------|----------|---------------|")
        for r in sorted(failed, key=lambda x: x.get("created_at", "")):
            cat = classify(r.get("status_detail", ""))
            sid_short = r["session_id"][-12:]
            detail = (r.get("status_detail") or "(none)").replace("|", "\\|").replace("\n", " ")
            md.append(f"| {r['created_at'][:10]} | {r['batch']} | …{sid_short} | {cat} | {detail} |")
        md.append("")

        unknowns = fail_buckets.get("unknown", []) + fail_buckets.get("no_detail", [])
        if unknowns:
            md.append("## Sessions whose failure reason doesn't match known patterns\n")
            md.append("These are the ones to investigate manually:\n")
            for r in unknowns:
                md.append(f"- **{r['created_at'][:10]}** · {r['batch']} · `{r['session_id']}` · "
                          f"branch `{r.get('branch')}` · detail: `{r.get('status_detail') or '(none)'}`")
            md.append("")

    if completed_no_dec:
        md.append("## Silent failures: completed but no decisions written\n")
        md.append("These ran to completion without errors, yet the agent never wrote "
                  "`runs/<id>/decisions.json`. Likely the routine decided 'no trades today' "
                  "or aborted mid-run after exceeding context.\n")
        md.append("| Date | Routine | Session | Events processed |")
        md.append("|------|---------|---------|----------------:|")
        for r in sorted(completed_no_dec, key=lambda x: x.get("created_at", "")):
            md.append(f"| {r['created_at'][:10]} | {r['batch']} | …{r['session_id'][-12:]} "
                      f"| {r.get('total_events', '?')} |")
        md.append("")

    md.append("## Answer to the original question\n")
    if failed:
        usage_n = len(fail_buckets.get("usage_limit", []))
        timeout_n = len(fail_buckets.get("timeout", []))
        other_n = len(failed) - usage_n - timeout_n
        md.append(f"Of {len(failed)} explicitly-failed routine sessions:\n")
        md.append(f"- **{usage_n} were usage-limit hits** (monthly cap, or daily/hourly resets)")
        md.append(f"- **{timeout_n} were timeouts** ('Stream idle timeout — partial response received')")
        md.append(f"- **{other_n} were other / no-detail failures**\n")
        if timeout_n > usage_n:
            md.append("So: **timeouts are the bigger problem, not usage limits.** Most failed routines are running so "
                      "long that the API stops streaming a response back. Worth shrinking each routine's scope "
                      "(fewer tickers per batch, fewer agents, or splitting into more triggers) before assuming "
                      "you need a bigger plan.\n")
        else:
            md.append("So: usage limits dominate. Increasing your plan or trimming routine scope will help.\n")
    else:
        md.append("No explicit failures captured — every failure surfaced as a silent 'completed without decisions'.\n")

    OUT.write_text("\n".join(md))
    print(f"wrote {OUT}")
    print(f"  {len(failed)} explicit failures, {len(completed_no_dec)} silent failures")
    print(f"  failure categories: {dict(Counter(classify(r.get('status_detail','')) for r in failed))}")


if __name__ == "__main__":
    main()
