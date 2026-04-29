#!/usr/bin/env python3
"""Fail loudly when CLAUDE.md asserts counts that don't match the code.

This is the small piece that prevents documentation lies from creeping back in.
Run it locally (`python scripts/check_docs_drift.py`) or wire it into pre-commit.

Returns exit code 0 on clean, 1 on drift.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"


def count_helper_defs() -> int:
    src = (ROOT / "ai_hedge" / "personas" / "helpers.py").read_text()
    return len(re.findall(r"^def ", src, flags=re.MULTILINE))


def count_swing_agents() -> int:
    """SWING_AGENTS list in swing_facts_builder is the full count after the 9→5 collapse."""
    from ai_hedge.personas.swing_facts_builder import SWING_AGENTS  # type: ignore
    return len(SWING_AGENTS)


def count_dt_agents() -> int:
    from ai_hedge.personas.dt_facts_builder import DT_AGENTS  # type: ignore
    return len(DT_AGENTS)


def count_invest_personas() -> int:
    from ai_hedge.personas.facts_builder import PERSONA_BUILDERS  # type: ignore
    return len(PERSONA_BUILDERS)


def find_count_in_doc(pattern: str, text: str) -> int | None:
    """Return the first integer captured by `pattern`, or None."""
    m = re.search(pattern, text)
    return int(m.group(1)) if m else None


def main() -> int:
    text = CLAUDE_MD.read_text()
    drift = []

    # 1. Helper count: "<N> deterministic helper functions"
    real_helpers = count_helper_defs()
    doc_helpers = find_count_in_doc(r"(\d+)\s+deterministic helper functions", text)
    if doc_helpers is not None and doc_helpers != real_helpers:
        drift.append(f"helpers: doc says {doc_helpers}, code has {real_helpers}")

    # 2. Swing agents: "Swing strategies (<N>)"
    real_swing = count_swing_agents()
    doc_swing = find_count_in_doc(r"Swing strategies \((\d+)\)", text)
    if doc_swing is not None and doc_swing != real_swing:
        drift.append(f"swing agents: doc says {doc_swing}, code has {real_swing}")

    # 3. DT agents: "Day-trade strategies (<N>)"
    real_dt = count_dt_agents()
    doc_dt = find_count_in_doc(r"Day-trade strategies \((\d+)\)", text)
    if doc_dt is not None and doc_dt != real_dt:
        drift.append(f"daytrade agents: doc says {doc_dt}, code has {real_dt}")

    # 4. Invest personas: "<N> investor personas"
    real_invest = count_invest_personas()
    doc_invest = find_count_in_doc(r"(\d+) investor personas", text)
    if doc_invest is not None and doc_invest != real_invest:
        drift.append(f"invest personas: doc says {doc_invest}, code has {real_invest}")

    if drift:
        print("CLAUDE.md is out of sync with code:", file=sys.stderr)
        for d in drift:
            print(f"  - {d}", file=sys.stderr)
        print("Update CLAUDE.md or update the code, then re-run.", file=sys.stderr)
        return 1

    print(f"✓ CLAUDE.md matches code: helpers={real_helpers}, "
          f"swing={real_swing}, dt={real_dt}, invest={real_invest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
