"""
Display final trading decisions in a colored table.

Usage:
    python -m ai_hedge.runner.finalize --run-id 20240101_120000
"""
import argparse
import json
import os

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

    class _NoColor:
        GREEN = RED = YELLOW = CYAN = WHITE = RESET = ""

    class _NoStyle:
        BRIGHT = RESET_ALL = ""

    Fore = _NoColor()
    Style = _NoStyle()


ACTION_COLORS = {
    "buy": Fore.GREEN,
    "cover": Fore.GREEN,
    "sell": Fore.RED,
    "short": Fore.RED,
    "hold": Fore.YELLOW,
}


def _signal_color(signal: str) -> str:
    if signal == "bullish":
        return Fore.GREEN
    if signal == "bearish":
        return Fore.RED
    return Fore.YELLOW


def main():
    parser = argparse.ArgumentParser(description="Display hedge fund trading decisions.")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    args = parser.parse_args()

    run_dir = os.path.join("runs", args.run_id)
    decisions_path = os.path.join(run_dir, "decisions.json")
    combined_path = os.path.join(run_dir, "signals_combined.json")

    if not os.path.exists(decisions_path):
        print(f"Error: {decisions_path} not found. Has the portfolio manager run?")
        return

    with open(decisions_path) as f:
        decisions_data = json.load(f)

    analyst_signals = {}
    if os.path.exists(combined_path):
        with open(combined_path) as f:
            combined = json.load(f)
        analyst_signals = combined.get("analyst_signals", {})

    decisions = decisions_data.get("decisions", {})

    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== TRADING DECISIONS ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    for ticker, decision in decisions.items():
        action = decision.get("action", "hold").lower()
        quantity = decision.get("quantity", 0)
        confidence = decision.get("confidence", 0)
        reasoning = decision.get("reasoning", "")

        color = ACTION_COLORS.get(action, Fore.WHITE)
        print(f"{Style.BRIGHT}{ticker}{Style.RESET_ALL}")
        print(f"  Action:     {color}{action.upper()}{Style.RESET_ALL}")
        print(f"  Quantity:   {quantity}")
        print(f"  Confidence: {confidence}%")
        if reasoning:
            print(f"  Reasoning:  {reasoning}")

        # Analyst signal summary
        bullish = bearish = neutral = 0
        for agent, signals in analyst_signals.items():
            if ticker in signals:
                sig = signals[ticker].get("signal", "neutral").lower()
                if sig == "bullish":
                    bullish += 1
                elif sig == "bearish":
                    bearish += 1
                else:
                    neutral += 1

        total = bullish + bearish + neutral
        if total > 0:
            print(f"\n  Analyst signals ({total} total):")
            print(f"    {Fore.GREEN}Bullish: {bullish}{Style.RESET_ALL}  "
                  f"{Fore.RED}Bearish: {bearish}{Style.RESET_ALL}  "
                  f"{Fore.YELLOW}Neutral: {neutral}{Style.RESET_ALL}")

            print(f"\n  Per-analyst breakdown:")
            for agent, signals in analyst_signals.items():
                if ticker in signals:
                    sig = signals[ticker].get("signal", "neutral")
                    conf = signals[ticker].get("confidence", "?")
                    rsn = signals[ticker].get("reasoning", "")
                    rsn_short = rsn[:80] + "..." if len(rsn) > 80 else rsn
                    sig_col = _signal_color(sig)
                    print(f"    {agent:35s} {sig_col}{sig:8s}{Style.RESET_ALL} "
                          f"({conf}%) {rsn_short}")

        print()

    # Portfolio summary
    if os.path.exists(combined_path):
        portfolio = combined.get("portfolio", {})
        cash = portfolio.get("cash", 0)
        print(f"{Style.BRIGHT}{'─' * 60}")
        print("Portfolio Summary")
        print(f"{'─' * 60}{Style.RESET_ALL}")
        print(f"  Cash:               ${cash:,.2f}")
        print(f"  Margin used:        ${portfolio.get('margin_used', 0):,.2f}")
        print(f"  Margin requirement: {portfolio.get('margin_requirement', 0):.0%}")
        print()


if __name__ == "__main__":
    main()
