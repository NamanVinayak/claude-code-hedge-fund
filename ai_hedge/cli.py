"""CLI entry point: ai-hedge-fund install / uninstall"""
import os
import sys
import shutil
from pathlib import Path

SKILL_NAMES = ["invest", "swing", "daytrade", "research"]


def get_skills_source_dir():
    """Skills are in .claude/skills/ relative to the package root."""
    pkg_dir = Path(__file__).parent.parent
    return pkg_dir / ".claude" / "skills"


def get_target_dir():
    """User's .claude/skills/ in current working directory."""
    return Path(".claude") / "skills"


def install():
    source_dir = get_skills_source_dir()
    target_dir = get_target_dir()

    installed = []
    for name in SKILL_NAMES:
        src = source_dir / name / "SKILL.md"
        dst = target_dir / name / "SKILL.md"

        if not src.exists():
            print(f"  Warning: {src} not found, skipping")
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dst.resolve():
            shutil.copy2(src, dst)
        installed.append(name)
        print(f"  Installed /{name}")

    if installed:
        print(f"\nDone! You now have {len(installed)} commands:")
        print(f"  /invest AAPL,MSFT     — Long-term portfolio decisions")
        print(f"  /swing TSLA           — Swing trade setups (2-20 days)")
        print(f"  /daytrade SPY         — Intraday trade plans")
        print(f"  /research NVDA        — Comprehensive research report")
    else:
        print("No skills found to install. Is the package installed correctly?")


def uninstall():
    source_dir = get_skills_source_dir()
    target_dir = get_target_dir()
    removed = []
    for name in SKILL_NAMES:
        skill_dir = target_dir / name
        src_dir = source_dir / name
        if skill_dir.exists():
            if skill_dir.resolve() == src_dir.resolve():
                print(f"  Skipping /{name} (source dir — use pip uninstall instead)")
                continue
            shutil.rmtree(skill_dir)
            removed.append(name)
            print(f"  Removed /{name}")

    if removed:
        print(f"\n{len(removed)} skills uninstalled.")
    else:
        print("No skills found to remove.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("install", "uninstall"):
        print("AI Hedge Fund — Claude Code Skill Collection")
        print()
        print("Usage: ai-hedge-fund <command>")
        print()
        print("Commands:")
        print("  install     Install /invest, /swing, /daytrade, /research slash commands")
        print("  uninstall   Remove all slash commands")
        sys.exit(1)

    if sys.argv[1] == "install":
        install()
    else:
        uninstall()


if __name__ == "__main__":
    main()
