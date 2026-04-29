"""Position monitoring and status display for crypto paper trading."""

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from crypto_tracker.db import get_session, Trade, get_available_cash

UTC = ZoneInfo('UTC')


def _parse_max_days(timeframe_str):
    """Parse '5-10 days' → 10. Default 14 for crypto."""
    if not timeframe_str:
        return 14
    nums = re.findall(r'\d+', str(timeframe_str))
    if len(nums) >= 2:
        return int(nums[1])
    elif len(nums) == 1:
        return int(nums[0])
    return 14


def monitor_positions():
    """Check for expired trades and display summary."""
    session = get_session()

    try:
        now = datetime.now(UTC)

        # Check for expired trades (calendar days)
        entered = session.query(Trade).filter(Trade.status == 'entered').all()
        expired_count = 0
        for trade in entered:
            if not trade.entered_at:
                continue
            max_days = _parse_max_days(trade.timeframe)
            entered_at = trade.entered_at
            if entered_at.tzinfo is None:
                entered_at = entered_at.replace(tzinfo=UTC)
            days_held = (now - entered_at).days
            if days_held > max_days:
                trade.status = 'expired'
                trade.closed_at = now
                session.commit()
                print(f"  EXPIRED: {trade.ticker} after {days_held} calendar days")
                expired_count += 1

        if expired_count:
            print(f"\n  Expired {expired_count} trade(s)")

        show_status(session=session)

    finally:
        session.close()


def show_status(session=None):
    """Print current open positions and recent activity."""
    own_session = session is None
    if own_session:
        session = get_session()

    try:
        available = get_available_cash()
        open_trades = session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).all()
        recent_closed = session.query(Trade).filter(
            Trade.status.in_(['target_hit', 'stop_hit', 'expired'])
        ).order_by(Trade.closed_at.desc()).limit(5).all()

        print(f"\n{'='*55}")
        print(f"  CRYPTO PAPER TRADING STATUS")
        print(f"  Available cash: ${available:,.2f}")
        print(f"  Open positions: {len(open_trades)}")
        print(f"{'='*55}")

        if open_trades:
            print(f"\n  OPEN POSITIONS:")
            for t in open_trades:
                stop_str = f"${t.stop_loss:,.2f}" if t.stop_loss else "N/A"
                target_str = f"${t.target_price:,.2f}" if t.target_price else "N/A"
                print(f"    {t.direction.upper():5s} {t.quantity:.6f} {t.ticker:10s} "
                      f"@ ${t.entry_price:,.2f} | stop {stop_str} | target {target_str} | {t.status}")

        if recent_closed:
            print(f"\n  RECENT CLOSES:")
            for t in recent_closed:
                pnl_str = f"${t.pnl:+,.2f}" if t.pnl else "N/A"
                print(f"    {t.ticker:10s} {t.status:12s} | P&L: {pnl_str}")

        print()
    finally:
        if own_session:
            session.close()
