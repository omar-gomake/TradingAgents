# Phase 2: Smart Scheduler & Director Agent
## Adaptive Analyst Selection and LLM Routing

**Duration:** 2 weeks (Weeks 3-4)
**Difficulty:** High
**Impact:** ⭐⭐⭐⭐⭐ (+10-15% from optimal resource allocation)
**Prerequisites:** Phase 1 (Financial CoT) completed

---

## Overview

The Director Agent is FinRobot's adaptive intelligence layer that dynamically selects which analysts to use and which LLMs to route tasks to, based on:
1. **Market regime** (bull/bear/volatile/crisis)
2. **Historical analyst performance** (track record by regime)
3. **Task complexity** (simple vs complex decisions)
4. **Cost/performance tradeoffs**

**Key Innovation:** Instead of always running all analysts, the system learns which analysts perform best under which conditions and only uses them when needed.

---

## Architecture

### New Components

```
┌─────────────────────────────────────────────────────────────┐
│                    DIRECTOR AGENT                            │
│  - Analyze market regime                                     │
│  - Select optimal analyst combination                        │
│  - Route to best LLM per task                                │
│  - Adjust debate rounds based on complexity                  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│               PERFORMANCE TRACKER                            │
│  - Store all decisions with outcomes                         │
│  - Track analyst accuracy by regime                          │
│  - Track LLM performance by task type                        │
│  - Calculate performance-based weights                       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 AGENT REGISTRY                               │
│  - Register all available agents                             │
│  - Define capabilities and supported regimes                 │
│  - Track cost per agent invocation                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Guide

### Step 1: Create Performance Database

```python
# File: tradingagents/agents/meta/performance_db.py

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd


class PerformanceDatabase:
    """
    Tracks all trading decisions and outcomes for meta-learning.
    """

    def __init__(self, db_path: str = "performance_tracking.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Decisions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                ticker TEXT,
                date TEXT,
                regime TEXT,
                decision TEXT,  -- BUY/SELL/HOLD
                confidence REAL,
                analysts_used TEXT,  -- JSON list
                analyst_weights TEXT,  -- JSON dict
                llm_deep TEXT,
                llm_quick TEXT,
                debate_rounds INTEGER,
                created_at TEXT
            )
        """)

        # Outcomes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id TEXT,
                days_held INTEGER,
                return_pct REAL,
                win INTEGER,  -- 1=win, 0=loss
                sharpe REAL,
                max_drawdown REAL,
                recorded_at TEXT,
                FOREIGN KEY (decision_id) REFERENCES decisions (decision_id)
            )
        """)

        # Analyst performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyst_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analyst_type TEXT,
                regime TEXT,
                sector TEXT,
                accuracy REAL,
                avg_return REAL,
                sample_size INTEGER,
                last_updated TEXT
            )
        """)

        # LLM performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS llm_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llm_model TEXT,
                task_type TEXT,  -- analysis, reasoning, prediction
                regime TEXT,
                accuracy REAL,
                avg_latency REAL,
                cost_per_call REAL,
                sample_size INTEGER,
                last_updated TEXT
            )
        """)

        conn.commit()
        conn.close()

    def record_decision(
        self,
        decision_id: str,
        ticker: str,
        date: str,
        regime: str,
        decision: str,
        confidence: float,
        analysts_used: List[str],
        analyst_weights: Dict[str, float],
        llm_deep: str,
        llm_quick: str,
        debate_rounds: int
    ):
        """Record a trading decision."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO decisions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            decision_id,
            ticker,
            date,
            regime,
            decision,
            confidence,
            json.dumps(analysts_used),
            json.dumps(analyst_weights),
            llm_deep,
            llm_quick,
            debate_rounds,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def record_outcome(
        self,
        decision_id: str,
        days_held: int,
        return_pct: float,
        sharpe: float = None,
        max_drawdown: float = None
    ):
        """Record outcome of a decision."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        win = 1 if return_pct > 0 else 0

        cursor.execute("""
            INSERT INTO outcomes (decision_id, days_held, return_pct, win, sharpe, max_drawdown, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            decision_id,
            days_held,
            return_pct,
            win,
            sharpe,
            max_drawdown,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        # Update analyst performance
        self._update_analyst_performance(decision_id, return_pct > 0)

    def _update_analyst_performance(self, decision_id: str, success: bool):
        """Update analyst performance metrics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get decision details
        cursor.execute("""
            SELECT analysts_used, regime FROM decisions WHERE decision_id = ?
        """, (decision_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return

        analysts_used = json.loads(row[0])
        regime = row[1]

        # Update each analyst's performance
        for analyst in analysts_used:
            cursor.execute("""
                SELECT accuracy, sample_size FROM analyst_performance
                WHERE analyst_type = ? AND regime = ?
            """, (analyst, regime))

            result = cursor.fetchone()

            if result:
                current_accuracy, sample_size = result
                new_accuracy = (current_accuracy * sample_size + (1 if success else 0)) / (sample_size + 1)
                new_sample_size = sample_size + 1

                cursor.execute("""
                    UPDATE analyst_performance
                    SET accuracy = ?, sample_size = ?, last_updated = ?
                    WHERE analyst_type = ? AND regime = ?
                """, (new_accuracy, new_sample_size, datetime.now().isoformat(), analyst, regime))
            else:
                cursor.execute("""
                    INSERT INTO analyst_performance (analyst_type, regime, sector, accuracy, avg_return, sample_size, last_updated)
                    VALUES (?, ?, 'ALL', ?, 0, 1, ?)
                """, (analyst, regime, 1 if success else 0, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_analyst_weights(self, regime: str, min_sample_size: int = 5) -> Dict[str, float]:
        """
        Get performance-based weights for analysts in given regime.

        Returns:
            Dict mapping analyst_type to weight (0-1)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT analyst_type, accuracy, sample_size
            FROM analyst_performance
            WHERE regime = ? AND sample_size >= ?
        """, (regime, min_sample_size))

        results = cursor.fetchall()
        conn.close()

        if not results:
            # Equal weights if no data
            return {
                'market': 0.25,
                'fundamentals': 0.25,
                'news': 0.25,
                'social': 0.25
            }

        # Calculate weights proportional to accuracy
        total_accuracy = sum(r[1] for r in results)
        weights = {r[0]: r[1] / total_accuracy for r in results}

        return weights

    def get_best_analysts(
        self,
        regime: str,
        top_n: int = 3,
        min_sample_size: int = 5
    ) -> List[str]:
        """Get top N performing analysts for regime."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT analyst_type, accuracy
            FROM analyst_performance
            WHERE regime = ? AND sample_size >= ?
            ORDER BY accuracy DESC
            LIMIT ?
        """, (regime, min_sample_size, top_n))

        results = cursor.fetchall()
        conn.close()

        return [r[0] for r in results]

    def get_optimal_llm(self, task_type: str, regime: str) -> str:
        """Get best performing LLM for task type and regime."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT llm_model, accuracy
            FROM llm_performance
            WHERE task_type = ? AND regime = ?
            ORDER BY accuracy DESC
            LIMIT 1
        """, (task_type, regime))

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            # Defaults
            if task_type == "deep_reasoning":
                return "o4-mini"
            else:
                return "gpt-4o-mini"
```

### Step 2: Create Director Agent

```python
# File: tradingagents/agents/meta/director_agent.py

from typing import List, Dict, Any, Optional
from .performance_db import PerformanceDatabase
from .regime_detector import MarketRegimeDetector


class DirectorAgent:
    """
    Orchestrates analyst selection and LLM routing based on market conditions
    and historical performance.
    """

    def __init__(self, performance_db: PerformanceDatabase):
        self.performance_db = performance_db
        self.regime_detector = MarketRegimeDetector()

        # Default analyst combinations by regime (used when no historical data)
        self.default_analyst_combos = {
            'bull_trending': ['market', 'fundamentals', 'social'],
            'bear_trending': ['market', 'news', 'fundamentals'],
            'high_volatility': ['market', 'news', 'risk'],
            'mean_reverting': ['market', 'fundamentals'],
            'crisis': ['market', 'news', 'fundamentals', 'social'],  # all hands on deck
        }

    def select_analysts(
        self,
        ticker: str,
        date: str,
        complexity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Select optimal analysts for current situation.

        Args:
            ticker: Stock symbol
            date: Analysis date
            complexity: "simple", "medium", "complex"

        Returns:
            {
                'analysts': ['market', 'fundamentals', 'news'],
                'weights': {'market': 0.35, 'fundamentals': 0.40, 'news': 0.25},
                'regime': 'bull_trending',
                'debate_rounds': 2,
                'llm_deep': 'o4-mini',
                'llm_quick': 'gpt-4o-mini'
            }
        """
        # Detect current regime
        regime_info = self.regime_detector.detect_regime(ticker, date)
        regime = regime_info['regime']

        # Get historical performance-based weights
        analyst_weights = self.performance_db.get_analyst_weights(regime)

        # If we have enough historical data, use top performers
        best_analysts = self.performance_db.get_best_analysts(regime, top_n=4)

        if best_analysts:
            selected_analysts = best_analysts
        else:
            # Fall back to defaults
            selected_analysts = self.default_analyst_combos.get(
                regime,
                ['market', 'fundamentals', 'news']
            )

        # Adjust based on complexity
        if complexity == "simple":
            # Use fewer analysts for simple decisions
            selected_analysts = selected_analysts[:2]
            debate_rounds = 1
        elif complexity == "complex":
            # Use all analysts for complex decisions
            if len(selected_analysts) < 4:
                selected_analysts.extend(['news', 'social'])
            debate_rounds = 3
        else:
            debate_rounds = 2

        # Get optimal LLMs for this regime
        llm_deep = self.performance_db.get_optimal_llm("deep_reasoning", regime)
        llm_quick = self.performance_db.get_optimal_llm("analysis", regime)

        return {
            'analysts': selected_analysts,
            'weights': analyst_weights,
            'regime': regime,
            'regime_info': regime_info,
            'debate_rounds': debate_rounds,
            'llm_deep': llm_deep,
            'llm_quick': llm_quick,
            'complexity': complexity
        }

    def assess_decision_complexity(
        self,
        ticker: str,
        recent_volatility: float,
        recent_news_count: int
    ) -> str:
        """
        Assess decision complexity to determine resource allocation.

        Returns:
            "simple", "medium", or "complex"
        """
        complexity_score = 0

        # Volatility factor
        if recent_volatility > 0.4:  # High volatility
            complexity_score += 2
        elif recent_volatility > 0.25:
            complexity_score += 1

        # News factor
        if recent_news_count > 10:  # Lots of news
            complexity_score += 2
        elif recent_news_count > 5:
            complexity_score += 1

        if complexity_score >= 3:
            return "complex"
        elif complexity_score >= 1:
            return "medium"
        else:
            return "simple"
```

### Step 3: Create Simple Regime Detector

```python
# File: tradingagents/agents/meta/regime_detector.py

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any


class MarketRegimeDetector:
    """
    Detects market regime for strategy adaptation.
    """

    def detect_regime(self, ticker: str, date: str) -> Dict[str, Any]:
        """
        Detect current market regime.

        Returns:
            {
                'regime': 'bull_trending',
                'confidence': 0.85,
                'volatility_percentile': 0.35,
                'trend_strength': 0.72
            }
        """
        # Download price data
        stock = yf.Ticker(ticker)
        end_date = pd.to_datetime(date)
        start_date = end_date - pd.Timedelta(days=200)

        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            return {
                'regime': 'unknown',
                'confidence': 0.0,
                'volatility_percentile': 0.5,
                'trend_strength': 0.5
            }

        # Calculate indicators
        df['returns'] = df['Close'].pct_change()
        df['sma_50'] = df['Close'].rolling(window=50).mean()
        df['sma_200'] = df['Close'].rolling(window=200).mean()

        # Volatility (20-day)
        df['volatility'] = df['returns'].rolling(window=20).std() * np.sqrt(252)

        current_price = df['Close'].iloc[-1]
        sma_50 = df['sma_50'].iloc[-1]
        sma_200 = df['sma_200'].iloc[-1]
        volatility = df['volatility'].iloc[-1]

        # Volatility percentile
        vol_percentile = (df['volatility'].iloc[-60:] < volatility).sum() / 60

        # Trend strength
        if pd.notna(sma_50) and pd.notna(sma_200):
            trend_strength = abs(current_price - sma_200) / sma_200
        else:
            trend_strength = 0.0

        # Determine regime
        if pd.notna(sma_50) and pd.notna(sma_200):
            if current_price > sma_50 > sma_200:
                if vol_percentile < 0.4:
                    regime = 'bull_trending'
                    confidence = 0.9
                else:
                    regime = 'high_volatility'
                    confidence = 0.75
            elif current_price < sma_50 < sma_200:
                regime = 'bear_trending'
                confidence = 0.85
            elif vol_percentile > 0.7:
                regime = 'high_volatility'
                confidence = 0.8
            else:
                regime = 'mean_reverting'
                confidence = 0.7
        else:
            regime = 'unknown'
            confidence = 0.5

        return {
            'regime': regime,
            'confidence': confidence,
            'volatility_percentile': vol_percentile,
            'trend_strength': trend_strength
        }
```

### Step 4: Integrate Director Agent into TradingAgentsGraph

```python
# File: tradingagents/graph/trading_graph.py (Modified)

from tradingagents.agents.meta.director_agent import DirectorAgent
from tradingagents.agents.meta.performance_db import PerformanceDatabase

class TradingAgentsGraph:
    def __init__(self, selected_analysts=None, debug=False, config=None):
        """
        Enhanced initialization with Director Agent.
        """
        self.debug = debug
        self.config = config or DEFAULT_CONFIG

        # NEW: Initialize Director Agent and Performance Tracking
        self.performance_db = PerformanceDatabase()
        self.director_agent = DirectorAgent(self.performance_db)

        # If selected_analysts is None, let Director choose
        self.use_director = (selected_analysts is None)
        self.default_selected_analysts = selected_analysts or ["market", "fundamentals", "news"]

        # Rest of initialization...
        # (Keep existing code)

    def propagate(self, ticker: str, date: str):
        """
        Enhanced propagate with Director Agent selection.
        """
        # NEW: Let Director select analysts if enabled
        if self.use_director:
            director_decision = self.director_agent.select_analysts(
                ticker=ticker,
                date=date,
                complexity="medium"  # Can be made dynamic
            )

            selected_analysts = director_decision['analysts']
            analyst_weights = director_decision['weights']
            regime_info = director_decision['regime_info']

            if self.debug:
                print(f"\n[Director] Selected analysts: {selected_analysts}")
                print(f"[Director] Regime: {regime_info['regime']} (confidence: {regime_info['confidence']:.2f})")
                print(f"[Director] Analyst weights: {analyst_weights}")
        else:
            selected_analysts = self.default_selected_analysts
            analyst_weights = None
            regime_info = None

        # Build graph with selected analysts
        graph = self.graph_setup.setup_graph(selected_analysts=selected_analysts)

        # Run propagation
        # ... (existing code)

        # NEW: Store decision for performance tracking
        decision_id = f"{ticker}_{date}"
        if hasattr(self, 'performance_db'):
            self.performance_db.record_decision(
                decision_id=decision_id,
                ticker=ticker,
                date=date,
                regime=regime_info['regime'] if regime_info else 'unknown',
                decision=final_decision,
                confidence=0.75,  # Extract from state
                analysts_used=selected_analysts,
                analyst_weights=analyst_weights or {},
                llm_deep=self.config['deep_think_llm'],
                llm_quick=self.config['quick_think_llm'],
                debate_rounds=self.config['max_debate_rounds']
            )

        return final_state, final_decision
```

---

## Testing

### Test 1: Performance Tracking

```python
from tradingagents.agents.meta.performance_db import PerformanceDatabase

# Initialize database
db = PerformanceDatabase()

# Record a decision
db.record_decision(
    decision_id="AAPL_2024-01-15",
    ticker="AAPL",
    date="2024-01-15",
    regime="bull_trending",
    decision="BUY",
    confidence=0.85,
    analysts_used=["market", "fundamentals", "news"],
    analyst_weights={"market": 0.35, "fundamentals": 0.40, "news": 0.25},
    llm_deep="o4-mini",
    llm_quick="gpt-4o-mini",
    debate_rounds=2
)

# Later, record outcome
db.record_outcome(
    decision_id="AAPL_2024-01-15",
    days_held=14,
    return_pct=0.08,  # 8% profit
    sharpe=1.5
)

# Check analyst performance
weights = db.get_analyst_weights("bull_trending")
print(f"Analyst weights for bull market: {weights}")
```

### Test 2: Director Agent Selection

```python
from tradingagents.agents.meta.director_agent import DirectorAgent
from tradingagents.agents.meta.performance_db import PerformanceDatabase

db = PerformanceDatabase()
director = DirectorAgent(db)

# Get recommendations
selection = director.select_analysts(
    ticker="AAPL",
    date="2024-01-15",
    complexity="medium"
)

print(f"Selected analysts: {selection['analysts']}")
print(f"Regime: {selection['regime']}")
print(f"Debate rounds: {selection['debate_rounds']}")
print(f"LLMs: {selection['llm_deep']} (deep), {selection['llm_quick']} (quick)")
```

---

## Expected Results

### Before Director Agent:
- Always uses same 4 analysts regardless of market condition
- Fixed number of debate rounds
- No learning from past performance
- Equal weighting of all analysts

### After Director Agent:
- Adapts analyst selection to regime (e.g., uses fundamentals more in earnings season)
- Learns which analysts perform best in which conditions
- Adjusts debate rounds based on complexity
- Performance-weighted analyst aggregation
- **Result: +10-15% improvement from optimal resource allocation**

---

## Next Phase

Continue to **[05_PHASE3_SEC_ANALYZER.md](05_PHASE3_SEC_ANALYZER.md)** to add deep SEC filing analysis capabilities.

---

**Completion Checklist:**

- [ ] Create PerformanceDatabase
- [ ] Create RegimeDetector
- [ ] Create DirectorAgent
- [ ] Integrate into TradingAgentsGraph
- [ ] Test performance tracking
- [ ] Test director selection
- [ ] Run backtest comparison
- [ ] Document performance improvements

**Estimated Time:** 10-14 days (2 weeks)
**Effort Level:** High
