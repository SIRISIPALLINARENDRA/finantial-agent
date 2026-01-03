import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)


class NewsService:
    """Service for fetching financial news and sentiment data."""

    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"

    async def get_stock_news(
        self,
        ticker: str,
        days_back: int = 7,
        max_articles: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles related to a specific stock ticker.

        Args:
            ticker: Stock ticker symbol
            days_back: Number of days to look back for news
            max_articles: Maximum number of articles to return

        Returns:
            List of news articles with metadata
        """
        try:
            from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

            params = {
                "q": ticker,
                "from": from_date,
                "sortBy": "relevancy",
                "pageSize": max_articles,
                "apiKey": self.api_key,
                "language": "en"
            }

            import ssl

            # Create SSL context that doesn't verify certificates (for development)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(f"{self.base_url}/everything", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])

                        # Process and structure articles
                        processed_articles = []
                        for article in articles:
                            processed_articles.append({
                                "title": article.get("title"),
                                "description": article.get("description"),
                                "source": article.get("source", {}).get("name"),
                                "url": article.get("url"),
                                "published_at": article.get("publishedAt"),
                                "content": article.get("content", "")[:500]  # Truncate for efficiency
                            })

                        return processed_articles
                    else:
                        logger.error(f"News API error: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []

    async def get_market_news(
        self,
        category: str = "business",
        max_articles: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch general market/financial news.

        Args:
            category: News category (business, technology, etc.)
            max_articles: Maximum number of articles to return

        Returns:
            List of news articles
        """
        try:
            params = {
                "category": category,
                "pageSize": max_articles,
                "apiKey": self.api_key,
                "country": "us"
            }

            import ssl

            # Create SSL context that doesn't verify certificates (for development)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(f"{self.base_url}/top-headlines", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("articles", [])
                    else:
                        logger.error(f"News API error: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Error fetching market news: {e}")
            return []

    def calculate_simple_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Calculate simple sentiment score for text.
        In production, use a proper sentiment analysis model.

        Args:
            text: Text to analyze

        Returns:
            Sentiment analysis result
        """
        positive_words = [
            "growth", "profit", "gain", "surge", "rally", "bullish",
            "positive", "strong", "beat", "outperform", "success"
        ]
        negative_words = [
            "loss", "decline", "fall", "drop", "bearish", "negative",
            "weak", "miss", "underperform", "risk", "concern"
        ]

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (positive_count - negative_count) / total

        if sentiment_score > 0.2:
            sentiment_label = "positive"
        elif sentiment_score < -0.2:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        return {
            "score": sentiment_score,
            "label": sentiment_label,
            "positive_mentions": positive_count,
            "negative_mentions": negative_count
        }


# Global instance
news_service = NewsService()
