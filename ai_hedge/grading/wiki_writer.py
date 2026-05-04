"""Append graded persona calls to `wiki/agents/<persona>/track_record.md`.

Called from finalize.py after the run's summary is written. Idempotent: if
this run_id has already been appended, the call is a no-op.

V1 keeps the markdown body simple: a YAML front-matter block + a single
"## Graded calls log" section of dated bullets. Aggregate statistics are
deferred to V2 (when enough data accumulates to be informative).
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


WIKI_AGENTS_ROOT = Path("wiki") / "agents"


_FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _bootstrap_body(persona: str, today: str, run_id: str) -> str:
    return f"""---
name: {persona} track record
last_updated: {today}
last_run_id: {run_id}
stale_after_days: 365
target_words: 1200
summary: 0 graded calls. (Appended by ai_hedge.grading.wiki_writer.)
---

# {persona} — Track Record

Auto-appended by the grading pipeline after each swing run. Each bullet is
one resolved call scored against yfinance daily OHLC.

## Graded calls log

"""


def _bullet(verdict: dict[str, Any]) -> str:
    """Format one verdict as a single log bullet."""
    direction = verdict.get("prior_signal", "?")
    entry = verdict.get("prior_entry")
    target = verdict.get("prior_target")
    stop = verdict.get("prior_stop")
    v = verdict.get("verdict", "?")
    days = verdict.get("days_elapsed")
    mfe = verdict.get("mfe_pct")
    mae = verdict.get("mae_pct")
    first_hit_date = verdict.get("first_hit_date") or "—"
    tie = " [tie-broken]" if verdict.get("tie_breaker_applied") else ""
    ticker = verdict.get("ticker", "?")
    run_id = verdict.get("run_id", "?")
    prior_run_id = verdict.get("prior_run_id", "?")
    return (
        f"- {first_hit_date} | {ticker} | {direction} ${entry}→${target} "
        f"stop ${stop} | **{v}** (day {days}, MFE {mfe}%, MAE {mae}%){tie} "
        f"_(prior_run={prior_run_id}, graded_in={run_id})_"
    )


def _read_grading_files(run_id: str, runs_root: Path) -> list[dict]:
    """Load every `runs/<id>/grading/*.json` for this run."""
    grading_dir = runs_root / run_id / "grading"
    if not grading_dir.exists():
        return []
    out: list[dict] = []
    for path in sorted(grading_dir.glob("*.json")):
        try:
            out.append(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def _update_front_matter(body: str, today: str, run_id: str, total_calls: int) -> str:
    """Rewrite the front-matter `last_updated`, `last_run_id`, `summary` fields."""
    match = _FRONT_MATTER_RE.match(body)
    if not match:
        return body  # malformed, leave alone
    fm = match.group(1)

    def _set(field: str, value: str, fm_text: str) -> str:
        pattern = re.compile(rf"^{re.escape(field)}:\s*.*$", re.MULTILINE)
        repl = f"{field}: {value}"
        if pattern.search(fm_text):
            return pattern.sub(repl, fm_text, count=1)
        return fm_text + f"\n{repl}"

    fm = _set("last_updated", today, fm)
    fm = _set("last_run_id", run_id, fm)
    fm = _set(
        "summary",
        f"{total_calls} graded calls. (Appended by ai_hedge.grading.wiki_writer.)",
        fm,
    )
    return f"---\n{fm}\n---\n" + body[match.end():]


def _already_appended(body: str, run_id: str) -> bool:
    return f"graded_in={run_id}" in body


def append_track_records(
    run_id: str,
    runs_root: str | Path = "runs",
    wiki_agents_root: str | Path = WIKI_AGENTS_ROOT,
    today: date | None = None,
) -> dict[str, Any]:
    """Group verdicts by persona and append bullets. Idempotent on run_id."""
    runs_root = Path(runs_root)
    wiki_agents_root = Path(wiki_agents_root)
    today_str = (today or date.today()).isoformat()

    verdicts = _read_grading_files(run_id, runs_root)
    if not verdicts:
        return {"skipped": True, "reason": "no grading files", "appended": 0}

    by_persona: dict[str, list[dict]] = {}
    for v in verdicts:
        persona = v.get("persona")
        if not persona:
            continue
        by_persona.setdefault(persona, []).append(v)

    appended_files = 0
    skipped_idempotent = 0

    for persona, items in by_persona.items():
        persona_dir = wiki_agents_root / persona
        persona_dir.mkdir(parents=True, exist_ok=True)
        track_path = persona_dir / "track_record.md"

        if track_path.exists():
            body = track_path.read_text()
        else:
            body = _bootstrap_body(persona, today_str, run_id)

        if _already_appended(body, run_id):
            skipped_idempotent += 1
            continue

        # Append bullets at end of file.
        bullets = "\n".join(_bullet(v) for v in items)
        if not body.endswith("\n"):
            body += "\n"
        body += bullets + "\n"

        # Total calls = number of bullets in the log section. Cheap regex.
        total_calls = len(re.findall(r"^- \d{4}-\d{2}-\d{2}", body, re.MULTILINE))
        # Bootstrap header bullet ("## Graded calls log") doesn't match.

        body = _update_front_matter(body, today_str, run_id, total_calls)
        track_path.write_text(body)
        appended_files += 1

    return {
        "skipped": False,
        "appended": appended_files,
        "skipped_idempotent": skipped_idempotent,
        "verdict_count": len(verdicts),
    }


__all__ = ["append_track_records"]
