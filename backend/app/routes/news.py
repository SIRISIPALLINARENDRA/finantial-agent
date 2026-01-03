from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
import logging

from ..core.security import get_current_active_user
from ..models.user import User
from ..services.news_service import news_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/news", tags=["News"])


@router.get("/financial", response_model=List[Dict[str, Any]])
async def get_financial_news(
    category: Optional[str] = Query(default="business", description="News category: business, technology, etc."),
    max_articles: int = Query(default=30, le=100, description="Maximum articles to fetch"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get general financial and business news.

    Args:
        category: News category (business, technology, etc.)
        max_articles: Maximum number of articles to return
        current_user: Authenticated user

    Returns:
        List of financial news articles
    """
    try:
        articles = await news_service.get_market_news(
            category=category,
            max_articles=max_articles
        )

        logger.info(f"User {current_user.username} fetched {len(articles)} financial news articles")
        return articles

    except Exception as e:
        logger.error(f"Error fetching financial news: {e}")
        return []


@router.get("/search", response_model=List[Dict[str, Any]])
async def search_news(
    query: str = Query(..., description="Search query (stock ticker, company name, topic)"),
    days_back: int = Query(default=7, le=30, description="Days to look back"),
    max_articles: int = Query(default=20, le=100, description="Maximum articles to fetch"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search for news articles by query (ticker, company, topic).

    Args:
        query: Search query (e.g., "AAPL", "Tesla", "cryptocurrency")
        days_back: Number of days to look back
        max_articles: Maximum number of articles to return
        current_user: Authenticated user

    Returns:
        List of news articles matching the query
    """
    try:
        articles = await news_service.get_stock_news(
            ticker=query,
            days_back=days_back,
            max_articles=max_articles
        )

        logger.info(f"User {current_user.username} searched news for '{query}': {len(articles)} results")
        return articles

    except Exception as e:
        logger.error(f"Error searching news for {query}: {e}")
        return []


@router.get("/topics/{topic}", response_model=List[Dict[str, Any]])
async def get_topic_news(
    topic: str,
    days_back: int = Query(default=7, le=30, description="Days to look back"),
    max_articles: int = Query(default=20, le=100, description="Maximum articles to fetch"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get news for specific topics (stocks, crypto, forex, commodities).

    Args:
        topic: Topic (stocks, crypto, bitcoin, ethereum, gold, oil, etc.)
        days_back: Number of days to look back
        max_articles: Maximum number of articles to return
        current_user: Authenticated user

    Returns:
        List of news articles for the topic
    """
    try:
        # Map topics to search queries
        topic_queries = {
            "stocks": "stock market",
            "crypto": "cryptocurrency bitcoin ethereum",
            "bitcoin": "bitcoin BTC",
            "ethereum": "ethereum ETH",
            "forex": "forex currency exchange",
            "commodities": "commodities gold oil",
            "gold": "gold commodity",
            "oil": "crude oil",
            "tech": "technology stocks",
            "finance": "finance financial markets"
        }

        search_query = topic_queries.get(topic.lower(), topic)

        articles = await news_service.get_stock_news(
            ticker=search_query,
            days_back=days_back,
            max_articles=max_articles
        )

        logger.info(f"User {current_user.username} fetched {len(articles)} articles for topic '{topic}'")
        return articles

    except Exception as e:
        logger.error(f"Error fetching news for topic {topic}: {e}")
        return []
