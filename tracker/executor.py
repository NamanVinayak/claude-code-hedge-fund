import json
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from tracker.db import get_session, Trade, get_available_cash, get_available_cash_for_mode

# Major US market holidays (month, day) — static list, not exhaustive
US_MARKET_HOLIDAYS_2026 = {
    (1, 1), (1, 19), (2, 16), (4, 3), (5, 25), (7, 3),
    (9, 7), (11, 26), (12, 25),
}


def is_market_open():
    """Check if US stock market is currently open (9:30 AM - 4:00 PM ET, weekdays)."""
    et = ZoneInfo('America/New_York')
    now = datetime.now(et)

    # Weekend check
    if now.weekday() >= 5:
        return False, f"Weekend ({now.strftime('%A')})"

    # Holiday check (basic)
    if (now.month, now.day) in US_MARKET_HOLIDAYS_2026:
        return False, "Market holiday"

    # Hours check
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

    if now < market_open:
        return False, f"Pre-market (opens {market_open.strftime('%I:%M %p ET')})"
    if now >= market_close:
        return False, "After hours (closed at 4:00 PM ET)"

    return True, "Market is open"


def execute_run(run_id):
    """Read decisions.json and place paper trades on Moomoo."""
    from tracker.moomoo_client import MoomooClient

    # Market hours check
    market_open, reason = is_market_open()
    if not market_open:
        print(f"\n⚠️  Market is CLOSED: {reason}")
        print("   Orders placed now use TimeInForce.DAY and will be cancelled")
        print("   by Moomoo before next open. Run during market hours (9:30 AM - 4:00 PM ET).")
        print("   Continuing anyway...\n")

    # Load config
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    max_per_position = config['settings']['max_position_size_usd']  # 250
    max_concurrent = config['settings']['max_concurrent_trades']  # 5

    # Load run data
    meta_path = os.path.join('runs', run_id, 'metadata.json')
    decisions_path = os.path.join('runs', run_id, 'decisions.json')

    if not os.path.exists(decisions_path):
        print(f"No decisions.json found for run {run_id}")
        return

    with open(meta_path) as f:
        meta = json.load(f)
    with open(decisions_path) as f:
        decisions_data = json.load(f)

    mode = meta['mode']
    if mode not in ('swing', 'daytrade'):
        print(f"Mode '{mode}' not supported for paper trading. Use swing or daytrade.")
        return

    decisions = decisions_data.get('decisions', {})
    if not decisions:
        print("No decisions found.")
        return

    # Check available budget (per-mode)
    available = get_available_cash_for_mode(mode)
    print(f"\n=== Executing {mode} run {run_id} ===")
    print(f"Available cash ({mode}): ${available:,.2f}")

    # Check concurrent trade limit
    session = get_session()
    open_count = session.query(Trade).filter(Trade.mode == mode, Trade.status.in_(['pending', 'entered'])).count()
    if open_count >= max_concurrent:
        print(f"Already at max concurrent trades ({max_concurrent}). Skipping.")
        session.close()
        return

    # Connect to Moomoo
    client = MoomooClient()
    trades_placed = 0

    try:
        for ticker, decision in decisions.items():
            action = decision.get('action', decision.get('direction', 'hold'))

            # Skip non-actionable
            if action in ('hold', 'no_trade', 'neutral'):
                print(f"  {ticker}: {action} — skipping")
                continue

            # Determine direction
            if action in ('buy', 'cover'):
                direction = 'long'
            elif action in ('sell', 'short'):
                direction = 'short'
            else:
                print(f"  {ticker}: unknown action '{action}' — skipping")
                continue

            # Extract prices (handle field aliases)
            entry_price = decision.get('entry_price', decision.get('entry'))
            target_price = decision.get('target_price', decision.get('target', decision.get('target_1')))
            target_price_2 = decision.get('target_price_2', decision.get('target_2'))
            stop_loss = decision.get('stop_loss', decision.get('stop'))

            # For daytrade: targets array
            targets = decision.get('targets', [])
            if targets and not target_price:
                target_price = targets[0] if len(targets) > 0 else None
                target_price_2 = targets[1] if len(targets) > 1 else None

            if not entry_price or not stop_loss:
                print(f"  {ticker}: missing entry_price or stop_loss — skipping")
                continue

            # Calculate quantity within budget
            quantity = decision.get('quantity', decision.get('position_size', 1))
            if isinstance(quantity, str):
                # Handle string position sizes like "2 shares"
                import re
                nums = re.findall(r'\d+', quantity)
                quantity = int(nums[0]) if nums else 1
            quantity = int(quantity)
            max_qty = int(max_per_position / entry_price)
            quantity = min(quantity, max_qty)

            if quantity < 1:
                print(f"  {ticker}: ${entry_price:.2f}/share too expensive for ${max_per_position} limit — skipping")
                continue

            position_value = entry_price * quantity
            if position_value > available:
                # Try to fit what we can
                quantity = int(available / entry_price)
                if quantity < 1:
                    print(f"  {ticker}: insufficient cash (${available:.2f}) — skipping")
                    continue
                position_value = entry_price * quantity

            # Check concurrent limit
            if open_count + trades_placed >= max_concurrent:
                print(f"  {ticker}: max concurrent trades reached — skipping")
                break

            # Place orders
            try:
                entry_oid = client.place_entry(ticker, direction, quantity, entry_price)
                print(f"  {ticker}: entry {direction.upper()} {quantity} @ ${entry_price:.2f} — order {entry_oid}")

                stop_oid = None
                if stop_loss:
                    try:
                        stop_oid = client.place_stop(ticker, direction, quantity, stop_loss)
                        print(f"  {ticker}: stop @ ${stop_loss:.2f} — order {stop_oid}")
                    except Exception as e:
                        print(f"  {ticker}: stop order failed: {e}")

                target_oid = None
                if target_price:
                    try:
                        target_oid = client.place_target(ticker, direction, quantity, target_price)
                        print(f"  {ticker}: target @ ${target_price:.2f} — order {target_oid}")
                    except Exception as e:
                        print(f"  {ticker}: target order failed: {e}")

                # Save to DB
                trade = Trade(
                    run_id=run_id,
                    mode=mode,
                    ticker=ticker,
                    direction=direction,
                    quantity=quantity,
                    entry_price=entry_price,
                    target_price=target_price,
                    target_price_2=target_price_2,
                    stop_loss=stop_loss,
                    confidence=decision.get('confidence'),
                    timeframe=decision.get('timeframe', decision.get('time_window', '')),
                    entry_order_id=entry_oid,
                    stop_order_id=stop_oid,
                    target_order_id=target_oid,
                    status='pending',
                    raw_decision=json.dumps(decision)
                )
                session.add(trade)
                session.commit()

                available -= position_value
                trades_placed += 1

            except Exception as e:
                print(f"  {ticker}: order placement failed: {e}")
                continue

    finally:
        client.close()
        session.close()

    print(f"\n  Placed {trades_placed} trades. Remaining cash: ${available:,.2f}")
