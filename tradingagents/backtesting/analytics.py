"""
Performance analytics and metrics calculation for backtesting.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class BacktestResults:
    """
    Container for backtest results with performance analytics.
    """
    
    def __init__(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        initial_cash: float,
        final_value: float,
        trade_history: List[Dict],
        decisions: List[Dict],
        agent_states: List[Dict],
        portfolio_values: pd.Series,
        benchmark_values: Optional[pd.Series] = None,
    ):
        """Initialize backtest results."""
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.final_value = final_value
        self.trade_history = trade_history
        self.decisions = decisions
        self.agent_states = agent_states
        self.portfolio_values = portfolio_values
        self.benchmark_values = benchmark_values
        
        # Calculate metrics
        self._calculate_metrics()
    
    def _calculate_metrics(self):
        """Calculate all performance metrics."""
        # Basic returns
        self.total_return = (self.final_value - self.initial_cash) / self.initial_cash
        self.total_profit = self.final_value - self.initial_cash
        
        # Trade statistics
        if self.trade_history:
            returns = [t['returns'] for t in self.trade_history]
            profits = [t['profit'] for t in self.trade_history]
            
            self.num_trades = len(self.trade_history)
            self.winning_trades = sum(1 for r in returns if r > 0)
            self.losing_trades = sum(1 for r in returns if r < 0)
            self.win_rate = self.winning_trades / self.num_trades if self.num_trades > 0 else 0
            
            self.avg_return = np.mean(returns) if returns else 0
            self.avg_profit = np.mean(profits) if profits else 0
            
            winning_returns = [r for r in returns if r > 0]
            losing_returns = [r for r in returns if r < 0]
            
            self.avg_win = np.mean(winning_returns) if winning_returns else 0
            self.avg_loss = np.mean(losing_returns) if losing_returns else 0
            
            # Profit factor
            total_wins = sum(p for p in profits if p > 0)
            total_losses = abs(sum(p for p in profits if p < 0))
            self.profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            # Best and worst trades
            self.best_trade = max(returns) if returns else 0
            self.worst_trade = min(returns) if returns else 0
        else:
            self.num_trades = 0
            self.winning_trades = 0
            self.losing_trades = 0
            self.win_rate = 0
            self.avg_return = 0
            self.avg_profit = 0
            self.avg_win = 0
            self.avg_loss = 0
            self.profit_factor = 0
            self.best_trade = 0
            self.worst_trade = 0
        
        # Portfolio-based metrics
        if len(self.portfolio_values) > 1:
            # Calculate daily returns
            daily_returns = self.portfolio_values.pct_change().dropna()
            
            # Annualized return
            num_days = len(self.portfolio_values)
            years = num_days / 252  # Approximate trading days per year
            self.annualized_return = (1 + self.total_return) ** (1 / years) - 1 if years > 0 else 0
            
            # Volatility (annualized)
            self.volatility = daily_returns.std() * np.sqrt(252) if len(daily_returns) > 0 else 0
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            excess_return = self.annualized_return - risk_free_rate
            self.sharpe_ratio = excess_return / self.volatility if self.volatility > 0 else 0
            
            # Sortino ratio (using downside deviation)
            downside_returns = daily_returns[daily_returns < 0]
            downside_std = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
            self.sortino_ratio = excess_return / downside_std if downside_std > 0 else 0
            
            # Maximum drawdown
            cumulative_returns = (1 + daily_returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            self.max_drawdown = drawdown.min()
            self.max_drawdown_pct = abs(self.max_drawdown)
            
            # Calmar ratio (annualized return / max drawdown)
            self.calmar_ratio = self.annualized_return / self.max_drawdown_pct if self.max_drawdown_pct > 0 else 0
            
        else:
            self.annualized_return = 0
            self.volatility = 0
            self.sharpe_ratio = 0
            self.sortino_ratio = 0
            self.max_drawdown = 0
            self.max_drawdown_pct = 0
            self.calmar_ratio = 0
        
        # Benchmark comparison
        if self.benchmark_values is not None and len(self.benchmark_values) > 1:
            benchmark_return = (self.benchmark_values.iloc[-1] - self.benchmark_values.iloc[0]) / self.benchmark_values.iloc[0]
            self.benchmark_total_return = benchmark_return
            self.excess_return = self.total_return - benchmark_return
            self.alpha = self.annualized_return - benchmark_return
        else:
            self.benchmark_total_return = 0
            self.excess_return = 0
            self.alpha = 0
    
    def print_metrics(self):
        """Print formatted performance metrics."""
        print("\n" + "="*60)
        print(f"BACKTEST RESULTS: {self.ticker}")
        print("="*60)
        print(f"Period: {self.start_date} to {self.end_date}")
        print(f"\n{'RETURNS':-^60}")
        print(f"Initial Capital:        ${self.initial_cash:>15,.2f}")
        print(f"Final Value:            ${self.final_value:>15,.2f}")
        print(f"Total Profit:           ${self.total_profit:>15,.2f}")
        print(f"Total Return:           {self.total_return:>15.2%}")
        print(f"Annualized Return:      {self.annualized_return:>15.2%}")
        
        if self.benchmark_values is not None:
            print(f"\n{'BENCHMARK COMPARISON':-^60}")
            print(f"Benchmark Return:       {self.benchmark_total_return:>15.2%}")
            print(f"Excess Return:          {self.excess_return:>15.2%}")
            print(f"Alpha:                  {self.alpha:>15.2%}")
        
        print(f"\n{'RISK METRICS':-^60}")
        print(f"Volatility (Annual):    {self.volatility:>15.2%}")
        print(f"Sharpe Ratio:           {self.sharpe_ratio:>15.3f}")
        print(f"Sortino Ratio:          {self.sortino_ratio:>15.3f}")
        print(f"Max Drawdown:           {self.max_drawdown_pct:>15.2%}")
        print(f"Calmar Ratio:           {self.calmar_ratio:>15.3f}")
        
        print(f"\n{'TRADE STATISTICS':-^60}")
        print(f"Total Trades:           {self.num_trades:>15}")
        print(f"Winning Trades:         {self.winning_trades:>15}")
        print(f"Losing Trades:          {self.losing_trades:>15}")
        print(f"Win Rate:               {self.win_rate:>15.2%}")
        print(f"Average Return:         {self.avg_return:>15.2%}")
        print(f"Average Win:            {self.avg_win:>15.2%}")
        print(f"Average Loss:           {self.avg_loss:>15.2%}")
        print(f"Profit Factor:          {self.profit_factor:>15.2f}")
        print(f"Best Trade:             {self.best_trade:>15.2%}")
        print(f"Worst Trade:            {self.worst_trade:>15.2%}")
        print("="*60 + "\n")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary."""
        def _safe_value(v):
            """Convert value to JSON-serializable format."""
            if isinstance(v, (pd.Series, pd.DataFrame)):
                return None  # Skip Series/DataFrame objects
            elif isinstance(v, (np.integer, np.floating)):
                return float(v)
            elif isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
                return None
            return v
        
        return {
            'ticker': self.ticker,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_cash': _safe_value(self.initial_cash),
            'final_value': _safe_value(self.final_value),
            'total_return': _safe_value(self.total_return),
            'total_profit': _safe_value(self.total_profit),
            'annualized_return': _safe_value(self.annualized_return),
            'volatility': _safe_value(self.volatility),
            'sharpe_ratio': _safe_value(self.sharpe_ratio),
            'sortino_ratio': _safe_value(self.sortino_ratio),
            'max_drawdown': _safe_value(self.max_drawdown_pct),
            'calmar_ratio': _safe_value(self.calmar_ratio),
            'num_trades': _safe_value(self.num_trades),
            'winning_trades': _safe_value(self.winning_trades),
            'losing_trades': _safe_value(self.losing_trades),
            'win_rate': _safe_value(self.win_rate),
            'avg_return': _safe_value(self.avg_return),
            'avg_win': _safe_value(self.avg_win),
            'avg_loss': _safe_value(self.avg_loss),
            'profit_factor': _safe_value(self.profit_factor),
            'best_trade': _safe_value(self.best_trade),
            'worst_trade': _safe_value(self.worst_trade),
            'benchmark_return': _safe_value(self.benchmark_total_return),
            'excess_return': _safe_value(self.excess_return),
            'alpha': _safe_value(self.alpha),
        }
    
    def to_json(self, filepath: str):
        """Save results to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def to_csv(self, filepath: str):
        """Save trade history to CSV file."""
        if self.trade_history:
            df = pd.DataFrame(self.trade_history)
            df.to_csv(filepath, index=False)
    
    def get_monthly_returns(self) -> pd.Series:
        """Calculate monthly returns."""
        daily_returns = self.portfolio_values.pct_change().dropna()
        
        # Convert index to datetime if needed
        if not isinstance(daily_returns.index, pd.DatetimeIndex):
            daily_returns.index = pd.to_datetime(daily_returns.index)
        
        monthly_returns = daily_returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
        return monthly_returns
    
    def get_yearly_returns(self) -> pd.Series:
        """Calculate yearly returns."""
        daily_returns = self.portfolio_values.pct_change().dropna()
        
        # Convert index to datetime if needed
        if not isinstance(daily_returns.index, pd.DatetimeIndex):
            daily_returns.index = pd.to_datetime(daily_returns.index)
        
        yearly_returns = daily_returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
        return yearly_returns

