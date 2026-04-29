"""Wiki linter.

Phase-1 scope: size + front-matter checks. Cross-ref + tier rolling are
Phase 2 (compactor).

Used by:
- the curator's post-write check (rejects oversized writes),
- a future `scripts/wiki_lint.py` CLI (Phase 2),
- tests / smoke checks.
"""

from __future__ import annotations

from pathlib import Path

from ai_hedge.wiki.loader import parse_front_matter, read_full

REQUIRED_FRONT_MATTER_KEYS = (
    "name",
    "last_updated",
    "last_run_id",
    "target_words",
    "stale_after_days",
)


def word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


def check_front_matter(path: Path | str) -> list[str]:
    """Return a list of human-readable issues. Empty list = clean."""
    fm = parse_front_matter(path)
    issues: list[str] = []
    for key in REQUIRED_FRONT_MATTER_KEYS:
        if key not in fm:
            issues.append(f"missing front-matter key: {key}")
    return issues


def check_size(path: Path | str, *, tolerance: float = 0.20) -> list[str]:
    """Flag pages that exceed `target_words` by more than `tolerance` (fraction)."""
    fm = parse_front_matter(path)
    target = fm.get("target_words")
    if not isinstance(target, int) or target <= 0:
        return []
    body = read_full(path)
    actual = word_count(body)
    cap = int(target * (1 + tolerance))
    if actual > cap:
        return [f"oversize: {actual} words > {cap} cap (target {target})"]
    return []


def check_page(path: Path | str) -> list[str]:
    """Run all Phase-1 checks against one page."""
    issues = []
    issues.extend(check_front_matter(path))
    issues.extend(check_size(path))
    return issues


def lint_directory(root: Path | str = "wiki") -> dict[str, list[str]]:
    """Lint every .md page under `root`. Returns {path: [issues]}."""
    out: dict[str, list[str]] = {}
    root = Path(root)
    if not root.exists():
        return out
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        if rel.name in ("README.md", "INDEX.md", "LOG.md"):
            continue
        if rel.parts and rel.parts[0] == "_archive":
            continue
        issues = check_page(md)
        if issues:
            out[str(md)] = issues
    return out


__all__ = [
    "REQUIRED_FRONT_MATTER_KEYS",
    "word_count",
    "check_front_matter",
    "check_size",
    "check_page",
    "lint_directory",
]
