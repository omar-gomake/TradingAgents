"""
Basic tests for backtesting functionality.

Run with: python tests/test_backtesting.py
"""

def test_imports():
    """Test that all backtesting modules can be imported."""
    print("Testing imports...")
    
    try:
        from tradingagents.backtesting import BacktestEngine, BacktestConfig, BacktestResults
        print("✓ Main classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main classes: {e}")
        return False
    
    try:
        from tradingagents.backtesting.strategy import TradingAgentsStrategy
        print("✓ Strategy class imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import strategy: {e}")
        return False
    
    try:
        from tradingagents.backtesting.analytics import BacktestResults
        print("✓ Analytics module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import analytics: {e}")
        return False
    
    try:
        from tradingagents.backtesting.visualization import BacktestVisualizer
        print("✓ Visualization module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import visualization: {e}")
        return False
    
    try:
        from tradingagents.backtesting.utils import parse_date, calculate_position_size
        print("✓ Utility functions imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    return True


def test_config():
    """Test BacktestConfig initialization."""
    print("\nTesting BacktestConfig...")
    
    try:
        from tradingagents.backtesting import BacktestConfig
        
        # Default config
        config = BacktestConfig()
        assert config.initial_cash == 100000.0
        assert config.commission == 0.001
        print("✓ Default config created successfully")
        
        # Custom config
        config = BacktestConfig(
            initial_cash=50000,
            commission=0.002,
            position_sizing="percentage",
            position_size_value=0.95
        )
        assert config.initial_cash == 50000
        assert config.position_size_value == 0.95
        print("✓ Custom config created successfully")
        
        # Invalid config should raise error
        try:
            config = BacktestConfig(initial_cash=-1000)
            print("✗ Invalid config should have raised error")
            return False
        except ValueError:
            print("✓ Invalid config correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from tradingagents.backtesting.utils import (
            parse_date, calculate_position_size, format_currency, format_percentage
        )
        from datetime import datetime
        
        # Test parse_date
        date = parse_date("2024-01-15")
        assert isinstance(date, datetime)
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
        print("✓ parse_date works correctly")
        
        # Test calculate_position_size
        size = calculate_position_size(
            current_value=100000,
            price=150,
            sizing_method="percentage",
            sizing_value=0.95
        )
        assert size > 0
        assert size == int((100000 * 0.95) / 150)
        print("✓ calculate_position_size works correctly")
        
        # Test format functions
        assert format_currency(1234.56) == "$1,234.56"
        assert format_percentage(0.1234, 2) == "12.34%"
        print("✓ Format functions work correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Utils test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backtest_engine_initialization():
    """Test BacktestEngine can be initialized."""
    print("\nTesting BacktestEngine initialization...")
    
    try:
        from tradingagents.backtesting import BacktestEngine, BacktestConfig
        
        config = BacktestConfig(initial_cash=10000)
        
        engine = BacktestEngine(
            ticker="AAPL",
            start_date="2024-01-01",
            end_date="2024-01-31",
            initial_cash=10000,
            config=config,
            debug=False
        )
        
        assert engine.ticker == "AAPL"
        assert engine.start_date == "2024-01-01"
        assert engine.end_date == "2024-01-31"
        print("✓ BacktestEngine initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Engine initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running Backtesting Framework Tests")
    print("="*60)
    
    tests = [
        test_imports,
        test_config,
        test_utils,
        test_backtest_engine_initialization,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("="*60)
    
    if all(results):
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed")
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)

