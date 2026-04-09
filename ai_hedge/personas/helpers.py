"""Verbatim helper functions from upstream persona agents.
Duplicate function names across personas are prefixed with a persona short-code.
Short codes: wb=warren_buffett, cm=charlie_munger, bg=ben_graham, ba=bill_ackman,
cw=cathie_wood, mb=michael_burry, nt=nassim_taleb, pl=peter_lynch, pf=phil_fisher,
sd=stanley_druckenmiller, mp=mohnish_pabrai, rj=rakesh_jhunjhunwala,
ad=aswath_damodaran, ga=growth_agent, ns=news_sentiment
"""
from __future__ import annotations
import math, statistics
from typing import Any
import numpy as np
import pandas as pd
from ai_hedge.data.api import get_financial_metrics, search_line_items, get_market_cap, get_insider_trades, get_company_news, get_prices, prices_to_df
from ai_hedge.data.models import FinancialMetrics, LineItem, InsiderTrade, CompanyNews, Price


# ==========================
# Warren Buffett helpers
# ==========================

def analyze_fundamentals(metrics: list) -> dict[str, any]:
    """Analyze company fundamentals based on Buffett's criteria."""
    if not metrics:
        return {"score": 0, "details": "Insufficient fundamental data"}

    latest_metrics = metrics[0]

    score = 0
    reasoning = []

    # Check ROE (Return on Equity)
    if latest_metrics.return_on_equity and latest_metrics.return_on_equity > 0.15:  # 15% ROE threshold
        score += 2
        reasoning.append(f"Strong ROE of {latest_metrics.return_on_equity:.1%}")
    elif latest_metrics.return_on_equity:
        reasoning.append(f"Weak ROE of {latest_metrics.return_on_equity:.1%}")
    else:
        reasoning.append("ROE data not available")

    # Check Debt to Equity
    if latest_metrics.debt_to_equity and latest_metrics.debt_to_equity < 0.5:
        score += 2
        reasoning.append("Conservative debt levels")
    elif latest_metrics.debt_to_equity:
        reasoning.append(f"High debt to equity ratio of {latest_metrics.debt_to_equity:.1f}")
    else:
        reasoning.append("Debt to equity data not available")

    # Check Operating Margin
    if latest_metrics.operating_margin and latest_metrics.operating_margin > 0.15:
        score += 2
        reasoning.append("Strong operating margins")
    elif latest_metrics.operating_margin:
        reasoning.append(f"Weak operating margin of {latest_metrics.operating_margin:.1%}")
    else:
        reasoning.append("Operating margin data not available")

    # Check Current Ratio
    if latest_metrics.current_ratio and latest_metrics.current_ratio > 1.5:
        score += 1
        reasoning.append("Good liquidity position")
    elif latest_metrics.current_ratio:
        reasoning.append(f"Weak liquidity with current ratio of {latest_metrics.current_ratio:.1f}")
    else:
        reasoning.append("Current ratio data not available")

    return {"score": score, "details": "; ".join(reasoning), "metrics": latest_metrics.model_dump()}

def analyze_consistency(financial_line_items: list) -> dict[str, any]:
    """Analyze earnings consistency and growth."""
    if len(financial_line_items) < 4:  # Need at least 4 periods for trend analysis
        return {"score": 0, "details": "Insufficient historical data"}

    score = 0
    reasoning = []

    # Check earnings growth trend
    earnings_values = [item.net_income for item in financial_line_items if item.net_income]
    if len(earnings_values) >= 4:
        # Simple check: is each period's earnings bigger than the next?
        earnings_growth = all(earnings_values[i] > earnings_values[i + 1] for i in range(len(earnings_values) - 1))

        if earnings_growth:
            score += 3
            reasoning.append("Consistent earnings growth over past periods")
        else:
            reasoning.append("Inconsistent earnings growth pattern")

        # Calculate total growth rate from oldest to latest
        if len(earnings_values) >= 2 and earnings_values[-1] != 0:
            growth_rate = (earnings_values[0] - earnings_values[-1]) / abs(earnings_values[-1])
            reasoning.append(f"Total earnings growth of {growth_rate:.1%} over past {len(earnings_values)} periods")
    else:
        reasoning.append("Insufficient earnings data for trend analysis")

    return {
        "score": score,
        "details": "; ".join(reasoning),
    }

def analyze_moat(metrics: list) -> dict[str, any]:
    """
    Evaluate whether the company likely has a durable competitive advantage (moat).
    Enhanced to include multiple moat indicators that Buffett actually looks for:
    1. Consistent high returns on capital
    2. Pricing power (stable/growing margins)
    3. Scale advantages (improving metrics with size)
    4. Brand strength (inferred from margins and consistency)
    5. Switching costs (inferred from customer retention)
    """
    if not metrics or len(metrics) < 5:  # Need more data for proper moat analysis
        return {"score": 0, "max_score": 5, "details": "Insufficient data for comprehensive moat analysis"}

    reasoning = []
    moat_score = 0
    max_score = 5

    # 1. Return on Capital Consistency (Buffett's favorite moat indicator)
    historical_roes = [m.return_on_equity for m in metrics if m.return_on_equity is not None]
    historical_roics = [m.return_on_invested_capital for m in metrics if
                        hasattr(m, 'return_on_invested_capital') and m.return_on_invested_capital is not None]

    if len(historical_roes) >= 5:
        # Check for consistently high ROE (>15% for most periods)
        high_roe_periods = sum(1 for roe in historical_roes if roe > 0.15)
        roe_consistency = high_roe_periods / len(historical_roes)

        if roe_consistency >= 0.8:  # 80%+ of periods with ROE > 15%
            moat_score += 2
            avg_roe = sum(historical_roes) / len(historical_roes)
            reasoning.append(
                f"Excellent ROE consistency: {high_roe_periods}/{len(historical_roes)} periods >15% (avg: {avg_roe:.1%}) - indicates durable competitive advantage")
        elif roe_consistency >= 0.6:
            moat_score += 1
            reasoning.append(f"Good ROE performance: {high_roe_periods}/{len(historical_roes)} periods >15%")
        else:
            reasoning.append(f"Inconsistent ROE: only {high_roe_periods}/{len(historical_roes)} periods >15%")
    else:
        reasoning.append("Insufficient ROE history for moat analysis")

    # 2. Operating Margin Stability (Pricing Power Indicator)
    historical_margins = [m.operating_margin for m in metrics if m.operating_margin is not None]
    if len(historical_margins) >= 5:
        # Check for stable or improving margins (sign of pricing power)
        avg_margin = sum(historical_margins) / len(historical_margins)
        recent_margins = historical_margins[:3]  # Last 3 periods
        older_margins = historical_margins[-3:]  # First 3 periods

        recent_avg = sum(recent_margins) / len(recent_margins)
        older_avg = sum(older_margins) / len(older_margins)

        if avg_margin > 0.2 and recent_avg >= older_avg:  # 20%+ margins and stable/improving
            moat_score += 1
            reasoning.append(f"Strong and stable operating margins (avg: {avg_margin:.1%}) indicate pricing power moat")
        elif avg_margin > 0.15:  # At least decent margins
            reasoning.append(f"Decent operating margins (avg: {avg_margin:.1%}) suggest some competitive advantage")
        else:
            reasoning.append(f"Low operating margins (avg: {avg_margin:.1%}) suggest limited pricing power")

    # 3. Asset Efficiency and Scale Advantages
    if len(metrics) >= 5:
        # Check asset turnover trends (revenue efficiency)
        asset_turnovers = []
        for m in metrics:
            if hasattr(m, 'asset_turnover') and m.asset_turnover is not None:
                asset_turnovers.append(m.asset_turnover)

        if len(asset_turnovers) >= 3:
            if any(turnover > 1.0 for turnover in asset_turnovers):  # Efficient asset use
                moat_score += 1
                reasoning.append("Efficient asset utilization suggests operational moat")

    # 4. Competitive Position Strength (inferred from trend stability)
    if len(historical_roes) >= 5 and len(historical_margins) >= 5:
        # Calculate coefficient of variation (stability measure)
        roe_avg = sum(historical_roes) / len(historical_roes)
        roe_variance = sum((roe - roe_avg) ** 2 for roe in historical_roes) / len(historical_roes)
        roe_stability = 1 - (roe_variance ** 0.5) / roe_avg if roe_avg > 0 else 0

        margin_avg = sum(historical_margins) / len(historical_margins)
        margin_variance = sum((margin - margin_avg) ** 2 for margin in historical_margins) / len(historical_margins)
        margin_stability = 1 - (margin_variance ** 0.5) / margin_avg if margin_avg > 0 else 0

        overall_stability = (roe_stability + margin_stability) / 2

        if overall_stability > 0.7:  # High stability indicates strong competitive position
            moat_score += 1
            reasoning.append(f"High performance stability ({overall_stability:.1%}) suggests strong competitive moat")

    # Cap the score at max_score
    moat_score = min(moat_score, max_score)

    return {
        "score": moat_score,
        "max_score": max_score,
        "details": "; ".join(reasoning) if reasoning else "Limited moat analysis available",
    }

def wb_analyze_management_quality(financial_line_items: list) -> dict[str, any]:
    """
    Checks for share dilution or consistent buybacks, and some dividend track record.
    A simplified approach:
      - if there's net share repurchase or stable share count, it suggests management
        might be shareholder-friendly.
      - if there's a big new issuance, it might be a negative sign (dilution).
    """
    if not financial_line_items:
        return {"score": 0, "max_score": 2, "details": "Insufficient data for management analysis"}

    reasoning = []
    mgmt_score = 0

    latest = financial_line_items[0]
    if hasattr(latest,
               "issuance_or_purchase_of_equity_shares") and latest.issuance_or_purchase_of_equity_shares and latest.issuance_or_purchase_of_equity_shares < 0:
        # Negative means the company spent money on buybacks
        mgmt_score += 1
        reasoning.append("Company has been repurchasing shares (shareholder-friendly)")

    if hasattr(latest,
               "issuance_or_purchase_of_equity_shares") and latest.issuance_or_purchase_of_equity_shares and latest.issuance_or_purchase_of_equity_shares > 0:
        # Positive issuance means new shares => possible dilution
        reasoning.append("Recent common stock issuance (potential dilution)")
    else:
        reasoning.append("No significant new stock issuance detected")

    # Check for any dividends
    if hasattr(latest,
               "dividends_and_other_cash_distributions") and latest.dividends_and_other_cash_distributions and latest.dividends_and_other_cash_distributions < 0:
        mgmt_score += 1
        reasoning.append("Company has a track record of paying dividends")
    else:
        reasoning.append("No or minimal dividends paid")

    return {
        "score": mgmt_score,
        "max_score": 2,
        "details": "; ".join(reasoning),
    }

def calculate_owner_earnings(financial_line_items: list) -> dict[str, any]:
    """
    Calculate owner earnings (Buffett's preferred measure of true earnings power).
    Enhanced methodology: Net Income + Depreciation/Amortization - Maintenance CapEx - Working Capital Changes
    Uses multi-period analysis for better maintenance capex estimation.
    """
    if not financial_line_items or len(financial_line_items) < 2:
        return {"owner_earnings": None, "details": ["Insufficient data for owner earnings calculation"]}

    latest = financial_line_items[0]
    details = []

    # Core components
    net_income = latest.net_income
    depreciation = latest.depreciation_and_amortization
    capex = latest.capital_expenditure

    if not all([net_income is not None, depreciation is not None, capex is not None]):
        missing = []
        if net_income is None: missing.append("net income")
        if depreciation is None: missing.append("depreciation")
        if capex is None: missing.append("capital expenditure")
        return {"owner_earnings": None, "details": [f"Missing components: {', '.join(missing)}"]}

    # Enhanced maintenance capex estimation using historical analysis
    maintenance_capex = estimate_maintenance_capex(financial_line_items)

    # Working capital change analysis (if data available)
    working_capital_change = 0
    if len(financial_line_items) >= 2:
        try:
            current_assets_current = getattr(latest, 'current_assets', None)
            current_liab_current = getattr(latest, 'current_liabilities', None)

            previous = financial_line_items[1]
            current_assets_previous = getattr(previous, 'current_assets', None)
            current_liab_previous = getattr(previous, 'current_liabilities', None)

            if all([current_assets_current, current_liab_current, current_assets_previous, current_liab_previous]):
                wc_current = current_assets_current - current_liab_current
                wc_previous = current_assets_previous - current_liab_previous
                working_capital_change = wc_current - wc_previous
                details.append(f"Working capital change: ${working_capital_change:,.0f}")
        except:
            pass  # Skip working capital adjustment if data unavailable

    # Calculate owner earnings
    owner_earnings = net_income + depreciation - maintenance_capex - working_capital_change

    # Sanity checks
    if owner_earnings < net_income * 0.3:  # Owner earnings shouldn't be less than 30% of net income typically
        details.append("Warning: Owner earnings significantly below net income - high capex intensity")

    if maintenance_capex > depreciation * 2:  # Maintenance capex shouldn't typically exceed 2x depreciation
        details.append("Warning: Estimated maintenance capex seems high relative to depreciation")

    details.extend([
        f"Net income: ${net_income:,.0f}",
        f"Depreciation: ${depreciation:,.0f}",
        f"Estimated maintenance capex: ${maintenance_capex:,.0f}",
        f"Owner earnings: ${owner_earnings:,.0f}"
    ])

    return {
        "owner_earnings": owner_earnings,
        "components": {
            "net_income": net_income,
            "depreciation": depreciation,
            "maintenance_capex": maintenance_capex,
            "working_capital_change": working_capital_change,
            "total_capex": abs(capex) if capex else 0
        },
        "details": details,
    }

def estimate_maintenance_capex(financial_line_items: list) -> float:
    """
    Estimate maintenance capital expenditure using multiple approaches.
    Buffett considers this crucial for understanding true owner earnings.
    """
    if not financial_line_items:
        return 0

    # Approach 1: Historical average as % of revenue
    capex_ratios = []
    depreciation_values = []

    for item in financial_line_items[:5]:  # Last 5 periods
        if hasattr(item, 'capital_expenditure') and hasattr(item, 'revenue'):
            if item.capital_expenditure and item.revenue and item.revenue > 0:
                capex_ratio = abs(item.capital_expenditure) / item.revenue
                capex_ratios.append(capex_ratio)

        if hasattr(item, 'depreciation_and_amortization') and item.depreciation_and_amortization:
            depreciation_values.append(item.depreciation_and_amortization)

    # Approach 2: Percentage of depreciation (typically 80-120% for maintenance)
    latest_depreciation = financial_line_items[0].depreciation_and_amortization if financial_line_items[
        0].depreciation_and_amortization else 0

    # Approach 3: Industry-specific heuristics
    latest_capex = abs(financial_line_items[0].capital_expenditure) if financial_line_items[
        0].capital_expenditure else 0

    # Conservative estimate: Use the higher of:
    # 1. 85% of total capex (assuming 15% is growth capex)
    # 2. 100% of depreciation (replacement of worn-out assets)
    # 3. Historical average if stable

    method_1 = latest_capex * 0.85  # 85% of total capex
    method_2 = latest_depreciation  # 100% of depreciation

    # If we have historical data, use average capex ratio
    if len(capex_ratios) >= 3:
        avg_capex_ratio = sum(capex_ratios) / len(capex_ratios)
        latest_revenue = financial_line_items[0].revenue if hasattr(financial_line_items[0], 'revenue') and \
                                                            financial_line_items[0].revenue else 0
        method_3 = avg_capex_ratio * latest_revenue if latest_revenue else 0

        # Use the median of the three approaches for conservatism
        estimates = sorted([method_1, method_2, method_3])
        return estimates[1]  # Median
    else:
        # Use the higher of method 1 and 2
        return max(method_1, method_2)

def wb_calculate_intrinsic_value(financial_line_items: list) -> dict[str, any]:
    """
    Calculate intrinsic value using enhanced DCF with owner earnings.
    Uses more sophisticated assumptions and conservative approach like Buffett.
    """
    if not financial_line_items or len(financial_line_items) < 3:
        return {"intrinsic_value": None, "details": ["Insufficient data for reliable valuation"]}

    # Calculate owner earnings with better methodology
    earnings_data = calculate_owner_earnings(financial_line_items)
    if not earnings_data["owner_earnings"]:
        return {"intrinsic_value": None, "details": earnings_data["details"]}

    owner_earnings = earnings_data["owner_earnings"]
    latest_financial_line_items = financial_line_items[0]
    shares_outstanding = latest_financial_line_items.outstanding_shares

    if not shares_outstanding or shares_outstanding <= 0:
        return {"intrinsic_value": None, "details": ["Missing or invalid shares outstanding data"]}

    # Enhanced DCF with more realistic assumptions
    details = []

    # Estimate growth rate based on historical performance (more conservative)
    historical_earnings = []
    for item in financial_line_items[:5]:  # Last 5 years
        if hasattr(item, 'net_income') and item.net_income:
            historical_earnings.append(item.net_income)

    # Calculate historical growth rate
    if len(historical_earnings) >= 3:
        oldest_earnings = historical_earnings[-1]
        latest_earnings = historical_earnings[0]
        years = len(historical_earnings) - 1

        if oldest_earnings > 0:
            historical_growth = ((latest_earnings / oldest_earnings) ** (1 / years)) - 1
            # Conservative adjustment - cap growth and apply haircut
            historical_growth = max(-0.05, min(historical_growth, 0.15))  # Cap between -5% and 15%
            conservative_growth = historical_growth * 0.7  # Apply 30% haircut for conservatism
        else:
            conservative_growth = 0.03  # Default 3% if negative base
    else:
        conservative_growth = 0.03  # Default conservative growth

    # Buffett's conservative assumptions
    stage1_growth = min(conservative_growth, 0.08)  # Stage 1: cap at 8%
    stage2_growth = min(conservative_growth * 0.5, 0.04)  # Stage 2: half of stage 1, cap at 4%
    terminal_growth = 0.025  # Long-term GDP growth rate

    # Risk-adjusted discount rate based on business quality
    base_discount_rate = 0.09  # Base 9%

    # Adjust based on analysis scores (if available in calling context)
    # For now, use conservative 10%
    discount_rate = 0.10

    # Three-stage DCF model
    stage1_years = 5  # High growth phase
    stage2_years = 5  # Transition phase

    present_value = 0
    details.append(
        f"Using three-stage DCF: Stage 1 ({stage1_growth:.1%}, {stage1_years}y), Stage 2 ({stage2_growth:.1%}, {stage2_years}y), Terminal ({terminal_growth:.1%})")

    # Stage 1: Higher growth
    stage1_pv = 0
    for year in range(1, stage1_years + 1):
        future_earnings = owner_earnings * (1 + stage1_growth) ** year
        pv = future_earnings / (1 + discount_rate) ** year
        stage1_pv += pv

    # Stage 2: Transition growth
    stage2_pv = 0
    stage1_final_earnings = owner_earnings * (1 + stage1_growth) ** stage1_years
    for year in range(1, stage2_years + 1):
        future_earnings = stage1_final_earnings * (1 + stage2_growth) ** year
        pv = future_earnings / (1 + discount_rate) ** (stage1_years + year)
        stage2_pv += pv

    # Terminal value using Gordon Growth Model
    final_earnings = stage1_final_earnings * (1 + stage2_growth) ** stage2_years
    terminal_earnings = final_earnings * (1 + terminal_growth)
    terminal_value = terminal_earnings / (discount_rate - terminal_growth)
    terminal_pv = terminal_value / (1 + discount_rate) ** (stage1_years + stage2_years)

    # Total intrinsic value
    intrinsic_value = stage1_pv + stage2_pv + terminal_pv

    # Apply additional margin of safety (Buffett's conservatism)
    conservative_intrinsic_value = intrinsic_value * 0.85  # 15% additional haircut

    details.extend([
        f"Stage 1 PV: ${stage1_pv:,.0f}",
        f"Stage 2 PV: ${stage2_pv:,.0f}",
        f"Terminal PV: ${terminal_pv:,.0f}",
        f"Total IV: ${intrinsic_value:,.0f}",
        f"Conservative IV (15% haircut): ${conservative_intrinsic_value:,.0f}",
        f"Owner earnings: ${owner_earnings:,.0f}",
        f"Discount rate: {discount_rate:.1%}"
    ])

    return {
        "intrinsic_value": conservative_intrinsic_value,
        "raw_intrinsic_value": intrinsic_value,
        "owner_earnings": owner_earnings,
        "assumptions": {
            "stage1_growth": stage1_growth,
            "stage2_growth": stage2_growth,
            "terminal_growth": terminal_growth,
            "discount_rate": discount_rate,
            "stage1_years": stage1_years,
            "stage2_years": stage2_years,
            "historical_growth": conservative_growth if 'conservative_growth' in locals() else None,
        },
        "details": details,
    }

def analyze_book_value_growth(financial_line_items: list) -> dict[str, any]:
    """Analyze book value per share growth - a key Buffett metric."""
    if len(financial_line_items) < 3:
        return {"score": 0, "details": "Insufficient data for book value analysis"}

    # Extract book values per share
    book_values = [
        item.shareholders_equity / item.outstanding_shares
        for item in financial_line_items
        if hasattr(item, 'shareholders_equity') and hasattr(item, 'outstanding_shares')
        and item.shareholders_equity and item.outstanding_shares
    ]

    if len(book_values) < 3:
        return {"score": 0, "details": "Insufficient book value data for growth analysis"}

    score = 0
    reasoning = []

    # Analyze growth consistency
    growth_periods = sum(1 for i in range(len(book_values) - 1) if book_values[i] > book_values[i + 1])
    growth_rate = growth_periods / (len(book_values) - 1)

    # Score based on consistency
    if growth_rate >= 0.8:
        score += 3
        reasoning.append("Consistent book value per share growth (Buffett's favorite metric)")
    elif growth_rate >= 0.6:
        score += 2
        reasoning.append("Good book value per share growth pattern")
    elif growth_rate >= 0.4:
        score += 1
        reasoning.append("Moderate book value per share growth")
    else:
        reasoning.append("Inconsistent book value per share growth")

    # Calculate and score CAGR
    cagr_score, cagr_reason = _calculate_book_value_cagr(book_values)
    score += cagr_score
    reasoning.append(cagr_reason)

    return {"score": score, "details": "; ".join(reasoning)}

def _calculate_book_value_cagr(book_values: list) -> tuple[int, str]:
    """Helper function to safely calculate book value CAGR and return score + reasoning."""
    if len(book_values) < 2:
        return 0, "Insufficient data for CAGR calculation"

    oldest_bv, latest_bv = book_values[-1], book_values[0]
    years = len(book_values) - 1

    # Handle different scenarios
    if oldest_bv > 0 and latest_bv > 0:
        cagr = ((latest_bv / oldest_bv) ** (1 / years)) - 1
        if cagr > 0.15:
            return 2, f"Excellent book value CAGR: {cagr:.1%}"
        elif cagr > 0.1:
            return 1, f"Good book value CAGR: {cagr:.1%}"
        else:
            return 0, f"Book value CAGR: {cagr:.1%}"
    elif oldest_bv < 0 < latest_bv:
        return 3, "Excellent: Company improved from negative to positive book value"
    elif oldest_bv > 0 > latest_bv:
        return 0, "Warning: Company declined from positive to negative book value"
    else:
        return 0, "Unable to calculate meaningful book value CAGR due to negative values"

def analyze_pricing_power(financial_line_items: list, metrics: list) -> dict[str, any]:
    """
    Analyze pricing power - Buffett's key indicator of a business moat.
    Looks at ability to raise prices without losing customers (margin expansion during inflation).
    """
    if not financial_line_items or not metrics:
        return {"score": 0, "details": "Insufficient data for pricing power analysis"}

    score = 0
    reasoning = []

    # Check gross margin trends (ability to maintain/expand margins)
    gross_margins = []
    for item in financial_line_items:
        if hasattr(item, 'gross_margin') and item.gross_margin is not None:
            gross_margins.append(item.gross_margin)

    if len(gross_margins) >= 3:
        # Check margin stability/improvement
        recent_avg = sum(gross_margins[:2]) / 2 if len(gross_margins) >= 2 else gross_margins[0]
        older_avg = sum(gross_margins[-2:]) / 2 if len(gross_margins) >= 2 else gross_margins[-1]

        if recent_avg > older_avg + 0.02:  # 2%+ improvement
            score += 3
            reasoning.append("Expanding gross margins indicate strong pricing power")
        elif recent_avg > older_avg:
            score += 2
            reasoning.append("Improving gross margins suggest good pricing power")
        elif abs(recent_avg - older_avg) < 0.01:  # Stable within 1%
            score += 1
            reasoning.append("Stable gross margins during economic uncertainty")
        else:
            reasoning.append("Declining gross margins may indicate pricing pressure")

    # Check if company has been able to maintain high margins consistently
    if gross_margins:
        avg_margin = sum(gross_margins) / len(gross_margins)
        if avg_margin > 0.5:  # 50%+ gross margins
            score += 2
            reasoning.append(f"Consistently high gross margins ({avg_margin:.1%}) indicate strong pricing power")
        elif avg_margin > 0.3:  # 30%+ gross margins
            score += 1
            reasoning.append(f"Good gross margins ({avg_margin:.1%}) suggest decent pricing power")

    return {
        "score": score,
        "details": "; ".join(reasoning) if reasoning else "Limited pricing power analysis available"
    }


# ==========================
# Charlie Munger helpers
# ==========================

def analyze_moat_strength(metrics: list, financial_line_items: list) -> dict:
    """
    Analyze the business's competitive advantage using Munger's approach:
    - Consistent high returns on capital (ROIC)
    - Pricing power (stable/improving gross margins)
    - Low capital requirements
    - Network effects and intangible assets (R&D investments, goodwill)
    """
    score = 0
    details = []
    
    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze moat strength"
        }
    
    # 1. Return on Invested Capital (ROIC) analysis - Munger's favorite metric
    roic_values = [item.return_on_invested_capital for item in financial_line_items 
                   if hasattr(item, 'return_on_invested_capital') and item.return_on_invested_capital is not None]
    
    if roic_values:
        # Check if ROIC consistently above 15% (Munger's threshold)
        high_roic_count = sum(1 for r in roic_values if r > 0.15)
        if high_roic_count >= len(roic_values) * 0.8:  # 80% of periods show high ROIC
            score += 3
            details.append(f"Excellent ROIC: >15% in {high_roic_count}/{len(roic_values)} periods")
        elif high_roic_count >= len(roic_values) * 0.5:  # 50% of periods
            score += 2
            details.append(f"Good ROIC: >15% in {high_roic_count}/{len(roic_values)} periods")
        elif high_roic_count > 0:
            score += 1
            details.append(f"Mixed ROIC: >15% in only {high_roic_count}/{len(roic_values)} periods")
        else:
            details.append("Poor ROIC: Never exceeds 15% threshold")
    else:
        details.append("No ROIC data available")
    
    # 2. Pricing power - check gross margin stability and trends
    gross_margins = [item.gross_margin for item in financial_line_items 
                    if hasattr(item, 'gross_margin') and item.gross_margin is not None]
    
    if gross_margins and len(gross_margins) >= 3:
        # Munger likes stable or improving gross margins
        margin_trend = sum(1 for i in range(1, len(gross_margins)) if gross_margins[i] >= gross_margins[i-1])
        if margin_trend >= len(gross_margins) * 0.7:  # Improving in 70% of periods
            score += 2
            details.append("Strong pricing power: Gross margins consistently improving")
        elif sum(gross_margins) / len(gross_margins) > 0.3:  # Average margin > 30%
            score += 1
            details.append(f"Good pricing power: Average gross margin {sum(gross_margins)/len(gross_margins):.1%}")
        else:
            details.append("Limited pricing power: Low or declining gross margins")
    else:
        details.append("Insufficient gross margin data")
    
    # 3. Capital intensity - Munger prefers low capex businesses
    if len(financial_line_items) >= 3:
        capex_to_revenue = []
        for item in financial_line_items:
            if (hasattr(item, 'capital_expenditure') and item.capital_expenditure is not None and 
                hasattr(item, 'revenue') and item.revenue is not None and item.revenue > 0):
                # Note: capital_expenditure is typically negative in financial statements
                capex_ratio = abs(item.capital_expenditure) / item.revenue
                capex_to_revenue.append(capex_ratio)
        
        if capex_to_revenue:
            avg_capex_ratio = sum(capex_to_revenue) / len(capex_to_revenue)
            if avg_capex_ratio < 0.05:  # Less than 5% of revenue
                score += 2
                details.append(f"Low capital requirements: Avg capex {avg_capex_ratio:.1%} of revenue")
            elif avg_capex_ratio < 0.10:  # Less than 10% of revenue
                score += 1
                details.append(f"Moderate capital requirements: Avg capex {avg_capex_ratio:.1%} of revenue")
            else:
                details.append(f"High capital requirements: Avg capex {avg_capex_ratio:.1%} of revenue")
        else:
            details.append("No capital expenditure data available")
    else:
        details.append("Insufficient data for capital intensity analysis")
    
    # 4. Intangible assets - Munger values R&D and intellectual property
    r_and_d = [item.research_and_development for item in financial_line_items
              if hasattr(item, 'research_and_development') and item.research_and_development is not None]
    
    goodwill_and_intangible_assets = [item.goodwill_and_intangible_assets for item in financial_line_items
               if hasattr(item, 'goodwill_and_intangible_assets') and item.goodwill_and_intangible_assets is not None]

    if r_and_d and len(r_and_d) > 0:
        if sum(r_and_d) > 0:  # If company is investing in R&D
            score += 1
            details.append("Invests in R&D, building intellectual property")
    
    if (goodwill_and_intangible_assets and len(goodwill_and_intangible_assets) > 0):
        score += 1
        details.append("Significant goodwill/intangible assets, suggesting brand value or IP")
    
    # Scale score to 0-10 range
    final_score = min(10, score * 10 / 9)  # Max possible raw score is 9
    
    return {
        "score": final_score,
        "details": "; ".join(details)
        
    }

def cm_analyze_management_quality(financial_line_items: list, insider_trades: list) -> dict:
    """
    Evaluate management quality using Munger's criteria:
    - Capital allocation wisdom
    - Insider ownership and transactions
    - Cash management efficiency
    - Candor and transparency
    - Long-term focus
    """
    score = 0
    details = []
    
    if not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze management quality"
        }
    
    # 1. Capital allocation - Check FCF to net income ratio
    # Munger values companies that convert earnings to cash
    fcf_values = [item.free_cash_flow for item in financial_line_items 
                 if hasattr(item, 'free_cash_flow') and item.free_cash_flow is not None]
    
    net_income_values = [item.net_income for item in financial_line_items 
                        if hasattr(item, 'net_income') and item.net_income is not None]
    
    if fcf_values and net_income_values and len(fcf_values) == len(net_income_values):
        # Calculate FCF to Net Income ratio for each period
        fcf_to_ni_ratios = []
        for i in range(len(fcf_values)):
            if net_income_values[i] and net_income_values[i] > 0:
                fcf_to_ni_ratios.append(fcf_values[i] / net_income_values[i])
        
        if fcf_to_ni_ratios:
            avg_ratio = sum(fcf_to_ni_ratios) / len(fcf_to_ni_ratios)
            if avg_ratio > 1.1:  # FCF > net income suggests good accounting
                score += 3
                details.append(f"Excellent cash conversion: FCF/NI ratio of {avg_ratio:.2f}")
            elif avg_ratio > 0.9:  # FCF roughly equals net income
                score += 2
                details.append(f"Good cash conversion: FCF/NI ratio of {avg_ratio:.2f}")
            elif avg_ratio > 0.7:  # FCF somewhat lower than net income
                score += 1
                details.append(f"Moderate cash conversion: FCF/NI ratio of {avg_ratio:.2f}")
            else:
                details.append(f"Poor cash conversion: FCF/NI ratio of only {avg_ratio:.2f}")
        else:
            details.append("Could not calculate FCF to Net Income ratios")
    else:
        details.append("Missing FCF or Net Income data")
    
    # 2. Debt management - Munger is cautious about debt
    debt_values = [item.total_debt for item in financial_line_items 
                  if hasattr(item, 'total_debt') and item.total_debt is not None]
    
    equity_values = [item.shareholders_equity for item in financial_line_items 
                    if hasattr(item, 'shareholders_equity') and item.shareholders_equity is not None]
    
    if debt_values and equity_values and len(debt_values) == len(equity_values):
        # Calculate D/E ratio for most recent period
        recent_de_ratio = debt_values[0] / equity_values[0] if equity_values[0] > 0 else float('inf')
        
        if recent_de_ratio < 0.3:  # Very low debt
            score += 3
            details.append(f"Conservative debt management: D/E ratio of {recent_de_ratio:.2f}")
        elif recent_de_ratio < 0.7:  # Moderate debt
            score += 2
            details.append(f"Prudent debt management: D/E ratio of {recent_de_ratio:.2f}")
        elif recent_de_ratio < 1.5:  # Higher but still reasonable debt
            score += 1
            details.append(f"Moderate debt level: D/E ratio of {recent_de_ratio:.2f}")
        else:
            details.append(f"High debt level: D/E ratio of {recent_de_ratio:.2f}")
    else:
        details.append("Missing debt or equity data")
    
    # 3. Cash management efficiency - Munger values appropriate cash levels
    cash_values = [item.cash_and_equivalents for item in financial_line_items
                  if hasattr(item, 'cash_and_equivalents') and item.cash_and_equivalents is not None]
    revenue_values = [item.revenue for item in financial_line_items
                     if hasattr(item, 'revenue') and item.revenue is not None]
    
    if cash_values and revenue_values and len(cash_values) > 0 and len(revenue_values) > 0:
        # Calculate cash to revenue ratio (Munger likes 10-20% for most businesses)
        cash_to_revenue = cash_values[0] / revenue_values[0] if revenue_values[0] > 0 else 0
        
        if 0.1 <= cash_to_revenue <= 0.25:
            # Goldilocks zone - not too much, not too little
            score += 2
            details.append(f"Prudent cash management: Cash/Revenue ratio of {cash_to_revenue:.2f}")
        elif 0.05 <= cash_to_revenue < 0.1 or 0.25 < cash_to_revenue <= 0.4:
            # Reasonable but not ideal
            score += 1
            details.append(f"Acceptable cash position: Cash/Revenue ratio of {cash_to_revenue:.2f}")
        elif cash_to_revenue > 0.4:
            # Too much cash - potentially inefficient capital allocation
            details.append(f"Excess cash reserves: Cash/Revenue ratio of {cash_to_revenue:.2f}")
        else:
            # Too little cash - potentially risky
            details.append(f"Low cash reserves: Cash/Revenue ratio of {cash_to_revenue:.2f}")
    else:
        details.append("Insufficient cash or revenue data")
    
    # 4. Insider activity - Munger values skin in the game
    if insider_trades and len(insider_trades) > 0:
        # Count buys vs. sells
        buys = sum(1 for trade in insider_trades if hasattr(trade, 'transaction_type') and 
                   trade.transaction_type and trade.transaction_type.lower() in ['buy', 'purchase'])
        sells = sum(1 for trade in insider_trades if hasattr(trade, 'transaction_type') and 
                    trade.transaction_type and trade.transaction_type.lower() in ['sell', 'sale'])
        
        # Calculate the buy ratio
        total_trades = buys + sells
        if total_trades > 0:
            buy_ratio = buys / total_trades
            if buy_ratio > 0.7:  # Strong insider buying
                score += 2
                details.append(f"Strong insider buying: {buys}/{total_trades} transactions are purchases")
            elif buy_ratio > 0.4:  # Balanced insider activity
                score += 1
                details.append(f"Balanced insider trading: {buys}/{total_trades} transactions are purchases")
            elif buy_ratio < 0.1 and sells > 5:  # Heavy selling
                score -= 1  # Penalty for excessive selling
                details.append(f"Concerning insider selling: {sells}/{total_trades} transactions are sales")
            else:
                details.append(f"Mixed insider activity: {buys}/{total_trades} transactions are purchases")
        else:
            details.append("No recorded insider transactions")
    else:
        details.append("No insider trading data available")
    
    # 5. Consistency in share count - Munger prefers stable/decreasing shares
    share_counts = [item.outstanding_shares for item in financial_line_items
                   if hasattr(item, 'outstanding_shares') and item.outstanding_shares is not None]
    
    if share_counts and len(share_counts) >= 3:
        if share_counts[0] < share_counts[-1] * 0.95:  # 5%+ reduction in shares
            score += 2
            details.append("Shareholder-friendly: Reducing share count over time")
        elif share_counts[0] < share_counts[-1] * 1.05:  # Stable share count
            score += 1
            details.append("Stable share count: Limited dilution")
        elif share_counts[0] > share_counts[-1] * 1.2:  # >20% dilution
            score -= 1  # Penalty for excessive dilution
            details.append("Concerning dilution: Share count increased significantly")
        else:
            details.append("Moderate share count increase over time")
    else:
        details.append("Insufficient share count data")
    

    # FCF / NI ratios -> already computed for scoring
    insider_buy_ratio = None
    recent_de_ratio = None
    cash_to_revenue = None
    share_count_trend = "unknown"

    # Debt ratio (D/E) -> we compute `recent_de_ratio`
    if debt_values and equity_values and len(debt_values) == len(equity_values):
        recent_de_ratio = debt_values[0] / equity_values[0] if equity_values[0] > 0 else float("inf")

    # Cash/Revenue -> we compute `cash_to_revenue`
    if cash_values and revenue_values and revenue_values[0] and revenue_values[0] > 0:
        cash_to_revenue = cash_values[0] / revenue_values[0]

    # Insider ratio -> we compute `insider_buy_ratio`
    if insider_trades and len(insider_trades) > 0:
        buys = sum(1 for t in insider_trades
                   if getattr(t, "transaction_type", None)
                   and t.transaction_type.lower() in ["buy", "purchase"])
        sells = sum(1 for t in insider_trades
                    if getattr(t, "transaction_type", None)
                    and t.transaction_type.lower() in ["sell", "sale"])
        total = buys + sells
        insider_buy_ratio = (buys / total) if total > 0 else None

    # Share count trend (decreasing / stable / increasing)
    share_counts = [item.outstanding_shares for item in financial_line_items
                    if hasattr(item, "outstanding_shares") and item.outstanding_shares is not None]
    if share_counts and len(share_counts) >= 3:
        if share_counts[0] < share_counts[-1] * 0.95:
            share_count_trend = "decreasing"
        elif share_counts[0] > share_counts[-1] * 1.05:
            share_count_trend = "increasing"
        else:
            share_count_trend = "stable"

    # Scale score to 0-10 range
    # Maximum possible raw score would be 12 (3+3+2+2+2)
    final_score = max(0, min(10, score * 10 / 12))
    
    return {
        "score": final_score,
        "details": "; ".join(details),
        "insider_buy_ratio": insider_buy_ratio,
        "recent_de_ratio": recent_de_ratio,
        "cash_to_revenue": cash_to_revenue,
        "share_count_trend": share_count_trend,
    }

def analyze_predictability(financial_line_items: list) -> dict:
    """
    Assess the predictability of the business - Munger strongly prefers businesses
    whose future operations and cashflows are relatively easy to predict.
    """
    score = 0
    details = []
    
    if not financial_line_items or len(financial_line_items) < 5:
        return {
            "score": 0,
            "details": "Insufficient data to analyze business predictability (need 5+ years)"
        }
    
    # 1. Revenue stability and growth
    revenues = [item.revenue for item in financial_line_items 
               if hasattr(item, 'revenue') and item.revenue is not None]
    
    if revenues and len(revenues) >= 5:
        # Calculate year-over-year growth rates, handling zero division
        growth_rates = []
        for i in range(len(revenues)-1):
            if revenues[i+1] != 0:  # Avoid division by zero
                growth_rate = (revenues[i] / revenues[i+1] - 1)
                growth_rates.append(growth_rate)
        
        if not growth_rates:
            details.append("Cannot calculate revenue growth: zero revenue values found")
        else:
            avg_growth = sum(growth_rates) / len(growth_rates)
            growth_volatility = sum(abs(r - avg_growth) for r in growth_rates) / len(growth_rates)
            
            if avg_growth > 0.05 and growth_volatility < 0.1:
                # Steady, consistent growth (Munger loves this)
                score += 3
                details.append(f"Highly predictable revenue: {avg_growth:.1%} avg growth with low volatility")
            elif avg_growth > 0 and growth_volatility < 0.2:
                # Positive but somewhat volatile growth
                score += 2
                details.append(f"Moderately predictable revenue: {avg_growth:.1%} avg growth with some volatility")
            elif avg_growth > 0:
                # Growing but unpredictable
                score += 1
                details.append(f"Growing but less predictable revenue: {avg_growth:.1%} avg growth with high volatility")
            else:
                details.append(f"Declining or highly unpredictable revenue: {avg_growth:.1%} avg growth")
    else:
        details.append("Insufficient revenue history for predictability analysis")
    
    # 2. Operating income stability
    op_income = [item.operating_income for item in financial_line_items 
                if hasattr(item, 'operating_income') and item.operating_income is not None]
    
    if op_income and len(op_income) >= 5:
        # Count positive operating income periods
        positive_periods = sum(1 for income in op_income if income > 0)
        
        if positive_periods == len(op_income):
            # Consistently profitable operations
            score += 3
            details.append("Highly predictable operations: Operating income positive in all periods")
        elif positive_periods >= len(op_income) * 0.8:
            # Mostly profitable operations
            score += 2
            details.append(f"Predictable operations: Operating income positive in {positive_periods}/{len(op_income)} periods")
        elif positive_periods >= len(op_income) * 0.6:
            # Somewhat profitable operations
            score += 1
            details.append(f"Somewhat predictable operations: Operating income positive in {positive_periods}/{len(op_income)} periods")
        else:
            details.append(f"Unpredictable operations: Operating income positive in only {positive_periods}/{len(op_income)} periods")
    else:
        details.append("Insufficient operating income history")
    
    # 3. Margin consistency - Munger values stable margins
    op_margins = [item.operating_margin for item in financial_line_items 
                 if hasattr(item, 'operating_margin') and item.operating_margin is not None]
    
    if op_margins and len(op_margins) >= 5:
        # Calculate margin volatility
        avg_margin = sum(op_margins) / len(op_margins)
        margin_volatility = sum(abs(m - avg_margin) for m in op_margins) / len(op_margins)
        
        if margin_volatility < 0.03:  # Very stable margins
            score += 2
            details.append(f"Highly predictable margins: {avg_margin:.1%} avg with minimal volatility")
        elif margin_volatility < 0.07:  # Moderately stable margins
            score += 1
            details.append(f"Moderately predictable margins: {avg_margin:.1%} avg with some volatility")
        else:
            details.append(f"Unpredictable margins: {avg_margin:.1%} avg with high volatility ({margin_volatility:.1%})")
    else:
        details.append("Insufficient margin history")
    
    # 4. Cash generation reliability
    fcf_values = [item.free_cash_flow for item in financial_line_items 
                 if hasattr(item, 'free_cash_flow') and item.free_cash_flow is not None]
    
    if fcf_values and len(fcf_values) >= 5:
        # Count positive FCF periods
        positive_fcf_periods = sum(1 for fcf in fcf_values if fcf > 0)
        
        if positive_fcf_periods == len(fcf_values):
            # Consistently positive FCF
            score += 2
            details.append("Highly predictable cash generation: Positive FCF in all periods")
        elif positive_fcf_periods >= len(fcf_values) * 0.8:
            # Mostly positive FCF
            score += 1
            details.append(f"Predictable cash generation: Positive FCF in {positive_fcf_periods}/{len(fcf_values)} periods")
        else:
            details.append(f"Unpredictable cash generation: Positive FCF in only {positive_fcf_periods}/{len(fcf_values)} periods")
    else:
        details.append("Insufficient free cash flow history")
    
    # Scale score to 0-10 range
    # Maximum possible raw score would be 10 (3+3+2+2)
    final_score = min(10, score * 10 / 10)
    
    return {
        "score": final_score,
        "details": "; ".join(details)
    }

def calculate_munger_valuation(financial_line_items: list, market_cap: float) -> dict:
    """
    Calculate intrinsic value using Munger's approach:
    - Focus on owner earnings (approximated by FCF)
    - Simple multiple on normalized earnings
    - Prefer paying a fair price for a wonderful business
    """
    score = 0
    details = []
    
    if not financial_line_items or market_cap is None:
        return {
            "score": 0,
            "details": "Insufficient data to perform valuation"
        }
    
    # Get FCF values (Munger's preferred "owner earnings" metric)
    fcf_values = [item.free_cash_flow for item in financial_line_items 
                 if hasattr(item, 'free_cash_flow') and item.free_cash_flow is not None]
    
    if not fcf_values or len(fcf_values) < 3:
        return {
            "score": 0,
            "details": "Insufficient free cash flow data for valuation"
        }
    
    # 1. Normalize earnings by taking average of last 3-5 years
    # (Munger prefers to normalize earnings to avoid over/under-valuation based on cyclical factors)
    normalized_fcf = sum(fcf_values[:min(5, len(fcf_values))]) / min(5, len(fcf_values))
    
    if normalized_fcf <= 0:
        return {
            "score": 0,
            "details": f"Negative or zero normalized FCF ({normalized_fcf}), cannot value",
            "intrinsic_value": None
        }
    
    # 2. Calculate FCF yield (inverse of P/FCF multiple)
    if market_cap <= 0:
        return {
            "score": 0,
            "details": f"Invalid market cap ({market_cap}), cannot value"
        }
    
    fcf_yield = normalized_fcf / market_cap
    
    # 3. Apply Munger's FCF multiple based on business quality
    # Munger would pay higher multiples for wonderful businesses
    # Let's use a sliding scale where higher FCF yields are more attractive
    if fcf_yield > 0.08:  # >8% FCF yield (P/FCF < 12.5x)
        score += 4
        details.append(f"Excellent value: {fcf_yield:.1%} FCF yield")
    elif fcf_yield > 0.05:  # >5% FCF yield (P/FCF < 20x)
        score += 3
        details.append(f"Good value: {fcf_yield:.1%} FCF yield")
    elif fcf_yield > 0.03:  # >3% FCF yield (P/FCF < 33x)
        score += 1
        details.append(f"Fair value: {fcf_yield:.1%} FCF yield")
    else:
        details.append(f"Expensive: Only {fcf_yield:.1%} FCF yield")
    
    # 4. Calculate simple intrinsic value range
    # Munger tends to use straightforward valuations, avoiding complex DCF models
    conservative_value = normalized_fcf * 10  # 10x FCF = 10% yield
    reasonable_value = normalized_fcf * 15    # 15x FCF ≈ 6.7% yield
    optimistic_value = normalized_fcf * 20    # 20x FCF = 5% yield
    
    # 5. Calculate margins of safety
    margin_of_safety_vs_fair_value = (reasonable_value - market_cap) / market_cap
    
    if margin_of_safety_vs_fair_value > 0.3:  # >30% upside
        score += 3
        details.append(f"Large margin of safety: {margin_of_safety_vs_fair_value:.1%} upside to reasonable value")
    elif margin_of_safety_vs_fair_value > 0.1:  # >10% upside
        score += 2
        details.append(f"Moderate margin of safety: {margin_of_safety_vs_fair_value:.1%} upside to reasonable value")
    elif margin_of_safety_vs_fair_value > -0.1:  # Within 10% of reasonable value
        score += 1
        details.append(f"Fair price: Within 10% of reasonable value ({margin_of_safety_vs_fair_value:.1%})")
    else:
        details.append(f"Expensive: {-margin_of_safety_vs_fair_value:.1%} premium to reasonable value")
    
    # 6. Check earnings trajectory for additional context
    # Munger likes growing owner earnings
    if len(fcf_values) >= 3:
        recent_avg = sum(fcf_values[:3]) / 3
        older_avg = sum(fcf_values[-3:]) / 3 if len(fcf_values) >= 6 else fcf_values[-1]
        
        if recent_avg > older_avg * 1.2:  # >20% growth in FCF
            score += 3
            details.append("Growing FCF trend adds to intrinsic value")
        elif recent_avg > older_avg:
            score += 2
            details.append("Stable to growing FCF supports valuation")
        else:
            details.append("Declining FCF trend is concerning")

    # Scale score to 0-10 range
    # Maximum possible raw score would be 10 (4+3+3)
    final_score = min(10, score * 10 / 10) 
    
    return {
        "score": final_score,
        "details": "; ".join(details),
        "intrinsic_value_range": {
            "conservative": conservative_value,
            "reasonable": reasonable_value,
            "optimistic": optimistic_value
        },
        "fcf_yield": fcf_yield,
        "normalized_fcf": normalized_fcf,
        "margin_of_safety_vs_fair_value": margin_of_safety_vs_fair_value,

    }

def analyze_news_sentiment(news_items: list) -> str:
    """
    Simple qualitative analysis of recent news.
    Munger pays attention to significant news but doesn't overreact to short-term stories.
    """
    if not news_items or len(news_items) == 0:
        return "No news data available"
    
    # Just return a simple count for now - in a real implementation, this would use NLP
    return f"Qualitative review of {len(news_items)} recent news items would be needed"

def make_munger_facts_bundle(analysis: dict[str, any]) -> dict[str, any]:
    moat = analysis.get("moat_analysis") or {}
    mgmt = analysis.get("management_analysis") or {}
    pred = analysis.get("predictability_analysis") or {}
    val  = analysis.get("valuation_analysis") or {}
    ivr  = val.get("intrinsic_value_range") or {}

    moat_score = _r(moat.get("score"), 2) or 0
    mgmt_score = _r(mgmt.get("score"), 2) or 0
    pred_score = _r(pred.get("score"), 2) or 0
    val_score  = _r(val.get("score"), 2) or 0

    # Simple mental-model flags (booleans/ints = cheap tokens, strong guidance)
    flags = {
        "moat_strong": moat_score >= 7,
        "predictable": pred_score >= 7,
        "owner_aligned": (mgmt_score >= 7) or ((mgmt.get("insider_buy_ratio") or 0) >= 0.6),
        "low_leverage": (mgmt.get("recent_de_ratio") is not None and mgmt.get("recent_de_ratio") < 0.7),
        "sensible_cash": (mgmt.get("cash_to_revenue") is not None and 0.1 <= mgmt.get("cash_to_revenue") <= 0.25),
        "low_capex": None,  # inferred in moat score already; keep placeholder if you later expose a ratio
        "mos_positive": (val.get("mos_to_reasonable") or 0) > 0.0,
        "fcf_yield_ok": (val.get("fcf_yield") or 0) >= 0.05,
        "share_count_friendly": (mgmt.get("share_count_trend") == "decreasing"),
    }

    return {
        "pre_signal": analysis.get("signal"),
        "score": _r(analysis.get("score"), 2),
        "max_score": _r(analysis.get("max_score"), 2),
        "moat_score": moat_score,
        "mgmt_score": mgmt_score,
        "predictability_score": pred_score,
        "valuation_score": val_score,
        "fcf_yield": _r(val.get("fcf_yield"), 4),
        "normalized_fcf": _r(val.get("normalized_fcf"), 0),
        "reasonable_value": _r(ivr.get("reasonable"), 0),
        "margin_of_safety_vs_fair_value": _r(val.get("margin_of_safety_vs_fair_value"), 3),
        "insider_buy_ratio": _r(mgmt.get("insider_buy_ratio"), 2),
        "recent_de_ratio": _r(mgmt.get("recent_de_ratio"), 2),
        "cash_to_revenue": _r(mgmt.get("cash_to_revenue"), 2),
        "share_count_trend": mgmt.get("share_count_trend"),
        "flags": flags,
        # keep one-liners, very short
        "notes": {
            "moat": (moat.get("details") or "")[:120],
            "mgmt": (mgmt.get("details") or "")[:120],
            "predictability": (pred.get("details") or "")[:120],
            "valuation": (val.get("details") or "")[:120],
        },
    }

def compute_confidence(analysis: dict, signal: str) -> int:
    # Pull component scores (0..10 each in your pipeline)
    moat = float((analysis.get("moat_analysis") or {}).get("score") or 0)
    mgmt = float((analysis.get("management_analysis") or {}).get("score") or 0)
    pred = float((analysis.get("predictability_analysis") or {}).get("score") or 0)
    val  = float((analysis.get("valuation_analysis") or {}).get("score") or 0)

    # Quality dominates (Munger): 0.35*moat + 0.25*mgmt + 0.25*pred (max 8.5)
    quality = 0.35 * moat + 0.25 * mgmt + 0.25 * pred  # 0..8.5
    quality_pct = 100 * (quality / 8.5) if quality > 0 else 0  # 0..100

    # Valuation bump from MOS vs “reasonable”
    mos = (analysis.get("valuation_analysis") or {}).get("margin_of_safety_vs_fair_value")
    mos = float(mos) if mos is not None else 0.0
    # Convert MOS into a bounded +/-10pp adjustment
    val_adj = max(-10.0, min(10.0, mos * 100.0 / 3.0))  # ~+/-10pp if MOS is around +/-30%

    # Base confidence: weighted toward quality, then small valuation adjustment
    base = 0.85 * quality_pct + 0.15 * (val * 10)  # val score 0..10 -> 0..100
    base = base + val_adj

    # Ensure bucket semantics by clamping into Munger buckets depending on signal
    if signal == "bullish":
        # If overvalued (mos<0), cap to mixed bucket
        upper = 100 if mos > 0 else 69
        lower = 50 if quality_pct >= 55 else 30
    elif signal == "bearish":
        # If clearly overvalued (mos< -0.05), allow very low bucket
        lower = 10 if mos < -0.05 else 30
        upper = 49
    else:  # neutral
        lower, upper = 50, 69

    conf = int(round(max(lower, min(upper, base))))
    # Keep inside global 10..100
    return max(10, min(100, conf))


# ==========================
# Ben Graham helpers
# ==========================

def analyze_earnings_stability(metrics: list, financial_line_items: list) -> dict:
    """
    Graham wants at least several years of consistently positive earnings (ideally 5+).
    We'll check:
    1. Number of years with positive EPS.
    2. Growth in EPS from first to last period.
    """
    score = 0
    details = []

    if not metrics or not financial_line_items:
        return {"score": score, "details": "Insufficient data for earnings stability analysis"}

    eps_vals = []
    for item in financial_line_items:
        if item.earnings_per_share is not None:
            eps_vals.append(item.earnings_per_share)

    if len(eps_vals) < 2:
        details.append("Not enough multi-year EPS data.")
        return {"score": score, "details": "; ".join(details)}

    # 1. Consistently positive EPS
    positive_eps_years = sum(1 for e in eps_vals if e > 0)
    total_eps_years = len(eps_vals)
    if positive_eps_years == total_eps_years:
        score += 3
        details.append("EPS was positive in all available periods.")
    elif positive_eps_years >= (total_eps_years * 0.8):
        score += 2
        details.append("EPS was positive in most periods.")
    else:
        details.append("EPS was negative in multiple periods.")

    # 2. EPS growth from earliest to latest
    if eps_vals[0] > eps_vals[-1]:
        score += 1
        details.append("EPS grew from earliest to latest period.")
    else:
        details.append("EPS did not grow from earliest to latest period.")

    return {"score": score, "details": "; ".join(details)}

def analyze_financial_strength(financial_line_items: list) -> dict:
    """
    Graham checks liquidity (current ratio >= 2), manageable debt,
    and dividend record (preferably some history of dividends).
    """
    score = 0
    details = []

    if not financial_line_items:
        return {"score": score, "details": "No data for financial strength analysis"}

    latest_item = financial_line_items[0]
    total_assets = latest_item.total_assets or 0
    total_liabilities = latest_item.total_liabilities or 0
    current_assets = latest_item.current_assets or 0
    current_liabilities = latest_item.current_liabilities or 0

    # 1. Current ratio
    if current_liabilities > 0:
        current_ratio = current_assets / current_liabilities
        if current_ratio >= 2.0:
            score += 2
            details.append(f"Current ratio = {current_ratio:.2f} (>=2.0: solid).")
        elif current_ratio >= 1.5:
            score += 1
            details.append(f"Current ratio = {current_ratio:.2f} (moderately strong).")
        else:
            details.append(f"Current ratio = {current_ratio:.2f} (<1.5: weaker liquidity).")
    else:
        details.append("Cannot compute current ratio (missing or zero current_liabilities).")

    # 2. Debt vs. Assets
    if total_assets > 0:
        debt_ratio = total_liabilities / total_assets
        if debt_ratio < 0.5:
            score += 2
            details.append(f"Debt ratio = {debt_ratio:.2f}, under 0.50 (conservative).")
        elif debt_ratio < 0.8:
            score += 1
            details.append(f"Debt ratio = {debt_ratio:.2f}, somewhat high but could be acceptable.")
        else:
            details.append(f"Debt ratio = {debt_ratio:.2f}, quite high by Graham standards.")
    else:
        details.append("Cannot compute debt ratio (missing total_assets).")

    # 3. Dividend track record
    div_periods = [item.dividends_and_other_cash_distributions for item in financial_line_items if item.dividends_and_other_cash_distributions is not None]
    if div_periods:
        # In many data feeds, dividend outflow is shown as a negative number
        # (money going out to shareholders). We'll consider any negative as 'paid a dividend'.
        div_paid_years = sum(1 for d in div_periods if d < 0)
        if div_paid_years > 0:
            # e.g. if at least half the periods had dividends
            if div_paid_years >= (len(div_periods) // 2 + 1):
                score += 1
                details.append("Company paid dividends in the majority of the reported years.")
            else:
                details.append("Company has some dividend payments, but not most years.")
        else:
            details.append("Company did not pay dividends in these periods.")
    else:
        details.append("No dividend data available to assess payout consistency.")

    return {"score": score, "details": "; ".join(details)}

def analyze_valuation_graham(financial_line_items: list, market_cap: float) -> dict:
    """
    Core Graham approach to valuation:
    1. Net-Net Check: (Current Assets - Total Liabilities) vs. Market Cap
    2. Graham Number: sqrt(22.5 * EPS * Book Value per Share)
    3. Compare per-share price to Graham Number => margin of safety
    """
    if not financial_line_items or not market_cap or market_cap <= 0:
        return {"score": 0, "details": "Insufficient data to perform valuation"}

    latest = financial_line_items[0]
    current_assets = latest.current_assets or 0
    total_liabilities = latest.total_liabilities or 0
    book_value_ps = latest.book_value_per_share or 0
    eps = latest.earnings_per_share or 0
    shares_outstanding = latest.outstanding_shares or 0

    details = []
    score = 0

    # 1. Net-Net Check
    #   NCAV = Current Assets - Total Liabilities
    #   If NCAV > Market Cap => historically a strong buy signal
    net_current_asset_value = current_assets - total_liabilities
    if net_current_asset_value > 0 and shares_outstanding > 0:
        net_current_asset_value_per_share = net_current_asset_value / shares_outstanding
        price_per_share = market_cap / shares_outstanding if shares_outstanding else 0

        details.append(f"Net Current Asset Value = {net_current_asset_value:,.2f}")
        details.append(f"NCAV Per Share = {net_current_asset_value_per_share:,.2f}")
        details.append(f"Price Per Share = {price_per_share:,.2f}")

        if net_current_asset_value > market_cap:
            score += 4  # Very strong Graham signal
            details.append("Net-Net: NCAV > Market Cap (classic Graham deep value).")
        else:
            # For partial net-net discount
            if net_current_asset_value_per_share >= (price_per_share * 0.67):
                score += 2
                details.append("NCAV Per Share >= 2/3 of Price Per Share (moderate net-net discount).")
    else:
        details.append("NCAV not exceeding market cap or insufficient data for net-net approach.")

    # 2. Graham Number
    #   GrahamNumber = sqrt(22.5 * EPS * BVPS).
    #   Compare the result to the current price_per_share
    #   If GrahamNumber >> price, indicates undervaluation
    graham_number = None
    if eps > 0 and book_value_ps > 0:
        graham_number = math.sqrt(22.5 * eps * book_value_ps)
        details.append(f"Graham Number = {graham_number:.2f}")
    else:
        details.append("Unable to compute Graham Number (EPS or Book Value missing/<=0).")

    # 3. Margin of Safety relative to Graham Number
    if graham_number and shares_outstanding > 0:
        current_price = market_cap / shares_outstanding
        if current_price > 0:
            margin_of_safety = (graham_number - current_price) / current_price
            details.append(f"Margin of Safety (Graham Number) = {margin_of_safety:.2%}")
            if margin_of_safety > 0.5:
                score += 3
                details.append("Price is well below Graham Number (>=50% margin).")
            elif margin_of_safety > 0.2:
                score += 1
                details.append("Some margin of safety relative to Graham Number.")
            else:
                details.append("Price close to or above Graham Number, low margin of safety.")
        else:
            details.append("Current price is zero or invalid; can't compute margin of safety.")
    # else: already appended details for missing graham_number

    return {"score": score, "details": "; ".join(details)}


# ==========================
# Bill Ackman helpers
# ==========================

def analyze_business_quality(metrics: list, financial_line_items: list) -> dict:
    """
    Analyze whether the company has a high-quality business with stable or growing cash flows,
    durable competitive advantages (moats), and potential for long-term growth.
    Also tries to infer brand strength if intangible_assets data is present (optional).
    """
    score = 0
    details = []
    
    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze business quality"
        }
    
    # 1. Multi-period revenue growth analysis
    revenues = [item.revenue for item in financial_line_items if item.revenue is not None]
    if len(revenues) >= 2:
        initial, final = revenues[-1], revenues[0]
        if initial and final and final > initial:
            growth_rate = (final - initial) / abs(initial)
            if growth_rate > 0.5:  # e.g., 50% cumulative growth
                score += 2
                details.append(f"Revenue grew by {(growth_rate*100):.1f}% over the full period (strong growth).")
            else:
                score += 1
                details.append(f"Revenue growth is positive but under 50% cumulatively ({(growth_rate*100):.1f}%).")
        else:
            details.append("Revenue did not grow significantly or data insufficient.")
    else:
        details.append("Not enough revenue data for multi-period trend.")
    
    # 2. Operating margin and free cash flow consistency
    fcf_vals = [item.free_cash_flow for item in financial_line_items if item.free_cash_flow is not None]
    op_margin_vals = [item.operating_margin for item in financial_line_items if item.operating_margin is not None]
    
    if op_margin_vals:
        above_15 = sum(1 for m in op_margin_vals if m > 0.15)
        if above_15 >= (len(op_margin_vals) // 2 + 1):
            score += 2
            details.append("Operating margins have often exceeded 15% (indicates good profitability).")
        else:
            details.append("Operating margin not consistently above 15%.")
    else:
        details.append("No operating margin data across periods.")
    
    if fcf_vals:
        positive_fcf_count = sum(1 for f in fcf_vals if f > 0)
        if positive_fcf_count >= (len(fcf_vals) // 2 + 1):
            score += 1
            details.append("Majority of periods show positive free cash flow.")
        else:
            details.append("Free cash flow not consistently positive.")
    else:
        details.append("No free cash flow data across periods.")
    
    # 3. Return on Equity (ROE) check from the latest metrics
    latest_metrics = metrics[0]
    if latest_metrics.return_on_equity and latest_metrics.return_on_equity > 0.15:
        score += 2
        details.append(f"High ROE of {latest_metrics.return_on_equity:.1%}, indicating a competitive advantage.")
    elif latest_metrics.return_on_equity:
        details.append(f"ROE of {latest_metrics.return_on_equity:.1%} is moderate.")
    else:
        details.append("ROE data not available.")
    
    # 4. (Optional) Brand Intangible (if intangible_assets are fetched)
    # intangible_vals = [item.intangible_assets for item in financial_line_items if item.intangible_assets]
    # if intangible_vals and sum(intangible_vals) > 0:
    #     details.append("Significant intangible assets may indicate brand value or proprietary tech.")
    #     score += 1
    
    return {
        "score": score,
        "details": "; ".join(details)
    }

def analyze_financial_discipline(metrics: list, financial_line_items: list) -> dict:
    """
    Evaluate the company's balance sheet over multiple periods:
    - Debt ratio trends
    - Capital returns to shareholders over time (dividends, buybacks)
    """
    score = 0
    details = []
    
    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze financial discipline"
        }
    
    # 1. Multi-period debt ratio or debt_to_equity
    debt_to_equity_vals = [item.debt_to_equity for item in financial_line_items if item.debt_to_equity is not None]
    if debt_to_equity_vals:
        below_one_count = sum(1 for d in debt_to_equity_vals if d < 1.0)
        if below_one_count >= (len(debt_to_equity_vals) // 2 + 1):
            score += 2
            details.append("Debt-to-equity < 1.0 for the majority of periods (reasonable leverage).")
        else:
            details.append("Debt-to-equity >= 1.0 in many periods (could be high leverage).")
    else:
        # Fallback to total_liabilities / total_assets
        liab_to_assets = []
        for item in financial_line_items:
            if item.total_liabilities and item.total_assets and item.total_assets > 0:
                liab_to_assets.append(item.total_liabilities / item.total_assets)
        
        if liab_to_assets:
            below_50pct_count = sum(1 for ratio in liab_to_assets if ratio < 0.5)
            if below_50pct_count >= (len(liab_to_assets) // 2 + 1):
                score += 2
                details.append("Liabilities-to-assets < 50% for majority of periods.")
            else:
                details.append("Liabilities-to-assets >= 50% in many periods.")
        else:
            details.append("No consistent leverage ratio data available.")
    
    # 2. Capital allocation approach (dividends + share counts)
    dividends_list = [
        item.dividends_and_other_cash_distributions
        for item in financial_line_items
        if item.dividends_and_other_cash_distributions is not None
    ]
    if dividends_list:
        paying_dividends_count = sum(1 for d in dividends_list if d < 0)
        if paying_dividends_count >= (len(dividends_list) // 2 + 1):
            score += 1
            details.append("Company has a history of returning capital to shareholders (dividends).")
        else:
            details.append("Dividends not consistently paid or no data on distributions.")
    else:
        details.append("No dividend data found across periods.")
    
    # Check for decreasing share count (simple approach)
    shares = [item.outstanding_shares for item in financial_line_items if item.outstanding_shares is not None]
    if len(shares) >= 2:
        # For buybacks, the newest count should be less than the oldest count
        if shares[0] < shares[-1]:
            score += 1
            details.append("Outstanding shares have decreased over time (possible buybacks).")
        else:
            details.append("Outstanding shares have not decreased over the available periods.")
    else:
        details.append("No multi-period share count data to assess buybacks.")
    
    return {
        "score": score,
        "details": "; ".join(details)
    }

def analyze_activism_potential(financial_line_items: list) -> dict:
    """
    Bill Ackman often engages in activism if a company has a decent brand or moat
    but is underperforming operationally.
    
    We'll do a simplified approach:
    - Look for positive revenue trends but subpar margins
    - That may indicate 'activism upside' if operational improvements could unlock value.
    """
    if not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data for activism potential"
        }
    
    # Check revenue growth vs. operating margin
    revenues = [item.revenue for item in financial_line_items if item.revenue is not None]
    op_margins = [item.operating_margin for item in financial_line_items if item.operating_margin is not None]
    
    if len(revenues) < 2 or not op_margins:
        return {
            "score": 0,
            "details": "Not enough data to assess activism potential (need multi-year revenue + margins)."
        }
    
    initial, final = revenues[-1], revenues[0]
    revenue_growth = (final - initial) / abs(initial) if initial else 0
    avg_margin = sum(op_margins) / len(op_margins)
    
    score = 0
    details = []
    
    # Suppose if there's decent revenue growth but margins are below 10%, Ackman might see activism potential.
    if revenue_growth > 0.15 and avg_margin < 0.10:
        score += 2
        details.append(
            f"Revenue growth is healthy (~{revenue_growth*100:.1f}%), but margins are low (avg {avg_margin*100:.1f}%). "
            "Activism could unlock margin improvements."
        )
    else:
        details.append("No clear sign of activism opportunity (either margins are already decent or growth is weak).")
    
    return {"score": score, "details": "; ".join(details)}

def ba_analyze_valuation(financial_line_items: list, market_cap: float) -> dict:
    """
    Ackman invests in companies trading at a discount to intrinsic value.
    Uses a simplified DCF with FCF as a proxy, plus margin of safety analysis.
    """
    if not financial_line_items or market_cap is None:
        return {
            "score": 0,
            "details": "Insufficient data to perform valuation"
        }
    
    # Since financial_line_items are in descending order (newest first),
    # the most recent period is the first element
    latest = financial_line_items[0]
    fcf = latest.free_cash_flow if latest.free_cash_flow else 0
    
    if fcf <= 0:
        return {
            "score": 0,
            "details": f"No positive FCF for valuation; FCF = {fcf}",
            "intrinsic_value": None
        }
    
    # Basic DCF assumptions
    growth_rate = 0.06
    discount_rate = 0.10
    terminal_multiple = 15
    projection_years = 5
    
    present_value = 0
    for year in range(1, projection_years + 1):
        future_fcf = fcf * (1 + growth_rate) ** year
        pv = future_fcf / ((1 + discount_rate) ** year)
        present_value += pv
    
    # Terminal Value
    terminal_value = (
        fcf * (1 + growth_rate) ** projection_years * terminal_multiple
    ) / ((1 + discount_rate) ** projection_years)
    
    intrinsic_value = present_value + terminal_value
    margin_of_safety = (intrinsic_value - market_cap) / market_cap
    
    score = 0
    # Simple scoring
    if margin_of_safety > 0.3:
        score += 3
    elif margin_of_safety > 0.1:
        score += 1
    
    details = [
        f"Calculated intrinsic value: ~{intrinsic_value:,.2f}",
        f"Market cap: ~{market_cap:,.2f}",
        f"Margin of safety: {margin_of_safety:.2%}"
    ]
    
    return {
        "score": score,
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety
    }


# ==========================
# Cathie Wood helpers
# ==========================

def analyze_disruptive_potential(metrics: list, financial_line_items: list) -> dict:
    """
    Analyze whether the company has disruptive products, technology, or business model.
    Evaluates multiple dimensions of disruptive potential:
    1. Revenue Growth Acceleration - indicates market adoption
    2. R&D Intensity - shows innovation investment
    3. Gross Margin Trends - suggests pricing power and scalability
    4. Operating Leverage - demonstrates business model efficiency
    5. Market Share Dynamics - indicates competitive position
    """
    score = 0
    details = []

    if not metrics or not financial_line_items:
        return {"score": 0, "details": "Insufficient data to analyze disruptive potential"}

    # 1. Revenue Growth Analysis - Check for accelerating growth
    revenues = [item.revenue for item in financial_line_items if item.revenue]
    if len(revenues) >= 3:  # Need at least 3 periods to check acceleration
        growth_rates = []
        for i in range(len(revenues) - 1):
            if revenues[i] and revenues[i + 1]:
                growth_rate = (revenues[i] - revenues[i + 1]) / abs(revenues[i + 1]) if revenues[i + 1] != 0 else 0
                growth_rates.append(growth_rate)

        # Check if growth is accelerating (first growth rate higher than last, since they're in reverse order)
        if len(growth_rates) >= 2 and growth_rates[0] > growth_rates[-1]:
            score += 2
            details.append(f"Revenue growth is accelerating: {(growth_rates[0]*100):.1f}% vs {(growth_rates[-1]*100):.1f}%")

        # Check absolute growth rate (most recent growth rate is at index 0)
        latest_growth = growth_rates[0] if growth_rates else 0
        if latest_growth > 1.0:
            score += 3
            details.append(f"Exceptional revenue growth: {(latest_growth*100):.1f}%")
        elif latest_growth > 0.5:
            score += 2
            details.append(f"Strong revenue growth: {(latest_growth*100):.1f}%")
        elif latest_growth > 0.2:
            score += 1
            details.append(f"Moderate revenue growth: {(latest_growth*100):.1f}%")
    else:
        details.append("Insufficient revenue data for growth analysis")

    # 2. Gross Margin Analysis - Check for expanding margins
    gross_margins = [item.gross_margin for item in financial_line_items if hasattr(item, "gross_margin") and item.gross_margin is not None]
    if len(gross_margins) >= 2:
        margin_trend = gross_margins[0] - gross_margins[-1]
        if margin_trend > 0.05:  # 5% improvement
            score += 2
            details.append(f"Expanding gross margins: +{(margin_trend*100):.1f}%")
        elif margin_trend > 0:
            score += 1
            details.append(f"Slightly improving gross margins: +{(margin_trend*100):.1f}%")

        # Check absolute margin level (most recent margin is at index 0)
        if gross_margins[0] > 0.50:  # High margin business
            score += 2
            details.append(f"High gross margin: {(gross_margins[0]*100):.1f}%")
    else:
        details.append("Insufficient gross margin data")

    # 3. Operating Leverage Analysis
    revenues = [item.revenue for item in financial_line_items if item.revenue]
    operating_expenses = [item.operating_expense for item in financial_line_items if hasattr(item, "operating_expense") and item.operating_expense]

    if len(revenues) >= 2 and len(operating_expenses) >= 2:
        rev_growth = (revenues[0] - revenues[-1]) / abs(revenues[-1])
        opex_growth = (operating_expenses[0] - operating_expenses[-1]) / abs(operating_expenses[-1])

        if rev_growth > opex_growth:
            score += 2
            details.append("Positive operating leverage: Revenue growing faster than expenses")
    else:
        details.append("Insufficient data for operating leverage analysis")

    # 4. R&D Investment Analysis
    rd_expenses = [item.research_and_development for item in financial_line_items if hasattr(item, "research_and_development") and item.research_and_development is not None]
    if rd_expenses and revenues:
        rd_intensity = rd_expenses[0] / revenues[0]
        if rd_intensity > 0.15:  # High R&D intensity
            score += 3
            details.append(f"High R&D investment: {(rd_intensity*100):.1f}% of revenue")
        elif rd_intensity > 0.08:
            score += 2
            details.append(f"Moderate R&D investment: {(rd_intensity*100):.1f}% of revenue")
        elif rd_intensity > 0.05:
            score += 1
            details.append(f"Some R&D investment: {(rd_intensity*100):.1f}% of revenue")
    else:
        details.append("No R&D data available")

    # Normalize score to be out of 5
    max_possible_score = 12  # Sum of all possible points
    normalized_score = (score / max_possible_score) * 5

    return {"score": normalized_score, "details": "; ".join(details), "raw_score": score, "max_score": max_possible_score}

def analyze_innovation_growth(metrics: list, financial_line_items: list) -> dict:
    """
    Evaluate the company's commitment to innovation and potential for exponential growth.
    Analyzes multiple dimensions:
    1. R&D Investment Trends - measures commitment to innovation
    2. Free Cash Flow Generation - indicates ability to fund innovation
    3. Operating Efficiency - shows scalability of innovation
    4. Capital Allocation - reveals innovation-focused management
    5. Growth Reinvestment - demonstrates commitment to future growth
    """
    score = 0
    details = []

    if not metrics or not financial_line_items:
        return {"score": 0, "details": "Insufficient data to analyze innovation-driven growth"}

    # 1. R&D Investment Trends
    rd_expenses = [item.research_and_development for item in financial_line_items if hasattr(item, "research_and_development") and item.research_and_development]
    revenues = [item.revenue for item in financial_line_items if item.revenue]

    if rd_expenses and revenues and len(rd_expenses) >= 2:
        rd_growth = (rd_expenses[0] - rd_expenses[-1]) / abs(rd_expenses[-1]) if rd_expenses[-1] != 0 else 0
        if rd_growth > 0.5:  # 50% growth in R&D
            score += 3
            details.append(f"Strong R&D investment growth: +{(rd_growth*100):.1f}%")
        elif rd_growth > 0.2:
            score += 2
            details.append(f"Moderate R&D investment growth: +{(rd_growth*100):.1f}%")

        # Check R&D intensity trend (corrected for reverse chronological order)
        rd_intensity_start = rd_expenses[-1] / revenues[-1]
        rd_intensity_end = rd_expenses[0] / revenues[0]
        if rd_intensity_end > rd_intensity_start:
            score += 2
            details.append(f"Increasing R&D intensity: {(rd_intensity_end*100):.1f}% vs {(rd_intensity_start*100):.1f}%")
    else:
        details.append("Insufficient R&D data for trend analysis")

    # 2. Free Cash Flow Analysis
    fcf_vals = [item.free_cash_flow for item in financial_line_items if item.free_cash_flow]
    if fcf_vals and len(fcf_vals) >= 2:
        fcf_growth = (fcf_vals[0] - fcf_vals[-1]) / abs(fcf_vals[-1])
        positive_fcf_count = sum(1 for f in fcf_vals if f > 0)

        if fcf_growth > 0.3 and positive_fcf_count == len(fcf_vals):
            score += 3
            details.append("Strong and consistent FCF growth, excellent innovation funding capacity")
        elif positive_fcf_count >= len(fcf_vals) * 0.75:
            score += 2
            details.append("Consistent positive FCF, good innovation funding capacity")
        elif positive_fcf_count > len(fcf_vals) * 0.5:
            score += 1
            details.append("Moderately consistent FCF, adequate innovation funding capacity")
    else:
        details.append("Insufficient FCF data for analysis")

    # 3. Operating Efficiency Analysis
    op_margin_vals = [item.operating_margin for item in financial_line_items if item.operating_margin]
    if op_margin_vals and len(op_margin_vals) >= 2:
        margin_trend = op_margin_vals[0] - op_margin_vals[-1]

        if op_margin_vals[0] > 0.15 and margin_trend > 0:
            score += 3
            details.append(f"Strong and improving operating margin: {(op_margin_vals[0]*100):.1f}%")
        elif op_margin_vals[0] > 0.10:
            score += 2
            details.append(f"Healthy operating margin: {(op_margin_vals[0]*100):.1f}%")
        elif margin_trend > 0:
            score += 1
            details.append("Improving operating efficiency")
    else:
        details.append("Insufficient operating margin data")

    # 4. Capital Allocation Analysis
    capex = [item.capital_expenditure for item in financial_line_items if hasattr(item, "capital_expenditure") and item.capital_expenditure]
    if capex and revenues and len(capex) >= 2:
        capex_intensity = abs(capex[0]) / revenues[0]
        capex_growth = (abs(capex[0]) - abs(capex[-1])) / abs(capex[-1]) if capex[-1] != 0 else 0

        if capex_intensity > 0.10 and capex_growth > 0.2:
            score += 2
            details.append("Strong investment in growth infrastructure")
        elif capex_intensity > 0.05:
            score += 1
            details.append("Moderate investment in growth infrastructure")
    else:
        details.append("Insufficient CAPEX data")

    # 5. Growth Reinvestment Analysis
    dividends = [item.dividends_and_other_cash_distributions for item in financial_line_items if hasattr(item, "dividends_and_other_cash_distributions") and item.dividends_and_other_cash_distributions]
    if dividends and fcf_vals:
        latest_payout_ratio = dividends[0] / fcf_vals[0] if fcf_vals[0] != 0 else 1
        if latest_payout_ratio < 0.2:  # Low dividend payout ratio suggests reinvestment focus
            score += 2
            details.append("Strong focus on reinvestment over dividends")
        elif latest_payout_ratio < 0.4:
            score += 1
            details.append("Moderate focus on reinvestment over dividends")
    else:
        details.append("Insufficient dividend data")

    # Normalize score to be out of 5
    max_possible_score = 15  # Sum of all possible points
    normalized_score = (score / max_possible_score) * 5

    return {"score": normalized_score, "details": "; ".join(details), "raw_score": score, "max_score": max_possible_score}

def analyze_cathie_wood_valuation(financial_line_items: list, market_cap: float) -> dict:
    """
    Cathie Wood often focuses on long-term exponential growth potential. We can do
    a simplified approach looking for a large total addressable market (TAM) and the
    company's ability to capture a sizable portion.
    """
    if not financial_line_items or market_cap is None:
        return {"score": 0, "details": "Insufficient data for valuation"}

    latest = financial_line_items[0]
    fcf = latest.free_cash_flow if latest.free_cash_flow else 0

    if fcf <= 0:
        return {"score": 0, "details": f"No positive FCF for valuation; FCF = {fcf}", "intrinsic_value": None}

    # Instead of a standard DCF, let's assume a higher growth rate for an innovative company.
    # Example values:
    growth_rate = 0.20  # 20% annual growth
    discount_rate = 0.15
    terminal_multiple = 25
    projection_years = 5

    present_value = 0
    for year in range(1, projection_years + 1):
        future_fcf = fcf * (1 + growth_rate) ** year
        pv = future_fcf / ((1 + discount_rate) ** year)
        present_value += pv

    # Terminal Value
    terminal_value = (fcf * (1 + growth_rate) ** projection_years * terminal_multiple) / ((1 + discount_rate) ** projection_years)
    intrinsic_value = present_value + terminal_value

    margin_of_safety = (intrinsic_value - market_cap) / market_cap

    score = 0
    if margin_of_safety > 0.5:
        score += 3
    elif margin_of_safety > 0.2:
        score += 1

    details = [f"Calculated intrinsic value: ~{intrinsic_value:,.2f}", f"Market cap: ~{market_cap:,.2f}", f"Margin of safety: {margin_of_safety:.2%}"]

    return {"score": score, "details": "; ".join(details), "intrinsic_value": intrinsic_value, "margin_of_safety": margin_of_safety}


# ==========================
# Michael Burry helpers
# ==========================

def _analyze_value(metrics, line_items, market_cap):
    """Free cash‑flow yield, EV/EBIT, other classic deep‑value metrics."""

    max_score = 6  # 4 pts for FCF‑yield, 2 pts for EV/EBIT
    score = 0
    details: list[str] = []

    # Free‑cash‑flow yield
    latest_item = _latest_line_item(line_items)
    fcf = getattr(latest_item, "free_cash_flow", None) if latest_item else None
    if fcf is not None and market_cap:
        fcf_yield = fcf / market_cap
        if fcf_yield >= 0.15:
            score += 4
            details.append(f"Extraordinary FCF yield {fcf_yield:.1%}")
        elif fcf_yield >= 0.12:
            score += 3
            details.append(f"Very high FCF yield {fcf_yield:.1%}")
        elif fcf_yield >= 0.08:
            score += 2
            details.append(f"Respectable FCF yield {fcf_yield:.1%}")
        else:
            details.append(f"Low FCF yield {fcf_yield:.1%}")
    else:
        details.append("FCF data unavailable")

    # EV/EBIT (from financial metrics)
    if metrics:
        ev_ebit = getattr(metrics[0], "ev_to_ebit", None)
        if ev_ebit is not None:
            if ev_ebit < 6:
                score += 2
                details.append(f"EV/EBIT {ev_ebit:.1f} (<6)")
            elif ev_ebit < 10:
                score += 1
                details.append(f"EV/EBIT {ev_ebit:.1f} (<10)")
            else:
                details.append(f"High EV/EBIT {ev_ebit:.1f}")
        else:
            details.append("EV/EBIT data unavailable")
    else:
        details.append("Financial metrics unavailable")

    return {"score": score, "max_score": max_score, "details": "; ".join(details)}

def _analyze_balance_sheet(metrics, line_items):
    """Leverage and liquidity checks."""

    max_score = 3
    score = 0
    details: list[str] = []

    latest_metrics = metrics[0] if metrics else None
    latest_item = _latest_line_item(line_items)

    debt_to_equity = getattr(latest_metrics, "debt_to_equity", None) if latest_metrics else None
    if debt_to_equity is not None:
        if debt_to_equity < 0.5:
            score += 2
            details.append(f"Low D/E {debt_to_equity:.2f}")
        elif debt_to_equity < 1:
            score += 1
            details.append(f"Moderate D/E {debt_to_equity:.2f}")
        else:
            details.append(f"High leverage D/E {debt_to_equity:.2f}")
    else:
        details.append("Debt‑to‑equity data unavailable")

    # Quick liquidity sanity check (cash vs total debt)
    if latest_item is not None:
        cash = getattr(latest_item, "cash_and_equivalents", None)
        total_debt = getattr(latest_item, "total_debt", None)
        if cash is not None and total_debt is not None:
            if cash > total_debt:
                score += 1
                details.append("Net cash position")
            else:
                details.append("Net debt position")
        else:
            details.append("Cash/debt data unavailable")

    return {"score": score, "max_score": max_score, "details": "; ".join(details)}

def _analyze_insider_activity(insider_trades):
    """Net insider buying over the last 12 months acts as a hard catalyst."""

    max_score = 2
    score = 0
    details: list[str] = []

    if not insider_trades:
        details.append("No insider trade data")
        return {"score": score, "max_score": max_score, "details": "; ".join(details)}

    shares_bought = sum(t.transaction_shares or 0 for t in insider_trades if (t.transaction_shares or 0) > 0)
    shares_sold = abs(sum(t.transaction_shares or 0 for t in insider_trades if (t.transaction_shares or 0) < 0))
    net = shares_bought - shares_sold
    if net > 0:
        score += 2 if net / max(shares_sold, 1) > 1 else 1
        details.append(f"Net insider buying of {net:,} shares")
    else:
        details.append("Net insider selling")

    return {"score": score, "max_score": max_score, "details": "; ".join(details)}

def _analyze_contrarian_sentiment(news):
    """Very rough gauge: a wall of recent negative headlines can be a *positive* for a contrarian."""

    max_score = 1
    score = 0
    details: list[str] = []

    if not news:
        details.append("No recent news")
        return {"score": score, "max_score": max_score, "details": "; ".join(details)}

    # Count negative sentiment articles
    sentiment_negative_count = sum(
        1 for n in news if n.sentiment and n.sentiment.lower() in ["negative", "bearish"]
    )
    
    if sentiment_negative_count >= 5:
        score += 1  # The more hated, the better (assuming fundamentals hold up)
        details.append(f"{sentiment_negative_count} negative headlines (contrarian opportunity)")
    else:
        details.append("Limited negative press")

    return {"score": score, "max_score": max_score, "details": "; ".join(details)}


# ==========================
# Nassim Taleb helpers
# ==========================

def safe_float(value, default=0.0):
    """Safely convert a value to float, handling NaN cases."""
    try:
        if pd.isna(value) or np.isnan(value):
            return default
        return float(value)
    except (ValueError, TypeError, OverflowError):
        return default

def analyze_tail_risk(prices_df: pd.DataFrame) -> dict[str, any]:
    """Assess fat tails, skewness, tail ratio, and max drawdown."""
    if prices_df.empty or len(prices_df) < 20:
        return {"score": 0, "max_score": 8, "details": "Insufficient price data for tail risk analysis"}

    score = 0
    reasoning = []

    returns = prices_df["close"].pct_change().dropna()

    # Excess kurtosis (use rolling 63-day if enough data, else full series)
    if len(returns) >= 63:
        kurt = safe_float(returns.rolling(63).kurt().iloc[-1])
    else:
        kurt = safe_float(returns.kurt())

    if kurt > 5:
        score += 2
        reasoning.append(f"Extremely fat tails (kurtosis {kurt:.1f})")
    elif kurt > 2:
        score += 1
        reasoning.append(f"Moderate fat tails (kurtosis {kurt:.1f})")
    else:
        reasoning.append(f"Near-Gaussian tails (kurtosis {kurt:.1f}) — suspiciously thin")

    # Skewness
    if len(returns) >= 63:
        skew = safe_float(returns.rolling(63).skew().iloc[-1])
    else:
        skew = safe_float(returns.skew())

    if skew > 0.5:
        score += 2
        reasoning.append(f"Positive skew ({skew:.2f}) favors long convexity")
    elif skew > -0.5:
        score += 1
        reasoning.append(f"Symmetric distribution (skew {skew:.2f})")
    else:
        reasoning.append(f"Negative skew ({skew:.2f}) — crash-prone")

    # Tail ratio (95th percentile gains / abs(5th percentile losses))
    positive_returns = returns[returns > 0]
    negative_returns = returns[returns < 0]

    if len(positive_returns) > 20 and len(negative_returns) > 20:
        right_tail = np.percentile(positive_returns, 95)
        left_tail = abs(np.percentile(negative_returns, 5))
        tail_ratio = right_tail / left_tail if left_tail > 0 else 1.0

        if tail_ratio > 1.2:
            score += 2
            reasoning.append(f"Asymmetric upside (tail ratio {tail_ratio:.2f})")
        elif tail_ratio > 0.8:
            score += 1
            reasoning.append(f"Balanced tails (tail ratio {tail_ratio:.2f})")
        else:
            reasoning.append(f"Asymmetric downside (tail ratio {tail_ratio:.2f})")
    else:
        reasoning.append("Insufficient data for tail ratio")

    # Max drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_dd = safe_float(drawdown.min())

    if max_dd > -0.15:
        score += 2
        reasoning.append(f"Resilient (max drawdown {max_dd:.1%})")
    elif max_dd > -0.30:
        score += 1
        reasoning.append(f"Moderate drawdown ({max_dd:.1%})")
    else:
        reasoning.append(f"Severe drawdown ({max_dd:.1%}) — fragile")

    return {"score": score, "max_score": 8, "details": "; ".join(reasoning)}

def analyze_antifragility(metrics: list, line_items: list, market_cap: float | None) -> dict[str, any]:
    """Evaluate whether the company benefits from disorder: low debt, high cash, stable margins."""
    if not metrics and not line_items:
        return {"score": 0, "max_score": 10, "details": "Insufficient data for antifragility analysis"}

    score = 0
    reasoning = []
    latest_metrics = metrics[0] if metrics else None
    latest_item = line_items[0] if line_items else None

    # Net cash position
    cash = getattr(latest_item, "cash_and_equivalents", None) if latest_item else None
    total_debt = getattr(latest_item, "total_debt", None) if latest_item else None
    total_assets = getattr(latest_item, "total_assets", None) if latest_item else None

    if cash is not None and total_debt is not None:
        net_cash = cash - total_debt
        if net_cash > 0 and market_cap and cash > 0.20 * market_cap:
            score += 3
            reasoning.append(f"War chest: net cash ${net_cash:,.0f}, cash is {cash / market_cap:.0%} of market cap")
        elif net_cash > 0:
            score += 2
            reasoning.append(f"Net cash positive (${net_cash:,.0f})")
        elif total_assets and total_debt < 0.30 * total_assets:
            score += 1
            reasoning.append("Net debt but manageable relative to assets")
        else:
            reasoning.append("Leveraged position — not antifragile")
    else:
        reasoning.append("Cash/debt data not available")

    # Debt-to-equity
    debt_to_equity = getattr(latest_metrics, "debt_to_equity", None) if latest_metrics else None
    if debt_to_equity is not None:
        if debt_to_equity < 0.3:
            score += 2
            reasoning.append(f"Taleb-approved low leverage (D/E {debt_to_equity:.2f})")
        elif debt_to_equity < 0.7:
            score += 1
            reasoning.append(f"Moderate leverage (D/E {debt_to_equity:.2f})")
        else:
            reasoning.append(f"High leverage (D/E {debt_to_equity:.2f}) — fragile")
    else:
        reasoning.append("Debt-to-equity data not available")

    # Operating margin stability (CV across periods)
    op_margins = [m.operating_margin for m in metrics if m.operating_margin is not None]
    if len(op_margins) >= 3:
        mean_margin = sum(op_margins) / len(op_margins)
        variance = sum((m - mean_margin) ** 2 for m in op_margins) / len(op_margins)
        std_margin = variance ** 0.5
        cv = std_margin / abs(mean_margin) if mean_margin != 0 else float("inf")

        if cv < 0.15 and mean_margin > 0.15:
            score += 3
            reasoning.append(f"Stable high margins (avg {mean_margin:.1%}, CV {cv:.2f}) — antifragile pricing power")
        elif cv < 0.30 and mean_margin > 0.10:
            score += 2
            reasoning.append(f"Reasonable margin stability (avg {mean_margin:.1%}, CV {cv:.2f})")
        elif cv < 0.30:
            score += 1
            reasoning.append(f"Margins somewhat stable (CV {cv:.2f}) but low (avg {mean_margin:.1%})")
        else:
            reasoning.append(f"Volatile margins (CV {cv:.2f}) — fragile pricing power")
    else:
        reasoning.append("Insufficient margin history for stability analysis")

    # FCF consistency
    fcf_values = [getattr(item, "free_cash_flow", None) for item in line_items] if line_items else []
    fcf_values = [v for v in fcf_values if v is not None]
    if fcf_values:
        positive_count = sum(1 for v in fcf_values if v > 0)
        if positive_count == len(fcf_values):
            score += 2
            reasoning.append(f"Consistent FCF generation ({positive_count}/{len(fcf_values)} periods positive)")
        elif positive_count > len(fcf_values) / 2:
            score += 1
            reasoning.append(f"Majority positive FCF ({positive_count}/{len(fcf_values)} periods)")
        else:
            reasoning.append(f"Inconsistent FCF ({positive_count}/{len(fcf_values)} periods positive)")
    else:
        reasoning.append("FCF data not available")

    return {"score": score, "max_score": 10, "details": "; ".join(reasoning)}

def analyze_convexity(
    metrics: list, line_items: list, prices_df: pd.DataFrame, market_cap: float | None
) -> dict[str, any]:
    """Measure asymmetric payoff potential: R&D optionality, upside/downside ratio, cash optionality."""
    if not metrics and not line_items and prices_df.empty:
        return {"score": 0, "max_score": 10, "details": "Insufficient data for convexity analysis"}

    score = 0
    reasoning = []
    latest_item = line_items[0] if line_items else None

    # R&D as embedded optionality
    rd = getattr(latest_item, "research_and_development", None) if latest_item else None
    revenue = getattr(latest_item, "revenue", None) if latest_item else None

    if rd is not None and revenue and revenue > 0:
        rd_ratio = abs(rd) / revenue
        if rd_ratio > 0.15:
            score += 3
            reasoning.append(f"Significant embedded optionality via R&D ({rd_ratio:.1%} of revenue)")
        elif rd_ratio > 0.08:
            score += 2
            reasoning.append(f"Meaningful R&D investment ({rd_ratio:.1%} of revenue)")
        elif rd_ratio > 0.03:
            score += 1
            reasoning.append(f"Modest R&D ({rd_ratio:.1%} of revenue)")
        else:
            reasoning.append(f"Minimal R&D ({rd_ratio:.1%} of revenue)")
    else:
        reasoning.append("R&D data not available — no penalty for non-R&D sectors")

    # Upside/downside capture ratio
    if not prices_df.empty and len(prices_df) >= 20:
        returns = prices_df["close"].pct_change().dropna()
        upside = returns[returns > 0]
        downside = returns[returns < 0]

        if len(upside) > 10 and len(downside) > 10:
            avg_up = upside.mean()
            avg_down = abs(downside.mean())
            up_down_ratio = avg_up / avg_down if avg_down > 0 else 1.0

            if up_down_ratio > 1.3:
                score += 2
                reasoning.append(f"Convex return profile (up/down ratio {up_down_ratio:.2f})")
            elif up_down_ratio > 1.0:
                score += 1
                reasoning.append(f"Slight positive asymmetry (up/down ratio {up_down_ratio:.2f})")
            else:
                reasoning.append(f"Concave returns (up/down ratio {up_down_ratio:.2f}) — unfavorable")
        else:
            reasoning.append("Insufficient return data for asymmetry analysis")
    else:
        reasoning.append("Insufficient price data for return asymmetry analysis")

    # Cash optionality (cash / market_cap)
    cash = getattr(latest_item, "cash_and_equivalents", None) if latest_item else None
    if cash is not None and market_cap and market_cap > 0:
        cash_ratio = cash / market_cap
        if cash_ratio > 0.30:
            score += 3
            reasoning.append(f"Cash is a call option on future opportunities ({cash_ratio:.0%} of market cap)")
        elif cash_ratio > 0.15:
            score += 2
            reasoning.append(f"Strong cash position ({cash_ratio:.0%} of market cap)")
        elif cash_ratio > 0.05:
            score += 1
            reasoning.append(f"Moderate cash buffer ({cash_ratio:.0%} of market cap)")
        else:
            reasoning.append(f"Low cash relative to market cap ({cash_ratio:.0%})")
    else:
        reasoning.append("Cash/market cap data not available")

    # FCF yield
    latest_metrics = metrics[0] if metrics else None
    fcf_yield = None
    if latest_item and market_cap and market_cap > 0:
        fcf = getattr(latest_item, "free_cash_flow", None)
        if fcf is not None:
            fcf_yield = fcf / market_cap
    if fcf_yield is None and latest_metrics:
        fcf_yield = getattr(latest_metrics, "free_cash_flow_yield", None)

    if fcf_yield is not None:
        if fcf_yield > 0.10:
            score += 2
            reasoning.append(f"High FCF yield ({fcf_yield:.1%}) provides margin for convex bet")
        elif fcf_yield > 0.05:
            score += 1
            reasoning.append(f"Decent FCF yield ({fcf_yield:.1%})")
        else:
            reasoning.append(f"Low FCF yield ({fcf_yield:.1%})")
    else:
        reasoning.append("FCF yield data not available")

    return {"score": score, "max_score": 10, "details": "; ".join(reasoning)}

def analyze_fragility(metrics: list, line_items: list) -> dict[str, any]:
    """Via Negativa: detect fragile companies. High score = NOT fragile."""
    if not metrics:
        return {"score": 0, "max_score": 8, "details": "Insufficient data for fragility analysis"}

    score = 0
    reasoning = []
    latest_metrics = metrics[0]

    # Leverage fragility
    debt_to_equity = getattr(latest_metrics, "debt_to_equity", None)
    if debt_to_equity is not None:
        if debt_to_equity > 2.0:
            reasoning.append(f"Extremely fragile balance sheet (D/E {debt_to_equity:.2f})")
        elif debt_to_equity > 1.0:
            score += 1
            reasoning.append(f"Elevated leverage (D/E {debt_to_equity:.2f})")
        elif debt_to_equity > 0.5:
            score += 2
            reasoning.append(f"Moderate leverage (D/E {debt_to_equity:.2f})")
        else:
            score += 3
            reasoning.append(f"Low leverage (D/E {debt_to_equity:.2f}) — not fragile")
    else:
        reasoning.append("Debt-to-equity data not available")

    # Interest coverage
    interest_coverage = getattr(latest_metrics, "interest_coverage", None)
    if interest_coverage is not None:
        if interest_coverage > 10:
            score += 2
            reasoning.append(f"Interest coverage {interest_coverage:.1f}x — debt is irrelevant")
        elif interest_coverage > 5:
            score += 1
            reasoning.append(f"Comfortable interest coverage ({interest_coverage:.1f}x)")
        else:
            reasoning.append(f"Low interest coverage ({interest_coverage:.1f}x) — fragile to rate changes")
    else:
        reasoning.append("Interest coverage data not available")

    # Earnings volatility
    earnings_growth_values = [m.earnings_growth for m in metrics if m.earnings_growth is not None]
    if len(earnings_growth_values) >= 3:
        mean_eg = sum(earnings_growth_values) / len(earnings_growth_values)
        variance = sum((e - mean_eg) ** 2 for e in earnings_growth_values) / len(earnings_growth_values)
        std_eg = variance ** 0.5

        if std_eg < 0.20:
            score += 2
            reasoning.append(f"Stable earnings (growth std {std_eg:.2f}) — robust")
        elif std_eg < 0.50:
            score += 1
            reasoning.append(f"Moderate earnings volatility (growth std {std_eg:.2f})")
        else:
            reasoning.append(f"Highly volatile earnings (growth std {std_eg:.2f}) — fragile")
    else:
        reasoning.append("Insufficient earnings history for volatility analysis")

    # Net margin buffer
    net_margin = getattr(latest_metrics, "net_margin", None)
    if net_margin is not None:
        if net_margin > 0.15:
            score += 1
            reasoning.append(f"Fat margins ({net_margin:.1%}) buffer shocks")
        elif net_margin >= 0.05:
            reasoning.append(f"Moderate margins ({net_margin:.1%})")
        else:
            reasoning.append(f"Paper-thin margins ({net_margin:.1%}) — one shock away from loss")
    else:
        reasoning.append("Net margin data not available")

    # Clamp score at minimum 0
    score = max(score, 0)

    return {"score": score, "max_score": 8, "details": "; ".join(reasoning)}

def analyze_skin_in_game(insider_trades: list) -> dict[str, any]:
    """Assess insider alignment: net insider buying signals trust."""
    if not insider_trades:
        return {"score": 1, "max_score": 4, "details": "No insider trade data — neutral assumption"}

    score = 0
    reasoning = []

    shares_bought = sum(t.transaction_shares or 0 for t in insider_trades if (t.transaction_shares or 0) > 0)
    shares_sold = abs(sum(t.transaction_shares or 0 for t in insider_trades if (t.transaction_shares or 0) < 0))
    net = shares_bought - shares_sold

    if net > 0:
        buy_sell_ratio = net / max(shares_sold, 1)
        if buy_sell_ratio > 2.0:
            score = 4
            reasoning.append(f"Strong skin in the game — net insider buying {net:,} shares (ratio {buy_sell_ratio:.1f}x)")
        elif buy_sell_ratio > 0.5:
            score = 3
            reasoning.append(f"Moderate insider conviction — net buying {net:,} shares")
        else:
            score = 2
            reasoning.append(f"Net insider buying of {net:,} shares")
    else:
        reasoning.append(f"Insiders selling — no skin in the game (net {net:,} shares)")

    return {"score": score, "max_score": 4, "details": "; ".join(reasoning)}

def analyze_volatility_regime(prices_df: pd.DataFrame) -> dict[str, any]:
    """Volatility regime analysis. Key Taleb insight: low vol is dangerous (turkey problem)."""
    if prices_df.empty or len(prices_df) < 30:
        return {"score": 0, "max_score": 6, "details": "Insufficient price data for volatility analysis"}

    score = 0
    reasoning = []

    returns = prices_df["close"].pct_change().dropna()

    # Historical volatility (annualized, 21-day rolling)
    hist_vol = returns.rolling(21).std() * math.sqrt(252)

    # Vol regime ratio (current vol / 63-day avg vol)
    if len(hist_vol.dropna()) >= 63:
        vol_ma = hist_vol.rolling(63).mean()
        current_vol = safe_float(hist_vol.iloc[-1])
        avg_vol = safe_float(vol_ma.iloc[-1])
        vol_regime = current_vol / avg_vol if avg_vol > 0 else 1.0
    elif len(hist_vol.dropna()) >= 21:
        # Fallback: compare current to overall mean
        current_vol = safe_float(hist_vol.iloc[-1])
        avg_vol = safe_float(hist_vol.mean())
        vol_regime = current_vol / avg_vol if avg_vol > 0 else 1.0
    else:
        return {"score": 0, "max_score": 6, "details": "Insufficient data for volatility regime analysis"}

    # Vol regime scoring (max 4)
    if vol_regime < 0.7:
        reasoning.append(f"Dangerously low vol (regime {vol_regime:.2f}) — turkey problem")
    elif vol_regime < 0.9:
        score += 1
        reasoning.append(f"Below-average vol (regime {vol_regime:.2f}) — approaching complacency")
    elif vol_regime <= 1.3:
        score += 3
        reasoning.append(f"Normal vol regime ({vol_regime:.2f}) — fair pricing")
    elif vol_regime <= 2.0:
        score += 4
        reasoning.append(f"Elevated vol (regime {vol_regime:.2f}) — opportunity for the antifragile")
    else:
        score += 2
        reasoning.append(f"Extreme vol (regime {vol_regime:.2f}) — crisis mode")

    # Vol-of-vol scoring (max 2)
    if len(hist_vol.dropna()) >= 42:
        vol_of_vol = hist_vol.rolling(21).std()
        vol_of_vol_clean = vol_of_vol.dropna()
        if len(vol_of_vol_clean) > 0:
            current_vov = safe_float(vol_of_vol_clean.iloc[-1])
            median_vov = safe_float(vol_of_vol_clean.median())
            if median_vov > 0:
                if current_vov > 2 * median_vov:
                    score += 2
                    reasoning.append(f"Highly unstable vol (vol-of-vol {current_vov:.4f} vs median {median_vov:.4f}) — regime change likely")
                elif current_vov > median_vov:
                    score += 1
                    reasoning.append(f"Elevated vol-of-vol ({current_vov:.4f} vs median {median_vov:.4f})")
                else:
                    reasoning.append(f"Stable vol-of-vol ({current_vov:.4f})")
            else:
                reasoning.append("Vol-of-vol median is zero — unusual")
        else:
            reasoning.append("Insufficient vol-of-vol data")
    else:
        reasoning.append("Insufficient history for vol-of-vol analysis")

    return {"score": score, "max_score": 6, "details": "; ".join(reasoning)}

def analyze_black_swan_sentinel(news: list, prices_df: pd.DataFrame) -> dict[str, any]:
    """Monitor for crisis signals: abnormal news sentiment, volume spikes, price dislocations."""
    score = 2  # Default: normal conditions
    reasoning = []

    # News sentiment analysis
    neg_ratio = 0.0
    if news:
        total = len(news)
        neg_count = sum(1 for n in news if n.sentiment and n.sentiment.lower() in ["negative", "bearish"])
        neg_ratio = neg_count / total if total > 0 else 0
    else:
        reasoning.append("No recent news data")

    # Volume spike detection
    volume_spike = 1.0
    recent_return = 0.0
    if not prices_df.empty and len(prices_df) >= 10:
        if "volume" in prices_df.columns:
            recent_vol = prices_df["volume"].iloc[-5:].mean()
            avg_vol = prices_df["volume"].iloc[-63:].mean() if len(prices_df) >= 63 else prices_df["volume"].mean()
            volume_spike = recent_vol / avg_vol if avg_vol > 0 else 1.0

        if len(prices_df) >= 5:
            recent_return = safe_float(prices_df["close"].iloc[-1] / prices_df["close"].iloc[-5] - 1)

    # Scoring
    if neg_ratio > 0.7 and volume_spike > 2.0:
        score = 0
        reasoning.append(f"Black swan warning — {neg_ratio:.0%} negative news, {volume_spike:.1f}x volume spike")
    elif neg_ratio > 0.5 or volume_spike > 2.5:
        score = 1
        reasoning.append(f"Elevated stress signals (neg news {neg_ratio:.0%}, volume {volume_spike:.1f}x)")
    elif neg_ratio > 0.3 and abs(recent_return) > 0.10:
        score = 1
        reasoning.append(f"Moderate stress with price dislocation ({recent_return:.1%} move, {neg_ratio:.0%} negative news)")
    elif neg_ratio < 0.3 and volume_spike < 1.5:
        score = 3
        reasoning.append("No black swan signals detected")
    else:
        reasoning.append(f"Normal conditions (neg news {neg_ratio:.0%}, volume {volume_spike:.1f}x)")

    # Contrarian bonus: high negative news but no volume panic could be opportunity
    if neg_ratio > 0.4 and volume_spike < 1.5 and score < 4:
        score = min(score + 1, 4)
        reasoning.append("Contrarian opportunity — negative sentiment without panic selling")

    return {"score": score, "max_score": 4, "details": "; ".join(reasoning)}


# ==========================
# Peter Lynch helpers
# ==========================

def analyze_lynch_growth(financial_line_items: list) -> dict:
    """
    Evaluate growth based on revenue and EPS trends:
      - Consistent revenue growth
      - Consistent EPS growth
    Peter Lynch liked companies with steady, understandable growth,
    often searching for potential 'ten-baggers' with a long runway.
    """
    if not financial_line_items or len(financial_line_items) < 2:
        return {"score": 0, "details": "Insufficient financial data for growth analysis"}

    details = []
    raw_score = 0  # We'll sum up points, then scale to 0–10 eventually

    # 1) Revenue Growth
    revenues = [fi.revenue for fi in financial_line_items if fi.revenue is not None]
    if len(revenues) >= 2:
        latest_rev = revenues[0]
        older_rev = revenues[-1]
        if older_rev > 0:
            rev_growth = (latest_rev - older_rev) / abs(older_rev)
            if rev_growth > 0.25:
                raw_score += 3
                details.append(f"Strong revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.10:
                raw_score += 2
                details.append(f"Moderate revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.02:
                raw_score += 1
                details.append(f"Slight revenue growth: {rev_growth:.1%}")
            else:
                details.append(f"Flat or negative revenue growth: {rev_growth:.1%}")
        else:
            details.append("Older revenue is zero/negative; can't compute revenue growth.")
    else:
        details.append("Not enough revenue data to assess growth.")

    # 2) EPS Growth
    eps_values = [fi.earnings_per_share for fi in financial_line_items if fi.earnings_per_share is not None]
    if len(eps_values) >= 2:
        latest_eps = eps_values[0]
        older_eps = eps_values[-1]
        if abs(older_eps) > 1e-9:
            eps_growth = (latest_eps - older_eps) / abs(older_eps)
            if eps_growth > 0.25:
                raw_score += 3
                details.append(f"Strong EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.10:
                raw_score += 2
                details.append(f"Moderate EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.02:
                raw_score += 1
                details.append(f"Slight EPS growth: {eps_growth:.1%}")
            else:
                details.append(f"Minimal or negative EPS growth: {eps_growth:.1%}")
        else:
            details.append("Older EPS is near zero; skipping EPS growth calculation.")
    else:
        details.append("Not enough EPS data for growth calculation.")

    # raw_score can be up to 6 => scale to 0–10
    final_score = min(10, (raw_score / 6) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_lynch_fundamentals(financial_line_items: list) -> dict:
    """
    Evaluate basic fundamentals:
      - Debt/Equity
      - Operating margin (or gross margin)
      - Positive Free Cash Flow
    Lynch avoided heavily indebted or complicated businesses.
    """
    if not financial_line_items:
        return {"score": 0, "details": "Insufficient fundamentals data"}

    details = []
    raw_score = 0  # We'll accumulate up to 6 points, then scale to 0–10

    # 1) Debt-to-Equity
    debt_values = [fi.total_debt for fi in financial_line_items if fi.total_debt is not None]
    eq_values = [fi.shareholders_equity for fi in financial_line_items if fi.shareholders_equity is not None]
    if debt_values and eq_values and len(debt_values) == len(eq_values) and len(debt_values) > 0:
        recent_debt = debt_values[0]
        recent_equity = eq_values[0] if eq_values[0] else 1e-9
        de_ratio = recent_debt / recent_equity
        if de_ratio < 0.5:
            raw_score += 2
            details.append(f"Low debt-to-equity: {de_ratio:.2f}")
        elif de_ratio < 1.0:
            raw_score += 1
            details.append(f"Moderate debt-to-equity: {de_ratio:.2f}")
        else:
            details.append(f"High debt-to-equity: {de_ratio:.2f}")
    else:
        details.append("No consistent debt/equity data available.")

    # 2) Operating Margin
    om_values = [fi.operating_margin for fi in financial_line_items if fi.operating_margin is not None]
    if om_values:
        om_recent = om_values[0]
        if om_recent > 0.20:
            raw_score += 2
            details.append(f"Strong operating margin: {om_recent:.1%}")
        elif om_recent > 0.10:
            raw_score += 1
            details.append(f"Moderate operating margin: {om_recent:.1%}")
        else:
            details.append(f"Low operating margin: {om_recent:.1%}")
    else:
        details.append("No operating margin data available.")

    # 3) Positive Free Cash Flow
    fcf_values = [fi.free_cash_flow for fi in financial_line_items if fi.free_cash_flow is not None]
    if fcf_values and fcf_values[0] is not None:
        if fcf_values[0] > 0:
            raw_score += 2
            details.append(f"Positive free cash flow: {fcf_values[0]:,.0f}")
        else:
            details.append(f"Recent FCF is negative: {fcf_values[0]:,.0f}")
    else:
        details.append("No free cash flow data available.")

    # raw_score up to 6 => scale to 0–10
    final_score = min(10, (raw_score / 6) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_lynch_valuation(financial_line_items: list, market_cap: float | None) -> dict:
    """
    Peter Lynch's approach to 'Growth at a Reasonable Price' (GARP):
      - Emphasize the PEG ratio: (P/E) / Growth Rate
      - Also consider a basic P/E if PEG is unavailable
    A PEG < 1 is very attractive; 1-2 is fair; >2 is expensive.
    """
    if not financial_line_items or market_cap is None:
        return {"score": 0, "details": "Insufficient data for valuation"}

    details = []
    raw_score = 0

    # Gather data for P/E
    net_incomes = [fi.net_income for fi in financial_line_items if fi.net_income is not None]
    eps_values = [fi.earnings_per_share for fi in financial_line_items if fi.earnings_per_share is not None]

    # Approximate P/E via (market cap / net income) if net income is positive
    pe_ratio = None
    if net_incomes and net_incomes[0] and net_incomes[0] > 0:
        pe_ratio = market_cap / net_incomes[0]
        details.append(f"Estimated P/E: {pe_ratio:.2f}")
    else:
        details.append("No positive net income => can't compute approximate P/E")

    # If we have at least 2 EPS data points, let's estimate growth
    eps_growth_rate = None
    if len(eps_values) >= 2:
        latest_eps = eps_values[0]
        older_eps = eps_values[-1]
        if older_eps > 0:
            # Calculate annualized growth rate (CAGR) for PEG ratio
            num_years = len(eps_values) - 1
            if latest_eps > 0:
                # CAGR formula: (ending_value/beginning_value)^(1/years) - 1
                eps_growth_rate = (latest_eps / older_eps) ** (1 / num_years) - 1
            else:
                # If latest EPS is negative, use simple average growth
                eps_growth_rate = (latest_eps - older_eps) / (older_eps * num_years)
            details.append(f"Annualized EPS growth rate: {eps_growth_rate:.1%}")
        else:
            details.append("Cannot compute EPS growth rate (older EPS <= 0)")
    else:
        details.append("Not enough EPS data to compute growth rate")

    # Compute PEG if possible
    peg_ratio = None
    if pe_ratio and eps_growth_rate and eps_growth_rate > 0:
        # PEG ratio formula: P/E divided by growth rate (as percentage)
        # Since eps_growth_rate is stored as decimal (0.25 for 25%),
        # we multiply by 100 to convert to percentage for the PEG calculation
        # Example: P/E=20, growth=0.25 (25%) => PEG = 20/25 = 0.8
        peg_ratio = pe_ratio / (eps_growth_rate * 100)
        details.append(f"PEG ratio: {peg_ratio:.2f}")

    # Scoring logic:
    #   - P/E < 15 => +2, < 25 => +1
    #   - PEG < 1 => +3, < 2 => +2, < 3 => +1
    if pe_ratio is not None:
        if pe_ratio < 15:
            raw_score += 2
        elif pe_ratio < 25:
            raw_score += 1

    if peg_ratio is not None:
        if peg_ratio < 1:
            raw_score += 3
        elif peg_ratio < 2:
            raw_score += 2
        elif peg_ratio < 3:
            raw_score += 1

    final_score = min(10, (raw_score / 5) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def pl_analyze_sentiment(news_items: list) -> dict:
    """
    Basic news sentiment check. Negative headlines weigh on the final score.
    """
    if not news_items:
        return {"score": 5, "details": "No news data; default to neutral sentiment"}

    negative_keywords = ["lawsuit", "fraud", "negative", "downturn", "decline", "investigation", "recall"]
    negative_count = 0
    for news in news_items:
        title_lower = (news.title or "").lower()
        if any(word in title_lower for word in negative_keywords):
            negative_count += 1

    details = []
    if negative_count > len(news_items) * 0.3:
        # More than 30% negative => somewhat bearish => 3/10
        score = 3
        details.append(f"High proportion of negative headlines: {negative_count}/{len(news_items)}")
    elif negative_count > 0:
        # Some negativity => 6/10
        score = 6
        details.append(f"Some negative headlines: {negative_count}/{len(news_items)}")
    else:
        # Mostly positive => 8/10
        score = 8
        details.append("Mostly positive or neutral headlines")

    return {"score": score, "details": "; ".join(details)}

def pl_analyze_insider_activity(insider_trades: list) -> dict:
    """
    Simple insider-trade analysis:
      - If there's heavy insider buying, it's a positive sign.
      - If there's mostly selling, it's a negative sign.
      - Otherwise, neutral.
    """
    # Default 5 (neutral)
    score = 5
    details = []

    if not insider_trades:
        details.append("No insider trades data; defaulting to neutral")
        return {"score": score, "details": "; ".join(details)}

    buys, sells = 0, 0
    for trade in insider_trades:
        if trade.transaction_shares is not None:
            if trade.transaction_shares > 0:
                buys += 1
            elif trade.transaction_shares < 0:
                sells += 1

    total = buys + sells
    if total == 0:
        details.append("No significant buy/sell transactions found; neutral stance")
        return {"score": score, "details": "; ".join(details)}

    buy_ratio = buys / total
    if buy_ratio > 0.7:
        # Heavy buying => +3 => total 8
        score = 8
        details.append(f"Heavy insider buying: {buys} buys vs. {sells} sells")
    elif buy_ratio > 0.4:
        # Some buying => +1 => total 6
        score = 6
        details.append(f"Moderate insider buying: {buys} buys vs. {sells} sells")
    else:
        # Mostly selling => -1 => total 4
        score = 4
        details.append(f"Mostly insider selling: {buys} buys vs. {sells} sells")

    return {"score": score, "details": "; ".join(details)}


# ==========================
# Phil Fisher helpers
# ==========================

def analyze_fisher_growth_quality(financial_line_items: list) -> dict:
    """
    Evaluate growth & quality:
      - Consistent Revenue Growth
      - Consistent EPS Growth
      - R&D as a % of Revenue (if relevant, indicative of future-oriented spending)
    """
    if not financial_line_items or len(financial_line_items) < 2:
        return {
            "score": 0,
            "details": "Insufficient financial data for growth/quality analysis",
        }

    details = []
    raw_score = 0  # up to 9 raw points => scale to 0–10

    # 1. Revenue Growth (annualized CAGR)
    revenues = [fi.revenue for fi in financial_line_items if fi.revenue is not None]
    if len(revenues) >= 2:
        # Calculate annualized growth rate (CAGR) for proper comparison
        latest_rev = revenues[0]
        oldest_rev = revenues[-1]
        num_years = len(revenues) - 1
        if oldest_rev > 0 and latest_rev > 0:
            # CAGR formula: (ending_value/beginning_value)^(1/years) - 1
            rev_growth = (latest_rev / oldest_rev) ** (1 / num_years) - 1
            if rev_growth > 0.20:  # 20% annualized
                raw_score += 3
                details.append(f"Very strong annualized revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.10:  # 10% annualized
                raw_score += 2
                details.append(f"Moderate annualized revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.03:  # 3% annualized
                raw_score += 1
                details.append(f"Slight annualized revenue growth: {rev_growth:.1%}")
            else:
                details.append(f"Minimal or negative annualized revenue growth: {rev_growth:.1%}")
        else:
            details.append("Oldest revenue is zero/negative; cannot compute growth.")
    else:
        details.append("Not enough revenue data points for growth calculation.")

    # 2. EPS Growth (annualized CAGR)
    eps_values = [fi.earnings_per_share for fi in financial_line_items if fi.earnings_per_share is not None]
    if len(eps_values) >= 2:
        latest_eps = eps_values[0]
        oldest_eps = eps_values[-1]
        num_years = len(eps_values) - 1
        if oldest_eps > 0 and latest_eps > 0:
            # CAGR formula for EPS
            eps_growth = (latest_eps / oldest_eps) ** (1 / num_years) - 1
            if eps_growth > 0.20:  # 20% annualized
                raw_score += 3
                details.append(f"Very strong annualized EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.10:  # 10% annualized
                raw_score += 2
                details.append(f"Moderate annualized EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.03:  # 3% annualized
                raw_score += 1
                details.append(f"Slight annualized EPS growth: {eps_growth:.1%}")
            else:
                details.append(f"Minimal or negative annualized EPS growth: {eps_growth:.1%}")
        else:
            details.append("Oldest EPS near zero; skipping EPS growth calculation.")
    else:
        details.append("Not enough EPS data points for growth calculation.")

    # 3. R&D as % of Revenue (if we have R&D data)
    rnd_values = [fi.research_and_development for fi in financial_line_items if fi.research_and_development is not None]
    if rnd_values and revenues and len(rnd_values) == len(revenues):
        # We'll just look at the most recent for a simple measure
        recent_rnd = rnd_values[0]
        recent_rev = revenues[0] if revenues[0] else 1e-9
        rnd_ratio = recent_rnd / recent_rev
        # Generally, Fisher admired companies that invest aggressively in R&D,
        # but it must be appropriate. We'll assume "3%-15%" is healthy, just as an example.
        if 0.03 <= rnd_ratio <= 0.15:
            raw_score += 3
            details.append(f"R&D ratio {rnd_ratio:.1%} indicates significant investment in future growth")
        elif rnd_ratio > 0.15:
            raw_score += 2
            details.append(f"R&D ratio {rnd_ratio:.1%} is very high (could be good if well-managed)")
        elif rnd_ratio > 0.0:
            raw_score += 1
            details.append(f"R&D ratio {rnd_ratio:.1%} is somewhat low but still positive")
        else:
            details.append("No meaningful R&D expense ratio")
    else:
        details.append("Insufficient R&D data to evaluate")

    # scale raw_score (max 9) to 0–10
    final_score = min(10, (raw_score / 9) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_margins_stability(financial_line_items: list) -> dict:
    """
    Looks at margin consistency (gross/operating margin) and general stability over time.
    """
    if not financial_line_items or len(financial_line_items) < 2:
        return {
            "score": 0,
            "details": "Insufficient data for margin stability analysis",
        }

    details = []
    raw_score = 0  # up to 6 => scale to 0-10

    # 1. Operating Margin Consistency
    op_margins = [fi.operating_margin for fi in financial_line_items if fi.operating_margin is not None]
    if len(op_margins) >= 2:
        # Check if margins are stable or improving (comparing oldest to newest)
        oldest_op_margin = op_margins[-1]
        newest_op_margin = op_margins[0]
        if newest_op_margin >= oldest_op_margin > 0:
            raw_score += 2
            details.append(f"Operating margin stable or improving ({oldest_op_margin:.1%} -> {newest_op_margin:.1%})")
        elif newest_op_margin > 0:
            raw_score += 1
            details.append(f"Operating margin positive but slightly declined")
        else:
            details.append(f"Operating margin may be negative or uncertain")
    else:
        details.append("Not enough operating margin data points")

    # 2. Gross Margin Level
    gm_values = [fi.gross_margin for fi in financial_line_items if fi.gross_margin is not None]
    if gm_values:
        # We'll just take the most recent
        recent_gm = gm_values[0]
        if recent_gm > 0.5:
            raw_score += 2
            details.append(f"Strong gross margin: {recent_gm:.1%}")
        elif recent_gm > 0.3:
            raw_score += 1
            details.append(f"Moderate gross margin: {recent_gm:.1%}")
        else:
            details.append(f"Low gross margin: {recent_gm:.1%}")
    else:
        details.append("No gross margin data available")

    # 3. Multi-year Margin Stability
    #   e.g. if we have at least 3 data points, see if standard deviation is low.
    if len(op_margins) >= 3:
        stdev = statistics.pstdev(op_margins)
        if stdev < 0.02:
            raw_score += 2
            details.append("Operating margin extremely stable over multiple years")
        elif stdev < 0.05:
            raw_score += 1
            details.append("Operating margin reasonably stable")
        else:
            details.append("Operating margin volatility is high")
    else:
        details.append("Not enough margin data points for volatility check")

    # scale raw_score (max 6) to 0-10
    final_score = min(10, (raw_score / 6) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_management_efficiency_leverage(financial_line_items: list) -> dict:
    """
    Evaluate management efficiency & leverage:
      - Return on Equity (ROE)
      - Debt-to-Equity ratio
      - Possibly check if free cash flow is consistently positive
    """
    if not financial_line_items:
        return {
            "score": 0,
            "details": "No financial data for management efficiency analysis",
        }

    details = []
    raw_score = 0  # up to 6 => scale to 0–10

    # 1. Return on Equity (ROE)
    ni_values = [fi.net_income for fi in financial_line_items if fi.net_income is not None]
    eq_values = [fi.shareholders_equity for fi in financial_line_items if fi.shareholders_equity is not None]
    if ni_values and eq_values and len(ni_values) == len(eq_values):
        recent_ni = ni_values[0]
        recent_eq = eq_values[0] if eq_values[0] else 1e-9
        if recent_ni > 0:
            roe = recent_ni / recent_eq
            if roe > 0.2:
                raw_score += 3
                details.append(f"High ROE: {roe:.1%}")
            elif roe > 0.1:
                raw_score += 2
                details.append(f"Moderate ROE: {roe:.1%}")
            elif roe > 0:
                raw_score += 1
                details.append(f"Positive but low ROE: {roe:.1%}")
            else:
                details.append(f"ROE is near zero or negative: {roe:.1%}")
        else:
            details.append("Recent net income is zero or negative, hurting ROE")
    else:
        details.append("Insufficient data for ROE calculation")

    # 2. Debt-to-Equity
    debt_values = [fi.total_debt for fi in financial_line_items if fi.total_debt is not None]
    if debt_values and eq_values and len(debt_values) == len(eq_values):
        recent_debt = debt_values[0]
        recent_equity = eq_values[0] if eq_values[0] else 1e-9
        dte = recent_debt / recent_equity
        if dte < 0.3:
            raw_score += 2
            details.append(f"Low debt-to-equity: {dte:.2f}")
        elif dte < 1.0:
            raw_score += 1
            details.append(f"Manageable debt-to-equity: {dte:.2f}")
        else:
            details.append(f"High debt-to-equity: {dte:.2f}")
    else:
        details.append("Insufficient data for debt/equity analysis")

    # 3. FCF Consistency
    fcf_values = [fi.free_cash_flow for fi in financial_line_items if fi.free_cash_flow is not None]
    if fcf_values and len(fcf_values) >= 2:
        # Check if FCF is positive in recent years
        positive_fcf_count = sum(1 for x in fcf_values if x and x > 0)
        # We'll be simplistic: if most are positive, reward
        ratio = positive_fcf_count / len(fcf_values)
        if ratio > 0.8:
            raw_score += 1
            details.append(f"Majority of periods have positive FCF ({positive_fcf_count}/{len(fcf_values)})")
        else:
            details.append(f"Free cash flow is inconsistent or often negative")
    else:
        details.append("Insufficient or no FCF data to check consistency")

    final_score = min(10, (raw_score / 6) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_fisher_valuation(financial_line_items: list, market_cap: float | None) -> dict:
    """
    Phil Fisher is willing to pay for quality and growth, but still checks:
      - P/E
      - P/FCF
      - (Optionally) Enterprise Value metrics, but simpler approach is typical
    We will grant up to 2 points for each of two metrics => max 4 raw => scale to 0–10.
    """
    if not financial_line_items or market_cap is None:
        return {"score": 0, "details": "Insufficient data to perform valuation"}

    details = []
    raw_score = 0

    # Gather needed data
    net_incomes = [fi.net_income for fi in financial_line_items if fi.net_income is not None]
    fcf_values = [fi.free_cash_flow for fi in financial_line_items if fi.free_cash_flow is not None]

    # 1) P/E
    recent_net_income = net_incomes[0] if net_incomes else None
    if recent_net_income and recent_net_income > 0:
        pe = market_cap / recent_net_income
        pe_points = 0
        if pe < 20:
            pe_points = 2
            details.append(f"Reasonably attractive P/E: {pe:.2f}")
        elif pe < 30:
            pe_points = 1
            details.append(f"Somewhat high but possibly justifiable P/E: {pe:.2f}")
        else:
            details.append(f"Very high P/E: {pe:.2f}")
        raw_score += pe_points
    else:
        details.append("No positive net income for P/E calculation")

    # 2) P/FCF
    recent_fcf = fcf_values[0] if fcf_values else None
    if recent_fcf and recent_fcf > 0:
        pfcf = market_cap / recent_fcf
        pfcf_points = 0
        if pfcf < 20:
            pfcf_points = 2
            details.append(f"Reasonable P/FCF: {pfcf:.2f}")
        elif pfcf < 30:
            pfcf_points = 1
            details.append(f"Somewhat high P/FCF: {pfcf:.2f}")
        else:
            details.append(f"Excessively high P/FCF: {pfcf:.2f}")
        raw_score += pfcf_points
    else:
        details.append("No positive free cash flow for P/FCF calculation")

    # scale raw_score (max 4) to 0–10
    final_score = min(10, (raw_score / 4) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def pf_analyze_insider_activity(insider_trades: list) -> dict:
    """
    Simple insider-trade analysis:
      - If there's heavy insider buying, we nudge the score up.
      - If there's mostly selling, we reduce it.
      - Otherwise, neutral.
    """
    # Default is neutral (5/10).
    score = 5
    details = []

    if not insider_trades:
        details.append("No insider trades data; defaulting to neutral")
        return {"score": score, "details": "; ".join(details)}

    buys, sells = 0, 0
    for trade in insider_trades:
        if trade.transaction_shares is not None:
            if trade.transaction_shares > 0:
                buys += 1
            elif trade.transaction_shares < 0:
                sells += 1

    total = buys + sells
    if total == 0:
        details.append("No buy/sell transactions found; neutral")
        return {"score": score, "details": "; ".join(details)}

    buy_ratio = buys / total
    if buy_ratio > 0.7:
        score = 8
        details.append(f"Heavy insider buying: {buys} buys vs. {sells} sells")
    elif buy_ratio > 0.4:
        score = 6
        details.append(f"Moderate insider buying: {buys} buys vs. {sells} sells")
    else:
        score = 4
        details.append(f"Mostly insider selling: {buys} buys vs. {sells} sells")

    return {"score": score, "details": "; ".join(details)}

def pf_analyze_sentiment(news_items: list) -> dict:
    """
    Basic news sentiment: negative keyword check vs. overall volume.
    """
    if not news_items:
        return {"score": 5, "details": "No news data; defaulting to neutral sentiment"}

    negative_keywords = ["lawsuit", "fraud", "negative", "downturn", "decline", "investigation", "recall"]
    negative_count = 0
    for news in news_items:
        title_lower = (news.title or "").lower()
        if any(word in title_lower for word in negative_keywords):
            negative_count += 1

    details = []
    if negative_count > len(news_items) * 0.3:
        score = 3
        details.append(f"High proportion of negative headlines: {negative_count}/{len(news_items)}")
    elif negative_count > 0:
        score = 6
        details.append(f"Some negative headlines: {negative_count}/{len(news_items)}")
    else:
        score = 8
        details.append("Mostly positive/neutral headlines")

    return {"score": score, "details": "; ".join(details)}


# ==========================
# Stanley Druckenmiller helpers
# ==========================

def analyze_growth_and_momentum(financial_line_items: list, prices: list) -> dict:
    """
    Evaluate:
      - Revenue Growth (YoY)
      - EPS Growth (YoY)
      - Price Momentum
    """
    if not financial_line_items or len(financial_line_items) < 2:
        return {"score": 0, "details": "Insufficient financial data for growth analysis"}

    details = []
    raw_score = 0  # We'll sum up a maximum of 9 raw points, then scale to 0–10

    #
    # 1. Revenue Growth (annualized CAGR)
    #
    revenues = [fi.revenue for fi in financial_line_items if fi.revenue is not None]
    if len(revenues) >= 2:
        latest_rev = revenues[0]
        older_rev = revenues[-1]
        num_years = len(revenues) - 1
        if older_rev > 0 and latest_rev > 0:
            # CAGR formula: (ending_value/beginning_value)^(1/years) - 1
            rev_growth = (latest_rev / older_rev) ** (1 / num_years) - 1
            if rev_growth > 0.08:  # 8% annualized (adjusted for CAGR)
                raw_score += 3
                details.append(f"Strong annualized revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.04:  # 4% annualized
                raw_score += 2
                details.append(f"Moderate annualized revenue growth: {rev_growth:.1%}")
            elif rev_growth > 0.01:  # 1% annualized
                raw_score += 1
                details.append(f"Slight annualized revenue growth: {rev_growth:.1%}")
            else:
                details.append(f"Minimal/negative revenue growth: {rev_growth:.1%}")
        else:
            details.append("Older revenue is zero/negative; can't compute revenue growth.")
    else:
        details.append("Not enough revenue data points for growth calculation.")

    #
    # 2. EPS Growth (annualized CAGR)
    #
    eps_values = [fi.earnings_per_share for fi in financial_line_items if fi.earnings_per_share is not None]
    if len(eps_values) >= 2:
        latest_eps = eps_values[0]
        older_eps = eps_values[-1]
        num_years = len(eps_values) - 1
        # Calculate CAGR for positive EPS values
        if older_eps > 0 and latest_eps > 0:
            # CAGR formula for EPS
            eps_growth = (latest_eps / older_eps) ** (1 / num_years) - 1
            if eps_growth > 0.08:  # 8% annualized (adjusted for CAGR)
                raw_score += 3
                details.append(f"Strong annualized EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.04:  # 4% annualized
                raw_score += 2
                details.append(f"Moderate annualized EPS growth: {eps_growth:.1%}")
            elif eps_growth > 0.01:  # 1% annualized
                raw_score += 1
                details.append(f"Slight annualized EPS growth: {eps_growth:.1%}")
            else:
                details.append(f"Minimal/negative annualized EPS growth: {eps_growth:.1%}")
        else:
            details.append("Older EPS is near zero; skipping EPS growth calculation.")
    else:
        details.append("Not enough EPS data points for growth calculation.")

    #
    # 3. Price Momentum
    #
    # We'll give up to 3 points for strong momentum
    if prices and len(prices) > 30:
        sorted_prices = sorted(prices, key=lambda p: p.time)
        close_prices = [p.close for p in sorted_prices if p.close is not None]
        if len(close_prices) >= 2:
            start_price = close_prices[0]
            end_price = close_prices[-1]
            if start_price > 0:
                pct_change = (end_price - start_price) / start_price
                if pct_change > 0.50:
                    raw_score += 3
                    details.append(f"Very strong price momentum: {pct_change:.1%}")
                elif pct_change > 0.20:
                    raw_score += 2
                    details.append(f"Moderate price momentum: {pct_change:.1%}")
                elif pct_change > 0:
                    raw_score += 1
                    details.append(f"Slight positive momentum: {pct_change:.1%}")
                else:
                    details.append(f"Negative price momentum: {pct_change:.1%}")
            else:
                details.append("Invalid start price (<= 0); can't compute momentum.")
        else:
            details.append("Insufficient price data for momentum calculation.")
    else:
        details.append("Not enough recent price data for momentum analysis.")

    # We assigned up to 3 points each for:
    #   revenue growth, eps growth, momentum
    # => max raw_score = 9
    # Scale to 0–10
    final_score = min(10, (raw_score / 9) * 10)

    return {"score": final_score, "details": "; ".join(details)}

def sd_analyze_insider_activity(insider_trades: list) -> dict:
    """
    Simple insider-trade analysis:
      - If there's heavy insider buying, we nudge the score up.
      - If there's mostly selling, we reduce it.
      - Otherwise, neutral.
    """
    # Default is neutral (5/10).
    score = 5
    details = []

    if not insider_trades:
        details.append("No insider trades data; defaulting to neutral")
        return {"score": score, "details": "; ".join(details)}

    buys, sells = 0, 0
    for trade in insider_trades:
        # Use transaction_shares to determine if it's a buy or sell
        # Negative shares = sell, positive shares = buy
        if trade.transaction_shares is not None:
            if trade.transaction_shares > 0:
                buys += 1
            elif trade.transaction_shares < 0:
                sells += 1

    total = buys + sells
    if total == 0:
        details.append("No buy/sell transactions found; neutral")
        return {"score": score, "details": "; ".join(details)}

    buy_ratio = buys / total
    if buy_ratio > 0.7:
        # Heavy buying => +3 points from the neutral 5 => 8
        score = 8
        details.append(f"Heavy insider buying: {buys} buys vs. {sells} sells")
    elif buy_ratio > 0.4:
        # Moderate buying => +1 => 6
        score = 6
        details.append(f"Moderate insider buying: {buys} buys vs. {sells} sells")
    else:
        # Low insider buying => -1 => 4
        score = 4
        details.append(f"Mostly insider selling: {buys} buys vs. {sells} sells")

    return {"score": score, "details": "; ".join(details)}

def sd_analyze_sentiment(news_items: list) -> dict:
    """
    Basic news sentiment: negative keyword check vs. overall volume.
    """
    if not news_items:
        return {"score": 5, "details": "No news data; defaulting to neutral sentiment"}

    negative_keywords = ["lawsuit", "fraud", "negative", "downturn", "decline", "investigation", "recall"]
    negative_count = 0
    for news in news_items:
        title_lower = (news.title or "").lower()
        if any(word in title_lower for word in negative_keywords):
            negative_count += 1

    details = []
    if negative_count > len(news_items) * 0.3:
        # More than 30% negative => somewhat bearish => 3/10
        score = 3
        details.append(f"High proportion of negative headlines: {negative_count}/{len(news_items)}")
    elif negative_count > 0:
        # Some negativity => 6/10
        score = 6
        details.append(f"Some negative headlines: {negative_count}/{len(news_items)}")
    else:
        # Mostly positive => 8/10
        score = 8
        details.append("Mostly positive/neutral headlines")

    return {"score": score, "details": "; ".join(details)}

def analyze_risk_reward(financial_line_items: list, prices: list) -> dict:
    """
    Assesses risk via:
      - Debt-to-Equity
      - Price Volatility
    Aims for strong upside with contained downside.
    """
    if not financial_line_items or not prices:
        return {"score": 0, "details": "Insufficient data for risk-reward analysis"}

    details = []
    raw_score = 0  # We'll accumulate up to 6 raw points, then scale to 0-10

    #
    # 1. Debt-to-Equity
    #
    debt_values = [fi.total_debt for fi in financial_line_items if fi.total_debt is not None]
    equity_values = [fi.shareholders_equity for fi in financial_line_items if fi.shareholders_equity is not None]

    if debt_values and equity_values and len(debt_values) == len(equity_values) and len(debt_values) > 0:
        recent_debt = debt_values[0]
        recent_equity = equity_values[0] if equity_values[0] else 1e-9
        de_ratio = recent_debt / recent_equity
        if de_ratio < 0.3:
            raw_score += 3
            details.append(f"Low debt-to-equity: {de_ratio:.2f}")
        elif de_ratio < 0.7:
            raw_score += 2
            details.append(f"Moderate debt-to-equity: {de_ratio:.2f}")
        elif de_ratio < 1.5:
            raw_score += 1
            details.append(f"Somewhat high debt-to-equity: {de_ratio:.2f}")
        else:
            details.append(f"High debt-to-equity: {de_ratio:.2f}")
    else:
        details.append("No consistent debt/equity data available.")

    #
    # 2. Price Volatility
    #
    if len(prices) > 10:
        sorted_prices = sorted(prices, key=lambda p: p.time)
        close_prices = [p.close for p in sorted_prices if p.close is not None]
        if len(close_prices) > 10:
            daily_returns = []
            for i in range(1, len(close_prices)):
                prev_close = close_prices[i - 1]
                if prev_close > 0:
                    daily_returns.append((close_prices[i] - prev_close) / prev_close)
            if daily_returns:
                stdev = statistics.pstdev(daily_returns)  # population stdev
                if stdev < 0.01:
                    raw_score += 3
                    details.append(f"Low volatility: daily returns stdev {stdev:.2%}")
                elif stdev < 0.02:
                    raw_score += 2
                    details.append(f"Moderate volatility: daily returns stdev {stdev:.2%}")
                elif stdev < 0.04:
                    raw_score += 1
                    details.append(f"High volatility: daily returns stdev {stdev:.2%}")
                else:
                    details.append(f"Very high volatility: daily returns stdev {stdev:.2%}")
            else:
                details.append("Insufficient daily returns data for volatility calc.")
        else:
            details.append("Not enough close-price data points for volatility analysis.")
    else:
        details.append("Not enough price data for volatility analysis.")

    # raw_score out of 6 => scale to 0–10
    final_score = min(10, (raw_score / 6) * 10)
    return {"score": final_score, "details": "; ".join(details)}

def analyze_druckenmiller_valuation(financial_line_items: list, market_cap: float | None) -> dict:
    """
    Druckenmiller is willing to pay up for growth, but still checks:
      - P/E
      - P/FCF
      - EV/EBIT
      - EV/EBITDA
    Each can yield up to 2 points => max 8 raw points => scale to 0–10.
    """
    if not financial_line_items or market_cap is None:
        return {"score": 0, "details": "Insufficient data to perform valuation"}

    details = []
    raw_score = 0

    # Gather needed data
    net_incomes = [fi.net_income for fi in financial_line_items if fi.net_income is not None]
    fcf_values = [fi.free_cash_flow for fi in financial_line_items if fi.free_cash_flow is not None]
    ebit_values = [fi.ebit for fi in financial_line_items if fi.ebit is not None]
    ebitda_values = [fi.ebitda for fi in financial_line_items if fi.ebitda is not None]

    # For EV calculation, let's get the most recent total_debt & cash
    debt_values = [fi.total_debt for fi in financial_line_items if fi.total_debt is not None]
    cash_values = [fi.cash_and_equivalents for fi in financial_line_items if fi.cash_and_equivalents is not None]
    recent_debt = debt_values[0] if debt_values else 0
    recent_cash = cash_values[0] if cash_values else 0

    enterprise_value = market_cap + recent_debt - recent_cash

    # 1) P/E
    recent_net_income = net_incomes[0] if net_incomes else None
    if recent_net_income and recent_net_income > 0:
        pe = market_cap / recent_net_income
        pe_points = 0
        if pe < 15:
            pe_points = 2
            details.append(f"Attractive P/E: {pe:.2f}")
        elif pe < 25:
            pe_points = 1
            details.append(f"Fair P/E: {pe:.2f}")
        else:
            details.append(f"High or Very high P/E: {pe:.2f}")
        raw_score += pe_points
    else:
        details.append("No positive net income for P/E calculation")

    # 2) P/FCF
    recent_fcf = fcf_values[0] if fcf_values else None
    if recent_fcf and recent_fcf > 0:
        pfcf = market_cap / recent_fcf
        pfcf_points = 0
        if pfcf < 15:
            pfcf_points = 2
            details.append(f"Attractive P/FCF: {pfcf:.2f}")
        elif pfcf < 25:
            pfcf_points = 1
            details.append(f"Fair P/FCF: {pfcf:.2f}")
        else:
            details.append(f"High/Very high P/FCF: {pfcf:.2f}")
        raw_score += pfcf_points
    else:
        details.append("No positive free cash flow for P/FCF calculation")

    # 3) EV/EBIT
    recent_ebit = ebit_values[0] if ebit_values else None
    if enterprise_value > 0 and recent_ebit and recent_ebit > 0:
        ev_ebit = enterprise_value / recent_ebit
        ev_ebit_points = 0
        if ev_ebit < 15:
            ev_ebit_points = 2
            details.append(f"Attractive EV/EBIT: {ev_ebit:.2f}")
        elif ev_ebit < 25:
            ev_ebit_points = 1
            details.append(f"Fair EV/EBIT: {ev_ebit:.2f}")
        else:
            details.append(f"High EV/EBIT: {ev_ebit:.2f}")
        raw_score += ev_ebit_points
    else:
        details.append("No valid EV/EBIT because EV <= 0 or EBIT <= 0")

    # 4) EV/EBITDA
    recent_ebitda = ebitda_values[0] if ebitda_values else None
    if enterprise_value > 0 and recent_ebitda and recent_ebitda > 0:
        ev_ebitda = enterprise_value / recent_ebitda
        ev_ebitda_points = 0
        if ev_ebitda < 10:
            ev_ebitda_points = 2
            details.append(f"Attractive EV/EBITDA: {ev_ebitda:.2f}")
        elif ev_ebitda < 18:
            ev_ebitda_points = 1
            details.append(f"Fair EV/EBITDA: {ev_ebitda:.2f}")
        else:
            details.append(f"High EV/EBITDA: {ev_ebitda:.2f}")
        raw_score += ev_ebitda_points
    else:
        details.append("No valid EV/EBITDA because EV <= 0 or EBITDA <= 0")

    # We have up to 2 points for each of the 4 metrics => 8 raw points max
    # Scale raw_score to 0–10
    final_score = min(10, (raw_score / 8) * 10)

    return {"score": final_score, "details": "; ".join(details)}


# ==========================
# Mohnish Pabrai helpers
# ==========================

def analyze_downside_protection(financial_line_items: list) -> dict[str, any]:
    """Assess balance-sheet strength and downside resiliency (capital preservation first)."""
    if not financial_line_items:
        return {"score": 0, "details": "Insufficient data"}

    latest = financial_line_items[0]
    details: list[str] = []
    score = 0

    cash = getattr(latest, "cash_and_equivalents", None)
    debt = getattr(latest, "total_debt", None)
    current_assets = getattr(latest, "current_assets", None)
    current_liabilities = getattr(latest, "current_liabilities", None)
    equity = getattr(latest, "shareholders_equity", None)

    # Net cash position is a strong downside protector
    net_cash = None
    if cash is not None and debt is not None:
        net_cash = cash - debt
        if net_cash > 0:
            score += 3
            details.append(f"Net cash position: ${net_cash:,.0f}")
        else:
            details.append(f"Net debt position: ${net_cash:,.0f}")

    # Current ratio
    if current_assets is not None and current_liabilities is not None and current_liabilities > 0:
        current_ratio = current_assets / current_liabilities
        if current_ratio >= 2.0:
            score += 2
            details.append(f"Strong liquidity (current ratio {current_ratio:.2f})")
        elif current_ratio >= 1.2:
            score += 1
            details.append(f"Adequate liquidity (current ratio {current_ratio:.2f})")
        else:
            details.append(f"Weak liquidity (current ratio {current_ratio:.2f})")

    # Low leverage
    if equity is not None and equity > 0 and debt is not None:
        de_ratio = debt / equity
        if de_ratio < 0.3:
            score += 2
            details.append(f"Very low leverage (D/E {de_ratio:.2f})")
        elif de_ratio < 0.7:
            score += 1
            details.append(f"Moderate leverage (D/E {de_ratio:.2f})")
        else:
            details.append(f"High leverage (D/E {de_ratio:.2f})")

    # Free cash flow positive and stable
    fcf_values = [getattr(li, "free_cash_flow", None) for li in financial_line_items if getattr(li, "free_cash_flow", None) is not None]
    if fcf_values and len(fcf_values) >= 3:
        recent_avg = sum(fcf_values[:3]) / 3
        older = sum(fcf_values[-3:]) / 3 if len(fcf_values) >= 6 else fcf_values[-1]
        if recent_avg > 0 and recent_avg >= older:
            score += 2
            details.append("Positive and improving/stable FCF")
        elif recent_avg > 0:
            score += 1
            details.append("Positive but declining FCF")
        else:
            details.append("Negative FCF")

    return {"score": min(10, score), "details": "; ".join(details)}

def analyze_pabrai_valuation(financial_line_items: list, market_cap: float | None) -> dict[str, any]:
    """Value via simple FCF yield and asset-light preference (keep it simple, low mistakes)."""
    if not financial_line_items or market_cap is None or market_cap <= 0:
        return {"score": 0, "details": "Insufficient data", "fcf_yield": None, "normalized_fcf": None}

    details: list[str] = []
    fcf_values = [getattr(li, "free_cash_flow", None) for li in financial_line_items if getattr(li, "free_cash_flow", None) is not None]
    capex_vals = [abs(getattr(li, "capital_expenditure", 0) or 0) for li in financial_line_items]

    if not fcf_values or len(fcf_values) < 3:
        return {"score": 0, "details": "Insufficient FCF history", "fcf_yield": None, "normalized_fcf": None}

    normalized_fcf = sum(fcf_values[:min(5, len(fcf_values))]) / min(5, len(fcf_values))
    if normalized_fcf <= 0:
        return {"score": 0, "details": "Non-positive normalized FCF", "fcf_yield": None, "normalized_fcf": normalized_fcf}

    fcf_yield = normalized_fcf / market_cap

    score = 0
    if fcf_yield > 0.10:
        score += 4
        details.append(f"Exceptional value: {fcf_yield:.1%} FCF yield")
    elif fcf_yield > 0.07:
        score += 3
        details.append(f"Attractive value: {fcf_yield:.1%} FCF yield")
    elif fcf_yield > 0.05:
        score += 2
        details.append(f"Reasonable value: {fcf_yield:.1%} FCF yield")
    elif fcf_yield > 0.03:
        score += 1
        details.append(f"Borderline value: {fcf_yield:.1%} FCF yield")
    else:
        details.append(f"Expensive: {fcf_yield:.1%} FCF yield")

    # Asset-light tilt: lower capex intensity preferred
    if capex_vals and len(financial_line_items) >= 3:
        revenue_vals = [getattr(li, "revenue", None) for li in financial_line_items]
        capex_to_revenue = []
        for i, li in enumerate(financial_line_items):
            revenue = getattr(li, "revenue", None)
            capex = abs(getattr(li, "capital_expenditure", 0) or 0)
            if revenue and revenue > 0:
                capex_to_revenue.append(capex / revenue)
        if capex_to_revenue:
            avg_ratio = sum(capex_to_revenue) / len(capex_to_revenue)
            if avg_ratio < 0.05:
                score += 2
                details.append(f"Asset-light: Avg capex {avg_ratio:.1%} of revenue")
            elif avg_ratio < 0.10:
                score += 1
                details.append(f"Moderate capex: Avg capex {avg_ratio:.1%} of revenue")
            else:
                details.append(f"Capex heavy: Avg capex {avg_ratio:.1%} of revenue")

    return {"score": min(10, score), "details": "; ".join(details), "fcf_yield": fcf_yield, "normalized_fcf": normalized_fcf}

def analyze_double_potential(financial_line_items: list, market_cap: float | None) -> dict[str, any]:
    """Estimate low-risk path to double capital in ~2-3 years: runway from FCF growth + rerating."""
    if not financial_line_items or market_cap is None or market_cap <= 0:
        return {"score": 0, "details": "Insufficient data"}

    details: list[str] = []

    # Use revenue and FCF trends as rough growth proxy (keep it simple)
    revenues = [getattr(li, "revenue", None) for li in financial_line_items if getattr(li, "revenue", None) is not None]
    fcfs = [getattr(li, "free_cash_flow", None) for li in financial_line_items if getattr(li, "free_cash_flow", None) is not None]

    score = 0
    if revenues and len(revenues) >= 3:
        recent_rev = sum(revenues[:3]) / 3
        older_rev = sum(revenues[-3:]) / 3 if len(revenues) >= 6 else revenues[-1]
        if older_rev > 0:
            rev_growth = (recent_rev / older_rev) - 1
            if rev_growth > 0.15:
                score += 2
                details.append(f"Strong revenue trajectory ({rev_growth:.1%})")
            elif rev_growth > 0.05:
                score += 1
                details.append(f"Modest revenue growth ({rev_growth:.1%})")

    if fcfs and len(fcfs) >= 3:
        recent_fcf = sum(fcfs[:3]) / 3
        older_fcf = sum(fcfs[-3:]) / 3 if len(fcfs) >= 6 else fcfs[-1]
        if older_fcf != 0:
            fcf_growth = (recent_fcf / older_fcf) - 1
            if fcf_growth > 0.20:
                score += 3
                details.append(f"Strong FCF growth ({fcf_growth:.1%})")
            elif fcf_growth > 0.08:
                score += 2
                details.append(f"Healthy FCF growth ({fcf_growth:.1%})")
            elif fcf_growth > 0:
                score += 1
                details.append(f"Positive FCF growth ({fcf_growth:.1%})")

    # If FCF yield is already high (>8%), doubling can come from cash generation alone in few years
    tmp_val = analyze_pabrai_valuation(financial_line_items, market_cap)
    fcf_yield = tmp_val.get("fcf_yield")
    if fcf_yield is not None:
        if fcf_yield > 0.08:
            score += 3
            details.append("High FCF yield can drive doubling via retained cash/Buybacks")
        elif fcf_yield > 0.05:
            score += 1
            details.append("Reasonable FCF yield supports moderate compounding")

    return {"score": min(10, score), "details": "; ".join(details)}


# ==========================
# Rakesh Jhunjhunwala helpers
# ==========================

def analyze_profitability(financial_line_items: list) -> dict[str, any]:
    """
    Analyze profitability metrics like net income, EBIT, EPS, operating income.
    Focus on strong, consistent earnings growth and operating efficiency.
    """
    if not financial_line_items:
        return {"score": 0, "details": "No profitability data available"}

    latest = financial_line_items[0]
    score = 0
    reasoning = []

    # Calculate ROE (Return on Equity) - Jhunjhunwala's key metric
    if (getattr(latest, 'net_income', None) and latest.net_income > 0 and
        getattr(latest, 'total_assets', None) and getattr(latest, 'total_liabilities', None) and 
        latest.total_assets and latest.total_liabilities):
        
        shareholders_equity = latest.total_assets - latest.total_liabilities
        if shareholders_equity > 0:
            roe = (latest.net_income / shareholders_equity) * 100
            if roe > 20:  # Excellent ROE
                score += 3
                reasoning.append(f"Excellent ROE: {roe:.1f}%")
            elif roe > 15:  # Good ROE
                score += 2
                reasoning.append(f"Good ROE: {roe:.1f}%")
            elif roe > 10:  # Decent ROE
                score += 1
                reasoning.append(f"Decent ROE: {roe:.1f}%")
            else:
                reasoning.append(f"Low ROE: {roe:.1f}%")
        else:
            reasoning.append("Negative shareholders equity")
    else:
        reasoning.append("Unable to calculate ROE - missing data")

    # Operating Margin Analysis
    if (getattr(latest, "operating_income", None) and latest.operating_income and 
        getattr(latest, "revenue", None) and latest.revenue and latest.revenue > 0):
        operating_margin = (latest.operating_income / latest.revenue) * 100
        if operating_margin > 20:  # Excellent margin
            score += 2
            reasoning.append(f"Excellent operating margin: {operating_margin:.1f}%")
        elif operating_margin > 15:  # Good margin
            score += 1
            reasoning.append(f"Good operating margin: {operating_margin:.1f}%")
        elif operating_margin > 0:
            reasoning.append(f"Positive operating margin: {operating_margin:.1f}%")
        else:
            reasoning.append(f"Negative operating margin: {operating_margin:.1f}%")
    else:
        reasoning.append("Unable to calculate operating margin")

    # EPS Growth Consistency (3-year trend)
    eps_values = [getattr(item, "earnings_per_share", None) for item in financial_line_items 
                  if getattr(item, "earnings_per_share", None) is not None and getattr(item, "earnings_per_share", None) > 0]
    
    if len(eps_values) >= 3:
        # Calculate CAGR for EPS
        initial_eps = eps_values[-1]  # Oldest value
        final_eps = eps_values[0]     # Latest value
        years = len(eps_values) - 1
        
        if initial_eps > 0:
            eps_cagr = ((final_eps / initial_eps) ** (1/years) - 1) * 100
            if eps_cagr > 20:  # High growth
                score += 3
                reasoning.append(f"High EPS CAGR: {eps_cagr:.1f}%")
            elif eps_cagr > 15:  # Good growth
                score += 2
                reasoning.append(f"Good EPS CAGR: {eps_cagr:.1f}%")
            elif eps_cagr > 10:  # Moderate growth
                score += 1
                reasoning.append(f"Moderate EPS CAGR: {eps_cagr:.1f}%")
            else:
                reasoning.append(f"Low EPS CAGR: {eps_cagr:.1f}%")
        else:
            reasoning.append("Cannot calculate EPS growth from negative base")
    else:
        reasoning.append("Insufficient EPS data for growth analysis")

    return {"score": score, "details": "; ".join(reasoning)}

def analyze_growth(financial_line_items: list) -> dict[str, any]:
    """
    Analyze revenue and net income growth trends using CAGR.
    Jhunjhunwala favored companies with strong, consistent compound growth.
    """
    if len(financial_line_items) < 3:
        return {"score": 0, "details": "Insufficient data for growth analysis"}

    score = 0
    reasoning = []

    # Revenue CAGR Analysis
    revenues = [getattr(item, "revenue", None) for item in financial_line_items 
                if getattr(item, "revenue", None) is not None and getattr(item, "revenue", None) > 0]
    
    if len(revenues) >= 3:
        initial_revenue = revenues[-1]  # Oldest
        final_revenue = revenues[0]     # Latest
        years = len(revenues) - 1
        
        if initial_revenue > 0:  # Fixed: Add zero check
            revenue_cagr = ((final_revenue / initial_revenue) ** (1/years) - 1) * 100
            
            if revenue_cagr > 20:  # High growth
                score += 3
                reasoning.append(f"Excellent revenue CAGR: {revenue_cagr:.1f}%")
            elif revenue_cagr > 15:  # Good growth
                score += 2
                reasoning.append(f"Good revenue CAGR: {revenue_cagr:.1f}%")
            elif revenue_cagr > 10:  # Moderate growth
                score += 1
                reasoning.append(f"Moderate revenue CAGR: {revenue_cagr:.1f}%")
            else:
                reasoning.append(f"Low revenue CAGR: {revenue_cagr:.1f}%")
        else:
            reasoning.append("Cannot calculate revenue CAGR from zero base")
    else:
        reasoning.append("Insufficient revenue data for CAGR calculation")

    # Net Income CAGR Analysis
    net_incomes = [getattr(item, "net_income", None) for item in financial_line_items 
                   if getattr(item, "net_income", None) is not None and getattr(item, "net_income", None) > 0]
    
    if len(net_incomes) >= 3:
        initial_income = net_incomes[-1]  # Oldest
        final_income = net_incomes[0]     # Latest
        years = len(net_incomes) - 1
        
        if initial_income > 0:  # Fixed: Add zero check
            income_cagr = ((final_income / initial_income) ** (1/years) - 1) * 100
            
            if income_cagr > 25:  # Very high growth
                score += 3
                reasoning.append(f"Excellent income CAGR: {income_cagr:.1f}%")
            elif income_cagr > 20:  # High growth
                score += 2
                reasoning.append(f"High income CAGR: {income_cagr:.1f}%")
            elif income_cagr > 15:  # Good growth
                score += 1
                reasoning.append(f"Good income CAGR: {income_cagr:.1f}%")
            else:
                reasoning.append(f"Moderate income CAGR: {income_cagr:.1f}%")
        else:
            reasoning.append("Cannot calculate income CAGR from zero base")
    else:
        reasoning.append("Insufficient net income data for CAGR calculation")

    # Revenue Consistency Check (year-over-year)
    if len(revenues) >= 3:
        declining_years = sum(1 for i in range(1, len(revenues)) if revenues[i-1] > revenues[i])
        consistency_ratio = 1 - (declining_years / (len(revenues) - 1))
        
        if consistency_ratio >= 0.8:  # 80% or more years with growth
            score += 1
            reasoning.append(f"Consistent growth pattern ({consistency_ratio*100:.0f}% of years)")
        else:
            reasoning.append(f"Inconsistent growth pattern ({consistency_ratio*100:.0f}% of years)")

    return {"score": score, "details": "; ".join(reasoning)}

def analyze_balance_sheet(financial_line_items: list) -> dict[str, any]:
    """
    Check financial strength - healthy asset/liability structure, liquidity.
    Jhunjhunwala favored companies with clean balance sheets and manageable debt.
    """
    if not financial_line_items:
        return {"score": 0, "details": "No balance sheet data"}

    latest = financial_line_items[0]
    score = 0
    reasoning = []

    # Debt to asset ratio
    if (getattr(latest, "total_assets", None) and getattr(latest, "total_liabilities", None) 
        and latest.total_assets and latest.total_liabilities 
        and latest.total_assets > 0):
        debt_ratio = latest.total_liabilities / latest.total_assets
        if debt_ratio < 0.5:
            score += 2
            reasoning.append(f"Low debt ratio: {debt_ratio:.2f}")
        elif debt_ratio < 0.7:
            score += 1
            reasoning.append(f"Moderate debt ratio: {debt_ratio:.2f}")
        else:
            reasoning.append(f"High debt ratio: {debt_ratio:.2f}")
    else:
        reasoning.append("Insufficient data to calculate debt ratio")

    # Current ratio (liquidity)
    if (getattr(latest, "current_assets", None) and getattr(latest, "current_liabilities", None) 
        and latest.current_assets and latest.current_liabilities 
        and latest.current_liabilities > 0):
        current_ratio = latest.current_assets / latest.current_liabilities
        if current_ratio > 2.0:
            score += 2
            reasoning.append(f"Excellent liquidity with current ratio: {current_ratio:.2f}")
        elif current_ratio > 1.5:
            score += 1
            reasoning.append(f"Good liquidity with current ratio: {current_ratio:.2f}")
        else:
            reasoning.append(f"Weak liquidity with current ratio: {current_ratio:.2f}")
    else:
        reasoning.append("Insufficient data to calculate current ratio")

    return {"score": score, "details": "; ".join(reasoning)}

def analyze_cash_flow(financial_line_items: list) -> dict[str, any]:
    """
    Evaluate free cash flow and dividend behavior.
    Jhunjhunwala appreciated companies generating strong free cash flow and rewarding shareholders.
    """
    if not financial_line_items:
        return {"score": 0, "details": "No cash flow data"}

    latest = financial_line_items[0]
    score = 0
    reasoning = []

    # Free cash flow analysis
    if getattr(latest, "free_cash_flow", None) and latest.free_cash_flow:
        if latest.free_cash_flow > 0:
            score += 2
            reasoning.append(f"Positive free cash flow: {latest.free_cash_flow}")
        else:
            reasoning.append(f"Negative free cash flow: {latest.free_cash_flow}")
    else:
        reasoning.append("Free cash flow data not available")

    # Dividend analysis
    if getattr(latest, "dividends_and_other_cash_distributions", None) and latest.dividends_and_other_cash_distributions:
        if latest.dividends_and_other_cash_distributions < 0:  # Negative indicates cash outflow for dividends
            score += 1
            reasoning.append("Company pays dividends to shareholders")
        else:
            reasoning.append("No significant dividend payments")
    else:
        reasoning.append("No dividend payment data available")

    return {"score": score, "details": "; ".join(reasoning)}

def analyze_management_actions(financial_line_items: list) -> dict[str, any]:
    """
    Look at share issuance or buybacks to assess shareholder friendliness.
    Jhunjhunwala liked managements who buy back shares or avoid dilution.
    """
    if not financial_line_items:
        return {"score": 0, "details": "No management action data"}

    latest = financial_line_items[0]
    score = 0
    reasoning = []

    issuance = getattr(latest, "issuance_or_purchase_of_equity_shares", None)
    if issuance is not None:
        if issuance < 0:  # Negative indicates share buybacks
            score += 2
            reasoning.append(f"Company buying back shares: {abs(issuance)}")
        elif issuance > 0:
            reasoning.append(f"Share issuance detected (potential dilution): {issuance}")
        else:
            score += 1
            reasoning.append("No recent share issuance or buyback")
    else:
        reasoning.append("No data on share issuance or buybacks")

    return {"score": score, "details": "; ".join(reasoning)}

def assess_quality_metrics(financial_line_items: list) -> float:
    """
    Assess company quality based on Jhunjhunwala's criteria.
    Returns a score between 0 and 1.
    """
    if not financial_line_items:
        return 0.5  # Neutral score
    
    latest = financial_line_items[0]
    quality_factors = []
    
    # ROE consistency and level
    if (getattr(latest, 'net_income', None) and getattr(latest, 'total_assets', None) and 
        getattr(latest, 'total_liabilities', None) and latest.total_assets and latest.total_liabilities):
        
        shareholders_equity = latest.total_assets - latest.total_liabilities
        if shareholders_equity > 0 and latest.net_income:
            roe = latest.net_income / shareholders_equity
            if roe > 0.20:  # ROE > 20%
                quality_factors.append(1.0)
            elif roe > 0.15:  # ROE > 15%
                quality_factors.append(0.8)
            elif roe > 0.10:  # ROE > 10%
                quality_factors.append(0.6)
            else:
                quality_factors.append(0.3)
        else:
            quality_factors.append(0.0)
    else:
        quality_factors.append(0.5)
    
    # Debt levels (lower is better)
    if (getattr(latest, 'total_assets', None) and getattr(latest, 'total_liabilities', None) and 
        latest.total_assets and latest.total_liabilities):
        debt_ratio = latest.total_liabilities / latest.total_assets
        if debt_ratio < 0.3:  # Low debt
            quality_factors.append(1.0)
        elif debt_ratio < 0.5:  # Moderate debt
            quality_factors.append(0.7)
        elif debt_ratio < 0.7:  # High debt
            quality_factors.append(0.4)
        else:  # Very high debt
            quality_factors.append(0.1)
    else:
        quality_factors.append(0.5)
    
    # Growth consistency
    net_incomes = [getattr(item, "net_income", None) for item in financial_line_items[:4] 
                   if getattr(item, "net_income", None) is not None and getattr(item, "net_income", None) > 0]
    
    if len(net_incomes) >= 3:
        declining_years = sum(1 for i in range(1, len(net_incomes)) if net_incomes[i-1] > net_incomes[i])
        consistency = 1 - (declining_years / (len(net_incomes) - 1))
        quality_factors.append(consistency)
    else:
        quality_factors.append(0.5)
    
    # Return average quality score
    return sum(quality_factors) / len(quality_factors) if quality_factors else 0.5

def rj_calculate_intrinsic_value(financial_line_items: list, market_cap: float) -> float:
    """
    Calculate intrinsic value using Rakesh Jhunjhunwala's approach:
    - Focus on earnings power and growth
    - Conservative discount rates
    - Quality premium for consistent performers
    """
    if not financial_line_items or not market_cap:
        return None
    
    try:
        latest = financial_line_items[0]
        
        # Need positive earnings as base
        if not getattr(latest, 'net_income', None) or latest.net_income <= 0:
            return None
        
        # Get historical earnings for growth calculation
        net_incomes = [getattr(item, "net_income", None) for item in financial_line_items[:5] 
                       if getattr(item, "net_income", None) is not None and getattr(item, "net_income", None) > 0]
        
        if len(net_incomes) < 2:
            # Use current earnings with conservative multiple for stable companies
            return latest.net_income * 12  # Conservative P/E of 12
        
        # Calculate sustainable growth rate using historical data
        initial_income = net_incomes[-1]  # Oldest
        final_income = net_incomes[0]     # Latest
        years = len(net_incomes) - 1
        
        # Calculate historical CAGR
        if initial_income > 0:  # Fixed: Add zero check
            historical_growth = ((final_income / initial_income) ** (1/years) - 1)
        else:
            historical_growth = 0.05  # Default to 5%
        
        # Conservative growth assumptions (Jhunjhunwala style)
        if historical_growth > 0.25:  # Cap at 25% for sustainability
            sustainable_growth = 0.20  # Conservative 20%
        elif historical_growth > 0.15:
            sustainable_growth = historical_growth * 0.8  # 80% of historical
        elif historical_growth > 0.05:
            sustainable_growth = historical_growth * 0.9  # 90% of historical
        else:
            sustainable_growth = 0.05  # Minimum 5% for inflation
        
        # Quality assessment affects discount rate
        quality_score = assess_quality_metrics(financial_line_items)
        
        # Discount rate based on quality (Jhunjhunwala preferred quality)
        if quality_score >= 0.8:  # High quality
            discount_rate = 0.12  # 12% for high quality companies
            terminal_multiple = 18
        elif quality_score >= 0.6:  # Medium quality
            discount_rate = 0.15  # 15% for medium quality
            terminal_multiple = 15
        else:  # Lower quality
            discount_rate = 0.18  # 18% for riskier companies
            terminal_multiple = 12
        
        # Simple DCF with terminal value
        current_earnings = latest.net_income
        terminal_value = 0
        dcf_value = 0
        
        # Project 5 years of earnings
        for year in range(1, 6):
            projected_earnings = current_earnings * ((1 + sustainable_growth) ** year)
            present_value = projected_earnings / ((1 + discount_rate) ** year)
            dcf_value += present_value
        
        # Terminal value (year 5 earnings * terminal multiple)
        year_5_earnings = current_earnings * ((1 + sustainable_growth) ** 5)
        terminal_value = (year_5_earnings * terminal_multiple) / ((1 + discount_rate) ** 5)
        
        total_intrinsic_value = dcf_value + terminal_value
        
        return total_intrinsic_value
        
    except Exception:
        # Fallback to simple earnings multiple
        if getattr(latest, 'net_income', None) and latest.net_income > 0:
            return latest.net_income * 15
        return None

def analyze_rakesh_jhunjhunwala_style(
    financial_line_items: list,
    owner_earnings: float = None,
    intrinsic_value: float = None,
    current_price: float = None,
) -> dict[str, any]:
    """
    Comprehensive analysis in Rakesh Jhunjhunwala's investment style.
    """
    # Run sub-analyses
    profitability = analyze_profitability(financial_line_items)
    growth = analyze_growth(financial_line_items)
    balance_sheet = analyze_balance_sheet(financial_line_items)
    cash_flow = analyze_cash_flow(financial_line_items)
    management = analyze_management_actions(financial_line_items)

    total_score = (
        profitability["score"]
        + growth["score"]
        + balance_sheet["score"]
        + cash_flow["score"]
        + management["score"]
    )

    details = (
        f"Profitability: {profitability['details']}\n"
        f"Growth: {growth['details']}\n"
        f"Balance Sheet: {balance_sheet['details']}\n"
        f"Cash Flow: {cash_flow['details']}\n"
        f"Management Actions: {management['details']}"
    )

    # Use provided intrinsic value or calculate if not provided
    if not intrinsic_value:
        intrinsic_value = calculate_intrinsic_value(financial_line_items, current_price)

    valuation_gap = None
    if intrinsic_value and current_price:
        valuation_gap = intrinsic_value - current_price

    return {
        "total_score": total_score,
        "details": details,
        "owner_earnings": owner_earnings,
        "intrinsic_value": intrinsic_value,
        "current_price": current_price,
        "valuation_gap": valuation_gap,
        "breakdown": {
            "profitability": profitability,
            "growth": growth,
            "balance_sheet": balance_sheet,
            "cash_flow": cash_flow,
            "management": management,
        },
    }


# ==========================
# Aswath Damodaran helpers
# ==========================

def analyze_growth_and_reinvestment(metrics: list, line_items: list) -> dict[str, any]:
    """
    Growth score (0-4):
      +2  5-yr CAGR of revenue > 8 %
      +1  5-yr CAGR of revenue > 3 %
      +1  Positive FCFF growth over 5 yr
    Reinvestment efficiency (ROIC > WACC) adds +1
    """
    max_score = 4
    if len(metrics) < 2:
        return {"score": 0, "max_score": max_score, "details": "Insufficient history"}

    # Revenue CAGR (oldest to latest)
    revs = [m.revenue for m in reversed(metrics) if hasattr(m, "revenue") and m.revenue]
    if len(revs) >= 2 and revs[0] > 0:
        cagr = (revs[-1] / revs[0]) ** (1 / (len(revs) - 1)) - 1
    else:
        cagr = None

    score, details = 0, []

    if cagr is not None:
        if cagr > 0.08:
            score += 2
            details.append(f"Revenue CAGR {cagr:.1%} (> 8 %)")
        elif cagr > 0.03:
            score += 1
            details.append(f"Revenue CAGR {cagr:.1%} (> 3 %)")
        else:
            details.append(f"Sluggish revenue CAGR {cagr:.1%}")
    else:
        details.append("Revenue data incomplete")

    # FCFF growth (proxy: free_cash_flow trend)
    fcfs = [li.free_cash_flow for li in reversed(line_items) if li.free_cash_flow]
    if len(fcfs) >= 2 and fcfs[-1] > fcfs[0]:
        score += 1
        details.append("Positive FCFF growth")
    else:
        details.append("Flat or declining FCFF")

    # Reinvestment efficiency (ROIC vs. 10 % hurdle)
    latest = metrics[0]
    if latest.return_on_invested_capital and latest.return_on_invested_capital > 0.10:
        score += 1
        details.append(f"ROIC {latest.return_on_invested_capital:.1%} (> 10 %)")

    return {"score": score, "max_score": max_score, "details": "; ".join(details), "metrics": latest.model_dump()}

def analyze_risk_profile(metrics: list, line_items: list) -> dict[str, any]:
    """
    Risk score (0-3):
      +1  Beta < 1.3
      +1  Debt/Equity < 1
      +1  Interest Coverage > 3×
    """
    max_score = 3
    if not metrics:
        return {"score": 0, "max_score": max_score, "details": "No metrics"}

    latest = metrics[0]
    score, details = 0, []

    # Beta
    beta = getattr(latest, "beta", None)
    if beta is not None:
        if beta < 1.3:
            score += 1
            details.append(f"Beta {beta:.2f}")
        else:
            details.append(f"High beta {beta:.2f}")
    else:
        details.append("Beta NA")

    # Debt / Equity
    dte = getattr(latest, "debt_to_equity", None)
    if dte is not None:
        if dte < 1:
            score += 1
            details.append(f"D/E {dte:.1f}")
        else:
            details.append(f"High D/E {dte:.1f}")
    else:
        details.append("D/E NA")

    # Interest coverage
    ebit = getattr(latest, "ebit", None)
    interest = getattr(latest, "interest_expense", None)
    if ebit and interest and interest != 0:
        coverage = ebit / abs(interest)
        if coverage > 3:
            score += 1
            details.append(f"Interest coverage × {coverage:.1f}")
        else:
            details.append(f"Weak coverage × {coverage:.1f}")
    else:
        details.append("Interest coverage NA")

    # Compute cost of equity for later use
    cost_of_equity = estimate_cost_of_equity(beta)

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "beta": beta,
        "cost_of_equity": cost_of_equity,
    }

def analyze_relative_valuation(metrics: list) -> dict[str, any]:
    """
    Simple PE check vs. historical median (proxy since sector comps unavailable):
      +1 if TTM P/E < 70 % of 5-yr median
      +0 if between 70 %-130 %
      ‑1 if >130 %
    """
    max_score = 1
    if not metrics or len(metrics) < 5:
        return {"score": 0, "max_score": max_score, "details": "Insufficient P/E history"}

    pes = [m.price_to_earnings_ratio for m in metrics if m.price_to_earnings_ratio]
    if len(pes) < 5:
        return {"score": 0, "max_score": max_score, "details": "P/E data sparse"}

    ttm_pe = pes[0]
    median_pe = sorted(pes)[len(pes) // 2]

    if ttm_pe < 0.7 * median_pe:
        score, desc = 1, f"P/E {ttm_pe:.1f} vs. median {median_pe:.1f} (cheap)"
    elif ttm_pe > 1.3 * median_pe:
        score, desc = -1, f"P/E {ttm_pe:.1f} vs. median {median_pe:.1f} (expensive)"
    else:
        score, desc = 0, f"P/E inline with history"

    return {"score": score, "max_score": max_score, "details": desc}

def calculate_intrinsic_value_dcf(metrics: list, line_items: list, risk_analysis: dict) -> dict[str, any]:
    """
    FCFF DCF with:
      • Base FCFF = latest free cash flow
      • Growth = 5-yr revenue CAGR (capped 12 %)
      • Fade linearly to terminal growth 2.5 % by year 10
      • Discount @ cost of equity (no debt split given data limitations)
    """
    if not metrics or len(metrics) < 2 or not line_items:
        return {"intrinsic_value": None, "details": ["Insufficient data"]}

    latest_m = metrics[0]
    fcff0 = getattr(latest_m, "free_cash_flow", None)
    shares = getattr(line_items[0], "outstanding_shares", None)
    if not fcff0 or not shares:
        return {"intrinsic_value": None, "details": ["Missing FCFF or share count"]}

    # Growth assumptions
    revs = [m.revenue for m in reversed(metrics) if m.revenue]
    if len(revs) >= 2 and revs[0] > 0:
        base_growth = min((revs[-1] / revs[0]) ** (1 / (len(revs) - 1)) - 1, 0.12)
    else:
        base_growth = 0.04  # fallback

    terminal_growth = 0.025
    years = 10

    # Discount rate
    discount = risk_analysis.get("cost_of_equity") or 0.09

    # Project FCFF and discount
    pv_sum = 0.0
    g = base_growth
    g_step = (terminal_growth - base_growth) / (years - 1)
    for yr in range(1, years + 1):
        fcff_t = fcff0 * (1 + g)
        pv = fcff_t / (1 + discount) ** yr
        pv_sum += pv
        g += g_step

    # Terminal value (perpetuity with terminal growth)
    tv = (
        fcff0
        * (1 + terminal_growth)
        / (discount - terminal_growth)
        / (1 + discount) ** years
    )

    equity_value = pv_sum + tv
    intrinsic_per_share = equity_value / shares

    return {
        "intrinsic_value": equity_value,
        "intrinsic_per_share": intrinsic_per_share,
        "assumptions": {
            "base_fcff": fcff0,
            "base_growth": base_growth,
            "terminal_growth": terminal_growth,
            "discount_rate": discount,
            "projection_years": years,
        },
        "details": ["FCFF DCF completed"],
    }

def estimate_cost_of_equity(beta: float | None) -> float:
    """CAPM: r_e = r_f + β × ERP (use Damodaran's long-term averages)."""
    risk_free = 0.04          # 10-yr US Treasury proxy
    erp = 0.05                # long-run US equity risk premium
    beta = beta if beta is not None else 1.0
    return risk_free + beta * erp


# ==========================
# Growth Agent helpers
# ==========================

def _calculate_trend(data: list[float | None]) -> float:
    """Calculates the slope of the trend line for the given data."""
    clean_data = [d for d in data if d is not None]
    if len(clean_data) < 2:
        return 0.0
    
    y = clean_data
    x = list(range(len(y)))
    
    try:
        # Simple linear regression
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(i * j for i, j in zip(x, y))
        sum_x2 = sum(i**2 for i in x)
        n = len(y)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        return slope
    except ZeroDivisionError:
        return 0.0

def analyze_growth_trends(metrics: list) -> dict:
    """Analyzes historical growth trends."""
    
    rev_growth = [m.revenue_growth for m in metrics]
    eps_growth = [m.earnings_per_share_growth for m in metrics]
    fcf_growth = [m.free_cash_flow_growth for m in metrics]

    rev_trend = _calculate_trend(rev_growth)
    eps_trend = _calculate_trend(eps_growth)
    fcf_trend = _calculate_trend(fcf_growth)

    # Score based on recent growth and trend
    score = 0
    
    # Revenue
    if rev_growth[0] is not None:
        if rev_growth[0] > 0.20:
            score += 0.4
        elif rev_growth[0] > 0.10:
            score += 0.2
        if rev_trend > 0:
            score += 0.1 # Accelerating
            
    # EPS
    if eps_growth[0] is not None:
        if eps_growth[0] > 0.20:
            score += 0.25
        elif eps_growth[0] > 0.10:
            score += 0.1
        if eps_trend > 0:
            score += 0.05
    
    # FCF
    if fcf_growth[0] is not None:
        if fcf_growth[0] > 0.15:
            score += 0.1
            
    score = min(score, 1.0)

    return {
        "score": score,
        "revenue_growth": rev_growth[0],
        "revenue_trend": rev_trend,
        "eps_growth": eps_growth[0],
        "eps_trend": eps_trend,
        "fcf_growth": fcf_growth[0],
        "fcf_trend": fcf_trend
    }

def ga_analyze_valuation(metrics) -> dict:
    """Analyzes valuation from a growth perspective."""
    
    peg_ratio = metrics.peg_ratio
    ps_ratio = metrics.price_to_sales_ratio
    
    score = 0
    
    # PEG Ratio
    if peg_ratio is not None:
        if peg_ratio < 1.0:
            score += 0.5
        elif peg_ratio < 2.0:
            score += 0.25
            
    # Price to Sales Ratio
    if ps_ratio is not None:
        if ps_ratio < 2.0:
            score += 0.5
        elif ps_ratio < 5.0:
            score += 0.25
            
    score = min(score, 1.0)
    
    return {
        "score": score,
        "peg_ratio": peg_ratio,
        "price_to_sales_ratio": ps_ratio
    }

def analyze_margin_trends(metrics: list) -> dict:
    """Analyzes historical margin trends."""
    
    gross_margins = [m.gross_margin for m in metrics]
    operating_margins = [m.operating_margin for m in metrics]
    net_margins = [m.net_margin for m in metrics]

    gm_trend = _calculate_trend(gross_margins)
    om_trend = _calculate_trend(operating_margins)
    nm_trend = _calculate_trend(net_margins)
    
    score = 0
    
    # Gross Margin
    if gross_margins[0] is not None:
        if gross_margins[0] > 0.5: # Healthy margin
            score += 0.2
        if gm_trend > 0: # Expanding
            score += 0.2

    # Operating Margin
    if operating_margins[0] is not None:
        if operating_margins[0] > 0.15: # Healthy margin
            score += 0.2
        if om_trend > 0: # Expanding
            score += 0.2
            
    # Net Margin Trend
    if nm_trend > 0:
        score += 0.2
        
    score = min(score, 1.0)
    
    return {
        "score": score,
        "gross_margin": gross_margins[0],
        "gross_margin_trend": gm_trend,
        "operating_margin": operating_margins[0],
        "operating_margin_trend": om_trend,
        "net_margin": net_margins[0],
        "net_margin_trend": nm_trend
    }

def analyze_insider_conviction(trades: list) -> dict:
    """Analyzes insider trading activity."""
    
    buys = sum(t.transaction_value for t in trades if t.transaction_value and t.transaction_shares > 0)
    sells = sum(abs(t.transaction_value) for t in trades if t.transaction_value and t.transaction_shares < 0)
    
    if (buys + sells) == 0:
        net_flow_ratio = 0
    else:
        net_flow_ratio = (buys - sells) / (buys + sells)
    
    score = 0
    if net_flow_ratio > 0.5:
        score = 1.0
    elif net_flow_ratio > 0.1:
        score = 0.7
    elif net_flow_ratio > -0.1:
        score = 0.5 # Neutral
    else:
        score = 0.2
        
    return {
        "score": score,
        "net_flow_ratio": net_flow_ratio,
        "buys": buys,
        "sells": sells
    }

def check_financial_health(metrics) -> dict:
    """Checks the company's financial health."""
    
    debt_to_equity = metrics.debt_to_equity
    current_ratio = metrics.current_ratio
    
    score = 1.0
    
    # Debt to Equity
    if debt_to_equity is not None:
        if debt_to_equity > 1.5:
            score -= 0.5
        elif debt_to_equity > 0.8:
            score -= 0.2
            
    # Current Ratio
    if current_ratio is not None:
        if current_ratio < 1.0:
            score -= 0.5
        elif current_ratio < 1.5:
            score -= 0.2
            
    score = max(score, 0.0)
    
    return {
        "score": score,
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio
    }


# ==========================
# News Sentiment helpers
# ==========================

def _calculate_confidence_score(
    sentiment_confidences: dict,
    company_news: list,
    overall_signal: str,
    bullish_signals: int,
    bearish_signals: int,
    total_signals: int
) -> float:
    """
    Calculate confidence score for a sentiment signal.
    
    Uses a weighted approach combining LLM confidence scores (70%) with 
    signal proportion (30%) when LLM classifications are available.
    
    Args:
        sentiment_confidences: Dictionary mapping news article IDs to confidence scores.
        company_news: List of CompanyNews objects.
        overall_signal: The overall sentiment signal ("bullish", "bearish", or "neutral").
        bullish_signals: Count of bullish signals.
        bearish_signals: Count of bearish signals.
        total_signals: Total number of signals.
        
    Returns:
        Confidence score as a float between 0 and 100.
    """
    if total_signals == 0:
        return 0.0
    
    # Calculate weighted confidence using LLM confidence scores when available
    if sentiment_confidences:
        # Get articles that match the overall signal
        matching_articles = [
            news for news in company_news 
            if news.sentiment and (
                (overall_signal == "bullish" and news.sentiment == "positive") or
                (overall_signal == "bearish" and news.sentiment == "negative") or
                (overall_signal == "neutral" and news.sentiment == "neutral")
            )
        ]
        
        # Calculate average confidence from LLM-classified articles that match the signal
        llm_confidences = [
            sentiment_confidences[id(news)] 
            for news in matching_articles 
            if id(news) in sentiment_confidences
        ]
        
        if llm_confidences:
            # Weight: 70% from LLM confidence scores, 30% from signal proportion
            avg_llm_confidence = sum(llm_confidences) / len(llm_confidences)
            signal_proportion = (max(bullish_signals, bearish_signals) / total_signals) * 100
            return round(0.7 * avg_llm_confidence + 0.3 * signal_proportion, 2)
    
    # Fallback to proportion-based confidence
    return round((max(bullish_signals, bearish_signals) / total_signals) * 100, 2)

