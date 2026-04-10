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
