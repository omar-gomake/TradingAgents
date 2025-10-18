"""
Simple backtesting example for TradingAgents.

This example demonstrates how to run a basic backtest for a single stock
with default configuration.
"""

from tradingagents.backtesting import BacktestEngine, BacktestConfig
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Run a simple backtest example."""
    
    # Configuration
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    initial_cash = 100000.0
    
    print("="*60)
    print("Simple Backtest Example - TradingAgents")
    print("="*60)
    print(f"Ticker: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_cash:,.2f}")
    print("="*60 + "\n")
    
    # Create backtest configuration
    config = BacktestConfig(
        initial_cash=initial_cash,
        commission=0.001,  # 0.1% commission
        position_sizing="percentage",
        position_size_value=0.95,  # Use 95% of portfolio
        enable_reflection=True,  # Enable agent learning
    )
    
    # Configure TradingAgents
    ta_config = DEFAULT_CONFIG.copy()
    ta_config["quick_think_llm"] = "gpt-4o-mini"
    ta_config["deep_think_llm"] = "gpt-4o-mini"
    ta_config["max_debate_rounds"] = 1  # Keep it simple for faster execution
    
    # Create backtest engine
    engine = BacktestEngine(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        initial_cash=initial_cash,
        config=config,
        ta_config=ta_config,
        selected_analysts=["market", "news", "fundamentals"],  # Use 3 analysts
        debug=False,
    )
    
    # Run the backtest
    results = engine.run()
    
    # Print performance metrics
    results.print_metrics()
    
    # Save results to files
    output_dir = f"results/backtests/{ticker}_simple_example"
    engine.save_results(output_dir)
    
    # Generate and save visualizations
    engine.plot(output_dir + "/plots")
    
    print(f"\n✓ Results saved to {output_dir}")
    print(f"✓ Check {output_dir}/plots/ for visualizations")
    
    # Access specific metrics
    print("\nKey Metrics:")
    print(f"  Total Return: {results.total_return:.2%}")
    print(f"  Sharpe Ratio: {results.sharpe_ratio:.2f}")
    print(f"  Max Drawdown: {results.max_drawdown_pct:.2%}")
    print(f"  Win Rate: {results.win_rate:.2%}")
    print(f"  Number of Trades: {results.num_trades}")


if __name__ == "__main__":
    main()

