"""Read decisions.json and create simulated crypto paper trades."""

import json
import os
import re
from crypto_tracker.db import get_session, Trade, get_available_cash
from crypto_tracker.sim_client import SimClient


def execute_run(run_id):
    """Read decisions.json and create simulated paper trades."""
    # Load config
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    max_per_position = config['settings']['max_position_size_usd']
    max_concurrent = config['settings']['max_concurrent_trades']

    # Load run data
    decisions_path = os.path.join('runs', run_id, 'decisions.json')
    meta_path = os.path.join('runs', run_id, 'metadata.json')

    if not os.path.exists(decisions_path):
        print(f"No decisions.json found for run {run_id}")
        return

    with open(meta_path) as f:
        meta = json.load(f)
    with open(decisions_path) as f:
        decisions_data = json.load(f)

    mode = meta['mode']
    decisions = decisions_data.get('decisions', {})
    if not decisions:
        print("No decisions found.")
        return

    available = get_available_cash()
    print(f"\n=== Executing crypto {mode} run {run_id} ===")
    print(f"Available cash: ${available:,.2f}")

    session = get_session()
    open_count = session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).count()
    if open_count >= max_concurrent:
        print(f"Already at max concurrent trades ({max_concurrent}). Skipping.")
        session.close()
        return

    client = SimClient()
    trades_placed = 0

    try:
        for ticker, decision in decisions.items():
            action = decision.get('action', decision.get('direction', 'hold'))

            if action in ('hold', 'no_trade', 'neutral'):
                print(f"  {ticker}: {action} — skipping")
                continue

            if action in ('buy', 'cover', 'long'):
                direction = 'long'
            elif action in ('sell', 'short'):
                direction = 'short'
            else:
                print(f"  {ticker}: unknown action '{action}' — skipping")
                continue

            entry_price = decision.get('entry_price', decision.get('entry'))
            target_price = decision.get('target_price', decision.get('target', decision.get('target_1')))
            target_price_2 = decision.get('target_price_2', decision.get('target_2'))
            stop_loss = decision.get('stop_loss', decision.get('stop'))

            targets = decision.get('targets', [])
            if targets and not target_price:
                target_price = targets[0] if len(targets) > 0 else None
                target_price_2 = targets[1] if len(targets) > 1 else None

            if not entry_price or not stop_loss:
                print(f"  {ticker}: missing entry_price or stop_loss — skipping")
                continue

            # Calculate quantity — support fractional crypto
            quantity = decision.get('quantity', decision.get('position_size'))
            if quantity is None:
                quantity = max_per_position / entry_price
            if isinstance(quantity, str):
                nums = re.findall(r'[\d.]+', quantity)
                quantity = float(nums[0]) if nums else max_per_position / entry_price
            quantity = float(quantity)

            # Cap by max position size
            max_qty = max_per_position / entry_price
            quantity = min(quantity, max_qty)

            if quantity <= 0:
                print(f"  {ticker}: quantity too small — skipping")
                continue

            position_value = entry_price * quantity
            if position_value > available:
                quantity = available / entry_price
                if quantity <= 0:
                    print(f"  {ticker}: insufficient cash (${available:.2f}) — skipping")
                    continue
                position_value = entry_price * quantity

            if open_count + trades_placed >= max_concurrent:
                print(f"  {ticker}: max concurrent trades reached — skipping")
                break

            # Place simulated orders
            entry_oid = client.place_entry(ticker, direction, quantity, entry_price)
            print(f"  {ticker}: entry {direction.upper()} {quantity:.6f} @ ${entry_price:.2f} — sim order {entry_oid}")

            stop_oid = None
            if stop_loss:
                stop_oid = client.place_stop(ticker, direction, quantity, stop_loss)
                print(f"  {ticker}: stop @ ${stop_loss:.2f} — sim order {stop_oid}")

            target_oid = None
            if target_price:
                target_oid = client.place_target(ticker, direction, quantity, target_price)
                print(f"  {ticker}: target @ ${target_price:.2f} — sim order {target_oid}")

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
                raw_decision=json.dumps(decision),
            )
            session.add(trade)
            session.commit()

            # Link orders to trade
            from crypto_tracker.db import SimOrder
            for oid in [entry_oid, stop_oid, target_oid]:
                if oid:
                    order = session.query(SimOrder).get(int(oid))
                    if order:
                        order.trade_id = trade.id
            session.commit()

            available -= position_value
            trades_placed += 1

    finally:
        client.close()
        session.close()

    print(f"\n  Placed {trades_placed} trades. Remaining cash: ${available:,.2f}")
