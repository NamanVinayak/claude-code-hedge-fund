from tracker.db import get_session, Trade
from datetime import datetime, timedelta


def _mode_summary_block(trades, mode_label, session):
    """Print a one-section summary block for a set of trades, including open position count."""
    total = len(trades)
    wins = len([t for t in trades if (t.pnl or 0) > 0])
    losses = total - wins
    total_pnl = sum(t.pnl or 0 for t in trades)
    hit_rate = (wins / total * 100) if total > 0 else 0

    mode_val = trades[0].mode if trades else None
    open_count = 0
    if mode_val:
        open_count = session.query(Trade).filter(
            Trade.mode == mode_val,
            Trade.status.in_(['pending', 'entered'])
        ).count()

    targets_hit = len([t for t in trades if t.status == 'target_hit'])
    stops_hit = len([t for t in trades if t.status == 'stop_hit'])
    expired = len([t for t in trades if t.status == 'expired'])

    avg_win = sum(t.pnl for t in trades if (t.pnl or 0) > 0) / max(wins, 1)
    avg_loss = sum(t.pnl for t in trades if (t.pnl or 0) <= 0) / max(losses, 1)
    rr = f"{abs(avg_win / avg_loss):.2f}:1" if avg_loss != 0 else "N/A"

    print(f"\n  {mode_label}")
    print(f"  {'-'*40}")
    print(f"  Closed trades: {total} | Wins: {wins} | Losses: {losses} | Open: {open_count}")
    print(f"  Win rate: {hit_rate:.1f}%  |  Total P&L: ${total_pnl:+,.2f}  |  Avg R/R: {rr}")
    print(f"  Targets hit: {targets_hit} | Stops hit: {stops_hit} | Expired: {expired}")


def _detailed_mode_block(trades, session):
    """Print full detailed breakdown for a single mode."""
    total = len(trades)
    wins = len([t for t in trades if (t.pnl or 0) > 0])
    losses = total - wins
    total_pnl = sum(t.pnl or 0 for t in trades)
    hit_rate = (wins / total * 100) if total > 0 else 0

    targets_hit = len([t for t in trades if t.status == 'target_hit'])
    stops_hit = len([t for t in trades if t.status == 'stop_hit'])
    expired = len([t for t in trades if t.status == 'expired'])

    print(f"  Total trades: {total} | Wins: {wins} | Losses: {losses}")
    print(f"  Hit rate: {hit_rate:.1f}%")
    print(f"  Total P&L: ${total_pnl:+,.2f}")
    print(f"  Targets hit: {targets_hit} | Stops hit: {stops_hit} | Expired: {expired}")

    if total > 0:
        avg_pnl = total_pnl / total
        avg_win = sum(t.pnl for t in trades if (t.pnl or 0) > 0) / max(wins, 1)
        avg_loss = sum(t.pnl for t in trades if (t.pnl or 0) <= 0) / max(losses, 1)
        print(f"\n  Avg P&L per trade: ${avg_pnl:+.2f}")
        print(f"  Avg win: ${avg_win:+.2f} | Avg loss: ${avg_loss:+.2f}")
        if avg_loss != 0:
            print(f"  Win/loss ratio (R/R): {abs(avg_win/avg_loss):.2f}:1")

    print(f"\n  CONFIDENCE CALIBRATION:")
    any_bucket = False
    for bucket_start in range(50, 100, 10):
        bucket_end = bucket_start + 10
        bucket_trades = [t for t in trades if t.confidence and bucket_start <= t.confidence < bucket_end]
        if bucket_trades:
            any_bucket = True
            bucket_wins = len([t for t in bucket_trades if (t.pnl or 0) > 0])
            actual = bucket_wins / len(bucket_trades) * 100
            match = "+" if abs(actual - (bucket_start + 5)) < 15 else "x"
            print(f"    {bucket_start}-{bucket_end}% conf: {actual:.0f}% actual ({len(bucket_trades)} trades) [{match}]")
    if not any_bucket:
        print("    No confidence data yet.")


def report(days=7, mode=None):
    """Print accuracy dashboard."""
    session = get_session()

    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        base_query = session.query(Trade).filter(
            Trade.status.in_(['target_hit', 'stop_hit', 'expired']),
            Trade.closed_at >= cutoff
        )

        if mode:
            # Detailed single-mode view
            trades = base_query.filter(Trade.mode == mode).all()

            print(f"\n{'='*55}")
            print(f"  PAPER TRADING REPORT -- {mode.upper()} (last {days} days)")
            print(f"{'='*55}")

            if not trades:
                print(f"  No closed {mode} trades in the last {days} days.")
                print()
                return

            _detailed_mode_block(trades, session)
            print()

        else:
            # Two-section overview: SWING + DAYTRADE
            all_trades = base_query.all()

            print(f"\n{'='*55}")
            print(f"  PAPER TRADING REPORT (last {days} days)")
            print(f"{'='*55}")

            if not all_trades:
                print(f"  No closed trades in the last {days} days.")
                print()
                return

            for m in ('swing', 'daytrade'):
                m_trades = [t for t in all_trades if t.mode == m]
                if m_trades:
                    _mode_summary_block(m_trades, m.upper(), session)
                else:
                    open_count = session.query(Trade).filter(
                        Trade.mode == m,
                        Trade.status.in_(['pending', 'entered'])
                    ).count()
                    print(f"\n  {m.upper()}")
                    print(f"  {'-'*40}")
                    print(f"  No closed trades | Open: {open_count}")

            # Any other modes present in data
            other_modes = set(t.mode for t in all_trades) - {'swing', 'daytrade'}
            for m in sorted(other_modes):
                m_trades = [t for t in all_trades if t.mode == m]
                _mode_summary_block(m_trades, m.upper(), session)

            print()

    finally:
        session.close()
