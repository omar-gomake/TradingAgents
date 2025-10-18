# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

TradingAgents is a multi-agent LLM-powered trading framework built with LangGraph. It simulates a trading firm with specialized agents (analysts, researchers, traders, risk managers) that collaborate to make trading decisions. The framework supports both live analysis and comprehensive backtesting with agent learning capabilities.

## Development Commands

### Setup
```bash
# Create virtual environment (Python 3.10+)
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt

# Configure API keys (required)
export OPENAI_API_KEY=your_key
export ALPHA_VANTAGE_API_KEY=your_key
# Or create .env file with these variables
```

### Running the Framework
```bash
# Interactive CLI for trading analysis
python -m cli.main

# Run trading graph programmatically
python main.py

# Run backtests (interactive)
python -m cli.main backtest run

# Run backtests with parameters
python -m cli.main backtest run -t AAPL -s 2023-01-01 -e 2024-01-01 -c 100000

# Compare multiple tickers
python -m cli.main backtest compare "AAPL,GOOGL,MSFT" -s 2023-01-01 -e 2024-01-01
```

### Testing
```bash
# Run basic backtesting tests
python tests/test_backtesting.py

# Run example scripts
python examples/simple_backtest.py
python examples/portfolio_backtest.py
python examples/advanced_backtest.py
```

## Architecture

### Core Components

**TradingAgentsGraph** ([tradingagents/graph/trading_graph.py](tradingagents/graph/trading_graph.py))
- Main orchestrator that initializes LLMs, memories, and the agent workflow graph
- Manages the full decision-making pipeline via `propagate(ticker, date)`
- Handles reflection/learning through `reflect_and_remember(returns)`
- Uses LangGraph for the agent state machine

**Agent State Machine** ([tradingagents/graph/setup.py](tradingagents/graph/setup.py))
- Builds a directed graph of agent nodes with conditional routing
- Supports dynamic analyst selection (market, social, news, fundamentals)
- State flows: Analysts → Researchers → Trader → Risk Managers → Portfolio Manager

**State Definitions** ([tradingagents/agents/utils/agent_states.py](tradingagents/agents/utils/agent_states.py))
- `AgentState`: Main state containing reports from all agents and trading decisions
- `InvestDebateState`: Tracks bull/bear researcher debate history and conclusions
- `RiskDebateState`: Tracks risk management team (risky/neutral/safe) discussions

### Agent Teams

**Analyst Team** ([tradingagents/agents/analysts/](tradingagents/agents/analysts/))
- Market Analyst: Technical indicators (MACD, RSI) and price patterns
- Fundamentals Analyst: Financial statements, company metrics
- News Analyst: Global news, insider transactions, sentiment
- Social Media Analyst: Social sentiment scoring

**Researcher Team** ([tradingagents/agents/researchers/](tradingagents/agents/researchers/))
- Bull Researcher: Argues for investment opportunities
- Bear Researcher: Argues against investment, highlights risks
- Research Manager: Judges debate and synthesizes investment plan

**Trader** ([tradingagents/agents/trader/trader.py](tradingagents/agents/trader/trader.py))
- Creates detailed investment plans based on analyst and researcher inputs
- Proposes specific trade actions (BUY/SELL/HOLD) with sizing

**Risk Management Team** ([tradingagents/agents/risk_mgmt/](tradingagents/agents/risk_mgmt/))
- Aggressive/Neutral/Conservative Debators: Evaluate risk from different perspectives
- Risk Manager: Makes final trading decision after team debate

### Data Flow Architecture

**Data Vendors** ([tradingagents/dataflows/interface.py](tradingagents/dataflows/interface.py))
- Abstraction layer supporting multiple data sources: yfinance, Alpha Vantage, OpenAI, local
- Category-based configuration: `core_stock_apis`, `technical_indicators`, `fundamental_data`, `news_data`
- Tool-level overrides available in config
- Default: yfinance for price/technical data, Alpha Vantage for fundamentals/news

**Tool System** ([tradingagents/agents/utils/](tradingagents/agents/utils/))
- `core_stock_tools.py`: Stock price data (OHLCV)
- `technical_indicators_tools.py`: Technical analysis indicators
- `fundamental_data_tools.py`: Financial statements, company fundamentals
- `news_data_tools.py`: News, insider data, sentiment
- Each tool routes to appropriate vendor via `agent_utils.py`

### Memory and Learning

**FinancialSituationMemory** ([tradingagents/agents/utils/memory.py](tradingagents/agents/utils/memory.py))
- Each agent type has its own memory instance
- Stores past decisions and outcomes for reflection
- Used by reflection system to improve future decisions

**Reflection System** ([tradingagents/graph/reflection.py](tradingagents/graph/reflection.py))
- After trades close, agents reflect on actual returns vs predictions
- Updates agent memories with lessons learned
- Critical for backtesting performance improvement over time

### Backtesting Framework

**BacktestEngine** ([tradingagents/backtesting/engine.py](tradingagents/backtesting/engine.py))
- Runs TradingAgentsGraph over historical date ranges
- Manages positions, tracks equity, calculates returns
- Integrates with reflection system for agent learning
- Supports position sizing strategies: percentage, fixed, all-in
- Implements stop-loss, take-profit, and commission modeling

**BacktestConfig** ([tradingagents/backtesting/config.py](tradingagents/backtesting/config.py))
- Configures backtesting parameters: capital, costs, position sizing, risk limits
- `enable_reflection`: Controls whether agents learn during backtest
- `reflection_on_close_only`: Learn only when positions close (more realistic)

**Performance Metrics** ([tradingagents/backtesting/analytics.py](tradingagents/backtesting/analytics.py))
- Comprehensive metrics: returns, Sharpe/Sortino ratios, max drawdown, win rate
- Benchmark comparison against buy-and-hold and SPY
- Monthly/yearly return breakdowns
- Trade-level statistics (profit factor, average win/loss)

**Visualization** ([tradingagents/backtesting/visualization.py](tradingagents/backtesting/visualization.py))
- Equity curves with drawdown shading
- Trade markers on price charts
- Monthly returns heatmaps
- Performance dashboards

## Configuration

### Default Config ([tradingagents/default_config.py](tradingagents/default_config.py))

Key configuration options:
- `deep_think_llm`: Model for complex reasoning (default: "o4-mini")
- `quick_think_llm`: Model for fast analysis (default: "gpt-4o-mini")
- `llm_provider`: "openai", "anthropic", "google", or "ollama"
- `max_debate_rounds`: Number of researcher debate iterations
- `max_risk_discuss_rounds`: Number of risk management discussions
- `data_vendors`: Map categories to vendor implementations
- `tool_vendors`: Per-tool vendor overrides

### Data Vendor Configuration

The framework uses a two-tier vendor configuration system:

1. **Category-level** (applies to all tools in category):
   ```python
   "data_vendors": {
       "core_stock_apis": "yfinance",
       "technical_indicators": "yfinance",
       "fundamental_data": "alpha_vantage",
       "news_data": "alpha_vantage"
   }
   ```

2. **Tool-level** (overrides category default):
   ```python
   "tool_vendors": {
       "get_stock_data": "alpha_vantage",  # Override for specific tool
   }
   ```

## Common Development Patterns

### Adding a New Analyst

1. Create agent file in `tradingagents/agents/analysts/new_analyst.py`
2. Define agent creation function following existing patterns
3. Add report field to `AgentState` in `agent_states.py`
4. Register in `GraphSetup.setup_graph()` with analyst key
5. Create corresponding tool node in `TradingAgentsGraph._create_tool_nodes()`
6. Update CLI to support the new analyst type

### Adding a New Data Vendor

1. Create vendor module in `tradingagents/dataflows/vendor_name.py`
2. Implement required functions (see `interface.py` for available tools)
3. Add vendor to `VENDOR_METHODS` mapping in `interface.py`
4. Update `VENDOR_LIST` if adding new vendor type
5. Update config to support new vendor in `data_vendors` or `tool_vendors`

### Customizing Agent Behavior

Agents use LangGraph's function calling and state management. To modify:
1. Agent prompts are in individual agent files (e.g., `fundamentals_analyst.py`)
2. Agent state is passed through the graph and updated by each node
3. Conditional routing logic is in `conditional_logic.py`
4. Memory access for learning is via `FinancialSituationMemory` instances

### Running Custom Backtests

```python
from tradingagents.backtesting import BacktestEngine, BacktestConfig
from tradingagents.default_config import DEFAULT_CONFIG

# Customize TradingAgents config
ta_config = DEFAULT_CONFIG.copy()
ta_config["max_debate_rounds"] = 2
ta_config["quick_think_llm"] = "gpt-4o-mini"

# Customize backtest config
bt_config = BacktestConfig(
    initial_cash=100000,
    commission=0.001,
    position_sizing="percentage",
    position_size_value=0.95,
    stop_loss=0.10,
    take_profit=0.20,
    enable_reflection=True
)

# Run backtest
engine = BacktestEngine(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    config=bt_config,
    ta_config=ta_config,
    selected_analysts=["market", "news", "fundamentals"]
)

results = engine.run()
results.print_metrics()
engine.save_results("results/backtests/AAPL")
engine.plot("results/backtests/AAPL/plots")
```

## Important Constraints

### API Rate Limits
- Default uses Alpha Vantage for fundamentals/news (60 req/min for TradingAgents users)
- yfinance for price data has no hard limits but can be throttled
- For production, consider Alpha Vantage Premium or caching strategies
- Local vendor option available for offline testing (requires Tauric TradingDB - in development)

### LLM Costs
- Framework makes many LLM calls (analysts + researchers + debaters)
- Recommended for testing: o4-mini + gpt-4o-mini to minimize costs
- Recommended for research: o1-preview + gpt-4o for best performance
- Reduce costs: decrease `max_debate_rounds`, select fewer analysts

### Reflection Performance
- Enabling reflection improves performance over time but increases runtime
- Each reflection requires additional LLM calls
- Use `reflection_on_close_only=True` for more realistic learning (only learns from completed trades)

## File Organization

```
tradingagents/
├── agents/                    # Agent implementations
│   ├── analysts/             # Market, news, fundamentals, social analysts
│   ├── researchers/          # Bull/bear researchers
│   ├── trader/               # Trader agent
│   ├── risk_mgmt/           # Risk management team
│   ├── managers/            # Research and risk managers
│   └── utils/               # Agent tools, states, memory
├── backtesting/              # Backtesting framework
│   ├── engine.py            # Main backtest engine
│   ├── config.py            # Backtest configuration
│   ├── analytics.py         # Performance metrics
│   ├── visualization.py     # Charts and plots
│   ├── strategy.py          # Strategy wrapper
│   └── utils.py             # Helper functions
├── dataflows/                # Data vendor integrations
│   ├── interface.py         # Vendor abstraction layer
│   ├── alpha_vantage*.py   # Alpha Vantage integration
│   ├── y_finance.py        # yfinance integration
│   ├── openai.py           # OpenAI data generation
│   └── local.py            # Local data access
├── graph/                    # LangGraph orchestration
│   ├── trading_graph.py    # Main graph class
│   ├── setup.py            # Graph construction
│   ├── propagation.py      # State propagation
│   ├── reflection.py       # Learning system
│   ├── signal_processing.py # Decision processing
│   └── conditional_logic.py # Routing logic
└── default_config.py         # Default configuration

cli/                          # Command-line interface
├── main.py                   # CLI entry point
├── backtest.py              # Backtest CLI commands
├── models.py                # CLI data models
└── utils.py                 # CLI utilities

examples/                     # Example scripts
├── simple_backtest.py       # Basic single-ticker backtest
├── portfolio_backtest.py    # Multi-ticker portfolio
└── advanced_backtest.py     # Advanced configuration

tests/                        # Test suite
└── test_backtesting.py      # Backtesting tests
```

## Research Context

This framework implements the TradingAgents research paper (arXiv:2412.20138). The multi-agent architecture with debate, reflection, and specialized roles is core to the approach. When modifying the system, maintain the separation of concerns between analyst research, researcher debate, trader planning, and risk management approval.
