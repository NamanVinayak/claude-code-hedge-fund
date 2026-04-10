"""Tests for the explainer agent schema and display logic."""
import json
from ai_hedge.schemas import ExplainerOutput, TickerExplanation


def test_explainer_output_schema_valid():
    """ExplainerOutput accepts well-formed data."""
    data = ExplainerOutput(
        tldr="Apple looks strong. Most analysts are bullish due to solid fundamentals.",
        narrative="The AI hedge fund analyzed Apple using 14 different perspectives...\n\nOverall, the picture is positive.",
        per_ticker={
            "AAPL": TickerExplanation(
                verdict="BUY with 78% confidence — strong fundamentals and momentum align.",
                bull_case="Warren Buffett's framework loves Apple's consistent margins...",
                bear_case="Michael Burry flags the P/E ratio at 32 as stretched...",
                key_numbers={
                    "P/E Ratio": "32 (investors pay $32 per $1 of earnings — above market average of ~20)",
                    "Revenue Growth": "8.5% year-over-year (steady but not explosive)",
                },
                risk_summary="Main risk is valuation — if growth slows, the high price could correct.",
            )
        },
        concepts={
            "P/E Ratio": "Price-to-Earnings ratio. How much investors pay for each dollar of profit. Lower usually means cheaper.",
            "RSI": "Relative Strength Index. Measures if a stock has been bought or sold too aggressively. Below 30 = oversold, above 70 = overbought.",
        },
    )
    assert data.tldr.startswith("Apple")
    assert "AAPL" in data.per_ticker
    assert len(data.concepts) == 2


def test_explainer_output_json_roundtrip():
    """ExplainerOutput survives JSON serialization."""
    data = ExplainerOutput(
        tldr="Test summary.",
        narrative="Test narrative.",
        per_ticker={
            "MSFT": TickerExplanation(
                verdict="HOLD",
                bull_case="Good growth.",
                bear_case="High valuation.",
                key_numbers={"P/E": "35"},
                risk_summary="Valuation risk.",
            )
        },
        concepts={"P/E": "Price to earnings."},
    )
    dumped = json.loads(data.model_dump_json())
    restored = ExplainerOutput(**dumped)
    assert restored.tldr == "Test summary."
    assert restored.per_ticker["MSFT"].verdict == "HOLD"


import io
import sys


def _make_sample_explanation() -> dict:
    """Return a sample explanation.json as a dict."""
    return {
        "tldr": "Apple is a strong buy. 10 out of 14 analysts are bullish, driven by rock-solid margins and steady growth.",
        "narrative": (
            "The AI hedge fund ran Apple through 14 different analytical lenses — from Warren Buffett's "
            "value investing approach to Cathie Wood's innovation-focused framework.\n\n"
            "The overwhelming consensus is bullish. Apple's fundamentals are excellent: 26% net margins, "
            "8.5% revenue growth, and a fortress balance sheet with $60B in cash.\n\n"
            "The main pushback comes from valuation-focused analysts like Michael Burry and Ben Graham, "
            "who flag the P/E ratio of 32 as expensive. But momentum and quality analysts counter that "
            "Apple's consistency justifies a premium."
        ),
        "per_ticker": {
            "AAPL": {
                "verdict": "BUY 150 shares with 78% confidence — fundamentals and momentum align.",
                "bull_case": "Strong margins, steady growth, Buffett and Lynch both bullish.",
                "bear_case": "Valuation stretched at 32x earnings, Burry and Graham bearish.",
                "key_numbers": {
                    "P/E Ratio": "32 (paying $32 per $1 of earnings — above market avg of ~20)",
                    "Net Margin": "26% (keeps 26 cents of every dollar — very healthy)",
                },
                "risk_summary": "If growth slows, the premium valuation could correct sharply.",
            }
        },
        "concepts": {
            "P/E Ratio": "How much investors pay per dollar of profit. Lower = cheaper stock.",
            "Net Margin": "What percentage of revenue becomes actual profit after all costs.",
        },
    }


def test_display_explanation_produces_output():
    """_display_explanation prints the TL;DR, narrative, and per-ticker sections."""
    from ai_hedge.runner.finalize import _display_explanation

    explanation = _make_sample_explanation()
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        _display_explanation(explanation)
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    assert "Apple is a strong buy" in output
    assert "AAPL" in output
    assert "P/E Ratio" in output
    assert "Concepts" in output or "GLOSSARY" in output


def test_display_explanation_handles_empty():
    """_display_explanation gracefully handles missing/empty explanation."""
    from ai_hedge.runner.finalize import _display_explanation

    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        _display_explanation({})
        _display_explanation(None)
    finally:
        sys.stdout = old_stdout
    # Should not crash
