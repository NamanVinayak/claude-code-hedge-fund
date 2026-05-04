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


def _load_mode(run_dir: str) -> str:
    """Load mode from metadata.json, defaulting to 'invest'."""
    meta_path = os.path.join(run_dir, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f).get("mode", "invest")
    return "invest"


# ---------------------------------------------------------------------------
# Invest mode display (original)
# ---------------------------------------------------------------------------

def _display_invest(decisions_data: dict, analyst_signals: dict, combined: dict):
    decisions = decisions_data.get("decisions", {})
    duration = decisions_data.get("duration", "")

    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== TRADING DECISIONS (INVEST) ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    if duration:
        print(f"  Portfolio Duration: {Fore.CYAN}{duration}{Style.RESET_ALL}\n")

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
                    hp = signals[ticker].get("holding_period", "")
                    rsn = signals[ticker].get("reasoning", "")
                    rsn = str(rsn) if not isinstance(rsn, str) else rsn
                    rsn_short = rsn[:80] + "..." if len(rsn) > 80 else rsn
                    sig_col = _signal_color(sig)
                    hp_str = f" [{hp}]" if hp else ""
                    print(f"    {agent:35s} {sig_col}{sig:8s}{Style.RESET_ALL} "
                          f"({conf}%){hp_str} {rsn_short}")

        print()

    _display_portfolio_summary(combined)


# ---------------------------------------------------------------------------
# Swing mode display
# ---------------------------------------------------------------------------

def _display_swing(decisions_data: dict, analyst_signals: dict, combined: dict):
    decisions = decisions_data.get("decisions", decisions_data)

    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== SWING TRADE PLAN ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    # Head Trader synthesis
    synthesis = decisions_data.get("synthesis", "")
    if synthesis:
        print(f"  {Style.BRIGHT}Head Trader Synthesis:{Style.RESET_ALL}")
        print(f"  {synthesis}\n")

    tickers = decisions if isinstance(decisions, dict) else {}
    for ticker, plan in tickers.items():
        if ticker in ("synthesis", "duration"):
            continue
        print(f"{Style.BRIGHT}{Fore.CYAN}{ticker}{Style.RESET_ALL}")
        signal = plan.get("signal", plan.get("action", "neutral"))
        sig_col = _signal_color(signal) if signal in ("bullish", "bearish", "neutral") else ACTION_COLORS.get(signal, Fore.WHITE)
        print(f"  Signal:       {sig_col}{signal.upper()}{Style.RESET_ALL}")
        print(f"  Entry:        ${plan.get('entry', plan.get('entry_price', 'N/A'))}")
        print(f"  Target:       ${plan.get('target', plan.get('target_price', 'N/A'))}")
        print(f"  Stop:         ${plan.get('stop', plan.get('stop_loss', 'N/A'))}")
        rr = plan.get("risk_reward", plan.get("risk_reward_ratio", "N/A"))
        print(f"  Risk/Reward:  {rr}")
        tf = plan.get("timeframe", plan.get("holding_period", "N/A"))
        print(f"  Timeframe:    {tf}")
        conf = plan.get("confidence", "")
        if conf:
            print(f"  Confidence:   {conf}%")
        reasoning = plan.get("reasoning", "")
        if reasoning:
            rsn_short = str(reasoning)[:120] + "..." if len(str(reasoning)) > 120 else reasoning
            print(f"  Reasoning:    {rsn_short}")

        # Per-strategy breakdown from analyst signals
        strat_count = 0
        for agent, signals in analyst_signals.items():
            if ticker in signals:
                strat_count += 1
        if strat_count > 0:
            print(f"\n  Strategy signals ({strat_count}):")
            for agent, signals in analyst_signals.items():
                if ticker in signals:
                    sig = signals[ticker].get("signal", "neutral")
                    conf_s = signals[ticker].get("confidence", "?")
                    sig_col = _signal_color(sig)
                    print(f"    {agent:35s} {sig_col}{sig:8s}{Style.RESET_ALL} ({conf_s}%)")
        print()

    _display_portfolio_summary(combined)


# ---------------------------------------------------------------------------
# Day-trade mode display
# ---------------------------------------------------------------------------

def _display_daytrade(decisions_data: dict, analyst_signals: dict, combined: dict):
    decisions = decisions_data.get("decisions", decisions_data)

    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== DAY TRADE PLAN ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    # Head Trader synthesis
    synthesis = decisions_data.get("synthesis", "")
    if synthesis:
        print(f"  {Style.BRIGHT}Head Trader Synthesis:{Style.RESET_ALL}")
        print(f"  {synthesis}\n")

    tickers = decisions if isinstance(decisions, dict) else {}
    for ticker, plan in tickers.items():
        if ticker in ("synthesis", "duration"):
            continue
        print(f"{Style.BRIGHT}{Fore.CYAN}{ticker}{Style.RESET_ALL}")
        setup = plan.get("setup", plan.get("signal", "N/A"))
        print(f"  Setup:          {setup}")
        print(f"  Entry Trigger:  {plan.get('entry_trigger', plan.get('entry', 'N/A'))}")
        targets = plan.get("targets", [])
        if not targets:
            t1 = plan.get("target_1")
            t2 = plan.get("target_2")
            if t1:
                targets.append(t1)
            if t2:
                targets.append(t2)
        if not targets:
            targets = [plan.get("target", plan.get("target_price", "N/A"))]
        if isinstance(targets, list):
            for i, t in enumerate(targets, 1):
                print(f"  Target {i}:       ${t}")
        else:
            print(f"  Target:         ${targets}")
        print(f"  Stop:           ${plan.get('stop', plan.get('stop_loss', 'N/A'))}")
        pos_size = plan.get("position_size", plan.get("quantity", "N/A"))
        print(f"  Position Size:  {pos_size}")
        window = plan.get("time_window", plan.get("timeframe", "N/A"))
        print(f"  Time Window:    {window}")
        conf = plan.get("confidence", "")
        if conf:
            print(f"  Confidence:     {conf}%")
        reasoning = plan.get("reasoning", "")
        if reasoning:
            rsn_short = str(reasoning)[:120] + "..." if len(str(reasoning)) > 120 else reasoning
            print(f"  Reasoning:      {rsn_short}")

        # Per-strategy signals
        strat_count = 0
        for agent, signals in analyst_signals.items():
            if ticker in signals:
                strat_count += 1
        if strat_count > 0:
            print(f"\n  Strategy signals ({strat_count}):")
            for agent, signals in analyst_signals.items():
                if ticker in signals:
                    sig = signals[ticker].get("signal", "neutral")
                    conf_s = signals[ticker].get("confidence", "?")
                    sig_col = _signal_color(sig)
                    print(f"    {agent:35s} {sig_col}{sig:8s}{Style.RESET_ALL} ({conf_s}%)")
        print()

    _display_portfolio_summary(combined)


# ---------------------------------------------------------------------------
# Research mode display
# ---------------------------------------------------------------------------

def _display_research(decisions_data: dict, analyst_signals: dict, combined: dict):
    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== COMPREHENSIVE RESEARCH REPORT ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    # Bull case
    bull_case = decisions_data.get("bull_case", [])
    if bull_case:
        print(f"  {Style.BRIGHT}{Fore.GREEN}BULL CASE{Style.RESET_ALL}")
        for item in bull_case:
            if isinstance(item, dict):
                print(f"    + {item.get('agent', 'Unknown')}: {item.get('reasoning', '')}")
            else:
                print(f"    + {item}")
        print()

    # Bear case
    bear_case = decisions_data.get("bear_case", [])
    if bear_case:
        print(f"  {Style.BRIGHT}{Fore.RED}BEAR CASE{Style.RESET_ALL}")
        for item in bear_case:
            if isinstance(item, dict):
                print(f"    - {item.get('agent', 'Unknown')}: {item.get('reasoning', '')}")
            else:
                print(f"    - {item}")
        print()

    # Key metrics
    key_metrics = decisions_data.get("key_metrics", {})
    if key_metrics:
        print(f"  {Style.BRIGHT}KEY METRICS{Style.RESET_ALL}")
        for metric, value in key_metrics.items():
            print(f"    {metric:30s} {value}")
        print()

    # Risk factors
    risk_factors = decisions_data.get("risk_factors", [])
    if risk_factors:
        print(f"  {Style.BRIGHT}{Fore.YELLOW}RISK FACTORS{Style.RESET_ALL}")
        for rf in risk_factors:
            print(f"    ! {rf}")
        print()

    # Sentiment distribution
    sentiment = decisions_data.get("sentiment_distribution", {})
    if sentiment:
        print(f"  {Style.BRIGHT}SENTIMENT DISTRIBUTION{Style.RESET_ALL}")
        b = sentiment.get("bullish", 0)
        br = sentiment.get("bearish", 0)
        n = sentiment.get("neutral", 0)
        total = b + br + n
        print(f"    {Fore.GREEN}Bullish: {b}{Style.RESET_ALL}  "
              f"{Fore.RED}Bearish: {br}{Style.RESET_ALL}  "
              f"{Fore.YELLOW}Neutral: {n}{Style.RESET_ALL}  "
              f"(Total: {total})")
        print()

    # Full agent signal grid
    tickers = combined.get("tickers", [])
    if analyst_signals and tickers:
        print(f"  {Style.BRIGHT}AGENT SIGNAL GRID{Style.RESET_ALL}")
        header = f"    {'Agent':35s}"
        for t in tickers:
            header += f" {t:>12s}"
        print(header)
        print(f"    {'─' * (35 + 13 * len(tickers))}")

        for agent in sorted(analyst_signals.keys()):
            signals = analyst_signals[agent]
            row = f"    {agent:35s}"
            for t in tickers:
                if t in signals:
                    sig = signals[t].get("signal", "?")
                    conf = signals[t].get("confidence", "?")
                    sig_col = _signal_color(sig)
                    row += f" {sig_col}{sig[:4]:>4s}{Style.RESET_ALL}({conf:>3s}%) " if isinstance(conf, str) else f" {sig_col}{sig[:4]:>4s}{Style.RESET_ALL}({int(conf):>3d}%) "
                else:
                    row += f" {'─':>12s}"
            print(row)
        print()


# ---------------------------------------------------------------------------
# Explanation display (all modes)
# ---------------------------------------------------------------------------

def _display_explanation(explanation: dict | None):
    """Display the explainer agent's educational narrative."""
    if not explanation:
        return

    tldr = explanation.get("tldr", "")
    narrative = explanation.get("narrative", "")
    per_ticker = explanation.get("per_ticker", {})
    concepts = explanation.get("concepts", {})

    if not tldr and not narrative:
        return

    print(f"\n{Style.BRIGHT}{'=' * 60}")
    print(f"{'=== ANALYSIS EXPLAINED ===':^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    # TL;DR
    if tldr:
        print(f"  {Style.BRIGHT}TL;DR{Style.RESET_ALL}")
        print(f"  {tldr}\n")

    # Narrative
    if narrative:
        print(f"  {Style.BRIGHT}THE FULL STORY{Style.RESET_ALL}")
        for paragraph in narrative.split("\n"):
            paragraph = paragraph.strip()
            if paragraph:
                # Word-wrap at ~76 chars with 2-space indent
                words = paragraph.split()
                line = "  "
                for word in words:
                    if len(line) + len(word) + 1 > 78:
                        print(line)
                        line = "  " + word
                    else:
                        line = line + " " + word if line.strip() else "  " + word
                if line.strip():
                    print(line)
                print()

    # Per-ticker breakdown
    for ticker, details in per_ticker.items():
        if not isinstance(details, dict):
            continue
        print(f"  {Style.BRIGHT}{Fore.CYAN}{ticker}{Style.RESET_ALL}")

        verdict = details.get("verdict", "")
        if verdict:
            print(f"    {Style.BRIGHT}Verdict:{Style.RESET_ALL} {verdict}")

        bull = details.get("bull_case", "")
        if bull:
            print(f"    {Fore.GREEN}Bull Case:{Style.RESET_ALL} {bull}")

        bear = details.get("bear_case", "")
        if bear:
            print(f"    {Fore.RED}Bear Case:{Style.RESET_ALL} {bear}")

        key_numbers = details.get("key_numbers", {})
        if key_numbers:
            print(f"    {Style.BRIGHT}Key Numbers:{Style.RESET_ALL}")
            for metric, value in key_numbers.items():
                print(f"      {metric}: {value}")

        risk = details.get("risk_summary", "")
        if risk:
            print(f"    {Fore.YELLOW}Risk:{Style.RESET_ALL} {risk}")

        print()

    # Concepts glossary
    if concepts:
        print(f"  {Style.BRIGHT}GLOSSARY{Style.RESET_ALL}")
        for term, definition in concepts.items():
            print(f"    {Style.BRIGHT}{term}:{Style.RESET_ALL} {definition}")
        print()


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _display_portfolio_summary(combined: dict):
    portfolio = combined.get("portfolio", {})
    if not portfolio:
        return
    cash = portfolio.get("cash", 0)
    print(f"{Style.BRIGHT}{'─' * 60}")
    print("Portfolio Summary")
    print(f"{'─' * 60}{Style.RESET_ALL}")
    print(f"  Cash:               ${cash:,.2f}")
    print(f"  Margin used:        ${portfolio.get('margin_used', 0):,.2f}")
    print(f"  Margin requirement: {portfolio.get('margin_requirement', 0):.0%}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

MODE_DISPLAY = {
    "invest": _display_invest,
    "swing": _display_swing,
    "daytrade": _display_daytrade,
    "research": _display_research,
}


# ---------------------------------------------------------------------------
# summary.json writer (dashboard-ready structured output)
# ---------------------------------------------------------------------------

_SWING_STRATEGY_AGENTS = {
    "swing_trend_momentum",
    "swing_mean_reversion",
    "swing_breakout",
    "swing_catalyst_news",
    "swing_macro_context",
}


def _reasoning_tldr(reasoning: object, max_chars: int = 200) -> str:
    text = str(reasoning or "")
    first = text.split(". ")[0]
    return first[:max_chars] if len(first) > max_chars else first


def write_summary(run_id: str, run_dir: str) -> None:
    """Write runs/<id>/summary.json after the run closes.

    Reads decisions.json + signals_combined.json + runs/index.json + watchlist.
    Wrapped in try/except by caller — failures logged to summary_error.txt.
    """
    decisions_path = os.path.join(run_dir, "decisions.json")
    combined_path = os.path.join(run_dir, "signals_combined.json")

    if not os.path.exists(decisions_path):
        raise FileNotFoundError(f"decisions.json missing at {decisions_path}")

    with open(decisions_path) as f:
        decisions_data = json.load(f)
    combined: dict = {}
    if os.path.exists(combined_path):
        with open(combined_path) as f:
            combined = json.load(f)

    mode = _load_mode(run_dir)

    # --- run index entry (started_at / ended_at / tickers) ---
    from ai_hedge.runner.run_index import _load as _load_index
    index_entries = _load_index()
    index_entry = next((e for e in index_entries if e.get("run_id") == run_id), {})
    started_at = index_entry.get("started_at")
    ended_at = index_entry.get("ended_at")
    tickers: list[str] = index_entry.get("tickers") or list(
        (decisions_data.get("decisions") or decisions_data or {}).keys()
    )
    tickers = [t for t in tickers if t not in ("synthesis", "duration", "portfolio_summary")]

    # --- decisions list ---
    raw_decisions = decisions_data.get("decisions") or decisions_data
    decision_rows = []
    if isinstance(raw_decisions, dict):
        for ticker, d in raw_decisions.items():
            if not isinstance(d, dict) or ticker in ("synthesis", "duration", "portfolio_summary"):
                continue
            action = (d.get("action") or d.get("signal") or "no_action").lower()
            reasoning_tldr = _reasoning_tldr(d.get("reasoning", ""))
            decision_rows.append({
                "ticker": ticker,
                "action": action,
                "confidence": d.get("confidence") or 0,
                "entry": d.get("entry_price") or d.get("entry"),
                "stop": d.get("stop_loss") or d.get("stop"),
                "target": d.get("target_price") or d.get("target"),
                "reasoning_tldr": reasoning_tldr,
            })

    # --- portfolio_state ---
    portfolio = combined.get("portfolio", {})
    portfolio_summary = decisions_data.get("portfolio_summary", {})
    positions_held = len(portfolio.get("positions") or {})
    cash = float(portfolio.get("cash") or portfolio_summary.get("cash_available") or 0)
    exposure = float(
        portfolio_summary.get("open_exposure_analyzed")
        or portfolio.get("margin_used")
        or 0
    )

    # --- agent_summary ---
    analyst_signals = combined.get("analyst_signals", {})
    strategy_received = sum(
        1 for a in analyst_signals if a in _SWING_STRATEGY_AGENTS
        and any(analyst_signals[a].values())
    )
    # head_trader synthesis label
    ht_signals = analyst_signals.get("swing_head_trader", {})
    ht_consensus_values = [
        v.get("consensus_signal", "").lower()
        for v in ht_signals.values()
        if isinstance(v, dict)
    ]
    if ht_consensus_values:
        unique = set(v for v in ht_consensus_values if v)
        if len(unique) == 1:
            ht_synthesis = unique.pop()
        elif unique & {"bullish", "bearish"}:
            ht_synthesis = "mixed"
        else:
            ht_synthesis = ht_consensus_values[0] or "neutral"
    else:
        ht_synthesis = "neutral"
    degraded_inputs: list[str] = combined.get("degraded_inputs") or []

    # --- wiki_state ---
    wiki_enabled = False
    try:
        watchlist_path = os.path.join("tracker", "watchlist.json")
        if os.path.exists(watchlist_path):
            with open(watchlist_path) as f:
                wl = json.load(f)
            wiki_enabled = bool(wl.get("settings", {}).get("wiki_enabled", False))
    except Exception:
        pass

    summary = {
        "run_id": run_id,
        "mode": mode,
        "started_at": started_at,
        "ended_at": ended_at,
        "tickers": tickers,
        "decisions": decision_rows,
        "portfolio_state": {
            "positions_held": positions_held,
            "cash": cash,
            "exposure": exposure,
        },
        "agent_summary": {
            "strategy_signals_received": strategy_received,
            "head_trader_synthesis": ht_synthesis,
            "degraded_inputs": degraded_inputs,
        },
        "wiki_state": {
            "wiki_enabled": wiki_enabled,
            "wiki_pages_updated": 0,
        },
    }

    summary_path = os.path.join(run_dir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[summary] wrote {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="Display hedge fund trading decisions.")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    args = parser.parse_args()

    run_dir = os.path.join("runs", args.run_id)
    mode = _load_mode(run_dir)

    # Determine decisions file based on mode
    decisions_path = os.path.join(run_dir, "decisions.json")
    combined_path = os.path.join(run_dir, "signals_combined.json")

    if not os.path.exists(decisions_path):
        print(f"Error: {decisions_path} not found. Has the final agent run?")
        return

    with open(decisions_path) as f:
        decisions_data = json.load(f)

    analyst_signals = {}
    combined = {}
    if os.path.exists(combined_path):
        with open(combined_path) as f:
            combined = json.load(f)
        analyst_signals = combined.get("analyst_signals", {})

    # Display explanation first (if available)
    explanation_path = os.path.join(run_dir, "explanation.json")
    if os.path.exists(explanation_path):
        with open(explanation_path) as f:
            explanation = json.load(f)
        _display_explanation(explanation)

    # Then display the raw data tables
    display_fn = MODE_DISPLAY.get(mode, _display_invest)
    display_fn(decisions_data, analyst_signals, combined)

    # Close the run-index entry. Count actionable decisions so the index
    # shows at-a-glance whether the run produced trades.
    from ai_hedge.runner.run_index import close_run
    decisions = decisions_data.get("decisions") or decisions_data
    actionable = 0
    if isinstance(decisions, dict):
        for d in decisions.values():
            if isinstance(d, dict):
                action = (d.get("action") or d.get("direction") or "").lower()
                if action in ("buy", "sell", "long", "short", "cover"):
                    actionable += 1
    close_run(args.run_id, status="completed", decision_count=actionable)

    # Write a structured summary for future dashboard consumption.
    try:
        write_summary(args.run_id, run_dir)
    except Exception as exc:
        err_path = os.path.join(run_dir, "summary_error.txt")
        with open(err_path, "w") as f:
            f.write(str(exc))
        print(f"[WARN] summary.json failed: {exc}")

    # Refresh wiki/INDEX.md with the latest last_updated dates. Feature-
    # flagged via tracker/watchlist.json:settings.wiki_enabled; no-op when
    # off. Wrapped so wiki failures never break finalize output.
    try:
        from ai_hedge.wiki.inject import touch_index
        touch_index(args.run_id)
    except Exception as exc:
        print(f"[WARN] wiki touch_index failed: {exc}")

    # Append graded persona calls to wiki/agents/<persona>/track_record.md.
    # Idempotent on run_id; no-op when no grading files exist (non-swing).
    try:
        from ai_hedge.grading.wiki_writer import append_track_records
        report = append_track_records(args.run_id)
        if not report.get("skipped") and report.get("appended", 0) > 0:
            print(
                f"[grading] appended {report['appended']} persona track records "
                f"({report['verdict_count']} verdicts)"
            )
    except Exception as exc:
        print(f"[WARN] grading wiki append failed: {exc}")


if __name__ == "__main__":
    main()
