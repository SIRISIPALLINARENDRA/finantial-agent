from typing import Dict, Any, List
import logging
import os

from phi.assistant import Assistant
from phi.llm.google import Gemini

from ..core.config import settings

logger = logging.getLogger(__name__)

# Set environment variable for Google Generativeai library
os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY


class DecisionSynthesisAgent:
    """Agent for synthesizing insights from multiple agents and providing decision support."""

    def __init__(self):
        self.agent = Assistant(
            name="Decision Synthesis Coordinator",
            llm=Gemini(model="gemini-2.5-flash"),
            description="Coordinates insights from all agents and provides synthesized decision support",
            instructions=[
                "Synthesize insights from multiple analytical perspectives",
                "Identify consensus and conflicting signals",
                "Provide balanced, holistic recommendations",
                "Emphasize explainability and transparency",
                "Always include risk disclaimers",
                "Focus on decision-support, not trading execution",
                "Maintain objectivity and responsible AI principles"
            ],
            markdown=True,
            show_tool_calls=False
        )

    async def synthesize_insights(
        self,
        ticker: str,
        market_analysis: Dict[str, Any],
        news_sentiment: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize insights from all agents.

        Args:
            ticker: Stock ticker symbol
            market_analysis: Market data agent analysis
            news_sentiment: News sentiment agent analysis
            risk_assessment: Risk agent assessment

        Returns:
            Synthesized decision support
        """
        try:
            prompt = f"""
Synthesize the following analyses for {ticker} into a coherent decision support summary:

MARKET ANALYSIS:
{market_analysis.get('analysis', 'N/A')}
Confidence: {market_analysis.get('confidence', 'N/A')}

NEWS & SENTIMENT:
{news_sentiment.get('summary', 'N/A')}
Sentiment: {news_sentiment.get('sentiment', 'N/A')}
Confidence: {news_sentiment.get('confidence', 'N/A')}

RISK ASSESSMENT:
{risk_assessment.get('assessment', 'N/A')}
Risk Level: {risk_assessment.get('risk_level', 'N/A')}
Confidence: {risk_assessment.get('confidence', 'N/A')}

Provide a synthesized decision support summary including:
1. Key consensus points across analyses
2. Conflicting signals or areas of uncertainty
3. Overall market outlook for this ticker
4. Recommended considerations for decision-making
5. Critical risk factors to monitor
6. Overall confidence in synthesis (0-1)

IMPORTANT: This is decision-support only. No trading recommendations. Emphasize responsible investing.

Keep response actionable and under 300 words.
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

            overall_confidence = self._calculate_weighted_confidence(
                market_analysis.get('confidence', 0.5),
                news_sentiment.get('confidence', 0.5),
                risk_assessment.get('confidence', 0.5)
            )

            overall_risk = risk_assessment.get('risk_level', 'medium')

            return {
                "agent_name": "Decision Synthesis Agent",
                "ticker": ticker,
                "synthesis": response_text,
                "overall_confidence": overall_confidence,
                "overall_risk": overall_risk,
                "reasoning": "Synthesized from market, sentiment, and risk analyses",
                "disclaimer": "This is decision-support analysis only. Not financial advice. Consult a qualified financial advisor."
            }

        except Exception as e:
            logger.error(f"Decision synthesis error for {ticker}: {e}")
            return {
                "agent_name": "Decision Synthesis Agent",
                "ticker": ticker,
                "synthesis": "Unable to synthesize insights",
                "overall_confidence": 0.0,
                "error": str(e)
            }

    def _calculate_weighted_confidence(self, *confidences: float) -> float:
        """Calculate weighted average confidence from multiple sources."""
        valid_confidences = [c for c in confidences if c > 0]

        if not valid_confidences:
            return 0.5

        return sum(valid_confidences) / len(valid_confidences)

    async def explain_decision_factors(
        self,
        ticker: str,
        all_insights: List[Dict[str, Any]]
    ) -> str:
        """
        Provide an explainable breakdown of decision factors.

        Args:
            ticker: Stock ticker symbol
            all_insights: All agent insights

        Returns:
            Human-readable explanation
        """
        factors = []

        for insight in all_insights:
            agent_name = insight.get('agent_name', 'Unknown')
            confidence = insight.get('confidence', 0.0)
            reasoning = insight.get('reasoning', '')

            factors.append(f"- {agent_name} (Confidence: {confidence:.2f}): {reasoning}")

        explanation = f"Decision factors for {ticker}:\n\n" + "\n".join(factors)
        explanation += "\n\nAll factors are considered with explainability and transparency in mind."

        return explanation


# Global instance
decision_agent = DecisionSynthesisAgent()
