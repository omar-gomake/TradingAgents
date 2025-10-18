"""
One-Day Backtest Test - Fastest Validation
Tests the system with a single trading day to verify everything works
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tradingagents.backtesting import BacktestEngine, BacktestConfig
from tradingagents.fast_backtest_config import FAST_BACKTEST_CONFIG

def main():
    print("\n" + "=" * 80)
    print("QUICK 3-DAY BACKTEST TEST (Fastest Validation)")
    print("=" * 80)
    print("\n✨ This will complete in ~5-10 minutes")
    print("\nConfiguration:")
    print("  Ticker: AAPL")
    print("  Period: Jan 29-31, 2024 (3 trading days)")
    print("  Capital: $10,000")
    print("  Analysts: Market only")
    print("  LLM: gpt-4o-mini")
    print("  Debates: Disabled (max_debate_rounds=0)")
    print("\n" + "=" * 80 + "\n")
    
    # Minimal configuration
    bt_config = BacktestConfig(
        initial_cash=10000,
        commission=0.001,
        position_sizing="percentage",
        position_size_value=0.95,
        enable_reflection=False,  # Disable for quick test
    )
    
    ta_config = FAST_BACKTEST_CONFIG.copy()
    
    try:
        engine = BacktestEngine(
            ticker="AAPL",
            start_date="2024-01-29",
            end_date="2024-01-31",
            config=bt_config,
            ta_config=ta_config,
            selected_analysts=["market"],
            debug=False,  # Minimal output for speed
        )
        
        print("🚀 Running backtest...\n")
        results = engine.run()
        
        print("\n" + "=" * 80)
        print("✅ BACKTEST COMPLETED!")
        print("=" * 80)
        
        # Show key metrics
        print(f"\nFinal Portfolio Value: ${results.final_value:,.2f}")
        print(f"Total Return: {results.total_return:.2%}")
        print(f"Total Trades: {results.num_trades}")
        
        if results.num_trades > 0:
            print(f"Win Rate: {results.win_rate:.1%}")
        
        # Save
        output_dir = "results/backtests/quick_3day_test"
        engine.save_results(output_dir)
        print(f"\n📁 Results saved to: {output_dir}")
        
        print("\n" + "=" * 80)
        print("🎉 Success! The backtesting system is working perfectly!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Try 5-day test: python examples/quick_test.py")
        print("  2. Try full month: python examples/simple_backtest.py")
        print("  3. Use CLI for custom backtests: python -m cli.main backtest run")
        print("\n💡 Tip: Edit tradingagents/default_config.py to adjust LLM models & settings")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

