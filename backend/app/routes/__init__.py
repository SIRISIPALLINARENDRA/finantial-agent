from .auth import router as auth_router
from .market import router as market_router
from .insights import router as insights_router
from .news import router as news_router

__all__ = ["auth_router", "market_router", "insights_router", "news_router"]
