"""
Build per-persona facts bundles from raw data saved by prepare.py.

Each bundle is the exact analysis_data[ticker] dict that the upstream persona
agent would have built before calling its LLM. The subagent reads the bundle
and the system prompt, then produces the signal JSON.

growth_agent is fully deterministic — its signal is written directly to
signals/growth_analyst_agent.json (aggregate.py picks it up automatically).

Usage:
    python -m ai_hedge.personas.facts_builder --run-id <id> --tickers AAPL,MSFT
"""
from __future__ import annotations

import argparse
import json
import math
import os
from typing import Any

import numpy as np
import pandas as pd

from ai_hedge.data.api import prices_to_df
from ai_hedge.data.models import (
    CompanyNews,
    FinancialMetrics,
    InsiderTrade,
    LineItem,
    Price,
)
from ai_hedge.personas.helpers import (
    # Warren Buffett
    analyze_fundamentals,
    analyze_consistency,
    analyze_moat,
    analyze_pricing_power,
    analyze_book_value_growth,
    wb_analyze_management_quality,
    wb_calculate_intrinsic_value,
    # Charlie Munger
    analyze_moat_strength,
    cm_analyze_management_quality,
    analyze_predictability,
    calculate_munger_valuation,
    analyze_news_sentiment,
    # Ben Graham
    analyze_earnings_stability,
    analyze_financial_strength,
    analyze_valuation_graham,
    # Bill Ackman
    analyze_business_quality,
    analyze_financial_discipline,
    analyze_activism_potential,
    ba_analyze_valuation,
    # Cathie Wood
    analyze_disruptive_potential,
    analyze_innovation_growth,
    analyze_cathie_wood_valuation,
    # Michael Burry
    _analyze_value,
    _analyze_balance_sheet,
    _analyze_insider_activity,
    _analyze_contrarian_sentiment,
    # Nassim Taleb
    analyze_tail_risk,
    analyze_antifragility,
    analyze_convexity,
    analyze_fragility,
    analyze_skin_in_game,
    analyze_volatility_regime,
    analyze_black_swan_sentinel,
    # Peter Lynch
    analyze_lynch_growth,
    analyze_lynch_fundamentals,
    analyze_lynch_valuation,
    pl_analyze_sentiment,
    pl_analyze_insider_activity,
    # Phil Fisher
    analyze_fisher_growth_quality,
    analyze_margins_stability,
    analyze_management_efficiency_leverage,
    analyze_fisher_valuation,
    pf_analyze_insider_activity,
    pf_analyze_sentiment,
    # Stanley Druckenmiller
    analyze_growth_and_momentum,
    sd_analyze_sentiment,
    sd_analyze_insider_activity,
    analyze_risk_reward,
    analyze_druckenmiller_valuation,
    # Mohnish Pabrai
    analyze_downside_protection,
    analyze_pabrai_valuation,
    analyze_double_potential,
    # Rakesh Jhunjhunwala
    analyze_growth,
    analyze_profitability,
    analyze_balance_sheet,
    analyze_cash_flow,
    analyze_management_actions,
    rj_calculate_intrinsic_value,
    assess_quality_metrics,
    analyze_rakesh_jhunjhunwala_style,
    # Aswath Damodaran
    analyze_growth_and_reinvestment,
    analyze_risk_profile,
    calculate_intrinsic_value_dcf,
    analyze_relative_valuation,
    # Growth Agent (fully deterministic)
    analyze_growth_trends,
    ga_analyze_valuation,
    analyze_margin_trends,
    analyze_insider_conviction,
    check_financial_health,
)


# ── JSON serialisation helpers ────────────────────────────────────────────────

def _safe_val(v: Any) -> Any:
    """Coerce numpy scalars and math special values to JSON-safe Python types."""
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def _safe_serialize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _safe_serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_serialize(i) for i in obj]
    if hasattr(obj, "model_dump"):
        return _safe_serialize(obj.model_dump())
    return _safe_val(obj)


# ── raw data loading ──────────────────────────────────────────────────────────

def _load_raw(run_id: str, ticker: str) -> dict:
    path = os.path.join("runs", run_id, "raw", f"{ticker}.json")
    with open(path) as f:
        return json.load(f)


def _rebuild(raw: dict) -> dict:
    """Reconstruct Pydantic model lists from the dicts saved by prepare.py."""

    def _make(cls, lst: list) -> list:
        out = []
        for item in lst or []:
            try:
                out.append(cls(**item))
            except Exception:
                pass
        return out

    metrics = _make(FinancialMetrics, raw.get("financial_metrics", []))
    line_items = _make(LineItem, raw.get("line_items", []))
    insider_trades = _make(InsiderTrade, raw.get("insider_trades", []))
    company_news = _make(CompanyNews, raw.get("company_news", []))
    prices = _make(Price, raw.get("prices", []))
    prices_df = prices_to_df(prices) if prices else pd.DataFrame()

    return {
        "metrics": metrics,
        "line_items": line_items,
        "insider_trades": insider_trades,
        "company_news": company_news,
        "prices": prices,
        "prices_df": prices_df,
        "market_cap": raw.get("market_cap"),
        "start_date": raw.get("start_date"),
        "end_date": raw.get("end_date"),
    }


# ── per-persona facts builders ────────────────────────────────────────────────

def _warren_buffett(m: dict, ticker: str) -> dict:
    metrics, line_items, market_cap = m["metrics"], m["line_items"], m["market_cap"]

    fundamental = analyze_fundamentals(metrics)
    consistency = analyze_consistency(line_items)
    moat = analyze_moat(metrics)
    pricing_power = analyze_pricing_power(line_items, metrics)
    book_value = analyze_book_value_growth(line_items)
    mgmt = wb_analyze_management_quality(line_items)
    intrinsic = wb_calculate_intrinsic_value(line_items)

    total_score = (
        fundamental["score"] + consistency["score"] + moat["score"]
        + mgmt["score"] + pricing_power["score"] + book_value["score"]
    )
    max_score = 10 + moat.get("max_score", 0) + mgmt.get("max_score", 0) + 5 + 5

    iv = intrinsic.get("intrinsic_value")
    margin_of_safety = (iv - market_cap) / market_cap if iv and market_cap else None

    return {
        "ticker": ticker,
        "score": total_score,
        "max_score": max_score,
        "fundamental_analysis": fundamental,
        "consistency_analysis": consistency,
        "moat_analysis": moat,
        "pricing_power_analysis": pricing_power,
        "book_value_analysis": book_value,
        "management_analysis": mgmt,
        "intrinsic_value_analysis": intrinsic,
        "market_cap": market_cap,
        "margin_of_safety": margin_of_safety,
    }


def _charlie_munger(m: dict, ticker: str) -> dict:
    metrics, line_items = m["metrics"], m["line_items"]
    market_cap = m["market_cap"]
    insider_trades = m["insider_trades"]
    company_news = m["company_news"]

    moat = analyze_moat_strength(metrics, line_items)
    mgmt = cm_analyze_management_quality(line_items, insider_trades)
    predictability = analyze_predictability(line_items)
    valuation = calculate_munger_valuation(line_items, market_cap)

    total_score = (
        moat["score"] * 0.35
        + mgmt["score"] * 0.25
        + predictability["score"] * 0.25
        + valuation["score"] * 0.15
    )
    max_score = 10

    if total_score >= 7.5:
        signal = "bullish"
    elif total_score <= 5.5:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "moat_analysis": moat,
        "management_analysis": mgmt,
        "predictability_analysis": predictability,
        "valuation_analysis": valuation,
        "news_sentiment": analyze_news_sentiment(company_news) if company_news else "No news data available",
    }


def _ben_graham(m: dict, ticker: str) -> dict:
    metrics, line_items, market_cap = m["metrics"], m["line_items"], m["market_cap"]

    earnings = analyze_earnings_stability(metrics, line_items)
    strength = analyze_financial_strength(line_items)
    valuation = analyze_valuation_graham(line_items, market_cap)

    total_score = earnings["score"] + strength["score"] + valuation["score"]
    max_score = 15

    if total_score >= 0.7 * max_score:
        signal = "bullish"
    elif total_score <= 0.3 * max_score:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "earnings_analysis": earnings,
        "strength_analysis": strength,
        "valuation_analysis": valuation,
    }


def _bill_ackman(m: dict, ticker: str) -> dict:
    metrics, line_items, market_cap = m["metrics"], m["line_items"], m["market_cap"]

    quality = analyze_business_quality(metrics, line_items)
    balance = analyze_financial_discipline(metrics, line_items)
    activism = analyze_activism_potential(line_items)
    valuation = ba_analyze_valuation(line_items, market_cap)

    total_score = quality["score"] + balance["score"] + activism["score"] + valuation["score"]
    max_score = 20

    if total_score >= 0.7 * max_score:
        signal = "bullish"
    elif total_score <= 0.3 * max_score:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "quality_analysis": quality,
        "balance_sheet_analysis": balance,
        "activism_analysis": activism,
        "valuation_analysis": valuation,
    }


def _cathie_wood(m: dict, ticker: str) -> dict:
    metrics, line_items, market_cap = m["metrics"], m["line_items"], m["market_cap"]

    disruptive = analyze_disruptive_potential(metrics, line_items)
    innovation = analyze_innovation_growth(metrics, line_items)
    valuation = analyze_cathie_wood_valuation(line_items, market_cap)

    total_score = disruptive["score"] + innovation["score"] + valuation["score"]
    max_score = 15

    if total_score >= 0.7 * max_score:
        signal = "bullish"
    elif total_score <= 0.3 * max_score:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "disruptive_analysis": disruptive,
        "innovation_analysis": innovation,
        "valuation_analysis": valuation,
    }


def _michael_burry(m: dict, ticker: str) -> dict:
    metrics, line_items = m["metrics"], m["line_items"]
    insider_trades = m["insider_trades"]
    news = m["company_news"]
    market_cap = m["market_cap"]

    value = _analyze_value(metrics, line_items, market_cap)
    balance = _analyze_balance_sheet(metrics, line_items)
    insider = _analyze_insider_activity(insider_trades)
    contrarian = _analyze_contrarian_sentiment(news)

    total_score = value["score"] + balance["score"] + insider["score"] + contrarian["score"]
    max_score = (
        value["max_score"] + balance["max_score"]
        + insider["max_score"] + contrarian["max_score"]
    )

    if total_score >= 0.7 * max_score:
        signal = "bullish"
    elif total_score <= 0.3 * max_score:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "value_analysis": value,
        "balance_sheet_analysis": balance,
        "insider_analysis": insider,
        "contrarian_analysis": contrarian,
        "market_cap": market_cap,
    }


def _nassim_taleb(m: dict, ticker: str) -> dict:
    metrics, line_items = m["metrics"], m["line_items"]
    insider_trades = m["insider_trades"]
    news = m["company_news"]
    market_cap = m["market_cap"]
    prices_df = m["prices_df"]

    tail_risk = analyze_tail_risk(prices_df)
    antifragility = analyze_antifragility(metrics, line_items, market_cap)
    convexity = analyze_convexity(metrics, line_items, prices_df, market_cap)
    fragility = analyze_fragility(metrics, line_items)
    skin = analyze_skin_in_game(insider_trades)
    vol_regime = analyze_volatility_regime(prices_df)
    black_swan = analyze_black_swan_sentinel(news, prices_df)

    total_score = (
        tail_risk["score"] + antifragility["score"] + convexity["score"]
        + fragility["score"] + skin["score"] + vol_regime["score"] + black_swan["score"]
    )
    max_score = (
        tail_risk["max_score"] + antifragility["max_score"] + convexity["max_score"]
        + fragility["max_score"] + skin["max_score"] + vol_regime["max_score"] + black_swan["max_score"]
    )

    return {
        "ticker": ticker,
        "score": total_score,
        "max_score": max_score,
        "tail_risk_analysis": tail_risk,
        "antifragility_analysis": antifragility,
        "convexity_analysis": convexity,
        "fragility_analysis": fragility,
        "skin_in_game_analysis": skin,
        "volatility_regime_analysis": vol_regime,
        "black_swan_analysis": black_swan,
        "market_cap": market_cap,
    }


def _peter_lynch(m: dict, ticker: str) -> dict:
    line_items = m["line_items"]
    insider_trades = m["insider_trades"]
    company_news = m["company_news"]
    market_cap = m["market_cap"]

    growth = analyze_lynch_growth(line_items)
    fundamentals = analyze_lynch_fundamentals(line_items)
    valuation = analyze_lynch_valuation(line_items, market_cap)
    sentiment = pl_analyze_sentiment(company_news)
    insider = pl_analyze_insider_activity(insider_trades)

    total_score = (
        growth["score"] * 0.30
        + valuation["score"] * 0.25
        + fundamentals["score"] * 0.20
        + sentiment["score"] * 0.15
        + insider["score"] * 0.10
    )
    max_score = 10.0

    if total_score >= 7.5:
        signal = "bullish"
    elif total_score <= 4.5:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "growth_analysis": growth,
        "valuation_analysis": valuation,
        "fundamentals_analysis": fundamentals,
        "sentiment_analysis": sentiment,
        "insider_activity": insider,
    }


def _phil_fisher(m: dict, ticker: str) -> dict:
    line_items = m["line_items"]
    insider_trades = m["insider_trades"]
    company_news = m["company_news"]
    market_cap = m["market_cap"]

    growth_quality = analyze_fisher_growth_quality(line_items)
    margins = analyze_margins_stability(line_items)
    mgmt_eff = analyze_management_efficiency_leverage(line_items)
    valuation = analyze_fisher_valuation(line_items, market_cap)
    insider = pf_analyze_insider_activity(insider_trades)
    sentiment = pf_analyze_sentiment(company_news)

    total_score = (
        growth_quality["score"] * 0.30
        + margins["score"] * 0.25
        + mgmt_eff["score"] * 0.20
        + valuation["score"] * 0.15
        + insider["score"] * 0.05
        + sentiment["score"] * 0.05
    )
    max_score = 10

    if total_score >= 7.5:
        signal = "bullish"
    elif total_score <= 4.5:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "growth_quality": growth_quality,
        "margins_stability": margins,
        "management_efficiency": mgmt_eff,
        "valuation_analysis": valuation,
        "insider_activity": insider,
        "sentiment_analysis": sentiment,
    }


def _stanley_druckenmiller(m: dict, ticker: str) -> dict:
    line_items = m["line_items"]
    insider_trades = m["insider_trades"]
    company_news = m["company_news"]
    prices = m["prices"]
    market_cap = m["market_cap"]

    growth_momentum = analyze_growth_and_momentum(line_items, prices)
    sentiment = sd_analyze_sentiment(company_news)
    insider = sd_analyze_insider_activity(insider_trades)
    risk_reward = analyze_risk_reward(line_items, prices)
    valuation = analyze_druckenmiller_valuation(line_items, market_cap)

    total_score = (
        growth_momentum["score"] * 0.35
        + risk_reward["score"] * 0.20
        + valuation["score"] * 0.20
        + sentiment["score"] * 0.15
        + insider["score"] * 0.10
    )
    max_score = 10

    if total_score >= 7.5:
        signal = "bullish"
    elif total_score <= 4.5:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "growth_momentum_analysis": growth_momentum,
        "sentiment_analysis": sentiment,
        "insider_activity": insider,
        "risk_reward_analysis": risk_reward,
        "valuation_analysis": valuation,
    }


def _mohnish_pabrai(m: dict, ticker: str) -> dict:
    line_items = m["line_items"]
    market_cap = m["market_cap"]

    downside = analyze_downside_protection(line_items)
    valuation = analyze_pabrai_valuation(line_items, market_cap)
    double_pot = analyze_double_potential(line_items, market_cap)

    total_score = (
        downside["score"] * 0.45
        + valuation["score"] * 0.35
        + double_pot["score"] * 0.20
    )
    max_score = 10

    if total_score >= 7.5:
        signal = "bullish"
    elif total_score <= 4.0:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "downside_protection": downside,
        "valuation": valuation,
        "double_potential": double_pot,
        "market_cap": market_cap,
    }


def _rakesh_jhunjhunwala(m: dict, ticker: str) -> dict:
    line_items = m["line_items"]
    market_cap = m["market_cap"]

    # Each helper may fail on ETFs/instruments lacking financial statements
    try:
        growth = analyze_growth(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_growth failed: {exc}")
        growth = {"score": 0, "details": "No data available (ETF or missing financials)"}

    try:
        profitability = analyze_profitability(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_profitability failed: {exc}")
        profitability = {"score": 0, "details": "No data available"}

    try:
        balance = analyze_balance_sheet(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_balance_sheet failed: {exc}")
        balance = {"score": 0, "details": "No data available"}

    try:
        cashflow = analyze_cash_flow(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_cash_flow failed: {exc}")
        cashflow = {"score": 0, "details": "No data available"}

    try:
        mgmt = analyze_management_actions(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_management_actions failed: {exc}")
        mgmt = {"score": 0, "details": "No data available"}

    try:
        intrinsic_value = rj_calculate_intrinsic_value(line_items, market_cap)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: rj_calculate_intrinsic_value failed: {exc}")
        intrinsic_value = None

    total_score = (
        growth["score"] + profitability["score"] + balance["score"]
        + cashflow["score"] + mgmt["score"]
    )
    max_score = 24  # 8(prof) + 7(growth) + 4(bs) + 3(cf) + 2(mgmt)

    margin_of_safety = (
        (intrinsic_value - market_cap) / market_cap
        if intrinsic_value and market_cap else None
    )

    try:
        quality_score = assess_quality_metrics(line_items)
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: assess_quality_metrics failed: {exc}")
        quality_score = 0.5

    if margin_of_safety is not None and margin_of_safety >= 0.30:
        signal = "bullish"
    elif margin_of_safety is not None and margin_of_safety <= -0.30:
        signal = "bearish"
    else:
        if quality_score >= 0.7 and total_score >= max_score * 0.6:
            signal = "bullish"
        elif quality_score <= 0.4 or total_score <= max_score * 0.3:
            signal = "bearish"
        else:
            signal = "neutral"

    try:
        intrinsic_value_analysis = analyze_rakesh_jhunjhunwala_style(
            line_items,
            intrinsic_value=intrinsic_value,
            current_price=market_cap,
        )
    except Exception as exc:
        print(f"  [WARN] rakesh_jhunjhunwala/{ticker}: analyze_rakesh_jhunjhunwala_style failed: {exc}")
        intrinsic_value_analysis = {"details": "Analysis unavailable (ETF or missing financials)"}

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "margin_of_safety": margin_of_safety,
        "growth_analysis": growth,
        "profitability_analysis": profitability,
        "balancesheet_analysis": balance,
        "cashflow_analysis": cashflow,
        "management_analysis": mgmt,
        "intrinsic_value_analysis": intrinsic_value_analysis,
        "intrinsic_value": intrinsic_value,
        "market_cap": market_cap,
    }


def _aswath_damodaran(m: dict, ticker: str) -> dict:
    metrics, line_items = m["metrics"], m["line_items"]
    market_cap = m["market_cap"]

    growth = analyze_growth_and_reinvestment(metrics, line_items)
    risk = analyze_risk_profile(metrics, line_items)
    intrinsic = calculate_intrinsic_value_dcf(metrics, line_items, risk)
    relative_val = analyze_relative_valuation(metrics)

    total_score = growth["score"] + risk["score"] + relative_val["score"]
    max_score = growth["max_score"] + risk["max_score"] + relative_val["max_score"]

    iv = intrinsic.get("intrinsic_value")
    margin_of_safety = (iv - market_cap) / market_cap if iv and market_cap else None

    if margin_of_safety is not None and margin_of_safety >= 0.25:
        signal = "bullish"
    elif margin_of_safety is not None and margin_of_safety <= -0.25:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "score": total_score,
        "max_score": max_score,
        "margin_of_safety": margin_of_safety,
        "growth_analysis": growth,
        "risk_analysis": risk,
        "relative_val_analysis": relative_val,
        "intrinsic_val_analysis": intrinsic,
        "market_cap": market_cap,
    }


def _news_sentiment(m: dict, ticker: str) -> dict:
    """Facts for news_sentiment subagent: just the raw news articles to classify."""
    company_news = m["company_news"] or []
    return {
        "ticker": ticker,
        "company_news": [
            {
                "headline": n.title,
                "sentiment": n.sentiment,
                "date": n.date,
            }
            for n in company_news[:50]
        ],
    }


# ── persona dispatch table ─────────────────────────────────────────────────────

PERSONA_BUILDERS: dict[str, Any] = {
    "warren_buffett": _warren_buffett,
    "charlie_munger": _charlie_munger,
    "ben_graham": _ben_graham,
    "bill_ackman": _bill_ackman,
    "cathie_wood": _cathie_wood,
    "michael_burry": _michael_burry,
    "nassim_taleb": _nassim_taleb,
    "peter_lynch": _peter_lynch,
    "phil_fisher": _phil_fisher,
    "stanley_druckenmiller": _stanley_druckenmiller,
    "mohnish_pabrai": _mohnish_pabrai,
    "rakesh_jhunjhunwala": _rakesh_jhunjhunwala,
    "aswath_damodaran": _aswath_damodaran,
    "news_sentiment": _news_sentiment,
}


# ── growth agent (fully deterministic — writes signal directly) ───────────────

def _run_growth_agent(m: dict, ticker: str) -> dict | None:
    """Run the growth agent and return its signal dict, or None if insufficient data."""
    metrics = m["metrics"]
    insider_trades = m["insider_trades"]

    if not metrics:
        return None

    most_recent = metrics[0]

    growth_trends = analyze_growth_trends(metrics)
    valuation_metrics = ga_analyze_valuation(most_recent)
    margin_trends = analyze_margin_trends(metrics)
    insider_conviction = analyze_insider_conviction(insider_trades)
    financial_health = check_financial_health(most_recent)

    scores = {
        "growth": growth_trends["score"],
        "valuation": valuation_metrics["score"],
        "margins": margin_trends["score"],
        "insider": insider_conviction["score"],
        "health": financial_health["score"],
    }
    weights = {
        "growth": 0.40,
        "valuation": 0.25,
        "margins": 0.15,
        "insider": 0.10,
        "health": 0.10,
    }
    weighted_score = sum(scores[k] * weights[k] for k in scores)

    if weighted_score > 0.6:
        signal = "bullish"
    elif weighted_score < 0.4:
        signal = "bearish"
    else:
        signal = "neutral"

    confidence = round(abs(weighted_score - 0.5) * 2 * 100)

    reasoning = {
        "historical_growth": growth_trends,
        "growth_valuation": valuation_metrics,
        "margin_expansion": margin_trends,
        "insider_conviction": insider_conviction,
        "financial_health": financial_health,
        "final_analysis": {
            "signal": signal,
            "confidence": confidence,
            "weighted_score": round(weighted_score, 2),
        },
    }

    return {"signal": signal, "confidence": confidence, "reasoning": reasoning}


# ── main orchestrator ──────────────────────────────────────────────────────────

def build_all_facts(run_id: str, tickers: list[str]) -> None:
    facts_dir = os.path.join("runs", run_id, "facts")
    signals_dir = os.path.join("runs", run_id, "signals")
    os.makedirs(facts_dir, exist_ok=True)
    os.makedirs(signals_dir, exist_ok=True)

    growth_signals: dict[str, dict] = {}

    for ticker in tickers:
        print(f"\nBuilding facts for {ticker}...")
        raw = _load_raw(run_id, ticker)
        models = _rebuild(raw)

        # growth_agent: fully deterministic → write signal directly to signals/
        growth_result = _run_growth_agent(models, ticker)
        if growth_result:
            growth_signals[ticker] = growth_result
            print(f"  [growth_analyst_agent] signal={growth_result['signal']}")
        else:
            print(f"  [growth_analyst_agent] Not enough metrics, skipping.")

        # Load web research if available
        web_research_path = os.path.join("runs", run_id, "web_research", f"{ticker}.json")
        web_context = None
        if os.path.exists(web_research_path):
            try:
                with open(web_research_path) as f:
                    web_context = json.load(f)
                print(f"  [web_context] Loaded web research for {ticker}")
            except Exception as exc:
                print(f"  [web_context] Failed to load: {exc}")

        # LLM persona facts
        for persona, builder in PERSONA_BUILDERS.items():
            try:
                facts = builder(models, ticker)
                if web_context:
                    facts["web_context"] = web_context
                out_path = os.path.join(facts_dir, f"{persona}__{ticker}.json")
                with open(out_path, "w") as f:
                    json.dump(_safe_serialize(facts), f, indent=2, default=str)
                print(f"  wrote facts/{persona}__{ticker}.json")
            except Exception as exc:
                print(f"  [ERROR] {persona}/{ticker}: {exc}")

    # Write growth_analyst_agent signal so aggregate.py picks it up automatically
    if growth_signals:
        growth_path = os.path.join(signals_dir, "growth_analyst_agent.json")
        with open(growth_path, "w") as f:
            json.dump(_safe_serialize(growth_signals), f, indent=2, default=str)
        print(f"\nWrote signals/growth_analyst_agent.json")


def main():
    parser = argparse.ArgumentParser(description="Build persona facts bundles from raw data.")
    parser.add_argument("--run-id", required=True, help="Run identifier, e.g. 20240101_120000")
    parser.add_argument("--tickers", required=True, help="Comma-separated ticker symbols")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    build_all_facts(args.run_id, tickers)
    print("\nFacts built successfully.")


if __name__ == "__main__":
    main()
