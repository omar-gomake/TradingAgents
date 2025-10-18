"""
Visualization tools for backtesting results.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import Optional
from pathlib import Path


class BacktestVisualizer:
    """Creates visualizations for backtest results."""
    
    def __init__(self, results):
        """
        Initialize visualizer with backtest results.
        
        Args:
            results: BacktestResults instance
        """
        self.results = results
        
    def plot_equity_curve(
        self,
        save_path: Optional[str] = None,
        show: bool = True,
        figsize: tuple = (14, 8)
    ):
        """
        Plot equity curve with benchmark comparison.
        
        Args:
            save_path: Path to save the figure
            show: Whether to display the plot
            figsize: Figure size (width, height)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]})
        
        # Plot portfolio value
        dates = pd.to_datetime(self.results.portfolio_values.index)
        values = self.results.portfolio_values.values
        
        ax1.plot(dates, values, label='Portfolio', linewidth=2, color='#2E86AB')
        ax1.axhline(y=self.results.initial_cash, color='gray', linestyle='--', alpha=0.5, label='Initial Capital')
        
        # Plot benchmark if available
        if self.results.benchmark_values is not None:
            benchmark_norm = (self.results.benchmark_values / self.results.benchmark_values.iloc[0]) * self.results.initial_cash
            ax1.plot(dates, benchmark_norm.values, label='Benchmark (SPY)', linewidth=2, color='#A23B72', alpha=0.7)
        
        ax1.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax1.set_title(f'{self.results.ticker} Backtest: {self.results.start_date} to {self.results.end_date}', 
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        # Plot drawdown
        daily_returns = self.results.portfolio_values.pct_change().dropna()
        cumulative = (1 + daily_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        ax2.fill_between(dates[1:], drawdown.values * 100, 0, color='#D62828', alpha=0.5)
        ax2.set_ylabel('Drawdown (%)', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_trades(
        self,
        price_data: pd.Series,
        save_path: Optional[str] = None,
        show: bool = True,
        figsize: tuple = (14, 6)
    ):
        """
        Plot price chart with trade markers.
        
        Args:
            price_data: Series with price data (index should be dates)
            save_path: Path to save the figure
            show: Whether to display the plot
            figsize: Figure size (width, height)
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot price
        dates = pd.to_datetime(price_data.index)
        ax.plot(dates, price_data.values, label='Price', linewidth=1.5, color='#264653', alpha=0.8)
        
        # Mark trades
        for trade in self.results.trade_history:
            entry_date = pd.to_datetime(trade['entry_date'])
            exit_date = pd.to_datetime(trade['exit_date'])
            entry_price = trade['entry_price']
            exit_price = trade['exit_price']
            is_profitable = trade['returns'] > 0
            
            # Entry marker
            ax.scatter(entry_date, entry_price, marker='^', s=100, 
                      color='green', edgecolors='black', linewidth=1, zorder=5, label='Buy' if trade == self.results.trade_history[0] else '')
            
            # Exit marker
            color = 'darkgreen' if is_profitable else 'darkred'
            ax.scatter(exit_date, exit_price, marker='v', s=100,
                      color=color, edgecolors='black', linewidth=1, zorder=5, 
                      label='Profitable Sell' if is_profitable and trade == self.results.trade_history[0] else 'Loss Sell' if not is_profitable and trade == self.results.trade_history[0] else '')
            
            # Connect entry and exit
            ax.plot([entry_date, exit_date], [entry_price, exit_price], 
                   linestyle='--', linewidth=1, color=color, alpha=0.5)
        
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_title(f'{self.results.ticker} Price Chart with Trades', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_monthly_returns(
        self,
        save_path: Optional[str] = None,
        show: bool = True,
        figsize: tuple = (14, 6)
    ):
        """
        Plot monthly returns heatmap.
        
        Args:
            save_path: Path to save the figure
            show: Whether to display the plot
            figsize: Figure size (width, height)
        """
        monthly_returns = self.results.get_monthly_returns()
        
        if len(monthly_returns) == 0:
            print("No monthly returns to plot")
            return
        
        # Reshape to year x month matrix
        monthly_returns.index = pd.to_datetime(monthly_returns.index)
        years = monthly_returns.index.year.unique()
        months = range(1, 13)
        
        data = np.zeros((len(years), 12))
        data[:] = np.nan
        
        for i, year in enumerate(years):
            year_data = monthly_returns[monthly_returns.index.year == year]
            for month_val in year_data.index.month:
                month_return = year_data[year_data.index.month == month_val].iloc[0]
                data[i, month_val - 1] = month_return * 100
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=-10, vmax=10)
        
        # Set ticks
        ax.set_xticks(np.arange(12))
        ax.set_yticks(np.arange(len(years)))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_yticklabels(years)
        
        # Add text annotations
        for i in range(len(years)):
            for j in range(12):
                if not np.isnan(data[i, j]):
                    text = ax.text(j, i, f'{data[i, j]:.1f}%',
                                 ha="center", va="center", color="black", fontsize=9)
        
        ax.set_title('Monthly Returns (%)', fontsize=14, fontweight='bold')
        plt.colorbar(im, ax=ax, label='Return (%)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_metrics_dashboard(
        self,
        save_path: Optional[str] = None,
        show: bool = True,
        figsize: tuple = (16, 10)
    ):
        """
        Create a comprehensive dashboard with multiple metrics.
        
        Args:
            save_path: Path to save the figure
            show: Whether to display the plot
            figsize: Figure size (width, height)
        """
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Equity curve
        ax1 = fig.add_subplot(gs[0, :])
        dates = pd.to_datetime(self.results.portfolio_values.index)
        ax1.plot(dates, self.results.portfolio_values.values, linewidth=2, color='#2E86AB')
        ax1.set_title('Portfolio Equity Curve', fontweight='bold')
        ax1.set_ylabel('Value ($)')
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        # 2. Drawdown
        ax2 = fig.add_subplot(gs[1, :])
        daily_returns = self.results.portfolio_values.pct_change().dropna()
        cumulative = (1 + daily_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        ax2.fill_between(dates[1:], drawdown.values * 100, 0, color='#D62828', alpha=0.5)
        ax2.set_title('Drawdown', fontweight='bold')
        ax2.set_ylabel('Drawdown (%)')
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        # 3. Key metrics table
        ax3 = fig.add_subplot(gs[2, 0])
        ax3.axis('off')
        metrics_text = f"""
        Total Return: {self.results.total_return:.2%}
        Annual Return: {self.results.annualized_return:.2%}
        Sharpe Ratio: {self.results.sharpe_ratio:.2f}
        Max Drawdown: {self.results.max_drawdown_pct:.2%}
        """
        ax3.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center', family='monospace')
        ax3.set_title('Performance Metrics', fontweight='bold')
        
        # 4. Trade statistics
        ax4 = fig.add_subplot(gs[2, 1])
        ax4.axis('off')
        trade_text = f"""
        Total Trades: {self.results.num_trades}
        Win Rate: {self.results.win_rate:.2%}
        Avg Win: {self.results.avg_win:.2%}
        Avg Loss: {self.results.avg_loss:.2%}
        """
        ax4.text(0.1, 0.5, trade_text, fontsize=11, verticalalignment='center', family='monospace')
        ax4.set_title('Trade Statistics', fontweight='bold')
        
        # 5. Returns distribution
        ax5 = fig.add_subplot(gs[2, 2])
        if self.results.trade_history:
            returns = [t['returns'] * 100 for t in self.results.trade_history]
            ax5.hist(returns, bins=20, color='#2A9D8F', alpha=0.7, edgecolor='black')
            ax5.axvline(x=0, color='red', linestyle='--', linewidth=2)
            ax5.set_xlabel('Return (%)')
            ax5.set_ylabel('Frequency')
            ax5.set_title('Trade Returns Distribution', fontweight='bold')
            ax5.grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.results.ticker} Backtest Dashboard', fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def save_all_plots(self, output_dir: str, price_data: Optional[pd.Series] = None):
        """
        Generate and save all plots to a directory.
        
        Args:
            output_dir: Directory to save plots
            price_data: Optional price data for trade plot
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating visualizations in {output_dir}...")
        
        # Equity curve
        self.plot_equity_curve(
            save_path=str(output_path / 'equity_curve.png'),
            show=False
        )
        
        # Trades plot (if price data available)
        if price_data is not None:
            self.plot_trades(
                price_data=price_data,
                save_path=str(output_path / 'trades.png'),
                show=False
            )
        
        # Monthly returns
        self.plot_monthly_returns(
            save_path=str(output_path / 'monthly_returns.png'),
            show=False
        )
        
        # Dashboard
        self.plot_metrics_dashboard(
            save_path=str(output_path / 'dashboard.png'),
            show=False
        )
        
        print("All visualizations saved successfully!")

