"""
Advanced backtesting example with custom configuration.

This example shows how to:
1. Use custom analyst combinations
2. Configure position sizing strategies
3. Access detailed trade information
4. Generate custom analysis from results
"""

from tradingagents.backtesting import BacktestEngine, BacktestConfig
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()


def analyze_trades(results):
    """Perform custom analysis on trade results."""
    if not results.trade_history:
        print("No trades to analyze")
        return
    
    # Convert to DataFrame for easier analysis
    trades_df = pd.DataFrame(results.trade_history)
    
    print("\n" + "="*60)
    print("Trade Analysis")
    print("="*60)
    
    # Monthly performance
    trades_df['entry_date'] = pd.to_datetime(trades_df['entry_date'])
    trades_df['month'] = trades_df['entry_date'].dt.to_period('M')
    monthly_returns = trades_df.groupby('month')['returns'].mean()
    
    print("\nMonthly Average Returns:")
    for month, return_val in monthly_returns.items():
        print(f"  {month}: {return_val:>8.2%}")
    
    # Longest winning/losing streaks
    trades_df['is_win'] = trades_df['returns'] > 0
    streaks = []
    current_streak = 1
    current_type = trades_df['is_win'].iloc[0]
    
    for i in range(1, len(trades_df)):
        if trades_df['is_win'].iloc[i] == current_type:
            current_streak += 1
        else:
            streaks.append((current_type, current_streak))
            current_streak = 1
            current_type = trades_df['is_win'].iloc[i]
    streaks.append((current_type, current_streak))
    
    win_streaks = [s[1] for s in streaks if s[0]]
    loss_streaks = [s[1] for s in streaks if not s[0]]
    
    print(f"\nLongest winning streak: {max(win_streaks) if win_streaks else 0} trades")
    print(f"Longest losing streak: {max(loss_streaks) if loss_streaks else 0} trades")
    
    # Average holding period
    trades_df['holding_days'] = (pd.to_datetime(trades_df['exit_date']) - 
                                  pd.to_datetime(trades_df['entry_date'])).dt.days
    avg_holding = trades_df['holding_days'].mean()
    print(f"\nAverage holding period: {avg_holding:.1f} days")
    
    # Best and worst trades
    print("\nBest Trade:")
    best_trade = trades_df.loc[trades_df['returns'].idxmax()]
    print(f"  Entry: {best_trade['entry_date']} @ ${best_trade['entry_price']:.2f}")
    print(f"  Exit: {best_trade['exit_date']} @ ${best_trade['exit_price']:.2f}")
    print(f"  Return: {best_trade['returns']:.2%}")
    
    print("\nWorst Trade:")
    worst_trade = trades_df.loc[trades_df['returns'].idxmin()]
    print(f"  Entry: {worst_trade['entry_date']} @ ${worst_trade['entry_price']:.2f}")
    print(f"  Exit: {worst_trade['exit_date']} @ ${worst_trade['exit_price']:.2f}")
    print(f"  Return: {worst_trade['returns']:.2%}")


def main():
    """Run advanced backtest with custom configuration."""
    
    # Configuration
    ticker = "NVDA"  # High volatility stock
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    initial_cash = 50000.0
    
    print("="*60)
    print("Advanced Backtest Example - TradingAgents")
    print("="*60)
    print(f"Ticker: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Strategy: Technical + News focused with tight risk management")
    print("="*60 + "\n")
    
    # Advanced configuration
    config = BacktestConfig(
        initial_cash=initial_cash,
        commission=0.002,  # 0.2% commission (more realistic for retail)
        slippage=0.001,  # 0.1% slippage
        position_sizing="percentage",
        position_size_value=0.80,  # Conservative 80% allocation
        max_position_size=0.90,  # Hard cap at 90%
        stop_loss=0.08,  # Tight 8% stop loss
        take_profit=0.15,  # Conservative 15% take profit
        enable_reflection=True,
        reflection_on_close_only=True,
    )
    
    # Custom TradingAgents configuration
    ta_config = DEFAULT_CONFIG.copy()
    ta_config["quick_think_llm"] = "gpt-4o-mini"
    ta_config["deep_think_llm"] = "gpt-4o-mini"
    ta_config["max_debate_rounds"] = 3  # Thorough analysis
    ta_config["max_risk_discuss_rounds"] = 3
    
    # Use only technical and news analysts (focused strategy)
    selected_analysts = ["market", "news"]
    
    print(f"Analyst Configuration: {', '.join(selected_analysts)}")
    print(f"Debate Rounds: {ta_config['max_debate_rounds']}")
    print(f"Position Sizing: {config.position_sizing} ({config.position_size_value:.0%})")
    print(f"Risk Management: {config.stop_loss:.0%} SL / {config.take_profit:.0%} TP")
    print()
    
    # Create and run backtest
    engine = BacktestEngine(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        initial_cash=initial_cash,
        config=config,
        ta_config=ta_config,
        selected_analysts=selected_analysts,
        debug=False,
    )
    
    results = engine.run()
    
    # Print standard metrics
    results.print_metrics()
    
    # Perform custom analysis
    analyze_trades(results)
    
    # Access specific data points
    print("\n" + "="*60)
    print("Additional Insights")
    print("="*60)
    
    # Calculate consistency (% of months with positive returns)
    monthly_returns = results.get_monthly_returns()
    if len(monthly_returns) > 0:
        positive_months = (monthly_returns > 0).sum()
        consistency = positive_months / len(monthly_returns)
        print(f"\nConsistency: {consistency:.1%} of months were profitable")
        print(f"  ({positive_months} out of {len(monthly_returns)} months)")
    
    # Risk-adjusted return
    if results.max_drawdown_pct > 0:
        rar = results.total_return / results.max_drawdown_pct
        print(f"\nRisk-Adjusted Return: {rar:.2f}")
        print(f"  (Total Return / Max Drawdown)")
    
    # Save everything
    output_dir = f"results/backtests/{ticker}_advanced_example"
    engine.save_results(output_dir)
    engine.plot(output_dir + "/plots")
    
    print(f"\n✓ Complete results saved to {output_dir}")
    
    # Export trades for external analysis
    trades_csv = f"{output_dir}/detailed_trades.csv"
    results.to_csv(trades_csv)
    print(f"✓ Trade details exported to {trades_csv}")


if __name__ == "__main__":
    main()

