#!/usr/bin/env python3
"""
Consolidate routine_raw_results_v2_intermediate.json (Playwright fetch output)
into scripts/routine_raw_results_v2.json with the same schema as v1, plus
crypto routines and updated date range (Apr 17 -> Apr 27).
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
INTERMEDIATE = ROOT.parent / "routine_raw_results_v2_intermediate.json"
OUT = ROOT / "routine_raw_results_v2.json"


def parse_run_id(path: str) -> str | None:
    m = re.search(r"/runs/([0-9_]+)/decisions\.json", path)
    return m.group(1) if m else None


def main() -> None:
    raw = json.loads(INTERMEDIATE.read_text())
    if isinstance(raw, str):
        raw = json.loads(raw)

    runs = []
    for s in raw:
        decisions_writes = s.get("decisions_writes") or []
        # Use the LAST write (Write overwrites file)
        final_decisions = None
        run_id = None
        if decisions_writes:
            last = decisions_writes[-1]
            run_id = parse_run_id(last.get("path", "")) or s["created_at"][:10].replace("-", "_")
            try:
                content = json.loads(last["content"])
                final_decisions = content.get("decisions", content)
            except json.JSONDecodeError:
                final_decisions = None

        runs.append({
            "batch": s.get("trigger_name", "").strip(),
            "trigger_id": s.get("trigger_id"),
            "session_id": s.get("session_id"),
            "created_at": s.get("created_at"),
            "origin": s.get("origin"),
            "status": s.get("status_category") or "completed",
            "status_detail": s.get("status_detail") or "",
            "branch": s.get("branch"),
            "run_id": run_id,
            "source": "playwright_v2_events_write_tool" if final_decisions else "no_decisions_extracted",
            "total_events": s.get("total_events"),
            "decisions": final_decisions,
        })

    # Sort by created_at ascending
    runs.sort(key=lambda r: r["created_at"] or "")

    triggers_seen = {r["batch"]: r["trigger_id"] for r in runs}

    sessions_with_decisions = sum(1 for r in runs if r["decisions"])
    completed_with_decisions = sum(1 for r in runs if r["decisions"] and r["status"] == "completed")
    failed_with_decisions = sum(1 for r in runs if r["decisions"] and r["status"] == "failed")
    no_decisions = sum(1 for r in runs if not r["decisions"])

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Playwright MCP -> claude.ai /v1/sessions/<id>/events",
        "scope": "Stock Swing Batch 1+2, Crypto Morning, Crypto Evening (IPL routines excluded)",
        "routines": triggers_seen,
        "summary": {
            "total_sessions": len(runs),
            "sessions_with_decisions": sessions_with_decisions,
            "completed_with_decisions": completed_with_decisions,
            "failed_with_decisions": failed_with_decisions,
            "sessions_without_decisions": no_decisions,
        },
        "runs": runs,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    print(f"  {len(runs)} sessions, {sessions_with_decisions} with decisions")
    print(f"  date range: {min(r['created_at'][:10] for r in runs)} -> {max(r['created_at'][:10] for r in runs)}")
    print()
    print("By trigger / status / has-decisions:")
    c = Counter()
    for r in runs:
        c[(r["batch"], r["status"], "yes" if r["decisions"] else "no")] += 1
    for k, v in sorted(c.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
