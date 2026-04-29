"""Wiki compactor — deterministic housekeeping for wiki/.

Run independently on a Sunday cron (recommended: 0 16 * * 0):
    cd /Users/naman/Downloads/artist && .venv/bin/python -m scripts.wiki_compactor

Dry-run mode (no file changes, just report):
    .venv/bin/python -m scripts.wiki_compactor --dry-run

Operations (in order):
  1. Load every wiki page; collect metadata from front-matter.
  2. Word-budget check: flag pages exceeding target_words * 1.2.
  3. Trade tier rolling on tickers/<T>/trades.md.
  4. recent.md pruning: drop dated bullets > 30 days old.
  5. LOG.md rolling: entries > 60d → weekly summary; > 365d → monthly summary.
  6. Orphan detection: folders idle > 60d and not in watchlist.
  7. Stale flag: pages not updated within stale_after_days.
  8. Cross-ref check: broken markdown links.
  9. Front-matter integrity: required key check.

Outputs:
    wiki/meta/compactor_log.md  — append one section per run
    scripts/wiki_lint_report.md — overwrite with current flag state
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).parent.parent
WIKI_ROOT = REPO_ROOT / "wiki"
WATCHLIST_PATH = REPO_ROOT / "tracker" / "watchlist.json"
COMPACTOR_LOG = WIKI_ROOT / "meta" / "compactor_log.md"
LINT_REPORT = REPO_ROOT / "scripts" / "wiki_lint_report.md"

REQUIRED_FM_KEYS = ("name", "last_updated", "target_words", "stale_after_days")
TRADE_SECTION_30D = "Closed — last 30 days"
TRADE_SECTION_MONTHLY = "Closed — older, rolled by month"
TRADE_SECTION_6M = "Closed — older than 6 months"

# ─── helpers ─────────────────────────────────────────────────────────────────


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict[str, Any] = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            try:
                fm[key] = int(val)
            except ValueError:
                fm[key] = val
    return fm, parts[2].lstrip("\n")


def _word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(str(s), fmt).date()
        except ValueError:
            continue
    return None


def _load_watchlist_tickers() -> set[str]:
    """Return uppercase ticker symbols from tracker/watchlist.json."""
    if not WATCHLIST_PATH.exists():
        return set()
    try:
        data = json.loads(WATCHLIST_PATH.read_text())
    except json.JSONDecodeError:
        return set()
    tickers: set[str] = set()
    for item in data.get("tickers", []):
        sym = item.get("symbol", "") if isinstance(item, dict) else str(item)
        if sym:
            tickers.add(sym.upper())
    return tickers


def _collect_wiki_pages() -> list[Path]:
    """All .md files under wiki/ excluding INDEX, LOG, README and _archive."""
    pages = []
    for p in sorted(WIKI_ROOT.rglob("*.md")):
        rel = p.relative_to(WIKI_ROOT)
        if rel.name in ("INDEX.md", "LOG.md", "README.md"):
            continue
        if rel.parts and rel.parts[0] == "_archive":
            continue
        pages.append(p)
    return pages


# ─── operations ──────────────────────────────────────────────────────────────


def check_word_budgets(pages: list[Path]) -> list[str]:
    """Flag pages exceeding target_words * 1.2. Returns list of flag strings."""
    flags: list[str] = []
    for p in pages:
        fm, body = _split_front_matter(p.read_text())
        target = fm.get("target_words")
        if not isinstance(target, int) or target <= 0:
            continue
        actual = _word_count(body)
        cap = int(target * 1.2)
        if actual > cap:
            flags.append(f"OVERSIZE {p.relative_to(REPO_ROOT)}: {actual} words (cap {cap}, target {target})")
    return flags


def check_front_matter(pages: list[Path]) -> list[str]:
    flags: list[str] = []
    for p in pages:
        fm, _ = _split_front_matter(p.read_text())
        missing = [k for k in REQUIRED_FM_KEYS if k not in fm]
        if missing:
            flags.append(
                f"FRONT_MATTER {p.relative_to(REPO_ROOT)}: missing keys {missing}"
            )
    return flags


def check_stale(pages: list[Path], today: date) -> list[str]:
    flags: list[str] = []
    for p in pages:
        fm, _ = _split_front_matter(p.read_text())
        last_upd = _parse_date(str(fm.get("last_updated", "")))
        stale_days = fm.get("stale_after_days", 30)
        if last_upd and (today - last_upd) > timedelta(days=int(stale_days)):
            flags.append(
                f"STALE {p.relative_to(REPO_ROOT)}: last_updated {last_upd}"
                f" ({(today-last_upd).days}d ago, limit {stale_days}d)"
            )
    return flags


def check_cross_refs(pages: list[Path]) -> list[str]:
    """Find markdown links that point to missing files."""
    flags: list[str] = []
    link_re = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for p in pages:
        text = p.read_text()
        for _, href in link_re.findall(text):
            if href.startswith("http") or href.startswith("#"):
                continue
            # Resolve relative to the page's directory
            target = (p.parent / href).resolve()
            if not target.exists():
                flags.append(
                    f"BROKEN_XREF {p.relative_to(REPO_ROOT)}: link to '{href}' not found"
                )
    return flags


def roll_trades(trades_path: Path, today: date, dry_run: bool) -> int:
    """Roll closed trade entries in trades.md down the tier ladder.

    Returns count of entries rolled. Skips silently if sections are missing.
    """
    if not trades_path.exists():
        return 0
    text = trades_path.read_text()
    fm_text, body = _split_front_matter(text) if text.startswith("---") else ({}, text)

    # We need to find the sections by heading
    def _section_bounds(content: str, heading: str) -> tuple[int, int] | None:
        """Return (start_line_idx, end_line_idx_exclusive) of a section."""
        lines = content.splitlines(keepends=True)
        start = None
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == f"## {heading}":
                start = i
            elif start is not None and stripped.startswith("## ") and stripped != f"## {heading}":
                return (start, i)
        if start is not None:
            return (start, len(lines))
        return None

    bounds_30d = _section_bounds(body, TRADE_SECTION_30D)
    if not bounds_30d:
        return 0

    bounds_monthly = _section_bounds(body, TRADE_SECTION_MONTHLY)
    bounds_6m = _section_bounds(body, TRADE_SECTION_6M)

    lines = body.splitlines(keepends=True)
    section_30d_lines = lines[bounds_30d[0] + 1 : bounds_30d[1]]

    # Find entries with dates in the "last 30 days" section.
    # An entry is a block starting with a date-like heading: ### YYYY-MM-DD or
    # a date pattern on its own line.
    date_re = re.compile(r"(\d{4}-\d{2}-\d{2})")

    rolled_to_monthly: list[str] = []
    kept_in_30d: list[str] = []
    current_block: list[str] = []
    current_date: date | None = None

    def _flush_block():
        nonlocal current_block, current_date
        if not current_block:
            return
        if current_date and (today - current_date) > timedelta(days=30):
            summary = f"- {current_date} | {' '.join(''.join(current_block).split()[:15])}...\n"
            rolled_to_monthly.append(summary)
        else:
            kept_in_30d.extend(current_block)
        current_block = []
        current_date = None

    for line in section_30d_lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            _flush_block()
            m = date_re.search(stripped)
            current_date = _parse_date(m.group(1)) if m else None
            current_block = [line]
        else:
            current_block.append(line)

    _flush_block()

    if not rolled_to_monthly:
        return 0

    # Rebuild body with changes
    new_30d = f"## {TRADE_SECTION_30D}\n" + "".join(kept_in_30d)

    # Splice rolled entries into monthly section (or create it)
    if bounds_monthly:
        monthly_lines = lines[bounds_monthly[0] + 1 : bounds_monthly[1]]
        # Also roll monthly entries > 6 months into 6m section
        rolled_to_6m: list[str] = []
        kept_monthly: list[str] = []
        for mline in monthly_lines:
            m = date_re.search(mline)
            if m:
                d = _parse_date(m.group(1))
                if d and (today - d) > timedelta(days=180):
                    rolled_to_6m.append(mline)
                else:
                    kept_monthly.append(mline)
            else:
                kept_monthly.append(mline)
        new_monthly = (
            f"## {TRADE_SECTION_MONTHLY}\n"
            + "".join(kept_monthly)
            + "".join(rolled_to_monthly)
        )
        # Update 6m section
        if rolled_to_6m and bounds_6m:
            sixm_lines = lines[bounds_6m[0] + 1 : bounds_6m[1]]
            new_6m = f"## {TRADE_SECTION_6M}\n" + "".join(sixm_lines) + "".join(rolled_to_6m)
        elif rolled_to_6m:
            new_6m = f"## {TRADE_SECTION_6M}\n" + "".join(rolled_to_6m)
        else:
            new_6m = None
    else:
        kept_monthly = []
        new_monthly = (
            f"## {TRADE_SECTION_MONTHLY}\n" + "".join(rolled_to_monthly)
        )
        new_6m = None

    # Reconstruct body: keep lines outside the sections we touched
    touched_ranges = sorted(
        filter(None, [bounds_30d, bounds_monthly, bounds_6m]),
        key=lambda x: x[0],
    )

    rebuilt: list[str] = []
    prev_end = 0
    for (s, e) in touched_ranges:
        rebuilt.extend(lines[prev_end:s])
        prev_end = e

    rebuilt.extend(lines[prev_end:])

    # Now insert the new section blocks at their original positions (in order)
    # This is simpler: just do a text replace on the original body
    def _replace_section(content: str, heading: str, new_block: str) -> str:
        pattern = re.compile(
            rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)", re.DOTALL
        )
        replacement = new_block.rstrip("\n")
        result = pattern.sub(replacement, content, count=1)
        return result

    new_body = body
    new_body = _replace_section(new_body, TRADE_SECTION_30D, new_30d)
    new_body = _replace_section(new_body, TRADE_SECTION_MONTHLY, new_monthly)
    if new_6m:
        if bounds_6m:
            new_body = _replace_section(new_body, TRADE_SECTION_6M, new_6m)
        else:
            new_body = new_body.rstrip("\n") + "\n\n" + new_6m + "\n"

    if dry_run:
        return len(rolled_to_monthly)

    # Reconstruct full file with front-matter
    if text.startswith("---"):
        parts = text.split("---", 2)
        new_text = f"---{parts[1]}---\n\n{new_body}"
    else:
        new_text = new_body

    trades_path.write_text(new_text)
    return len(rolled_to_monthly)


def prune_recent(recent_path: Path, today: date, dry_run: bool) -> int:
    """Drop dated bullets in recent.md older than 30 days. Returns dropped count."""
    if not recent_path.exists():
        return 0
    text = recent_path.read_text()
    _, body = _split_front_matter(text)
    date_re = re.compile(r"^[-*]\s+\*?\*?(\d{4}-\d{2}-\d{2})")
    kept: list[str] = []
    dropped = 0
    for line in body.splitlines(keepends=True):
        m = date_re.match(line.strip())
        if m:
            d = _parse_date(m.group(1))
            if d and (today - d) > timedelta(days=30):
                dropped += 1
                continue
        kept.append(line)
    if dropped == 0 or dry_run:
        return dropped
    if text.startswith("---"):
        parts = text.split("---", 2)
        new_text = f"---{parts[1]}---\n\n{''.join(kept)}"
    else:
        new_text = "".join(kept)
    recent_path.write_text(new_text)
    return dropped


def roll_log(log_path: Path, today: date, dry_run: bool) -> int:
    """Roll LOG.md entries. Returns count of entries rolled."""
    if not log_path.exists():
        return 0
    text = log_path.read_text()

    # Split into preamble + entries
    entry_re = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\](.*)$", re.MULTILINE)
    matches = list(entry_re.finditer(text))
    if not matches:
        return 0

    preamble = text[: matches[0].start()]

    # Parse each entry and its date
    entries: list[tuple[date, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        full_line = text[m.start() : end].rstrip("\n")
        d = _parse_date(m.group(1))
        if d:
            entries.append((d, full_line))

    # Bucket entries
    recent: list[tuple[date, str]] = []
    mid: list[tuple[date, str]] = []  # 60-365 days → weekly summaries
    old: list[tuple[date, str]] = []  # >365 days → monthly summaries

    for d, line in entries:
        age = (today - d).days
        if age <= 60:
            recent.append((d, line))
        elif age <= 365:
            mid.append((d, line))
        else:
            old.append((d, line))

    rolled = len(mid) + len(old)
    if rolled == 0 or dry_run:
        return rolled

    # Build weekly summaries for mid-range
    weeks: dict[date, list[str]] = defaultdict(list)
    for d, line in mid:
        # ISO week Monday
        week_start = d - timedelta(days=d.weekday())
        weeks[week_start].append(line.splitlines()[0])

    weekly_lines: list[str] = []
    for ws in sorted(weeks):
        count = len(weeks[ws])
        weekly_lines.append(
            f"## [{ws.isoformat()}] weekly-summary | {count} run(s) rolled from this week\n"
        )

    # Build monthly summaries for old entries
    months: dict[str, list[str]] = defaultdict(list)
    for d, line in old:
        key = f"{d.year}-{d.month:02d}"
        months[key].append(line.splitlines()[0])

    monthly_lines: list[str] = []
    for ym in sorted(months):
        count = len(months[ym])
        monthly_lines.append(
            f"## [{ym}-01] monthly-summary | {count} run(s) rolled from {ym}\n"
        )

    new_text = (
        preamble
        + "".join(monthly_lines)
        + "".join(weekly_lines)
        + "\n".join(line for _, line in recent)
        + "\n"
    )
    if not dry_run:
        log_path.write_text(new_text)
    return rolled


def detect_orphans(tickers_dir: Path, watchlist_tickers: set[str], today: date) -> list[str]:
    """Find ticker folders idle > 60 days and not in watchlist."""
    orphans: list[str] = []
    if not tickers_dir.exists():
        return orphans
    for folder in sorted(tickers_dir.iterdir()):
        if not folder.is_dir():
            continue
        ticker = folder.name
        if ticker.startswith("_"):
            continue
        if ticker in watchlist_tickers:
            continue
        # Find most recently modified page
        pages = list(folder.rglob("*.md"))
        if not pages:
            orphans.append(ticker)
            continue
        latest_mtime = max(p.stat().st_mtime for p in pages)
        latest_date = date.fromtimestamp(latest_mtime)
        if (today - latest_date).days > 60:
            orphans.append(ticker)
    return orphans


def archive_orphans(orphans: list[str], tickers_dir: Path, archive_dir: Path, dry_run: bool) -> list[str]:
    archived: list[str] = []
    for ticker in orphans:
        src = tickers_dir / ticker
        dst = archive_dir / ticker
        if dry_run:
            archived.append(ticker)
            continue
        if src.exists():
            archive_dir.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
            archived.append(ticker)
    return archived


# ─── output ──────────────────────────────────────────────────────────────────


def write_lint_report(flags: list[str]) -> None:
    content = f"# Wiki Lint Report\n\nGenerated: {date.today().isoformat()}\n\n"
    if not flags:
        content += "_No issues found._\n"
    else:
        content += f"**{len(flags)} item(s) need review:**\n\n"
        for f in flags:
            content += f"- {f}\n"
    LINT_REPORT.write_text(content)


def append_compactor_log(
    today: date,
    dry_run: bool,
    rolled_count: int,
    archived_count: int,
    flags: list[str],
) -> None:
    COMPACTOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    existing = COMPACTOR_LOG.read_text() if COMPACTOR_LOG.exists() else "# Compactor Log\n\n"
    mode_tag = "[DRY-RUN] " if dry_run else ""
    section = (
        f"\n## {mode_tag}{today.isoformat()}\n\n"
        f"- Rolled entries: {rolled_count}\n"
        f"- Archived tickers: {archived_count}\n"
        f"- Flagged items: {len(flags)}\n"
    )
    if flags:
        section += "\n### Flags\n\n"
        for fl in flags:
            section += f"- {fl}\n"
    COMPACTOR_LOG.write_text(existing.rstrip("\n") + "\n" + section)


# ─── main ────────────────────────────────────────────────────────────────────


def run(dry_run: bool = False) -> None:
    today = date.today()
    print(f"Wiki compactor — {today.isoformat()} {'(DRY-RUN)' if dry_run else ''}")
    print(f"Wiki root: {WIKI_ROOT}")

    # 1. Collect pages
    pages = _collect_wiki_pages()
    print(f"  Pages found: {len(pages)}")

    all_flags: list[str] = []

    # 2. Word-budget check (flag only)
    budget_flags = check_word_budgets(pages)
    print(f"  Word-budget flags: {len(budget_flags)}")
    all_flags.extend(budget_flags)

    # 3. Front-matter integrity (flag only)
    fm_flags = check_front_matter(pages)
    print(f"  Front-matter flags: {len(fm_flags)}")
    all_flags.extend(fm_flags)

    # 4. Trade tier rolling
    rolled_count = 0
    tickers_dir = WIKI_ROOT / "tickers"
    if tickers_dir.exists():
        for ticker_dir in sorted(tickers_dir.iterdir()):
            if not ticker_dir.is_dir() or ticker_dir.name.startswith("_"):
                continue
            trades_path = ticker_dir / "trades.md"
            n = roll_trades(trades_path, today, dry_run)
            if n:
                print(f"    Rolled {n} trade entries in {ticker_dir.name}/trades.md")
                rolled_count += n

    # 5. recent.md pruning
    pruned = 0
    if tickers_dir.exists():
        for ticker_dir in sorted(tickers_dir.iterdir()):
            if not ticker_dir.is_dir() or ticker_dir.name.startswith("_"):
                continue
            recent_path = ticker_dir / "recent.md"
            n = prune_recent(recent_path, today, dry_run)
            if n:
                print(f"    Pruned {n} stale bullets from {ticker_dir.name}/recent.md")
                pruned += n

    # 6. LOG.md rolling
    log_path = WIKI_ROOT / "LOG.md"
    log_rolled = roll_log(log_path, today, dry_run)
    if log_rolled:
        print(f"  Rolled {log_rolled} LOG.md entries")
    rolled_count += log_rolled

    # 7. Orphan detection + archiving
    watchlist_tickers = _load_watchlist_tickers()
    orphans = detect_orphans(tickers_dir, watchlist_tickers, today)
    archive_dir = WIKI_ROOT / "_archive"
    archived: list[str] = []
    if orphans:
        print(f"  Orphan tickers found: {orphans}")
        archived = archive_orphans(orphans, tickers_dir, archive_dir, dry_run)
        if archived:
            print(f"  {'Would archive' if dry_run else 'Archived'}: {archived}")

    # 8. Stale flag (flag only — skip archived folders)
    live_pages = _collect_wiki_pages()  # re-collect after archiving
    stale_flags = check_stale(live_pages, today)
    print(f"  Stale-page flags: {len(stale_flags)}")
    all_flags.extend(stale_flags)

    # 9. Cross-ref check (flag only)
    xref_flags = check_cross_refs(live_pages)
    print(f"  Broken cross-ref flags: {len(xref_flags)}")
    all_flags.extend(xref_flags)

    # 10. Output files
    write_lint_report(all_flags)
    append_compactor_log(
        today=today,
        dry_run=dry_run,
        rolled_count=rolled_count,
        archived_count=len(archived),
        flags=all_flags,
    )

    print(f"\nDone. Flagged items: {len(all_flags)}. See scripts/wiki_lint_report.md")
    if all_flags:
        print("Wiki review needed:")
        for fl in all_flags[:10]:
            print(f"  {fl}")
        if len(all_flags) > 10:
            print(f"  ... and {len(all_flags) - 10} more")


def main() -> None:
    parser = argparse.ArgumentParser(description="Wiki compactor — deterministic housekeeping")
    parser.add_argument("--dry-run", action="store_true", help="Report only; make no file changes")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
