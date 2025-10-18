"""
Backtesting configuration settings.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class BacktestConfig:
    """Configuration for backtesting parameters."""
    
    # Capital settings
    initial_cash: float = 100000.0
    
    # Trading costs
    commission: float = 0.001  # 0.1% commission per trade
    slippage: float = 0.0005   # 0.05% slippage
    
    # Position sizing strategy
    position_sizing: Literal["percentage", "fixed", "all_in"] = "percentage"
    position_size_value: float = 0.95  # 95% of portfolio for percentage, or fixed dollar amount
    
    # Risk management
    max_position_size: Optional[float] = None  # Maximum position size as % of portfolio
    stop_loss: Optional[float] = None          # Stop loss as % (e.g., 0.10 for 10%)
    take_profit: Optional[float] = None        # Take profit as % (e.g., 0.20 for 20%)
    
    # Learning settings
    enable_reflection: bool = True             # Enable agent learning during backtest
    reflection_on_close_only: bool = True      # Only reflect when positions close
    
    # Performance tracking
    benchmark_ticker: str = "SPY"              # Benchmark for comparison
    risk_free_rate: float = 0.02               # Annual risk-free rate for Sharpe ratio
    
    # Data settings
    data_cache: bool = True                    # Cache historical data
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be positive")
        
        if self.commission < 0:
            raise ValueError("commission must be non-negative")
            
        if self.position_sizing == "percentage":
            if not 0 < self.position_size_value <= 1:
                raise ValueError("position_size_value must be between 0 and 1 for percentage sizing")
        elif self.position_sizing == "fixed":
            if self.position_size_value <= 0:
                raise ValueError("position_size_value must be positive for fixed sizing")

