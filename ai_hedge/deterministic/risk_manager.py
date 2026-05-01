from langchain_core.messages import HumanMessage
from ai_hedge.data.api import get_prices, prices_to_df, get_current_price
from ai_hedge.data.earnings_calendar import days_until_next_earnings
import json
import numpy as np
import pandas as pd

# Reject any candidate trade whose next earnings is within this many calendar
# days. Earnings cause 5–15% overnight moves unrelated to technical analysis,
# so the system skips trades inside the blackout window. Post-earnings is fine
# (the move already happened).
EARNINGS_BLACKOUT_DAYS = 3

# Sin #10 hard correlation cap. The risk_manager already builds a correlation
# matrix; before this fix it was used only as a soft sizing multiplier, so
# the PM could go long JPM + BAC + GS + WFC and pretend that was four
# diversified trades when it was really one bet on banks. Now: any candidate
# whose absolute correlation with any existing position exceeds the
# threshold is hard-rejected, and any single correlation cluster is capped
# at this percent of total portfolio value.
MAX_CORRELATION_THRESHOLD = 0.7
MAX_CLUSTER_EXPOSURE_PCT = 0.30

# Stub for compatibility - full AgentState not needed for deterministic agents
AgentState = dict
def show_agent_reasoning(output, agent_name):
    import json
    print(f"\n{'=' * 10} {agent_name.center(28)} {'=' * 10}")
    if isinstance(output, (dict, list)):
        print(json.dumps(output, indent=2, default=str))
    else:
        print(output)
    print("=" * 48)

class _NoopProgress:
    def update_status(self, *args, **kwargs): pass
progress = _NoopProgress()

def get_api_key_from_state(state, key_name): return None


##### Risk Management Agent #####
def risk_management_agent(state: AgentState, agent_id: str = "risk_management_agent"):
    """Controls position sizing based on volatility-adjusted risk factors for multiple tickers."""
    portfolio = state["data"]["portfolio"]
    data = state["data"]
    tickers = data["tickers"]
    asset_type = data.get("asset_type", "stock")
    api_key = get_api_key_from_state(state, "FINANCIAL_DATASETS_API_KEY")

    # Sin #9: pre-flight earnings blackout. Crypto tickers don't have earnings
    # so the check is skipped wholesale for them.
    earnings_blackout: dict[str, int] = {}
    if asset_type != "crypto":
        for ticker in tickers:
            days = days_until_next_earnings(ticker)
            if days is not None and 0 <= days <= EARNINGS_BLACKOUT_DAYS:
                earnings_blackout[ticker] = days
                print(f"[earnings blackout] {ticker} skipped — earnings in {days} days")

    # Initialize risk analysis for each ticker
    risk_analysis = {}
    current_prices = {}  # Store prices here to avoid redundant API calls
    volatility_data = {}  # Store volatility metrics
    returns_by_ticker: dict[str, pd.Series] = {}  # For correlation analysis

    # First, fetch prices and calculate volatility for all relevant tickers.
    # Include open-but-not-analyzed tickers (other_positions) so we can
    # correlation-check against them — without this, BAC vs JPM would be
    # invisible whenever JPM isn't in today's run.
    all_tickers = set(tickers) | set(portfolio.get("positions", {}).keys())
    for _p in portfolio.get("other_positions", []) or []:
        _tk = (_p.get("ticker") or "").upper()
        if _tk:
            all_tickers.add(_tk)

    for ticker in all_tickers:
        progress.update_status(agent_id, ticker, "Fetching price data and calculating volatility")

        prices = get_prices(
            ticker=ticker,
            start_date=data["start_date"],
            end_date=data["end_date"],
            api_key=api_key,
        )

        if not prices:
            progress.update_status(agent_id, ticker, "Warning: No price data found")
            volatility_data[ticker] = {
                "daily_volatility": 0.05,  # Default fallback volatility (5% daily)
                "annualized_volatility": 0.05 * np.sqrt(252),
                "volatility_percentile": 100,  # Assume high risk if no data
                "data_points": 0
            }
            continue

        prices_df = prices_to_df(prices)

        if not prices_df.empty and len(prices_df) > 1:
            # Prefer real-time price over yesterday's close
            realtime = get_current_price(ticker)
            current_price = realtime if realtime else prices_df["close"].iloc[-1]
            current_prices[ticker] = current_price

            # Calculate volatility metrics
            volatility_metrics = calculate_volatility_metrics(prices_df)
            volatility_data[ticker] = volatility_metrics

            # Store returns for correlation analysis (use close-to-close returns)
            daily_returns = prices_df["close"].pct_change().dropna()
            if len(daily_returns) > 0:
                returns_by_ticker[ticker] = daily_returns

            progress.update_status(
                agent_id,
                ticker,
                f"Price: {current_price:.2f}, Ann. Vol: {volatility_metrics['annualized_volatility']:.1%}"
            )
        else:
            progress.update_status(agent_id, ticker, "Warning: Insufficient price data")
            current_prices[ticker] = 0
            volatility_data[ticker] = {
                "daily_volatility": 0.05,
                "annualized_volatility": 0.05 * np.sqrt(252),
                "volatility_percentile": 100,
                "data_points": len(prices_df) if not prices_df.empty else 0
            }

    # Build returns DataFrame aligned across tickers for correlation analysis
    correlation_matrix = None
    if len(returns_by_ticker) >= 2:
        try:
            returns_df = pd.DataFrame(returns_by_ticker).dropna(how="any")
            if returns_df.shape[1] >= 2 and returns_df.shape[0] >= 5:
                correlation_matrix = returns_df.corr()
        except Exception:
            correlation_matrix = None

    # Determine which tickers currently have exposure (non-zero absolute position)
    active_positions = {
        t for t, pos in portfolio.get("positions", {}).items()
        if abs(pos.get("long", 0) - pos.get("short", 0)) > 0
    }

    # Calculate total portfolio value based on current market prices (Net Liquidation Value)
    total_portfolio_value = portfolio.get("cash", 0.0)

    for ticker, position in portfolio.get("positions", {}).items():
        if ticker in current_prices:
            # Add market value of long positions
            total_portfolio_value += position.get("long", 0) * current_prices[ticker]
            # Subtract market value of short positions
            total_portfolio_value -= position.get("short", 0) * current_prices[ticker]

    progress.update_status(agent_id, None, f"Total portfolio value: {total_portfolio_value:.2f}")

    # Sin #10: build a single map of every existing-position ticker → dollar
    # exposure. Used by both the per-candidate correlation rejection and the
    # cluster-cap pass. Combines analyzed-this-run positions (qty != 0) and
    # other_positions (open positions in tickers NOT analyzed today).
    existing_exposures: dict[str, float] = {}
    for _tk, _pos in portfolio.get("positions", {}).items():
        _net = float(_pos.get("long", 0) or 0) - float(_pos.get("short", 0) or 0)
        if _net != 0 and _tk in current_prices and current_prices[_tk] > 0:
            existing_exposures[_tk] = abs(_net) * current_prices[_tk]
    for _p in portfolio.get("other_positions", []) or []:
        _tk = (_p.get("ticker") or "").upper()
        if not _tk:
            continue
        _qty = float(_p.get("quantity", 0) or 0)
        _fill = float(_p.get("entry_fill_price") or _p.get("entry_price") or 0)
        # Mark-to-market when we have a current price; fall back to fill price.
        _px = current_prices.get(_tk) or _fill
        if _qty > 0 and _px > 0:
            existing_exposures[_tk] = existing_exposures.get(_tk, 0.0) + _qty * _px

    # Sin #10 per-candidate correlation rejection: any candidate whose
    # |correlation| with any existing position exceeds MAX_CORRELATION_THRESHOLD
    # is hard-rejected. Computed up front so the loop just looks it up.
    correlation_blocked: dict[str, dict] = {}
    if correlation_matrix is not None:
        for _t in tickers:
            if _t in earnings_blackout:
                continue
            if _t not in correlation_matrix.columns:
                continue
            worst: tuple[str, float, float] | None = None  # (held, abs_corr, raw)
            for _held in existing_exposures.keys():
                if _held == _t or _held not in correlation_matrix.columns:
                    continue
                try:
                    _c = correlation_matrix.loc[_t, _held]
                except KeyError:
                    continue
                if pd.isna(_c):
                    continue
                _ac = abs(float(_c))
                if _ac >= MAX_CORRELATION_THRESHOLD and (worst is None or _ac > worst[1]):
                    worst = (_held, _ac, float(_c))
            if worst is not None:
                _held, _ac, _raw = worst
                correlation_blocked[_t] = {
                    "blocking_ticker": _held,
                    "correlation": _raw,
                    "abs_correlation": _ac,
                    "threshold": MAX_CORRELATION_THRESHOLD,
                }
                print(
                    f"[correlation cap] {_t} skipped — "
                    f"{_ac:.2f} correlated with {_held} (already long)"
                )

    # Calculate volatility- and correlation-adjusted risk limits for each ticker
    for ticker in tickers:
        progress.update_status(agent_id, ticker, "Calculating volatility- and correlation-adjusted limits")

        # Sin #9: hard-reject candidates inside the earnings blackout window.
        if ticker in earnings_blackout:
            days = earnings_blackout[ticker]
            risk_analysis[ticker] = {
                "remaining_position_limit": 0.0,
                "current_price": float(current_prices.get(ticker, 0.0)),
                "earnings_blackout": {
                    "days_to_next_earnings": int(days),
                    "blackout_window_days": EARNINGS_BLACKOUT_DAYS,
                },
                "reasoning": {
                    "rejected": f"earnings in {days} days",
                    "earnings_blackout_window": EARNINGS_BLACKOUT_DAYS,
                },
            }
            progress.update_status(agent_id, ticker, f"Rejected: earnings in {days} days")
            continue

        # Sin #10: hard-reject candidates correlated > threshold with any
        # existing position. Runs AFTER earnings blackout, BEFORE sizing.
        if ticker in correlation_blocked:
            info = correlation_blocked[ticker]
            risk_analysis[ticker] = {
                "remaining_position_limit": 0.0,
                "current_price": float(current_prices.get(ticker, 0.0)),
                "correlation_blocked": True,
                "correlation_block_reason": (
                    f"{info['abs_correlation']*100:.0f}% correlated with "
                    f"{info['blocking_ticker']}"
                ),
                "reasoning": {
                    "rejected": "correlation cap",
                    "blocking_ticker": info["blocking_ticker"],
                    "correlation": info["correlation"],
                    "abs_correlation": info["abs_correlation"],
                    "threshold": MAX_CORRELATION_THRESHOLD,
                },
            }
            progress.update_status(
                agent_id,
                ticker,
                f"Rejected: correlated with {info['blocking_ticker']}",
            )
            continue

        if ticker not in current_prices or current_prices[ticker] <= 0:
            progress.update_status(agent_id, ticker, "Failed: No valid price data")
            risk_analysis[ticker] = {
                "remaining_position_limit": 0.0,
                "current_price": 0.0,
                "reasoning": {
                    "error": "Missing price data for risk calculation"
                }
            }
            continue

        current_price = current_prices[ticker]
        vol_data = volatility_data.get(ticker, {})

        # Calculate current market value of this position
        position = portfolio.get("positions", {}).get(ticker, {})
        long_value = position.get("long", 0) * current_price
        short_value = position.get("short", 0) * current_price
        current_position_value = abs(long_value - short_value)  # Use absolute exposure

        # Volatility-adjusted limit pct
        vol_adjusted_limit_pct = calculate_volatility_adjusted_limit(
            vol_data.get("annualized_volatility", 0.25)
        )

        # Correlation adjustment
        corr_metrics = {
            "avg_correlation_with_active": None,
            "max_correlation_with_active": None,
            "top_correlated_tickers": [],
        }
        corr_multiplier = 1.0
        if correlation_matrix is not None and ticker in correlation_matrix.columns:
            # Compute correlations with active positions (exclude self)
            comparable = [t for t in active_positions if t in correlation_matrix.columns and t != ticker]
            if not comparable:
                # If no active positions, compare with all other available tickers
                comparable = [t for t in correlation_matrix.columns if t != ticker]
            if comparable:
                series = correlation_matrix.loc[ticker, comparable]
                # Drop NaNs just in case
                series = series.dropna()
                if len(series) > 0:
                    avg_corr = float(series.mean())
                    max_corr = float(series.max())
                    corr_metrics["avg_correlation_with_active"] = avg_corr
                    corr_metrics["max_correlation_with_active"] = max_corr
                    # Top 3 most correlated tickers
                    top_corr = series.sort_values(ascending=False).head(3)
                    corr_metrics["top_correlated_tickers"] = [
                        {"ticker": idx, "correlation": float(val)} for idx, val in top_corr.items()
                    ]
                    corr_multiplier = calculate_correlation_multiplier(avg_corr)

        # NEW: Conviction-based sizing.
        # Volatility scaling is no longer used to throttle position size — the PM
        # decides conviction and account_risk_pct itself, then sizes by
        # quantity = (capital × risk_pct) / abs(entry - stop).
        # The risk manager's job is to enforce two hard caps and pass through
        # context (volatility, correlation) for the PM to consider qualitatively.

        MAX_POSITION_PCT = 0.30   # No single position > 30% of capital
        MAX_ACCOUNT_RISK_PCT = 2.5  # No single trade can risk > 2.5% of capital if stopped out

        max_position_dollars = total_portfolio_value * MAX_POSITION_PCT
        max_account_risk_dollars = total_portfolio_value * (MAX_ACCOUNT_RISK_PCT / 100.0)
        # Account for currently held value in this ticker — same hard cap applies to total exposure
        remaining_position_dollars = max(0.0, max_position_dollars - current_position_value)
        remaining_position_dollars = min(remaining_position_dollars, portfolio.get("cash", 0))

        risk_analysis[ticker] = {
            "remaining_position_limit": float(remaining_position_dollars),  # 30% hard cap, kept for compatibility
            "max_account_risk_pct": float(MAX_ACCOUNT_RISK_PCT),
            "max_account_risk_dollars": float(max_account_risk_dollars),
            "max_position_pct": float(MAX_POSITION_PCT),
            "current_price": float(current_price),
            "volatility_metrics": {
                "daily_volatility": float(vol_data.get("daily_volatility", 0.05)),
                "annualized_volatility": float(vol_data.get("annualized_volatility", 0.25)),
                "volatility_percentile": float(vol_data.get("volatility_percentile", 100)),
                "data_points": int(vol_data.get("data_points", 0))
            },
            "correlation_metrics": corr_metrics,
            "reasoning": {
                "portfolio_value": float(total_portfolio_value),
                "current_position_value": float(current_position_value),
                "available_cash": float(portfolio.get("cash", 0)),
                "max_position_pct": float(MAX_POSITION_PCT),
                "max_position_dollars": float(max_position_dollars),
                "max_account_risk_pct": float(MAX_ACCOUNT_RISK_PCT),
                "max_account_risk_dollars": float(max_account_risk_dollars),
                "sizing_model": (
                    f"PM picks conviction + account_risk_pct (≤{MAX_ACCOUNT_RISK_PCT}%); "
                    f"qty = (capital × risk_pct) / |entry - stop|. "
                    f"Hard cap: position ≤ {MAX_POSITION_PCT:.0%} of capital "
                    f"(${max_position_dollars:,.0f}). "
                    f"Vol/correlation are context for PM to consider qualitatively."
                ),
            },
        }

        progress.update_status(
            agent_id,
            ticker,
            f"Adj. limit: {combined_limit_pct:.1%}, Available: ${max_position_size:.0f}"
        )

    # Sin #10 cluster cap: even if no single pair crosses the threshold, a
    # basket of moderately-correlated tickers can still concentrate risk.
    # Group existing + accepted candidates into clusters at the threshold;
    # for any cluster whose total proposed exposure exceeds the cluster cap,
    # drop the latest accepted candidates until it fits. We never drop
    # already-filled (existing) positions — those are sunk capital.
    if correlation_matrix is not None and total_portfolio_value > 0:
        cluster_cap_dollars = MAX_CLUSTER_EXPOSURE_PCT * total_portfolio_value
        clusters = _correlation_clusters(correlation_matrix, MAX_CORRELATION_THRESHOLD)
        # Acceptance order = order of `tickers` argument
        accepted_candidates = [
            t for t in tickers
            if t in risk_analysis
            and float(risk_analysis[t].get("remaining_position_limit", 0.0)) > 0
        ]
        for cluster in clusters:
            if len(cluster) <= 1:
                continue
            existing_in_cluster = sum(
                existing_exposures.get(t, 0.0) for t in cluster
            )
            cluster_candidates = [t for t in accepted_candidates if t in cluster]
            candidate_exposure = sum(
                float(risk_analysis[t]["remaining_position_limit"])
                for t in cluster_candidates
            )
            total_cluster_exposure = existing_in_cluster + candidate_exposure
            if total_cluster_exposure <= cluster_cap_dollars:
                continue
            # Drop latest candidates first (LIFO) until cluster fits.
            for t in reversed(cluster_candidates):
                if total_cluster_exposure <= cluster_cap_dollars:
                    break
                dropped = float(risk_analysis[t]["remaining_position_limit"])
                risk_analysis[t]["remaining_position_limit"] = 0.0
                risk_analysis[t]["correlation_blocked"] = True
                risk_analysis[t]["correlation_block_reason"] = (
                    f"cluster cap: {sorted(cluster)} exposure "
                    f"${total_cluster_exposure:,.0f} > "
                    f"{MAX_CLUSTER_EXPOSURE_PCT*100:.0f}% of "
                    f"${total_portfolio_value:,.0f}"
                )
                _reasoning = risk_analysis[t].setdefault("reasoning", {})
                _reasoning["cluster_capped"] = True
                _reasoning["cluster_members"] = sorted(cluster)
                _reasoning["cluster_cap_pct"] = MAX_CLUSTER_EXPOSURE_PCT
                _reasoning["cluster_exposure_before_drop"] = float(total_cluster_exposure)
                total_cluster_exposure -= dropped
                print(
                    f"[correlation cap] {t} skipped — cluster cap "
                    f"({sorted(cluster)}) > {MAX_CLUSTER_EXPOSURE_PCT*100:.0f}%"
                )

    progress.update_status(agent_id, None, "Done")

    message = HumanMessage(
        content=json.dumps(risk_analysis),
        name=agent_id,
    )

    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(risk_analysis, "Volatility-Adjusted Risk Management Agent")

    # Add the signal to the analyst_signals list
    state["data"]["analyst_signals"][agent_id] = risk_analysis

    return {
        "messages": state.get("messages", []) + [message],
        "data": data,
    }


def calculate_volatility_metrics(prices_df: pd.DataFrame, lookback_days: int = 60) -> dict:
    """Calculate comprehensive volatility metrics from price data."""
    if len(prices_df) < 2:
        return {
            "daily_volatility": 0.05,
            "annualized_volatility": 0.05 * np.sqrt(252),
            "volatility_percentile": 100,
            "data_points": len(prices_df)
        }

    # Calculate daily returns
    daily_returns = prices_df["close"].pct_change().dropna()

    if len(daily_returns) < 2:
        return {
            "daily_volatility": 0.05,
            "annualized_volatility": 0.05 * np.sqrt(252),
            "volatility_percentile": 100,
            "data_points": len(daily_returns)
        }

    # Use the most recent lookback_days for volatility calculation
    recent_returns = daily_returns.tail(min(lookback_days, len(daily_returns)))

    # Calculate volatility metrics
    daily_vol = recent_returns.std()
    annualized_vol = daily_vol * np.sqrt(252)  # Annualize assuming 252 trading days

    # Calculate percentile rank of recent volatility vs historical volatility
    if len(daily_returns) >= 30:  # Need sufficient history for percentile calculation
        # Calculate 30-day rolling volatility for the full history
        rolling_vol = daily_returns.rolling(window=30).std().dropna()
        if len(rolling_vol) > 0:
            # Compare current volatility against historical rolling volatilities
            current_vol_percentile = (rolling_vol <= daily_vol).mean() * 100
        else:
            current_vol_percentile = 50  # Default to median
    else:
        current_vol_percentile = 50  # Default to median if insufficient data

    return {
        "daily_volatility": float(daily_vol) if not np.isnan(daily_vol) else 0.025,
        "annualized_volatility": float(annualized_vol) if not np.isnan(annualized_vol) else 0.25,
        "volatility_percentile": float(current_vol_percentile) if not np.isnan(current_vol_percentile) else 50.0,
        "data_points": len(recent_returns)
    }


def calculate_volatility_adjusted_limit(annualized_volatility: float) -> float:
    """
    Calculate position limit as percentage of portfolio based on volatility.

    Logic:
    - Low volatility (<15%): Up to 25% allocation
    - Medium volatility (15-30%): 15-20% allocation
    - High volatility (>30%): 10-15% allocation
    - Very high volatility (>50%): Max 10% allocation
    """
    base_limit = 0.20  # 20% baseline

    if annualized_volatility < 0.15:  # Low volatility
        # Allow higher allocation for stable stocks
        vol_multiplier = 1.25  # Up to 25%
    elif annualized_volatility < 0.30:  # Medium volatility
        # Standard allocation with slight adjustment based on volatility
        vol_multiplier = 1.0 - (annualized_volatility - 0.15) * 0.5  # 20% -> 12.5%
    elif annualized_volatility < 0.50:  # High volatility
        # Reduce allocation significantly
        vol_multiplier = 0.75 - (annualized_volatility - 0.30) * 0.5  # 15% -> 5%
    else:  # Very high volatility (>50%)
        # Minimum allocation for very risky stocks
        vol_multiplier = 0.50  # Max 10%

    # Apply bounds to ensure reasonable limits
    vol_multiplier = max(0.25, min(1.25, vol_multiplier))  # 5% to 25% range

    return base_limit * vol_multiplier


def calculate_correlation_multiplier(avg_correlation: float) -> float:
    """Map average correlation to an adjustment multiplier.
    - Very high correlation (>= 0.8): reduce limit sharply (0.7x)
    - High correlation (0.6-0.8): reduce (0.85x)
    - Moderate correlation (0.4-0.6): neutral (1.0x)
    - Low correlation (0.2-0.4): slight increase (1.05x)
    - Very low correlation (< 0.2): increase (1.10x)
    """
    if avg_correlation >= 0.80:
        return 0.70
    if avg_correlation >= 0.60:
        return 0.85
    if avg_correlation >= 0.40:
        return 1.00
    if avg_correlation >= 0.20:
        return 1.05
    return 1.10

def _correlation_clusters(correlation_matrix, threshold: float) -> list[set[str]]:
    """Group tickers into single-linkage clusters by absolute correlation.

    Two tickers belong to the same cluster iff there exists a chain of
    pairwise |correlation| >= threshold connections between them. Returns a
    list of sets, one per connected component. Tickers that don't strongly
    correlate with anyone come back as singleton clusters. Single-linkage
    (rather than complete-linkage) is correct here: if A↔B and B↔C are both
    above the threshold, A and C share a risk factor through B even if their
    direct correlation is moderate. Concentration risk follows the chain.
    """
    if correlation_matrix is None:
        return []
    try:
        empty = correlation_matrix.empty
    except AttributeError:
        empty = False
    if empty:
        return []

    tickers = list(correlation_matrix.columns)
    parent = {t: t for t in tickers}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i, a in enumerate(tickers):
        for b in tickers[i + 1:]:
            try:
                c = correlation_matrix.loc[a, b]
            except KeyError:
                continue
            if pd.isna(c):
                continue
            if abs(float(c)) >= threshold:
                union(a, b)

    groups: dict[str, set[str]] = {}
    for t in tickers:
        groups.setdefault(find(t), set()).add(t)
    return list(groups.values())


risk_manager_agent = risk_management_agent
