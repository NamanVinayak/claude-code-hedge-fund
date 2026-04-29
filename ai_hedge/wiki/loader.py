"""Read wiki pages off disk.

Three jobs:
- parse the YAML front-matter of a page,
- read the full body (everything after the front-matter),
- read just the TL;DR section (between `## TL;DR` and the next `## ` heading).

We deliberately do NOT use PyYAML — the front-matter we write is a tiny
flat key:value block; a hand parser is enough and avoids a dep.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

WIKI_ROOT = Path("wiki")


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Return (front_matter_dict, body) from a markdown file's text."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw_fm = parts[1]
    body = parts[2].lstrip("\n")
    fm: dict[str, Any] = {}
    for line in raw_fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() in ("true", "false"):
            fm[key] = (value.lower() == "true")
        else:
            try:
                fm[key] = int(value)
            except ValueError:
                fm[key] = value
    return fm, body


def parse_front_matter(path: Path | str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    fm, _ = _split_front_matter(p.read_text())
    return fm


def read_full(path: Path | str) -> str:
    """Body of the page (front-matter stripped). Empty string if missing."""
    p = Path(path)
    if not p.exists():
        return ""
    _, body = _split_front_matter(p.read_text())
    return body


def read_tldr(path: Path | str) -> str:
    """Return the TL;DR section text only.

    Looks for a heading `## TL;DR` and returns everything until the next
    `## ` heading (exclusive). Heading line itself is NOT included.
    """
    body = read_full(path)
    if not body:
        return ""
    lines = body.splitlines()
    in_tldr = False
    out: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            if not in_tldr and heading.startswith("tl;dr"):
                in_tldr = True
                continue
            if in_tldr:
                break  # next H2 — TL;DR is over
        if in_tldr:
            out.append(line)
    return "\n".join(out).strip()


def is_stale(front_matter: dict[str, Any], today: date | None = None) -> bool:
    """True if last_updated is older than stale_after_days."""
    today = today or date.today()
    raw = front_matter.get("last_updated")
    days = front_matter.get("stale_after_days", 30)
    if not raw:
        return False
    try:
        last = datetime.fromisoformat(str(raw)).date()
    except ValueError:
        return False
    try:
        return (today - last) > timedelta(days=int(days))
    except (TypeError, ValueError):
        return False


def page_path(category: str, basename: str, ticker: str | None = None) -> Path:
    """Return the wiki path for a given (category, basename, ticker)."""
    if category == "ticker":
        if not ticker:
            raise ValueError("ticker category requires a ticker")
        return WIKI_ROOT / "tickers" / ticker.upper() / f"{basename}.md"
    if category == "macro":
        return WIKI_ROOT / "macro" / f"{basename}.md"
    if category == "meta":
        return WIKI_ROOT / "meta" / f"{basename}.md"
    raise ValueError(f"unknown wiki category: {category}")
