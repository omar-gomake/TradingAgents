# Phase 7: Advanced Risk & Regime Detection
## Protect Downside and Adapt to Market Conditions

**Duration:** 2 weeks (Weeks 13-14)
**Difficulty:** High
**Impact:** ⭐⭐⭐⭐ (+20-30% from drawdown reduction)
**Prerequisites:** Phase 6 completed

---

## Overview

Advanced risk management and regime detection to:
- **Reduce maximum drawdown** by 40-60%
- **Adapt strategy** to market conditions automatically
- **Detect crises early** and reduce exposure before major losses
- **Optimize position sizing** by volatility regime

---

## Key Components

### 1. Enhanced Regime Detector

```python
# tradingagents/portfolio/regime_detector.py (Enhanced)

class AdvancedRegimeDetector:
    """
    Multi-timeframe, multi-asset regime detection.
    """

    def detect_regime(self, date: str) -> Dict:
        """
        Comprehensive regime classification.

        Regimes:
        1. BULL_TRENDING: Strong uptrend, low volatility
        2. BEAR_TRENDING: Strong downtrend
        3. HIGH_VOLATILITY: Large swings, choppy
        4. MEAN_REVERTING: Range-bound
        5. CRISIS: Severe market stress (VIX >40, correlations →1)

        Uses:
        - SPY trend (SMA 50/200)
        - VIX level and trend
        - Cross-asset correlations
        - Credit spreads (if available)
        - Market breadth (advance/decline)

        Returns:
            {
                'primary_regime': 'bull_trending',
                'confidence': 0.85,
                'regime_probabilities': {
                    'bull_trending': 0.75,
                    'mean_reverting': 0.20,
                    'high_volatility': 0.05
                },
                'regime_change_probability': 0.12,
                'days_in_regime': 45
            }
        """
        pass
```

### 2. Portfolio Risk Monitor

```python
# tradingagents/portfolio/risk_monitor.py

class PortfolioRiskMonitor:
    """Real-time portfolio risk monitoring."""

    def monitor(self, portfolio: Dict, market_data: Dict) -> Dict:
        """
        Calculate and monitor:

        - Portfolio Beta to SPY
        - Value at Risk (VaR) - 95th percentile
        - Expected Shortfall (CVaR) - tail risk
        - Correlation matrix health
        - Concentration risk (Herfindahl index)
        - Sector exposure
        - Leverage ratio
        - Liquidity score

        Triggers:
        - If VaR > limit → Reduce positions
        - If correlations → 1 → Diversification broken
        - If concentration > limit → Force rebalancing
        """
        pass

    def suggest_risk_reduction(self, risk_metrics: Dict) -> List[str]:
        """
        Suggest actions when risk is too high.

        Actions:
        - Reduce position sizes by X%
        - Close most volatile positions
        - Hedge with inverse ETF
        - Move to cash
        """
        pass
```

### 3. Regime-Adaptive Strategy

```python
# tradingagents/portfolio/adaptive_strategy.py

class RegimeAdaptiveStrategy:
    """Adjust trading parameters by regime."""

    def get_regime_parameters(self, regime: str) -> Dict:
        """
        Return optimal parameters for each regime.

        Example:
            regime = 'bull_trending'
            →  {
                'position_size': 0.95,  # Aggressive
                'stop_loss': 0.10,
                'take_profit': 0.25,
                'holding_period': 'weeks',
                'num_positions': 15,
                'analyst_selection': ['market', 'fundamentals', 'social'],
                'debate_rounds': 2
            }

            regime = 'crisis'
            →  {
                'position_size': 0.30,  # Very conservative
                'stop_loss': 0.05,
                'take_profit': 0.10,
                'holding_period': 'days',
                'num_positions': 5,
                'analyst_selection': ['market', 'news', 'risk'],
                'debate_rounds': 3
            }
        """
        pass
```

### 4. Drawdown Protection

```python
# tradingagents/portfolio/drawdown_protector.py

class DrawdownProtector:
    """Protect against large drawdowns."""

    def check_drawdown(self, equity_curve: List[float]) -> Dict:
        """
        Monitor portfolio drawdown.

        Actions based on drawdown level:
        - 5-10%: Alert, no action
        - 10-15%: Reduce position sizes by 25%
        - 15-20%: Reduce position sizes by 50%
        - >20%: Move to cash, reassess

        Returns:
            {
                'current_drawdown': 0.08,
                'max_drawdown': 0.12,
                'days_in_drawdown': 15,
                'action_required': 'reduce_25_percent'
            }
        """
        pass
```

---

## Regime-Specific Adjustments

| Regime | Position Size | Num Positions | Stop Loss | Take Profit | Strategy |
|--------|--------------|---------------|-----------|-------------|----------|
| Bull Trending | 90-95% | 15-20 | 10% | 25% | Momentum-following |
| Bear Trending | 40-50% | 5-10 | 5% | 12% | Defensive, short bias |
| High Volatility | 50-60% | 8-12 | 7% | 15% | Mean reversion, smaller size |
| Mean Reverting | 70-80% | 10-15 | 8% | 18% | Range trading |
| Crisis | 20-30% | 3-5 | 5% | 10% | Capital preservation |

---

## Expected Results

### Before Phase 7:
- Fixed position sizes regardless of volatility
- No adaptation to market regime changes
- Large drawdowns during crisis periods
- Max Drawdown: 15-25%

### After Phase 7:
- Adaptive position sizing by regime
- Early crisis detection → reduce exposure
- Regime-specific strategy selection
- **Max Drawdown: 8-12%** (50-60% improvement)
- **Sharpe Ratio improvement: +20-30%**

---

## Completion

**Congratulations!** After completing all 7 phases, you have built the ultimate autonomous trading system combining TradingAgents' multi-agent framework with FinRobot's adaptive intelligence.

**Continue to:** [10_DEPLOYMENT_GUIDE.md](10_DEPLOYMENT_GUIDE.md) for production deployment instructions.
