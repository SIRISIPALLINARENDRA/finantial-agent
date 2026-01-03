# System Architecture Documentation

## 🏛️ Architecture Overview

The Financial AI Agent Platform implements a modern, production-grade architecture based on microservices principles with clear separation of concerns.

## 📐 Design Principles

### 1. Separation of Concerns
- **Frontend**: User interface and interaction
- **Backend API**: Business logic and orchestration
- **Service Layer**: Specialized services for specific domains
- **Agent Layer**: AI-powered analysis and reasoning
- **Data Layer**: Persistence and external data sources

### 2. Async-First Architecture
- Non-blocking I/O throughout the stack
- AsyncIO for Python backend
- WebSocket for real-time streaming
- Concurrent agent execution

### 3. Security by Design
- JWT-based authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection prevention via ORM
- CORS protection

### 4. Modularity & Extensibility
- Pluggable market data providers
- Configurable AI agents
- Environment-based configuration
- Docker containerization

## 🔄 Data Flow

### User Authentication Flow
```
User Input → Frontend (Streamlit)
    ↓
POST /api/auth/login
    ↓
Backend validates credentials
    ↓
Generate JWT token
    ↓
Return token to frontend
    ↓
Frontend stores token in session
    ↓
All subsequent requests include token in Authorization header
```

### AI Analysis Flow
```
User selects tickers → Frontend
    ↓
POST /api/insights/analyze
    ↓
AgentOrchestrationService receives request
    ↓
Parallel agent execution:
    - Market Data Agent → analyze_price_action()
    - News Agent → analyze_news_sentiment()
    - Risk Agent → assess_risk()
    ↓
Decision Synthesis Agent → synthesize_insights()
    ↓
Save to QueryHistory
    ↓
Return AIQueryResponse
    ↓
Frontend displays results
```

### Real-Time Market Data Flow
```
User subscribes to tickers → Frontend
    ↓
WebSocket connection established
    ↓
Backend StockStreamManager
    ↓
Connect to Market Data Provider (Alpaca/Polygon/etc)
    ↓
Provider streams price updates
    ↓
StockStreamManager processes and broadcasts
    ↓
Frontend receives updates via WebSocket
    ↓
Live dashboard updates
```

## 🧱 Component Architecture

### Backend Components

#### 1. Core Layer (`app/core/`)
**Purpose**: Foundational infrastructure and utilities

- **config.py**: Environment-based configuration management
  - Loads from `.env` file
  - Type-safe settings with Pydantic
  - Validation of required variables

- **security.py**: Authentication and authorization
  - Password hashing (bcrypt)
  - JWT token generation and validation
  - User dependency injection
  - Access control

- **database.py**: Database connectivity
  - Async SQLAlchemy engine
  - Connection pooling
  - Session management
  - Transaction handling

#### 2. Models Layer (`app/models/`)
**Purpose**: Data models and ORM mappings

- **user.py**: User entity
  - Authentication data
  - Profile information
  - Relationships to watchlists and history

- **watchlist.py**: User stock tracking
  - Ticker symbols
  - Custom notes
  - Alert thresholds (JSON)
  - QueryHistory for analysis tracking

#### 3. Schemas Layer (`app/schemas/`)
**Purpose**: Request/response validation and serialization

- **auth.py**: Authentication schemas
  - UserCreate (registration)
  - UserLogin (authentication)
  - Token (JWT response)
  - UserResponse (profile data)

- **market.py**: Market data schemas
  - StockPrice (real-time quotes)
  - WatchlistCreate/Response
  - AIQueryRequest/Response
  - AgentInsight

#### 4. Routes Layer (`app/routes/`)
**Purpose**: API endpoint definitions

- **auth.py**: Authentication endpoints
  - POST /api/auth/signup
  - POST /api/auth/login
  - GET /api/auth/me
  - POST /api/auth/logout

- **market.py**: Market data endpoints
  - GET /api/market/quote/{ticker}
  - POST /api/market/watchlist
  - GET /api/market/watchlist
  - DELETE /api/market/watchlist/{id}
  - WS /api/market/ws/stream/{user_id}

- **insights.py**: AI analysis endpoints
  - POST /api/insights/analyze
  - GET /api/insights/history
  - GET /api/insights/history/{id}

#### 5. Services Layer (`app/services/`)
**Purpose**: Business logic and external integrations

- **stock_stream.py**: Real-time market data
  - Abstract MarketDataProvider interface
  - Provider implementations (Alpaca, Mock)
  - StockStreamManager for subscription management
  - WebSocket connection handling

- **news_service.py**: Financial news aggregation
  - News API integration
  - Article fetching and filtering
  - Simple sentiment analysis
  - Market news vs. ticker-specific news

- **agent_service.py**: AI agent orchestration
  - Query type routing
  - Parallel agent execution
  - Result aggregation
  - Performance tracking

#### 6. Agents Layer (`app/agents/`)
**Purpose**: AI-powered analysis

- **market_agent.py**: Technical analysis
  - Price trend identification
  - Volume analysis
  - Support/resistance detection
  - Confidence scoring

- **news_agent.py**: Sentiment analysis
  - News aggregation
  - Sentiment classification
  - Theme extraction
  - Source evaluation

- **risk_agent.py**: Risk assessment
  - Volatility evaluation
  - Risk level classification
  - ESG perspective
  - Downside analysis

- **decision_agent.py**: Synthesis
  - Multi-agent coordination
  - Consensus identification
  - Holistic recommendations
  - Explainability

### Frontend Components

#### 1. Main Application (`app.py`)
**Purpose**: Entry point and navigation

- Session state management
- Authentication flow
- Page routing
- Global configuration

#### 2. Pages (`pages/`)

- **dashboard.py**: Live market monitoring
  - Real-time quote display
  - Multi-ticker tracking
  - Auto-refresh
  - Quick stats

- **insights.py**: AI analysis interface
  - Query type selection
  - Ticker input
  - Result display
  - Agent insights breakdown

- **watchlist.py**: Personal tracking
  - Add/remove tickers
  - Custom notes
  - Alert configuration
  - List management

- **history.py**: Query tracking
  - Historical queries
  - Performance metrics
  - Result review
  - Pattern analysis

## 🔌 Integration Points

### External Services

1. **Google Gemini API**
   - Model: `gemini-2.0-flash-exp`
   - Purpose: AI reasoning and analysis
   - Integration: Phidata Agent framework
   - Rate limits: Managed by Google

2. **Market Data Providers**
   - Alpaca Markets: Real-time US equities
   - Polygon.io: Comprehensive market data
   - Finnhub: International markets
   - Integration: Pluggable provider pattern

3. **News API**
   - NewsAPI.org: Financial news aggregation
   - Rate limits: 100 requests/day (free tier)
   - Integration: aiohttp async client

### Internal Integrations

1. **Database**
   - MySQL 8.0+ with InnoDB engine
   - Connection: aiomysql async driver
   - ORM: SQLAlchemy 2.0+
   - Pooling: Pre-configured pool size

2. **WebSocket**
   - Protocol: WebSocket (RFC 6455)
   - Library: FastAPI WebSocket support
   - Use: Real-time price streaming

## 🔒 Security Architecture

### Authentication Flow
1. User submits credentials
2. Backend validates against hashed password
3. Generate JWT with user ID in payload
4. Set expiration (default: 30 minutes)
5. Return token to client
6. Client includes token in Authorization header
7. Backend validates token on each request
8. Extract user from token payload

### Authorization
- User-specific resources (watchlist, history)
- Ownership validation before operations
- Active user check
- Superuser flag for admin operations

### Data Protection
- Passwords: Bcrypt hashing with auto-salt
- Tokens: JWT with HMAC-SHA256
- Database: Parameterized queries via ORM
- API: Input validation with Pydantic
- Network: HTTPS in production (recommended)

## 📊 Database Design

### Relationships
```
users (1) ←→ (*) watchlists
users (1) ←→ (*) query_history
```

### Indexes
- users: email, username, (is_active, created_at)
- watchlists: user_id, ticker, (user_id, ticker) UNIQUE
- query_history: user_id, query_type, created_at

### Views
- user_activity_summary: Aggregated user statistics
- query_performance_stats: Query performance metrics

## 🚀 Deployment Architecture

### Development
```
[Local Machine]
├── Backend (localhost:8000)
├── Frontend (localhost:8501)
└── MySQL (localhost:3306)
```

### Production (Docker)
```
[Docker Host]
├── Container: MySQL (mysql:8.0)
│   └── Volume: mysql_data
├── Container: Backend (Python:3.11)
│   └── Depends: MySQL
└── Container: Frontend (Python:3.11)
    └── Depends: Backend
```

### Scalability Considerations

1. **Horizontal Scaling**
   - Multiple backend instances behind load balancer
   - Shared MySQL database
   - Session-less JWT authentication

2. **Vertical Scaling**
   - Increase container resources
   - Adjust connection pool sizes
   - Optimize query performance

3. **Caching**
   - Redis for session storage (future)
   - API response caching
   - Market data caching with TTL

4. **Async Benefits**
   - Non-blocking I/O
   - High concurrency
   - Efficient resource utilization

## 🔧 Configuration Management

### Environment-Based Config
- Development: .env file
- Production: Environment variables
- Docker: docker-compose.yml

### Secrets Management
- Never commit .env to version control
- Use secret management services in production
- Rotate keys regularly
- Minimum privilege principle

## 📈 Performance Optimization

### Backend
- Async/await throughout
- Connection pooling (size: 10, overflow: 20)
- Lazy loading for relationships
- Index optimization
- Query result limiting

### Frontend
- Session state caching
- Pagination for large lists
- Auto-refresh with configurable intervals
- Lazy component loading

### AI Agents
- Parallel agent execution
- Response caching (future)
- Configurable timeouts
- Error recovery

## 🧪 Testing Strategy

### Unit Tests
- Services: Mock external dependencies
- Agents: Test with mock Gemini responses
- Routes: Test with TestClient

### Integration Tests
- Database: Test with in-memory SQLite
- API: End-to-end flow testing
- Authentication: Token generation and validation

### Load Tests
- WebSocket connections
- Concurrent API requests
- Database query performance

## 📚 Design Patterns Used

1. **Dependency Injection**: FastAPI dependencies
2. **Repository Pattern**: Database access abstraction
3. **Factory Pattern**: Market data provider creation
4. **Strategy Pattern**: Pluggable providers
5. **Observer Pattern**: WebSocket subscriptions
6. **Singleton Pattern**: Service instances
7. **MVC Pattern**: Routes → Services → Models

## 🔮 Future Architecture Enhancements

1. **Microservices Split**
   - Auth service
   - Market data service
   - AI agent service
   - API gateway

2. **Event-Driven Architecture**
   - Message queue (RabbitMQ/Kafka)
   - Event sourcing
   - CQRS pattern

3. **Caching Layer**
   - Redis for sessions
   - API response caching
   - Market data caching

4. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Distributed tracing
   - Centralized logging

---

**This architecture is designed for production-grade performance, security, and scalability.**
