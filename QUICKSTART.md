# TradingAgents Backtesting - Quick Start

## ✅ Setup Complete!

The backtesting framework is now fully installed and working!

## How to Use

### Step 1: Activate Virtual Environment

```bash
cd /Users/omarsabbah/Desktop/TradingAgents
source venv/bin/activate
```

### Step 2: Run Backtesting

Now you have several options:

#### Interactive CLI (Recommended)

```bash
python -m cli.main backtest run
```

This will guide you through all the options interactively.

#### Command-Line Mode

```bash
# Simple backtest
python -m cli.main backtest run -t AAPL -s 2023-01-01 -e 2024-01-01 -c 100000

# Compare multiple tickers
python -m cli.main backtest compare "AAPL,GOOGL,MSFT" -s 2023-01-01 -e 2024-01-01
```

#### Run Examples

```bash
# Simple example
python examples/simple_backtest.py

# Portfolio example
python examples/portfolio_backtest.py

# Advanced example
python examples/advanced_backtest.py
```

## Available Commands

```bash
# See all commands
python -m cli.main --help

# See backtest options
python -m cli.main backtest --help

# See run command options
python -m cli.main backtest run --help

# See compare command options
python -m cli.main backtest compare --help
```

## What You Get

After running a backtest, you'll find in `results/backtests/`:

- **metrics.json** - All performance metrics
- **trades.csv** - Detailed trade history
- **decisions.csv** - Agent decisions
- **portfolio_values.csv** - Daily portfolio values
- **plots/** directory with:
  - equity_curve.png
  - trades.png
  - monthly_returns.png
  - dashboard.png

## Example Output

```
Total Return: 15.23%
Annualized Return: 14.87%
Sharpe Ratio: 1.45
Max Drawdown: -8.32%
Win Rate: 65.2%
Number of Trades: 23
Profit Factor: 2.14
```

## Environment Variables

Make sure you have your API keys set:

```bash
export OPENAI_API_KEY="your-key"
export ALPHA_VANTAGE_API_KEY="your-key"
```

Or create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-key" > .env
echo "ALPHA_VANTAGE_API_KEY=your-key" >> .env
```

## Documentation

- **Quick Start**: This file
- **Complete Guide**: `docs/BACKTESTING.md`
- **Installation Help**: `INSTALL_INSTRUCTIONS.md`
- **Technical Details**: `IMPLEMENTATION_SUMMARY.md`

## Troubleshooting

### If commands don't work:

1. **Make sure virtual environment is activated:**

   ```bash
   source venv/bin/activate
   ```

   You should see `(venv)` in your terminal prompt.

2. **Check Python version:**

   ```bash
   python --version  # Should be 3.10+
   ```

3. **Reinstall if needed:**
   ```bash
   pip install -r requirements.txt
   ```

## Next Steps

1. ✅ Virtual environment is set up
2. ✅ All dependencies installed
3. ✅ Backtest command working
4. 🚀 Ready to run your first backtest!

Try it now:

```bash
source venv/bin/activate
python -m cli.main backtest run
```

Happy backtesting! 📈
