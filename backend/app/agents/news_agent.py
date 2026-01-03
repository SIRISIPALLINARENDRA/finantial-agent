from typing import Dict, Any, List
import logging
import os

from phi.assistant import Assistant
from phi.llm.google import Gemini

from ..core.config import settings
from ..services.news_service import news_service

logger = logging.getLogger(__name__)

# Set environment variable for Google Generativeai library
os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY


class NewsAndSentimentAgent:
    """Agent for analyzing news and market sentiment."""

    def __init__(self):
        self.agent = Assistant(
            name="News & Sentiment Analyst",
            llm=Gemini(model="gemini-2.5-flash"),
            description="Specialized in analyzing financial news and market sentiment",
            instructions=[
                "Analyze news articles for market impact",
                "Evaluate sentiment (bullish, bearish, neutral)",
                "Identify key themes and narratives",
                "Assess credibility and relevance of sources",
                "Provide balanced, objective analysis",
                "Consider both short-term and long-term implications"
            ],
            markdown=True,
            show_tool_calls=False
        )

    async def analyze_news_sentiment(
        self,
        ticker: str,
        days_back: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze news sentiment for a ticker.

        Args:
            ticker: Stock ticker symbol
            days_back: Number of days to look back for news

        Returns:
            Sentiment analysis with key insights
        """
        try:
            articles = await news_service.get_stock_news(ticker, days_back=days_back, max_articles=15)

            if not articles:
                return {
                    "agent_name": "News & Sentiment Agent",
                    "ticker": ticker,
                    "sentiment": "neutral",
                    "confidence": 0.3,
                    "summary": "Insufficient news data for analysis",
                    "article_count": 0
                }

            # Prepare news summary for agent
            news_summary = self._prepare_news_summary(articles)

            prompt = f"""
Analyze the following recent news articles for {ticker}:

{news_summary}

Provide a sentiment analysis including:
1. Overall sentiment (bullish/bearish/neutral)
2. Key themes and narratives
3. Potential market impact
4. Confidence level (0-1)
5. Notable concerns or opportunities

Keep your response concise and actionable (under 250 words).
"""

            response = self.agent.run(prompt)

            # Get response content (handle generator)
            response_text = ""
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                # Response is a generator, collect all chunks
                for chunk in response:
                    if hasattr(chunk, 'content'):
                        response_text += chunk.content

            sentiment = self._extract_sentiment(response_text)
            confidence = self._extract_confidence(response_text)

            return {
                "agent_name": "News & Sentiment Agent",
                "ticker": ticker,
                "sentiment": sentiment,
                "confidence": confidence,
                "summary": response_text,
                "article_count": len(articles),
                "reasoning": "Analysis based on recent news articles and market narratives"
            }

        except Exception as e:
            logger.error(f"News agent analysis error for {ticker}: {e}")
            return {
                "agent_name": "News & Sentiment Agent",
                "ticker": ticker,
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }

    def _prepare_news_summary(self, articles: List[Dict[str, Any]]) -> str:
        """Prepare a concise summary of articles for the agent."""
        summaries = []

        for i, article in enumerate(articles[:10], 1):
            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get("source", "Unknown")

            summaries.append(f"{i}. [{source}] {title}\n   {description[:150]}...")

        return "\n\n".join(summaries)

    def _extract_sentiment(self, text: str) -> str:
        """Extract sentiment label from agent response."""
        text_lower = text.lower()

        if "bullish" in text_lower or "positive" in text_lower:
            return "bullish"
        elif "bearish" in text_lower or "negative" in text_lower:
            return "bearish"
        else:
            return "neutral"

    def _extract_confidence(self, text: str) -> float:
        """Extract confidence score from agent response."""
        import re

        confidence_pattern = r'confidence[:\s]+([0-9.]+)'
        match = re.search(confidence_pattern, text.lower())

        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass

        return 0.65


# Global instance
news_agent = NewsAndSentimentAgent()
