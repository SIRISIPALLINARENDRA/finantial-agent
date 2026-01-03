from typing import Dict, Any, List
import logging
import os

from phi.assistant import Assistant
from phi.llm.google import Gemini

from ..core.config import settings

logger = logging.getLogger(__name__)

# Set environment variable for Google Generativeai library
os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY


class RiskAndESGAgent:
    """Agent for risk assessment and ESG (Environmental, Social, Governance) analysis."""

    def __init__(self):
        self.agent = Assistant(
            name="Risk & ESG Analyst",
            llm=Gemini(model="gemini-2.5-flash"),
            description="Specialized in risk assessment, volatility analysis, and ESG considerations",
            instructions=[
                "Evaluate market and company-specific risks",
                "Assess volatility and downside potential",
                "Consider ESG factors and sustainability",
                "Identify regulatory and compliance risks",
                "Provide risk-adjusted perspectives",
                "Emphasize responsible investing principles"
            ],
            markdown=True,
            show_tool_calls=False
        )

    async def assess_risk(
        self,
        ticker: str,
        market_data: Dict[str, Any],
        news_sentiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess investment risk for a ticker.

        Args:
            ticker: Stock ticker symbol
            market_data: Current market data and price action
            news_sentiment: Sentiment analysis from news

        Returns:
            Risk assessment with recommendations
        """
        try:
            prompt = f"""
Perform a risk assessment for {ticker} based on the following:

Market Data:
- Current Price: ${market_data.get('current_price', 'N/A')}
- Volatility: {market_data.get('volatility', 'N/A')}
- Volume: {market_data.get('volume', 'N/A')}
- Price Change: {market_data.get('change_percent', 'N/A')}%

Sentiment Analysis:
- Overall Sentiment: {news_sentiment.get('sentiment', 'N/A')}
- Confidence: {news_sentiment.get('confidence', 'N/A')}

Provide a comprehensive risk assessment including:
1. Overall risk level (low/medium/high)
2. Key risk factors
3. Volatility assessment
4. Downside potential
5. Risk mitigation suggestions
6. Confidence in assessment (0-1)

Focus on actionable, responsible investment guidance (under 250 words).
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

            risk_level = self._extract_risk_level(response_text)
            confidence = self._extract_confidence(response_text)

            return {
                "agent_name": "Risk & ESG Agent",
                "ticker": ticker,
                "risk_level": risk_level,
                "confidence": confidence,
                "assessment": response_text,
                "reasoning": "Risk analysis based on volatility, market conditions, and sentiment"
            }

        except Exception as e:
            logger.error(f"Risk agent analysis error for {ticker}: {e}")
            return {
                "agent_name": "Risk & ESG Agent",
                "ticker": ticker,
                "risk_level": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }

    async def evaluate_esg_factors(self, ticker: str) -> Dict[str, Any]:
        """
        Evaluate ESG (Environmental, Social, Governance) factors.

        Args:
            ticker: Stock ticker symbol

        Returns:
            ESG evaluation
        """
        try:
            prompt = f"""
Provide a general ESG (Environmental, Social, Governance) perspective for {ticker}.

Consider:
1. Environmental impact and sustainability
2. Social responsibility and community impact
3. Governance structure and corporate ethics
4. Overall ESG risk level

Note: This is a high-level assessment. For detailed ESG scores, consult specialized ESG rating agencies.

Keep response under 200 words.
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

            return {
                "agent_name": "Risk & ESG Agent",
                "ticker": ticker,
                "esg_perspective": response_text,
                "disclaimer": "High-level assessment. Consult ESG rating agencies for detailed scores."
            }

        except Exception as e:
            logger.error(f"ESG evaluation error for {ticker}: {e}")
            return {
                "agent_name": "Risk & ESG Agent",
                "ticker": ticker,
                "error": str(e)
            }

    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from agent response."""
        text_lower = text.lower()

        if "high risk" in text_lower or "risk level: high" in text_lower:
            return "high"
        elif "low risk" in text_lower or "risk level: low" in text_lower:
            return "low"
        elif "medium risk" in text_lower or "risk level: medium" in text_lower:
            return "medium"
        else:
            return "medium"

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


# Global instance
risk_agent = RiskAndESGAgent()
