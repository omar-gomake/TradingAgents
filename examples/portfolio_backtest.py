"""
Portfolio backtesting example for TradingAgents.

This example demonstrates how to run a backtest across multiple stocks
with advanced configuration including stop-loss and take-profit.
"""

from tradingagents.backtesting import MultiTickerBacktestEngine, BacktestConfig
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Run a portfolio backtest example."""
    
    # Configuration
    tickers = ["AAPL", "GOOGL", "MSFT"]  # Tech portfolio
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    total_capital = 300000.0  # $300k total
    capital_per_ticker = 100000.0  # $100k per stock
    
    print("="*60)
    print("Portfolio Backtest Example - TradingAgents")
    print("="*60)
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Total Capital: ${total_capital:,.2f}")
    print(f"Capital per ticker: ${capital_per_ticker:,.2f}")
    print("="*60 + "\n")
    
    # Create advanced backtest configuration
    config = BacktestConfig(
        initial_cash=capital_per_ticker,  # Per ticker
        commission=0.001,  # 0.1% commission
        slippage=0.0005,  # 0.05% slippage
        position_sizing="percentage",
        position_size_value=0.90,  # Use 90% of capital
        stop_loss=0.10,  # 10% stop loss
        take_profit=0.20,  # 20% take profit
        enable_reflection=True,  # Enable agent learning
        reflection_on_close_only=True,
    )
    
    # Configure TradingAgents with better models
    ta_config = DEFAULT_CONFIG.copy()
    ta_config["quick_think_llm"] = "gpt-4o-mini"
    ta_config["deep_think_llm"] = "gpt-4o-mini"
    ta_config["max_debate_rounds"] = 2  # More thorough analysis
    ta_config["max_risk_discuss_rounds"] = 2
    
    # Create multi-ticker backtest engine
    engine = MultiTickerBacktestEngine(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        initial_cash=total_capital,
        cash_per_ticker=capital_per_ticker,
        config=config,
        ta_config=ta_config,
        selected_analysts=["market", "social", "news", "fundamentals"],  # All analysts
        debug=False,
    )
    
    # Run the backtest
    results = engine.run()
    
    # Print individual results
    print("\n" + "="*60)
    print("Individual Ticker Results")
    print("="*60)
    
    for ticker, result in results.items():
        print(f"\n{ticker}:")
        print(f"  Return: {result.total_return:>8.2%}")
        print(f"  Sharpe: {result.sharpe_ratio:>8.2f}")
        print(f"  Max DD: {result.max_drawdown_pct:>8.2%}")
        print(f"  Trades: {result.num_trades:>8}")
        print(f"  Win Rate: {result.win_rate:>8.2%}")
    
    # Calculate portfolio metrics
    total_final_value = sum(r.final_value for r in results.values())
    portfolio_return = (total_final_value - total_capital) / total_capital
    
    print("\n" + "="*60)
    print("Portfolio Summary")
    print("="*60)
    print(f"Initial Capital: ${total_capital:>15,.2f}")
    print(f"Final Value:     ${total_final_value:>15,.2f}")
    print(f"Total Return:    {portfolio_return:>15.2%}")
    print("="*60)
    
    # Save all results
    output_dir = "results/backtests/portfolio_example"
    engine.save_all_results(output_dir)
    
    print(f"\n✓ Results saved to {output_dir}")
    print(f"✓ Check {output_dir}/<ticker>/plots/ for individual visualizations")
    
    # Show best and worst performers
    sorted_results = sorted(results.items(), key=lambda x: x[1].total_return, reverse=True)
    best_ticker, best_result = sorted_results[0]
    worst_ticker, worst_result = sorted_results[-1]
    
    print("\n📈 Best Performer:")
    print(f"   {best_ticker}: {best_result.total_return:.2%} return")
    print("\n📉 Worst Performer:")
    print(f"   {worst_ticker}: {worst_result.total_return:.2%} return")


if __name__ == "__main__":
    main()

