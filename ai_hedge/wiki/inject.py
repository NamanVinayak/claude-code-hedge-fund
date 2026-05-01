"""Read-phase wiki integration.

After `build_swing_facts()` runs, we walk the agent manifest and merge a
`wiki_context` block into each existing facts file. Strategy agents see
that block alongside their normal indicators.

The wiki itself is never modified here. This module is purely the read
half of the wiki pipeline.

Feature-flagged. When `wiki_enabled` in tracker/watchlist.json is false,
all entry points are no-ops so the routine schedule is unaffected.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from ai_hedge.wiki.loader import (
    is_stale,
    page_path,
    parse_front_matter,
    read_full,
    read_tldr,
)
from ai_hedge.wiki.manifest import AGENT_MANIFEST


WATCHLIST_PATH = Path("tracker") / "watchlist.json"
WIKI_ROOT = Path("wiki")


def is_wiki_enabled(watchlist_path: Path | str = WATCHLIST_PATH) -> bool:
    """Read the wiki_enabled feature flag from tracker/watchlist.json."""
    p = Path(watchlist_path)
    if not p.exists():
        return False
    try:
        cfg = json.loads(p.read_text())
    except json.JSONDecodeError:
        return False
    return bool(cfg.get("settings", {}).get("wiki_enabled", False))


def _slice_for(category: str, basename: str, mode: str, ticker: str | None) -> dict[str, Any]:
    """Read one page slice and return a serialized dict for the facts bundle.

    Returns an empty dict when the page does not exist (caller will mark
    the slice with `new_ticker: true` at a higher level).
    """
    path = page_path(category, basename, ticker)
    if not path.exists():
        return {}
    fm = parse_front_matter(path)
    text = read_tldr(path) if mode == "tldr" else read_full(path)
    out = {
        "path": str(path),
        "mode": mode,
        "content": text,
        "last_updated": fm.get("last_updated"),
        "stale": is_stale(fm),
    }
    # Expose numeric confidence_score from thesis pages (set by the daily
    # lesson writer on every closed trade: -10 on stop_hit/expired, +5 on
    # target_hit, clamped to [0,100]; default 70). Agents read this as a
    # confidence dial — low score = thesis has been losing recently.
    if basename == "thesis" and "confidence_score" in fm:
        out["confidence_score"] = fm["confidence_score"]
    return out


def build_wiki_context(agent: str, ticker: str) -> dict[str, Any]:
    """Assemble the `wiki_context` block for one (agent, ticker)."""
    entries = AGENT_MANIFEST.get(agent, [])
    if not entries:
        return {}

    slices: dict[str, dict[str, Any]] = {}
    any_ticker_page_exists = False
    needs_ticker_page = False

    for category, basename, mode in entries:
        # Slice key is e.g. "thesis_tldr", "technicals_full", "regime_tldr".
        key = f"{basename}_{mode}"
        if category == "ticker":
            needs_ticker_page = True
            slc = _slice_for(category, basename, mode, ticker)
            if slc:
                any_ticker_page_exists = True
            slices[key] = slc or {"missing": True, "mode": mode}
        else:
            slc = _slice_for(category, basename, mode, ticker=None)
            slices[key] = slc or {"missing": True, "mode": mode}

    out: dict[str, Any] = {"slices": slices}
    if needs_ticker_page and not any_ticker_page_exists:
        out["new_ticker"] = True
    return out


def inject_context(run_id: str, tickers: list[str], mode: str = "swing") -> dict[str, Any]:
    """Merge `wiki_context` into every relevant facts file for a run.

    Idempotent: rewrites each touched facts file with the new key. If the
    feature flag is off, this is a no-op and returns {"skipped": True}.

    Returns a small report dict (used by tests + the bootstrap script).
    """
    if not is_wiki_enabled():
        return {"skipped": True, "reason": "wiki_enabled=false"}

    if mode != "swing":
        # Phase 1 is swing-only.
        return {"skipped": True, "reason": f"mode={mode} not supported in Phase 1"}

    facts_dir = Path("runs") / run_id / "facts"
    if not facts_dir.exists():
        return {"skipped": True, "reason": "facts dir missing"}

    written: list[str] = []
    for agent in AGENT_MANIFEST:
        for ticker in tickers:
            facts_path = facts_dir / f"{agent}__{ticker.upper()}.json"
            if not facts_path.exists():
                continue
            try:
                data = json.loads(facts_path.read_text())
            except json.JSONDecodeError:
                continue
            data["wiki_context"] = build_wiki_context(agent, ticker)
            facts_path.write_text(json.dumps(data, indent=2, default=str))
            written.append(str(facts_path))

    return {"skipped": False, "written": written, "count": len(written)}


def touch_index(run_id: str) -> None:
    """Rewrite `wiki/INDEX.md` last_updated dates after a run.

    Lightweight: walks `wiki/` and regenerates the catalog from each
    page's front-matter. Cheap (<1s) and deterministic.
    """
    if not is_wiki_enabled():
        return

    index_path = WIKI_ROOT / "INDEX.md"
    if not WIKI_ROOT.exists():
        return

    rows: list[tuple[str, str, str]] = []  # (display_path, last_updated, summary)
    for md_path in sorted(WIKI_ROOT.rglob("*.md")):
        rel = md_path.relative_to(WIKI_ROOT)
        if rel.name in ("INDEX.md", "LOG.md", "README.md"):
            continue
        if rel.parts and rel.parts[0] == "_archive":
            continue
        fm = parse_front_matter(md_path)
        last = str(fm.get("last_updated") or "—")
        summary = str(fm.get("summary") or "")
        rows.append((str(rel), last, summary))

    today = date.today().isoformat()
    lines = [
        "---",
        f"name: wiki index",
        f"last_updated: {today}",
        f"last_run_id: {run_id}",
        "---",
        "",
        "# Wiki Index",
        "",
        f"Auto-regenerated by `finalize.py` after run `{run_id}`. Do not edit by hand.",
        "",
    ]
    if not rows:
        lines.append("_No pages yet — bootstrap has not run._")
    else:
        for display, last, summary in rows:
            suffix = f" — {summary}" if summary else ""
            lines.append(f"- [{display}]({display}) — last_updated {last}{suffix}")
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(lines) + "\n")


__all__ = [
    "build_wiki_context",
    "inject_context",
    "is_wiki_enabled",
    "touch_index",
]
