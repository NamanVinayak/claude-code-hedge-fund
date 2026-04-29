from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'tracker.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    run_id = Column(String, nullable=False)
    mode = Column(String, nullable=False)  # swing or daytrade
    ticker = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # long or short
    quantity = Column(Integer, nullable=False)
    entry_price = Column(Float, nullable=False)
    target_price = Column(Float)
    target_price_2 = Column(Float)
    stop_loss = Column(Float)
    confidence = Column(Integer)
    timeframe = Column(String)
    entry_order_id = Column(String)
    stop_order_id = Column(String)
    target_order_id = Column(String)
    status = Column(String, default='pending')  # pending/entered/target_hit/stop_hit/expired/cancelled/abandoned
    entry_fill_price = Column(Float)
    exit_fill_price = Column(Float)
    pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    entered_at = Column(DateTime)
    closed_at = Column(DateTime)
    raw_decision = Column(Text)


class DailySummary(Base):
    __tablename__ = 'daily_summary'
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


def get_available_cash_for_mode(mode):
    """Calculate available cash for a specific mode (swing or daytrade)."""
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    budget = config['settings'].get(f'{mode}_budget', config['settings'].get('paper_account_size', 5000))

    session = get_session()
    open_trades = session.query(Trade).filter(
        Trade.mode == mode,
        Trade.status.in_(['pending', 'entered'])
    ).all()
    closed_trades = session.query(Trade).filter(
        Trade.mode == mode,
        Trade.status.in_(['target_hit', 'stop_hit', 'expired', 'closed'])
    ).all()
    session.close()

    open_exposure = sum(t.entry_price * t.quantity for t in open_trades)
    realized_pnl = sum(t.pnl or 0 for t in closed_trades)
    return max(0, budget + realized_pnl - open_exposure)


def get_open_positions():
    """Return all currently-entered stock positions as plain dicts.

    Used by the aggregator to inject real portfolio state into the PM prompt
    so it stops pretending every run starts with $100k of fresh cash.
    Only rows with status == 'entered' are returned (NOT 'pending', NOT closed).
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
    """Calculate available cash from DB state (global, all modes)."""
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    base = config['settings']['paper_account_size']

    session = get_session()
    # Add closed trade P&L
    closed = session.query(Trade).filter(Trade.status.in_(['target_hit', 'stop_hit', 'expired'])).all()
    realized_pnl = sum(t.pnl or 0 for t in closed)
    # Subtract open position values
    open_trades = session.query(Trade).filter(Trade.status.in_(['pending', 'entered'])).all()
    open_exposure = sum(t.entry_price * t.quantity for t in open_trades)
    session.close()

    available = base + realized_pnl - open_exposure
    return max(0, available)
