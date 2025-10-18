# Phase 4: Dynamic Strategy Generator (Text2Code)
## Generate Custom Algorithms On-The-Fly

**Duration:** 2 weeks (Weeks 7-8)
**Difficulty:** Very High
**Impact:** ⭐⭐⭐⭐ (+8-12% from market adaptability)
**Prerequisites:** Phases 1-2 completed (Phase 3 optional)

---

## Overview

Implement FinRobot's Text2Code capability to generate custom trading algorithms dynamically based on market conditions.

**Examples:**
- Detect market is mean-reverting → generate mean-reversion indicator
- High volatility regime → generate adaptive position sizing algorithm
- Earnings season → generate event-driven entry/exit rules

---

## Core Components

### 1. Strategy Generator Agent

```python
# tradingagents/agents/generators/strategy_generator.py

class StrategyGenerator:
    """Generate custom algorithms using LLM code generation."""

    def generate_indicator(self, market_condition: str, objective: str) -> str:
        """
        Generate Python code for custom indicator.

        Example:
            market_condition = "high_volatility_mean_reverting"
            objective = "identify_oversold_bounces"

        Returns:
            Safe, validated Python function
        """
        prompt = f"""
        Generate a Python function for a custom technical indicator.

        Market Condition: {market_condition}
        Objective: {objective}

        Requirements:
        - Input: pandas DataFrame with OHLCV data
        - Output: Series with indicator values
        - Use only: pandas, numpy, ta-lib (if needed)
        - No external API calls
        - No file I/O
        - Include docstring with usage

        Return ONLY the function code, nothing else.
        """

        # Get code from LLM
        # Validate code safety
        # Test with sample data
        # Return if valid
        pass

    def generate_position_sizing(self, regime: str, volatility: float) -> str:
        """Generate adaptive position sizing logic."""
        pass
```

### 2. Code Validation & Sandboxing

```python
# tradingagents/agents/generators/code_validator.py

class CodeValidator:
    """Validate and sandbox generated code for safety."""

    def validate_code(self, code: str) -> bool:
        """
        Check code is safe to execute.

        Blocks:
        - import os, sys, subprocess
        - file I/O operations
        - network calls
        - dangerous builtins (eval, exec, __import__)
        """
        pass

    def execute_safely(self, code: str, data: pd.DataFrame) -> pd.Series:
        """Execute code in restricted environment."""
        pass
```

---

## Use Cases

1. **Regime-Specific Indicators**
   - Bull market: momentum-following indicators
   - Bear market: defensive, reversal indicators
   - Volatile: risk-adjusted signals

2. **Adaptive Position Sizing**
   - High confidence + low volatility = larger positions
   - Low confidence + high volatility = smaller positions

3. **Custom Entry/Exit Rules**
   - Earnings events: specific timing rules
   - Fed announcements: volatility-adjusted entries

---

## Safety First

**Critical:** Generated code must be:
1. Validated for safety (no dangerous operations)
2. Tested on sample data before production use
3. Sandboxed execution environment
4. Fallback to known-good indicators if generation fails

---

## Next Phase

Continue to [07_PHASE5_ENSEMBLE_PREDICTOR.md](07_PHASE5_ENSEMBLE_PREDICTOR.md)
