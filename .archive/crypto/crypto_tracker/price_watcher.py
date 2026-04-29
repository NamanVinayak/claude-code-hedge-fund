"""Crypto Price Watcher — 24/7 price monitoring that simulates order fills.

This IS the exchange: it checks yfinance prices every 5 minutes and "fills"
simulated orders when price levels are hit. Handles entries, stops, and targets.
"""

import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import yfinance as yf

from crypto_tracker.db import get_session, Trade, SimOrder
from crypto_tracker.sim_client import SimClient

UTC = ZoneInfo('UTC')
CHECK_INTERVAL = 300  # 5 minutes
ENTRY_TOLERANCE = 0.015  # 1.5% — trigger entry if price is within this range of entry level


def fetch_prices(tickers):
    """Fetch latest prices for a list of tickers via yfinance."""
    prices = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).fast_info
            prices[t] = info['lastPrice']
        except Exception:
            pass
    return prices


def _parse_max_days(timeframe_str):
    """Parse '5-10 days' → 10. Default 14 if unparseable. Uses calendar days for crypto."""
    if not timeframe_str:
        return 14
    nums = re.findall(r'\d+', str(timeframe_str))
    if len(nums) >= 2:
        return int(nums[1])
    elif len(nums) == 1:
        return int(nums[0])
    return 14


def _process_entries(session, client, prices):
    """Check pending entry orders and fill when price is hit."""
    triggered = 0
    pending = session.query(Trade).filter(Trade.status == 'pending').all()

    for trade in pending:
        price = prices.get(trade.ticker)
        if price is None:
            continue

        hit = False
        # Long: trigger if price is at or below entry, OR within tolerance above entry
        # e.g., entry $73,250, tolerance 1.5% → trigger at $74,349 or below
        if trade.direction == 'long':
            trigger_ceiling = trade.entry_price * (1 + ENTRY_TOLERANCE)
            if price <= trigger_ceiling:
                hit = True
        # Short: trigger if price is at or above entry, OR within tolerance below entry
        elif trade.direction == 'short':
            trigger_floor = trade.entry_price * (1 - ENTRY_TOLERANCE)
            if price >= trigger_floor:
                hit = True

        if hit:
            # Fill the entry order
            if trade.entry_order_id:
                client.fill_order(trade.entry_order_id, price)

            trade.status = 'entered'
            trade.entry_fill_price = price
            trade.entered_at = datetime.now(UTC)
            session.commit()

            side_label = 'BUY' if trade.direction == 'long' else 'SELL'
            stop_str = f" | stop ${trade.stop_loss:.2f}" if trade.stop_loss else ""
            target_str = f" | target ${trade.target_price:.2f}" if trade.target_price else ""
            print(f"    ENTERED: {side_label} {trade.quantity:.6f} {trade.ticker} @ ${price:.2f}{stop_str}{target_str}")
            triggered += 1
        else:
            diff_pct = (trade.entry_price - price) / price * 100
            if trade.direction == 'long':
                trigger_at = trade.entry_price * (1 + ENTRY_TOLERANCE)
                print(f"  {trade.ticker}: ${price:,.2f} (triggers below ${trigger_at:,.2f} — {abs(diff_pct):.1f}% away)")
            else:
                trigger_at = trade.entry_price * (1 - ENTRY_TOLERANCE)
                print(f"  {trade.ticker}: ${price:,.2f} (triggers above ${trigger_at:,.2f} — {abs(diff_pct):.1f}% away)")

    return triggered


def _process_stops_and_targets(session, client, prices):
    """Check entered trades for stop/target hits."""
    closed = 0
    entered = session.query(Trade).filter(Trade.status == 'entered').all()

    for trade in entered:
        price = prices.get(trade.ticker)
        if price is None:
            continue

        fill_price = trade.entry_fill_price or trade.entry_price

        # Check stop loss
        stop_hit = False
        if trade.stop_loss:
            if trade.direction == 'long' and price <= trade.stop_loss:
                stop_hit = True
            elif trade.direction == 'short' and price >= trade.stop_loss:
                stop_hit = True

        if stop_hit:
            if trade.stop_order_id:
                client.fill_order(trade.stop_order_id, price)
            if trade.target_order_id:
                client.cancel_order(trade.target_order_id)

            trade.status = 'stop_hit'
            trade.exit_fill_price = price
            if trade.direction == 'long':
                trade.pnl = (price - fill_price) * trade.quantity
            else:
                trade.pnl = (fill_price - price) * trade.quantity
            trade.closed_at = datetime.now(UTC)
            session.commit()
            print(f"    STOP HIT: {trade.ticker} @ ${price:,.2f} | P&L: ${trade.pnl:+,.2f}")
            closed += 1
            continue

        # Check target
        target_hit = False
        if trade.target_price:
            if trade.direction == 'long' and price >= trade.target_price:
                target_hit = True
            elif trade.direction == 'short' and price <= trade.target_price:
                target_hit = True

        if target_hit:
            if trade.target_order_id:
                client.fill_order(trade.target_order_id, price)
            if trade.stop_order_id:
                client.cancel_order(trade.stop_order_id)

            trade.status = 'target_hit'
            trade.exit_fill_price = price
            if trade.direction == 'long':
                trade.pnl = (price - fill_price) * trade.quantity
            else:
                trade.pnl = (fill_price - price) * trade.quantity
            trade.closed_at = datetime.now(UTC)
            session.commit()
            print(f"    TARGET HIT: {trade.ticker} @ ${price:,.2f} | P&L: ${trade.pnl:+,.2f}")
            closed += 1
            continue

        # Show current P&L for open positions
        if trade.direction == 'long':
            unrealized = (price - fill_price) * trade.quantity
        else:
            unrealized = (fill_price - price) * trade.quantity
        print(f"  {trade.ticker}: ${price:,.2f} (unrealized ${unrealized:+,.2f})")

    return closed


def _process_expiry(session, client):
    """Check for trades that exceeded their timeframe (calendar days)."""
    expired = 0
    entered = session.query(Trade).filter(Trade.status == 'entered').all()
    now = datetime.now(UTC)

    for trade in entered:
        if not trade.entered_at:
            continue
        max_days = _parse_max_days(trade.timeframe)
        entered_at = trade.entered_at
        if entered_at.tzinfo is None:
            entered_at = entered_at.replace(tzinfo=UTC)
        days_held = (now - entered_at).days
        if days_held > max_days:
            if trade.stop_order_id:
                client.cancel_order(trade.stop_order_id)
            if trade.target_order_id:
                client.cancel_order(trade.target_order_id)
            trade.status = 'expired'
            trade.closed_at = now
            session.commit()
            print(f"    EXPIRED: {trade.ticker} after {days_held} calendar days")
            expired += 1

    return expired


def run_watcher():
    """Main loop: check prices every 5 minutes, 24/7."""
    session = get_session()
    client = SimClient()

    pending = session.query(Trade).filter(Trade.status == 'pending').count()
    entered = session.query(Trade).filter(Trade.status == 'entered').count()
    total_active = pending + entered

    print(f"\n=== Crypto Price Watcher Started (24/7) ===")
    print(f"Monitoring: {pending} pending entries, {entered} open positions")
    if total_active == 0:
        print("No active trades — watcher will wait for new trades.\n")

    entered_count = 0
    closed_count = 0

    try:
        while True:
            now_str = datetime.now(UTC).strftime('%H:%M UTC')

            # Collect all tickers with active orders
            active_trades = session.query(Trade).filter(
                Trade.status.in_(['pending', 'entered'])
            ).all()

            if not active_trades:
                print(f"[{now_str}] No active trades. Waiting...")
                time.sleep(CHECK_INTERVAL)
                continue

            tickers = sorted(set(t.ticker for t in active_trades))
            print(f"[{now_str}] Checking {len(tickers)} tickers...")

            prices = fetch_prices(tickers)
            if not prices:
                print("  Price fetch failed — retrying next cycle")
                time.sleep(CHECK_INTERVAL)
                continue

            # Process entries
            new_entries = _process_entries(session, client, prices)
            entered_count += new_entries

            # Process stops and targets
            new_closes = _process_stops_and_targets(session, client, prices)
            closed_count += new_closes

            # Check expiry
            new_expiries = _process_expiry(session, client)
            closed_count += new_expiries

            # Summary
            still_pending = session.query(Trade).filter(Trade.status == 'pending').count()
            still_entered = session.query(Trade).filter(Trade.status == 'entered').count()
            next_check = datetime.now(UTC) + timedelta(seconds=CHECK_INTERVAL)
            print(f"  [{still_pending} pending, {still_entered} open] "
                  f"Next check at {next_check.strftime('%H:%M UTC')}\n")

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    finally:
        print(f"\nSession: {entered_count} entries filled, {closed_count} trades closed.")
        client.close()
        session.close()
