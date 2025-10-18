# TradingAgents Backtesting Guide

## Overview

The TradingAgents backtesting framework allows you to test your trading strategies over historical periods with realistic trading constraints, comprehensive performance metrics, and integrated agent learning capabilities.

## Table of Contents

- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Position Sizing Strategies](#position-sizing-strategies)
- [Risk Management](#risk-management)
- [Performance Metrics](#performance-metrics)
- [Agent Learning](#agent-learning)
- [Multi-Ticker Backtesting](#multi-ticker-backtesting)
- [Visualization](#visualization)
- [Advanced Usage](#advanced-usage)

## Quick Start

### CLI Interface

The simplest way to run a backtest:

```bash
python -m cli.main backtest run
```

This launches an interactive interface that guides you through:

1. Ticker selection
2. Date range
3. Capital settings
4. Position sizing strategy
5. Trading costs
6. Risk management parameters
7. Analyst configuration
8. LLM settings

### Python API

For programmatic control:

```python
from tradingagents.backtesting import BacktestEngine
from dotenv import load_dotenv

load_dotenv()

engine = BacktestEngine(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    initial_cash=100000
)

results = engine.run()
results.print_metrics()
```

## Configuration

### BacktestConfig

The `BacktestConfig` class controls all backtesting parameters:

```python
from tradingagents.backtesting import BacktestConfig

config = BacktestConfig(
    # Capital settings
    initial_cash=100000.0,

    # Trading costs
    commission=0.001,  # 0.1% per trade
    slippage=0.0005,   # 0.05% slippage

    # Position sizing
    position_sizing="percentage",  # Options: "percentage", "fixed", "all_in"
    position_size_value=0.95,      # 95% of portfolio

    # Risk management
    max_position_size=None,  # Maximum position as % of portfolio
    stop_loss=0.10,         # 10% stop loss
    take_profit=0.20,       # 20% take profit

    # Learning
    enable_reflection=True,
    reflection_on_close_only=True,

    # Benchmark
    benchmark_ticker="SPY",
    risk_free_rate=0.02,  # Annual risk-free rate
)
```

### TradingAgents Configuration

Customize the agent behavior:

```python
from tradingagents.default_config import DEFAULT_CONFIG

ta_config = DEFAULT_CONFIG.copy()
ta_config["quick_think_llm"] = "gpt-4o-mini"
ta_config["deep_think_llm"] = "gpt-4o-mini"
ta_config["max_debate_rounds"] = 2
ta_config["max_risk_discuss_rounds"] = 2

engine = BacktestEngine(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    ta_config=ta_config,
    selected_analysts=["market", "news", "fundamentals"]
)
```

## Position Sizing Strategies

### Percentage-Based

Use a fixed percentage of current portfolio value:

```python
config = BacktestConfig(
    position_sizing="percentage",
    position_size_value=0.95  # 95% of portfolio
)
```

### Fixed Dollar Amount

Trade a fixed dollar amount per signal:

```python
config = BacktestConfig(
    position_sizing="fixed",
    position_size_value=50000  # $50,000 per trade
)
```

### All-In

Use 100% of available capital:

```python
config = BacktestConfig(
    position_sizing="all_in",
)
```

## Risk Management

### Stop Loss

Automatically exit positions when losses exceed a threshold:

```python
config = BacktestConfig(
    stop_loss=0.10  # Exit if position drops 10%
)
```

### Take Profit

Lock in gains when they reach a target:

```python
config = BacktestConfig(
    take_profit=0.20  # Exit if position gains 20%
)
```

### Maximum Position Size

Cap the maximum position size:

```python
config = BacktestConfig(
    max_position_size=0.90  # Never exceed 90% of portfolio
)
```

## Performance Metrics

The `BacktestResults` object provides comprehensive metrics:

### Returns

- **Total Return**: Overall portfolio return
- **Annualized Return**: Return normalized to annual basis
- **Monthly/Yearly Returns**: Period-specific breakdowns

### Risk Metrics

- **Sharpe Ratio**: Risk-adjusted return (higher is better)
- **Sortino Ratio**: Like Sharpe, but only penalizes downside volatility
- **Max Drawdown**: Largest peak-to-trough decline
- **Volatility**: Standard deviation of returns (annualized)
- **Calmar Ratio**: Annualized return / Max drawdown

### Trade Statistics

- **Number of Trades**: Total completed trades
- **Win Rate**: Percentage of profitable trades
- **Average Win/Loss**: Mean profit of winning/losing trades
- **Profit Factor**: Total wins / Total losses
- **Best/Worst Trade**: Largest gain and loss

### Benchmark Comparison

- **Benchmark Return**: Buy-and-hold return for comparison
- **Excess Return**: Strategy return - Benchmark return
- **Alpha**: Risk-adjusted excess return

### Accessing Metrics

```python
results = engine.run()

# Print all metrics
results.print_metrics()

# Access specific metrics
print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
print(f"Win Rate: {results.win_rate:.2%}")
print(f"Max Drawdown: {results.max_drawdown_pct:.2%}")

# Export to dictionary
metrics_dict = results.to_dict()

# Save to JSON
results.to_json("metrics.json")

# Export trades to CSV
results.to_csv("trades.csv")
```

## Agent Learning

The backtesting framework integrates with TradingAgents' reflection system:

```python
config = BacktestConfig(
    enable_reflection=True,         # Enable learning
    reflection_on_close_only=True,  # Learn only when trades close
)
```

### How It Works

1. **Trade Execution**: Agent makes a BUY/SELL/HOLD decision
2. **Position Opened**: Trade is executed at current market price
3. **Position Closed**: When the opposite signal occurs or risk limits hit
4. **Reflection**: Agent analyzes the actual return and updates its memory
5. **Learning**: Future decisions incorporate lessons from past trades

### Benefits

- Agents improve over the backtest period
- Mistakes are remembered and avoided
- Successful patterns are reinforced
- More realistic simulation of adaptive trading

### Disabling Learning

For faster initial runs or baseline comparisons:

```python
config = BacktestConfig(
    enable_reflection=False
)
```

## Multi-Ticker Backtesting

Test strategies across multiple stocks:

```python
from tradingagents.backtesting import MultiTickerBacktestEngine

engine = MultiTickerBacktestEngine(
    tickers=["AAPL", "GOOGL", "MSFT", "AMZN"],
    start_date="2023-01-01",
    end_date="2024-01-01",
    initial_cash=400000,        # Total capital
    cash_per_ticker=100000,     # Per-ticker allocation
    config=config,
)

results = engine.run()

# Access individual results
for ticker, result in results.items():
    print(f"{ticker}: {result.total_return:.2%}")

# Save all results
engine.save_all_results("results/backtests/portfolio")
```

### Portfolio Summary

The multi-ticker engine automatically calculates:

- Total portfolio return
- Individual ticker performance
- Best/worst performers
- Aggregate statistics

## Visualization

### Automatic Plots

Generate all visualizations at once:

```python
engine.plot("output_directory/plots")
```

This creates:

- `equity_curve.png`: Portfolio value over time with benchmark
- `trades.png`: Price chart with trade markers
- `monthly_returns.png`: Monthly returns heatmap
- `dashboard.png`: Comprehensive metrics dashboard

### Individual Plots

```python
from tradingagents.backtesting import BacktestVisualizer

visualizer = BacktestVisualizer(results)

# Equity curve with drawdown
visualizer.plot_equity_curve(save_path="equity.png")

# Trade markers on price chart
import yfinance as yf
price_data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")['Close']
visualizer.plot_trades(price_data, save_path="trades.png")

# Monthly returns heatmap
visualizer.plot_monthly_returns(save_path="monthly.png")

# Comprehensive dashboard
visualizer.plot_metrics_dashboard(save_path="dashboard.png")
```

## Advanced Usage

### Custom Analysis

Access detailed trade data:

```python
results = engine.run()

# Get trade history
for trade in results.trade_history:
    print(f"Entry: {trade['entry_date']} @ ${trade['entry_price']:.2f}")
    print(f"Exit: {trade['exit_date']} @ ${trade['exit_price']:.2f}")
    print(f"Return: {trade['returns']:.2%}")
    print()

# Get agent decisions
for decision in results.decisions:
    print(f"{decision['date']}: {decision['decision']} @ ${decision['price']:.2f}")

# Get agent states for analysis
for state in results.agent_states:
    print(state['market_report'])
    print(state['final_trade_decision'])
```

### Monthly/Yearly Analysis

```python
# Monthly returns
monthly = results.get_monthly_returns()
print(monthly)

# Yearly returns
yearly = results.get_yearly_returns()
print(yearly)
```

### Comparing Strategies

Run multiple backtests with different configurations:

```python
configs = [
    BacktestConfig(position_sizing="percentage", position_size_value=0.95),
    BacktestConfig(position_sizing="percentage", position_size_value=0.80),
    BacktestConfig(position_sizing="percentage", position_size_value=0.50),
]

results_list = []
for i, config in enumerate(configs):
    engine = BacktestEngine(ticker="AAPL", start_date="2023-01-01",
                          end_date="2024-01-01", config=config)
    results = engine.run()
    results_list.append(results)

# Compare results
for i, results in enumerate(results_list):
    print(f"Strategy {i+1}: {results.total_return:.2%}")
```

### CLI Comparison

Compare multiple tickers:

```bash
python -m cli.main backtest compare "AAPL,GOOGL,MSFT" -s 2023-01-01 -e 2024-01-01
```

## Best Practices

### 1. Start with Longer Periods

Test over at least 1 year of data to capture different market conditions:

```python
start_date = "2022-01-01"
end_date = "2024-01-01"
```

### 2. Use Realistic Costs

Include commissions and slippage for accurate results:

```python
config = BacktestConfig(
    commission=0.002,  # 0.2% for retail traders
    slippage=0.001,    # 0.1% slippage
)
```

### 3. Test Multiple Configurations

Run parameter sweeps to find optimal settings:

- Different analyst combinations
- Various position sizes
- Multiple debate rounds
- Different stop-loss/take-profit levels

### 4. Compare Against Benchmark

Always evaluate against buy-and-hold:

```python
print(f"Strategy: {results.total_return:.2%}")
print(f"Benchmark: {results.benchmark_total_return:.2%}")
print(f"Excess: {results.excess_return:.2%}")
```

### 5. Watch for Overfitting

If results are too good to be true, test on different time periods:

- Training period: 2022-2023
- Testing period: 2024

### 6. Account for Learning Curve

Early trades may underperform as agents learn. Consider:

- Pre-training on an earlier period
- Analyzing performance over time
- Comparing with and without reflection enabled

## Troubleshooting

### Slow Execution

Backtesting makes many API calls. To speed up:

```python
# Use fewer debate rounds
ta_config["max_debate_rounds"] = 1

# Use fewer analysts
selected_analysts = ["market", "fundamentals"]  # Drop social/news

# Disable reflection for initial runs
config = BacktestConfig(enable_reflection=False)
```

### Data Issues

If data is missing:

```python
# Check date range
print(f"Start: {start_date}, End: {end_date}")

# Verify ticker
import yfinance as yf
data = yf.download("TICKER", start=start_date, end=end_date)
print(data.head())
```

### API Rate Limits

If hitting rate limits:

```python
# Use local data vendor (if available)
ta_config["data_vendors"]["news_data"] = "local"

# Reduce API calls by caching
config = BacktestConfig(data_cache=True)
```

## Examples

See the `examples/` directory for complete working examples:

- `simple_backtest.py`: Basic single-ticker example
- `portfolio_backtest.py`: Multi-ticker portfolio with risk management
- `advanced_backtest.py`: Custom configuration and detailed analysis

Run any example:

```bash
python examples/simple_backtest.py
```

## Next Steps

- Experiment with different analyst combinations
- Test various position sizing strategies
- Compare performance across multiple tickers
- Analyze agent decisions to understand reasoning
- Export results for external analysis

For more information, see the main [README](../README.md) or join the [Tauric Research community](https://tauric.ai/).
