from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'crypto_tracker.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Trade(Base):
    __tablename__ = 'crypto_trades'
    id = Column(Integer, primary_key=True)
    run_id = Column(String, nullable=False)
    mode = Column(String, nullable=False)  # swing or daytrade
    ticker = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # long or short
    quantity = Column(Float, nullable=False)  # float for fractional crypto
    entry_price = Column(Float, nullable=False)
    target_price = Column(Float)
    target_price_2 = Column(Float)
    stop_loss = Column(Float)
    confidence = Column(Integer)
    timeframe = Column(String)
    entry_order_id = Column(String)
    stop_order_id = Column(String)
    target_order_id = Column(String)
    status = Column(String, default='pending')  # pending/entered/target_hit/stop_hit/expired/cancelled
    entry_fill_price = Column(Float)
    exit_fill_price = Column(Float)
    pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    entered_at = Column(DateTime)
    closed_at = Column(DateTime)
    raw_decision = Column(Text)


class SimOrder(Base):
    __tablename__ = 'crypto_sim_orders'
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, ForeignKey('crypto_trades.id'), nullable=True)
    ticker = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy or sell
    quantity = Column(Float, nullable=False)
    price = Column(Float)  # None for market orders
    order_type = Column(String, nullable=False)  # entry/stop/target/market_entry
    status = Column(String, default='pending')  # pending/filled/cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    filled_at = Column(DateTime)
    fill_price = Column(Float)


class DailySummary(Base):
    __tablename__ = 'crypto_daily_summary'
    id = Column(Integer, primary_key=True)
    date = Column(String, unique=True)
    total_trades = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    total_pnl = Column(Float, default=0.0)
    open_positions = Column(Integer, default=0)


def create_tables():
    Base.metadata.create_all(engine)


def get_session():
    create_tables()
    return Session()


def get_open_crypto_positions():
    """Return all currently-entered crypto positions as plain dicts.

    Used by the aggregator to inject real portfolio state into the crypto PM
    prompt. Only rows with status == 'entered' are returned (NOT 'pending',
    NOT closed). Quantities are floats since crypto supports fractional sizes.
    """
    session = get_session()
    rows = session.query(Trade).filter(Trade.status == 'entered').all()
    out = [
        {
            "ticker": t.ticker,
            "direction": t.direction,
            "quantity": t.quantity,
            "entry_fill_price": t.entry_fill_price,
            "entry_price": t.entry_price,
            "stop_loss": t.stop_loss,
            "target_price": t.target_price,
            "mode": t.mode,
            "run_id": t.run_id,
            "entered_at": t.entered_at.isoformat() if t.entered_at else None,
        }
        for t in rows
    ]
    session.close()
    return out


def get_available_cash():
    """Calculate available cash from DB state."""
    import json
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    base = config['settings']['paper_account_size']

    session = get_session()
    closed = session.query(Trade).filter(Trade.status.in_(['target_hit', 'stop_hit', 'expired'])).all()
    realized_pnl = sum(t.pnl or 0 for t in closed)
    open_trades = session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).all()
    open_exposure = sum(t.entry_price * t.quantity for t in open_trades)
    session.close()

    available = base + realized_pnl - open_exposure
    return max(0, available)
