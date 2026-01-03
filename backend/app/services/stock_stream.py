from abc import ABC, abstractmethod
from typing import Dict, Set, Callable, Optional, List
import asyncio
import json
from datetime import datetime
import logging

from ..core.config import settings
from ..schemas.market import StockPrice

logger = logging.getLogger(__name__)


class MarketDataProvider(ABC):
    """Abstract base class for market data providers."""

    @abstractmethod
    async def connect(self):
        """Establish connection to data provider."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Close connection to data provider."""
        pass

    @abstractmethod
    async def subscribe(self, tickers: List[str]):
        """Subscribe to ticker updates."""
        pass

    @abstractmethod
    async def unsubscribe(self, tickers: List[str]):
        """Unsubscribe from ticker updates."""
        pass

    @abstractmethod
    async def get_latest_quote(self, ticker: str) -> Optional[StockPrice]:
        """Get the latest quote for a ticker."""
        pass


class AlpacaProvider(MarketDataProvider):
    """Alpaca Markets WebSocket provider implementation."""

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.ws = None
        self.connected = False
        self._subscribed_tickers: Set[str] = set()

    async def connect(self):
        """Connect to Alpaca WebSocket."""
        try:
            import websockets

            # Alpaca WebSocket URL (for real-time data use IEX feed)
            url = "wss://stream.data.alpaca.markets/v2/iex"
            self.ws = await websockets.connect(url)

            # Authenticate
            auth_message = {
                "action": "auth",
                "key": self.api_key,
                "secret": self.secret_key
            }
            await self.ws.send(json.dumps(auth_message))

            response = await self.ws.recv()
            response_data = json.loads(response)

            if response_data[0].get("T") == "success":
                self.connected = True
                logger.info("Connected to Alpaca WebSocket")
            else:
                raise Exception(f"Authentication failed: {response_data}")

        except Exception as e:
            logger.error(f"Failed to connect to Alpaca: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Alpaca WebSocket."""
        if self.ws:
            await self.ws.close()
            self.connected = False
            logger.info("Disconnected from Alpaca WebSocket")

    async def subscribe(self, tickers: List[str]):
        """Subscribe to ticker updates."""
        if not self.connected:
            await self.connect()

        subscribe_message = {
            "action": "subscribe",
            "trades": tickers,
            "quotes": tickers,
            "bars": tickers
        }
        await self.ws.send(json.dumps(subscribe_message))
        self._subscribed_tickers.update(tickers)
        logger.info(f"Subscribed to tickers: {tickers}")

    async def unsubscribe(self, tickers: List[str]):
        """Unsubscribe from ticker updates."""
        unsubscribe_message = {
            "action": "unsubscribe",
            "trades": tickers,
            "quotes": tickers,
            "bars": tickers
        }
        await self.ws.send(json.dumps(unsubscribe_message))
        self._subscribed_tickers.difference_update(tickers)
        logger.info(f"Unsubscribed from tickers: {tickers}")

    async def get_latest_quote(self, ticker: str) -> Optional[StockPrice]:
        """Get the latest quote for a ticker."""
        # This would typically call Alpaca's REST API for historical/snapshot data
        # For real-time, you'd listen to the WebSocket stream
        return None

    async def listen(self, callback: Callable[[StockPrice], None]):
        """Listen to WebSocket messages and invoke callback."""
        while self.connected:
            try:
                message = await self.ws.recv()
                data = json.loads(message)

                for item in data:
                    msg_type = item.get("T")

                    # Handle trades
                    if msg_type == "t":
                        stock_price = StockPrice(
                            ticker=item.get("S"),
                            price=float(item.get("p")),
                            volume=int(item.get("s", 0)),
                            timestamp=datetime.fromisoformat(item.get("t").replace("Z", "+00:00"))
                        )
                        await callback(stock_price)

                    # Handle quotes
                    elif msg_type == "q":
                        stock_price = StockPrice(
                            ticker=item.get("S"),
                            price=float(item.get("ap")),  # Ask price
                            volume=0,
                            timestamp=datetime.fromisoformat(item.get("t").replace("Z", "+00:00"))
                        )
                        await callback(stock_price)

            except Exception as e:
                logger.error(f"Error in WebSocket listener: {e}")
                break


class FinnhubProvider(MarketDataProvider):
    """Finnhub WebSocket and REST API provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws = None
        self.connected = False
        self._subscribed_tickers: Set[str] = set()
        self.base_url = "https://finnhub.io/api/v1"

    async def connect(self):
        """Connect to Finnhub WebSocket."""
        try:
            import websockets

            url = f"wss://ws.finnhub.io?token={self.api_key}"
            self.ws = await websockets.connect(url)
            self.connected = True
            logger.info("Connected to Finnhub WebSocket")

        except Exception as e:
            logger.error(f"Failed to connect to Finnhub: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Finnhub WebSocket."""
        if self.ws:
            await self.ws.close()
            self.connected = False
            logger.info("Disconnected from Finnhub WebSocket")

    async def subscribe(self, tickers: List[str]):
        """Subscribe to ticker updates."""
        if not self.connected:
            await self.connect()

        for ticker in tickers:
            subscribe_message = json.dumps({"type": "subscribe", "symbol": ticker})
            await self.ws.send(subscribe_message)
            self._subscribed_tickers.add(ticker)

        logger.info(f"Subscribed to tickers: {tickers}")

    async def unsubscribe(self, tickers: List[str]):
        """Unsubscribe from ticker updates."""
        for ticker in tickers:
            unsubscribe_message = json.dumps({"type": "unsubscribe", "symbol": ticker})
            await self.ws.send(unsubscribe_message)
            self._subscribed_tickers.discard(ticker)

        logger.info(f"Unsubscribed from tickers: {tickers}")

    async def get_latest_quote(self, ticker: str) -> Optional[StockPrice]:
        """Get the latest quote for a ticker using REST API."""
        try:
            import aiohttp
            import ssl

            url = f"{self.base_url}/quote"
            params = {"symbol": ticker, "token": self.api_key}

            # Create SSL context that doesn't verify certificates (for development)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Check if data is valid (not empty response)
                        if not data.get("c"):
                            logger.error(f"No data returned for ticker: {ticker}")
                            return None

                        return StockPrice(
                            ticker=ticker,
                            price=float(data.get("c") or 0),  # Current price
                            volume=int(data.get("v") or 0),  # Volume
                            timestamp=datetime.utcnow(),
                            change=float(data.get("d") or 0),  # Change
                            change_percent=float(data.get("dp") or 0),  # Change percent
                            open=float(data.get("o") or 0),  # Open
                            high=float(data.get("h") or 0),  # High
                            low=float(data.get("l") or 0),  # Low
                            close=float(data.get("pc") or 0)  # Previous close
                        )
                    else:
                        logger.error(f"Finnhub API error: {response.status}")
                        return None

        except Exception as e:
            logger.error(f"Error fetching quote from Finnhub: {e}")
            return None

    async def listen(self, callback: Callable[[StockPrice], None]):
        """Listen to WebSocket messages and invoke callback."""
        while self.connected:
            try:
                message = await self.ws.recv()
                data = json.loads(message)

                if data.get("type") == "trade":
                    for trade in data.get("data", []):
                        stock_price = StockPrice(
                            ticker=trade.get("s"),
                            price=float(trade.get("p")),
                            volume=int(trade.get("v", 0)),
                            timestamp=datetime.fromtimestamp(trade.get("t", 0) / 1000)
                        )
                        await callback(stock_price)

            except Exception as e:
                logger.error(f"Error in Finnhub WebSocket listener: {e}")
                break


class MockProvider(MarketDataProvider):
    """Mock provider for testing and development."""

    def __init__(self):
        self.connected = False
        self._subscribed_tickers: Set[str] = set()

    async def connect(self):
        self.connected = True
        logger.info("Connected to Mock Provider")

    async def disconnect(self):
        self.connected = False
        logger.info("Disconnected from Mock Provider")

    async def subscribe(self, tickers: List[str]):
        self._subscribed_tickers.update(tickers)
        logger.info(f"Mock: Subscribed to {tickers}")

    async def unsubscribe(self, tickers: List[str]):
        self._subscribed_tickers.difference_update(tickers)
        logger.info(f"Mock: Unsubscribed from {tickers}")

    async def get_latest_quote(self, ticker: str) -> Optional[StockPrice]:
        import random
        return StockPrice(
            ticker=ticker,
            price=round(random.uniform(100, 500), 2),
            volume=random.randint(1000, 100000),
            timestamp=datetime.utcnow(),
            change=round(random.uniform(-5, 5), 2),
            change_percent=round(random.uniform(-2, 2), 2)
        )


class StockStreamManager:
    """Manager for handling real-time stock data streams."""

    def __init__(self):
        self.provider: Optional[MarketDataProvider] = None
        self.active_subscriptions: Dict[str, Set[str]] = {}  # user_id -> set of tickers
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the configured market data provider."""
        provider_name = settings.MARKET_DATA_PROVIDER.lower()

        if provider_name == "alpaca":
            self.provider = AlpacaProvider(
                api_key=settings.MARKET_DATA_API_KEY,
                secret_key=settings.MARKET_DATA_SECRET_KEY
            )
        elif provider_name == "finnhub":
            self.provider = FinnhubProvider(
                api_key=settings.MARKET_DATA_API_KEY
            )
        elif provider_name == "mock":
            self.provider = MockProvider()
        else:
            logger.warning(f"Unknown provider {provider_name}, using Mock")
            self.provider = MockProvider()

    async def subscribe_user(self, user_id: str, tickers: List[str]):
        """Subscribe a user to ticker updates."""
        if user_id not in self.active_subscriptions:
            self.active_subscriptions[user_id] = set()

        new_tickers = set(tickers) - self.active_subscriptions[user_id]

        if new_tickers:
            await self.provider.subscribe(list(new_tickers))
            self.active_subscriptions[user_id].update(new_tickers)

    async def unsubscribe_user(self, user_id: str, tickers: Optional[List[str]] = None):
        """Unsubscribe a user from ticker updates."""
        if user_id not in self.active_subscriptions:
            return

        if tickers is None:
            tickers = list(self.active_subscriptions[user_id])

        await self.provider.unsubscribe(tickers)
        self.active_subscriptions[user_id].difference_update(tickers)

        if not self.active_subscriptions[user_id]:
            del self.active_subscriptions[user_id]

    async def get_quote(self, ticker: str) -> Optional[StockPrice]:
        """Get the latest quote for a ticker."""
        return await self.provider.get_latest_quote(ticker)


# Global instance
stock_stream_manager = StockStreamManager()
