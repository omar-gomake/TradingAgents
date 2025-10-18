"""
TradingAgents Backtesting Module

Comprehensive backtesting framework for TradingAgents strategies using backtrader.
"""

from .engine import BacktestEngine, MultiTickerBacktestEngine
from .analytics import BacktestResults
from .config import BacktestConfig
from .visualization import BacktestVisualizer

__all__ = ["BacktestEngine", "MultiTickerBacktestEngine", "BacktestResults", "BacktestConfig", "BacktestVisualizer"]

