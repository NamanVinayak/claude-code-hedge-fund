"""Wiki memory layer for the swing-stock pipeline.

Reads markdown pages at wiki/ to inject prior context into agent facts
bundles, and writes those pages via the wiki_curator agent after a run.

See scripts/wiki_memory_plan.md for the full design.
"""

from ai_hedge.wiki.manifest import AGENT_MANIFEST, pages_for
from ai_hedge.wiki.inject import inject_context, touch_index, is_wiki_enabled
from ai_hedge.wiki.loader import read_tldr, read_full, parse_front_matter
from ai_hedge.wiki import lint, templates

__all__ = [
    "AGENT_MANIFEST",
    "pages_for",
    "inject_context",
    "touch_index",
    "is_wiki_enabled",
    "read_tldr",
    "read_full",
    "parse_front_matter",
    "lint",
    "templates",
]
