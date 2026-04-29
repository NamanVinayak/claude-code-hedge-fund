import os
import re
from datetime import datetime, timedelta
from tracker.db import get_session, Trade, DailySummary


def _count_business_days(start_date, end_date):
    """Count business days between two dates."""
    days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Mon-Fri
            days += 1
        current += timedelta(days=1)
    return days


def _parse_max_days(timeframe_str):
    """Parse '8-15 trading days' → 15. Default 10 if unparseable."""
    if not timeframe_str:
        return 10
    nums = re.findall(r'\d+', str(timeframe_str))
    if len(nums) >= 2:
        return int(nums[1])
    elif len(nums) == 1:
        return int(nums[0])
    return 10


def monitor_positions():
    """Check Moomoo for fills, update DB, manage stops/targets."""
    from tracker.moomoo_client import MoomooClient

    session = get_session()
    client = MoomooClient()

    try:
        orders_df = client.get_orders()

        # Build order status lookup: order_id → status, dealt_avg_price
        order_status = {}
        if not orders_df.empty:
            for _, row in orders_df.iterrows():
                oid = str(row.get('order_id', ''))
                order_status[oid] = {
                    'status': str(row.get('order_status', '')),
                    'dealt_avg_price': float(row.get('dealt_avg_price', 0) or 0),
                    'dealt_qty': int(row.get('dealt_qty', 0) or 0),
                }

        # Process pending trades (waiting for entry fill)
        pending = session.query(Trade).filter(Trade.status == 'pending').all()
        cancelled_count = 0
        for trade in pending:
            entry_info = order_status.get(trade.entry_order_id, {})
            entry_status = entry_info.get('status', '')

            if 'FILLED_ALL' in entry_status:
                trade.status = 'entered'
                trade.entry_fill_price = entry_info.get('dealt_avg_price', trade.entry_price)
                trade.entered_at = datetime.utcnow()
                print(f"  FILLED: {trade.direction.upper()} {trade.quantity} {trade.ticker} @ ${trade.entry_fill_price:.2f}")
                session.commit()

            elif ('CANCELLED' in entry_status or 'DELETED' in entry_status
                  or (trade.entry_order_id and trade.entry_order_id not in order_status)):
                # Entry order was cancelled by Moomoo (DAY expiry) or no longer exists
                reason = entry_status if entry_status else "order not found on Moomoo"
                trade.status = 'cancelled'
                trade.closed_at = datetime.utcnow()
                # Cancel associated stop/target orders if they exist
                if trade.stop_order_id:
                    client.cancel_order(trade.stop_order_id)
                if trade.target_order_id:
                    client.cancel_order(trade.target_order_id)
                cancelled_count += 1
                print(f"  CANCELLED: Trade #{trade.id} {trade.ticker} — entry order {reason} (DAY expiry)")
                session.commit()

        if cancelled_count:
            print(f"\n  Cleaned up {cancelled_count} stale pending trade(s)")

        # Process entered trades (waiting for target/stop/expiry)
        entered = session.query(Trade).filter(Trade.status == 'entered').all()
        for trade in entered:
            target_info = order_status.get(trade.target_order_id, {})
            stop_info = order_status.get(trade.stop_order_id, {})

            # Target hit?
            if trade.target_order_id and 'FILLED_ALL' in target_info.get('status', ''):
                trade.status = 'target_hit'
                trade.exit_fill_price = target_info.get('dealt_avg_price', trade.target_price)
                if trade.direction == 'long':
                    trade.pnl = (trade.exit_fill_price - trade.entry_fill_price) * trade.quantity
                else:
                    trade.pnl = (trade.entry_fill_price - trade.exit_fill_price) * trade.quantity
                trade.closed_at = datetime.utcnow()
                # Cancel the stop order
                if trade.stop_order_id:
                    client.cancel_order(trade.stop_order_id)
                print(f"  TARGET HIT: {trade.ticker} P&L: ${trade.pnl:+.2f}")
                session.commit()
                continue

            # Stop hit?
            if trade.stop_order_id and 'FILLED_ALL' in stop_info.get('status', ''):
                trade.status = 'stop_hit'
                trade.exit_fill_price = stop_info.get('dealt_avg_price', trade.stop_loss)
                if trade.direction == 'long':
                    trade.pnl = (trade.exit_fill_price - trade.entry_fill_price) * trade.quantity
                else:
                    trade.pnl = (trade.entry_fill_price - trade.exit_fill_price) * trade.quantity
                trade.closed_at = datetime.utcnow()
                # Cancel the target order
                if trade.target_order_id:
                    client.cancel_order(trade.target_order_id)
                print(f"  STOP HIT: {trade.ticker} P&L: ${trade.pnl:+.2f}")
                session.commit()
                continue

            # Check for cancelled stop/target orders on open positions (DAY expiry)
            # Position is still open — just warn that protection orders need re-placing
            stale_orders = []
            if trade.stop_order_id:
                stop_status = stop_info.get('status', '')
                if ('CANCELLED' in stop_status or 'DELETED' in stop_status
                        or trade.stop_order_id not in order_status):
                    stale_orders.append('stop')
            if trade.target_order_id:
                target_status = target_info.get('status', '')
                if ('CANCELLED' in target_status or 'DELETED' in target_status
                        or trade.target_order_id not in order_status):
                    stale_orders.append('target')
            if stale_orders:
                print(f"  ⚠️  {trade.ticker}: {'/'.join(stale_orders)} order(s) cancelled (DAY expiry) — position still open, needs re-placed")

            # Expired?
            if trade.entered_at:
                max_days = _parse_max_days(trade.timeframe)
                days_held = _count_business_days(trade.entered_at, datetime.utcnow())
                if days_held > max_days:
                    # Cancel all orders and flatten
                    if trade.stop_order_id:
                        client.cancel_order(trade.stop_order_id)
                    if trade.target_order_id:
                        client.cancel_order(trade.target_order_id)
                    client.flatten_position(trade.ticker, trade.quantity, trade.direction)
                    trade.status = 'expired'
                    trade.closed_at = datetime.utcnow()
                    # P&L will be approximate until we get fill price
                    print(f"  EXPIRED: {trade.ticker} after {days_held} days — flattened at market")
                    session.commit()

        # Print summary
        show_status(session=session)

    finally:
        client.close()
        session.close()


def show_status(session=None):
    """Print current open positions and recent activity."""
    from tracker.db import get_available_cash

    own_session = session is None
    if own_session:
        from tracker.db import get_session
        session = get_session()

    try:
        available = get_available_cash()
        open_trades = session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).all()
        recent_closed = session.query(Trade).filter(
            Trade.status.in_(['target_hit', 'stop_hit', 'expired'])
        ).order_by(Trade.closed_at.desc()).limit(5).all()

        print(f"\n{'='*50}")
        print(f"  PAPER TRADING STATUS")
        print(f"  Available cash: ${available:,.2f}")
        print(f"  Open positions: {len(open_trades)}")
        print(f"{'='*50}")

        if open_trades:
            print(f"\n  OPEN POSITIONS:")
            for t in open_trades:
                stop_str = f"${t.stop_loss:.2f}" if t.stop_loss else "N/A"
                target_str = f"${t.target_price:.2f}" if t.target_price else "N/A"
                print(f"    {t.direction.upper():5s} {t.quantity} {t.ticker:5s} @ ${t.entry_price:.2f} | stop {stop_str} | target {target_str} | status: {t.status}")

        if recent_closed:
            print(f"\n  RECENT CLOSES:")
            for t in recent_closed:
                pnl_str = f"${t.pnl:+.2f}" if t.pnl else "N/A"
                print(f"    {t.ticker:5s} {t.status:12s} | P&L: {pnl_str}")

        print()
    finally:
        if own_session:
            session.close()
