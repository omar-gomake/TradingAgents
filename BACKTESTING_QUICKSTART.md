# Backtesting Quick Start Guide

## Installation

The backtesting framework has been successfully implemented! To use it, you need to install the updated dependencies:

```bash
# Make sure you're in the TradingAgents directory
cd /Users/omarsabbah/Desktop/TradingAgents

# Install/update dependencies
pip install -r requirements.txt
```

## Verify Installation

Test that everything is installed correctly:

```bash
# Test imports
python3 -c "from tradingagents.backtesting import BacktestEngine; print('✓ Backtesting module ready!')"

# Test CLI
python -m cli.main --help
```

You should see `backtest` listed as a command.

## Usage

### Option 1: Interactive CLI (Recommended for First Time)

```bash
python -m cli.main backtest run
```

This will guide you through:

- Ticker selection
- Date range
- Capital settings
- Position sizing
- Risk management
- Analyst configuration
- And more...

### Option 2: Command Line (Quick)

```bash
# Single ticker backtest
python -m cli.main backtest run -t AAPL -s 2023-01-01 -e 2024-01-01 -c 100000

# Compare multiple tickers
python -m cli.main backtest compare "AAPL,GOOGL,MSFT" -s 2023-01-01 -e 2024-01-01
```

### Option 3: Python API (Most Flexible)

```bash
# Run the simple example
python examples/simple_backtest.py

# Run the portfolio example
python examples/portfolio_backtest.py

# Run the advanced example
python examples/advanced_backtest.py
```

Or write your own:

```python
from tradingagents.backtesting import BacktestEngine, BacktestConfig
from dotenv import load_dotenv

load_dotenv()

# Configure backtest
config = BacktestConfig(
    initial_cash=100000,
    commission=0.001,
    position_sizing="percentage",
    position_size_value=0.95,
    stop_loss=0.10,
    take_profit=0.20,
    enable_reflection=True,
)

# Run backtest
engine = BacktestEngine(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    config=config,
    selected_analysts=["market", "news", "fundamentals"]
)

results = engine.run()
results.print_metrics()

# Save results
engine.save_results("results/backtests/AAPL")
engine.plot("results/backtests/AAPL/plots")
```

## What You Get

After running a backtest, you'll get:

### Performance Metrics

- Total Return, Annualized Return
- Sharpe Ratio, Sortino Ratio, Calmar Ratio
- Maximum Drawdown, Volatility
- Win Rate, Profit Factor
- Average Win/Loss, Best/Worst Trade
- Benchmark Comparison (vs SPY)

### Visualizations (in `/plots` directory)

- `equity_curve.png` - Portfolio value over time
- `trades.png` - Price chart with buy/sell markers
- `monthly_returns.png` - Monthly performance heatmap
- `dashboard.png` - Comprehensive performance dashboard

### Data Files

- `metrics.json` - All performance metrics
- `trades.csv` - Detailed trade history
- `decisions.csv` - Agent decisions for each day
- `portfolio_values.csv` - Daily portfolio values

## Troubleshooting

### Issue: "Got unexpected extra arguments (backtest run)"

**Solution:** Install missing dependencies:

```bash
pip install typer numpy matplotlib python-dotenv
```

### Issue: "No module named 'tradingagents'"

**Solution:** Make sure you're running from the project root:

```bash
cd /Users/omarsabbah/Desktop/TradingAgents
python -m cli.main backtest run
```

### Issue: Backtest is too slow

**Solution:** Use fewer debate rounds and analysts:

```python
ta_config = DEFAULT_CONFIG.copy()
ta_config["max_debate_rounds"] = 1  # Faster
config = BacktestConfig(enable_reflection=False)  # Even faster
selected_analysts = ["market", "fundamentals"]  # Fewer analysts
```

### Issue: API rate limits

**Solution:** The framework uses yfinance for price data (no limits) and Alpha Vantage for fundamentals (60 req/min for TradingAgents users). If you hit limits:

- Backtest shorter periods
- Use fewer tickers
- Add delays between requests

## Key Features

### 1. **Agent Learning**

Agents improve over time during the backtest by learning from actual returns:

```python
config = BacktestConfig(
    enable_reflection=True,  # Agents learn from mistakes
    reflection_on_close_only=True  # Learn only when trades close
)
```

### 2. **Position Sizing**

Three strategies available:

- **Percentage**: Use X% of portfolio (e.g., 95%)
- **Fixed**: Trade fixed dollar amount (e.g., $50,000)
- **All-in**: Use 100% of capital

### 3. **Risk Management**

Automatic stop-loss and take-profit:

```python
config = BacktestConfig(
    stop_loss=0.10,      # Exit if down 10%
    take_profit=0.20,    # Exit if up 20%
)
```

### 4. **Multi-Ticker Portfolio**

Test multiple stocks simultaneously:

```python
from tradingagents.backtesting import MultiTickerBacktestEngine

engine = MultiTickerBacktestEngine(
    tickers=["AAPL", "GOOGL", "MSFT"],
    start_date="2023-01-01",
    end_date="2024-01-01",
    initial_cash=300000,
)

results = engine.run()
```

## Next Steps

1. **Try the examples**: Run `python examples/simple_backtest.py`
2. **Read the docs**: See `docs/BACKTESTING.md` for comprehensive guide
3. **Experiment**: Try different analysts, position sizes, and tickers
4. **Analyze results**: Check the generated plots and metrics

## Documentation

- **Quick Start**: This file
- **Comprehensive Guide**: `docs/BACKTESTING.md`
- **API Reference**: See docstrings in `tradingagents/backtesting/`
- **Examples**: `examples/simple_backtest.py`, `portfolio_backtest.py`, `advanced_backtest.py`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

## Support

- GitHub Issues: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- Discord: [TradingResearch Community](https://discord.com/invite/hk9PGKShPK)
- Paper: [arXiv:2412.20138](https://arxiv.org/abs/2412.20138)

---

**Happy Backtesting! 📈**
