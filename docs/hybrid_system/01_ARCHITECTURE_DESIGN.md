# System Architecture Design
## TradingAgents × FinRobot Hybrid System

**Last Updated:** 2025-10-18
**Status:** Detailed Design

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Layer-by-Layer Design](#layer-by-layer-design)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Agent Communication Patterns](#agent-communication-patterns)
5. [State Management](#state-management)
6. [Memory and Learning Systems](#memory-and-learning-systems)
7. [Technology Stack](#technology-stack)
8. [Integration Points](#integration-points)

---

## Architecture Overview

The hybrid system follows a **7-layer architecture** that combines TradingAgents' proven multi-agent framework with FinRobot's adaptive intelligence layer.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 7: AUTONOMOUS PORTFOLIO MANAGER                                │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │  Universe   │ │ Portfolio   │ │    Risk     │ │ Rebalancing │   │
│ │  Screener   │→│ Optimizer   │→│  Allocator  │→│   Engine    │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │
│ │   Regime    │ │   Capital   │ │ Performance │                   │
│ │  Detector   │→│   Manager   │→│   Monitor   │                   │
│ └─────────────┘ └─────────────┘ └─────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 6: SMART SCHEDULER & DIRECTOR AGENT (FinRobot)                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │  Director   │ │ Performance │ │   Agent     │ │   Model     │   │
│ │   Agent     │→│   Tracker   │→│  Registry   │→│   Router    │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 5: ENHANCED ANALYST LAYER (Hybrid)                             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │   Market    │ │     SEC     │ │Fundamentals │ │    News     │   │
│ │ Analyst+CoT │ │ Analyst NEW │ │ Analyst+CoT │ │ Analyst+CoT │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
│ ┌─────────────┐ ┌─────────────┐                                    │
│ │   Social    │ │   Dynamic   │                                    │
│ │  Analyst    │ │  Strategy   │                                    │
│ │             │ │  Generator  │                                    │
│ └─────────────┘ └─────────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 4: RESEARCHER DEBATE LAYER (TradingAgents)                     │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                    │
│ │    Bull     │↔│    Bear     │→│  Research   │                    │
│ │ Researcher  │ │ Researcher  │ │   Manager   │                    │
│ └─────────────┘ └─────────────┘ └─────────────┘                    │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 3: TRADER & ENSEMBLE PREDICTION (Enhanced)                     │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                    │
│ │   Trader    │ │   Ensemble  │ │   Custom    │                    │
│ │ Agent + CoT │→│  Predictor  │→│  Algorithm  │                    │
│ └─────────────┘ └─────────────┘ └─────────────┘                    │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 2: RISK MANAGEMENT LAYER (TradingAgents)                       │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │ Aggressive  │↔│  Neutral    │↔│Conservative │→│    Risk     │   │
│ │  Debator    │ │  Debator    │ │  Debator    │ │   Manager   │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 1: EXECUTION & REFLECTION (TradingAgents Enhanced)             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │  Position   │→│   Order     │→│ Performance │→│Multi-Agent  │   │
│ │   Sizing    │ │  Execution  │ │  Tracking   │ │ Reflection  │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer-by-Layer Design

### Layer 7: Autonomous Portfolio Manager

**Purpose:** Complete portfolio-level automation without human intervention

**Components:**

#### 7.1 Universe Screener
```python
# File: tradingagents/portfolio/universe_screener.py

class UniverseScreener:
    """
    Screens thousands of stocks to identify best opportunities.

    Capabilities:
    - Multi-factor scoring (momentum, value, quality, growth)
    - Liquidity filtering (minimum volume, market cap)
    - Sector diversification constraints
    - Custom factor models
    - Dynamic universe expansion/contraction
    """

    def screen_universe(self, date: str, target_count: int = 50) -> List[str]:
        """
        Screen universe and return top opportunities.

        Returns:
            List of tickers ranked by multi-factor score
        """
        pass
```

#### 7.2 Portfolio Optimizer
```python
# File: tradingagents/portfolio/optimizer.py

class PortfolioOptimizer:
    """
    Optimizes portfolio weights based on multiple objectives.

    Methods:
    - Mean-variance optimization (Markowitz)
    - Risk parity allocation
    - Hierarchical Risk Parity (HRP)
    - Black-Litterman with agent views
    - Kelly Criterion with safety margin
    """

    def optimize(
        self,
        candidates: List[Dict],
        current_portfolio: Dict,
        regime: str
    ) -> Dict[str, float]:
        """
        Calculate optimal portfolio weights.

        Args:
            candidates: Analyzed opportunities with scores
            current_portfolio: Current holdings
            regime: Market regime (bull/bear/volatile/crisis)

        Returns:
            Dict of ticker: target_weight
        """
        pass
```

#### 7.3 Risk Allocator
```python
# File: tradingagents/portfolio/risk_allocator.py

class RiskAllocator:
    """
    Manages portfolio-level risk budgets.

    Features:
    - Position-level risk limits
    - Portfolio VaR constraints
    - Correlation-based diversification
    - Sector exposure limits
    - Dynamic leverage adjustment
    """

    def allocate_risk(
        self,
        optimal_weights: Dict[str, float],
        risk_budget: float
    ) -> Dict[str, float]:
        """
        Adjust weights to meet risk constraints.
        """
        pass
```

#### 7.4 Regime Detector
```python
# File: tradingagents/portfolio/regime_detector.py

class MarketRegimeDetector:
    """
    Detects current market regime for strategy adaptation.

    Regimes:
    - Bull Trending: High momentum, low volatility
    - Bear Trending: Sustained downtrend
    - High Volatility: Large swings, choppy action
    - Mean Reverting: Range-bound market
    - Crisis: Severe risk-off environment
    """

    def detect_regime(self, date: str) -> Dict[str, Any]:
        """
        Classify current market regime.

        Returns:
            {
                'regime': 'bull_trending',
                'confidence': 0.85,
                'volatility_percentile': 0.35,
                'trend_strength': 0.72
            }
        """
        pass
```

#### 7.5 Rebalancing Engine
```python
# File: tradingagents/portfolio/rebalancing_engine.py

class RebalancingEngine:
    """
    Executes portfolio rebalancing decisions.

    Features:
    - Transaction cost minimization
    - Tax-loss harvesting
    - Gradual rebalancing (reduce market impact)
    - Cash management
    - Dividend reinvestment
    """

    def generate_trades(
        self,
        current_portfolio: Dict,
        target_portfolio: Dict,
        cash_available: float
    ) -> List[Trade]:
        """
        Generate optimal sequence of trades.
        """
        pass
```

---

### Layer 6: Smart Scheduler & Director Agent

**Purpose:** Adaptive agent selection and LLM routing based on performance

**Components:**

#### 6.1 Director Agent
```python
# File: tradingagents/agents/meta/director_agent.py

class DirectorAgent:
    """
    Orchestrates analyst selection based on market regime and past performance.

    Responsibilities:
    - Evaluate market conditions
    - Select optimal analyst combination
    - Determine debate rounds needed
    - Adjust agent weights dynamically
    - Route to best LLM per task
    """

    def select_analysts(
        self,
        ticker: str,
        date: str,
        regime: Dict[str, Any],
        complexity: str = "medium"
    ) -> List[str]:
        """
        Select optimal analysts for current situation.

        Examples:
        - Bull market + tech stock → market, social, fundamentals
        - Earnings season → fundamentals, news, SEC
        - High volatility → market, risk, news
        - Crisis → all analysts, max debate rounds

        Returns:
            List of analyst types to activate
        """
        pass

    def select_llm(self, task_type: str, complexity: str) -> str:
        """
        Route to best LLM based on task and historical performance.

        Task Types:
        - "analysis": Quick thinking LLM
        - "reasoning": Deep thinking LLM
        - "prediction": FinGPT or ensemble
        - "code_gen": GPT-4 for Text2Code
        """
        pass
```

#### 6.2 Performance Tracker
```python
# File: tradingagents/agents/meta/performance_tracker.py

class PerformanceTracker:
    """
    Tracks agent and model performance across market conditions.

    Metrics Tracked:
    - Analyst accuracy by regime
    - LLM performance by task type
    - Debate effectiveness
    - Time to decision
    - Cost per decision
    """

    def record_decision(
        self,
        decision: Dict,
        outcome: Dict,
        regime: str,
        analysts_used: List[str]
    ):
        """
        Record decision and eventual outcome for learning.
        """
        pass

    def get_analyst_weights(
        self,
        regime: str,
        ticker_sector: str
    ) -> Dict[str, float]:
        """
        Get performance-based weights for analyst aggregation.

        Returns:
            {'market': 0.35, 'fundamentals': 0.40, 'news': 0.25}
        """
        pass
```

#### 6.3 Agent Registry
```python
# File: tradingagents/agents/meta/agent_registry.py

class AgentRegistry:
    """
    Maintains registry of all available agents and their capabilities.
    """

    def register_agent(
        self,
        agent_type: str,
        capabilities: List[str],
        supported_regimes: List[str],
        cost: float
    ):
        """Register a new agent type."""
        pass

    def get_compatible_agents(
        self,
        task: str,
        regime: str,
        max_cost: float = None
    ) -> List[str]:
        """Get agents compatible with task and regime."""
        pass
```

---

### Layer 5: Enhanced Analyst Layer

**Purpose:** Deep market analysis with Financial Chain-of-Thought reasoning

**Key Enhancement:** All analysts now use Financial CoT prompting patterns

#### 5.1 Financial CoT Prompt Structure

Every analyst follows this reasoning chain:

```
1. DATA GATHERING STEP
   - What data do I need?
   - How do I validate data quality?
   - What's missing?

2. COMPONENT ANALYSIS STEP
   - Break down complex information
   - Analyze each component separately
   - Look for patterns and anomalies

3. CROSS-VALIDATION STEP
   - Check for contradictions
   - Verify key assumptions
   - Test edge cases

4. SYNTHESIS STEP
   - Combine insights
   - Weigh relative importance
   - Form coherent picture

5. PREDICTION STEP
   - Make specific forecast
   - Quantify confidence level
   - State key risks
```

#### 5.2 Enhanced Market Analyst
```python
# File: tradingagents/agents/analysts/market_analyst.py (Enhanced)

# New Financial CoT System Prompt:
MARKET_ANALYST_COT_PROMPT = """
You are a professional technical analyst following a structured analysis workflow.

STEP 1 - DATA GATHERING:
- First, identify which technical indicators are most relevant for the current market condition
- Call get_stock_data to retrieve price history
- Call get_indicators with selected indicators
- Validate data completeness and quality

STEP 2 - COMPONENT ANALYSIS:
- Analyze trend indicators (SMAs, EMAs) separately
- Analyze momentum indicators (RSI, MACD) separately
- Analyze volatility indicators (Bollinger Bands, ATR) separately
- Analyze volume patterns independently

STEP 3 - CROSS-VALIDATION:
- Check for contradictions between indicators
- Verify support/resistance levels with multiple timeframes
- Compare current patterns to historical analogs
- Test whether signals are confirmed across indicator types

STEP 4 - SYNTHESIS:
- Weight each indicator by reliability in current regime
- Combine signals into coherent market view
- Identify confluence zones (multiple signals agreeing)
- Note divergences that might signal reversals

STEP 5 - PREDICTION & CONFIDENCE:
- State clear directional bias (bullish/bearish/neutral)
- Quantify confidence level (high/medium/low)
- Identify key price levels and catalysts
- List primary risks to your thesis

OUTPUT FORMAT:
Provide detailed analysis following these steps, then create a summary markdown table.
"""
```

#### 5.3 NEW: SEC Document Analyst
```python
# File: tradingagents/agents/analysts/sec_analyst.py

class SECAnalyst:
    """
    Deep analysis of SEC filings (10-K, 10-Q, 8-K, earnings transcripts).

    Capabilities:
    - Download and parse latest filings
    - Extract Risk Factors section → identify emerging risks
    - Analyze MD&A → understand management outlook
    - Track quarter-over-quarter changes
    - Identify accounting red flags
    - Compare competitive positioning
    - Extract forward guidance
    """

    def analyze_filing(
        self,
        ticker: str,
        filing_type: str,
        date: str
    ) -> Dict[str, Any]:
        """
        Comprehensive SEC filing analysis.

        Returns:
            {
                'risk_factors': {...},
                'management_outlook': {...},
                'accounting_quality': {...},
                'competitive_position': {...},
                'guidance': {...},
                'red_flags': [...],
                'key_changes': [...]
            }
        """
        pass
```

#### 5.4 Dynamic Strategy Generator (Text2Code)
```python
# File: tradingagents/agents/generators/strategy_generator.py

class DynamicStrategyGenerator:
    """
    Generates custom indicators and algorithms on-the-fly.

    Powered by FinRobot's Text2Code capability.
    """

    def generate_custom_indicator(
        self,
        market_condition: str,
        objective: str,
        data_available: List[str]
    ) -> str:
        """
        Generate Python code for custom indicator.

        Example:
            generate_custom_indicator(
                market_condition="high_volatility_mean_reverting",
                objective="identify_oversold_bounces",
                data_available=["price", "volume", "RSI", "ATR"]
            )

        Returns:
            Python function code (validated and safe to execute)
        """
        pass

    def generate_position_sizing_algorithm(
        self,
        regime: str,
        risk_tolerance: float,
        portfolio_state: Dict
    ) -> str:
        """
        Generate custom position sizing logic.
        """
        pass
```

---

### Layer 4: Researcher Debate Layer

**Purpose:** Multi-perspective investment analysis through structured debate

**No changes to core logic, but enhanced with:**
- Financial CoT in researcher prompts
- Performance-based weighting from Layer 6
- Adaptive debate rounds based on complexity

```python
# File: tradingagents/agents/researchers/bull_researcher.py (Enhanced)

# Enhanced with Financial CoT:
BULL_RESEARCHER_COT_PROMPT = """
You are a bullish investment researcher. Follow this structured analysis:

STEP 1 - GATHER BULLISH EVIDENCE:
- Review all analyst reports systematically
- Extract positive signals and catalysts
- Identify growth opportunities

STEP 2 - ANALYZE STRENGTH OF EVIDENCE:
- Rate quality of each bullish signal
- Check historical reliability
- Verify with independent sources

STEP 3 - ANTICIPATE COUNTER-ARGUMENTS:
- Identify weaknesses in bullish case
- Prepare responses to bearish concerns
- Acknowledge uncertainties

STEP 4 - BUILD INVESTMENT THESIS:
- Synthesize evidence into coherent narrative
- Prioritize by impact and probability
- Create risk-adjusted expected return estimate

STEP 5 - FORMULATE POSITION:
- State bullish thesis clearly
- Recommend position size based on conviction
- Define success metrics and exit criteria
"""
```

---

### Layer 3: Trader & Ensemble Prediction

**Purpose:** Trading decision with multi-model prediction

#### 3.1 Enhanced Trader Agent
```python
# File: tradingagents/agents/trader/trader.py (Enhanced)

class EnhancedTrader:
    """
    Trader agent with Financial CoT and ensemble predictions.
    """

    def make_decision(
        self,
        investment_plan: str,
        analyst_reports: Dict,
        ensemble_predictions: Dict,
        custom_indicators: Dict
    ) -> Dict[str, Any]:
        """
        Final trading decision incorporating all inputs.

        Returns:
            {
                'action': 'BUY',
                'confidence': 0.78,
                'position_size': 0.15,  # 15% of portfolio
                'stop_loss': 0.08,
                'take_profit': 0.25,
                'holding_period': '2-4 weeks',
                'reasoning': '...'
            }
        """
        pass
```

#### 3.2 Ensemble Predictor
```python
# File: tradingagents/agents/predictors/ensemble_predictor.py

class EnsemblePredictor:
    """
    Combines predictions from multiple LLM models.

    Models:
    - GPT-4o (general reasoning)
    - o4-mini (deep analytical thinking)
    - Claude (alternative perspective)
    - FinGPT-Forecaster (domain-specific)
    """

    def predict(
        self,
        ticker: str,
        date: str,
        horizon: str,
        analyst_reports: Dict
    ) -> Dict[str, Any]:
        """
        Generate ensemble prediction.

        Returns:
            {
                'predicted_return': 0.12,
                'confidence_interval': (0.05, 0.20),
                'uncertainty': 0.35,
                'model_agreement': 0.82,
                'individual_predictions': {
                    'gpt4o': 0.15,
                    'o4mini': 0.11,
                    'claude': 0.10,
                    'fingpt': 0.13
                }
            }
        """
        pass
```

---

### Layer 2: Risk Management Layer

**Purpose:** Multi-perspective risk evaluation

**Enhanced with:**
- Portfolio-level risk metrics from Layer 7
- Regime-aware risk tolerance adjustment
- Financial CoT in risk debator prompts

---

### Layer 1: Execution & Reflection

**Purpose:** Trade execution and multi-agent learning

**Enhanced with:**
- Performance tracking feeds Layer 6
- Agent-specific reflection based on individual performance
- Portfolio-level reflection for meta-learning

```python
# File: tradingagents/graph/reflection.py (Enhanced)

class EnhancedReflector:
    """
    Multi-level reflection system.
    """

    def reflect_agent_performance(
        self,
        agent_type: str,
        decision: Dict,
        outcome: Dict,
        regime: str
    ):
        """
        Agent-specific reflection and memory update.
        """
        pass

    def reflect_portfolio_performance(
        self,
        period_results: Dict,
        regime_changes: List[Dict]
    ):
        """
        Portfolio-level meta-learning.

        Learns:
        - Which agent combinations work best
        - Optimal regime detection thresholds
        - Position sizing effectiveness
        - Rebalancing frequency optimization
        """
        pass
```

---

## Data Flow Architecture

### Primary Data Flow

```
External Data Sources
        │
        ├─→ yfinance (Price Data)
        ├─→ Alpha Vantage (Fundamentals, News)
        ├─→ SEC EDGAR (Filings)
        └─→ Reddit/Twitter APIs (Sentiment)
        │
        ▼
Data Vendor Layer (tradingagents/dataflows/)
        │
        ├─→ Caching Layer (Reduce API calls)
        ├─→ Data Validation
        └─→ Format Standardization
        │
        ▼
Tool Layer (tradingagents/agents/utils/*_tools.py)
        │
        ├─→ get_stock_data()
        ├─→ get_indicators()
        ├─→ get_fundamentals()
        ├─→ get_news()
        └─→ get_sec_filings() [NEW]
        │
        ▼
Analyst Layer (With Financial CoT)
        │
        ├─→ Market Analyst
        ├─→ SEC Analyst [NEW]
        ├─→ Fundamentals Analyst
        ├─→ News Analyst
        └─→ Social Analyst
        │
        ▼
Smart Scheduler (Director Agent selects best analysts)
        │
        ▼
Researcher Debate (Bull vs Bear)
        │
        ▼
Ensemble Prediction (Multiple LLMs)
        │
        ▼
Trader Decision (Financial CoT)
        │
        ▼
Risk Debate (3-way discussion)
        │
        ▼
Portfolio Optimization
        │
        ▼
Execution
        │
        ▼
Reflection & Learning → Feeds back to Performance Tracker
```

---

## Agent Communication Patterns

### Pattern 1: Sequential Analysis (Current TradingAgents)
```
Analyst A → Analyst B → Analyst C → Researcher Team → Trader → Risk Team
```

### Pattern 2: Director-Orchestrated (NEW)
```
Director Agent → Selects [Analyst B, Analyst D, Analyst F]
              → Analysts execute in parallel
              → Director aggregates with performance weights
              → Researcher Team (adaptive rounds)
              → Ensemble Prediction
              → Trader
              → Risk Team (adaptive rounds)
```

### Pattern 3: Portfolio-Level (NEW)
```
Regime Detector → Universe Screener → (For each candidate):
                                       ├→ Director Agent
                                       ├→ Analysis Pipeline
                                       └→ Decision
                → Portfolio Optimizer
                → Risk Allocator
                → Rebalancing Engine
                → Execution
```

---

## State Management

### Enhanced AgentState

```python
# File: tradingagents/agents/utils/agent_states.py (Enhanced)

class EnhancedAgentState(MessagesState):
    """Enhanced state with new fields for hybrid system."""

    # Existing fields
    company_of_interest: str
    trade_date: str
    sender: str

    # Analyst reports (existing)
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str

    # NEW: Additional analyst reports
    sec_report: str  # SEC filing analysis
    custom_indicators: Dict[str, Any]  # Dynamic indicators

    # NEW: Director Agent metadata
    selected_analysts: List[str]  # Which analysts were chosen
    analyst_weights: Dict[str, float]  # Performance-based weights
    complexity_score: float  # Decision complexity assessment
    regime_info: Dict[str, Any]  # Market regime data

    # Debate states (existing)
    investment_debate_state: InvestDebateState
    risk_debate_state: RiskDebateState

    # NEW: Ensemble prediction
    ensemble_predictions: Dict[str, Any]
    model_uncertainty: float

    # Trading decision (existing)
    investment_plan: str
    trader_investment_plan: str
    final_trade_decision: str

    # NEW: Portfolio context
    portfolio_state: Dict[str, Any]
    position_limits: Dict[str, float]
    risk_budget: float
```

### Portfolio State

```python
# File: tradingagents/portfolio/state.py

class PortfolioState:
    """Complete portfolio state for autonomous management."""

    current_positions: Dict[str, Position]
    cash_available: float
    total_equity: float
    unrealized_pnl: float
    realized_pnl: float

    # Risk metrics
    portfolio_beta: float
    portfolio_var: float
    max_drawdown: float
    correlation_matrix: pd.DataFrame

    # Regime tracking
    current_regime: str
    regime_confidence: float
    regime_change_date: Optional[str]

    # Performance tracking
    daily_returns: List[float]
    sharpe_ratio: float
    win_rate: float
```

---

## Memory and Learning Systems

### Three-Tier Memory Architecture

#### Tier 1: Agent-Level Memory (Existing - Enhanced)
```python
# File: tradingagents/agents/utils/memory.py (Enhanced)

class FinancialSituationMemory:
    """
    Enhanced with performance tracking.
    """

    def add_situation_with_metadata(
        self,
        situation: str,
        recommendation: str,
        outcome: Dict,
        regime: str,
        confidence: float
    ):
        """Store memory with rich metadata for better retrieval."""
        pass

    def get_relevant_memories(
        self,
        current_situation: str,
        current_regime: str,
        n_matches: int = 3
    ) -> List[Dict]:
        """Retrieve memories filtered by regime similarity."""
        pass
```

#### Tier 2: Performance Tracking Database (NEW)
```python
# File: tradingagents/agents/meta/performance_db.py

class PerformanceDatabase:
    """
    Central database for all performance metrics.

    Schema:
    - decisions: All trading decisions with context
    - outcomes: Actual returns and metrics
    - analyst_performance: Accuracy by analyst type
    - model_performance: LLM performance by task
    - regime_performance: Strategy effectiveness by regime
    """

    def record_decision_outcome(
        self,
        decision_id: str,
        outcome: Dict,
        analysts_used: List[str],
        regime: str
    ):
        """Record for meta-learning."""
        pass

    def query_best_strategy(
        self,
        regime: str,
        sector: str,
        market_cap: str
    ) -> Dict[str, Any]:
        """Query historical best practices."""
        pass
```

#### Tier 3: Meta-Learning System (NEW)
```python
# File: tradingagents/portfolio/meta_learner.py

class MetaLearner:
    """
    Learn across all trades and agents.

    Meta-Learning Objectives:
    - Optimal analyst combinations by regime
    - Best LLM routing strategies
    - Effective debate round counts
    - Position sizing heuristics
    - Rebalancing frequency
    """

    def learn_analyst_selection(
        self,
        historical_decisions: List[Dict]
    ) -> Dict[str, Any]:
        """
        Learn which analyst combinations work best.

        Returns:
            Rules like: "In bull markets for tech stocks,
            use [market, fundamentals, social] with weights [0.3, 0.5, 0.2]"
        """
        pass
```

---

## Technology Stack

### Core Frameworks
- **LangChain**: Agent framework and LLM orchestration
- **LangGraph**: Workflow state machine and graph execution
- **Backtrader**: Backtesting engine
- **Pandas/NumPy**: Data manipulation
- **SQLite/PostgreSQL**: Performance tracking database

### LLM Providers
- **OpenAI**: GPT-4o, o4-mini (primary)
- **Anthropic**: Claude 3.5 Sonnet (alternative perspective)
- **Google**: Gemini (optional)
- **FinGPT**: Domain-specific financial models

### Data Sources
- **yfinance**: Price and technical data
- **Alpha Vantage**: Fundamentals and news
- **SEC EDGAR**: Official filings (10-K, 10-Q, 8-K)
- **Reddit/Twitter APIs**: Social sentiment

### Deployment
- **Docker**: Containerization
- **FastAPI**: REST API for external access
- **Celery**: Task queue for async processing
- **Redis**: Caching and message broker
- **Grafana**: Monitoring and dashboards

---

## Integration Points

### External System Integration

#### Brokerage Integration (Future)
```python
# File: tradingagents/execution/broker_interface.py

class BrokerInterface:
    """
    Abstract interface for broker integration.

    Supported Brokers:
    - Interactive Brokers (IBKR)
    - Alpaca
    - TD Ameritrade
    - Paper trading (simulation)
    """

    def place_order(self, order: Order) -> str:
        """Place order and return order ID."""
        pass

    def get_positions(self) -> Dict[str, Position]:
        """Get current positions."""
        pass

    def get_account_info(self) -> Dict[str, Any]:
        """Get account balance and buying power."""
        pass
```

#### Notification System
```python
# File: tradingagents/notifications/notifier.py

class Notifier:
    """
    Multi-channel notification system.

    Channels:
    - Email (critical alerts)
    - Slack (daily summaries)
    - Telegram (trade executions)
    - Dashboard (real-time)
    """

    def send_trade_notification(self, trade: Trade):
        """Notify on trade execution."""
        pass

    def send_performance_summary(self, period: str):
        """Send periodic performance reports."""
        pass

    def send_alert(self, alert_type: str, message: str):
        """Send critical system alerts."""
        pass
```

---

## Next Steps

**Continue to:** [03_PHASE1_FINANCIAL_COT.md](03_PHASE1_FINANCIAL_COT.md) for detailed implementation guide of Phase 1.

---

**Revision History:**
- 2025-10-18: Initial architecture design completed
