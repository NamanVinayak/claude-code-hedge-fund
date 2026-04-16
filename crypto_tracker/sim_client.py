"""Simulated exchange client for crypto paper trading.

Same interface as tracker/moomoo_client.py so we can swap to a real exchange later.
All methods create/update SimOrder records in the DB — no external API calls.
"""

from datetime import datetime
from crypto_tracker.db import get_session, SimOrder


class SimClient:
    def __init__(self):
        self.session = get_session()

    def _create_order(self, ticker, side, qty, price, order_type, trade_id=None):
        """Create a SimOrder record and return its ID."""
        order = SimOrder(
            trade_id=trade_id,
            ticker=ticker,
            side=side,
            quantity=qty,
            price=price,
            order_type=order_type,
            status='pending',
        )
        self.session.add(order)
        self.session.commit()
        return str(order.id)

    def place_entry(self, ticker, side, qty, price):
        """Place limit entry order. side='long' or 'short'."""
        order_side = 'buy' if side == 'long' else 'sell'
        return self._create_order(ticker, order_side, qty, price, 'entry')

    def place_market_entry(self, ticker, side, qty):
        """Place market entry order (filled immediately by watcher at current price)."""
        order_side = 'buy' if side == 'long' else 'sell'
        return self._create_order(ticker, order_side, qty, None, 'market_entry')

    def place_stop(self, ticker, side, qty, price):
        """Place stop loss. side is the ENTRY side — stop goes opposite."""
        order_side = 'sell' if side == 'long' else 'buy'
        return self._create_order(ticker, order_side, qty, price, 'stop')

    def place_target(self, ticker, side, qty, price):
        """Place take-profit. side is the ENTRY side — target goes opposite."""
        order_side = 'sell' if side == 'long' else 'buy'
        return self._create_order(ticker, order_side, qty, price, 'target')

    def cancel_order(self, order_id):
        """Cancel a specific order."""
        try:
            order = self.session.query(SimOrder).get(int(order_id))
            if order and order.status == 'pending':
                order.status = 'cancelled'
                self.session.commit()
        except Exception:
            pass

    def fill_order(self, order_id, fill_price):
        """Mark an order as filled at the given price."""
        order = self.session.query(SimOrder).get(int(order_id))
        if order and order.status == 'pending':
            order.status = 'filled'
            order.fill_price = fill_price
            order.filled_at = datetime.utcnow()
            self.session.commit()

    def get_orders(self):
        """Return all orders as list of dicts."""
        orders = self.session.query(SimOrder).all()
        return [
            {
                'id': o.id, 'trade_id': o.trade_id, 'ticker': o.ticker,
                'side': o.side, 'quantity': o.quantity, 'price': o.price,
                'order_type': o.order_type, 'status': o.status,
                'fill_price': o.fill_price,
            }
            for o in orders
        ]

    def get_pending_orders(self):
        """Return pending orders as list of SimOrder objects."""
        return self.session.query(SimOrder).filter(SimOrder.status == 'pending').all()

    def get_positions(self):
        """Derive open positions from Trade status in DB."""
        from crypto_tracker.db import Trade
        trades = self.session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).all()
        return [
            {
                'ticker': t.ticker, 'direction': t.direction,
                'quantity': t.quantity, 'entry_price': t.entry_price,
                'status': t.status,
            }
            for t in trades
        ]

    def close(self):
        """No-op for simulated client."""
        self.session.close()
