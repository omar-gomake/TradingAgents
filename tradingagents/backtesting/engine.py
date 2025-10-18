"""
Main backtesting engine for TradingAgents.
"""

import backtrader as bt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

from .strategy import TradingAgentsStrategy
from .config import BacktestConfig
from .analytics import BacktestResults
from .visualization import BacktestVisualizer
from .utils import parse_date, create_data_feed

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


class BacktestEngine:
    """
    Main engine for running backtests with TradingAgents.
    """
    
    def __init__(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        initial_cash: float = 100000.0,
        config: Optional[BacktestConfig] = None,
        ta_config: Optional[Dict[str, Any]] = None,
        selected_analysts: List[str] = ["market", "social", "news", "fundamentals"],
        debug: bool = False,
    ):
        """
        Initialize the backtest engine.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            initial_cash: Initial capital for backtesting
            config: BacktestConfig instance (if None, uses defaults)
            ta_config: TradingAgents configuration dict (if None, uses DEFAULT_CONFIG)
            selected_analysts: List of analysts to use
            debug: Whether to run in debug mode
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.debug = debug
        self.selected_analysts = selected_analysts
        
        # Set up configs
        self.config = config or BacktestConfig(initial_cash=initial_cash)
        self.ta_config = ta_config or DEFAULT_CONFIG.copy()
        
        # Initialize TradingAgents
        self.ta_graph = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            debug=False,  # Disable debug to avoid cluttering output
            config=self.ta_config
        )
        
        # Backtrader cerebro instance
        self.cerebro = None
        
        # Results
        self.results = None
        self.strategy_instance = None
        
    def setup_cerebro(self):
        """Set up the backtrader Cerebro instance."""
        self.cerebro = bt.Cerebro()
        
        # Add data feed
        print(f"Loading data for {self.ticker}...")
        data = create_data_feed(self.ticker, self.start_date, self.end_date)
        self.cerebro.adddata(data, name=self.ticker)
        
        # Add strategy with parameters
        self.cerebro.addstrategy(
            TradingAgentsStrategy,
            trading_agents_graph=self.ta_graph,
            config=self.config,
            ticker=self.ticker,
            verbose=self.debug,
        )
        
        # Set initial cash
        self.cerebro.broker.setcash(self.initial_cash)
        
        # Set commission
        self.cerebro.broker.setcommission(commission=self.config.commission)
        
        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='time_return')
        
        print(f"Cerebro setup complete. Initial cash: ${self.initial_cash:,.2f}")
    
    def run(self) -> BacktestResults:
        """
        Run the backtest.
        
        Returns:
            BacktestResults instance with performance metrics
        """
        if self.cerebro is None:
            self.setup_cerebro()
        
        print(f"\nStarting backtest for {self.ticker}")
        print(f"Period: {self.start_date} to {self.end_date}")
        print(f"Analysts: {', '.join(self.selected_analysts)}")
        print("-" * 60)
        
        # Run the backtest
        starting_value = self.cerebro.broker.getvalue()
        print(f"Starting Portfolio Value: ${starting_value:,.2f}")
        
        strategies = self.cerebro.run()
        self.strategy_instance = strategies[0]
        
        ending_value = self.cerebro.broker.getvalue()
        print(f"Ending Portfolio Value: ${ending_value:,.2f}")
        print(f"Total Return: {((ending_value - starting_value) / starting_value):.2%}")
        print("-" * 60)
        
        # Extract portfolio values over time
        portfolio_values = self._extract_portfolio_values()
        
        # Get benchmark data
        benchmark_values = self._get_benchmark_data()
        
        # Create BacktestResults
        self.results = BacktestResults(
            ticker=self.ticker,
            start_date=self.start_date,
            end_date=self.end_date,
            initial_cash=self.initial_cash,
            final_value=ending_value,
            trade_history=self.strategy_instance.trade_history,
            decisions=self.strategy_instance.decisions,
            agent_states=self.strategy_instance.agent_states,
            portfolio_values=portfolio_values,
            benchmark_values=benchmark_values,
        )
        
        return self.results
    
    def _extract_portfolio_values(self) -> pd.Series:
        """Extract portfolio values over time from the strategy."""
        # Get dates and values from decisions
        dates = [d['date'] for d in self.strategy_instance.decisions]
        
        # We need to reconstruct portfolio values
        # Since backtrader doesn't easily expose historical portfolio values,
        # we'll use the cerebro's TimeReturn analyzer
        analyzer = self.strategy_instance.analyzers.time_return
        returns_dict = analyzer.get_analysis()
        
        # Convert to pandas Series
        if returns_dict:
            dates_from_returns = list(returns_dict.keys())
            returns = list(returns_dict.values())
            
            # Calculate cumulative portfolio value
            portfolio_values = [self.initial_cash]
            for ret in returns:
                portfolio_values.append(portfolio_values[-1] * (1 + ret))
            
            series = pd.Series(portfolio_values[1:], index=dates_from_returns)
        else:
            # Fallback: use dates from decisions
            series = pd.Series([self.initial_cash] * len(dates), index=dates)
        
        return series
    
    def _get_benchmark_data(self) -> Optional[pd.Series]:
        """Get benchmark data for comparison."""
        try:
            benchmark_ticker = self.config.benchmark_ticker
            print(f"Loading benchmark data ({benchmark_ticker})...")
            
            # Add buffer for data
            start = parse_date(self.start_date)
            end = parse_date(self.end_date)
            
            benchmark_df = yf.download(
                benchmark_ticker,
                start=start,
                end=end,
                progress=False
            )
            
            if not benchmark_df.empty:
                # Return close prices
                return benchmark_df['Close']
            else:
                print(f"Warning: No benchmark data found for {benchmark_ticker}")
                return None
                
        except Exception as e:
            print(f"Warning: Could not load benchmark data: {e}")
            return None
    
    def plot(self, output_dir: Optional[str] = None):
        """
        Generate and display/save visualizations.
        
        Args:
            output_dir: Optional directory to save plots
        """
        if self.results is None:
            raise RuntimeError("Must run backtest before plotting. Call run() first.")
        
        visualizer = BacktestVisualizer(self.results)
        
        if output_dir:
            # Get price data for trades plot
            try:
                price_data = yf.download(
                    self.ticker,
                    start=self.start_date,
                    end=self.end_date,
                    progress=False
                )['Close']
            except:
                price_data = None
            
            visualizer.save_all_plots(output_dir, price_data)
        else:
            visualizer.plot_metrics_dashboard()
    
    def save_results(self, output_dir: str):
        """
        Save backtest results to files.
        
        Args:
            output_dir: Directory to save results
        """
        if self.results is None:
            raise RuntimeError("Must run backtest before saving. Call run() first.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\nSaving results to {output_dir}...")
        
        # Save metrics as JSON
        self.results.to_json(str(output_path / 'metrics.json'))
        
        # Save trade history as CSV
        self.results.to_csv(str(output_path / 'trades.csv'))
        
        # Save decisions as CSV
        if self.results.decisions:
            decisions_df = pd.DataFrame(self.results.decisions)
            decisions_df.to_csv(str(output_path / 'decisions.csv'), index=False)
        
        # Save portfolio values
        self.results.portfolio_values.to_csv(str(output_path / 'portfolio_values.csv'))
        
        print("Results saved successfully!")


class MultiTickerBacktestEngine:
    """
    Engine for backtesting multiple tickers (portfolio approach).
    """
    
    def __init__(
        self,
        tickers: List[str],
        start_date: str,
        end_date: str,
        initial_cash: float = 100000.0,
        cash_per_ticker: Optional[float] = None,
        config: Optional[BacktestConfig] = None,
        ta_config: Optional[Dict[str, Any]] = None,
        selected_analysts: List[str] = ["market", "social", "news", "fundamentals"],
        debug: bool = False,
    ):
        """
        Initialize multi-ticker backtest engine.
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            initial_cash: Total initial capital
            cash_per_ticker: Cash to allocate per ticker (if None, splits equally)
            config: BacktestConfig instance
            ta_config: TradingAgents configuration dict
            selected_analysts: List of analysts to use
            debug: Whether to run in debug mode
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.cash_per_ticker = cash_per_ticker or (initial_cash / len(tickers))
        self.config = config
        self.ta_config = ta_config
        self.selected_analysts = selected_analysts
        self.debug = debug
        
        self.engines = {}
        self.results = {}
    
    def run(self) -> Dict[str, BacktestResults]:
        """
        Run backtests for all tickers.
        
        Returns:
            Dictionary mapping ticker to BacktestResults
        """
        print(f"\nRunning multi-ticker backtest for {len(self.tickers)} tickers")
        print(f"Total capital: ${self.initial_cash:,.2f}")
        print(f"Capital per ticker: ${self.cash_per_ticker:,.2f}")
        print("=" * 60)
        
        for ticker in self.tickers:
            print(f"\n{'='*60}")
            print(f"Processing {ticker}")
            print("=" * 60)
            
            try:
                engine = BacktestEngine(
                    ticker=ticker,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    initial_cash=self.cash_per_ticker,
                    config=self.config,
                    ta_config=self.ta_config,
                    selected_analysts=self.selected_analysts,
                    debug=self.debug,
                )
                
                result = engine.run()
                self.engines[ticker] = engine
                self.results[ticker] = result
                
                print(f"\n{ticker} backtest completed successfully")
                
            except Exception as e:
                print(f"\nError processing {ticker}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'='*60}")
        print("Multi-ticker backtest complete")
        print("=" * 60)
        
        self._print_portfolio_summary()
        
        return self.results
    
    def _print_portfolio_summary(self):
        """Print summary of portfolio performance."""
        if not self.results:
            return
        
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        
        total_final_value = sum(r.final_value for r in self.results.values())
        total_return = (total_final_value - self.initial_cash) / self.initial_cash
        
        print(f"Initial Capital:      ${self.initial_cash:>15,.2f}")
        print(f"Final Value:          ${total_final_value:>15,.2f}")
        print(f"Total Return:         {total_return:>15.2%}")
        
        print(f"\n{'Individual Tickers':-^60}")
        for ticker, result in self.results.items():
            print(f"{ticker:>8}: Return: {result.total_return:>8.2%} | "
                  f"Sharpe: {result.sharpe_ratio:>6.2f} | "
                  f"Trades: {result.num_trades:>3}")
        
        print("="*60 + "\n")
    
    def save_all_results(self, output_dir: str):
        """Save results for all tickers."""
        output_path = Path(output_dir)
        
        for ticker, engine in self.engines.items():
            ticker_dir = output_path / ticker
            engine.save_results(str(ticker_dir))
            engine.plot(str(ticker_dir / 'plots'))
        
        # Save portfolio summary
        summary = {
            'tickers': self.tickers,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_cash': self.initial_cash,
            'total_final_value': sum(r.final_value for r in self.results.values()),
            'total_return': (sum(r.final_value for r in self.results.values()) - self.initial_cash) / self.initial_cash,
            'ticker_results': {
                ticker: result.to_dict() for ticker, result in self.results.items()
            }
        }
        
        import json
        with open(output_path / 'portfolio_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"All results saved to {output_dir}")

