"""Per-agent wiki reading manifest.

Each entry says: for this agent, what pages does it read, and in what mode
(`tldr` = only the TL;DR section; `full` = entire page).

Pages are referenced as a (category, basename) pair. Per-ticker pages use
category `"ticker"`; macro pages use `"macro"`; meta pages use `"meta"`.

The injector walks this manifest and assembles a `wiki_context` dict per
(agent, ticker) which gets merged into the existing facts bundle.

See scripts/wiki_memory_plan.md §3 for rationale.
"""

from __future__ import annotations

# (category, basename, mode)
#  category: "ticker" (one per analysis ticker), "macro", "meta"
#  basename: filename without .md
#  mode: "tldr" or "full"
AGENT_MANIFEST: dict[str, list[tuple[str, str, str]]] = {
    "swing_trend_momentum": [
        ("ticker", "technicals", "tldr"),
        ("macro", "regime", "tldr"),
    ],
    "swing_mean_reversion": [
        ("ticker", "technicals", "tldr"),
        ("ticker", "recent", "tldr"),
    ],
    "swing_breakout": [
        ("ticker", "technicals", "full"),
    ],
    "swing_catalyst_news": [
        ("ticker", "catalysts", "full"),
        ("macro", "calendar", "full"),
    ],
    "swing_macro_context": [
        ("macro", "regime", "full"),
        ("macro", "sectors", "full"),
        ("ticker", "thesis", "tldr"),
    ],
    # Head trader intentionally omitted — synthesizes strategy signals only.
    "swing_portfolio_manager": [
        ("ticker", "thesis", "tldr"),
        ("ticker", "trades", "full"),
        ("meta", "lessons", "tldr"),
    ],
}


def pages_for(agent: str) -> list[tuple[str, str, str]]:
    """Return the manifest entries for an agent (empty list if not listed)."""
    return AGENT_MANIFEST.get(agent, [])


def agents_with_wiki_context() -> list[str]:
    """Names of agents whose prompts must mention `wiki_context`."""
    return list(AGENT_MANIFEST.keys())
