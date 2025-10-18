"""
Quick Backtest Test - Minimal Configuration
Runs a very short backtest with reduced LLM calls to validate the system
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tradingagents.backtesting import BacktestEngine, BacktestConfig
from tradingagents.fast_backtest_config import FAST_BACKTEST_CONFIG

def main():
    print("=" * 80)
    print("QUICK BACKTEST TEST")
    print("=" * 80)
    print("\nConfiguration:")
    print(f"  Ticker: AAPL")
    print(f"  Period: Jan 25-31, 2024 (~5 trading days)")
    print(f"  Capital: $10,000")
    print(f"  Analysts: Market only")
    print(f"  LLM: gpt-4o-mini (fast)")
    print(f"  Debates: Skipped (max_debate_rounds=0)")
    print(f"  Reflection: Enabled")
    print("\n" + "=" * 80)
    
    # Minimal backtest configuration
    bt_config = BacktestConfig(
        initial_cash=10000,
        commission=0.001,  # 0.1% commission
        position_sizing="percentage",
        position_size_value=0.95,  # Use 95% of capital
        enable_reflection=True,
        reflection_on_close_only=True,
    )
    
    # Use fast config
    ta_config = FAST_BACKTEST_CONFIG.copy()
    
    try:
        # Create and run engine
        engine = BacktestEngine(
            ticker="AAPL",
            start_date="2024-01-25",
            end_date="2024-01-31",
            config=bt_config,
            ta_config=ta_config,
            selected_analysts=["market"],  # Only market analyst
            debug=False,  # Minimal output
        )
        
        print("\n🚀 Starting backtest...\n")
        results = engine.run()
        
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        results.print_metrics()
        
        # Save results
        output_dir = "results/backtests/quick_test"
        engine.save_results(output_dir)
        print(f"\n✅ Results saved to: {output_dir}")
        
        # Try to generate plots
        try:
            engine.plot(f"{output_dir}/plots")
            print(f"✅ Plots saved to: {output_dir}/plots")
        except Exception as e:
            print(f"⚠️  Could not generate plots: {e}")
        
        print("\n" + "=" * 80)
        print("✨ Backtest completed successfully!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Backtest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

