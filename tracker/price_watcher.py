"""Price Watcher — monitors prices and places market orders when entry levels are hit.

Solves the problem that Moomoo paper trading only supports DAY orders (no GTC),
so limit orders placed after hours get cancelled. This script runs during market
hours, checks prices every 5 minutes, and fires market orders at entry levels.
"""

import time
from datetime import datetime
from zoneinfo import ZoneInfo

import yfinance as yf

from tracker.db import get_session, Trade
from tracker.executor import is_market_open


ET = ZoneInfo('America/New_York')
CHECK_INTERVAL = 300  # 5 minutes


def get_pending_trades(session):
    """Return all trades with status='pending'."""
    return session.query(Trade).filter(Trade.status == 'pending').all()


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


def is_triggered(trade, current_price):
    """Check if current price has reached the entry level."""
    if trade.direction == 'long':
        return current_price <= trade.entry_price
    else:  # short
        return current_price >= trade.entry_price


def execute_trigger(client, session, trade, current_price):
    """Place market entry + stop/target orders for a triggered trade."""
    # Cancel stale limit entry order if one exists
    if trade.entry_order_id:
        client.cancel_order(trade.entry_order_id)

    # Place market entry
    entry_oid = client.place_market_entry(trade.ticker, trade.direction, trade.quantity)

    # Place stop loss
    stop_oid = None
    if trade.stop_loss:
        try:
            stop_oid = client.place_stop(trade.ticker, trade.direction, trade.quantity, trade.stop_loss)
        except Exception as e:
            print(f"    stop order failed: {e}")

    # Place target
    target_oid = None
    if trade.target_price:
        try:
            target_oid = client.place_target(trade.ticker, trade.direction, trade.quantity, trade.target_price)
        except Exception as e:
            print(f"    target order failed: {e}")

    # Update DB
    trade.entry_order_id = entry_oid
    trade.stop_order_id = stop_oid
    trade.target_order_id = target_oid
    trade.status = 'entered'
    trade.entered_at = datetime.now(ET)
    session.commit()

    side_label = 'BUY' if trade.direction == 'long' else 'SELL'
    stop_str = f" | stop ${trade.stop_loss:.2f}" if trade.stop_loss else ""
    target_str = f" | target ${trade.target_price:.2f}" if trade.target_price else ""
    print(f"    ENTERED: {side_label} {trade.quantity} {trade.ticker} @ market{stop_str}{target_str}")


def run_watcher():
    """Main loop: check prices every 5 minutes, trigger entries when hit."""
    # Wait for market open if started early
    market_open, reason = is_market_open()
    if not market_open:
        print(f"\nMarket is CLOSED: {reason}")
        print("Waiting for market open (9:30 AM ET / 6:30 AM PT)...\n")
        while True:
            time.sleep(60)  # check every minute
            market_open, reason = is_market_open()
            if market_open:
                print("Market is now open! Starting watcher.\n")
                break
            # Show a dot every 15 min so user knows it's alive
            now = datetime.now(ET)
            if now.minute % 15 == 0 and now.second < 60:
                print(f"  [{now.strftime('%I:%M %p ET')}] Still waiting... {reason}")

    session = get_session()
    pending = get_pending_trades(session)

    if not pending:
        print("\nNo pending trades to watch.")
        session.close()
        return

    tickers = sorted(set(t.ticker for t in pending))
    print(f"\n=== Price Watcher Started ===")
    print(f"Market is open (closes 4:00 PM ET)")
    print(f"Watching {len(pending)} pending trades: {', '.join(tickers)}\n")

    from tracker.moomoo_client import MoomooClient
    client = MoomooClient()
    entered_today = 0

    try:
        while True:
            # Check market hours
            market_open, reason = is_market_open()
            if not market_open:
                print(f"\n[{datetime.now(ET).strftime('%H:%M')}] Market closed. Stopping.")
                break

            now_str = datetime.now(ET).strftime('%H:%M')
            print(f"[{now_str}] Checking prices...")

            # Refresh pending list
            pending = get_pending_trades(session)
            if not pending:
                print("  No more pending trades. Done.")
                break

            tickers = sorted(set(t.ticker for t in pending))
            prices = fetch_prices(tickers)

            for trade in pending:
                price = prices.get(trade.ticker)
                if price is None:
                    print(f"  {trade.ticker}: price unavailable — skipping")
                    continue

                if is_triggered(trade, price):
                    side_label = 'BUY' if trade.direction == 'long' else 'SELL'
                    print(f"  {trade.ticker}: ${price:.2f} — TRIGGERED! "
                          f"(entry ${trade.entry_price:.2f})")
                    try:
                        execute_trigger(client, session, trade, price)
                        entered_today += 1
                    except Exception as e:
                        print(f"    order placement failed: {e}")
                else:
                    diff_pct = (trade.entry_price - price) / price * 100
                    sign = '+' if diff_pct > 0 else ''
                    print(f"  {trade.ticker}: ${price:.2f} "
                          f"(entry ${trade.entry_price:.2f} — waiting, need {sign}{diff_pct:.1f}%)")

            # Calculate next check time
            next_check = datetime.now(ET)
            next_min = next_check.minute + 5
            print(f"  Next check at {next_check.strftime('%H')}:{next_min:02d}\n")

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    finally:
        # Summary
        still_pending = len(get_pending_trades(session))
        print(f"\n{entered_today} trades entered today, {still_pending} still pending.")
        client.close()
        session.close()
