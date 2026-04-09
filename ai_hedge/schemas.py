from pydantic import BaseModel, Field
from typing import Literal


class WarrenBuffettSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")
    holding_period: str = Field(description="Recommended holding period")


class CharlieMungerSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class BenGrahamSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class BillAckmanSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class CathieWoodSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class MichaelBurrySignal(BaseModel):
    """Schema returned by the LLM."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0–100
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class NassimTalebSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")
    holding_period: str = Field(description="Recommended holding period")


class PeterLynchSignal(BaseModel):
    """
    Container for the Peter Lynch-style output signal.
    """
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class PhilFisherSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class StanleyDruckenmillerSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class MohnishPabraiSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class RakeshJhunjhunwalaSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class AswathDamodaranSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float          # 0‒100
    reasoning: str
    holding_period: str = Field(description="Recommended holding period")


class NewsSentimentSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float = Field(description="Confidence level 0-100")
    reasoning: str = Field(description="Brief reasoning for the sentiment assessment")
    holding_period: str = Field(description="Recommended holding period")


class Sentiment(BaseModel):
    """Represents the sentiment of a news article."""

    sentiment: Literal["positive", "negative", "neutral"]
    confidence: int = Field(description="Confidence 0-100")


class PortfolioDecision(BaseModel):
    action: Literal["buy", "sell", "short", "cover", "hold"]
    quantity: int = Field(description="Number of shares to trade")
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")
    duration: str = Field(description="Recommended holding duration synthesized from analyst signals")


class PortfolioManagerOutput(BaseModel):
    decisions: dict[str, PortfolioDecision] = Field(description="Dictionary of ticker to trading decisions")


class SwingSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float = Field(description="Confidence 0-100")
    reasoning: str
    entry_price: float = Field(description="Suggested entry price")
    target_price: float = Field(description="Target exit price")
    stop_loss: float = Field(description="Stop loss price")
    timeframe: str = Field(description="Expected holding period, e.g. '5-10 trading days'")


class SwingPortfolioDecision(BaseModel):
    action: Literal["buy", "sell", "short", "cover", "hold"]
    entry_price: float = Field(description="Entry price level")
    target_price: float = Field(description="Target price")
    stop_loss: float = Field(description="Stop loss price")
    risk_reward_ratio: str = Field(description="Risk reward ratio e.g. '3.2:1'")
    timeframe: str = Field(description="Expected trade duration")
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str


class DayTradeSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float = Field(description="Confidence 0-100")
    reasoning: str
    entry_trigger: str = Field(description="Entry condition, e.g. 'break above 248.50'")
    target_1: float = Field(description="First target price")
    target_2: float = Field(description="Second target price")
    stop_loss: float = Field(description="Stop loss price")
    risk_reward: str = Field(description="Risk reward ratio")
    time_window: str = Field(description="When the setup is valid, e.g. 'first 2 hours'")


class DayTradePortfolioDecision(BaseModel):
    setup_name: str = Field(description="Name of the trade setup")
    direction: Literal["long", "short", "no_trade"]
    entry_trigger: str = Field(description="Entry condition")
    targets: list[float] = Field(description="Target prices in order")
    stop_loss: float = Field(description="Stop loss price")
    position_size: str = Field(description="Position sizing guidance")
    time_window: str = Field(description="When the setup is valid")
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str


class HeadTraderSignal(BaseModel):
    consensus_signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Synthesis of all strategy signals")
    agent_agreement_pct: float = Field(description="Percentage of agents that agree with consensus")
    key_conflicts: str = Field(description="Summary of main disagreements between agents")
    recommended_action: str = Field(description="Recommended trade action based on synthesis")


class ResearchReport(BaseModel):
    bull_case: str = Field(description="Summary of bullish arguments across all agents")
    bear_case: str = Field(description="Summary of bearish arguments across all agents")
    key_metrics: dict = Field(description="Important financial and technical metrics")
    risks: list[str] = Field(description="Key risk factors identified")
    agent_breakdown: dict = Field(description="Per-agent signal summary")
    overall_sentiment: Literal["bullish", "bearish", "neutral", "mixed"]
    confidence_range: str = Field(description="Range of confidence across agents, e.g. '45-92'")
