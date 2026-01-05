from typing import Dict, Any, List
import logging
import os

from phi.assistant import Assistant
from phi.llm.google import Gemini

from ..core.config import settings
from ..services.stock_stream import stock_stream_manager

logger = logging.getLogger(__name__)

# Set environment variable for Google Generativeai library
os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY


class MarketDataAgent:
    """Agent for analyzing market data and price movements."""

    def __init__(self):
        self.agent = Assistant(
            name="Comprehensive Market Analyst",
            llm=Gemini(model="gemini-2.0-flash-exp"),
            description="Expert in comprehensive stock analysis including price action, technical indicators, volume analysis, and risk assessment",
            instructions=[
                "Provide DETAILED analysis with specific insights and actionable information",
                "Analyze price trends, support/resistance levels, and volume patterns",
                "Evaluate momentum indicators and trend strength",
                "Include risk factors and volatility analysis",
                "Provide clear, structured explanations with bullet points",
                "Use professional financial terminology",
                "Always be specific with numbers and percentages",
                "Give both short-term and longer-term perspectives",
                "Focus on factual, data-driven analysis with comprehensive reasoning"
            ],
            markdown=True,
            show_tool_calls=False
        )

    async def analyze_price_action(
        self,
        ticker: str,
        price_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze price action for a given ticker.

        Args:
            ticker: Stock ticker symbol
            price_data: Current and historical price data

        Returns:
            Analysis results with insights and confidence score
        """
        try:
            prompt = f"""
Analyze the following price data for {ticker}:

Current Price: ${price_data.get('current_price', 'N/A')}
Change: {price_data.get('change', 'N/A')} ({price_data.get('change_percent', 'N/A')}%)
Volume: {price_data.get('volume', 'N/A')}
Open: ${price_data.get('open', 'N/A')}
High: ${price_data.get('high', 'N/A')}
Low: ${price_data.get('low', 'N/A')}

Provide a concise technical analysis including:
1. Price trend (bullish/bearish/neutral)
2. Volume analysis
3. Key support/resistance levels if apparent
4. Overall market strength indicator
5. Your confidence level (0-1)

Keep your response structured and under 200 words.
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

            # Extract confidence from response or default
            confidence = self._extract_confidence(response_text)

            return {
                "agent_name": "Market Data Agent",
                "ticker": ticker,
                "analysis": response_text,
                "confidence": confidence,
                "data_points_analyzed": len(price_data),
                "reasoning": "Technical analysis based on price, volume, and trend patterns"
            }

        except Exception as e:
            logger.error(f"Market agent analysis error for {ticker}: {e}")
            return {
                "agent_name": "Market Data Agent",
                "ticker": ticker,
                "analysis": f"Unable to perform analysis: {str(e)[:100]}",
                "confidence": 0.0,
                "reasoning": "Analysis failed due to API error",
                "error": str(e)
            }

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

        return 0.7

    async def get_market_snapshot(self, tickers: List[str]) -> Dict[str, Any]:
        """Get a quick market snapshot for multiple tickers."""
        snapshots = {}

        for ticker in tickers:
            quote = await stock_stream_manager.get_quote(ticker)
            if quote:
                snapshots[ticker] = {
                    "price": quote.price,
                    "volume": quote.volume,
                    "change": quote.change,
                    "change_percent": quote.change_percent,
                    "timestamp": quote.timestamp.isoformat()
                }

        return snapshots


# Global instance
market_agent = MarketDataAgent()
