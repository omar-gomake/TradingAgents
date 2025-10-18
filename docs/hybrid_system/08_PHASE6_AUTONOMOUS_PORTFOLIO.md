# Phase 6: Autonomous Portfolio Manager
## Full Portfolio-Level Automation - The Crown Jewel

**Duration:** 2 weeks (Weeks 11-12)
**Difficulty:** Very High
**Impact:** ⭐⭐⭐⭐⭐ (FULL AUTONOMY + 15-20% from optimization)
**Prerequisites:** Phases 1-2 required, 3-5 recommended

---

## Overview

This is THE transformative phase that creates a truly autonomous trading system:

**Current State:** Analyze single stocks when YOU tell it to
**Target State:** System automatically screens universe, selects opportunities, manages portfolio, rebalances, and learns - 24/7 without human intervention

---

## Complete Autonomous Workflow

### Daily 6:00 AM - Regime Detection
```python
regime = regime_detector.detect_regime(market="SPY", date=today)
# → Classifies: bull_trending / bear_trending / high_volatility / crisis
```

### Daily 6:30 AM - Universe Screening
```python
screener = UniverseScreener()
candidates = screener.screen(
    universe=sp500_tickers,
    factors=['momentum', 'value', 'quality'],
    top_n=50
)
# → Returns top 50 opportunities ranked by multi-factor score
```

### Daily 7:00-9:00 AM - Deep Analysis
```python
for ticker in candidates:
    # Director selects optimal analysts for this stock + regime
    analysts_config = director.select_analysts(ticker, regime)

    # Run full TradingAgents pipeline
    decision = trading_graph.propagate(ticker, today)

    # Store analysis
    opportunity_pool.add(ticker, decision)
```

### Daily 9:15 AM - Portfolio Optimization
```python
optimizer = PortfolioOptimizer()
target_weights = optimizer.optimize(
    opportunities=opportunity_pool,
    current_portfolio=current_holdings,
    regime=regime,
    method='risk_parity'  # or 'mean_variance', 'black_litterman'
)
# → {'AAPL': 0.15, 'GOOGL': 0.12, 'MSFT': 0.13, ...}
```

### Daily 9:20 AM - Risk Allocation
```python
risk_allocator = RiskAllocator()
final_weights = risk_allocator.allocate(
    target_weights=target_weights,
    portfolio_var_limit=0.02,  # 2% daily VaR max
    sector_limits={'Tech': 0.40, 'Finance': 0.25, ...},
    correlation_limits=0.70  # Max pairwise correlation
)
```

### Daily 9:25 AM - Generate Trades
```python
rebalancer = RebalancingEngine()
trades = rebalancer.generate_trades(
    current_portfolio=current_holdings,
    target_portfolio=final_weights,
    minimize_tax=True,
    max_turnover=0.25  # Max 25% portfolio turnover per day
)
```

### Daily 9:30 AM - Execute
```python
executor = TradeExecutor()
for trade in trades:
    executor.place_order(trade)
    # → Actual brokerage integration
```

### Throughout Day - Monitor & Adjust
```python
monitor = PortfolioMonitor()
monitor.check_stop_losses()
monitor.check_take_profits()
monitor.check_risk_limits()

if monitor.regime_changed():
    # Re-optimize if regime shifts mid-day
    trigger_rebalance()
```

### Daily 4:00 PM - Close & Reflect
```python
reflector = PortfolioReflector()
reflector.analyze_day_performance()
reflector.update_agent_memories()
reflector.update_meta_learner()
```

---

## Key Components

### 1. Universe Screener
```python
# tradingagents/portfolio/universe_screener.py

class UniverseScreener:
    """Screen thousands of stocks for opportunities."""

    def screen(
        self,
        universe: List[str],
        factors: List[str],
        top_n: int = 50
    ) -> List[Dict]:
        """
        Multi-factor screening.

        Factors:
        - momentum: Price momentum (6mo, 3mo, 1mo)
        - value: P/E, P/B, EV/EBITDA
        - quality: ROE, debt/equity, cash flow
        - growth: Revenue growth, earnings growth
        - liquidity: Volume, market cap

        Returns:
            [
                {'ticker': 'AAPL', 'score': 0.85, 'factors': {...}},
                {'ticker': 'GOOGL', 'score': 0.82, 'factors': {...}},
                ...
            ]
        """
        pass
```

### 2. Portfolio Optimizer
```python
# tradingagents/portfolio/optimizer.py

class PortfolioOptimizer:
    """Optimize portfolio weights."""

    def optimize(
        self,
        opportunities: List[Dict],
        current_portfolio: Dict,
        regime: str,
        method: str = 'risk_parity'
    ) -> Dict[str, float]:
        """
        Methods:
        - mean_variance: Markowitz optimization
        - risk_parity: Equal risk contribution
        - black_litterman: Bayesian with agent views
        - hierarchical_risk_parity: Correlation-based
        - kelly: Kelly criterion with safety margin
        """
        pass
```

### 3. Risk Allocator
```python
# tradingagents/portfolio/risk_allocator.py

class RiskAllocator:
    """Manage portfolio-level risk."""

    def allocate(
        self,
        target_weights: Dict[str, float],
        constraints: Dict
    ) -> Dict[str, float]:
        """
        Enforce constraints:
        - Portfolio VaR < X%
        - Max position size
        - Sector exposure limits
        - Correlation limits
        - Leverage limits
        """
        pass
```

---

## Full Autonomy Checklist

- [ ] Universe screening (daily)
- [ ] Opportunity analysis (per candidate)
- [ ] Portfolio optimization (daily)
- [ ] Risk management (real-time)
- [ ] Order execution (automated)
- [ ] Position monitoring (real-time)
- [ ] Rebalancing (triggered or scheduled)
- [ ] Performance tracking (continuous)
- [ ] Meta-learning (daily)
- [ ] Error handling & recovery (24/7)
- [ ] Notifications (critical events)

---

## Expected Results

**Before Phase 6:**
- Manual stock selection
- Single-position decisions
- No portfolio optimization
- Human intervention required

**After Phase 6:**
- Fully autonomous operation
- Portfolio-level optimization
- Risk-managed diversification
- Zero human intervention needed
- **+15-20% from portfolio optimization**
- **True set-and-forget trading system**

---

## Next Phase

Continue to [09_PHASE7_RISK_REGIME.md](09_PHASE7_RISK_REGIME.md)
