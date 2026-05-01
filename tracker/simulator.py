import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import logging
from datetime import datetime, time, timezone
import pytz
import yfinance as yf
import pandas as pd
from tracker.turso_client import (
    get_pending_trades,
    get_open_positions,
    update_trade,
    log_fill,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

NY_TZ = pytz.timezone('America/New_York')
MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)

def is_market_hours(dt: datetime) -> bool:
    ny_dt = dt.astimezone(NY_TZ)
    return MARKET_OPEN <= ny_dt.time() <= MARKET_CLOSE

def run_simulator(dry_run: bool = False):
    pending = get_pending_trades()
    opened = get_open_positions()
    
    trades = pending + opened
    if not trades:
        print("Checked 0 positions: 0 entries filled, 0 stops hit, 0 targets hit, 0 unchanged")
        return

    tickers = list(set(t['ticker'] for t in trades))
    
    # Download 1m data for today
    logger.info(f"Fetching 1-minute bars for {len(tickers)} tickers: {tickers}")
    try:
        data = yf.download(
            tickers, 
            period="1d", 
            interval="1m", 
            auto_adjust=True, 
            group_by="ticker",
            progress=False
        )
    except Exception as e:
        logger.error(f"Failed to fetch data from yfinance: {e}")
        print(f"Checked {len(trades)} positions: 0 entries filled, 0 stops hit, 0 targets hit, {len(trades)} unchanged")
        return
        
    if data.empty:
        logger.warning("No data returned from yfinance.")
        print(f"Checked {len(trades)} positions: 0 entries filled, 0 stops hit, 0 targets hit, {len(trades)} unchanged")
        return
        
    entries_filled = 0
    stops_hit = 0
    targets_hit = 0
    unchanged = 0

    now_ny = datetime.now(NY_TZ)
    start_of_today = now_ny.replace(hour=0, minute=0, second=0, microsecond=0)

    for t in trades:
        trade_id = t['id']
        ticker = t['ticker']
        direction = t['direction']
        entry_price = t['entry_price']
        status = t['status']
        stop_loss = t.get('stop_loss')
        target_price = t.get('target_price')
        target_price_2 = t.get('target_price_2')
        qty = t['quantity']
        
        last_checked_str = t.get('last_checked_at')
        if last_checked_str:
            try:
                last_checked = pd.to_datetime(last_checked_str).to_pydatetime()
            except Exception:
                last_checked = start_of_today
        else:
            last_checked = start_of_today
            
        # Ensure last_checked is tz-aware for comparison
        if last_checked.tzinfo is None:
            last_checked = last_checked.replace(tzinfo=timezone.utc)
            
        try:
            # Handle multi-index columns from yfinance
            if len(tickers) == 1:
                # If only one ticker, yf may not return multi-level columns if group_by is ignored in some versions
                if isinstance(data.columns, pd.MultiIndex):
                    df = data[ticker].dropna(how='all')
                else:
                    df = data.dropna(how='all')
            else:
                if isinstance(data.columns, pd.MultiIndex) and ticker in data.columns.levels[0]:
                    df = data[ticker].dropna(how='all')
                else:
                    logger.warning(f"No data found in yfinance response for {ticker}")
                    unchanged += 1
                    continue
        except Exception as e:
            logger.error(f"Error extracting data for {ticker}: {e}")
            unchanged += 1
            continue
            
        if df.empty:
            logger.warning(f"Data empty for {ticker}")
            unchanged += 1
            continue

        initial_status = status
        latest_bar_time = None
        has_fill = False
        
        for idx, row in df.iterrows():
            # If idx is just integer, we can't use it as datetime. (unlikely with yfinance)
            try:
                bar_time = idx.to_pydatetime()
            except AttributeError:
                continue

            if bar_time.tzinfo is None:
                bar_time = NY_TZ.localize(bar_time)
                
            if bar_time <= last_checked:
                continue
                
            if not is_market_hours(bar_time):
                continue
                
            latest_bar_time = bar_time
            try:
                low = float(row['Low'])
                high = float(row['High'])
            except KeyError:
                continue
                
            bar_timestamp_str = bar_time.isoformat()
            
            # 1. Check entries for pending (with entry tolerance band)
            if status == 'pending':
                tolerance_pct = t.get('entry_tolerance_pct') or 1.0
                if direction == 'long':
                    entry_max = entry_price * (1 + tolerance_pct / 100.0)
                    if low <= entry_max:
                        fill_price = max(low, entry_price)  # ideal or worse-within-tolerance
                        status = 'entered'
                        has_fill = True
                        entries_filled += 1
                        if not dry_run:
                            update_trade(trade_id, status='entered', entered_at=bar_timestamp_str, entry_fill_price=fill_price)
                            reason = "long entry hit" if fill_price <= entry_price else f"long entry filled within tolerance ({tolerance_pct}%)"
                            log_fill(trade_id, "entry_filled", fill_price, bar_timestamp_str, reason)
                elif direction == 'short':
                    entry_min = entry_price * (1 - tolerance_pct / 100.0)
                    if high >= entry_min:
                        fill_price = min(high, entry_price)  # ideal or worse-within-tolerance
                        status = 'entered'
                        has_fill = True
                        entries_filled += 1
                        if not dry_run:
                            update_trade(trade_id, status='entered', entered_at=bar_timestamp_str, entry_fill_price=fill_price)
                            reason = "short entry hit" if fill_price >= entry_price else f"short entry filled within tolerance ({tolerance_pct}%)"
                            log_fill(trade_id, "entry_filled", fill_price, bar_timestamp_str, reason)

            # 2. Check stops/targets for entered
            if status == 'entered':
                if direction == 'long':
                    if stop_loss is not None and low <= stop_loss:
                        status = 'stop_hit'
                        has_fill = True
                        stops_hit += 1
                        if not dry_run:
                            pnl = (stop_loss - entry_price) * qty
                            update_trade(trade_id, status='stop_hit', closed_at=bar_timestamp_str, exit_fill_price=stop_loss, pnl=pnl)
                            log_fill(trade_id, "stop_hit", stop_loss, bar_timestamp_str, "long stop loss hit")
                        break
                    elif target_price is not None and high >= target_price:
                        if target_price_2 is not None:
                            has_fill = True
                            if not dry_run:
                                update_trade(trade_id, stop_loss=entry_price, target_price=target_price_2, target_price_2=None)
                                log_fill(trade_id, "target_hit", target_price, bar_timestamp_str, "long target 1 hit, trailing stop to entry")
                            stop_loss = entry_price
                            target_price = target_price_2
                            target_price_2 = None
                        else:
                            status = 'target_hit'
                            has_fill = True
                            targets_hit += 1
                            if not dry_run:
                                pnl = (target_price - entry_price) * qty
                                update_trade(trade_id, status='target_hit', closed_at=bar_timestamp_str, exit_fill_price=target_price, pnl=pnl)
                                log_fill(trade_id, "target_hit", target_price, bar_timestamp_str, "long target hit")
                            break
                            
                elif direction == 'short':
                    if stop_loss is not None and high >= stop_loss:
                        status = 'stop_hit'
                        has_fill = True
                        stops_hit += 1
                        if not dry_run:
                            pnl = (entry_price - stop_loss) * qty
                            update_trade(trade_id, status='stop_hit', closed_at=bar_timestamp_str, exit_fill_price=stop_loss, pnl=pnl)
                            log_fill(trade_id, "stop_hit", stop_loss, bar_timestamp_str, "short stop loss hit")
                        break
                    elif target_price is not None and low <= target_price:
                        if target_price_2 is not None:
                            has_fill = True
                            if not dry_run:
                                update_trade(trade_id, stop_loss=entry_price, target_price=target_price_2, target_price_2=None)
                                log_fill(trade_id, "target_hit", target_price, bar_timestamp_str, "short target 1 hit, trailing stop to entry")
                            stop_loss = entry_price
                            target_price = target_price_2
                            target_price_2 = None
                        else:
                            status = 'target_hit'
                            has_fill = True
                            targets_hit += 1
                            if not dry_run:
                                pnl = (entry_price - target_price) * qty
                                update_trade(trade_id, status='target_hit', closed_at=bar_timestamp_str, exit_fill_price=target_price, pnl=pnl)
                                log_fill(trade_id, "target_hit", target_price, bar_timestamp_str, "short target hit")
                            break

        if not has_fill:
            unchanged += 1
            
        if latest_bar_time is not None and not dry_run:
            update_trade(trade_id, last_checked_at=latest_bar_time.isoformat())

    print(f"Checked {len(trades)} positions: {entries_filled} entries filled, {stops_hit} stops hit, {targets_hit} targets hit, {unchanged} unchanged")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Fill Engine Simulator")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing to Turso")
    args = parser.parse_args()
    
    run_simulator(dry_run=args.dry_run)
