# 🤖 Crypto Trading Agent

An automated cryptocurrency trading system built with Python, FastAPI, and OpenAI. Features a multi-agent architecture with strict risk controls, paper trading mode, and production-ready containerization.

---

## Table of Contents

1. [What This System Does](#what-this-system-does)
2. [Key Terms Glossary](#key-terms-glossary)
3. [Architecture Overview](#architecture-overview)
4. [Folder Structure](#folder-structure)
5. [Environment Setup](#environment-setup)
6. [Configuration](#configuration)
7. [Running Locally with Docker](#running-locally-with-docker)
8. [Database Setup & Migrations](#database-setup--migrations)
9. [RAG Knowledge Base](#rag-knowledge-base)
10. [Data Ingestion Plan](#data-ingestion-plan)
11. [Trading Workflow](#trading-workflow)
12. [Observability](#observability)
13. [Testing Plan](#testing-plan)
14. [Safety Checklist](#safety-checklist)
15. [Milestones](#milestones)
16. [TODO by Module](#todo-by-module)
17. [Contributing](#contributing)
18. [Disclaimer](#disclaimer)

---

## What This System Does

This project is an **automated crypto trading agent** that:

1. **Collects market data** from Binance (prices, candles, volume)
2. **Generates trading signals** using configurable strategies
3. **Evaluates risk** before any trade (position sizing, loss limits)
4. **Executes orders** through a broker interface (paper trading first, real broker later)
5. **Monitors performance** and can trigger a kill switch if things go wrong
6. **Uses AI (OpenAI)** to assist with decision-making and answer questions about strategy/docs

The system is designed to run in **paper trading mode first** (simulated trades with fake money) so you can validate your strategy before risking real capital.

---

## Key Terms Glossary

| Term | Simple Explanation |
|------|-------------------|
| **Candle/OHLCV** | A data point showing Open, High, Low, Close prices and Volume for a time period |
| **Signal** | A recommendation to BUY, SELL, or HOLD based on analysis |
| **Position** | How much of an asset you currently own |
| **Position Sizing** | Deciding how much to buy/sell based on risk rules |
| **Drawdown** | The drop from peak portfolio value to current value |
| **Paper Trading** | Simulated trading with fake money to test strategies |
| **Kill Switch** | Emergency stop that halts all trading immediately |
| **RAG** | Retrieval-Augmented Generation - AI that can search documents to answer questions |
| **Slippage** | Difference between expected price and actual execution price |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOCKER COMPOSE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   API        │    │   WORKER     │    │  RAG INGEST  │                  │
│  │  (FastAPI)   │    │  (Runner)    │    │  (Batch Job) │                  │
│  │              │    │              │    │              │                  │
│  │ • REST API   │    │ • Data fetch │    │ • Doc loader │                  │
│  │ • Dashboard  │    │ • Signal gen │    │ • Embeddings │                  │
│  │ • Kill switch│    │ • Risk check │    │ • Vector DB  │                  │
│  │ • Status     │    │ • Execution  │    │              │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘                  │
│         │                   │                                               │
│         └─────────┬─────────┘                                               │
│                   │                                                         │
│         ┌─────────▼─────────┐         ┌──────────────┐                     │
│         │    POSTGRES       │         │   REDIS      │                     │
│         │   (Database)      │         │  (Cache/Q)   │ (optional)          │
│         └───────────────────┘         └──────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              EXTERNAL SERVICES
┌─────────────────────────────────────────────────────────────────────────────┐
│  Binance API (market data)  │  OpenAI API (agent)  │  Broker (execution)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Services

| Service | Purpose | Tech |
|---------|---------|------|
| **api** | REST API for monitoring, control, manual triggers | FastAPI |
| **worker** | Main trading loop: data → signal → risk → execute | Python |
| **rag-ingest** | Batch job to ingest documents into vector store | Python |
| **postgres** | Store trades, positions, metrics, state | PostgreSQL |
| **redis** | (Optional) Caching, rate limiting, pub/sub | Redis |

### Core Modules

| Module | Responsibility |
|--------|---------------|
| `data` | Fetch market data from Binance, cache, validate |
| `features` | Calculate technical indicators (SMA, RSI, etc.) |
| `strategies` | Define trading strategies, generate signals |
| `risk` | Position sizing, loss limits, drawdown checks |
| `execution` | Broker interface, order management, paper broker |
| `agents` | OpenAI-powered agents for decisions and Q&A |
| `monitoring` | Metrics collection, alerting, health checks |
| `db` | Database models, queries, migrations |
| `config` | Settings management, environment loading |
| `utils` | Logging, helpers, exceptions |

---

## Folder Structure

```
RobinHood-Crypto/
├── docker-compose.yml          # Orchestrates all services
├── Dockerfile.api              # API service container
├── Dockerfile.worker           # Worker service container
├── Makefile                    # Dev commands (make run, make test, etc.)
├── pyproject.toml              # Python project config
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Dev/test dependencies
├── .env.example                # Template for environment variables
├── .gitignore
├── README.md                   # This file
│
├── config/                     # Configuration files
│   ├── settings.yaml           # Main app settings
│   ├── symbols.yaml            # Trading pairs config
│   ├── strategies.yaml         # Strategy parameters
│   └── risk_limits.yaml        # Risk management rules
│
├── src/                        # Main source code
│   ├── __init__.py
│   │
│   ├── api/                    # FastAPI service
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py       # Health check endpoints
│   │   │   ├── trading.py      # Trading control endpoints
│   │   │   ├── positions.py    # Position queries
│   │   │   └── admin.py        # Kill switch, config
│   │   └── dependencies.py     # FastAPI dependencies
│   │
│   ├── worker/                 # Trading worker service
│   │   ├── __init__.py
│   │   ├── main.py             # Worker entry point
│   │   ├── trading_loop.py     # Main trading loop
│   │   └── scheduler.py        # Task scheduling
│   │
│   ├── data/                   # Data ingestion module
│   │   ├── __init__.py
│   │   ├── binance_client.py   # Binance REST API client
│   │   ├── binance_ws.py       # Binance WebSocket (optional)
│   │   ├── data_validator.py   # Validate incoming data
│   │   ├── cache.py            # Data caching layer
│   │   └── models.py           # Data models (Candle, Ticker, etc.)
│   │
│   ├── features/               # Feature engineering
│   │   ├── __init__.py
│   │   ├── indicators.py       # Technical indicators (SMA, RSI, MACD)
│   │   ├── pipeline.py         # Feature computation pipeline
│   │   └── normalizers.py      # Data normalization
│   │
│   ├── strategies/             # Trading strategies
│   │   ├── __init__.py
│   │   ├── base.py             # Base strategy interface
│   │   ├── sma_crossover.py    # Simple moving average crossover
│   │   ├── rsi_reversal.py     # RSI mean reversion
│   │   └── registry.py         # Strategy registry
│   │
│   ├── risk/                   # Risk management
│   │   ├── __init__.py
│   │   ├── manager.py          # Central risk manager
│   │   ├── position_sizer.py   # Calculate position sizes
│   │   ├── limits.py           # Loss limits, drawdown checks
│   │   └── kill_switch.py      # Emergency stop logic
│   │
│   ├── execution/              # Order execution
│   │   ├── __init__.py
│   │   ├── broker_base.py      # Abstract broker interface
│   │   ├── paper_broker.py     # Simulated paper trading
│   │   ├── robinhood_broker.py # Robinhood adapter (future)
│   │   ├── order_manager.py    # Order lifecycle management
│   │   └── models.py           # Order, Fill, Position models
│   │
│   ├── agents/                 # AI agents (OpenAI)
│   │   ├── __init__.py
│   │   ├── trading_agent.py    # Main trading decision agent
│   │   ├── research_agent.py   # RAG-powered research agent
│   │   ├── prompts/            # Prompt templates
│   │   │   ├── __init__.py
│   │   │   ├── trading.py
│   │   │   └── research.py
│   │   └── tools/              # Agent tools/functions
│   │       ├── __init__.py
│   │       ├── market_tools.py
│   │       └── risk_tools.py
│   │
│   ├── rag/                    # RAG knowledge base
│   │   ├── __init__.py
│   │   ├── ingest.py           # Document ingestion
│   │   ├── embeddings.py       # Embedding generation
│   │   ├── retriever.py        # Document retrieval
│   │   └── vector_store.py     # Vector DB interface
│   │
│   ├── monitoring/             # Observability
│   │   ├── __init__.py
│   │   ├── metrics.py          # Metrics collection
│   │   ├── alerter.py          # Alert dispatching
│   │   ├── health.py           # Health checks
│   │   └── dashboard.py        # Simple status dashboard
│   │
│   ├── db/                     # Database layer
│   │   ├── __init__.py
│   │   ├── database.py         # DB connection, session
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── queries.py          # Common queries
│   │   └── migrations/         # Alembic migrations
│   │       ├── env.py
│   │       ├── alembic.ini
│   │       └── versions/
│   │           └── .gitkeep
│   │
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py         # Pydantic settings
│   │   └── loader.py           # Config file loading
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logger.py           # Structured logging setup
│       ├── exceptions.py       # Custom exceptions
│       ├── helpers.py          # Helper functions
│       └── validators.py       # Input validation
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   │
│   ├── unit/                   # Unit tests
│   │   ├── __init__.py
│   │   ├── test_indicators.py
│   │   ├── test_strategies.py
│   │   ├── test_risk_manager.py
│   │   ├── test_position_sizer.py
│   │   └── test_data_validator.py
│   │
│   ├── integration/            # Integration tests
│   │   ├── __init__.py
│   │   ├── test_trading_loop.py
│   │   ├── test_order_flow.py
│   │   ├── test_data_pipeline.py
│   │   └── test_api_endpoints.py
│   │
│   ├── backtest/               # Backtesting tests
│   │   ├── __init__.py
│   │   ├── test_backtest_engine.py
│   │   └── test_strategy_perf.py
│   │
│   └── failure_modes/          # Failure scenario tests
│       ├── __init__.py
│       ├── test_api_failures.py
│       ├── test_kill_switch.py
│       └── test_double_orders.py
│
├── scripts/                    # Dev & ops scripts
│   ├── run_dev.py              # Local dev runner
│   ├── run_backtest.py         # Run backtests
│   ├── run_paper.py            # Start paper trading
│   ├── db_init.py              # Initialize database
│   ├── db_migrate.py           # Run migrations
│   ├── data_backfill.py        # Backfill historical data
│   ├── smoke_test.py           # Quick system smoke test
│   └── ingest_docs.py          # Ingest RAG documents
│
├── docs/                       # Documentation
│   ├── architecture.md         # Detailed architecture doc
│   ├── runbook.md              # Operational runbook
│   ├── decision_log.md         # Architecture decisions
│   ├── api_reference.md        # API documentation
│   └── strategies.md           # Strategy documentation
│
└── knowledge/                  # RAG knowledge base source
    ├── strategies/             # Strategy documentation
    │   └── .gitkeep
    ├── runbooks/               # Operational runbooks
    │   └── .gitkeep
    ├── market_research/        # Market analysis docs
    │   └── .gitkeep
    └── config_docs/            # Configuration explanations
        └── .gitkeep
```

---

## Environment Setup

### Prerequisites

- **Python 3.11+**
- **Docker** and **Docker Compose**
- **OpenAI API key**
- (Optional) **PostgreSQL** client for debugging

### Step 1: Clone and Setup

```bash
git clone <repository-url>
cd RobinHood-Crypto

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 2: Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Required variables (see `.env.example` for full list):

```ini
# Mode: paper or live
TRADING_MODE=paper

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/trading

# Risk limits
MAX_POSITION_SIZE_USD=100
MAX_DAILY_LOSS_USD=50
MAX_DRAWDOWN_PERCENT=10

# Kill switch (default: enabled)
KILL_SWITCH_ENABLED=true
```

---

## Configuration

### Config File Hierarchy

1. **`.env`** - Secrets and environment-specific values
2. **`config/settings.yaml`** - Main application settings
3. **`config/symbols.yaml`** - Which crypto pairs to trade
4. **`config/strategies.yaml`** - Strategy parameters
5. **`config/risk_limits.yaml`** - Risk rules and limits

### Example: `config/symbols.yaml`

```yaml
symbols:
  - symbol: BTCUSDT
    enabled: true
    min_trade_size: 0.001
  - symbol: ETHUSDT
    enabled: true
    min_trade_size: 0.01
```

### Example: `config/risk_limits.yaml`

```yaml
risk:
  max_position_pct: 5        # Max 5% of portfolio per position
  max_daily_loss_pct: 2      # Stop trading after 2% daily loss
  max_drawdown_pct: 10       # Kill switch at 10% drawdown
  max_open_positions: 3      # Max 3 positions at once
```

---

## Running Locally with Docker

### Quick Start

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Postgres | localhost:5432 | Database |

### Useful Commands

```bash
# View logs
docker-compose logs -f worker

# Stop everything
docker-compose down

# Reset database
docker-compose down -v
docker-compose up -d

# Run only specific services
docker-compose up api postgres
```

### Running Without Docker (Dev Mode)

```bash
# Terminal 1: Start Postgres (or use Docker just for Postgres)
docker-compose up postgres

# Terminal 2: Run API
python -m src.api.main

# Terminal 3: Run Worker
python -m src.worker.main
```

---

## Database Setup & Migrations

### Database Schema Overview

| Table | Purpose |
|-------|---------|
| `trades` | Record of all executed trades |
| `positions` | Current open positions |
| `orders` | Order history and status |
| `signals` | Generated trading signals |
| `metrics` | Performance metrics snapshots |
| `state` | System state (kill switch, etc.) |
| `documents` | RAG document metadata |

### Migration Workflow

We use **Alembic** for database migrations.

```bash
# Initialize (first time only)
alembic init src/db/migrations

# Create a new migration
alembic revision --autogenerate -m "Add trades table"

# Run migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

### Initial Setup Script

```bash
# Runs migrations and seeds initial data
python scripts/db_init.py
```

---

## RAG Knowledge Base

### What is RAG?

**RAG (Retrieval-Augmented Generation)** allows the AI agent to search through your documents and use that information when making decisions or answering questions.

### What Documents to Include

Place documents in the `knowledge/` folder:

| Folder | What to Put |
|--------|-------------|
| `strategies/` | Strategy explanations, entry/exit rules, backtesting notes |
| `runbooks/` | How to handle incidents, restart procedures |
| `market_research/` | Market analysis, coin research, news summaries |
| `config_docs/` | Explanations of config options and their effects |

### Ingestion Process

```bash
# Ingest all documents into vector store
python scripts/ingest_docs.py

# Ingest specific folder
python scripts/ingest_docs.py --folder knowledge/strategies
```

### How Ingestion Works

1. **Load** - Read files from `knowledge/` folders
2. **Chunk** - Split into smaller pieces (~500 tokens each)
3. **Embed** - Generate embeddings using OpenAI
4. **Store** - Save embeddings to vector store (Postgres pgvector or ChromaDB)

### How the Agent Uses RAG

When the trading agent needs information:

1. Agent formulates a search query
2. Retriever finds most relevant document chunks
3. Relevant context is added to the agent's prompt
4. Agent makes decision with full context

---

## Data Ingestion Plan

### Binance API Endpoints Used

| Endpoint | Purpose | Rate Limit |
|----------|---------|------------|
| `GET /api/v3/klines` | Historical candles (OHLCV) | 1200/min |
| `GET /api/v3/ticker/price` | Latest price | 1200/min |
| `GET /api/v3/ticker/24hr` | 24h volume and stats | 1200/min |

### Example: Fetching Candles

```
GET https://api.binance.com/api/v3/klines
  ?symbol=BTCUSDT
  &interval=1h
  &limit=100
```

### Polling Strategy

| Data Type | Interval | Reason |
|-----------|----------|--------|
| Candles (1h) | Every 5 min | Strategy uses hourly data |
| Latest Price | Every 30 sec | For position valuation |
| 24h Volume | Every 5 min | For liquidity checks |

### Caching Strategy

- **In-memory cache** for latest prices (TTL: 30 seconds)
- **Database cache** for historical candles (refresh on new candle close)
- **Rate limit tracking** to stay under Binance limits

### Data Validation

Before using data, validate:
- [ ] Timestamp is recent (not stale)
- [ ] Prices are positive numbers
- [ ] Volume is non-negative
- [ ] No missing candles in sequence

---

## Trading Workflow

### Complete Flow: Signal → Risk → Order → Record

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRADING LOOP                              │
│                     (runs every N seconds)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. DATA COLLECTION                                               │
│    • Fetch latest candles from Binance                          │
│    • Validate data freshness and quality                        │
│    • Update feature calculations (indicators)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SIGNAL GENERATION                                             │
│    • Run active strategies on updated data                      │
│    • Each strategy outputs: BUY / SELL / HOLD                   │
│    • Include confidence score (0-100)                           │
│    • Log signal to database                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. RISK EVALUATION (Gate)                                        │
│    • Check kill switch status → BLOCK if triggered              │
│    • Check daily loss limit → BLOCK if exceeded                 │
│    • Check max drawdown → BLOCK if exceeded                     │
│    • Check position limits → BLOCK if at max                    │
│    • Calculate position size based on risk rules                │
│    • Validate minimum trade size                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. ORDER EXECUTION                                               │
│    • Create order object with all details                       │
│    • Submit to broker (paper or live)                           │
│    • Handle response (fill, partial, reject)                    │
│    • Prevent duplicate orders (idempotency key)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. POST-TRADE RECORDING                                          │
│    • Update positions table                                      │
│    • Record trade in trades table                               │
│    • Update P&L metrics                                         │
│    • Check if new state triggers risk alerts                    │
│    • Send notifications if configured                           │
└─────────────────────────────────────────────────────────────────┘
```

### Signal Object Structure

```python
Signal:
  symbol: "BTCUSDT"
  action: "BUY" | "SELL" | "HOLD"
  confidence: 75  # 0-100
  strategy: "sma_crossover"
  timestamp: "2026-02-03T10:00:00Z"
  reason: "SMA20 crossed above SMA50"
```

### Risk Check Order (All Must Pass)

1. **Kill switch** - Is system allowed to trade?
2. **Trading hours** - Are we in allowed trading window?
3. **Daily loss** - Have we hit daily loss limit?
4. **Drawdown** - Is portfolio drawdown acceptable?
5. **Position count** - Do we have room for new positions?
6. **Position size** - Is calculated size above minimum?

### Order Lifecycle

```
CREATED → SUBMITTED → PENDING → FILLED
                        ↓
                    PARTIALLY_FILLED
                        ↓
                    CANCELLED / REJECTED
```

---

## Observability

### Logging Strategy

All logs use structured JSON format:

```json
{
  "timestamp": "2026-02-03T10:00:00Z",
  "level": "INFO",
  "service": "worker",
  "module": "trading_loop",
  "message": "Signal generated",
  "context": {
    "symbol": "BTCUSDT",
    "action": "BUY",
    "confidence": 75
  }
}
```

### Key Metrics to Track

| Metric | Type | Purpose |
|--------|------|---------|
| `portfolio_value_usd` | Gauge | Current total value |
| `daily_pnl_usd` | Gauge | Today's profit/loss |
| `drawdown_pct` | Gauge | Current drawdown |
| `trades_total` | Counter | Total trades executed |
| `signals_generated` | Counter | Signals by strategy |
| `api_latency_ms` | Histogram | Binance API latency |
| `errors_total` | Counter | Errors by type |

### Alert Conditions

| Condition | Severity | Action |
|-----------|----------|--------|
| Daily loss > 2% | WARNING | Notify |
| Drawdown > 5% | WARNING | Notify |
| Drawdown > 10% | CRITICAL | Kill switch + Notify |
| API errors > 5/min | WARNING | Notify |
| Kill switch triggered | CRITICAL | Notify immediately |

### Alert Channels (Placeholders)

Configure in settings:

```yaml
alerts:
  telegram:
    enabled: false
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
  email:
    enabled: false
    smtp_host: "smtp.example.com"
  webhook:
    enabled: false
    url: "${ALERT_WEBHOOK_URL}"
```

---

## Testing Plan

### Test Pyramid

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲         ← Few, slow, high confidence
                 ╱──────╲
                ╱        ╲
               ╱Integration╲     ← Some, moderate speed
              ╱────────────╲
             ╱              ╲
            ╱   Unit Tests   ╲   ← Many, fast, focused
           ╱──────────────────╲
```

### Unit Tests (`tests/unit/`)

**What to test:**
- [ ] Indicators calculate correctly (SMA, RSI, etc.)
- [ ] Strategies generate correct signals for known inputs
- [ ] Position sizer calculates expected sizes
- [ ] Risk limits trigger at correct thresholds
- [ ] Data validators catch bad data

**Run:**
```bash
pytest tests/unit/ -v
```

### Integration Tests (`tests/integration/`)

**What to test:**
- [ ] Trading loop processes data end-to-end
- [ ] Order flow from signal to execution
- [ ] Data pipeline fetches and stores correctly
- [ ] API endpoints return expected responses
- [ ] Database operations work correctly

**Run:**
```bash
pytest tests/integration/ -v
```

### Backtest Tests (`tests/backtest/`)

**What to test:**
- [ ] Backtest engine produces reproducible results
- [ ] Strategy performance matches expected on historical data
- [ ] Risk rules are enforced during backtest

**Run:**
```bash
pytest tests/backtest/ -v
```

### Failure Mode Tests (`tests/failure_modes/`)

**What to test:**
- [ ] System handles Binance API timeout gracefully
- [ ] System handles Binance API errors (4xx, 5xx)
- [ ] Kill switch activates on drawdown threshold
- [ ] Duplicate orders are prevented
- [ ] System recovers after restart

**Run:**
```bash
pytest tests/failure_modes/ -v
```

### Paper Trading Tests

Before going live, run paper trading for minimum:
- [ ] 1 week continuous operation
- [ ] Verify all signals are logged
- [ ] Verify P&L calculations match manual calc
- [ ] Verify risk limits trigger correctly
- [ ] Test kill switch manually

---

## Safety Checklist

### Before Paper Trading

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Kill switch is enabled and tested
- [ ] Risk limits are configured conservatively
- [ ] Logging is working and logs are being stored
- [ ] Can view current state via API
- [ ] Can manually trigger kill switch via API
- [ ] Alerting is configured (at least one channel)

### Before Live Trading

- [ ] Paper traded for minimum 2 weeks
- [ ] Reviewed all paper trades for correctness
- [ ] P&L matches expectations (even if negative)
- [ ] No unexpected errors in logs
- [ ] Risk limits tested and working
- [ ] Broker credentials secured (not in code)
- [ ] Start with TINY position sizes (e.g., $10)
- [ ] Have a manual kill procedure documented
- [ ] Someone knows how to stop the system
- [ ] Backups of database configured

### Daily Checklist (Live)

- [ ] Check system is running
- [ ] Review overnight trades
- [ ] Check error rate in logs
- [ ] Verify portfolio value matches broker
- [ ] Check drawdown level
- [ ] Confirm kill switch is enabled

---

## Milestones

### Milestone 0: Foundation (Week 1)

**Goal:** Basic infrastructure that doesn't trade

- [ ] Project structure created
- [ ] Docker setup working
- [ ] Database schema and migrations
- [ ] Config loading working
- [ ] Logging infrastructure
- [ ] Basic API endpoints (health, status)
- [ ] Kill switch mechanism (defaults ON = no trading)

### Milestone 1: Data Pipeline (Week 2)

**Goal:** Can fetch and store market data

- [ ] Binance client fetching candles
- [ ] Data validation working
- [ ] Caching layer implemented
- [ ] Historical data backfill script
- [ ] Data stored in database

### Milestone 2: First Strategy (Week 3)

**Goal:** Can generate signals (not execute)

- [ ] Indicator calculations (SMA, RSI)
- [ ] One simple strategy (SMA crossover)
- [ ] Signal logging to database
- [ ] Backtest engine basic version
- [ ] Run backtest on historical data

### Milestone 3: Risk Engine (Week 4)

**Goal:** Risk management fully working

- [ ] Position sizer implemented
- [ ] Daily loss limit working
- [ ] Drawdown monitoring
- [ ] Position count limits
- [ ] All risk rules have unit tests

### Milestone 4: Paper Trading (Week 5-6)

**Goal:** Full paper trading working

- [ ] Paper broker implemented
- [ ] Order manager working
- [ ] Trading loop complete
- [ ] Post-trade recording
- [ ] Run paper trading for 1 week
- [ ] Review and fix issues

### Milestone 5: Tiny Live (Week 7+)

**Goal:** Trade with real money (tiny amounts)

- [ ] Real broker adapter (Robinhood or other)
- [ ] Additional safety checks
- [ ] Start with $10-50 positions
- [ ] Monitor closely for 1 week
- [ ] Gradually increase if stable

### Milestone 6: AI Agent (Optional)

**Goal:** Add OpenAI-powered decision support

- [ ] RAG document ingestion
- [ ] Research agent for Q&A
- [ ] Trading agent for enhanced signals
- [ ] Agent tools for market data access

---

## TODO by Module

### `data/` - Data Ingestion
- [ ] Implement `binance_client.py` - REST API calls
- [ ] Implement `data_validator.py` - Validation logic
- [ ] Implement `cache.py` - Caching with TTL
- [ ] Implement `models.py` - Candle, Ticker dataclasses
- [ ] (Optional) Implement `binance_ws.py` - WebSocket streaming

### `features/` - Feature Engineering
- [ ] Implement `indicators.py` - SMA, EMA, RSI, MACD
- [ ] Implement `pipeline.py` - Feature computation flow
- [ ] Add tests for each indicator

### `strategies/` - Trading Strategies
- [ ] Implement `base.py` - Abstract strategy class
- [ ] Implement `sma_crossover.py` - First strategy
- [ ] Implement `registry.py` - Strategy lookup
- [ ] Add backtest tests for strategies

### `risk/` - Risk Management
- [ ] Implement `manager.py` - Central risk orchestrator
- [ ] Implement `position_sizer.py` - Size calculations
- [ ] Implement `limits.py` - Loss and drawdown checks
- [ ] Implement `kill_switch.py` - Emergency stop
- [ ] Add exhaustive unit tests

### `execution/` - Order Execution
- [ ] Implement `broker_base.py` - Abstract interface
- [ ] Implement `paper_broker.py` - Simulated broker
- [ ] Implement `order_manager.py` - Order lifecycle
- [ ] Implement `models.py` - Order, Position classes
- [ ] (Later) Implement `robinhood_broker.py`

### `agents/` - AI Agents
- [ ] Implement `trading_agent.py` - Decision agent
- [ ] Implement `research_agent.py` - RAG Q&A agent
- [ ] Create prompt templates
- [ ] Implement agent tools

### `rag/` - Knowledge Base
- [ ] Implement `ingest.py` - Document loading
- [ ] Implement `embeddings.py` - OpenAI embeddings
- [ ] Implement `retriever.py` - Similarity search
- [ ] Implement `vector_store.py` - Storage layer

### `monitoring/` - Observability
- [ ] Implement `metrics.py` - Metric collection
- [ ] Implement `alerter.py` - Alert dispatch
- [ ] Implement `health.py` - Health checks
- [ ] Set up alert channels

### `api/` - REST API
- [ ] Implement all route handlers
- [ ] Add authentication (API key)
- [ ] Add rate limiting
- [ ] OpenAPI documentation

### `worker/` - Trading Worker
- [ ] Implement `trading_loop.py` - Main loop
- [ ] Implement `scheduler.py` - Task timing
- [ ] Add graceful shutdown handling

### `db/` - Database
- [ ] Create all SQLAlchemy models
- [ ] Write common queries
- [ ] Create all migrations
- [ ] Add database indexes

### Scripts
- [ ] `db_init.py` - Database setup
- [ ] `data_backfill.py` - Historical data
- [ ] `smoke_test.py` - System verification
- [ ] `ingest_docs.py` - RAG ingestion

### Infrastructure
- [ ] Complete `Dockerfile.api`
- [ ] Complete `Dockerfile.worker`
- [ ] Complete `docker-compose.yml`
- [ ] Set up CI/CD (GitHub Actions)

---

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes with tests
3. Run test suite: `pytest`
4. Run linter: `ruff check .`
5. Submit pull request

### Code Style

- Use type hints everywhere
- Write docstrings for public functions
- Keep functions small and focused
- Log important events

---

## Disclaimer

⚠️ **IMPORTANT: READ BEFORE USING**

1. **This is not financial advice.** This software is for educational and experimental purposes only.

2. **Trading cryptocurrencies involves substantial risk of loss.** You could lose some or all of your investment.

3. **Paper trade first.** Never deploy to live trading without extensive paper trading and testing.

4. **Start with tiny amounts.** If you do trade live, start with amounts you can afford to lose completely.

5. **No guarantees.** The authors make no guarantees about the performance, reliability, or correctness of this software.

6. **You are responsible.** By using this software, you accept full responsibility for any financial losses.

7. **Regulatory compliance.** Ensure you comply with all applicable laws and regulations in your jurisdiction.

**USE AT YOUR OWN RISK.**

---

## License

MIT License - See LICENSE file for details.

---

*Last updated: February 2026*
