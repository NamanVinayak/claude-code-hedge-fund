from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

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
    status = Column(String, default='pending')  # pending/entered/target_hit/stop_hit/expired/cancelled
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


def get_available_cash():
    """Calculate available cash from DB state."""
    import json
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
    with open(watchlist_path) as f:
        config = json.load(f)
    base = config['settings']['paper_account_size']  # 1000

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
