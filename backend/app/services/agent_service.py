from typing import Dict, Any, List
import logging
import time
from datetime import datetime

from ..agents import market_agent, news_agent
from ..schemas.market import AIQueryRequest, AIQueryResponse, AgentInsight, QueryType
from .stock_stream import stock_stream_manager

logger = logging.getLogger(__name__)


class AgentOrchestrationService:
    """Optimized service for fast financial analysis with detailed responses."""

    async def execute_query(self, query_request: AIQueryRequest) -> AIQueryResponse:
        """
        Execute an AI query with optimized performance.

        Args:
            query_request: The query request with tickers and query type

        Returns:
            Comprehensive AI query response
        """
        start_time = time.time()

        try:
            insights = []
            tickers = query_request.tickers

            try:
                # Simplified: Only 2 query types for faster performance
                if query_request.query_type in [QueryType.MARKET_ANALYSIS, QueryType.RISK_ASSESSMENT, QueryType.DECISION_SYNTHESIS]:
                    # Combined market + risk analysis in one call
                    insights = await self._run_comprehensive_market_analysis(tickers)

                elif query_request.query_type == QueryType.NEWS_SENTIMENT:
                    insights = await self._run_news_sentiment_analysis(tickers)

            except Exception as e:
                logger.error(f"Agent execution error: {e}")
                return AIQueryResponse(
                    query_id=int(time.time()),
                    query_type=query_request.query_type,
                    tickers=tickers,
                    insights=[],
                    synthesis=f"AI Analysis temporarily unavailable. Please check your API quota or try again later.",
                    risk_level="unknown",
                    execution_time_ms=int((time.time() - start_time) * 1000),
                    timestamp=datetime.utcnow()
                )

            execution_time_ms = int((time.time() - start_time) * 1000)

            synthesis = insights[-1].summary if insights else "No insights generated"
            risk_level = self._determine_overall_risk(insights)

            return AIQueryResponse(
                query_id=int(time.time()),
                query_type=query_request.query_type,
                tickers=tickers,
                insights=insights,
                synthesis=synthesis,
                risk_level=risk_level,
                execution_time_ms=execution_time_ms,
                timestamp=datetime.utcnow()
            )

        except Exception as e:
            logger.error(f"Agent orchestration error: {e}")
            raise

    async def _run_comprehensive_market_analysis(self, tickers: List[str]) -> List[AgentInsight]:
        """
        Run comprehensive market + risk analysis in one call (OPTIMIZED).
        Combines market analysis and risk assessment for better performance.
        """
        insights = []

        for ticker in tickers:
            quote = await stock_stream_manager.get_quote(ticker)

            if quote:
                # Enhanced price data with risk indicators
                price_data = {
                    "current_price": quote.price,
                    "volume": quote.volume,
                    "change": quote.change,
                    "change_percent": quote.change_percent,
                    "open": quote.open,
                    "high": quote.high,
                    "low": quote.low,
                    # Calculate additional metrics
                    "price_range": quote.high - quote.low,
                    "volatility_pct": ((quote.high - quote.low) / quote.open * 100) if quote.open > 0 else 0,
                    "intraday_trend": "bullish" if quote.price > quote.open else "bearish",
                }

                # Single comprehensive prompt for detailed analysis
                result = await market_agent.analyze_price_action(ticker, price_data)

                # Enhanced reasoning with risk assessment
                enhanced_reasoning = f"{result['reasoning']}\n\n"
                enhanced_reasoning += f"**Risk Indicators:**\n"
                enhanced_reasoning += f"- Price Volatility: {price_data['volatility_pct']:.2f}%\n"
                enhanced_reasoning += f"- Intraday Trend: {price_data['intraday_trend'].title()}\n"
                enhanced_reasoning += f"- Price Change: {quote.change_percent:+.2f}%\n"

                # Determine risk level based on volatility and change
                if abs(quote.change_percent) > 5 or price_data['volatility_pct'] > 5:
                    risk_level = "high"
                    risk_note = "High volatility detected. Consider careful position sizing."
                elif abs(quote.change_percent) > 2 or price_data['volatility_pct'] > 3:
                    risk_level = "medium"
                    risk_note = "Moderate price movement. Monitor closely."
                else:
                    risk_level = "low"
                    risk_note = "Stable price action within normal range."

                enhanced_reasoning += f"- Risk Level: {risk_level.upper()}\n- {risk_note}"

                insights.append(AgentInsight(
                    agent_name="Comprehensive Market Analyst",
                    confidence=result["confidence"],
                    summary=result["analysis"],
                    details={
                        "ticker": ticker,
                        "price_data": price_data,
                        "risk_level": risk_level
                    },
                    reasoning=enhanced_reasoning
                ))

        return insights

    async def _run_news_sentiment_analysis(self, tickers: List[str]) -> List[AgentInsight]:
        """Run comprehensive news sentiment analysis."""
        insights = []

        for ticker in tickers:
            result = await news_agent.analyze_news_sentiment(ticker, days_back=7)

            # Enhanced summary with more detail
            enhanced_summary = result["summary"]
            if result["article_count"] > 0:
                enhanced_summary += f"\n\n📊 Analysis of {result['article_count']} recent articles shows "
                enhanced_summary += f"{result['sentiment'].upper()} sentiment. "

                # Add sentiment interpretation
                sentiment_map = {
                    "bullish": "Positive news flow may support upward price momentum.",
                    "bearish": "Negative coverage could create downward pressure.",
                    "neutral": "Mixed signals suggest waiting for clearer direction.",
                    "mixed": "Conflicting signals require careful monitoring."
                }
                enhanced_summary += sentiment_map.get(result['sentiment'].lower(), "")

            insights.append(AgentInsight(
                agent_name="News Sentiment Analyst",
                confidence=result["confidence"],
                summary=enhanced_summary,
                details={
                    "ticker": ticker,
                    "sentiment": result["sentiment"],
                    "article_count": result["article_count"]
                },
                reasoning=result["reasoning"]
            ))

        return insights

    def _determine_overall_risk(self, insights: List[AgentInsight]) -> str:
        """Determine overall risk level from insights."""
        risk_counts = {"low": 0, "medium": 0, "high": 0, "unknown": 0}

        for insight in insights:
            risk_level = insight.details.get("risk_level", "unknown")
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1

        if risk_counts["high"] > 0:
            return "high"
        elif risk_counts["medium"] > risk_counts["low"]:
            return "medium"
        else:
            return "low"


# Global instance
agent_orchestration_service = AgentOrchestrationService()
