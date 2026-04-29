"""String templates for the 5 Phase-1 wiki page types.

Each template is rendered at bootstrap time (and as a fallback when the
curator must create a fresh page on a brand-new ticker). The curator
otherwise produces page contents directly — these templates are NOT a
strict layout the curator must mimic, just a sane skeleton.

Word-budget metadata lives in the YAML front-matter so the linter and
compactor can enforce it without re-reading this module.
"""

from __future__ import annotations

from datetime import date


def _front_matter(
    *,
    name: str,
    target_words: int,
    stale_after_days: int,
    last_updated: str | None = None,
    last_run_id: str = "bootstrap",
    summary: str = "",
) -> str:
    last = last_updated or date.today().isoformat()
    return (
        "---\n"
        f"name: {name}\n"
        f"last_updated: {last}\n"
        f"last_run_id: {last_run_id}\n"
        f"target_words: {target_words}\n"
        f"stale_after_days: {stale_after_days}\n"
        f"word_count: 0\n"
        f"summary: {summary}\n"
        "---\n\n"
    )


def thesis_template(ticker: str, *, last_run_id: str = "bootstrap") -> str:
    return _front_matter(
        name=f"{ticker} thesis",
        target_words=500,
        stale_after_days=30,
        last_run_id=last_run_id,
        summary="durable bull/bear story",
    ) + (
        f"# {ticker} — Thesis\n\n"
        "## TL;DR\n\n"
        "_Bootstrap placeholder. Fill in after first run._\n\n"
        "## Bull case\n\n"
        "- _pending_\n\n"
        "## Bear case\n\n"
        "- _pending_\n\n"
        "## What would change my mind\n\n"
        "- _pending_\n\n"
        "## Last updated\n\n"
        "_pending_\n"
    )


def technicals_template(ticker: str, *, last_run_id: str = "bootstrap") -> str:
    return _front_matter(
        name=f"{ticker} technicals",
        target_words=350,
        stale_after_days=7,
        last_run_id=last_run_id,
        summary="current chart state",
    ) + (
        f"# {ticker} — Technicals\n\n"
        "## TL;DR\n\n"
        "_Bootstrap placeholder._\n\n"
        "## Multi-timeframe state\n\n"
        "_pending_\n\n"
        "## Key levels\n\n"
        "| level | value |\n"
        "|---|---|\n"
        "| support | _pending_ |\n"
        "| resistance | _pending_ |\n"
        "| entry zone | _pending_ |\n"
        "| invalidation | _pending_ |\n\n"
        "## Setup type\n\n"
        "_pending_\n\n"
        "## Last updated\n\n"
        "_pending_\n"
    )


def catalysts_template(ticker: str, *, last_run_id: str = "bootstrap") -> str:
    return _front_matter(
        name=f"{ticker} catalysts",
        target_words=400,
        stale_after_days=14,
        last_run_id=last_run_id,
        summary="upcoming events + recent news",
    ) + (
        f"# {ticker} — Catalysts\n\n"
        "## TL;DR\n\n"
        "_Bootstrap placeholder._\n\n"
        "## Upcoming events\n\n"
        "- _pending_\n\n"
        "## Recent news synthesis\n\n"
        "- _pending_\n\n"
        "## Insider activity\n\n"
        "_pending_\n\n"
        "## Analyst consensus\n\n"
        "_pending_\n\n"
        "## Last updated\n\n"
        "_pending_\n"
    )


def trades_template(ticker: str, *, last_run_id: str = "bootstrap") -> str:
    return _front_matter(
        name=f"{ticker} trades",
        target_words=800,
        stale_after_days=60,
        last_run_id=last_run_id,
        summary="trade journal for this ticker",
    ) + (
        f"# {ticker} — Trades\n\n"
        "## TL;DR\n\n"
        "_No trades yet._\n\n"
        "## Open positions\n\n"
        "_none_\n\n"
        "## Closed — last 30 days\n\n"
        "_none_\n\n"
        "## Closed — older, rolled by month\n\n"
        "_none_\n\n"
        "## Closed — older than 6 months\n\n"
        "_none_\n\n"
        "## Lifetime stats\n\n"
        "_none_\n"
    )


def regime_template(*, last_run_id: str = "bootstrap") -> str:
    return _front_matter(
        name="macro regime",
        target_words=400,
        stale_after_days=14,
        last_run_id=last_run_id,
        summary="current macro regime",
    ) + (
        "# Macro Regime\n\n"
        "## TL;DR\n\n"
        "_Bootstrap placeholder._\n\n"
        "## Fed posture\n\n"
        "_pending_\n\n"
        "## Rate trajectory & inflation\n\n"
        "_pending_\n\n"
        "## Geopolitical / regulatory\n\n"
        "_pending_\n\n"
        "## Risk-off triggers to watch\n\n"
        "- _pending_\n\n"
        "## Last updated\n\n"
        "_pending_\n"
    )


PAGE_TEMPLATES = {
    "thesis": thesis_template,
    "technicals": technicals_template,
    "catalysts": catalysts_template,
    "trades": trades_template,
    "regime": regime_template,
}


def render(page_kind: str, ticker: str | None = None, *, last_run_id: str = "bootstrap") -> str:
    """Render a fresh skeleton for one of the 5 page types."""
    if page_kind not in PAGE_TEMPLATES:
        raise ValueError(f"unknown page_kind: {page_kind}")
    fn = PAGE_TEMPLATES[page_kind]
    if page_kind == "regime":
        return fn(last_run_id=last_run_id)
    if not ticker:
        raise ValueError(f"page_kind={page_kind} requires ticker")
    return fn(ticker, last_run_id=last_run_id)
