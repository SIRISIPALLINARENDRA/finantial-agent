from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import logging

from ..core.database import get_db
from ..core.security import get_current_active_user
from ..models.user import User
from ..models.watchlist import QueryHistory
from ..schemas.market import AIQueryRequest, AIQueryResponse
from ..services.agent_service import agent_orchestration_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/insights", tags=["AI Insights"])


@router.post("/analyze", response_model=AIQueryResponse)
async def analyze_stocks(
    query_request: AIQueryRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Perform AI-powered analysis on selected stocks.

    Args:
        query_request: Query parameters including tickers and query type
        current_user: Authenticated user
        db: Database session

    Returns:
        Comprehensive AI analysis results
    """
    try:
        logger.info(
            f"User {current_user.username} requested {query_request.query_type} "
            f"analysis for {query_request.tickers}"
        )

        response = await agent_orchestration_service.execute_query(query_request)

        query_history = QueryHistory(
            user_id=current_user.id,
            query_type=query_request.query_type.value,
            query_params={
                "tickers": query_request.tickers,
                "additional_context": query_request.additional_context
            },
            agent_response={
                "query_id": response.query_id,
                "risk_level": response.risk_level,
                "insights_count": len(response.insights)
            },
            response_summary=response.synthesis[:1000],
            execution_time_ms=response.execution_time_ms
        )

        db.add(query_history)
        await db.commit()

        logger.info(
            f"Analysis completed for user {current_user.username} "
            f"in {response.execution_time_ms}ms"
        )

        return response

    except Exception as e:
        logger.error(f"Analysis error for user {current_user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/history", response_model=List[dict])
async def get_query_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's query history.

    Args:
        limit: Maximum number of history items to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of previous queries and results
    """
    result = await db.execute(
        select(QueryHistory)
        .where(QueryHistory.user_id == current_user.id)
        .order_by(desc(QueryHistory.created_at))
        .limit(limit)
    )
    history_items = result.scalars().all()

    return [
        {
            "id": item.id,
            "query_type": item.query_type,
            "query_params": item.query_params,
            "response_summary": item.response_summary,
            "execution_time_ms": item.execution_time_ms,
            "created_at": item.created_at.isoformat()
        }
        for item in history_items
    ]


@router.get("/history/{query_id}", response_model=dict)
async def get_query_detail(
    query_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed results of a specific query.

    Args:
        query_id: Query history ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Detailed query results
    """
    result = await db.execute(
        select(QueryHistory).where(
            (QueryHistory.id == query_id) &
            (QueryHistory.user_id == current_user.id)
        )
    )
    query_item = result.scalar_one_or_none()

    if not query_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query not found"
        )

    return {
        "id": query_item.id,
        "query_type": query_item.query_type,
        "query_params": query_item.query_params,
        "agent_response": query_item.agent_response,
        "response_summary": query_item.response_summary,
        "execution_time_ms": query_item.execution_time_ms,
        "created_at": query_item.created_at.isoformat()
    }
