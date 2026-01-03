from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from ..core.database import Base


class Watchlist(Base):
    """Watchlist model for storing user's tracked stocks."""

    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False, index=True)
    company_name = Column(String(200))

    # Additional metadata
    notes = Column(String(500))
    alert_threshold = Column(JSON)  # Store custom alert rules

    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="watchlists")

    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, ticker={self.ticker})>"


class QueryHistory(Base):
    """Query history model for tracking user queries and agent responses."""

    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    query_type = Column(String(50), nullable=False)  # market_analysis, news_sentiment, risk_assessment
    query_params = Column(JSON)  # Store query parameters (tickers, date ranges, etc.)

    agent_response = Column(JSON)  # Store structured agent response
    response_summary = Column(String(1000))  # Human-readable summary

    execution_time_ms = Column(Integer)  # Track query performance

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="query_history")

    def __repr__(self):
        return f"<QueryHistory(id={self.id}, user_id={self.user_id}, query_type={self.query_type})>"
