def compute_allowed_actions(
        tickers: list[str],
        current_prices: dict[str, float],
        max_shares: dict[str, float | int],
        portfolio: dict[str, float],
        *,
        fractional: bool = False,
        current_positions: list[dict] | None = None,
) -> dict[str, dict[str, float | int]]:
    """Compute allowed actions and max quantities for each ticker deterministically.

    Parameters
    ----------
    current_positions
        Optional list of currently-open positions across the entire portfolio
        (BOTH tickers being analyzed this run AND others). Each dict has at
        least: ticker, direction ('long'|'short'), quantity, entry_fill_price
        (or entry_price as fallback). When supplied:
          - cash is reduced by total open exposure (qty * fill_price) so the
            PM cannot double-spend capital that's already locked in trades
          - tickers we're already long in cannot be bought again (no 'buy')
          - tickers we're already short in cannot be shorted again (no 'short')
          - we still allow closing actions ('sell' on longs, 'cover' on shorts)
    """
    allowed = {}
    cash = float(portfolio.get("cash", 0.0))
    positions = portfolio.get("positions", {}) or {}
    margin_requirement = float(portfolio.get("margin_requirement", 0.5))
    margin_used = float(portfolio.get("margin_used", 0.0))
    equity = float(portfolio.get("equity", cash))

    # Reduce cash by exposure of all open positions (analyzed + others) so
    # downstream sizing math doesn't pretend locked capital is spendable.
    held_long: set[str] = set()
    held_short: set[str] = set()
    if current_positions:
        total_exposure = 0.0
        for p in current_positions:
            qty = float(p.get("quantity", 0) or 0)
            price = float(p.get("entry_fill_price") or p.get("entry_price") or 0)
            total_exposure += qty * price
            t = (p.get("ticker") or "").upper()
            if p.get("direction") == "long":
                held_long.add(t)
            elif p.get("direction") == "short":
                held_short.add(t)
        cash = max(0.0, cash - total_exposure)
        equity = max(0.0, equity - total_exposure)

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
        # Block re-buying when we already hold a long in this ticker — the PM
        # may decide to hold or sell, but cannot stack a second entry on top.
        if cash > 0 and price > 0 and ticker not in held_long:
            max_buy_cash = cash / price
            max_buy = _qty(max(0, min(max_qty, max_buy_cash)))
            if max_buy > 0:
                actions["buy"] = max_buy

        # Short side
        if short_shares > 0:
            actions["cover"] = _qty(short_shares)
        # Block re-shorting when we already hold a short in this ticker.
        if price > 0 and max_qty > 0 and ticker not in held_short:
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
