"""Audit wiki/tickers/<T>/trades.md against the Turso ledger.

Finds:
  - Phantom run IDs (mentioned in wiki but not present in Turso for that ticker)
  - Cross-ticker contamination (run IDs that exist for a different ticker)
  - Stale numbers (e.g. NVDA -$264.65 — the buggy pre-correction figure)

Usage:
    python -m scripts.audit_wiki_trades

Writes scripts/wiki_audit_report.md with findings; non-zero exit if issues found.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tracker.turso_client import get_all_trades

# Hard-coded list of stale-number patterns we want to flag.
# Add to this list as we discover more buggy numbers that escaped into the wiki.
STALE_NUMBER_PATTERNS = [
    (r"-\$264\.65", "NVDA pre-correction loss (should be -$63.20)"),
    (r"\$5,?000 paper budget", "stale $5K budget (current is $25K)"),
    (r"\$100,?000 phantom budget|--cash 100000", "phantom $100K budget bug (fixed in b2b472d)"),
    (r"\$100,?000 default budget|\$100k default budget", "phantom $100K budget bug (fixed in b2b472d)"),
]

# Run-id pattern (YYYYMMDD_HHMMSS)
RUN_ID_RE = re.compile(r"\b(20\d{6}_\d{6})\b")

# Section headers that contain TRADE CLAIMS (run_ids here must exist in Turso).
# Anywhere else (Run decision history, Lessons learned, footnotes) a run_id
# can be mentioned for context without a corresponding ledger row.
CLAIM_SECTION_HEADERS = re.compile(
    r"^##\s+(open\s+positions?|recently\s+closed|closed\s+trades?|active\s+positions?|filled\s+positions?)",
    re.IGNORECASE | re.MULTILINE,
)


def extract_claim_sections(text: str) -> str:
    """Return concatenated text of all sections that claim specific trades.
    Used to scope phantom-run / cross-contamination detection so we don't
    false-positive on legitimate historical mentions in run-decision tables."""
    headers = list(CLAIM_SECTION_HEADERS.finditer(text))
    if not headers:
        return ""
    chunks = []
    for i, h in enumerate(headers):
        start = h.start()
        # End at next ## header (any level 2 heading) or EOF
        next_h2 = re.search(r"^##\s+", text[h.end():], re.MULTILINE)
        end = h.end() + next_h2.start() if next_h2 else len(text)
        chunks.append(text[start:end])
    return "\n".join(chunks)


def collect_turso_runs_per_ticker() -> dict[str, set[str]]:
    """Return {ticker: {run_ids that have a Turso trade for this ticker}}."""
    out: dict[str, set[str]] = defaultdict(set)
    for t in get_all_trades():
        ticker = t.get("ticker")
        run_id = t.get("run_id")
        if ticker and run_id:
            out[ticker].add(run_id)
    return dict(out)


def all_turso_run_ids() -> set[str]:
    return {t["run_id"] for t in get_all_trades() if t.get("run_id")}


def audit_ticker(ticker: str, file: Path, ticker_runs: set[str], all_runs: set[str]) -> dict:
    text = file.read_text()

    # Only check claim sections — Open positions, Recently Closed, Closed trades.
    # Mentions in Run decision history / Lessons learned / footnotes are
    # legitimate context (HOLDs, prior runs that didn't ingest, etc.).
    claim_text = extract_claim_sections(text)
    if not claim_text:
        mentioned_runs: list[tuple[str, int]] = []
    else:
        mentioned_runs = [(m.group(1), m.start()) for m in RUN_ID_RE.finditer(claim_text)]

    # If a run is mentioned in a context explicitly stating "abandoned",
    # "no fill", "never filled", "not filled", or "expired without" — it's
    # a record that the trade did NOT execute. Not a false claim.
    no_trade_markers = re.compile(
        r"abandoned|no\s+fill|never\s+filled|not\s+filled|expired\s+without|did\s+not\s+(?:fill|execute)",
        re.IGNORECASE,
    )

    phantom_runs = []  # run claimed as a real trade but NOT in Turso
    cross_contamination = []  # run claimed that exists in Turso BUT for a different ticker
    for r, pos in mentioned_runs:
        if r in ticker_runs:
            continue
        # Check if the run is mentioned in a "this trade didn't happen" context
        ctx_start = max(0, pos - 200)
        ctx_end = min(len(claim_text), pos + 200)
        if no_trade_markers.search(claim_text[ctx_start:ctx_end]):
            continue  # explicitly labeled as not-a-real-trade, skip
        if r in all_runs:
            if r not in cross_contamination:
                cross_contamination.append(r)
        else:
            if r not in phantom_runs:
                phantom_runs.append(r)

    # Skip lines where the stale number appears alongside an annotation
    # marker ("corrected", "originally", "sizing bug", commit hash, etc.) —
    # those are intentional historical references, not bugs to fix.
    annotation_markers = re.compile(
        r"corrected|originally|sizing bug|fixed in|see commit|b2b472d|see `wiki/meta/lessons",
        re.IGNORECASE,
    )
    stale_findings = []
    for pattern, label in STALE_NUMBER_PATTERNS:
        # find each match individually and check its line
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            # take ±150 chars around match for annotation context
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 150)
            context = text[start:end]
            if annotation_markers.search(context):
                continue  # intentional annotation, not a stale leak
            stale_findings.append(label)
            break  # one finding per pattern is enough

    return {
        "ticker": ticker,
        "file": str(file),
        "mentioned_runs": sorted(mentioned_runs),
        "phantom_runs": sorted(phantom_runs),
        "cross_contamination": sorted(cross_contamination),
        "stale_findings": stale_findings,
        "is_clean": not (phantom_runs or cross_contamination or stale_findings),
    }


def main() -> int:
    ticker_runs = collect_turso_runs_per_ticker()
    all_runs = all_turso_run_ids()

    wiki_dir = Path("wiki/tickers")
    if not wiki_dir.exists():
        print("wiki/tickers/ not found, nothing to audit")
        return 0

    rows = []
    for tdir in sorted(wiki_dir.iterdir()):
        if not tdir.is_dir():
            continue
        trades_path = tdir / "trades.md"
        if not trades_path.exists():
            continue
        ticker = tdir.name
        rows.append(audit_ticker(ticker, trades_path, ticker_runs.get(ticker, set()), all_runs))

    issues = [r for r in rows if not r["is_clean"]]

    # Build report
    lines = [
        "# Wiki Trades Audit Report",
        "",
        f"Scanned {len(rows)} ticker `trades.md` files. Found {len(issues)} with discrepancies.",
        "",
        "Phantom runs = referenced in wiki but no Turso trade with that run_id.",
        "Cross-contamination = run_id exists in Turso for a different ticker.",
        "Stale findings = old/buggy numbers we flagged for cleanup.",
        "",
    ]

    if not issues:
        lines.append("**No issues found. All wiki trade pages match the Turso ledger.**")
    else:
        lines.append("## Tickers with issues")
        lines.append("")
        for r in issues:
            lines.append(f"### {r['ticker']}")
            lines.append(f"- File: `{r['file']}`")
            if r["phantom_runs"]:
                lines.append(f"- **Phantom runs** ({len(r['phantom_runs'])}): {', '.join(r['phantom_runs'])}")
            if r["cross_contamination"]:
                lines.append(f"- **Cross-contamination** ({len(r['cross_contamination'])}): {', '.join(r['cross_contamination'])}")
            if r["stale_findings"]:
                for s in r["stale_findings"]:
                    lines.append(f"- **Stale**: {s}")
            lines.append("")

    if rows:
        clean = [r for r in rows if r["is_clean"]]
        if clean:
            lines.append("## Tickers clean")
            lines.append("")
            lines.append(", ".join(r["ticker"] for r in clean))

    out_path = Path("scripts/wiki_audit_report.md")
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out_path}")
    print(f"Issues: {len(issues)} / {len(rows)} tickers")
    for r in issues:
        problems = []
        if r["phantom_runs"]:
            problems.append(f"{len(r['phantom_runs'])} phantom run(s)")
        if r["cross_contamination"]:
            problems.append(f"{len(r['cross_contamination'])} cross-contamination")
        if r["stale_findings"]:
            problems.append(f"{len(r['stale_findings'])} stale")
        print(f"  {r['ticker']}: {', '.join(problems)}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
