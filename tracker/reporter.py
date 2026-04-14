from tracker.db import get_session, Trade
from datetime import datetime, timedelta


def report(days=7, mode=None):
    """Print accuracy dashboard."""
    session = get_session()

    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = session.query(Trade).filter(
            Trade.status.in_(['target_hit', 'stop_hit', 'expired']),
            Trade.closed_at >= cutoff
        )
        if mode:
            query = query.filter(Trade.mode == mode)

        trades = query.all()

        if not trades:
            print(f"\nNo closed trades in the last {days} days.")
            return

        total = len(trades)
        wins = len([t for t in trades if (t.pnl or 0) > 0])
        losses = total - wins
        total_pnl = sum(t.pnl or 0 for t in trades)
        hit_rate = (wins / total * 100) if total > 0 else 0

        targets_hit = len([t for t in trades if t.status == 'target_hit'])
        stops_hit = len([t for t in trades if t.status == 'stop_hit'])
        expired = len([t for t in trades if t.status == 'expired'])

        print(f"\n{'='*55}")
        print(f"  PAPER TRADING REPORT (last {days} days)")
        print(f"{'='*55}")
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
                print(f"  Win/loss ratio: {abs(avg_win/avg_loss):.2f}:1")

        # Per-mode breakdown
        modes = set(t.mode for t in trades)
        if len(modes) > 1:
            print(f"\n  BY MODE:")
            for m in sorted(modes):
                m_trades = [t for t in trades if t.mode == m]
                m_wins = len([t for t in m_trades if (t.pnl or 0) > 0])
                m_pnl = sum(t.pnl or 0 for t in m_trades)
                m_rate = m_wins / len(m_trades) * 100
                print(f"    {m:10s}: {len(m_trades)} trades | {m_rate:.0f}% hit rate | ${m_pnl:+.2f}")

        # Confidence calibration
        print(f"\n  CONFIDENCE CALIBRATION:")
        for bucket_start in range(50, 100, 10):
            bucket_end = bucket_start + 10
            bucket_trades = [t for t in trades if t.confidence and bucket_start <= t.confidence < bucket_end]
            if bucket_trades:
                bucket_wins = len([t for t in bucket_trades if (t.pnl or 0) > 0])
                actual = bucket_wins / len(bucket_trades) * 100
                match = "✓" if abs(actual - (bucket_start + 5)) < 15 else "✗"
                print(f"    {bucket_start}-{bucket_end}% conf: {actual:.0f}% actual ({len(bucket_trades)} trades) {match}")

        print()
    finally:
        session.close()
