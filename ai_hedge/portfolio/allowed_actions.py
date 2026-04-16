def compute_allowed_actions(
        tickers: list[str],
        current_prices: dict[str, float],
        max_shares: dict[str, float | int],
        portfolio: dict[str, float],
        *,
        fractional: bool = False,
) -> dict[str, dict[str, float | int]]:
    """Compute allowed actions and max quantities for each ticker deterministically."""
    allowed = {}
    cash = float(portfolio.get("cash", 0.0))
    positions = portfolio.get("positions", {}) or {}
    margin_requirement = float(portfolio.get("margin_requirement", 0.5))
    margin_used = float(portfolio.get("margin_used", 0.0))
    equity = float(portfolio.get("equity", cash))

    def _qty(x: float) -> float | int:
        """Round quantity: fractional for crypto, integer for stocks."""
        if fractional:
            return round(x, 8)
        return int(x)

    for ticker in tickers:
        price = float(current_prices.get(ticker, 0.0))
        pos = positions.get(
            ticker,
            {"long": 0, "long_cost_basis": 0.0, "short": 0, "short_cost_basis": 0.0},
        )
        long_shares = float(pos.get("long", 0) or 0)
        short_shares = float(pos.get("short", 0) or 0)
        max_qty = float(max_shares.get(ticker, 0) or 0)

        # Start with zeros
        actions: dict[str, float | int] = {"buy": 0, "sell": 0, "short": 0, "cover": 0, "hold": 0}

        # Long side
        if long_shares > 0:
            actions["sell"] = _qty(long_shares)
        if cash > 0 and price > 0:
            max_buy_cash = cash / price
            max_buy = _qty(max(0, min(max_qty, max_buy_cash)))
            if max_buy > 0:
                actions["buy"] = max_buy

        # Short side
        if short_shares > 0:
            actions["cover"] = _qty(short_shares)
        if price > 0 and max_qty > 0:
            if margin_requirement <= 0.0:
                # If margin requirement is zero or unset, only cap by max_qty
                max_short = _qty(max_qty)
            else:
                available_margin = max(0.0, (equity / margin_requirement) - margin_used)
                max_short_margin = available_margin / price
                max_short = _qty(max(0, min(max_qty, max_short_margin)))
            if max_short > 0:
                actions["short"] = max_short

        # Hold always valid
        actions["hold"] = 0

        # Prune zero-capacity actions to reduce tokens, keep hold
        pruned: dict[str, float | int] = {"hold": 0}
        for k, v in actions.items():
            if k != "hold" and v > 0:
                pruned[k] = v

        allowed[ticker] = pruned

    return allowed
