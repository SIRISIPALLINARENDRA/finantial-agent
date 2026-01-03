from typing import Dict, Any, List
import logging
import time
from datetime import datetime

from ..agents import market_agent, news_agent, risk_agent, decision_agent
from ..schemas.market import AIQueryRequest, AIQueryResponse, AgentInsight, QueryType
from .stock_stream import stock_stream_manager

logger = logging.getLogger(__name__)


class AgentOrchestrationService:
    """Service for orchestrating multi-agent financial analysis."""

    async def execute_query(self, query_request: AIQueryRequest) -> AIQueryResponse:
        """
        Execute an AI query by coordinating multiple agents.

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
                if query_request.query_type == QueryType.MARKET_ANALYSIS:
                    insights = await self._run_market_analysis(tickers)

                elif query_request.query_type == QueryType.NEWS_SENTIMENT:
                    insights = await self._run_news_sentiment_analysis(tickers)

                elif query_request.query_type == QueryType.RISK_ASSESSMENT:
                    insights = await self._run_risk_assessment(tickers)

                elif query_request.query_type == QueryType.DECISION_SYNTHESIS:
                    insights = await self._run_full_synthesis(tickers)

            except Exception as e:
                logger.error(f"Agent execution error: {e}")
                # Return error response
                return AIQueryResponse(
                    query_id=int(time.time()),
                    query_type=query_request.query_type,
                    tickers=tickers,
                    insights=[],
                    synthesis=f"AI Analysis temporarily unavailable: {str(e)[:200]}. Please check your API quota or try again later.",
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

    async def _run_market_analysis(self, tickers: List[str]) -> List[AgentInsight]:
        """Run market data analysis for tickers."""
        insights = []

        for ticker in tickers:
            quote = await stock_stream_manager.get_quote(ticker)

            if quote:
                price_data = {
                    "current_price": quote.price,
                    "volume": quote.volume,
                    "change": quote.change,
                    "change_percent": quote.change_percent,
                    "open": quote.open,
                    "high": quote.high,
                    "low": quote.low
                }

                result = await market_agent.analyze_price_action(ticker, price_data)

                insights.append(AgentInsight(
                    agent_name=result["agent_name"],
                    confidence=result["confidence"],
                    summary=result["analysis"],
                    details={"ticker": ticker, "price_data": price_data},
                    reasoning=result["reasoning"]
                ))

        return insights

    async def _run_news_sentiment_analysis(self, tickers: List[str]) -> List[AgentInsight]:
        """Run news sentiment analysis for tickers."""
        insights = []

        for ticker in tickers:
            result = await news_agent.analyze_news_sentiment(ticker, days_back=7)

            insights.append(AgentInsight(
                agent_name=result["agent_name"],
                confidence=result["confidence"],
                summary=result["summary"],
                details={
                    "ticker": ticker,
                    "sentiment": result["sentiment"],
                    "article_count": result["article_count"]
                },
                reasoning=result["reasoning"]
            ))

        return insights

    async def _run_risk_assessment(self, tickers: List[str]) -> List[AgentInsight]:
        """Run risk assessment for tickers."""
        insights = []

        for ticker in tickers:
            quote = await stock_stream_manager.get_quote(ticker)
            market_data = {}

            if quote:
                market_data = {
                    "current_price": quote.price,
                    "volume": quote.volume,
                    "change_percent": quote.change_percent
                }

            news_sentiment_result = await news_agent.analyze_news_sentiment(ticker, days_back=7)

            result = await risk_agent.assess_risk(ticker, market_data, news_sentiment_result)

            insights.append(AgentInsight(
                agent_name=result["agent_name"],
                confidence=result["confidence"],
                summary=result["assessment"],
                details={
                    "ticker": ticker,
                    "risk_level": result["risk_level"]
                },
                reasoning=result["reasoning"]
            ))

        return insights

    async def _run_full_synthesis(self, tickers: List[str]) -> List[AgentInsight]:
        """Run full multi-agent synthesis."""
        all_insights = []

        for ticker in tickers:
            quote = await stock_stream_manager.get_quote(ticker)
            market_data = {}

            if quote:
                market_data = {
                    "current_price": quote.price,
                    "volume": quote.volume,
                    "change": quote.change,
                    "change_percent": quote.change_percent,
                    "open": quote.open,
                    "high": quote.high,
                    "low": quote.low
                }

            market_analysis = await market_agent.analyze_price_action(ticker, market_data)
            news_sentiment = await news_agent.analyze_news_sentiment(ticker, days_back=7)
            risk_assessment = await risk_agent.assess_risk(ticker, market_data, news_sentiment)

            synthesis = await decision_agent.synthesize_insights(
                ticker,
                market_analysis,
                news_sentiment,
                risk_assessment
            )

            all_insights.append(AgentInsight(
                agent_name=synthesis["agent_name"],
                confidence=synthesis["overall_confidence"],
                summary=synthesis["synthesis"],
                details={
                    "ticker": ticker,
                    "overall_risk": synthesis["overall_risk"],
                    "disclaimer": synthesis["disclaimer"]
                },
                reasoning=synthesis["reasoning"]
            ))

        return all_insights

    def _determine_overall_risk(self, insights: List[AgentInsight]) -> str:
        """Determine overall risk level from insights."""
        risk_counts = {"low": 0, "medium": 0, "high": 0}

        for insight in insights:
            risk_level = insight.details.get("risk_level")
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
