"""One-time wiki bootstrap orchestrator.

Phase 1 scope: identify the universe (tracker.db + watchlist.json), refuse
to run if any swing routine is in flight, then **prepare** per-ticker
input bundles for the `wiki_bootstrap` agent and seed skeleton pages from
templates so the wiki is non-empty before the next run.

This script does NOT dispatch the LLM bootstrap agent itself — Claude
Code is the orchestrator that dispatches subagents. Operator workflow:

1. Run this script. It writes:
   - `wiki/_bootstrap_manifest.json` listing the tickers needing real
     bootstrap and the run-history slices to feed each `wiki_bootstrap`
     dispatch.
   - Skeleton placeholder pages from `ai_hedge.wiki.templates` so the
     read-phase injector has *something* to inject on the next run.
2. Operator dispatches `wiki_bootstrap` agents per
   `_bootstrap_manifest.json` (one per ticker, one for macro). Each
   agent reads its slice and writes the real page.
3. Operator runs `python -c "from ai_hedge.wiki import lint; print(lint.lint_directory())"`
   to confirm the wiki is clean.

Phase 2 will replace step (1)+(2) with a single end-to-end runner that
dispatches the agents directly.

Recommended Sunday cron entry for the (Phase-2) compactor — kept here so
the operator has a single place to find it:

    0 16 * * 0 cd /Users/naman/Downloads/artist && .venv/bin/python -m scripts.wiki_compactor
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_hedge.wiki import templates


ROOT = Path(__file__).resolve().parent.parent
RUN_INDEX = ROOT / "runs" / "index.json"
WATCHLIST = ROOT / "tracker" / "watchlist.json"
WIKI_ROOT = ROOT / "wiki"
BOOTSTRAP_MANIFEST = WIKI_ROOT / "_bootstrap_manifest.json"


def _abort_if_run_in_progress() -> None:
    if not RUN_INDEX.exists():
        return
    try:
        entries = json.loads(RUN_INDEX.read_text())
    except json.JSONDecodeError:
        return
    in_progress = [e for e in entries if e.get("status") == "in_progress"]
    if in_progress:
        names = ", ".join(e.get("run_id", "?") for e in in_progress)
        sys.exit(
            f"refused: run(s) in progress per runs/index.json: {names}\n"
            f"wait for completion (or close the index entries) before bootstrapping."
        )


def _watchlist_tickers() -> list[str]:
    if not WATCHLIST.exists():
        return []
    try:
        cfg = json.loads(WATCHLIST.read_text())
    except json.JSONDecodeError:
        return []
    universe: set[str] = set()
    for sched in cfg.get("schedules", []):
        if sched.get("mode") == "swing":
            for t in sched.get("tickers", []) or []:
                universe.add(t.upper())
    return sorted(universe)


def _tracker_tickers() -> list[str]:
    """Pull recent tickers from tracker.db (last 90 days)."""
    try:
        from sqlalchemy import create_engine, text  # type: ignore
    except Exception:
        return []
    db = ROOT / "tracker" / "tracker.db"
    if not db.exists():
        return []
    try:
        engine = create_engine(f"sqlite:///{db}")
        with engine.connect() as conn:
            rows = conn.execute(
                text(
                    "SELECT DISTINCT ticker FROM trades "
                    "WHERE created_at >= datetime('now', '-90 days')"
                )
            )
            return sorted({r[0].upper() for r in rows if r[0]})
    except Exception:
        return []


def _recent_swing_runs(ticker: str, limit: int = 5) -> list[dict]:
    if not RUN_INDEX.exists():
        return []
    try:
        entries = json.loads(RUN_INDEX.read_text())
    except json.JSONDecodeError:
        return []
    matching = [
        e for e in entries
        if e.get("mode") == "swing"
        and e.get("status") == "completed"
        and ticker.upper() in [t.upper() for t in (e.get("tickers") or [])]
    ]
    matching.sort(key=lambda e: e.get("started_at") or "", reverse=True)
    return matching[:limit]


def _seed_skeleton(ticker: str) -> list[str]:
    """Write skeleton pages so read-phase injection has something to load."""
    folder = WIKI_ROOT / "tickers" / ticker
    folder.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for kind in ("thesis", "technicals", "catalysts", "trades"):
        path = folder / f"{kind}.md"
        if path.exists():
            continue
        path.write_text(templates.render(kind, ticker))
        written.append(str(path.relative_to(ROOT)))
    return written


def _seed_macro() -> list[str]:
    folder = WIKI_ROOT / "macro"
    folder.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    path = folder / "regime.md"
    if not path.exists():
        path.write_text(templates.render("regime"))
        written.append(str(path.relative_to(ROOT)))
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report planned work but do not write any files",
    )
    args = parser.parse_args(argv)

    _abort_if_run_in_progress()

    universe = sorted(set(_watchlist_tickers()) | set(_tracker_tickers()))
    if not universe:
        print("no tickers found in watchlist.json or tracker.db — nothing to do.")
        return 0

    plan = []
    seeded: list[str] = []
    for t in universe:
        plan.append({
            "scope": t,
            "recent_runs": _recent_swing_runs(t),
            "expected_pages": [
                f"wiki/tickers/{t}/thesis.md",
                f"wiki/tickers/{t}/technicals.md",
                f"wiki/tickers/{t}/catalysts.md",
                f"wiki/tickers/{t}/trades.md",
            ],
        })
        if not args.dry_run:
            seeded.extend(_seed_skeleton(t))

    plan.append({"scope": "MACRO", "expected_pages": ["wiki/macro/regime.md"]})
    if not args.dry_run:
        seeded.extend(_seed_macro())

    if not args.dry_run:
        BOOTSTRAP_MANIFEST.write_text(json.dumps(plan, indent=2))
    print(f"universe size: {len(universe)} tickers")
    print(f"skeletons seeded: {len(seeded)}")
    if seeded:
        for p in seeded:
            print(f"  + {p}")
    if not args.dry_run:
        print(f"manifest: {BOOTSTRAP_MANIFEST.relative_to(ROOT)}")
    print("next: dispatch wiki_bootstrap agents per the manifest, then re-run lint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
