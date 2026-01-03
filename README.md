# 📈 Financial AI Agent Platform

A production-grade, real-time financial intelligence system powered by multi-agent AI orchestration. This platform integrates live market data, financial news analysis, and agentic reasoning to provide comprehensive investment decision support.

## 🎯 Core Features

- **Real-time Market Data**: WebSocket-based live stock price streaming with pluggable data providers
- **Multi-Agent AI System**: Specialized agents for market analysis, sentiment evaluation, risk assessment, and decision synthesis
- **Secure Authentication**: JWT-based user authentication with password hashing
- **User Management**: Personal watchlists, query history, and profile management
- **Interactive Dashboard**: Streamlit-based frontend with real-time updates
- **Production-Ready**: Async architecture, Docker support, comprehensive error handling

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│              (Streamlit Interactive UI)                     │
│  - Login/Signup    - Live Dashboard    - AI Insights       │
│  - Watchlist       - Query History                          │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                   Backend API Layer                         │
│                   (FastAPI Service)                         │
│  - Auth Routes     - Market Routes     - Insights Routes   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  Service Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Stock Stream │  │ News Service │  │ Agent Service   │  │
│  │   Manager    │  │              │  │  (Orchestrator) │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│               AI Agent Layer (Phidata + Gemini)             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Market Data  │  │ News &       │  │ Risk & ESG      │  │
│  │   Agent      │  │ Sentiment    │  │   Agent         │  │
│  │              │  │   Agent      │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                             │
│                  ┌─────────────────┐                       │
│                  │ Decision        │                       │
│                  │ Synthesis Agent │                       │
│                  └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Data Layer                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ MySQL        │  │ Market Data  │  │ News API        │  │
│  │ Database     │  │ Provider     │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Agent System

The platform employs four specialized AI agents powered by Google Gemini:

1. **Market Data Agent**
   - Technical analysis of price movements
   - Volume pattern analysis
   - Support/resistance identification
   - Trend determination

2. **News & Sentiment Agent**
   - Financial news aggregation
   - Sentiment analysis (bullish/bearish/neutral)
   - Key theme identification
   - Source credibility assessment

3. **Risk & ESG Agent**
   - Investment risk assessment
   - Volatility evaluation
   - ESG factor consideration
   - Regulatory risk analysis

4. **Decision Synthesis Agent**
   - Orchestrates insights from all agents
   - Identifies consensus and conflicts
   - Provides holistic recommendations
   - Emphasizes explainability

## 📁 Project Structure

```
financial_ai_agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entry
│   │   │
│   │   ├── core/                    # Core utilities
│   │   │   ├── config.py            # Configuration management
│   │   │   ├── security.py          # JWT & password hashing
│   │   │   └── database.py          # MySQL connection & session
│   │   │
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── user.py              # User model
│   │   │   └── watchlist.py         # Watchlist & QueryHistory
│   │   │
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── auth.py              # Authentication schemas
│   │   │   └── market.py            # Market data schemas
│   │   │
│   │   ├── routes/                  # API endpoints
│   │   │   ├── auth.py              # Authentication routes
│   │   │   ├── market.py            # Market data routes
│   │   │   └── insights.py          # AI insights routes
│   │   │
│   │   ├── services/                # Business logic
│   │   │   ├── stock_stream.py      # Real-time data streaming
│   │   │   ├── news_service.py      # News aggregation
│   │   │   └── agent_service.py     # Agent orchestration
│   │   │
│   │   └── agents/                  # AI agents
│   │       ├── market_agent.py      # Market data analysis
│   │       ├── news_agent.py        # News sentiment analysis
│   │       ├── risk_agent.py        # Risk assessment
│   │       └── decision_agent.py    # Decision synthesis
│   │
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Backend container
│
├── frontend/
│   ├── app.py                       # Streamlit main app
│   ├── pages/
│   │   ├── dashboard.py             # Live market dashboard
│   │   ├── insights.py              # AI insights interface
│   │   ├── watchlist.py             # Watchlist management
│   │   └── history.py               # Query history
│   │
│   └── requirements.txt             # Frontend dependencies
│
├── docker-compose.yml               # Docker orchestration
├── DATABASE_SCHEMA.sql              # MySQL schema
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Docker & Docker Compose (optional)
- API Keys:
  - Google Gemini API
  - Market data provider (Alpaca/Polygon/Finnhub)
  - News API

### Method 1: Docker (Recommended)

1. **Clone and Configure**
   ```bash
   git clone <repository-url>
   cd financial_ai_agent
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Access**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Method 2: Manual Setup

1. **Database Setup**
   ```bash
   mysql -u root -p < DATABASE_SCHEMA.sql
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Configure .env file
   cp ../.env.example .env
   # Edit .env with your configuration

   # Run backend
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 🔐 Security Features

- **Password Hashing**: Bcrypt with automatic salting
- **JWT Authentication**: Secure token-based auth with expiration
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Protection**: Configurable allowed origins
- **Input Validation**: Pydantic models with comprehensive validation
- **Environment Variables**: Sensitive data stored securely

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login (returns JWT)
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

### Market Data
- `GET /api/market/quote/{ticker}` - Get stock quote
- `POST /api/market/watchlist` - Add to watchlist
- `GET /api/market/watchlist` - Get user watchlist
- `DELETE /api/market/watchlist/{id}` - Remove from watchlist
- `WS /api/market/ws/stream/{user_id}` - Real-time price stream

### AI Insights
- `POST /api/insights/analyze` - Request AI analysis
- `GET /api/insights/history` - Get query history
- `GET /api/insights/history/{id}` - Get query details

### Health & Status
- `GET /` - Service status
- `GET /health` - Health check

Full API documentation available at `/docs` when running.

## 🤖 AI Agent Usage

### Query Types

1. **Market Analysis**
   ```json
   {
     "tickers": ["AAPL", "GOOGL"],
     "query_type": "market_analysis"
   }
   ```

2. **News Sentiment**
   ```json
   {
     "tickers": ["TSLA"],
     "query_type": "news_sentiment",
     "additional_context": "Focus on recent earnings"
   }
   ```

3. **Risk Assessment**
   ```json
   {
     "tickers": ["MSFT"],
     "query_type": "risk_assessment"
   }
   ```

4. **Decision Synthesis** (Full Analysis)
   ```json
   {
     "tickers": ["AAPL", "MSFT"],
     "query_type": "decision_synthesis"
   }
   ```

## 🗄️ Database Schema

### Tables

**users**
- User authentication and profile information
- Relationships: watchlists, query_history

**watchlists**
- User-specific stock tracking
- Custom notes and alert thresholds

**query_history**
- Historical AI query tracking
- Performance metrics and results

See `DATABASE_SCHEMA.sql` for complete schema.

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=mysql+aiomysql://user:pass@localhost:3306/financial_agent_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
GEMINI_API_KEY=your-gemini-key

# Market Data
MARKET_DATA_PROVIDER=alpaca  # or polygon, finnhub
MARKET_DATA_API_KEY=your-key
MARKET_DATA_SECRET_KEY=your-secret

# News
NEWS_API_KEY=your-news-api-key
```

### Market Data Providers

The system supports pluggable market data providers:

- **Alpaca** (default): Free tier available, real-time for US markets
- **Polygon**: Comprehensive data, requires subscription
- **Finnhub**: Good for international markets
- **Mock Provider**: For development/testing

Configure in `.env` via `MARKET_DATA_PROVIDER`.

## 📊 Frontend Pages

### 1. Dashboard
- Real-time stock price monitoring
- Multi-ticker tracking
- Auto-refresh capability
- Quick stats and metrics

### 2. AI Insights
- Multi-agent analysis interface
- Query type selection
- Detailed agent insights
- Confidence scoring
- Risk level assessment

### 3. Watchlist
- Personal stock tracking
- Custom notes
- Alert thresholds
- Easy add/remove

### 4. Query History
- Historical analysis tracking
- Performance metrics
- Result review
- Pattern analysis

## 🚦 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8 .
pylint app/

# Type checking
mypy app/
```

## 📈 Performance Considerations

- **Async Architecture**: Non-blocking I/O for high concurrency
- **Database Connection Pooling**: Efficient connection management
- **Caching**: Strategic caching for API responses
- **WebSocket Streaming**: Real-time data with minimal latency
- **Agent Orchestration**: Parallel agent execution where possible

## ⚠️ Responsible AI & Disclaimers

**This platform is designed for decision-support only, not trading execution.**

Key principles:
- ✅ Explainable AI: Clear reasoning for all insights
- ✅ Transparency: Confidence scores and limitations disclosed
- ✅ No trading execution: Analysis only, no automated trades
- ✅ Risk awareness: Comprehensive risk assessment included
- ✅ User control: All decisions remain with the user

**Disclaimer**: This system does not constitute financial advice. Users should consult qualified financial advisors before making investment decisions.

## 🔮 Future Enhancements

- [ ] Advanced technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Portfolio optimization algorithms
- [ ] Backtesting capabilities
- [ ] Enhanced ESG scoring integration
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Advanced visualization dashboards
- [ ] Social sentiment analysis (Twitter/Reddit)
- [ ] Earnings calendar integration
- [ ] Webhook notifications

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **Phidata**: Agent orchestration framework
- **Google Gemini**: AI reasoning and analysis
- **FastAPI**: High-performance backend framework
- **Streamlit**: Interactive frontend framework
- **SQLAlchemy**: Database ORM

## 📧 Support

For issues, questions, or contributions:
- GitHub Issues: [Repository Issues]
- Documentation: [Wiki/Docs]
- Email: support@example.com

---

**Built with ❤️ for responsible AI-powered financial intelligence**

**Version**: 1.0.0
**Last Updated**: 2024
